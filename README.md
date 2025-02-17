# SKA Barefoot Switch Exporter

Custom Prometheus metrics exporter to report metrics for Barefoot P4 switches.

## Usage

```sh
$ bf_switch_exporter --help
Usage: bf_switch_exporter [OPTIONS]

  Run the Barefoot Switch Prometheus exporter.

Options:
  --sde-install-dir DIRECTORY     Path to the Barefoot SDE install directory
                                  [required]
  --rpc-host TEXT                 Hostname or IP address of the Barefoot RPC
                                  server  [required]
  --rpc-port INTEGER              Port number of the Barefoot RPC server
  --web-port INTEGER              Port number on which to expose metrics
  --log-level [DEBUG|INFO|WARNING|ERROR]
                                  Logging level used to configure the Python
                                  logger
  --help                          Show this message and exit.
```
