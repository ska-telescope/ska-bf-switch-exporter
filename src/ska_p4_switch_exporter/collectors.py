# pylint: disable=import-error
# pylint: disable=too-few-public-methods
# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
# pylint: disable=too-many-positional-arguments
# pylint: disable=too-many-statements

"""
Prometheus metric collectors.
"""

import abc
import contextlib
import logging
from types import ModuleType

from pltfm_mgr_rpc import pltfm_mgr_rpc
from prometheus_client.core import (
    CounterMetricFamily,
    GaugeMetricFamily,
    InfoMetricFamily,
)
from prometheus_client.registry import REGISTRY, Collector, CollectorRegistry
from thrift.protocol import TBinaryProtocol, TMultiplexedProtocol
from thrift.transport import TSocket, TTransport
from tofino.pal_rpc import pal

from ska_p4_switch_exporter import release

__all__ = [
    "ExporterInfoCollector",
    "PlatformManagerRpcCollector",
    "PalRpcCollector",
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
            "ska_p4_switch_exporter",
            "Information about the ska-p4-switch-exporter",
            value={"version": release.version},
        )


class _RpcCollectorBase(Collector, abc.ABC):
    def __init__(
        self,
        rpc_host: str,
        rpc_port: int,
        rpc_endpoint: str,
        rpc_module: ModuleType,
        logger: logging.Logger,
    ):
        self._rpc_host = rpc_host
        self._rpc_port = rpc_port
        self._rpc_endpoint = rpc_endpoint
        self._rpc_module = rpc_module
        self._logger = logger

    @contextlib.contextmanager
    def _get_rpc_client(self):
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

            self._logger.debug(
                "Creating RPC client for endpoint: %s",
                self._rpc_endpoint,
            )
            client = self._rpc_module.Client(
                TMultiplexedProtocol.TMultiplexedProtocol(
                    TBinaryProtocol.TBinaryProtocol(transport),
                    self._rpc_endpoint,
                )
            )
            yield client
        finally:
            if transport is not None:
                self._logger.debug("Disconnecting from RPC")
                transport.close()


