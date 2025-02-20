# pylint: disable=too-few-public-methods
# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
# pylint: disable=too-many-positional-arguments
# pylint: disable=too-many-statements

"""
Prometheus metric collectors.
"""

import importlib
import json
import logging
import pathlib
import sys

from prometheus_client.core import GaugeMetricFamily, InfoMetricFamily
from prometheus_client.registry import REGISTRY, Collector, CollectorRegistry

from ska_fpga_exporter import release

__all__ = [
    "ExporterInfoCollector",
    "FpgaXrtCollector",
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
            "ska_fpga_exporter",
            "Information about the ska-fpga-exporter",
            value={"version": release.version},
        )


class FpgaXrtCollector(Collector):
    """
    Custom Prometheus collector that collects metrics from Xilinx XRT FPGAs.
    """

    def __init__(
        self,
        xrt_install_dir: pathlib.Path,
        registry: CollectorRegistry | None = REGISTRY,
        logger: logging.Logger | None = None,
    ):
        self._logger = logger or logging.getLogger(__name__)

        xrt_python_path = xrt_install_dir / "python"
        self._logger.debug("Appending import path: %s", xrt_python_path)
        sys.path.append(str(xrt_python_path.resolve()))

        self._pyxrt = importlib.import_module("pyxrt")

        if registry:
            self._logger.info("Registering %s", self.__class__.__name__)
            registry.register(self)

    def collect(self):
        device_info = InfoMetricFamily(
            "fpga_xrt_device",
            "Information about the Xilinx XRT FPGA device",
            labels=["bdf"],
        )
        device_temperature = GaugeMetricFamily(
            "fpga_xrt_device_temperature",
            "Temperature of the Xilinx XRT FPGA device",
            labels=["bdf", "location", "description"],
            unit="degrees",
        )
        device_voltage = GaugeMetricFamily(
            "fpga_xrt_device_voltage",
            "Voltage of the Xilinx XRT FPGA device",
            labels=["bdf", "location", "description"],
            unit="volts",
        )
        device_current = GaugeMetricFamily(
            "fpga_xrt_device_current",
            "Current of the Xilinx XRT FPGA device",
            labels=["bdf", "location", "description"],
            unit="amps",
        )
        device_power = GaugeMetricFamily(
            "fpga_xrt_device_power",
            "Power consumption of the Xilinx XRT FPGA device",
            labels=["bdf"],
            unit="watts",
        )
        device_max_power = GaugeMetricFamily(
            "fpga_xrt_device_max_power",
            "Maximum power consumption of the Xilinx XRT FPGA device",
            labels=["bdf"],
            unit="watts",
        )
        device_power_warning = GaugeMetricFamily(
            "fpga_xrt_device_power_warning",
            "Whether the power consumption of the Xilinx XRT FPGA device "
            "is raising a warning",
            labels=["bdf"],
        )

        for device in self._iter_devices():
            bdf = device.get_info(self._pyxrt.xrt_info_device.bdf)
            name = device.get_info(self._pyxrt.xrt_info_device.name)
            host_info = json.loads(
                device.get_info(self._pyxrt.xrt_info_device.host)
            )
            platform_info = json.loads(
                device.get_info(self._pyxrt.xrt_info_device.platform)
            )

            device_info.add_metric(
                [bdf],
                {
                    "name": name,
                    "serial": platform_info["platforms"][0]["controller"][
                        "card_mgmt_controller"
                    ]["serial_number"],
                    "xrt_version": host_info["version"],
                    "xrt_branch": host_info["branch"],
                    "xrt_hash": host_info["hash"],
                    "xrt_build_date": host_info["build_date"],
                },
            )

            thermal_info = json.loads(
                device.get_info(self._pyxrt.xrt_info_device.thermal)
            )
            for reading in thermal_info:
                if reading["is_present"] != "true":
                    self._logger.debug(
                        "Skipping thermal reading (not present): %s",
                        reading,
                    )
                    continue

                device_temperature.add_metric(
                    [bdf, reading["location_id"], reading["description"]],
                    float(reading["temp_C"]),
                )

            electrical_info = json.loads(
                device.get_info(self._pyxrt.xrt_info_device.electrical)
            )
            device_power.add_metric(
                [bdf],
                float(electrical_info["power_consumption_watts"]),
            )
            device_max_power.add_metric(
                [bdf],
                float(electrical_info["power_consumption_max_watts"]),
            )
            device_power_warning.add_metric(
                [bdf],
                float(bool(electrical_info["power_consumption_warning"])),
            )

            for reading in electrical_info["power_rails"]:
                voltage_reading = reading["voltage"]
                current_reading = reading["current"]

                if voltage_reading["is_present"] == "true":
                    device_voltage.add_metric(
                        [bdf, reading["id"], reading["description"]],
                        float(voltage_reading["volts"]),
                    )
                else:
                    self._logger.debug(
                        "Skipping voltage reading (not present): %s",
                        voltage_reading,
                    )

                if current_reading["is_present"] == "true":
                    device_current.add_metric(
                        [bdf, reading["id"], reading["description"]],
                        float(current_reading["amps"]),
                    )
                else:
                    self._logger.debug(
                        "Skipping current reading (not present): %s",
                        current_reading,
                    )

        yield from [
            device_info,
            device_temperature,
            device_current,
            device_voltage,
            device_power,
            device_max_power,
            device_power_warning,
        ]

    def _iter_devices(self):
        i = 0
        while True:
            self._logger.debug("Attempting to retrieve XRT device %d", i)
            try:
                device = self._pyxrt.device(i)
                yield device
            except RuntimeError:
                self._logger.debug(
                    "Error while retrieving XRT device %d, "
                    "assuming no more devices are available",
                    i,
                    exc_info=True,
                )
