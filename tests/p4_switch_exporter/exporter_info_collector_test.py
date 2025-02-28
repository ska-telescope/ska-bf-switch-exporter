"""
Unit tests for the
:py:class:
`ska_xrt_fpga_exporter.exporter_info_collector.ExporterInfoCollector`.
"""

import pathlib
import sys

import pytest
from prometheus_client import CollectorRegistry

from ska_p4_switch_exporter import release
from ska_p4_switch_exporter.exporter_info_collector import (
    ExporterInfoCollector,
)


@pytest.fixture(autouse=True)
def register(
    registry: CollectorRegistry,
    tmp_path: pathlib.Path,
):
    """
    Register the collector with the registry.
    """
    ExporterInfoCollector(
        sde_install_path=tmp_path,
        registry=registry,
    )


@pytest.fixture(name="python_version")
def fxt_python_version(monkeypatch: pytest.MonkeyPatch):
    """
    Mocks the Python version returned from ``sys.version``
    """
    version = "1.2.3"
    monkeypatch.setattr(sys, "version", version)
    return version


@pytest.fixture(name="sde_version")
def fxt_sde_version(tmp_path: pathlib.Path):
    """
    Ensures the SDE version file is present at
    ``SDE_INSTALL_PATH/share/VERSION``, and returns the version contained in
    the file.
    """
    version = "9.8.7"
    parent_dir = tmp_path / "share"
    parent_dir.mkdir()
    version_file = parent_dir / "VERSION"
    version_file.write_text(version, encoding="utf-8")
    return version


def test_collector_exports_info(
    registry: CollectorRegistry,
    python_version: str,
    sde_version: str,
):
    """
    Test whether the collector yields the exporter info metric correctly.
    """
    assert (
        registry.get_sample_value(
            "ska_p4_switch_exporter_info",
            {
                "python_version": python_version,
                "sde_version": sde_version,
                "version": release.version,
            },
        )
        is not None
    )


def test_collector_exports_info_when_no_sde_version(
    registry: CollectorRegistry,
    python_version: str,
):
    """
    Test whether the collector yields the exporter info metric correctly when
    no SDE version information can be found on the file system.
    """
    assert (
        registry.get_sample_value(
            "ska_p4_switch_exporter_info",
            {
                "python_version": python_version,
                "sde_version": "unknown",
                "version": release.version,
            },
        )
        is not None
    )
