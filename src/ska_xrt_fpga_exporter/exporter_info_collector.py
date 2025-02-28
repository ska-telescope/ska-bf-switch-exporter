# pylint: disable=import-error
# pylint: disable=too-few-public-methods

"""
Custom Prometheus collector that exposes information about this exporter.
"""

import dataclasses
import json
import logging
import sys

import pyxrt
from prometheus_client.core import InfoMetricFamily
from prometheus_client.registry import REGISTRY, Collector, CollectorRegistry

from ska_xrt_fpga_exporter import release

__all__ = [
    "ExporterInfoCollector",
]


@dataclasses.dataclass
class XrtVersionInfo:
    """
    Version information about the XRT runtime.
    """

    version: str = "unknown"
    branch: str = "unknown"
    hash: str = "unknown"
    build_date: str = "unknown"

    def dict(self):
        """
        Create a dictionary representing the instance.
        """
        return {
            f"xrt_{key}": value
            for key, value in dataclasses.asdict(self).items()
        }


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
        xrt_version_info = self._get_xrt_version_info()
        yield InfoMetricFamily(
            "ska_xrt_fpga_exporter",
            "Information about the ska-xrt-fpga-exporter",
            value={
                **xrt_version_info.dict(),
                "python_version": sys.version,
                "version": release.version,
            },
        )

    def _get_xrt_version_info(self):
        version_info = XrtVersionInfo()
        try:
            self._logger.debug("Attempting to retrieve first XRT device")
            device = pyxrt.device(0)
            self._logger.debug("Reading host info from XRT device")
            host_info = json.loads(device.get_info(pyxrt.xrt_info_device.host))
            version_info.branch = host_info["branch"]
            version_info.build_date = host_info["build_date"]
            version_info.hash = host_info["hash"]
            version_info.version = host_info["version"]
        except RuntimeError:
            self._logger.debug(
                "Error while retrieving XRT information from device",
                exc_info=True,
            )
        return version_info
