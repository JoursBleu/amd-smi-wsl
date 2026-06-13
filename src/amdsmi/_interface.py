"""WSL2 / Windows re-implementation of the ``amdsmi`` Python API.

Every public ``amdsmi_*`` function from the upstream binding is defined here.
The subset that can be satisfied from the HIP runtime + Windows interop is
implemented for real; everything else raises
``AmdSmiLibraryException(AMDSMI_STATUS_NOT_SUPPORTED)`` — exactly the behaviour
the native library exhibits for unsupported features, so callers that already
guard against it keep working unchanged.
"""

from __future__ import annotations

from typing import Any

from . import _backend as backend
from . import _constants as C
from . import _device_map as dm
from ._enums import (
    AmdSmiClkType,
    AmdSmiInitFlags,
    AmdSmiLinkType,
    AmdSmiMemoryType,
    AmdSmiProcessorType,
    AmdSmiTemperatureMetric,
    AmdSmiTemperatureType,
)
from ._exceptions import (
    AmdSmiException,
    AmdSmiLibraryException,
    AmdSmiParameterException,
)
from ._handles import CpuHandle, GpuHandle, SocketHandle

__version__ = "0.3.0"

_initialized = False


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def _not_supported(name: str):
    raise AmdSmiLibraryException(C.AMDSMI_STATUS_NOT_SUPPORTED)


def _pad_hex(value: int, width: int) -> str:
    """Format an int as a lowercase ``0x``-prefixed string, zero-padded to
    ``width`` hex digits -- matching the upstream amdsmi output convention
    (e.g. ``0x1586``, ``0xc1``)."""
    try:
        return "0x" + format(int(value), "0{}x".format(width))
    except Exception:
        return "0x" + "0" * width


def _require_init() -> None:
    if not _initialized:
        raise AmdSmiLibraryException(C.AMDSMI_STATUS_NOT_INIT)


def _gpu(handle: Any) -> backend.GpuInfo:
    """Resolve a handle to its discovered GpuInfo."""
    _require_init()
    if not isinstance(handle, GpuHandle):
        raise AmdSmiParameterException(handle, GpuHandle)
    gpus = backend.discover()
    if handle.index >= len(gpus):
        raise AmdSmiLibraryException(C.AMDSMI_STATUS_NOT_FOUND)
    return gpus[handle.index]


def _torch():
    try:
        import torch

        return torch
    except Exception:
        return None


# --------------------------------------------------------------------------- #
# init / shutdown
# --------------------------------------------------------------------------- #
def amdsmi_init(flag=AmdSmiInitFlags.INIT_AMD_GPUS):
    global _initialized
    if backend.env_disabled():
        raise AmdSmiLibraryException(C.AMDSMI_STATUS_NOT_SUPPORTED)
    if backend.is_probing():
        # Re-entrant call triggered by torch's own device-count resolution
        # (torch ROCm counts devices via amdsmi).  Raise an AmdSmiException so
        # torch falls back to its native HIP device count instead of recursing
        # back into this package forever.
        raise AmdSmiLibraryException(C.AMDSMI_STATUS_NOT_SUPPORTED)
    backend.reset_cache()
    if not backend.available():
        # No HIP GPU visible -> behave like the native lib with no driver.
        raise AmdSmiLibraryException(C.AMDSMI_STATUS_DRIVER_NOT_LOADED)
    _initialized = True


def amdsmi_shut_down():
    global _initialized
    _initialized = False
    backend.reset_cache()


# --------------------------------------------------------------------------- #
# enumeration
# --------------------------------------------------------------------------- #
def amdsmi_get_processor_handles():
    _require_init()
    return [GpuHandle(i) for i in range(len(backend.discover()))]


def amdsmi_get_socket_handles():
    _require_init()
    return [SocketHandle(i) for i in range(len(backend.discover()))]


