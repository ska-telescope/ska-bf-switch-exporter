# pylint: disable=import-error
# pylint: disable=too-few-public-methods
# pylint: disable=too-many-locals
# pylint: disable=too-many-statements

"""
Custom Prometheus collector that collects QSFP metrics
using the Barefoot platform manager RPC.
"""

import logging

from pltfm_mgr_rpc import pltfm_mgr_rpc
from prometheus_client.core import GaugeMetricFamily, InfoMetricFamily
from prometheus_client.registry import REGISTRY, CollectorRegistry

from ska_p4_switch_exporter.rpc_collector_base import RpcCollectorBase

__all__ = [
    "QSFPCollector",
]


class QSFPCollector(RpcCollectorBase):
    """
    Custom Prometheus collector that collects QSFP metrics
    using the Barefoot platform manager RPC.
    """

    qsfp_info_byte_offsets = {
        "date_code": (424, 16),
        "part_number": (336, 32),
        "revision": (368, 4),
        "serial": (392, 32),
        "vendor": (296, 32),
    }

    def __init__(
        self,
        rpc_host: str,
        rpc_port: int,
        logger: logging.Logger | None = None,
        registry: CollectorRegistry | None = REGISTRY,
    ):
        logger = logger or logging.getLogger(__name__)
        super().__init__(
            rpc_host=rpc_host,
            rpc_port=rpc_port,
            rpc_endpoint="pltfm_mgr_rpc",
            rpc_module=pltfm_mgr_rpc,
            logger=logger,
        )

        if registry:
            logger.info("Registering %s", self.__class__.__name__)
            registry.register(self)

    def collect(self):
        qsfp_info = InfoMetricFamily(
            "p4_switch_qsfp",
            "QSFP information",
            labels=["port"],
        )
        qsfp_connected = GaugeMetricFamily(
            "p4_switch_qsfp_present",
            "Whether a QSFP is connected to the port",
            labels=["port"],
        )
        qsfp_temperature = GaugeMetricFamily(
            "p4_switch_qsfp_temperature",
            "Temperature of the QSFP",
            labels=["port"],
            unit="celsius",
        )
        qsfp_temperature_warning_min = GaugeMetricFamily(
            "p4_switch_qsfp_temperature_warning_min",
            "Minimum temperature of the QSFP"
            " below which a warning should be raised",
            labels=["port"],
            unit="celsius",
        )
        qsfp_temperature_warning_max = GaugeMetricFamily(
            "p4_switch_qsfp_temperature_warning_max",
            "Maximum temperature of the QSFP"
            " above which a warning should be raised",
            labels=["port"],
            unit="celsius",
        )
        qsfp_temperature_alarm_min = GaugeMetricFamily(
            "p4_switch_qsfp_temperature_alarm_min",
            "Minimum temperature of the QSFP"
            " below which an alarm should be raised",
            labels=["port"],
            unit="celsius",
        )
        qsfp_temperature_alarm_max = GaugeMetricFamily(
            "p4_switch_qsfp_temperature_alarm_max",
            "Maximum temperature of the QSFP"
            " above which an alarm should be raised",
            labels=["port"],
            unit="celsius",
        )
        qsfp_voltage = GaugeMetricFamily(
            "p4_switch_qsfp_voltage",
            "Voltage on the QSFP",
            labels=["port"],
            unit="volts",
        )
        qsfp_voltage_warning_min = GaugeMetricFamily(
            "p4_switch_qsfp_voltage_warning_min",
            "Minimum voltage of the QSFP"
            " below which a warning should be raised",
            labels=["port"],
            unit="volts",
        )
        qsfp_voltage_warning_max = GaugeMetricFamily(
            "p4_switch_qsfp_voltage_warning_max",
            "Maximum voltage of the QSFP"
            " above which a warning should be raised",
            labels=["port"],
            unit="volts",
        )
        qsfp_voltage_alarm_min = GaugeMetricFamily(
            "p4_switch_qsfp_voltage_alarm_min",
            "Minimum voltage of the QSFP"
            " below which an alarm should be raised",
            labels=["port"],
            unit="volts",
        )
        qsfp_voltage_alarm_max = GaugeMetricFamily(
            "p4_switch_qsfp_voltage_alarm_max",
            "Maximum voltage of the QSFP"
            " above which an alarm should be raised",
            labels=["port"],
            unit="volts",
        )
        qsfp_channel_count = GaugeMetricFamily(
            "p4_switch_qsfp_channel_count",
            "Number of channels active on the QSFP",
            labels=["port"],
        )
        qsfp_channel_rx_power = GaugeMetricFamily(
            "p4_switch_qsfp_channel_rx_power",
            "RX power on the QSFP channel",
            labels=["port", "channel"],
        )
        qsfp_channel_tx_power = GaugeMetricFamily(
            "p4_switch_qsfp_channel_tx_power",
            "TX power on the QSFP channel",
            labels=["port", "channel"],
        )
        qsfp_rx_power_warning_min = GaugeMetricFamily(
            "p4_switch_qsfp_rx_power_warning_min",
            "Minimum RX power on the QSFP channel"
            " below which a warning should be raised",
            labels=["port"],
        )
        qsfp_rx_power_warning_max = GaugeMetricFamily(
            "p4_switch_qsfp_rx_power_warning_max",
            "Maximum RX power on the QSFP channel"
            " above which a warning should be raised",
            labels=["port"],
        )
        qsfp_rx_power_alarm_min = GaugeMetricFamily(
            "p4_switch_qsfp_rx_power_alarm_min",
            "Minimum RX power on the QSFP channel"
            " below which an alarm should be raised",
            labels=["port"],
        )
        qsfp_rx_power_alarm_max = GaugeMetricFamily(
            "p4_switch_qsfp_rx_power_alarm_max",
            "Maximum RX power on the QSFP channel"
            " above which an alarm should be raised",
            labels=["port"],
        )
        qsfp_tx_power_warning_min = GaugeMetricFamily(
            "p4_switch_qsfp_tx_power_warning_min",
            "Minimum TX power on the QSFP channel"
            " below which a warning should be raised",
            labels=["port"],
        )
        qsfp_tx_power_warning_max = GaugeMetricFamily(
            "p4_switch_qsfp_tx_power_warning_max",
            "Maximum TX power on the QSFP channel"
            " above which a warning should be raised",
            labels=["port"],
        )
        qsfp_tx_power_alarm_min = GaugeMetricFamily(
            "p4_switch_qsfp_tx_power_alarm_min",
            "Minimum TX power on the QSFP channel"
            " below which an alarm should be raised",
            labels=["port"],
        )
        qsfp_tx_power_alarm_max = GaugeMetricFamily(
            "p4_switch_qsfp_tx_power_alarm_max",
            "Maximum TX power on the QSFP channel"
            " above which an alarm should be raised",
            labels=["port"],
        )

        with self._get_rpc_client() as client:
            for port in range(1, client.pltfm_mgr_qsfp_get_max_port()):
                port_label = str(port)
                connected = client.pltfm_mgr_qsfp_presence_get(port)
                self._logger.debug("Port %d connected: %s", port, connected)
                qsfp_connected.add_metric([port_label], 1 if connected else 0)

                if not connected:
                    continue

                info = client.pltfm_mgr_qsfp_info_get(port)
                try:
                    qsfp_info.add_metric(
                        [port_label],
                        {
                            key: bytes.fromhex(info[offset : offset + length])
                            .decode()
                            .strip()
                            for (
                                key,
                                (offset, length),
                            ) in self.qsfp_info_byte_offsets.items()
                        },
                    )
                except (UnicodeDecodeError, ValueError):
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
