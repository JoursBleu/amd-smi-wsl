"""Opaque processor / socket handles.

The native binding hands back ``ctypes`` handle objects.  Callers (vLLM and
friends) treat them as opaque tokens and only pass them back into the API, so
plain Python objects carrying the device index are sufficient here.
"""

from __future__ import annotations

from ._enums import AmdSmiProcessorType


class _Handle:
    __slots__ = ("index",)

    def __init__(self, index: int):
        self.index = index

    def __repr__(self) -> str:  # pragma: no cover - debug aid
        return f"{type(self).__name__}(index={self.index})"

    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and self.index == other.index  # type: ignore[attr-defined]

    def __hash__(self) -> int:
        return hash((type(self).__name__, self.index))


class GpuHandle(_Handle):
    processor_type = AmdSmiProcessorType.AMD_GPU


class SocketHandle(_Handle):
    pass


class CpuHandle(_Handle):
    processor_type = AmdSmiProcessorType.AMD_CPU


class CpuCoreHandle(_Handle):
    pass
