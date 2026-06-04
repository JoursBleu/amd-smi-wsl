"""Smoke tests for the amd-smi-wsl drop-in.

These run anywhere (no GPU required). When torch/HIP is absent, init raises
DRIVER_NOT_LOADED — which is itself the correct, tested behaviour.
"""

import importlib

import amdsmi
import pytest


def test_full_function_parity():
    from amdsmi._func_list import _ALL_FUNCTION_NAMES

    assert len(_ALL_FUNCTION_NAMES) == 189
    for name in _ALL_FUNCTION_NAMES:
        assert hasattr(amdsmi, name), f"missing {name}"
        assert callable(getattr(amdsmi, name))


def test_enums_present_and_valued():
    assert int(amdsmi.AmdSmiStatus.NOT_SUPPORTED) == 2
    assert int(amdsmi.AmdSmiProcessorType.AMD_GPU) >= 0
    # A representative sample of the 37 enums.
    for enum_name in [
        "AmdSmiClkType",
        "AmdSmiTemperatureType",
        "AmdSmiLinkType",
        "AmdSmiMemoryType",
        "AmdSmiInitFlags",
    ]:
        assert hasattr(amdsmi, enum_name)


def test_exception_hierarchy():
    assert issubclass(amdsmi.AmdSmiLibraryException, amdsmi.AmdSmiException)
    err = amdsmi.AmdSmiLibraryException(2)
    assert err.get_error_code() == 2
    assert "NOT_SUPPORTED" in err.err_info


def test_not_supported_stub_behaviour():
    # A CPU/HSMP function that can never work on WSL2.
    with pytest.raises(amdsmi.AmdSmiLibraryException) as ei:
        amdsmi.amdsmi_get_cpu_socket_power(object())
    assert ei.value.get_error_code() == 2  # AMDSMI_STATUS_NOT_SUPPORTED


def test_status_code_to_string():
    s = amdsmi.amdsmi_status_code_to_string(2)
    assert "NOT_SUPPORTED" in s


def test_init_without_gpu_raises_driver_not_loaded(monkeypatch):
    # Force "no GPU" regardless of host.
    monkeypatch.setattr(amdsmi._backend, "available", lambda: False)
    monkeypatch.setattr(amdsmi._backend, "env_disabled", lambda: False)
    with pytest.raises(amdsmi.AmdSmiLibraryException) as ei:
        amdsmi.amdsmi_init()
    assert ei.value.get_error_code() == 34  # DRIVER_NOT_LOADED


def test_env_disable(monkeypatch):
    monkeypatch.setenv("AMDSMI_WSL_DISABLE", "1")
    importlib.reload(amdsmi._backend)
    with pytest.raises(amdsmi.AmdSmiLibraryException):
        amdsmi.amdsmi_init()
