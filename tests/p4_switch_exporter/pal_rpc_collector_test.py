"""
Unit tests for the
:py:class:`ska_p4_switch_collector.collectors.PalRpcCollector`.

Note: the expected values in this test match the hard-coded test data
provided in ``pal_rpc_mock.py``.
"""

import itertools

import pytest
from prometheus_client import CollectorRegistry

from ska_p4_switch_exporter.collectors import PalRpcCollector

PORTS_UP = [
    "1/0",
    "3/0",
]
PORTS_DOWN = [
    "1/1",
    "1/2",
    "1/3",
    "2/0",
    "2/1",
    "2/2",
    "2/3",
    "3/1",
    "3/2",
    "3/3",
    "4/0",
    "4/1",
    "4/2",
    "4/3",
]


@pytest.fixture(autouse=True)
def register(registry: CollectorRegistry):
    """
    Register the collector with the registry.
    """
    PalRpcCollector(
        rpc_host="",
        rpc_port=9090,
        registry=registry,
    )


@pytest.mark.parametrize(
    ("port", "expected"),
    list(zip(PORTS_UP, itertools.repeat(1.0)))
    + list(zip(PORTS_DOWN, itertools.repeat(0.0))),
)
def test_port_up(
    registry: CollectorRegistry,
    port: str,
    expected: float,
):
    """
    Tests whether the ``p4_switch_port_up`` metric is correctly
    exported by the collector.
    """
    assert (
        registry.get_sample_value(
            "p4_switch_port_up",
            labels={"port": port},
        )
        == expected
    )


@pytest.mark.parametrize("port", PORTS_UP + PORTS_DOWN)
@pytest.mark.parametrize(
    "metric",
    [
        "p4_switch_port_frames_received_total",
        "p4_switch_port_frames_received_ok_total",
        "p4_switch_port_frames_received_nok_total",
        "p4_switch_port_frames_transmitted_total",
        "p4_switch_port_frames_transmitted_ok_total",
        "p4_switch_port_frames_transmitted_nok_total",
    ],
)
def test_port_counters_are_exported_for_all_ports(
    registry: CollectorRegistry,
    metric: str,
    port: str,
):
    """
    Tests whether the given metric is correctly exported by the collector,
    irrespective of whether that port is up or not.
    """
    assert (
        registry.get_sample_value(
            metric,
            labels={"port": port},
        )
        is not None
    )
