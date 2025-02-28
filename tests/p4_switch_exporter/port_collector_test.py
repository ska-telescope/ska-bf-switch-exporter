"""
Unit tests for the
:py:class:`ska_p4_switch_collector.port_collector.PortCollector`.

Note: the expected values in this test match the hard-coded test data
provided in ``pal_rpc_mock.py``.
"""

import pytest
from prometheus_client import CollectorRegistry

from ska_p4_switch_exporter.port_collector import PortCollector

PORTS_UP = [
    (1, 0),
    (3, 0),
]
PORTS_DOWN = [
    (1, 1),
    (1, 2),
    (1, 3),
    (2, 0),
    (2, 1),
    (2, 2),
    (2, 3),
    (3, 1),
    (3, 2),
    (3, 3),
    (4, 0),
    (4, 1),
    (4, 2),
    (4, 3),
]


@pytest.fixture(autouse=True)
def register(registry: CollectorRegistry):
    """
    Register the collector with the registry.
    """
    PortCollector(
        rpc_host="",
        rpc_port=9090,
        registry=registry,
    )


@pytest.mark.parametrize(("port", "channel"), PORTS_UP)
def test_port_up(
    registry: CollectorRegistry,
    port: int,
    channel: int,
):
    """
    Tests whether the ``p4_switch_port_up`` metric exports ``1.0`` for
    ports that are operational.
    """
    assert (
        registry.get_sample_value(
            "p4_switch_port_up",
            labels={"port": str(port), "channel": str(channel)},
        )
        == 1.0
    )


@pytest.mark.parametrize(("port", "channel"), PORTS_DOWN)
def test_port_not_up(
    registry: CollectorRegistry,
    port: int,
    channel: int,
):
    """
    Tests whether the ``p4_switch_port_up`` metric exports ``0.0`` for
    ports that are not operational.
    """
    assert (
        registry.get_sample_value(
            "p4_switch_port_up",
            labels={"port": str(port), "channel": str(channel)},
        )
        == 0.0
    )


@pytest.mark.parametrize(("port", "channel"), PORTS_UP + PORTS_DOWN)
@pytest.mark.parametrize(
    "metric",
    [
        "p4_switch_port_stats_rx_bytes_total",
        "p4_switch_port_stats_tx_bytes_total",
        "p4_switch_port_stats_rx_errors_total",
        "p4_switch_port_stats_tx_errors_total",
        "p4_switch_port_stats_rx_unicast_frames_total",
        "p4_switch_port_stats_rx_multicast_frames_total",
        "p4_switch_port_stats_rx_broadcast_frames_total",
        "p4_switch_port_stats_tx_unicast_frames_total",
        "p4_switch_port_stats_tx_multicast_frames_total",
        "p4_switch_port_stats_tx_broadcast_frames_total",
    ],
)
def test_port_counters_are_exported_for_all_ports(
    registry: CollectorRegistry,
    metric: str,
    port: int,
    channel: int,
):
    """
    Tests whether the given metric is correctly exported by the collector,
    irrespective of whether that port is up or not.
    """
    assert (
        registry.get_sample_value(
            metric,
            labels={"port": str(port), "channel": str(channel)},
        )
        is not None
    )


@pytest.mark.parametrize(("port", "channel"), PORTS_UP + PORTS_DOWN)
@pytest.mark.parametrize(
    "metric",
    [
        "p4_switch_port_stats_rx_frames_total",
        "p4_switch_port_stats_tx_frames_total",
    ],
)
@pytest.mark.parametrize(
    "length",
    [
        "<64",
        "64",
        "65-127",
        "128-255",
        "256-511",
        "512-1023",
        "1024-1518",
        "1519-2047",
        "2048-4095",
        "4096-8191",
        "8192-9215",
        "9216",
    ],
)
def test_port_frame_counters_are_exported_for_all_ports(
    registry: CollectorRegistry,
    metric: str,
    port: int,
    channel: int,
    length: str,
):
    """
    Tests whether the given metric is correctly exported by the collector,
    irrespective of whether that port is up or not.
    """
    assert (
        registry.get_sample_value(
            metric,
            labels={
                "port": str(port),
                "channel": str(channel),
                "length": length,
            },
        )
        is not None
    )
