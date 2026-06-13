# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.3.0] - 2026-06-13

### Added
- Auto-set `HSA_ENABLE_DXG_DETECTION=1` at import time when running under WSL2
  (unless already set, or `AMDSMI_WSL_DISABLE` is active). Without this env var
  the HIP runtime does not enumerate the DirectX-paravirtualized GPU, so
  `torch.cuda.is_available()` is `False` and `amdsmi_init()` raised
  `DRIVER_NOT_LOADED`. Importing `amdsmi` is the earliest point in a typical
  vLLM/PyTorch startup, so callers no longer have to export the variable
  themselves. Respects an explicit `HSA_ENABLE_DXG_DETECTION=0`.

### Tested
- Verified on WSL2 + AMD Radeon 8060S (Strix Halo, gfx1151) + ROCm 7.2.4 +
  PyTorch 2.10.0 from the published PyPI wheel: with no env var exported,
  `import amdsmi` auto-sets `HSA_ENABLE_DXG_DETECTION=1`, `amdsmi_init()`
  succeeds, and upstream vLLM resolves `RocmPlatform` /
  `get_device_name(0) == "AMD_Radeon_8060S"` / `get_device_capability(0) == (11, 5)`.

## [0.2.0] - 2026-06-11

### Fixed
- **Critical:** infinite recursion / `RecursionError` when used with a real
  PyTorch ROCm build. torch's ROCm device enumeration resolves the device count
  *through* `amdsmi` (`amdsmi_init` + `amdsmi_get_processor_handles`), which this
  package shadows, so `amdsmi_init()` -> backend probe -> `torch.cuda` ->
  `amdsmi_init()` looped forever. A thread-local re-entrancy guard now makes the
  re-entrant `amdsmi_init()` raise so torch falls back to its native HIP device
  count. This was the blocker that prevented the package (and vLLM through it)
  from working at all on the target WSL2 + torch-ROCm environment.
- `amdsmi_get_clock_info` / `amdsmi_get_temp_metric` / `amdsmi_get_power_info`
  could leak `AMDSMI_STATUS_NOT_FOUND` (and risk re-entrancy) when torch routed
  the sensor query back through amdsmi; they now degrade cleanly to
  `AMDSMI_STATUS_NOT_SUPPORTED`.

### Changed
- `amdsmi_get_gpu_asic_info` now returns `device_id`, `vendor_id`,
  `subvendor_id`, `subsystem_id` and `rev_id` as lowercase, zero-padded hex
  strings (e.g. `"0x1586"`, `"0xc1"`), matching the upstream contract. This lets
  vLLM resolve the canonical device name from its hex-keyed
  `_ROCM_DEVICE_ID_NAME_MAP` (e.g. `AMD_Radeon_8060S`) instead of falling back
  to the raw marketing string. `amdsmi_get_gpu_subsystem_id` /
  `amdsmi_get_gpu_revision` likewise return hex strings.
- `driver_date` from the Windows probe is parsed from the raw WMI
  `/Date(ms)/` serialization into a readable `YYYY-MM-DD` string.
- The Windows interop probe is cached persistently (PCI metadata is static), so
  vLLM's `with_amdsmi_context` no longer re-spawns `powershell.exe` on every
  call.
- Degenerate placeholder UUIDs reported by torch on WSL2 (e.g.
  `66666666-...`) are detected and replaced with a stable synthesized id, kept
  consistent across `device_uuid`, `asic_serial`, and board `product_serial`.

### Tested
- Verified end-to-end on WSL2 + AMD Radeon 8060S (Strix Halo, gfx1151) +
  ROCm 7.2.4 + PyTorch 2.9.1: `import amdsmi` works, vLLM ROCm platform
  detection succeeds, and `RocmPlatform.get_device_name(0)` returns
  `AMD_Radeon_8060S`.

## [0.1.0] - 2026-06-04

### Added
- Initial release: a drop-in replacement for the `amdsmi` Python package that
  works on WSL2 / Windows, where the native AMD SMI library cannot run because
  the KFD interface (`/dev/kfd`, `/sys/class/kfd`) is unavailable.
- Full API parity with upstream `amdsmi`: all 189 `amdsmi_*` functions, 37
  `AmdSmi*` enums, the complete exception hierarchy, and `AmdSmiEventReader`.
- Real implementations for the queryable subset, backed by:
  - the HIP runtime via `torch.cuda` (device count, name, gfx arch, VRAM, compute
    units, live memory usage), and
  - Windows interop (`powershell.exe Get-CimInstance Win32_VideoController`) to
    recover the real PCI device id, subsystem id, and driver version.
  - a static `gfx -> metadata` fallback table.
- Faithful degradation: capabilities that genuinely do not exist on WSL2 raise
  `AmdSmiLibraryException(AMDSMI_STATUS_NOT_SUPPORTED)`, matching native behavior.
- `AMDSMI_WSL_DISABLE` environment variable to disable the shim.

[Unreleased]: https://github.com/JoursBleu/amd-smi-wsl/compare/v0.3.0...HEAD
[0.3.0]: https://github.com/JoursBleu/amd-smi-wsl/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/JoursBleu/amd-smi-wsl/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/JoursBleu/amd-smi-wsl/releases/tag/v0.1.0
