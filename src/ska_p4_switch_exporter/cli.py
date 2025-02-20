"""
This is the main entrypoint of the application.
"""

import logging
import pathlib
import signal
import sys

import click
from prometheus_client import start_http_server
from prometheus_client.core import CollectorRegistry
from ska_ser_logging import configure_logging

from ska_p4_switch_exporter.collectors import (
    ExporterInfoCollector,
    PalRpcCollector,
    PlatformManagerRpcCollector,
)


@click.command(
    context_settings={
        "auto_envvar_prefix": "SKA_P4_SWITCH_EXPORTER",
    }
)
@click.option(
    "--sde-install-dir",
    type=click.Path(
        exists=True,
        file_okay=False,
        dir_okay=True,
        resolve_path=True,
        path_type=pathlib.Path,
    ),
    required=True,
    help="Path to the Barefoot SDE install directory",
)
@click.option(
    "--rpc-host",
    type=str,
    required=True,
    help="Hostname or IP address of the Barefoot RPC server",
)
@click.option(
    "--rpc-port",
    type=int,
    default=9090,
    help="Port number of the Barefoot RPC server",
)
@click.option(
    "--web-port",
    type=int,
    default=9102,
    help="Port number on which to expose metrics",
)
@click.option(
    "--log-level",
    type=click.Choice(
        ["DEBUG", "INFO", "WARNING", "ERROR"], case_sensitive=False
    ),
    default="INFO",
    help="Logging level used to configure the Python logger",
)
def run(
    sde_install_dir: pathlib.Path,
    rpc_host: str,
    rpc_port: int,
    web_port: int,
    log_level: str,
):
    """
    Run the SKA P4 Switch Prometheus Exporter.
    """
    configure_logging(level=log_level)
    logger = logging.getLogger(__name__)
    logger.info("Starting SKA P4 Switch Prometheus Exporter")

    for path in sde_install_dir.rglob("lib/python*/site-packages/"):
        logger.debug("Appending import path %s", path)
        sys.path.append(str(path))

    for path in sde_install_dir.rglob("lib/python*/site-packages/tofino/"):
        logger.debug("Appending import path %s", path)
        sys.path.append(str(path))

    registry = CollectorRegistry()
    ExporterInfoCollector(
        logger=logger,
        registry=registry,
    )
    PlatformManagerRpcCollector(
        rpc_host=rpc_host,
        rpc_port=rpc_port,
        logger=logger,
        registry=registry,
    )
    PalRpcCollector(
        rpc_host=rpc_host,
        rpc_port=rpc_port,
        logger=logger,
        registry=registry,
    )

    logger.info("Starting HTTP server on port %d", web_port)
    server, server_thread = start_http_server(
        web_port,
        registry=registry,
    )

    def shutdown(*args, **kwargs):  # pylint: disable=unused-argument
        logger.info("Shutting down HTTP server")
        server.shutdown()
        server_thread.join(timeout=10)

        logger.info("Shutdown complete")

    shutdown_signals = [signal.SIGINT, signal.SIGTERM]
    for sig in shutdown_signals:
        logger.debug("Adding shutdown hook for %s", sig)
        signal.signal(sig, shutdown)

    logger.info("Exporter is running")
    signal.pause()


if __name__ == "__main__":
    run()  # pylint: disable=no-value-for-parameter
