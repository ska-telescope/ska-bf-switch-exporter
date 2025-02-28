# pylint: disable=import-error
# pylint: disable=too-few-public-methods
# pylint: disable=too-many-locals

"""
Custom Prometheus collector that collects front-panel port metrics
using the Barefoot PAL RPC.
"""

import enum
import logging

from prometheus_client.core import CounterMetricFamily, GaugeMetricFamily
from prometheus_client.registry import REGISTRY, CollectorRegistry
from tofino.pal_rpc import pal

from ska_p4_switch_exporter.rpc_collector_base import RpcCollectorBase

__all__ = [
    "PortCollector",
]


class PalStat(enum.IntEnum):
    """
    Identifiers for the port statistics returned by the PAL RPC.

    Note: these values are taken from the PAL RPC thrift definition.
    """

    # pylint: disable=invalid-name

    FramesReceivedOK = 0
    FramesReceivedAll = 1
    FramesReceivedwithFCSError = 2
    FrameswithanyError = 3
    OctetsReceivedinGoodFrames = 4
    OctetsReceived = 5
    FramesReceivedwithUnicastAddresses = 6
    FramesReceivedwithMulticastAddresses = 7
    FramesReceivedwithBroadcastAddresses = 8
    FramesReceivedoftypePAUSE = 9
    FramesReceivedwithLengthError = 10
    FramesReceivedUndersized = 11
    FramesReceivedOversized = 12
    FragmentsReceived = 13
    JabberReceived = 14
    PriorityPauseFrames = 15
    CRCErrorStomped = 16
    FrameTooLong = 17
    RxVLANFramesGood = 18
    FramesDroppedBufferFull = 19
    FramesReceivedLength_lt_64 = 20
    FramesReceivedLength_eq_64 = 21
    FramesReceivedLength_65_127 = 22
    FramesReceivedLength_128_255 = 23
    FramesReceivedLength_256_511 = 24
    FramesReceivedLength_512_1023 = 25
    FramesReceivedLength_1024_1518 = 26
    FramesReceivedLength_1519_2047 = 27
    FramesReceivedLength_2048_4095 = 28
    FramesReceivedLength_4096_8191 = 29
    FramesReceivedLength_8192_9215 = 30
    FramesReceivedLength_9216 = 31
    FramesTransmittedOK = 32
    FramesTransmittedAll = 33
    FramesTransmittedwithError = 34
    OctetsTransmittedwithouterror = 35
    OctetsTransmittedTotal = 36
    FramesTransmittedUnicast = 37
    FramesTransmittedMulticast = 38
    FramesTransmittedBroadcast = 39
    FramesTransmittedPause = 40
    FramesTransmittedPriPause = 41
    FramesTransmittedVLAN = 42
    FramesTransmittedLength_lt_64 = 43
    FramesTransmittedLength_eq_64 = 44
    FramesTransmittedLength_65_127 = 45
    FramesTransmittedLength_128_255 = 46
    FramesTransmittedLength_256_511 = 47
    FramesTransmittedLength_512_1023 = 48
    FramesTransmittedLength_1024_1518 = 49
    FramesTransmittedLength_1519_2047 = 50
    FramesTransmittedLength_2048_4095 = 51
    FramesTransmittedLength_4096_8191 = 52
    FramesTransmittedLength_8192_9215 = 53
    FramesTransmittedLength_9216 = 54
    Pri0FramesTransmitted = 55
    Pri1FramesTransmitted = 56
    Pri2FramesTransmitted = 57
    Pri3FramesTransmitted = 58
    Pri4FramesTransmitted = 59
    Pri5FramesTransmitted = 60
    Pri6FramesTransmitted = 61
    Pri7FramesTransmitted = 62
    Pri0FramesReceived = 63
    Pri1FramesReceived = 64
    Pri2FramesReceived = 65
    Pri3FramesReceived = 66
    Pri4FramesReceived = 67
    Pri5FramesReceived = 68
    Pri6FramesReceived = 69
    Pri7FramesReceived = 70
    TransmitPri0Pause1USCount = 71
    TransmitPri1Pause1USCount = 72
    TransmitPri2Pause1USCount = 73
    TransmitPri3Pause1USCount = 74
    TransmitPri4Pause1USCount = 75
    TransmitPri5Pause1USCount = 76
    TransmitPri6Pause1USCount = 77
    TransmitPri7Pause1USCount = 78
    ReceivePri0Pause1USCount = 79
    ReceivePri1Pause1USCount = 80
    ReceivePri2Pause1USCount = 81
    ReceivePri3Pause1USCount = 82
    ReceivePri4Pause1USCount = 83
    ReceivePri5Pause1USCount = 84
    ReceivePri6Pause1USCount = 85
    ReceivePri7Pause1USCount = 86
    ReceiveStandardPause1USCount = 87
    FramesTruncated = 88


