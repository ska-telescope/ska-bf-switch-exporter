"""
Unit tests for the
:py:class:`ska_p4_switch_collector.collectors.PlatformManagerRpcCollector`.

Note: the expected values in this test match the hard-coded test data
provided in ``pltfm_mgr_rpc_mock.py``.
"""

import pytest
from prometheus_client import CollectorRegistry

from ska_p4_switch_exporter.collectors import PlatformManagerRpcCollector


@pytest.fixture(autouse=True)
def register(registry: CollectorRegistry):
    """
    Register the collector with the registry.
    """
    PlatformManagerRpcCollector(
        rpc_host="",
        rpc_port=9090,
        registry=registry,
    )


@pytest.mark.parametrize(
    ("loc", "expected"),
    [
        ("motherboard1", 40.0),
        ("motherboard3", 39.9),
        ("tofino", 47.5),
    ],
)
def test_system_temperature_celsius(
    registry: CollectorRegistry,
    loc: str,
    expected: float,
):
    """
    Tests whether the ``p4_switch_system_temperature_celsius`` metric
    is correctly exported by the collector.
    """
    assert (
        registry.get_sample_value(
            "p4_switch_system_temperature_celsius",
            labels={"id": loc},
        )
        == expected
    )


@pytest.mark.parametrize(
    ("port", "expected"),
    [
        ("1", 1.0),
        ("2", 0.0),
        ("3", 1.0),
        ("4", 0.0),
        ("5", 1.0),
    ],
)
def test_qsfp_present(
    registry: CollectorRegistry,
    port: str,
    expected: float,
):
    """
    Tests whether the ``p4_switch_qsfp_present`` metric is correctly
    exported by the collector.
    """
    assert (
        registry.get_sample_value(
            "p4_switch_qsfp_present",
            labels={"port": port},
        )
        == expected
    )


@pytest.mark.parametrize("port", ["2", "4"])
@pytest.mark.parametrize(
    "metric",
    [
        "p4_switch_qsfp_channel_count",
        "p4_switch_qsfp_channel_rx_power",
        "p4_switch_qsfp_channel_tx_power",
        "p4_switch_qsfp_info",
        "p4_switch_qsfp_temperature_celsius",
        "p4_switch_qsfp_voltage_volts",
    ],
)
def test_metric_not_exported_when_no_qsfp_present(
    registry: CollectorRegistry,
    metric: str,
    port: str,
):
    """
    Tests whether the given metric is *not* exported for ports where no QSFP
    is present.
    """
    matches = [
        s
        for m in registry.collect()
        for s in m.samples
        if s.name == metric and s.labels.get("port") == port
    ]
    assert matches == []


@pytest.mark.parametrize(
    ("port", "expected"),
    [
        ("1", 1.0),
        ("3", 3.0),
        ("5", 5.0),
    ],
)
def test_qsfp_channel_count(
    registry: CollectorRegistry,
    port: str,
    expected: float,
):
    """
    Tests whether the ``p4_switch_qsfp_channel_count`` metric is correctly
    exported by the collector.

    This metric should only be exported for ports where a QSFP is present.
    """
    assert (
        registry.get_sample_value(
            "p4_switch_qsfp_channel_count",
            labels={"port": port},
        )
        == expected
    )


@pytest.mark.parametrize(
    ("port", "expected"),
    [
        ("1", 10.0),
        ("3", 30.0),
        ("5", 50.0),
    ],
)
def test_qsfp_temperature_celsius(
    registry: CollectorRegistry,
    port: str,
    expected: float,
):
    """
    Tests whether the ``p4_switch_qsfp_temperature_celsius`` metric is
    correctly exported by the collector.

    This metric should only be exported for ports where a QSFP is present.
    """
    assert (
        registry.get_sample_value(
            "p4_switch_qsfp_temperature_celsius",
            labels={"port": port},
        )
        == expected
    )


@pytest.mark.parametrize("port", ["1", "3", "5"])
@pytest.mark.parametrize("expected", [12.0])
def test_qsfp_voltage_volts(
    registry: CollectorRegistry,
    port: str,
    expected: float,
):
    """
    Tests whether the ``p4_switch_qsfp_voltage_volts`` metric is correctly
    exported by the collector.

    This metric should only be exported for ports where a QSFP is present.
    """
    assert (
        registry.get_sample_value(
            "p4_switch_qsfp_voltage_volts",
            labels={"port": port},
        )
        == expected
    )


@pytest.mark.parametrize(
    ("port", "channel", "expected"),
    [
        ("1", "1", 1.0),
        ("3", "1", 3.0),
        ("3", "2", 6.0),
        ("3", "3", 9.0),
        ("5", "1", 5.0),
        ("5", "2", 10.0),
        ("5", "3", 15.0),
        ("5", "4", 20.0),
        ("5", "5", 25.0),
    ],
)
def test_qsfp_channel_rx_power(
    registry: CollectorRegistry,
    port: str,
    channel: str,
    expected: float,
):
    """
    Tests whether the ``p4_switch_qsfp_channel_rx_power`` metric is
    correctly exported by the collector.

    This metric should only be exported for ports where a QSFP is present.
    """
    assert (
        registry.get_sample_value(
            "p4_switch_qsfp_channel_rx_power",
            labels={"port": port, "channel": channel},
        )
        == expected
    )


