"""amd-smi-wsl — a drop-in ``amdsmi`` replacement for WSL2 / Windows.

The native AMD SMI library depends on the Linux KFD driver (``/dev/kfd``),
which is absent inside WSL2 where the GPU is exposed through DirectX
para-virtualisation (``/dev/dxg``).  Importing the real ``amdsmi`` therefore
fails, which in turn breaks ROCm platform detection and device queries in
projects such as vLLM.

This package provides the *same* import surface (``import amdsmi``) and
re-implements the queryable subset on top of the HIP runtime (via
``torch.cuda``) plus Windows interop (``Get-CimInstance Win32_VideoController``)
for PCI metadata.  Features that genuinely do not exist under WSL2 raise
``AmdSmiLibraryException(AMDSMI_STATUS_NOT_SUPPORTED)``, matching the native
library's behaviour for unsupported platforms.

Only install this where the real ``amdsmi`` cannot be used.
"""

from __future__ import annotations

# Exceptions (verbatim from upstream).
from ._exceptions import (
    AmdSmiBdfFormatException,
    AmdSmiException,
    AmdSmiKeyException,
    AmdSmiLibraryException,
    AmdSmiParameterException,
    AmdSmiRetryException,
    AmdSmiTimeoutException,
)

# Enums (verbatim values from upstream).
from . import _enums as _enums_mod
from ._enums import *  # noqa: F401,F403

# Event reader (unsupported stub).
from ._event import AmdSmiEventReader

# All amdsmi_* functions (real impls + NOT_SUPPORTED parity stubs).
from . import _interface as _iface
from ._interface import __version__

# Re-export every public amdsmi_* function into the package namespace.
from ._func_list import _ALL_FUNCTION_NAMES

for _name in _ALL_FUNCTION_NAMES:
    globals()[_name] = getattr(_iface, _name)
del _name

# Convenience alias used by some callers.
amdsmi_is_P2P_accessible = _iface.__dict__.get(
    "amdsmi_is_P2P_accessible", getattr(_iface, "amdsmi_topo_get_p2p_status")
)


def _enum_names() -> list[str]:
    return [n for n in dir(_enums_mod) if n.startswith("AmdSmi")]


# `from ._enums import *` pulls in the module's internal ``_constants`` alias
# (``amdsmi_wrapper``) because that submodule defines no ``__all__``. Drop it so
# the public package namespace stays clean (it was never part of ``__all__``).
globals().pop("amdsmi_wrapper", None)


__all__ = (
    [
        "AmdSmiException",
        "AmdSmiLibraryException",
        "AmdSmiRetryException",
        "AmdSmiTimeoutException",
        "AmdSmiParameterException",
        "AmdSmiKeyException",
        "AmdSmiBdfFormatException",
        "AmdSmiEventReader",
        "__version__",
    ]
    + list(_ALL_FUNCTION_NAMES)
    + _enum_names()
)
