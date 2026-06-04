"""Event reader — unsupported on WSL2 (no KFD event notification)."""

from __future__ import annotations

from . import _constants as C
from ._exceptions import AmdSmiLibraryException


class AmdSmiEventReader:
    """GPU event notification is not available under WSL2 / Windows."""

    def __init__(self, processor_handle, event_types):
        raise AmdSmiLibraryException(C.AMDSMI_STATUS_NOT_SUPPORTED)

    def read(self, timestamp, num_elem=10):  # pragma: no cover
        raise AmdSmiLibraryException(C.AMDSMI_STATUS_NOT_SUPPORTED)

    def stop(self):  # pragma: no cover
        raise AmdSmiLibraryException(C.AMDSMI_STATUS_NOT_SUPPORTED)

    def __enter__(self):  # pragma: no cover
        raise AmdSmiLibraryException(C.AMDSMI_STATUS_NOT_SUPPORTED)

    def __exit__(self, exc_type, exc_value, traceback):  # pragma: no cover
        return False
