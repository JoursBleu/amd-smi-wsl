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

import functools
import os
import re
import subprocess
from dataclasses import dataclass, field

from . import _device_map as dm


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
    if not (getattr(torch.version, "hip", None) and torch.cuda.is_available()):
        return []

    gpus: list[GpuInfo] = []
    for i in range(torch.cuda.device_count()):
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
            if uuid is not None:
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


def _windows_probe() -> list[dict]:
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
            "driver_date": str(entry.get("DriverDate") or ""),
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


def available() -> bool:
    """True if at least one ROCm/HIP GPU is visible via torch."""
    return len(discover()) > 0


def env_disabled() -> bool:
    return os.environ.get("AMDSMI_WSL_DISABLE", "").strip().lower() in {
        "1",
        "true",
        "yes",
    }
