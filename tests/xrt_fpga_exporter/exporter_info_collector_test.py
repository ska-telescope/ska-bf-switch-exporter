"""
Unit tests for the
:py:class:`ska_xrt_fpga_exporter.collectors.ExporterInfoCollector`.
"""

import pytest
from prometheus_client import CollectorRegistry

from ska_xrt_fpga_exporter import release
from ska_xrt_fpga_exporter.collectors import ExporterInfoCollector


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
            "ska_xrt_fpga_exporter_info",
            {
                "version": release.version,
            },
        )
        is not None
    )
