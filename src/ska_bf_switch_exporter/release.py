# pylint: disable=invalid-name
# pylint: disable=redefined-builtin

"""Release information for ska_bf_switch_exporter"""

import importlib.metadata

name = __package__
try:
    version = importlib.metadata.version(__package__)
except importlib.metadata.PackageNotFoundError:
    version = "unknown"
version_info = version.split(".")
description = "Prometheus exporter for SKA Barefoot P4 switches"
