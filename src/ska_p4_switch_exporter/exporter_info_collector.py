# pylint: disable=too-few-public-methods

"""
Custom Prometheus collector that exposes information about this exporter.
"""

import functools
import logging
import pathlib
import sys

from prometheus_client.core import InfoMetricFamily
from prometheus_client.registry import REGISTRY, Collector, CollectorRegistry

from ska_p4_switch_exporter import release

__all__ = [
    "ExporterInfoCollector",
]


class ExporterInfoCollector(Collector):
    """
    Custom Prometheus collector that exposes information about this exporter.
    """

    def __init__(
        self,
        sde_install_path: pathlib.Path,
        logger: logging.Logger | None = None,
        registry: CollectorRegistry | None = REGISTRY,
    ):
        self._version_file = sde_install_path / "share" / "VERSION"
        self._logger = logger or logging.getLogger(__name__)

        if registry:
            self._logger.info("Registering %s", self.__class__.__name__)
            registry.register(self)

    @functools.cached_property
    def sde_version(self):
        """
        Retrieve the SDE version from the SDE installation directory,
        or ``unknown`` if the version cannot be determined.
        """
        if not self._version_file.exists():
            self._logger.warning(
                "Unable to determine SDE version: %s does not exist",
                self._version_file,
            )
            return "unknown"

        return self._version_file.read_text(encoding="utf-8").strip()

    def collect(self):
        yield InfoMetricFamily(
            "ska_p4_switch_exporter",
            "Information about the ska-p4-switch-exporter",
            value={
                "python_version": sys.version,
                "sde_version": self.sde_version,
                "version": release.version,
            },
        )
