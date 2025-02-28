# pylint: disable=too-few-public-methods

"""
Custom Prometheus collector that exposes information about this exporter.
"""

import logging

from prometheus_client.core import InfoMetricFamily
from prometheus_client.registry import REGISTRY, Collector, CollectorRegistry

from ska_xrt_fpga_exporter import release

__all__ = [
    "ExporterInfoCollector",
]


class ExporterInfoCollector(Collector):
    """
    Custom Prometheus collector that exposes information about this exporter.
    """

    def __init__(
        self,
        logger: logging.Logger | None = None,
        registry: CollectorRegistry | None = REGISTRY,
    ):
        self._logger = logger or logging.getLogger(__name__)

        if registry:
            self._logger.info("Registering %s", self.__class__.__name__)
            registry.register(self)

    def collect(self):
        yield InfoMetricFamily(
            "ska_xrt_fpga_exporter",
            "Information about the ska-xrt-fpga-exporter",
            value={"version": release.version},
        )
