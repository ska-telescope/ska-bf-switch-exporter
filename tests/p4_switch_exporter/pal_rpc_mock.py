# pylint: disable=invalid-name
# pylint: disable=missing-function-docstring

"""
Mock for the BF SDE ``tofino.pal_rpc.pal`` module.
"""

import dataclasses
import random

STAT_COUNT = 89


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

        stats = list(
            self.pal_port_this_stat_get(dev_id, port, stat)
            for stat in range(STAT_COUNT)
        )
        return PortStats(entry=stats, entry_count=len(stats), status=0)

    def pal_port_this_stat_get(self, dev_id: int, port: int, stat_id: int):
        self._validate_dev_id(dev_id)
        self._validate_port(port)

        if stat_id >= STAT_COUNT:
            raise InvalidPalOperation(f"No stat with id {stat_id}")

        return random.randint(0, 10000)

    def _validate_dev_id(self, dev_id: int):
        if dev_id != self.dev_id:
            raise InvalidPalOperation(f"Invalid dev_id {dev_id}")

    def _validate_port(self, port: int):
        if port >= self.num_ports:
            raise InvalidPalOperation(f"Invalid port {port}")
