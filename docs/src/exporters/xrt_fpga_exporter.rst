*********************
ska-xrt-fpga-exporter
*********************

The ``ska-xrt-fpga-exporter`` exposes metrics extracted from the LOW-CBF Alveo U55C FPGAs.
It does so by utilizing the Python bindings that come with the Xilinx XRT.

Prerequisites
=============

- The Xilinx XRT needs to be installed

Usage
=====

:: 

  $ ska-xrt-fpga-exporter --help
  Usage: ska-xrt-fpga-exporter [OPTIONS]

  Run the SKA XRT FPGA Prometheus Exporter.

  Options:
  --version                       Show the version and exit.
  --web-port INTEGER              Port number on which to expose metrics
  --log-level [DEBUG|INFO|WARNING|ERROR]
                                  Logging level used to configure the Python
                                  logger
  --help                          Show this message and exit.

.. note::

  Before starting the exporter, make sure the system environment is prepared for use with the XRT.
  Use the ``setup.sh`` script that comes with the XRT to do this:

  .. code-block:: console

    $ source /opt/xilinx/xrt/setup.sh
  