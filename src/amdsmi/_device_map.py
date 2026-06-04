"""Static gfx-arch -> GPU metadata fallback table.

On WSL2 the native ``amdsmi`` cannot talk to KFD, and some asic fields
(PCI device id, marketing name, memory type) are not exposed by the HIP
runtime.  When the Windows-interop probe also fails to provide a value,
this table supplies a best-effort default keyed by the GCN architecture
name reported by ``torch.cuda`` (e.g. ``gfx1151``).

Values mirror the public AMD product / PCI-ID tables.  ``device_id`` is a
hex string to match vLLM's ``_ROCM_DEVICE_ID_NAME_MAP`` convention; it is
only used when the real PCI id cannot be read from the Windows host.
"""

from __future__ import annotations

# gfx arch -> metadata.  Keep keys lowercase, arch only (no feature flags).
GFX_INFO: dict[str, dict[str, object]] = {
    # Strix Halo APU (Radeon 8050S / 8060S) — the primary WSL2 target.
    "gfx1151": {
        "market_name": "AMD Radeon(TM) 8060S Graphics",
        "device_id": "0x1586",
        "vram_type": "LPDDR5",
        "num_compute_units": 40,
    },
    # RDNA3 discrete.
    "gfx1100": {
        "market_name": "AMD Radeon RX 7900 XTX",
        "device_id": "0x744c",
        "vram_type": "GDDR6",
        "num_compute_units": 96,
    },
    "gfx1101": {
        "market_name": "AMD Radeon RX 7800 XT",
        "device_id": "0x747e",
        "vram_type": "GDDR6",
        "num_compute_units": 60,
    },
    "gfx1102": {
        "market_name": "AMD Radeon RX 7600",
        "device_id": "0x7480",
        "vram_type": "GDDR6",
        "num_compute_units": 32,
    },
    # RDNA4 discrete.
    "gfx1200": {
        "market_name": "AMD Radeon RX 9060 XT",
        "device_id": "0x7551",
        "vram_type": "GDDR6",
        "num_compute_units": 32,
    },
    "gfx1201": {
        "market_name": "AMD Radeon RX 9070 XT",
        "device_id": "0x7550",
        "vram_type": "GDDR6",
        "num_compute_units": 64,
    },
    # CDNA datacenter (unlikely on WSL2 but kept for completeness).
    "gfx90a": {
        "market_name": "AMD Instinct MI250X",
        "device_id": "0x7408",
        "vram_type": "HBM2E",
        "num_compute_units": 110,
    },
    "gfx942": {
        "market_name": "AMD Instinct MI300X",
        "device_id": "0x74a1",
        "vram_type": "HBM3",
        "num_compute_units": 304,
    },
    "gfx950": {
        "market_name": "AMD Instinct MI350X",
        "device_id": "0x7550",
        "vram_type": "HBM3E",
        "num_compute_units": 256,
    },
}

AMD_VENDOR_ID = 0x1002
AMD_VENDOR_NAME = "Advanced Micro Devices, Inc. [AMD/ATI]"


def normalize_arch(gcn_arch_name: str | None) -> str:
    """Strip feature flags: ``gfx1151:sramecc+:xnack-`` -> ``gfx1151``."""
    if not gcn_arch_name:
        return ""
    return gcn_arch_name.split(":", 1)[0].strip().lower()


def lookup(gcn_arch_name: str | None) -> dict[str, object]:
    return dict(GFX_INFO.get(normalize_arch(gcn_arch_name), {}))
