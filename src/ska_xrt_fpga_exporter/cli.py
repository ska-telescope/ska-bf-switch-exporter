"""
This is the main entrypoint of the application.
"""

import logging
import pathlib
import signal

import click
from prometheus_client import start_http_server
from prometheus_client.core import CollectorRegistry
from ska_ser_logging import configure_logging

from ska_xrt_fpga_exporter import release
from ska_xrt_fpga_exporter.collectors import (
    ExporterInfoCollector,
    XrtFpgaCollector,
)


@click.command(
    context_settings={
        "auto_envvar_prefix": "SKA_XRT_FPGA_EXPORTER",
    }
)
@click.version_option(release.version)
@click.option(
    "--xrt-install-dir",
    type=click.Path(
        exists=True,
        file_okay=False,
        dir_okay=True,
        resolve_path=True,
        path_type=pathlib.Path,
    ),
    default=pathlib.Path("/opt/xilinx/xrt"),
    help="Path to the Xilinx XRT install directory",
)
@click.option(
    "--web-port",
    type=int,
    default=9101,
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
    xrt_install_dir: pathlib.Path,
    web_port: int,
    log_level: str,
):
    """
    Run the SKA XRT FPGA Prometheus Exporter.
    """
    configure_logging(level=log_level)
    logger = logging.getLogger(__name__)
    logger.info("Starting SKA XRT FPGA Prometheus Exporter")

    registry = CollectorRegistry()
    ExporterInfoCollector(
        logger=logger,
        registry=registry,
    )
    XrtFpgaCollector(
        xrt_install_dir=xrt_install_dir,
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
