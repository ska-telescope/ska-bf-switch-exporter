# pylint: disable=invalid-name
# pylint: disable=redefined-builtin

"""Release information for ska_xrt_fpga_exporter"""

import importlib.metadata

name = __package__
try:
    version = importlib.metadata.version("ska-ds-psi-prometheus-exporters")
except importlib.metadata.PackageNotFoundError:
    version = "unknown"
version_info = version.split(".")
description = "Prometheus exporter for SKA XRT FPGAs"
