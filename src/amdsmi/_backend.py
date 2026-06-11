"""Best-effort GPU discovery for WSL2 / Windows.

Native ``amdsmi`` relies on the Linux KFD driver (``/dev/kfd``) which does
not exist inside WSL2, where the AMD GPU is exposed through DirectX
para-virtualization (``/dev/dxg``).  This module reconstructs the subset of
information that the SMI surface needs from two sources that *do* work in
that environment:

1. The HIP runtime via ``torch.cuda`` — always available wherever vLLM runs
   (device count, name, GCN arch, total VRAM, compute units, UUID).
2. The Windows host via WSL interop (``powershell.exe`` /
   ``Get-CimInstance Win32_VideoController``) — supplies the real PCI device
   id, subsystem id, revision and driver version/date.

Anything that still cannot be resolved falls back to the static
``_device_map`` table.  Every probe is wrapped so that discovery never
raises; missing fields are simply left unset.
"""

from __future__ import annotations

import contextlib
import datetime
import functools
import os
import re
import subprocess
import threading
import warnings
from dataclasses import dataclass, field

from . import _device_map as dm

# Re-entrancy guard (thread-local).  On torch ROCm builds, torch.cuda's device
# enumeration resolves the device count by calling amdsmi.amdsmi_init() +
# amdsmi_get_processor_handles().  Because this package *is* ``amdsmi``, probing
# torch from inside discovery would recurse straight back into us.  While a
# probe is in flight we set ``_reentry.active`` so the re-entrant
# ``amdsmi_init()`` raises (see ``_interface.amdsmi_init``) and torch falls back
# to its native HIP device count instead of recursing forever.
_reentry = threading.local()


def is_probing() -> bool:
    """True while ``_torch_probe`` is calling into ``torch.cuda``."""
    return bool(getattr(_reentry, "active", False))


@contextlib.contextmanager
def reentry_guard():
    """Mark a torch.cuda call in flight so any re-entrant amdsmi call coming
    back from torch (device-count or telemetry on ROCm route through amdsmi)
    short-circuits instead of recursing."""
    prev = getattr(_reentry, "active", False)
    _reentry.active = True
    try:
        yield
    finally:
        _reentry.active = prev


def _is_degenerate_uuid(uuid: str) -> bool:
    """torch reports a placeholder UUID on WSL2 (all-zero / single repeated
    nibble, e.g. ``66666666-6666-...``). Treat those as absent so a stable id
    is synthesized instead."""
    if not uuid:
        return True
    hexed = uuid.replace("-", "").replace("GPU", "").strip().lower()
    return len(set(hexed)) <= 1


def _parse_wmi_date(raw) -> str:
    """WMI/CIM serializes dates as ``/Date(1771286400000)/`` (ms since epoch,
    optional ``+0000`` offset). Return a clean ``YYYY-MM-DD`` string."""
    if not raw:
        return ""
    m = re.search(r"/Date\((-?\d+)", str(raw))
    if not m:
        return str(raw)
    try:
        return datetime.datetime.fromtimestamp(
            int(m.group(1)) / 1000.0, datetime.timezone.utc
        ).strftime("%Y-%m-%d")
    except Exception:
        return ""


@dataclass
class GpuInfo:
    index: int
    name: str = ""
    gcn_arch: str = ""               # normalized, e.g. "gfx1151"
    raw_gcn_arch: str = ""           # as torch reports it
    total_memory: int = 0            # bytes
    num_compute_units: int = 0
    uuid: str = ""
    major: int = 0
    minor: int = 0
    # Filled from Windows interop / static map.
    device_id: int = 0               # PCI device id, e.g. 0x1586
    vendor_id: int = dm.AMD_VENDOR_ID
    subsystem_id: int = 0
    subsystem_device_id: int = 0
    rev_id: int = 0
    market_name: str = ""
    vram_type: str = ""
    driver_version: str = ""
    driver_date: str = ""
    bdf: str = ""                    # domain:bus:device.function
    extra: dict = field(default_factory=dict)


