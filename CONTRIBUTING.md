# Contributing

Thanks for your interest in improving `amd-smi-wsl`.

## Scope

This package is a **drop-in replacement** for the upstream `amdsmi` Python
binding, targeted at WSL2 / Windows environments where the native AMD SMI
library cannot run. The guiding principle is **API fidelity**: the public
surface (function names, signatures, return shapes, enums, exceptions) must
match upstream `amdsmi`. Where a capability cannot be supported on WSL2, the
corresponding function should raise
`AmdSmiLibraryException(AMDSMI_STATUS_NOT_SUPPORTED)` rather than returning
fabricated data.

## Development setup

```bash
git clone git@github.com:JoursBleu/amd-smi-wsl.git
cd amd-smi-wsl
python -m venv .venv && . .venv/bin/activate
pip install -e ".[test]"
pytest
```

## Guidelines

- Keep full parity with upstream `amdsmi` — do not rename or drop public symbols.
- Constants and enums are extracted verbatim from upstream; do not edit their
  values by hand.
- New real implementations must degrade gracefully when no GPU / no torch is
  present.
- Add or update tests in `tests/` for any behavior change.
- Run `pytest` before opening a pull request.

## Reporting issues

Please include: OS (Windows version + WSL distro), ROCm version, GPU model,
`python -c "import torch; print(torch.version.hip)"`, and the full traceback.
