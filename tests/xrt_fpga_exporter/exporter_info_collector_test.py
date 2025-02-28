"""
Unit tests for the
:py:class:
`ska_xrt_fpga_exporter.exporter_info_collector.ExporterInfoCollector`.
"""

import sys

import pytest
from prometheus_client import CollectorRegistry

from ska_xrt_fpga_exporter import release
from ska_xrt_fpga_exporter.exporter_info_collector import ExporterInfoCollector


@pytest.fixture(autouse=True)
def register(registry: CollectorRegistry):
    """
    Register the collector with the registry.
    """
    ExporterInfoCollector(registry=registry)


@pytest.fixture(name="python_version")
def fxt_python_version(monkeypatch: pytest.MonkeyPatch):
    """
    Mocks the Python version returned from ``sys.version``
    """
    version = "1.2.3"
    monkeypatch.setattr(sys, "version", version)
    return version


def test_collector_exports_info(
    registry: CollectorRegistry,
    python_version: str,
):
    """
    Test whether the collector yields the exporter info metric correctly.
    """
    assert (
        registry.get_sample_value(
            "ska_xrt_fpga_exporter_info",
            {
                "python_version": python_version,
                "version": release.version,
                "xrt_version": "2.14.354",
                "xrt_branch": "2022.2",
                "xrt_hash": "43926231f7183688add2dccfd391b36a1f000bea",
                "xrt_build_date": "2022-10-08 09:49:53",
            },
        )
        is not None
    )
