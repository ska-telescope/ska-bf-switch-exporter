**********************
ska-p4-switch-exporter
**********************

The ``ska-p4-switch-exporter`` exposes metrics extracted from the LOW-CBF P4 switches.
It does so by connecting to the Barefoot RPC servers that come with the SDE.

Prerequisites
=============

- The Barefoot SDE needs to be installed and compiled.

Usage
=====

::

  $ ska-p4-switch-exporter --help
  Usage: ska-p4-switch-exporter [OPTIONS]

  Run the SKA P4 Switch Prometheus Exporter.

  Options:
  --version                       Show the version and exit.
  --sde-install-path DIRECTORY    Path to the Barefoot SDE install directory
                                  [required]
  --rpc-host TEXT                 Hostname or IP address of the Barefoot RPC
                                  server
  --rpc-port INTEGER              Port number of the Barefoot RPC server
  --web-port INTEGER              Port number on which to expose metrics
  --log-level [DEBUG|INFO|WARNING|ERROR]
                                  Logging level used to configure the Python
                                  logger
  --help                          Show this message and exit.
