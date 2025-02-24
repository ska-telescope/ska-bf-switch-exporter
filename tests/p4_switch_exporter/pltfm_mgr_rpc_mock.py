# pylint: disable=missing-function-docstring
"""
Mock for the BF SDE ``pltfm_mgr_rpc.pltfm_mgr_rpc`` module.
"""

from dataclasses import dataclass


@dataclass
class FakeSysTmp:
    """
    Container used for system temperatures.
    """

    tmp1 = 40.0
    tmp2 = 41.1
    tmp3 = 39.9
    tmp4 = 40.8
    tmp5 = 40.2
    tmp6 = 47.5


@dataclass
class Thresholds:
    """
    Thresholds for a single value.
    """

    highalarm: float
    lowalarm: float
    highwarning: float
    lowwarning: float


@dataclass
class FakeQSFPThresholds:
    """
    Container for QSFP thresholds.
    """

    temp: Thresholds | None = None
    vcc: Thresholds | None = None
    rx_pwr: Thresholds | None = None
    tx_pwr: Thresholds | None = None

    @property
    def temp_is_set(self):
        return self.temp is not None

    @property
    def vcc_is_set(self):
        return self.vcc is not None

    @property
    def rx_pwr_is_set(self):
        return self.rx_pwr is not None

    @property
    def tx_pwr_is_set(self):
        return self.tx_pwr is not None


class Client:
    """
    Mock implementation of ``pltfm_mgr_rpc.pltfm_mgr_rpc.Client``.

    This implementation hard-codes the values returned by the RPC,
    to allow for some variation in which behavior is triggered when collecting
    metrics.
    """

    def __init__(self, *args, **kwargs):  # pylint: disable=unused-argument
        pass

    def pltfm_mgr_sys_tmp_get(self):
        return FakeSysTmp()

    def pltfm_mgr_qsfp_get_max_port(self):
        # Designed to return `N + 1`, so in this case the ports are [1,2,3,4,5]
        return 6

    def pltfm_mgr_qsfp_presence_get(self, port: int):
        self._validate_port(port)

        # Make ~50% of the ports connected
        return port % 2 == 1

    def pltfm_mgr_qsfp_chan_count_get(self, port: int):
        self._validate_port(port)
        self._validate_qsfp_present(port)

        # Port 1 has 1 channel, port 2 has 2 channels, etc.
        return port

    def pltfm_mgr_qsfp_info_get(self, port: int):
        self._validate_port(port)
        self._validate_qsfp_present(port)

        # This method normally returns a hex-encoded byte string containing
        # QSFP information. This is quite a complex mechanism, so here we
        # just returns one big string containing the port number repeatedly.
        #
        # Let's also test the case where we can't decode the information,
        # by returning an invalid hex string on one of the ports.
        if port > 3:
            return "notvalid" * 64

        port_str = str(port)
        return bytes.hex(
            bytes(port_str * (256 // len(port_str)), encoding="utf-8")
        )

    def pltfm_mgr_qsfp_temperature_get(self, port: int):
        self._validate_port(port)
        self._validate_qsfp_present(port)

        return 10 * port

    def pltfm_mgr_qsfp_voltage_get(self, port: int):
        self._validate_port(port)
        self._validate_qsfp_present(port)

        return 12

    def pltfm_mgr_qsfp_thresholds_get(self, port: int):
        self._validate_port(port)
        self._validate_qsfp_present(port)

        # Cover multiple scenarios:
        # - Port 1 has no thresholds set
        # - Port 3 has some thresholds set
        # - Port 5 has all thresholds set
        thresholds = FakeQSFPThresholds()

        if port > 1:
            thresholds.temp = Thresholds(
                highalarm=20 * port,
                lowalarm=0,
                highwarning=15 * port,
                lowwarning=5 * port,
            )
            thresholds.vcc = Thresholds(
                highalarm=10,
                lowalarm=0,
                highwarning=8,
                lowwarning=1,
            )

        if port > 3:
            thresholds.rx_pwr = Thresholds(
                highalarm=9 * port,
                lowalarm=-1,
                highwarning=8 * port,
                lowwarning=0,
            )
            thresholds.tx_pwr = Thresholds(
                highalarm=10 * port,
                lowalarm=0,
                highwarning=9 * port,
                lowwarning=1,
            )

        return thresholds

    def pltfm_mgr_qsfp_chan_rx_pwr_get(self, port: int):
        self._validate_port(port)
        self._validate_qsfp_present(port)

        num_chans = self.pltfm_mgr_qsfp_chan_count_get(port)
        return [port * chan for chan in range(1, num_chans + 1)]

    def pltfm_mgr_qsfp_chan_tx_pwr_get(self, port: int):
        self._validate_port(port)
        self._validate_qsfp_present(port)

        num_chans = self.pltfm_mgr_qsfp_chan_count_get(port)
        return [port * chan + 1 for chan in range(1, num_chans + 1)]

    def _validate_port(self, port: int):
        if port >= self.pltfm_mgr_qsfp_get_max_port():
            raise ValueError(f"Invalid port {port}")

    def _validate_qsfp_present(self, port: int):
        if not self.pltfm_mgr_qsfp_presence_get(port):
            raise ValueError(f"No QSFP in port {port}")

    def _validate_channel(self, port: int, chan: int):
        if chan >= self.pltfm_mgr_qsfp_chan_count_get(port):
            raise ValueError(f"Invalid channel {chan} for port {port}")
