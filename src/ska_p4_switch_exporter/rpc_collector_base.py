# pylint: disable=import-error
# pylint: disable=too-few-public-methods
# pylint: disable=too-many-arguments
# pylint: disable=too-many-positional-arguments

"""
Abstract base class for collectors exporting metrics using a
Barefoot RPC client.
"""

import abc
import contextlib
import logging
from types import ModuleType

from prometheus_client.registry import Collector
from thrift.protocol import TBinaryProtocol, TMultiplexedProtocol
from thrift.transport import TSocket, TTransport

__all__ = [
    "RpcCollectorBase",
]


class RpcCollectorBase(Collector, abc.ABC):
    """
    Abstract base class for collectors exporting metrics using a
    Barefoot RPC client.
    """

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