class PortCollector(RpcCollectorBase):
    """
    Custom Prometheus collector that collects front-panel port metrics
    using the Barefoot PAL RPC.
    """

    rx_frame_length_buckets = {
        "<64": PalStat.FramesReceivedLength_lt_64,
        "64": PalStat.FramesReceivedLength_eq_64,
        "65-127": PalStat.FramesReceivedLength_65_127,
        "128-255": PalStat.FramesReceivedLength_128_255,
        "256-511": PalStat.FramesReceivedLength_256_511,
        "512-1023": PalStat.FramesReceivedLength_512_1023,
        "1024-1518": PalStat.FramesReceivedLength_1024_1518,
        "1519-2047": PalStat.FramesReceivedLength_1519_2047,
        "2048-4095": PalStat.FramesReceivedLength_2048_4095,
        "4096-8191": PalStat.FramesReceivedLength_4096_8191,
        "8192-9215": PalStat.FramesReceivedLength_8192_9215,
        "9216": PalStat.FramesReceivedLength_9216,
    }

    tx_frame_length_buckets = {
        "<64": PalStat.FramesTransmittedLength_lt_64,
        "64": PalStat.FramesTransmittedLength_eq_64,
        "65-127": PalStat.FramesTransmittedLength_65_127,
        "128-255": PalStat.FramesTransmittedLength_128_255,
        "256-511": PalStat.FramesTransmittedLength_256_511,
        "512-1023": PalStat.FramesTransmittedLength_512_1023,
        "1024-1518": PalStat.FramesTransmittedLength_1024_1518,
        "1519-2047": PalStat.FramesTransmittedLength_1519_2047,
        "2048-4095": PalStat.FramesTransmittedLength_2048_4095,
        "4096-8191": PalStat.FramesTransmittedLength_4096_8191,
        "8192-9215": PalStat.FramesTransmittedLength_8192_9215,
        "9216": PalStat.FramesTransmittedLength_9216,
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
            labels=["port", "channel"],
        )
        port_stats_rx_bytes = CounterMetricFamily(
            "p4_switch_port_stats_rx_bytes",
            "Number of bytes received on the port",
            labels=["port", "channel"],
        )
        port_stats_tx_bytes = CounterMetricFamily(
            "p4_switch_port_stats_tx_bytes",
            "Number of bytes received on the port",
            labels=["port", "channel"],
        )
        port_stats_rx_frames_by_length = CounterMetricFamily(
            "p4_switch_port_stats_rx_frames",
            "Number of frames received on the port,"
            " grouped by frame length in bytes",
            labels=["port", "channel", "length"],
        )
        port_stats_tx_frames_by_length = CounterMetricFamily(
            "p4_switch_port_stats_tx_frames",
            "Number of frames transmitted on the port,"
            " grouped by frame length in bytes",
            labels=["port", "channel", "length"],
        )
        port_stats_rx_errors = CounterMetricFamily(
            "p4_switch_port_stats_rx_errors",
            "The total number of receive errors on the port",
            labels=["port", "channel"],
        )
        port_stats_tx_errors = CounterMetricFamily(
            "p4_switch_port_stats_tx_errors",
            "The total number of transmit errors on the port",
            labels=["port", "channel"],
        )
        port_stats_rx_frame_unicast = CounterMetricFamily(
            "p4_switch_port_stats_rx_unicast_frames",
            "The total number of unicast frames received on the port",
            labels=["port", "channel"],
        )
        port_stats_rx_frame_multicast = CounterMetricFamily(
            "p4_switch_port_stats_rx_multicast_frames",
            "The total number of multicast frames received on the port",
            labels=["port", "channel"],
        )
        port_stats_rx_frame_broadcast = CounterMetricFamily(
            "p4_switch_port_stats_rx_broadcast_frames",
            "The total number of broadcast frames received on the port",
            labels=["port", "channel"],
        )
        port_stats_tx_frame_unicast = CounterMetricFamily(
            "p4_switch_port_stats_tx_unicast_frames",
            "The total number of unicast frames transmitted on the port",
            labels=["port", "channel"],
        )
        port_stats_tx_frame_multicast = CounterMetricFamily(
            "p4_switch_port_stats_tx_multicast_frames",
            "The total number of multicast frames transmitted on the port",
            labels=["port", "channel"],
        )
        port_stats_tx_frame_broadcast = CounterMetricFamily(
            "p4_switch_port_stats_tx_broadcast_frames",
            "The total number of broadcast frames transmitted on the port",
            labels=["port", "channel"],
        )

        with self._get_rpc_client() as client:
            for port in self._iter_ports(client):
                fp_port = client.pal_port_dev_port_to_front_panel_port_get(
                    0, port
                )
                self._logger.debug(
                    "Port %d corresponds to front panel port %d/%d",
                    port,
                    fp_port.pal_front_port,
                    fp_port.pal_front_chnl,
                )

                labels = [
                    str(fp_port.pal_front_port),
                    str(fp_port.pal_front_chnl),
                ]

                port_up.add_metric(
                    labels,
                    float(client.pal_port_oper_status_get(0, port)),
                )

                stats = client.pal_port_all_stats_get(0, port)

                port_stats_rx_bytes.add_metric(
                    labels, float(stats.entry[PalStat.OctetsReceived])
                )
                port_stats_tx_bytes.add_metric(
                    labels, float(stats.entry[PalStat.OctetsTransmittedTotal])
                )

                for length, stat in self.rx_frame_length_buckets.items():
                    port_stats_rx_frames_by_length.add_metric(
                        [*labels, length], float(stats.entry[stat])
                    )

                for length, stat in self.tx_frame_length_buckets.items():
                    port_stats_tx_frames_by_length.add_metric(
                        [*labels, length], float(stats.entry[stat])
                    )

                port_stats_rx_errors.add_metric(
                    labels,
                    float(
                        stats.entry[PalStat.FramesReceivedAll]
                        - stats.entry[PalStat.FramesReceivedOK]
                    ),
                )

                port_stats_tx_errors.add_metric(
                    labels,
                    float(
                        stats.entry[PalStat.FramesTransmittedAll]
                        - stats.entry[PalStat.FramesTransmittedOK]
                    ),
                )

                port_stats_rx_frame_unicast.add_metric(
                    labels,
                    stats.entry[PalStat.FramesReceivedwithUnicastAddresses],
                )
                port_stats_rx_frame_multicast.add_metric(
                    labels,
                    stats.entry[PalStat.FramesReceivedwithMulticastAddresses],
                )
                port_stats_rx_frame_broadcast.add_metric(
                    labels,
                    stats.entry[PalStat.FramesReceivedwithBroadcastAddresses],
                )
                port_stats_tx_frame_unicast.add_metric(
                    labels, stats.entry[PalStat.FramesTransmittedUnicast]
                )
                port_stats_tx_frame_multicast.add_metric(
                    labels, stats.entry[PalStat.FramesTransmittedMulticast]
                )
                port_stats_tx_frame_broadcast.add_metric(
                    labels, stats.entry[PalStat.FramesTransmittedBroadcast]
                )

        yield from [
            port_up,
            port_stats_rx_bytes,
            port_stats_tx_bytes,
            port_stats_rx_frames_by_length,
            port_stats_tx_frames_by_length,
            port_stats_rx_errors,
            port_stats_tx_errors,
            port_stats_rx_frame_unicast,
            port_stats_rx_frame_multicast,
            port_stats_rx_frame_broadcast,
            port_stats_tx_frame_unicast,
            port_stats_tx_frame_multicast,
            port_stats_tx_frame_broadcast,
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
