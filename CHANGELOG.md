# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

[Unreleased]: https://github.com/JoursBleu/amd-smi-wsl/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/JoursBleu/amd-smi-wsl/releases/tag/v0.1.0
