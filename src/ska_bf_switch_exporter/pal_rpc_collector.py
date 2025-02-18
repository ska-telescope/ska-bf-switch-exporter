"""
Module for the Barefoot port manager collector.
"""

import importlib
import logging

from prometheus_client.core import CounterMetricFamily, GaugeMetricFamily
from prometheus_client.registry import REGISTRY, CollectorRegistry

from ska_bf_switch_exporter.rpc_collector import RpcCollectorBase

__all__ = ["PalRpcCollector"]

# pylint: disable=too-few-public-methods
# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
# pylint: disable=too-many-positional-arguments
# pylint: disable=too-many-statements


class PalRpcCollector(RpcCollectorBase):
    """
    Custom Prometheus collector that collects metrics exposed by the
    Barefoot PAL RPC.
    """

    def __init__(
        self,
        rpc_host: str,
        rpc_port: int,
        logger: logging.Logger,
        registry: CollectorRegistry | None = REGISTRY,
    ):
        super().__init__(
            rpc_host=rpc_host,
            rpc_port=rpc_port,
            rpc_endpoint="pal",
            rpc_module=importlib.import_module("pal_rpc.pal"),
            logger=logger,
        )

        if registry:
            logger.info("Registering %s", self.__class__.__name__)
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

        with self._get_rpc_client() as client:
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
