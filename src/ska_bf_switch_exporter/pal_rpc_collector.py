"""
Module for the Barefoot port manager collector.
"""

import contextlib
import importlib
import logging
import pathlib
import sys

from prometheus_client.core import CounterMetricFamily, GaugeMetricFamily
from prometheus_client.registry import REGISTRY, Collector, CollectorRegistry
from thrift.protocol import TBinaryProtocol, TMultiplexedProtocol
from thrift.transport import TSocket, TTransport

__all__ = ["PalRpcCollector"]

# pylint: disable=too-few-public-methods
# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
# pylint: disable=too-many-positional-arguments
# pylint: disable=too-many-statements


class PalRpcCollector(Collector):
    """
    Custom Prometheus collector that collects metrics exposed by the
    Barefoot PAL RPC.
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

        for path in sde_install_dir.rglob("lib/python*/site-packages/tofino/"):
            self._logger.debug("Appending import path %s", path)
            sys.path.append(str(path))

        self._rpc_module = importlib.import_module("pal_rpc.pal")

        if registry:
            self._logger.info("Registering %s", self.__class__.__name__)
            registry.register(self)

    def collect(self):
        port_up = GaugeMetricFamily(
            "bf_switch_port_up",
            "Operational status of the port",
            labels=["port"],
        )
        port_frames_received_total = CounterMetricFamily(
            "bf_switch_port_frames_received_total",
            "The total number of frames received on the port",
            labels=["port"],
        )
        port_frames_received_ok = CounterMetricFamily(
            "bf_switch_port_frames_received_ok",
            "The number of frames received OK on the port",
            labels=["port"],
        )
        port_frames_received_nok = CounterMetricFamily(
            "bf_switch_port_frames_received_nok",
            "The number of frames received NOK on the port",
            labels=["port"],
        )
        port_frames_transmitted_total = CounterMetricFamily(
            "bf_switch_port_frames_transmitted_total",
            "The total number of frames transmitted on the port",
            labels=["port"],
        )
        port_frames_transmitted_ok = CounterMetricFamily(
            "bf_switch_port_frames_transmitted_ok",
            "The number of frames transmitted OK on the port",
            labels=["port"],
        )
        port_frames_transmitted_nok = CounterMetricFamily(
            "bf_switch_port_frames_transmitted_nok",
            "The number of frames transmitted NOK on the port",
            labels=["port"],
        )

        with self._rpc_client() as client:
            port = client.pal_port_get_first(0)
            while port:
                try:
                    if not client.pal_port_is_valid(0, port):
                        port = client.pal_port_get_next(0, port)
                        continue

                    fp_port = client.pal_port_dev_port_to_front_panel_port_get(
                        0, port
                    )
                    port_label = (
                        f"{fp_port.pal_front_port}/{fp_port.pal_front_chnl}"
                    )

                    port_up.add_metric(
                        [port_label], client.pal_port_oper_status_get(0, port)
                    )
                    port_frames_received_total.add_metric(
                        [port_label], client.pal_port_this_stat_get(0, port, 1)
                    )
                    port_frames_received_ok.add_metric(
                        [port_label], client.pal_port_this_stat_get(0, port, 0)
                    )
                    port_frames_received_nok.add_metric(
                        [port_label], client.pal_port_this_stat_get(0, port, 3)
                    )
                    port_frames_transmitted_total.add_metric(
                        [port_label],
                        client.pal_port_this_stat_get(0, port, 33),
                    )
                    port_frames_transmitted_ok.add_metric(
                        [port_label],
                        client.pal_port_this_stat_get(0, port, 32),
                    )
                    port_frames_transmitted_nok.add_metric(
                        [port_label],
                        client.pal_port_this_stat_get(0, port, 34),
                    )

                    port = client.pal_port_get_next(0, port)
                except self._rpc_module.InvalidPalOperation:
                    break

        yield from [
            port_up,
            port_frames_received_total,
            port_frames_received_ok,
            port_frames_received_nok,
            port_frames_transmitted_total,
            port_frames_transmitted_ok,
            port_frames_transmitted_nok,
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
                    "pal",
                )
            )
            yield client
        finally:
            if transport is not None:
                self._logger.debug("Disconnecting from RPC")
                transport.close()