def amdsmi_get_socket_info(socket_handle):
    _require_init()
    if not isinstance(socket_handle, SocketHandle):
        raise AmdSmiParameterException(socket_handle, SocketHandle)
    return f"socket-{socket_handle.index}"


def amdsmi_get_processor_handles_by_type(socket_handle, processor_type):
    _require_init()
    if processor_type == AmdSmiProcessorType.AMD_GPU:
        return [GpuHandle(i) for i in range(len(backend.discover()))]
    return []


def amdsmi_get_processor_count_from_handles(processor_handles_list):
    n_gpu = sum(isinstance(h, GpuHandle) for h in processor_handles_list)
    n_cpu = sum(isinstance(h, CpuHandle) for h in processor_handles_list)
    return {
        "num_gpu_processors": n_gpu,
        "num_cpu_processors": n_cpu,
        "num_cpu_cores": 0,
    }


def amdsmi_get_processor_type(processor_handle):
    if isinstance(processor_handle, GpuHandle):
        return {"processor_type": AmdSmiProcessorType.AMD_GPU.name}
    if isinstance(processor_handle, CpuHandle):
        return {"processor_type": AmdSmiProcessorType.AMD_CPU.name}
    raise AmdSmiParameterException(processor_handle, GpuHandle)


def amdsmi_get_processor_handle_from_bdf(bdf):
    _require_init()
    for i, g in enumerate(backend.discover()):
        if g.bdf == bdf:
            return GpuHandle(i)
    raise AmdSmiLibraryException(C.AMDSMI_STATUS_NOT_FOUND)


# --------------------------------------------------------------------------- #
# identity / asic / board / vram
# --------------------------------------------------------------------------- #
def amdsmi_get_gpu_asic_info(processor_handle):
    g = _gpu(processor_handle)
    # Identity fields are formatted as lowercase hex strings to match the
    # upstream amdsmi contract (vLLM looks ``device_id`` up in its hex-keyed
    # _ROCM_DEVICE_ID_NAME_MAP, so it must be e.g. "0x1586", not an int).
    return {
        "market_name": g.market_name or g.name or "N/A",
        "vendor_id": _pad_hex(g.vendor_id, 4) if g.vendor_id else "N/A",
        "vendor_name": dm.AMD_VENDOR_NAME.replace(",", ""),
        "subvendor_id": _pad_hex(g.subsystem_id, 4),
        "device_id": _pad_hex(g.device_id, 4) if g.device_id else "N/A",
        "rev_id": _pad_hex(g.rev_id, 2),
        "asic_serial": g.uuid,
        "oam_id": g.index,
        "num_compute_units": g.num_compute_units,
        "target_graphics_version": g.gcn_arch,
        "subsystem_id": _pad_hex(g.subsystem_id, 4),
    }


def amdsmi_get_gpu_board_info(processor_handle):
    g = _gpu(processor_handle)
    return {
        "model_number": "",
        "product_serial": g.uuid,
        "fru_id": "",
        "product_name": g.market_name or g.name,
        "manufacturer_name": "AMD",
    }


def amdsmi_get_gpu_vram_info(processor_handle):
    g = _gpu(processor_handle)
    return {
        "vram_type": g.vram_type or "UNKNOWN",
        "vram_vendor": "AMD",
        "vram_size": g.total_memory // (1024 * 1024),  # MB
        "vram_bit_width": 0,
        "vram_max_bandwidth": 0,
    }


def amdsmi_get_gpu_vram_usage(processor_handle):
    g = _gpu(processor_handle)
    torch = _torch()
    total_mb = g.total_memory // (1024 * 1024)
    used_mb = 0
    if torch is not None:
        try:
            free, total = torch.cuda.mem_get_info(g.index)
            total_mb = total // (1024 * 1024)
            used_mb = (total - free) // (1024 * 1024)
        except Exception:
            try:
                used_mb = torch.cuda.memory_reserved(g.index) // (1024 * 1024)
            except Exception:
                used_mb = 0
    return {
        "total_vram": total_mb,
        "used_vram": used_mb,
        "free_vram": max(total_mb - used_mb, 0),
    }


