# amd-smi-wsl

A **drop-in replacement for the `amdsmi` Python package** that works inside
**WSL2 / Windows**, where the native AMD SMI library cannot run.

This is a property of the WSL2 GPU stack rather than of any single card, so it
applies broadly to AMD GPUs used with ROCm under WSL2 — across RDNA
generations (e.g. RDNA3 / RDNA3.5 / RDNA4 desktop Radeon and Radeon PRO cards,
as well as Ryzen AI APUs). The data sources it builds on (the HIP runtime and
Windows interop) are GPU-agnostic; only the per-device details (PCI id, market
name, gfx arch) differ from card to card.

```python
import amdsmi            # this package, not the native one
amdsmi.amdsmi_init()
h = amdsmi.amdsmi_get_processor_handles()[0]
print(amdsmi.amdsmi_get_gpu_asic_info(h)["market_name"])
```

## Why

On WSL2 **any** AMD GPU is exposed through DirectX para-virtualisation
(`/dev/dxg` + `dxgkrnl`), **not** the native `amdgpu` KFD driver. The Linux
`/dev/kfd` device and its sysfs topology simply do not exist, so — regardless
of which Radeon / Ryzen GPU you have:

- `import amdsmi` (native) fails / `amdsmi_init()` raises, and
- downstream code such as **vLLM** then fails ROCm platform detection and
  device-name / topology queries at startup,

even though the HIP runtime itself works perfectly via `/dev/dxg`.

This package restores the `amdsmi` import surface and re-implements the
*queryable* subset on top of data sources that **do** work in WSL2:

| Source | Provides |
| --- | --- |
| `torch.cuda` (HIP runtime) | device count, name, GCN arch, total VRAM, compute units, UUID, live mem usage |
| Windows interop (`Get-CimInstance Win32_VideoController`) | real PCI device id, subsystem id, revision, driver version/date |
| Static `gfx -> metadata` table | marketing name / VRAM type / device id fallbacks |

> **Note on `torch` re-entrancy.** PyTorch's ROCm build resolves its device
> count *through* `amdsmi` itself. Since this package replaces `amdsmi`, a
> naive probe would recurse (`amdsmi_init` -> `torch.cuda` -> `amdsmi_init` ...).
> A thread-local re-entrancy guard breaks that cycle so `torch` falls back to
> its native HIP device count. See the v0.2.0 entry in the changelog.

## API coverage

The package exposes **every** public symbol of the upstream binding —
all 189 `amdsmi_*` functions, all 37 `AmdSmi*` enums, and the full
exception hierarchy — so `import amdsmi` is binary-compatible at the
Python level.

- **Implemented for real** (read-only queries that map cleanly to HIP /
  Windows data): init / shutdown, processor & socket handle enumeration,
  `asic_info`, `board_info`, `vram_info`, `vram_usage`, `memory_total`,
  `memory_usage`, `device_uuid`, `device_bdf`, `driver_info`, `gpu_id`,
  `subsystem_id`/`name`, `revision`, `vendor_name`, `topo_get_link_type`,
  `topo_get_numa_node_number`, `lib_version`, `rocm_version`,
  `status_code_to_string`, and best-effort `activity` / `clock_info` /
  `temp_metric` / `power_info` (when the running `torch` build exposes them).
- **Faithful `NOT_SUPPORTED` stubs** for everything the platform genuinely
  lacks under WSL2: the entire CPU/HSMP/EPYC surface, performance counters,
  RAS/ECC, compute/memory partitioning, every `set_*` mutator, GPU reset,
  KFD info, XGMI status, and event notification. These raise
  `AmdSmiLibraryException(AMDSMI_STATUS_NOT_SUPPORTED)` — exactly what the
  native library does for unsupported features.

## Install

```bash
pip install amd-smi-wsl
```

`torch` (ROCm build) is expected to already be present in your environment and
is therefore **not** declared as a hard dependency.

> Only install this where the real `amdsmi` cannot be used. In a normal
> native-Linux ROCm install you should keep the official `amdsmi`.

## Environment variables

- `AMDSMI_WSL_DISABLE=1` — make `amdsmi_init()` raise `NOT_SUPPORTED`, useful
  to test a caller's fallback path.

## Relationship to vLLM

This package makes the native-`amdsmi` code paths in vLLM's
`vllm/platforms/rocm.py` and `vllm/platforms/__init__.py` work unchanged on
WSL2, as an alternative to patching vLLM with `torch.cuda` fallbacks
(cf. vLLM PR #37189).

With this package installed, vLLM resolves the **canonical** device name from
its hex-keyed `_ROCM_DEVICE_ID_NAME_MAP` (because `asic_info["device_id"]` is
returned as a lowercase hex string such as `"0x1586"`), e.g.:

```python
from vllm.platforms import rocm_platform_plugin
import vllm.platforms.rocm as rocm
rocm_platform_plugin()              # -> 'vllm.platforms.rocm.RocmPlatform'
rocm.RocmPlatform.get_device_name(0)  # -> 'AMD_Radeon_8060S'
rocm._GCN_ARCH                      # -> 'gfx1151'
```

## Verified environment

The mechanism is GPU-agnostic (it only relies on the HIP runtime + Windows
interop, which behave the same for any Radeon / Ryzen GPU under WSL2). The
numbers below are from one fully validated end-to-end setup — **WSL2 + AMD
Radeon 8060S (Strix Halo, gfx1151) + ROCm 7.2.4 + PyTorch 2.9.1** — and the
device-specific values (name, `device_id`, gfx arch) will naturally differ on
other cards:

| Check | Result |
| --- | --- |
| `import amdsmi` + `amdsmi_init()` | OK (no recursion) |
| `amdsmi_get_gpu_asic_info()["market_name"]` | `AMD Radeon(TM) 8060S Graphics` |
| `amdsmi_get_gpu_asic_info()["device_id"]` | `0x1586` (hex string) |
| `target_graphics_version` | `gfx1151` |
| test suite (`pytest`) | **16 passed** |
| vLLM `rocm_platform_plugin()` | `vllm.platforms.rocm.RocmPlatform` |
| vLLM `RocmPlatform.get_device_name(0)` | `AMD_Radeon_8060S` |
| vLLM `is_fully_connected([0])` | `True` |

Telemetry that the platform does not expose (`clock_info`, `temp_metric`,
`power_info`, `gpu_activity`) raises `AMDSMI_STATUS_NOT_SUPPORTED`, as expected.

## License

MIT. Status constants, enum values and exception classes are derived from the
MIT-licensed [ROCm/amdsmi](https://github.com/ROCm/amdsmi) project.