@pytest.mark.parametrize(
    ("port", "channel", "expected"),
    [
        ("1", "1", 2.0),
        ("3", "1", 4.0),
        ("3", "2", 7.0),
        ("3", "3", 10.0),
        ("5", "1", 6.0),
        ("5", "2", 11.0),
        ("5", "3", 16.0),
        ("5", "4", 21.0),
        ("5", "5", 26.0),
    ],
)
def test_qsfp_channel_tx_power(
    registry: CollectorRegistry,
    port: str,
    channel: str,
    expected: float,
):
    """
    Tests whether the ``p4_switch_qsfp_channel_tx_power`` metric is
    correctly exported by the collector.

    This metric should only be exported for ports where a QSFP is present.
    """
    assert (
        registry.get_sample_value(
            "p4_switch_qsfp_channel_tx_power",
            labels={"port": port, "channel": channel},
        )
        == expected
    )


@pytest.mark.parametrize("port", ["1", "3"])
def test_qsfp_info(registry: CollectorRegistry, port: str):
    """
    Tests whether the ``p4_switch_qsfp_info`` metric is correctly exported
    by the collector.

    This metric should only be exported for ports where a QSFP is present.

    The mock module is set up to return a valid hex string for ports 1 and 3.
    """
    expected_labels = {
        "port": port,
        "date_code": port * 8,
        "part_number": port * 16,
        "revision": port * 2,
        "serial": port * 16,
        "vendor": port * 16,
    }

    assert (
        registry.get_sample_value("p4_switch_qsfp_info", expected_labels)
        == 1.0
    )


@pytest.mark.parametrize("port", ["5"])
def test_no_qsfp_info_when_parsing_fails(
    registry: CollectorRegistry,
    port: str,
):
    """
    Tests the edge-case where the QSFP info returned by the RPC cannot be
    parsed.

    The mock module is set up to return an invalid hex string for port 5.
    """
    matches = [
        s
        for m in registry.collect()
        for s in m.samples
        if s.name == "p4_switch_qsfp_info" and s.labels.get("port") == port
    ]
    assert matches == []


@pytest.mark.parametrize(
    "metric",
    [
        "p4_switch_qsfp_temperature_alarm_max_celsius",
        "p4_switch_qsfp_temperature_alarm_min_celsius",
        "p4_switch_qsfp_temperature_warning_max_celsius",
        "p4_switch_qsfp_temperature_warning_min_celsius",
    ],
)
@pytest.mark.parametrize(
    ("port", "expected"),
    [
        ("1", False),
        ("3", True),
        ("5", True),
    ],
)
def test_qsfp_temperature_threshold_metric(
    registry: CollectorRegistry,
    metric: str,
    port: str,
    expected: bool,
):
    """
    Tests whether metrics related to QSFP temperature thresholds are
    correctly exported by the collector.
    """
    actual = registry.get_sample_value(
        metric,
        labels={"port": port},
    )
    if expected:
        assert actual is not None
    else:
        assert actual is None


@pytest.mark.parametrize(
    "metric",
    [
        "p4_switch_qsfp_voltage_alarm_max_volts",
        "p4_switch_qsfp_voltage_alarm_min_volts",
        "p4_switch_qsfp_voltage_warning_max_volts",
        "p4_switch_qsfp_voltage_warning_min_volts",
    ],
)
@pytest.mark.parametrize(
    ("port", "expected"),
    [
        ("1", False),
        ("3", True),
        ("5", True),
    ],
)
def test_qsfp_voltage_threshold_metric(
    registry: CollectorRegistry,
    metric: str,
    port: str,
    expected: bool,
):
    """
    Tests whether metrics related to QSFP voltage thresholds are
    correctly exported by the collector.
    """
    actual = registry.get_sample_value(
        metric,
        labels={"port": port},
    )
    if expected:
        assert actual is not None
    else:
        assert actual is None


@pytest.mark.parametrize(
    "metric",
    [
        "p4_switch_qsfp_rx_power_alarm_max",
        "p4_switch_qsfp_rx_power_alarm_min",
        "p4_switch_qsfp_rx_power_warning_max",
        "p4_switch_qsfp_rx_power_warning_min",
    ],
)
@pytest.mark.parametrize(
    ("port", "expected"),
    [
        ("1", False),
        ("3", False),
        ("5", True),
    ],
)
def test_qsfp_rx_power_threshold_metric(
    registry: CollectorRegistry,
    metric: str,
    port: str,
    expected: bool,
):
    """
    Tests whether metrics related to QSFP RX power thresholds are
    correctly exported by the collector.
    """
    actual = registry.get_sample_value(
        metric,
        labels={"port": port},
    )
    if expected:
        assert actual is not None
    else:
        assert actual is None


@pytest.mark.parametrize(
    "metric",
    [
        "p4_switch_qsfp_tx_power_alarm_max",
        "p4_switch_qsfp_tx_power_alarm_min",
        "p4_switch_qsfp_tx_power_warning_max",
        "p4_switch_qsfp_tx_power_warning_min",
    ],
)
@pytest.mark.parametrize(
    ("port", "expected"),
    [
        ("1", False),
        ("3", False),
        ("5", True),
    ],
)
def test_qsfp_tx_power_threshold_metric(
    registry: CollectorRegistry,
    metric: str,
    port: str,
    expected: bool,
):
    """
    Tests whether metrics related to QSFP TX power thresholds are
    correctly exported by the collector.
    """
    actual = registry.get_sample_value(
        metric,
        labels={"port": port},
    )
    if expected:
        assert actual is not None
    else:
        assert actual is None
