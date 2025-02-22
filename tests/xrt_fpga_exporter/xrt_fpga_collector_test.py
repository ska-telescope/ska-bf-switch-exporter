"""
Unit tests for the
:py:class:`ska_xrt_fpga_exporter.collectors.XrtFpgaCollector`.

Note: the expected values in this test match the hard-coded test data
provided by the mocked pyxrt library.
"""

import pytest
from prometheus_client import CollectorRegistry

from ska_xrt_fpga_exporter.collectors import XrtFpgaCollector


@pytest.fixture(autouse=True)
def register(registry: CollectorRegistry):
    """
    Register the collector with the registry.
    """
    XrtFpgaCollector(registry=registry)


@pytest.mark.parametrize(
    ("metric", "expected_value", "labels"),
    [
        (
            "xrt_fpga_info",
            1.0,
            {
                "bdf": "0000:00:00.1",
                "name": "xilinx_u55c_gen3x16_xdma_base_3",
                "serial": "000000000000",
                "xrt_version": "2.14.354",
                "xrt_branch": "2022.2",
                "xrt_hash": "43926231f7183688add2dccfd391b36a1f000bea",
                "xrt_build_date": "2022-10-08 09:49:53",
            },
        ),
        (
            "xrt_fpga_info",
            1.0,
            {
                "bdf": "0000:01:00.1",
                "name": "xilinx_u55c_gen3x16_xdma_base_3",
                "serial": "111111111111",
                "xrt_version": "2.14.354",
                "xrt_branch": "2022.2",
                "xrt_hash": "43926231f7183688add2dccfd391b36a1f000bea",
                "xrt_build_date": "2022-10-08 09:49:53",
            },
        ),
        (
            "xrt_fpga_temperature_degrees",
            27.0,
            {
                "bdf": "0000:00:00.1",
                "location": "fpga0",
                "description": "FPGA",
            },
        ),
        (
            "xrt_fpga_temperature_degrees",
            22.0,
            {
                "bdf": "0000:01:00.1",
                "location": "cage_temp_0",
                "description": "Cage0",
            },
        ),
        (
            "xrt_fpga_voltage_volts",
            0.85,
            {
                "bdf": "0000:00:00.1",
                "location": "vccint",
                "description": "Internal FPGA Vcc",
            },
        ),
        (
            "xrt_fpga_voltage_volts",
            5.028,
            {
                "bdf": "0000:01:00.1",
                "location": "5v5_system",
                "description": "5.5 Volts System",
            },
        ),
        (
            "xrt_fpga_current_amps",
            0.5,
            {
                "bdf": "0000:00:00.1",
                "location": "vccint_io",
                "description": "Internal FPGA Vcc IO",
            },
        ),
        (
            "xrt_fpga_current_amps",
            0.672,
            {
                "bdf": "0000:01:00.1",
                "location": "12v_pex",
                "description": "12 Volts PCI Express",
            },
        ),
        ("xrt_fpga_power_watts", 15.540264, {"bdf": "0000:00:00.1"}),
        ("xrt_fpga_power_watts", 15.425088, {"bdf": "0000:01:00.1"}),
        ("xrt_fpga_max_power_watts", 225.0, {"bdf": "0000:00:00.1"}),
        ("xrt_fpga_max_power_watts", 225.0, {"bdf": "0000:01:00.1"}),
        ("xrt_fpga_power_warning", 0.0, {"bdf": "0000:00:00.1"}),
        ("xrt_fpga_power_warning", 0.0, {"bdf": "0000:01:00.1"}),
    ],
)
def test_collector_exports_metric(
    registry: CollectorRegistry,
    metric: str,
    expected_value: float,
    labels: dict[str, str],
):
    """
    Test whether the exporter collected the expected metric with the given
    value and labels.

    This test case does not cover all permutations of available labels,
    but aims to cover every exported metric at least once per device.
    """
    assert registry.get_sample_value(metric, labels=labels) == expected_value


@pytest.mark.parametrize(
    ("metric", "labels"),
    [
        (
            "xrt_fpga_temperature_degrees",
            {
                "bdf": "0000:00:00.1",
                "location": "fpga_hbm",
                "description": "FPGA HBM",
            },
        ),
        (
            "xrt_fpga_temperature_degrees",
            {
                "bdf": "0000:01:00.1",
                "location": "fpga_hbm",
                "description": "FPGA HBM",
            },
        ),
        (
            "xrt_fpga_voltage_volts",
            {
                "bdf": "0000:00:00.1",
                "location": "3v3_aux",
                "description": "3.3 Volts Auxillary",
            },
        ),
        (
            "xrt_fpga_voltage_volts",
            {
                "bdf": "0000:01:00.1",
                "location": "0v9_vccint_vcu",
                "description": "0.9 Volts Vcc Vcu",
            },
        ),
        (
            "xrt_fpga_current_amps",
            {
                "bdf": "0000:01:00.1",
                "location": "hbm_1v2",
                "description": "1.2 Volts HBM",
            },
        ),
        (
            "xrt_fpga_current_amps",
            {
                "bdf": "0000:01:00.1",
                "location": "5v5_system",
                "description": "5.5 Volts System",
            },
        ),
    ],
)
def test_collector_does_not_export_metric(
    registry: CollectorRegistry,
    metric: str,
    labels: dict[str, str],
):
    """
    Test whether the exporter did not collect the expected metric with the
    given labels.

    This test case does not cover all permutations of available labels,
    but aims to cover every applicable metric at least once per device.
    """
    assert registry.get_sample_value(metric, labels=labels) is None
