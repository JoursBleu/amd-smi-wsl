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


def test_namespace_is_clean():
    # No private/internal aliases should leak into the public package namespace.
    assert not hasattr(amdsmi, "amdsmi_wrapper")
    # Every public amdsmi_* attribute must be callable (no stray modules).
    for n in dir(amdsmi):
        if n.startswith("amdsmi_"):
            assert callable(getattr(amdsmi, n)), f"{n} is not callable"
    # __all__ has no duplicates and every entry resolves.
    assert len(amdsmi.__all__) == len(set(amdsmi.__all__))
    for n in amdsmi.__all__:
        assert hasattr(amdsmi, n), f"__all__ entry missing: {n}"


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


# --------------------------------------------------------------------------- #
# Re-entrancy guard (the v0.2.0 recursion fix).  Runs anywhere, no GPU needed.
# --------------------------------------------------------------------------- #
def test_reentry_guard_default_off_and_scoped():
    backend = amdsmi._backend
    assert backend.is_probing() is False
    with backend.reentry_guard():
        assert backend.is_probing() is True
    assert backend.is_probing() is False


def test_init_does_not_recurse_when_torch_counts_via_amdsmi(monkeypatch):
    """Simulate torch ROCm: device_count()/is_available() call back into
    amdsmi.amdsmi_init().  Without the guard this recurses forever."""
    import sys
    import types

    # Patch the module object that amdsmi_init actually uses.
    backend = amdsmi._interface.backend
    calls = {"n": 0}

    fake_torch = types.ModuleType("torch")
    fake_torch.version = types.SimpleNamespace(hip="9.9.9")

    class _Props:
        gcnArchName = "gfx1151"
        total_memory = 1 << 30
        multi_processor_count = 40
        major, minor = 11, 0
        uuid = "abcd1234-0000-0000-0000-00000000abcd"

    class _Cuda:
        def is_available(self):
            return self.device_count() > 0

        def device_count(self):
            calls["n"] += 1
            # The re-entrant call torch makes on ROCm.
            try:
                amdsmi.amdsmi_init()
            except amdsmi.AmdSmiException:
                pass
            return 1

        def get_device_properties(self, i):
            return _Props()

        def get_device_name(self, i):
            return "AMD Radeon(TM) 8060S Graphics"

    fake_torch.cuda = _Cuda()
    monkeypatch.setitem(sys.modules, "torch", fake_torch)
    monkeypatch.setattr(backend, "_windows_probe", lambda: [])
    monkeypatch.setattr(backend, "env_disabled", lambda: False)
    backend.reset_cache()
    backend.reset_windows_probe_cache()

    amdsmi.amdsmi_init()  # must NOT raise RecursionError
    try:
        handles = amdsmi.amdsmi_get_processor_handles()
        assert len(handles) == 1
        asic = amdsmi.amdsmi_get_gpu_asic_info(handles[0])
        assert asic["target_graphics_version"] == "gfx1151"
        assert calls["n"] >= 1  # torch really did re-enter us
    finally:
        amdsmi.amdsmi_shut_down()
        backend.reset_cache()
        backend.reset_windows_probe_cache()


def test_parse_wmi_date():
    backend = amdsmi._backend
    assert backend._parse_wmi_date("/Date(1771286400000)/") == "2026-02-17"
    assert backend._parse_wmi_date("") == ""
    assert backend._parse_wmi_date(None) == ""


def test_degenerate_uuid_detection():
    backend = amdsmi._backend
    assert backend._is_degenerate_uuid("66666666-6666-6666-6666-666666666666")
    assert backend._is_degenerate_uuid("00000000-0000-0000-0000-000000000000")
    assert backend._is_degenerate_uuid("")
    assert not backend._is_degenerate_uuid("abcd1234-0000-0000-0000-00000000abcd")


# --------------------------------------------------------------------------- #
# Real-backend tests: only run where a HIP GPU is actually visible (WSL2 + ROCm
# torch).  Skipped automatically everywhere else.
# --------------------------------------------------------------------------- #
@pytest.fixture
def gpu_handle():
    try:
        amdsmi.amdsmi_init()
    except amdsmi.AmdSmiLibraryException:
        pytest.skip("no HIP GPU visible (native amdsmi env or no torch-ROCm)")
    handles = amdsmi.amdsmi_get_processor_handles()
    if not handles:
        amdsmi.amdsmi_shut_down()
        pytest.skip("no GPU handles")
    yield handles[0]
    amdsmi.amdsmi_shut_down()


def test_real_asic_info_hex_shapes(gpu_handle):
    asic = amdsmi.amdsmi_get_gpu_asic_info(gpu_handle)
    assert isinstance(asic["device_id"], str)
    assert asic["device_id"] == "N/A" or asic["device_id"].startswith("0x")
    assert isinstance(asic["market_name"], str) and asic["market_name"]
    tgv = asic["target_graphics_version"]
    assert tgv == "" or tgv.startswith("gfx")


def test_real_device_uuid_stable_and_not_degenerate(gpu_handle):
    uuid = amdsmi.amdsmi_get_gpu_device_uuid(gpu_handle)
    assert uuid
    assert not amdsmi._backend._is_degenerate_uuid(uuid)


def test_real_driver_info_keys(gpu_handle):
    di = amdsmi.amdsmi_get_gpu_driver_info(gpu_handle)
    assert {"driver_name", "driver_version", "driver_date"} <= set(di)


def test_real_memory_total_positive(gpu_handle):
    assert amdsmi.amdsmi_get_gpu_memory_total(gpu_handle) > 0


def test_real_telemetry_never_leaks_not_found(gpu_handle):
    # Each telemetry call must either return a real value or raise a *clean*
    # NOT_SUPPORTED -- never NOT_FOUND(31), and never RecursionError.
    for fn in (
        amdsmi.amdsmi_get_gpu_activity,
        amdsmi.amdsmi_get_clock_info,
        amdsmi.amdsmi_get_temp_metric,
        amdsmi.amdsmi_get_power_info,
    ):
        try:
            fn(gpu_handle)
        except amdsmi.AmdSmiLibraryException as e:
            assert e.get_error_code() == 2  # AMDSMI_STATUS_NOT_SUPPORTED