def amdsmi_get_gpu_memory_total(processor_handle, mem_type=AmdSmiMemoryType.VRAM):
    g = _gpu(processor_handle)
    return int(g.total_memory)


def amdsmi_get_gpu_memory_usage(processor_handle, mem_type=AmdSmiMemoryType.VRAM):
    g = _gpu(processor_handle)
    torch = _torch()
    if torch is not None:
        try:
            free, total = torch.cuda.mem_get_info(g.index)
            return int(total - free)
        except Exception:
            try:
                return int(torch.cuda.memory_reserved(g.index))
            except Exception:
                pass
    return 0


def amdsmi_get_gpu_device_uuid(processor_handle):
    return _gpu(processor_handle).uuid


def amdsmi_get_gpu_device_bdf(processor_handle):
    return _gpu(processor_handle).bdf


def amdsmi_get_gpu_bdf_id(processor_handle):
    return _gpu(processor_handle).bdf


def amdsmi_get_gpu_id(processor_handle):
    return _gpu(processor_handle).device_id


def amdsmi_get_gpu_revision(processor_handle):
    return _pad_hex(_gpu(processor_handle).rev_id, 2)


def amdsmi_get_gpu_vendor_name(processor_handle):
    _gpu(processor_handle)
    return dm.AMD_VENDOR_NAME


def amdsmi_get_gpu_subsystem_id(processor_handle):
    return _pad_hex(_gpu(processor_handle).subsystem_id, 4)


def amdsmi_get_gpu_subsystem_name(processor_handle):
    return _gpu(processor_handle).market_name


def amdsmi_get_gpu_vram_vendor(processor_handle):
    return "AMD"


def amdsmi_get_gpu_driver_info(processor_handle):
    g = _gpu(processor_handle)
    return {
        "driver_name": "dxgkrnl (WSL2)" if backend.is_wsl() else "amdgpu",
        "driver_version": g.driver_version,
        "driver_date": g.driver_date,
    }


# --------------------------------------------------------------------------- #
# topology
# --------------------------------------------------------------------------- #
def amdsmi_topo_get_link_type(processor_handle_src, processor_handle_dst):
    src = _gpu(processor_handle_src)
    dst = _gpu(processor_handle_dst)
    if src.index == dst.index:
        return {"hops": 0, "type": int(AmdSmiLinkType.AMDSMI_LINK_TYPE_INTERNAL)}
    # No XGMI topology is exposed under WSL2 — report a PCIe-style 1-hop link.
    return {"hops": 1, "type": int(AmdSmiLinkType.AMDSMI_LINK_TYPE_PCIE)}


def amdsmi_topo_get_numa_node_number(processor_handle):
    _gpu(processor_handle)
    return 0


def amdsmi_topo_get_link_weight(processor_handle_src, processor_handle_dst):
    src = _gpu(processor_handle_src)
    dst = _gpu(processor_handle_dst)
    return 0 if src.index == dst.index else 40


def amdsmi_get_gpu_topo_numa_affinity(processor_handle):
    _gpu(processor_handle)
    return 0


# --------------------------------------------------------------------------- #
# live telemetry (best-effort via torch; NOT_SUPPORTED when unavailable)
#
# torch ROCm resolves these sensors *through amdsmi itself*, so calling them
# from inside this package can re-enter us.  Every torch telemetry call is run
# under the backend re-entrancy guard and any failure degrades to a clean
# AMDSMI_STATUS_NOT_SUPPORTED -- which is the honest answer on WSL2, where
# per-sensor clock/temp/power telemetry is not exposed.
# --------------------------------------------------------------------------- #
def _torch_metric(fn):
    torch = _torch()
    if torch is None or backend.is_probing():
        return None
    try:
        with backend.reentry_guard():
            return fn(torch)
    except BaseException:
        return None


