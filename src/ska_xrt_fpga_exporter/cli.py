"""
This is the main entrypoint of the application.
"""

import logging
import signal

import click
from prometheus_client import start_http_server
from prometheus_client.core import CollectorRegistry
from ska_ser_logging import configure_logging

from ska_xrt_fpga_exporter import release


@click.command(
    context_settings={
        "auto_envvar_prefix": "SKA_XRT_FPGA_EXPORTER",
    }
)
@click.version_option(release.version)
@click.option(
    "--web-port",
    type=int,
    default=9101,
    help="Port number on which to expose metrics",
)
@click.option(
    "--log-level",
    type=click.Choice(
        ["DEBUG", "INFO", "WARNING", "ERROR"],
        case_sensitive=False,
    ),
    default="INFO",
    help="Logging level used to configure the Python logger",
)
def run(
    web_port: int,
    log_level: str,
):
    """
    Run the SKA XRT FPGA Prometheus Exporter.
    """
    configure_logging(level=log_level)
    logger = logging.getLogger(__name__)
    logger.info("Starting SKA XRT FPGA Prometheus Exporter")

    # The collectors are imported lazily because they depend on pyxrt which
    # may not be available. Importing them at the top level would make all
    # CLI invocations raise an ImportError, which is annoying when you just
    # want to print help text.
    # pylint: disable-next=import-outside-toplevel
    from ska_xrt_fpga_exporter import (
        exporter_info_collector,
        xrt_fpga_collector,
    )

    registry = CollectorRegistry()
    exporter_info_collector.ExporterInfoCollector(
        logger=logger,
        registry=registry,
    )
    xrt_fpga_collector.XrtFpgaCollector(
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
