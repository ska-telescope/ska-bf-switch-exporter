**********************
ska-p4-switch-exporter
**********************

Usage
=====

::

    $ ska-p4-switch-exporter --help
    Usage: ska-p4-switch-exporter [OPTIONS]

    Run the SKA P4 Switch Prometheus Exporter.

    Options:
    --version                       Show the version and exit.
    --sde-install-dir DIRECTORY     Path to the Barefoot SDE install directory
                                    [required]
    --rpc-host TEXT                 Hostname or IP address of the Barefoot RPC
                                    server
    --rpc-port INTEGER              Port number of the Barefoot RPC server
    --web-port INTEGER              Port number on which to expose metrics
    --log-level [DEBUG|INFO|WARNING|ERROR]
                                    Logging level used to configure the Python
                                    logger
    --help                          Show this message and exit.
