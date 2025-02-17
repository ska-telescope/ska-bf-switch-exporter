"""
Module for the Barefoot platform manager collector.
"""

import contextlib
import importlib
import logging
import pathlib
import sys

from prometheus_client.core import GaugeMetricFamily, InfoMetricFamily
from prometheus_client.registry import REGISTRY, Collector, CollectorRegistry
from thrift.protocol import TBinaryProtocol, TMultiplexedProtocol
from thrift.transport import TSocket, TTransport

__all__ = ["PlatformManagerCollector"]

# pylint: disable=too-few-public-methods
# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
# pylint: disable=too-many-positional-arguments
# pylint: disable=too-many-statements


class PlatformManagerCollector(Collector):
    """
    Custom Prometheus collector that collects metrics exposed by the
    Barefoot platform manager RPC.
    """

    def __init__(
        self,
        rpc_host: str,
        rpc_port: int,
        sde_install_dir: pathlib.Path,
        registry: CollectorRegistry | None = REGISTRY,
        logger: logging.Logger | None = None,
    ):
        self._rpc_host = rpc_host
        self._rpc_port = rpc_port
        self._logger = logger or logging.getLogger(__name__)

        for path in sde_install_dir.rglob("lib/python*/site-packages/"):
            self._logger.debug("Appending import path %s", path)
            sys.path.append(str(path))

        self._rpc_module = importlib.import_module(
            "pltfm_mgr_rpc.pltfm_mgr_rpc"
        )

        if registry:
            registry.register(self)

    def collect(self):
        qsfp_info = InfoMetricFamily(
            "bf_switch_qsfp",
            "QSFP information",
            labels=["port"],
        )
        qsfp_connected = GaugeMetricFamily(
            "bf_switch_qsfp_present",
            "Whether the QSFP port has a connected transceiver",
            labels=["port"],
        )
        qsfp_temperature = GaugeMetricFamily(
            "bf_switch_qsfp_temperature",
            "QSFP port temperature",
            labels=["port"],
            unit="degrees",
        )
        qsfp_temperature_warning_min = GaugeMetricFamily(
            "bf_switch_qsfp_temperature_warning_min",
            "QSFP port temperature",
            labels=["port"],
            unit="degrees",
        )
        qsfp_temperature_warning_max = GaugeMetricFamily(
            "bf_switch_qsfp_temperature_warning_max",
            "QSFP port temperature",
            labels=["port"],
            unit="degrees",
        )
        qsfp_temperature_alarm_min = GaugeMetricFamily(
            "bf_switch_qsfp_temperature_alarm_min",
            "QSFP port temperature",
            labels=["port"],
            unit="degrees",
        )
        qsfp_temperature_alarm_max = GaugeMetricFamily(
            "bf_switch_qsfp_temperature_alarm_max",
            "QSFP port temperature",
            labels=["port"],
            unit="degrees",
        )
        qsfp_voltage = GaugeMetricFamily(
            "bf_switch_qsfp_voltage",
            "QSFP port voltage",
            labels=["port"],
            unit="volts",
        )
        qsfp_voltage_warning_min = GaugeMetricFamily(
            "bf_switch_qsfp_voltage_warning_min",
            "QSFP port voltage",
            labels=["port"],
            unit="volts",
        )
        qsfp_voltage_warning_max = GaugeMetricFamily(
            "bf_switch_qsfp_voltage_warning_max",
            "QSFP port voltage",
            labels=["port"],
            unit="volts",
        )
        qsfp_voltage_alarm_min = GaugeMetricFamily(
            "bf_switch_qsfp_voltage_alarm_min",
            "QSFP port voltage",
            labels=["port"],
            unit="volts",
        )
        qsfp_voltage_alarm_max = GaugeMetricFamily(
            "bf_switch_qsfp_voltage_alarm_max",
            "QSFP port voltage",
            labels=["port"],
            unit="volts",
        )
        qsfp_channel_count = GaugeMetricFamily(
            "bf_switch_qsfp_channel_count",
            "QSFP port channel count",
            labels=["port"],
        )
        qsfp_channel_rx_power = GaugeMetricFamily(
            "bf_switch_qsfp_channel_rx_power",
            "QSFP port channel RX power",
            labels=["port", "channel"],
        )
        qsfp_channel_tx_power = GaugeMetricFamily(
            "bf_switch_qsfp_channel_tx_power",
            "QSFP port channel TX power",
            labels=["port", "channel"],
        )
        qsfp_rx_power_warning_min = GaugeMetricFamily(
            "bf_switch_qsfp_rx_power_warning_min",
            "QSFP port rx_power",
            labels=["port"],
        )
        qsfp_rx_power_warning_max = GaugeMetricFamily(
            "bf_switch_qsfp_rx_power_warning_max",
            "QSFP port rx_power",
            labels=["port"],
        )
        qsfp_rx_power_alarm_min = GaugeMetricFamily(
            "bf_switch_qsfp_rx_power_alarm_min",
            "QSFP port rx_power",
            labels=["port"],
        )
        qsfp_rx_power_alarm_max = GaugeMetricFamily(
            "bf_switch_qsfp_rx_power_alarm_max",
            "QSFP port rx_power",
            labels=["port"],
        )
        qsfp_tx_power_warning_min = GaugeMetricFamily(
            "bf_switch_qsfp_tx_power_warning_min",
            "QSFP port tx_power",
            labels=["port"],
        )
        qsfp_tx_power_warning_max = GaugeMetricFamily(
            "bf_switch_qsfp_tx_power_warning_max",
            "QSFP port tx_power",
            labels=["port"],
        )
        qsfp_tx_power_alarm_min = GaugeMetricFamily(
            "bf_switch_qsfp_tx_power_alarm_min",
            "QSFP port tx_power",
            labels=["port"],
        )
        qsfp_tx_power_alarm_max = GaugeMetricFamily(
            "bf_switch_qsfp_tx_power_alarm_max",
            "QSFP port tx_power",
            labels=["port"],
        )

        with self._rpc_client() as client:
            for port in range(1, client.pltfm_mgr_qsfp_get_max_port()):
                port_label = str(port)
                connected = client.pltfm_mgr_qsfp_presence_get(port)
                self._logger.debug("Port %d connected: %s", port, connected)
                qsfp_connected.add_metric([port_label], 1 if connected else 0)

                if not connected:
                    continue

                info = client.pltfm_mgr_qsfp_info_get(port)
                try:
                    # serial number is encoded in the info starting at byte
                    # 392 and finished when 0x202020 starts.
                    i1 = 392
                    i2 = i1 + info[i1:-1].index("202020")
                    qsfp_serial = bytes.fromhex(info[i1:i2]).decode()
                    qsfp_info.add_metric([port_label], {"serial": qsfp_serial})
                except UnicodeDecodeError:
                    self._logger.debug(
                        "Unable to decode QSFP serial number "
                        "from hex string: %s",
                        info,
                    )

                qsfp_temperature.add_metric(
                    [port_label], client.pltfm_mgr_qsfp_temperature_get(port)
                )
                qsfp_voltage.add_metric(
                    [port_label], client.pltfm_mgr_qsfp_voltage_get(port)
                )
                qsfp_channel_count.add_metric(
                    [port_label], client.pltfm_mgr_qsfp_chan_count_get(port)
                )

                thresholds = client.pltfm_mgr_qsfp_thresholds_get(port)

                if thresholds.temp_is_set:
                    qsfp_temperature_alarm_max.add_metric(
                        [port_label], thresholds.temp.highalarm
                    )
                    qsfp_temperature_alarm_min.add_metric(
                        [port_label], thresholds.temp.lowalarm
                    )
                    qsfp_temperature_warning_max.add_metric(
                        [port_label], thresholds.temp.highwarning
                    )
                    qsfp_temperature_warning_min.add_metric(
                        [port_label], thresholds.temp.lowwarning
                    )

                if thresholds.vcc_is_set:
                    qsfp_voltage_alarm_max.add_metric(
                        [port_label], thresholds.vcc.highalarm
                    )
                    qsfp_voltage_alarm_min.add_metric(
                        [port_label], thresholds.vcc.lowalarm
                    )
                    qsfp_voltage_warning_max.add_metric(
                        [port_label], thresholds.vcc.highwarning
                    )
                    qsfp_voltage_warning_min.add_metric(
                        [port_label], thresholds.vcc.lowwarning
                    )

                if thresholds.rx_pwr_is_set:
                    qsfp_rx_power_alarm_max.add_metric(
                        [port_label], thresholds.rx_pwr.highalarm
                    )
                    qsfp_rx_power_alarm_min.add_metric(
                        [port_label], thresholds.rx_pwr.lowalarm
                    )
                    qsfp_rx_power_warning_max.add_metric(
                        [port_label], thresholds.rx_pwr.highwarning
                    )
                    qsfp_rx_power_warning_min.add_metric(
                        [port_label], thresholds.rx_pwr.lowwarning
                    )

                if thresholds.tx_pwr_is_set:
                    qsfp_tx_power_alarm_max.add_metric(
                        [port_label], thresholds.tx_pwr.highalarm
                    )
                    qsfp_tx_power_alarm_min.add_metric(
                        [port_label], thresholds.tx_pwr.lowalarm
                    )
                    qsfp_tx_power_warning_max.add_metric(
                        [port_label], thresholds.tx_pwr.highwarning
                    )
                    qsfp_tx_power_warning_min.add_metric(
                        [port_label], thresholds.tx_pwr.lowwarning
                    )

                for channel, channel_rx_power in enumerate(
                    client.pltfm_mgr_qsfp_chan_rx_pwr_get(port)
                ):
                    qsfp_channel_rx_power.add_metric(
                        [port_label, str(channel + 1)], channel_rx_power
                    )

                for channel, channel_tx_power in enumerate(
                    client.pltfm_mgr_qsfp_chan_tx_pwr_get(port)
                ):
                    qsfp_channel_tx_power.add_metric(
                        [port_label, str(channel + 1)], channel_tx_power
                    )

        yield from [
            qsfp_connected,
            qsfp_channel_rx_power,
            qsfp_channel_tx_power,
            qsfp_channel_count,
            qsfp_info,
            qsfp_rx_power_alarm_max,
            qsfp_rx_power_alarm_min,
            qsfp_rx_power_warning_max,
            qsfp_rx_power_warning_min,
            qsfp_temperature,
            qsfp_temperature_alarm_max,
            qsfp_temperature_alarm_min,
            qsfp_temperature_warning_max,
            qsfp_temperature_warning_min,
            qsfp_tx_power_alarm_max,
            qsfp_tx_power_alarm_min,
            qsfp_tx_power_warning_max,
            qsfp_tx_power_warning_min,
            qsfp_voltage,
            qsfp_voltage_alarm_max,
            qsfp_voltage_alarm_min,
            qsfp_voltage_warning_max,
            qsfp_voltage_warning_min,
        ]

    @contextlib.contextmanager
    def _rpc_client(self):
        transport = None

        try:
            self._logger.debug(
                "Creating RPC transport to %s:%d",
                self._rpc_host,
                self._rpc_port,
            )
            transport = TSocket.TSocket(self._rpc_host, self._rpc_port)
            transport.setTimeout(5000)
            transport = TTransport.TBufferedTransport(transport)

            self._logger.debug("Opening RPC transport")
            transport.open()

            self._logger.debug("Creating RPC client")
            client = self._rpc_module.Client(
                TMultiplexedProtocol.TMultiplexedProtocol(
                    TBinaryProtocol.TBinaryProtocol(transport),
                    "pltfm_mgr_rpc",
                )
            )
            yield client
        finally:
            if transport is not None:
                self._logger.debug("Disconnecting from RPC")
                transport.close()
