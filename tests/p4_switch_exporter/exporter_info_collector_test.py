"""
Unit tests for the
:py:class:
`ska_xrt_fpga_exporter.exporter_info_collector.ExporterInfoCollector`.
"""

import pytest
from prometheus_client import CollectorRegistry

from ska_p4_switch_exporter import release
from ska_p4_switch_exporter.exporter_info_collector import (
    ExporterInfoCollector,
)


@pytest.fixture(autouse=True)
def register(registry: CollectorRegistry):
    """
    Register the collector with the registry.
    """
    ExporterInfoCollector(registry=registry)


def test_collector_exports_info(registry: CollectorRegistry):
    """
    Test whether the collector yields the exporter info metric correctly.
    """
    assert (
        registry.get_sample_value(
            "ska_p4_switch_exporter_info",
            {
                "version": release.version,
            },
        )
        is not None
    )
