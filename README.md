# amd-smi-wsl

A **drop-in replacement for the `amdsmi` Python package** that works inside
**WSL2 / Windows**, where the native AMD SMI library cannot run.

```python
import amdsmi            # this package, not the native one
amdsmi.amdsmi_init()
h = amdsmi.amdsmi_get_processor_handles()[0]
print(amdsmi.amdsmi_get_gpu_asic_info(h)["market_name"])
```

## Why

On WSL2 the AMD GPU is exposed through DirectX para-virtualisation
(`/dev/dxg` + `dxgkrnl`), **not** the native `amdgpu` KFD driver. The Linux
`/dev/kfd` device and its sysfs topology simply do not exist, so:

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

## License

MIT. Status constants, enum values and exception classes are derived from the
MIT-licensed [ROCm/amdsmi](https://github.com/ROCm/amdsmi) project.
