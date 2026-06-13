<div align="center">

# `amd-smi-wsl`

### Drop-in `amdsmi` for AMD GPUs on WSL2 — so vLLM, PyTorch ROCm & friends just work

[![PyPI](https://img.shields.io/pypi/v/amd-smi-wsl?color=ed1c24&label=PyPI)](https://pypi.org/project/amd-smi-wsl/)
[![Python](https://img.shields.io/pypi/pyversions/amd-smi-wsl?color=ff7a18)](https://pypi.org/project/amd-smi-wsl/)
[![License](https://img.shields.io/badge/license-MIT-3fb950)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-WSL2%20%7C%20ROCm-0a7bbb)](https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/compatibility/compatibilityrad/wsl/wsl_compatibility.html)

**[Website](https://joursbleu.github.io/amd-smi-wsl/)** · **[PyPI](https://pypi.org/project/amd-smi-wsl/)** · **[Changelog](CHANGELOG.md)** · **[Issues](https://github.com/JoursBleu/amd-smi-wsl/issues)** · **[ROCm/amdsmi](https://github.com/ROCm/amdsmi)**

</div>

---

On **WSL2** an AMD GPU is exposed through DirectX para-virtualisation
(`/dev/dxg`), **not** the native `amdgpu` KFD driver — so `/dev/kfd` doesn't
exist and `import amdsmi` fails, which breaks ROCm platform detection in tools
like **vLLM**. `amd-smi-wsl` restores the `amdsmi` import surface using data
sources that *do* work under WSL2 (the HIP runtime + Windows interop), so those
tools start cleanly — **no patching required**.

This is a property of the WSL2 GPU stack, not of any single card, so it applies
broadly across **RDNA generations** (RDNA3 / RDNA3.5 / RDNA4 desktop Radeon &
Radeon PRO, and Ryzen AI APUs).

```python
import amdsmi            # this package, not the native one
amdsmi.amdsmi_init()
h = amdsmi.amdsmi_get_processor_handles()[0]
print(amdsmi.amdsmi_get_gpu_asic_info(h)["market_name"])
# -> AMD Radeon(TM) 8060S Graphics
```

## ✨ Highlights

- **🔌 100% import-compatible** — every public symbol of the upstream binding:
  all **190** `amdsmi_*` functions, all enums, and the full exception hierarchy.
- **🧠 Real data, not fakes** — device name, gfx arch, VRAM, compute units, UUID
  and live memory from `torch.cuda` (HIP); PCI id, subsystem id, revision and
  driver info from Windows interop.
- **♻️ torch re-entrancy safe** — a thread-local guard breaks the
  `amdsmi_init → torch.cuda → amdsmi_init` recursion that PyTorch's ROCm build
  would otherwise trigger.
- **🎯 vLLM canonical names** — returns `device_id` as a hex string (`"0x1586"`)
  so vLLM resolves the canonical name (e.g. `AMD_Radeon_8060S`).
- **🧪 Honest `NOT_SUPPORTED` stubs** for features the platform genuinely lacks
  (RAS/ECC, partitioning, `set_*`, events…), exactly like the native library.
- **📦 Zero hard deps** — pure-Python, no compiled extensions; `torch` is never
  pinned so it won't fight your ROCm install.

## 🚀 Proven in production

Used as the platform shim to serve a **35B vision-MoE in 4-bit AWQ
(`Qwen3.6-35B-A3B`) on a single AMD Radeon 8060S (Strix Halo, gfx1151)** under
WSL2 with source-built vLLM — `amd-smi-wsl` supplies the `amdsmi` surface vLLM's
ROCm platform detection needs, end-to-end OpenAI-compatible serving included.

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
all 190 `amdsmi_*` functions, all `AmdSmi*` enums, and the full
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

- `HSA_ENABLE_DXG_DETECTION` — **auto-set to `1` for you.** On WSL2 the HIP/HSA
  runtime only enumerates the DirectX-paravirtualized GPU when this is exported
  *before* the first `torch.cuda` call. Importing this package sets it (via
  `os.environ.setdefault`, so an explicit value you set is always respected) when
  it detects WSL — so `import amdsmi` is self-contained and you no longer have to
  export it by hand. Only applied inside WSL, and skipped when
  `AMDSMI_WSL_DISABLE` is set.
- `AMDSMI_WSL_DISABLE=1` — make `amdsmi_init()` raise `NOT_SUPPORTED` (and skip
  the `HSA_ENABLE_DXG_DETECTION` auto-set), useful to test a caller's fallback
  path.

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
| test suite (`pytest`) | **17 passed** |
| vLLM `rocm_platform_plugin()` | `vllm.platforms.rocm.RocmPlatform` |
| vLLM `RocmPlatform.get_device_name(0)` | `AMD_Radeon_8060S` |
| vLLM `is_fully_connected([0])` | `True` |

Telemetry that the platform does not expose (`clock_info`, `temp_metric`,
`power_info`, `gpu_activity`) raises `AMDSMI_STATUS_NOT_SUPPORTED`, as expected.

## License

MIT. Status constants, enum values and exception classes are derived from the
MIT-licensed [ROCm/amdsmi](https://github.com/ROCm/amdsmi) project.
