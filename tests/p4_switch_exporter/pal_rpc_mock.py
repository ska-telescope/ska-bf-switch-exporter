# pylint: disable=invalid-name
# pylint: disable=missing-function-docstring

"""
Mock for the BF SDE ``tofino.pal_rpc.pal`` module.
"""

import dataclasses
import enum


class InvalidPalOperation(RuntimeError):
    """
    Error raised by the ``tofino.pal_rpc.pal`` module.
    """


@dataclasses.dataclass
class FrontPanelPort:
    """
    Mock implementation of the struct returned by
    ``tofino.pal_rpc.pal.Client.pal_port_dev_port_to_front_panel_port_get``.
    """

    pal_front_port: int
    pal_front_chnl: int


@dataclasses.dataclass
class PortStats:
    """
    Mock implementation of the struct returned by
    ``tofino.pal_rpc.pal.Client.pal_port_all_stats_get``.
    """

    entry: list[int]
    entry_count: int
    status: int


class Stat(enum.IntEnum):
    """
    Mock implementation of the enum values accepted by
    ``tofino.pal_rpc.pal.Client.pal_port_this_stat_get``.

    Note: these values are taken from the PAL RPC thrift definition.
    """

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


class Client:
    """
    Mock for the ``tofino.pal_rpc.pal.Client`` class.
    """

    dev_id = 0
    num_ports = 16

    def __init__(self, *args, **kwargs):
        pass

    def pal_port_get_first(self, dev_id: int):
        self._validate_dev_id(dev_id)
        return -10

    def pal_port_get_next(self, dev_id: int, current_port: int):
        self._validate_dev_id(dev_id)
        self._validate_port(current_port)

        next_port = current_port + 1
        if next_port < self.num_ports + 10:
            return next_port

        raise InvalidPalOperation("No more ports")

    def pal_port_is_valid(self, dev_id: int, port: int):
        self._validate_dev_id(dev_id)
        return 0 <= port < self.num_ports

    def pal_port_dev_port_to_front_panel_port_get(
        self,
        dev_id: int,
        port: int,
    ):
        self._validate_dev_id(dev_id)
        self._validate_port(port)

        return FrontPanelPort(
            pal_front_chnl=port % 4,
            pal_front_port=port // 4 + 1,
        )

    def pal_port_oper_status_get(self, dev_id: int, port: int):
        self._validate_dev_id(dev_id)
        self._validate_port(port)
        return int(port % 8 == 0)

    def pal_port_all_stats_get(self, dev_id: int, port: int):
        self._validate_dev_id(dev_id)
        self._validate_port(port)

        stats = list(s.value * 3 for s in Stat)
        return PortStats(entry=stats, entry_count=len(stats), status=0)

    def pal_port_this_stat_get(self, dev_id: int, port: int, stat_id: int):
        self._validate_dev_id(dev_id)
        self._validate_port(port)

        stat = next((s for s in Stat if s.value == stat_id), None)
        if stat is None:
            raise InvalidPalOperation(f"No stat with id {stat_id}")

        return stat_id * 3

    def _validate_dev_id(self, dev_id: int):
        if dev_id != self.dev_id:
            raise InvalidPalOperation(f"Invalid dev_id {dev_id}")

    def _validate_port(self, port: int):
        if port >= self.num_ports:
            raise InvalidPalOperation(f"Invalid port {port}")