class PalRpcCollector(_RpcCollectorBase):
    """
    Custom Prometheus collector that collects metrics exposed by the
    Barefoot PAL RPC.
    """

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
            rpc_endpoint="pal",
            rpc_module=pal,
            logger=logger,
        )

        if registry:
            logger.info("Registering %s", self.__class__.__name__)
            registry.register(self)

    def collect(self):
        port_up = GaugeMetricFamily(
            "p4_switch_port_up",
            "Operational status of the port",
            labels=["port"],
        )
        port_frames_received = CounterMetricFamily(
            "p4_switch_port_frames_received",
            "The total number of frames received on the port",
            labels=["port"],
        )
        port_frames_received_ok = CounterMetricFamily(
            "p4_switch_port_frames_received_ok",
            "The number of frames received OK on the port",
            labels=["port"],
        )
        port_frames_received_nok = CounterMetricFamily(
            "p4_switch_port_frames_received_nok",
            "The number of frames received NOK on the port",
            labels=["port"],
        )
        port_bytes_received = CounterMetricFamily(
            "p4_switch_port_bytes_received",
            "The total number of bytes received on the port",
            labels=["port"],
        )
        port_bytes_received_ok = CounterMetricFamily(
            "p4_switch_port_bytes_received_ok",
            "The total number of bytes received in OK frames on the port",
            labels=["port"],
        )
        port_frames_transmitted = CounterMetricFamily(
            "p4_switch_port_frames_transmitted",
            "The total number of frames transmitted on the port",
            labels=["port"],
        )
        port_frames_transmitted_ok = CounterMetricFamily(
            "p4_switch_port_frames_transmitted_ok",
            "The number of frames transmitted OK on the port",
            labels=["port"],
        )
        port_frames_transmitted_nok = CounterMetricFamily(
            "p4_switch_port_frames_transmitted_nok",
            "The number of frames transmitted NOK on the port",
            labels=["port"],
        )
        port_bytes_transmitted = CounterMetricFamily(
            "p4_switch_port_bytes_transmitted",
            "The total number of bytes transmitted on the port",
            labels=["port"],
        )
        port_bytes_transmitted_ok = CounterMetricFamily(
            "p4_switch_port_bytes_transmitted_ok",
            "The total number of bytes transmitted"
            " without errors on the port",
            labels=["port"],
        )

        with self._get_rpc_client() as client:
            for port in self._iter_ports(client):
                fp_port = client.pal_port_dev_port_to_front_panel_port_get(
                    0, port
                )
                port_label = (
                    f"{fp_port.pal_front_port}/{fp_port.pal_front_chnl}"
                )
                self._logger.debug(
                    "Port %d corresponds to front panel port %s",
                    port,
                    port_label,
                )

                port_up.add_metric(
                    [port_label],
                    float(client.pal_port_oper_status_get(0, port)),
                )
                port_frames_received.add_metric(
                    [port_label],
                    float(client.pal_port_this_stat_get(0, port, 1)),
                )
                port_frames_received_ok.add_metric(
                    [port_label],
                    float(client.pal_port_this_stat_get(0, port, 0)),
                )
                port_frames_received_nok.add_metric(
                    [port_label],
                    float(client.pal_port_this_stat_get(0, port, 3)),
                )
                port_bytes_received.add_metric(
                    [port_label],
                    float(client.pal_port_this_stat_get(0, port, 5)),
                )
                port_bytes_received_ok.add_metric(
                    [port_label],
                    float(client.pal_port_this_stat_get(0, port, 4)),
                )
                port_frames_transmitted.add_metric(
                    [port_label],
                    float(client.pal_port_this_stat_get(0, port, 33)),
                )
                port_frames_transmitted_ok.add_metric(
                    [port_label],
                    float(client.pal_port_this_stat_get(0, port, 32)),
                )
                port_frames_transmitted_nok.add_metric(
                    [port_label],
                    float(client.pal_port_this_stat_get(0, port, 34)),
                )
                port_bytes_transmitted.add_metric(
                    [port_label],
                    float(client.pal_port_this_stat_get(0, port, 36)),
                )
                port_bytes_transmitted_ok.add_metric(
                    [port_label],
                    float(client.pal_port_this_stat_get(0, port, 35)),
                )

        yield from [
            port_up,
            port_frames_received,
            port_frames_received_ok,
            port_frames_received_nok,
            port_bytes_received,
            port_bytes_received_ok,
            port_frames_transmitted,
            port_frames_transmitted_ok,
            port_frames_transmitted_nok,
            port_bytes_transmitted,
            port_bytes_transmitted_ok,
        ]

    def _iter_ports(self, client: pal.Client):
        port = client.pal_port_get_first(0)
        while True:
            self._logger.debug("Processing port %d", port)
            try:
                if not client.pal_port_is_valid(0, port):
                    self._logger.debug("Port %d is not valid, skipping", port)
                    port = client.pal_port_get_next(0, port)
                    continue

                yield port
                self._logger.debug("Retrieving next port")
                port = client.pal_port_get_next(0, port)
            except pal.InvalidPalOperation:
                self._logger.debug(
                    "Error while processing port %d,"
                    " assuming no more ports are available",
                    port,
                    exc_info=True,
                )
                break


class PlatformManagerRpcCollector(_RpcCollectorBase):
    """
    Custom Prometheus collector that collects metrics exposed by the
    Barefoot platform manager RPC.
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
        system_temperature = GaugeMetricFamily(
            "p4_switch_system_temperature",
            "Temperature of the system",
            labels=["id"],
            unit="celsius",
        )

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
            temperatures = client.pltfm_mgr_sys_tmp_get()

            for i in range(5):
                label = f"motherboard{i+1}"
                attr = f"tmp{i+1}"
                system_temperature.add_metric(
                    [label], getattr(temperatures, attr)
                )

            system_temperature.add_metric(["tofino"], temperatures.tmp6)

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
            system_temperature,
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
