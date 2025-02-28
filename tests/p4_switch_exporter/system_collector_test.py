"""
Unit tests for the
:py:class:`ska_p4_switch_collector.system_collector.SystemCollector`.

Note: the expected values in this test match the hard-coded test data
provided in ``pltfm_mgr_rpc_mock.py``.
"""

import pytest
from prometheus_client import CollectorRegistry

from ska_p4_switch_exporter.system_collector import SystemCollector


@pytest.fixture(autouse=True)
def register(registry: CollectorRegistry):
    """
    Register the collector with the registry.
    """
    SystemCollector(
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
