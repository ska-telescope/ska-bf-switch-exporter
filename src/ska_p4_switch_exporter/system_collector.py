# pylint: disable=import-error
# pylint: disable=too-few-public-methods

"""
Custom Prometheus collector that collects system metrics using the
Barefoot platform manager RPC.
"""

import logging

from pltfm_mgr_rpc import pltfm_mgr_rpc
from prometheus_client.core import GaugeMetricFamily
from prometheus_client.registry import REGISTRY, CollectorRegistry

from ska_p4_switch_exporter.rpc_collector_base import RpcCollectorBase

__all__ = [
    "SystemCollector",
]


class SystemCollector(RpcCollectorBase):
    """
    Custom Prometheus collector that collects system metrics using the
    Barefoot platform manager RPC.
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

        with self._get_rpc_client() as client:
            temperatures = client.pltfm_mgr_sys_tmp_get()

            for i in range(5):
                label = f"motherboard{i+1}"
                attr = f"tmp{i+1}"
                system_temperature.add_metric(
                    [label], getattr(temperatures, attr)
                )

            system_temperature.add_metric(["tofino"], temperatures.tmp6)

        yield system_temperature