def is_wsl() -> bool:
    try:
        with open("/proc/version", "r") as fh:
            v = fh.read().lower()
        return "microsoft" in v or "wsl" in v
    except OSError:
        return False


def _torch_probe() -> list[GpuInfo]:
    try:
        import torch
    except Exception:
        return []
    if not getattr(torch.version, "hip", None):
        return []

    # Guard against the torch<->amdsmi device-count recursion described above.
    if is_probing():
        return []
    try:
        # torch may emit "Can't initialize amdsmi" here as it falls back to
        # its native HIP device count -- that fallback is exactly what we want,
        # so silence the cosmetic warning.
        with reentry_guard(), warnings.catch_warnings():
            warnings.simplefilter("ignore")
            if not torch.cuda.is_available():
                return []
            device_count = torch.cuda.device_count()
    except Exception:
        return []

    gpus: list[GpuInfo] = []
    for i in range(device_count):
        info = GpuInfo(index=i)
        try:
            props = torch.cuda.get_device_properties(i)
        except Exception:
            props = None
        try:
            info.name = torch.cuda.get_device_name(i)
        except Exception:
            info.name = ""
        if props is not None:
            raw = getattr(props, "gcnArchName", "") or ""
            info.raw_gcn_arch = raw
            info.gcn_arch = dm.normalize_arch(raw)
            info.total_memory = int(getattr(props, "total_memory", 0) or 0)
            info.num_compute_units = int(
                getattr(props, "multi_processor_count", 0) or 0
            )
            info.major = int(getattr(props, "major", 0) or 0)
            info.minor = int(getattr(props, "minor", 0) or 0)
            uuid = getattr(props, "uuid", None)
            if uuid is not None and not _is_degenerate_uuid(str(uuid)):
                info.uuid = str(uuid)
        gpus.append(info)
    return gpus


# PNPDeviceID looks like: PCI\VEN_1002&DEV_1586&SUBSYS_12345678&REV_C1\...
_PNP_RE = re.compile(
    r"VEN_(?P<ven>[0-9A-Fa-f]{4})"
    r"&DEV_(?P<dev>[0-9A-Fa-f]{4})"
    r"(?:&SUBSYS_(?P<subsys>[0-9A-Fa-f]{8}))?"
    r"(?:&REV_(?P<rev>[0-9A-Fa-f]{2}))?"
)

# Persistent cache for the Windows interop probe (static PCI metadata).
_WIN_PROBE_CACHE: "list[dict] | None" = None


def _windows_probe() -> list[dict]:
    """Query Win32_VideoController through WSL interop, cached persistently.

    PCI metadata is static for the machine, and vLLM's ``with_amdsmi_context``
    resets the discovery cache around *every* call -- so without a persistent
    cache here we would spawn powershell.exe repeatedly (~1s each).
    """
    global _WIN_PROBE_CACHE
    if _WIN_PROBE_CACHE is not None:
        return _WIN_PROBE_CACHE
    _WIN_PROBE_CACHE = _windows_probe_uncached()
    return _WIN_PROBE_CACHE


