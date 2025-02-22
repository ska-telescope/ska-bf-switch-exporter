# pylint: disable=import-error
# pylint: disable=too-few-public-methods
# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
# pylint: disable=too-many-positional-arguments
# pylint: disable=too-many-statements

"""
Prometheus metric collectors.
"""

import json
import logging

import pyxrt
from prometheus_client.core import GaugeMetricFamily, InfoMetricFamily
from prometheus_client.registry import REGISTRY, Collector, CollectorRegistry

from ska_xrt_fpga_exporter import release

__all__ = [
    "ExporterInfoCollector",
    "XrtFpgaCollector",
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


class XrtFpgaCollector(Collector):
    """
    Custom Prometheus collector that collects metrics from Xilinx XRT FPGAs.
    """

    def __init__(
        self,
        registry: CollectorRegistry | None = REGISTRY,
        logger: logging.Logger | None = None,
    ):
        self._logger = logger or logging.getLogger(__name__)

        if registry:
            self._logger.info("Registering %s", self.__class__.__name__)
            registry.register(self)

    def collect(self):
        info = InfoMetricFamily(
            "xrt_fpga",
            "Information about the Xilinx XRT FPGA device",
            labels=["bdf"],
        )
        temperature = GaugeMetricFamily(
            "xrt_fpga_temperature",
            "Temperature of the Xilinx XRT FPGA device",
            labels=["bdf", "location", "description"],
            unit="degrees",
        )
        voltage = GaugeMetricFamily(
            "xrt_fpga_voltage",
            "Voltage of the Xilinx XRT FPGA device",
            labels=["bdf", "location", "description"],
            unit="volts",
        )
        current = GaugeMetricFamily(
            "xrt_fpga_current",
            "Current of the Xilinx XRT FPGA device",
            labels=["bdf", "location", "description"],
            unit="amps",
        )
        power = GaugeMetricFamily(
            "xrt_fpga_power",
            "Power consumption of the Xilinx XRT FPGA device",
            labels=["bdf"],
            unit="watts",
        )
        max_power = GaugeMetricFamily(
            "xrt_fpga_max_power",
            "Maximum power consumption of the Xilinx XRT FPGA device",
            labels=["bdf"],
            unit="watts",
        )
        power_warning = GaugeMetricFamily(
            "xrt_fpga_power_warning",
            "Whether the power consumption of the Xilinx XRT FPGA device "
            "is raising a warning",
            labels=["bdf"],
        )

        for device in self._iter_devices():
            bdf = device.get_info(pyxrt.xrt_info_device.bdf)
            name = device.get_info(pyxrt.xrt_info_device.name)
            host_info = json.loads(device.get_info(pyxrt.xrt_info_device.host))
            platform_info = json.loads(
                device.get_info(pyxrt.xrt_info_device.platform)
            )

            info.add_metric(
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
                device.get_info(pyxrt.xrt_info_device.thermal)
            )
            for reading in thermal_info["thermals"]:
                if reading["is_present"] != "true":
                    self._logger.debug(
                        "Skipping thermal reading (not present): %s",
                        reading,
                    )
                    continue

                temperature.add_metric(
                    [bdf, reading["location_id"], reading["description"]],
                    float(reading["temp_C"]),
                )

            electrical_info = json.loads(
                device.get_info(pyxrt.xrt_info_device.electrical)
            )
            power.add_metric(
                [bdf],
                float(electrical_info["power_consumption_watts"]),
            )
            max_power.add_metric(
                [bdf],
                float(electrical_info["power_consumption_max_watts"]),
            )
            power_warning.add_metric(
                [bdf],
                float(electrical_info["power_consumption_warning"] == "true"),
            )

            for reading in electrical_info["power_rails"]:
                voltage_reading = reading["voltage"]
                current_reading = reading["current"]

                if voltage_reading["is_present"] == "true":
                    voltage.add_metric(
                        [bdf, reading["id"], reading["description"]],
                        float(voltage_reading["volts"]),
                    )
                else:
                    self._logger.debug(
                        "Skipping voltage reading (not present): %s",
                        voltage_reading,
                    )

                if current_reading["is_present"] == "true":
                    current.add_metric(
                        [bdf, reading["id"], reading["description"]],
                        float(current_reading["amps"]),
                    )
                else:
                    self._logger.debug(
                        "Skipping current reading (not present): %s",
                        current_reading,
                    )

        yield from [
            info,
            temperature,
            current,
            voltage,
            power,
            max_power,
            power_warning,
        ]

    def _iter_devices(self):
        i = 0
        while True:
            self._logger.debug("Attempting to retrieve XRT device %d", i)
            try:
                device = pyxrt.device(i)
                yield device
                i += 1
            except RuntimeError:
                self._logger.debug(
                    "Error while retrieving XRT device %d, "
                    "assuming no more devices are available",
                    i,
                    exc_info=True,
                )
                break
