# SKA Barefoot Switch Exporter

Custom Prometheus metrics exporter to report metrics for Barefoot P4 switches.

## Usage

```sh
$ bf_switch_exporter --help
Usage: bf_switch_exporter [OPTIONS]

Options:
  --host TEXT     RPC host  [required]
  --port INTEGER  RPC port
  --help          Show this message and exit
```

## Development setup

### Prerequisites

- Apache Thrift

### Code generation

First, retrieve `pltfm_mgr_rpc.thrift` from the SDE and place it in the `thrift/` directory.

Then, generate the RPC code using:

```sh
thrift --gen py -out src -r thrift/pltfm_mgr_rpc.thrift
```