def _windows_probe_uncached() -> list[dict]:
    """Query Win32_VideoController through WSL interop. Best-effort."""
    if not is_wsl():
        return []
    pwsh = None
    for cand in ("powershell.exe", "pwsh.exe"):
        # We cannot easily `which`, just try to run it.
        pwsh = cand
        break
    cmd = (
        "Get-CimInstance Win32_VideoController | "
        "Select-Object Name,PNPDeviceID,DriverVersion,DriverDate,"
        "AdapterRAM,AdapterCompatibility | ConvertTo-Json -Compress"
    )
    try:
        out = subprocess.run(
            [pwsh, "-NoProfile", "-NonInteractive", "-Command", cmd],
            capture_output=True,
            text=True,
            timeout=15,
        )
    except Exception:
        return []
    if out.returncode != 0 or not out.stdout.strip():
        return []
    try:
        import json

        data = json.loads(out.stdout)
    except Exception:
        return []
    if isinstance(data, dict):
        data = [data]
    adapters: list[dict] = []
    for entry in data:
        compat = (entry.get("AdapterCompatibility") or "")
        pnp = entry.get("PNPDeviceID") or ""
        m = _PNP_RE.search(pnp)
        ven = int(m.group("ven"), 16) if m else 0
        # Keep only AMD adapters.
        if ven != dm.AMD_VENDOR_ID and "AMD" not in compat.upper() and "ATI" not in compat.upper():
            continue
        rec: dict = {
            "name": entry.get("Name") or "",
            "vendor_id": ven or dm.AMD_VENDOR_ID,
            "driver_version": entry.get("DriverVersion") or "",
            "driver_date": _parse_wmi_date(entry.get("DriverDate")),
            "adapter_ram": int(entry.get("AdapterRAM") or 0),
        }
        if m:
            rec["device_id"] = int(m.group("dev"), 16)
            if m.group("subsys"):
                subsys = int(m.group("subsys"), 16)
                rec["subsystem_id"] = subsys & 0xFFFF
                rec["subsystem_device_id"] = (subsys >> 16) & 0xFFFF
            if m.group("rev"):
                rec["rev_id"] = int(m.group("rev"), 16)
        adapters.append(rec)
    return adapters


def _merge(gpus: list[GpuInfo], adapters: list[dict]) -> None:
    for i, info in enumerate(gpus):
        # 1) Windows interop (positional match by AMD adapter order).
        win = adapters[i] if i < len(adapters) else {}
        if win.get("device_id"):
            info.device_id = win["device_id"]
        info.vendor_id = win.get("vendor_id", info.vendor_id)
        info.subsystem_id = win.get("subsystem_id", info.subsystem_id)
        info.subsystem_device_id = win.get(
            "subsystem_device_id", info.subsystem_device_id
        )
        info.rev_id = win.get("rev_id", info.rev_id)
        info.driver_version = win.get("driver_version", "")
        info.driver_date = win.get("driver_date", "")
        if win.get("name") and not info.market_name:
            info.market_name = win["name"]

        # 2) Static map fallback keyed on gfx arch.
        mp = dm.lookup(info.gcn_arch)
        if not info.market_name:
            info.market_name = str(mp.get("market_name") or info.name or "")
        if not info.device_id and mp.get("device_id"):
            info.device_id = int(str(mp["device_id"]), 16)
        if not info.vram_type:
            info.vram_type = str(mp.get("vram_type") or "")
        if not info.num_compute_units and mp.get("num_compute_units"):
            info.num_compute_units = int(mp["num_compute_units"])  # type: ignore[arg-type]

        # 3) Synthesize a stable BDF if unknown (WSL has no real PCI bus).
        if not info.bdf:
            info.bdf = "0000:%02x:00.0" % info.index
        # 4) Synthesize a UUID if torch did not provide one.
        if not info.uuid:
            info.uuid = "GPU-%016x" % (
                (info.device_id << 32) | (0xFFFFFFFF & hash((info.gcn_arch, info.index)))
            )


@functools.lru_cache(maxsize=1)
def discover() -> tuple[GpuInfo, ...]:
    gpus = _torch_probe()
    if not gpus:
        return tuple()
    try:
        adapters = _windows_probe()
    except Exception:
        adapters = []
    _merge(gpus, adapters)
    return tuple(gpus)


def reset_cache() -> None:
    discover.cache_clear()


def reset_windows_probe_cache() -> None:
    """Drop the persistent Windows-interop cache (mainly for tests)."""
    global _WIN_PROBE_CACHE
    _WIN_PROBE_CACHE = None


def available() -> bool:
    """True if at least one ROCm/HIP GPU is visible via torch."""
    return len(discover()) > 0


def env_disabled() -> bool:
    return os.environ.get("AMDSMI_WSL_DISABLE", "").strip().lower() in {
        "1",
        "true",
        "yes",
    }