def amdsmi_get_gpu_activity(processor_handle):
    g = _gpu(processor_handle)
    gfx = _torch_metric(lambda t: int(t.cuda.utilization(g.index)))
    if gfx is None:
        raise AmdSmiLibraryException(C.AMDSMI_STATUS_NOT_SUPPORTED)
    return {"gfx_activity": gfx, "umc_activity": 0, "mm_activity": 0}


def amdsmi_get_clock_info(processor_handle, clock_type=AmdSmiClkType.SYS):
    g = _gpu(processor_handle)
    cur = _torch_metric(lambda t: int(t.cuda.clock_rate(g.index)))  # MHz
    if cur is None:
        raise AmdSmiLibraryException(C.AMDSMI_STATUS_NOT_SUPPORTED)
    return {"cur_clk": cur, "max_clk": cur, "min_clk": 0, "sleep_clk": 0}


def amdsmi_get_temp_metric(
    processor_handle,
    sensor_type=AmdSmiTemperatureType.EDGE,
    metric=AmdSmiTemperatureMetric.CURRENT,
):
    g = _gpu(processor_handle)
    temp = _torch_metric(lambda t: int(t.cuda.temperature(g.index)))
    if temp is None:
        raise AmdSmiLibraryException(C.AMDSMI_STATUS_NOT_SUPPORTED)
    return temp


def amdsmi_get_power_info(processor_handle, *args, **kwargs):
    g = _gpu(processor_handle)
    watts = _torch_metric(lambda t: int(t.cuda.power_draw(g.index) / 1000))  # mW->W
    if watts is None:
        raise AmdSmiLibraryException(C.AMDSMI_STATUS_NOT_SUPPORTED)
    return {
        "current_socket_power": watts,
        "average_socket_power": watts,
        "gfx_voltage": 0,
        "soc_voltage": 0,
        "mem_voltage": 0,
        "power_limit": 0,
    }


# --------------------------------------------------------------------------- #
# versions / misc
# --------------------------------------------------------------------------- #
def amdsmi_get_lib_version():
    major, minor, patch = (__version__.split(".") + ["0", "0"])[:3]
    return {
        "year": 2026,
        "major": int(major),
        "minor": int(minor),
        "release": int(patch),
        "build": f"amd-smi-wsl-{__version__}",
    }


def amdsmi_get_rocm_version():
    torch = _torch()
    if torch is not None and getattr(torch.version, "hip", None):
        return str(torch.version.hip)
    raise AmdSmiLibraryException(C.AMDSMI_STATUS_NOT_SUPPORTED)


def amdsmi_status_code_to_string(status):
    try:
        err = AmdSmiLibraryException(int(status))
        return err.err_info
    except Exception:
        return "AMDSMI_STATUS_UNKNOWN_ERROR - An unknown error occurred"


# --------------------------------------------------------------------------- #
# Upstream parity: define a NOT_SUPPORTED stub for every public amdsmi_*
# function that is not implemented above.  This mirrors the native library,
# which returns AMDSMI_STATUS_NOT_SUPPORTED for features the platform lacks
# (the entire CPU/HSMP surface, counters, RAS/ECC, partitions, set_* ops,
# event notification, KFD/XGMI queries, ... none of which exist on WSL2).
# --------------------------------------------------------------------------- #
from ._func_list import _ALL_FUNCTION_NAMES  # noqa: E402


def _make_stub(_name):
    def _stub(*args, **kwargs):
        raise AmdSmiLibraryException(C.AMDSMI_STATUS_NOT_SUPPORTED)

    _stub.__name__ = _name
    _stub.__qualname__ = _name
    _stub.__doc__ = (
        f"{_name}: not supported on WSL2 / Windows "
        f"(raises AmdSmiLibraryException AMDSMI_STATUS_NOT_SUPPORTED)."
    )
    return _stub


_g = globals()
for _fname in _ALL_FUNCTION_NAMES:
    if _fname not in _g:
        _g[_fname] = _make_stub(_fname)
del _g, _fname
