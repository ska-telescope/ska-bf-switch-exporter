# pylint: disable=no-member

"""
Pytest configuration for this test module.
"""

import sys
from unittest import mock

from . import pal_rpc_mock, pltfm_mgr_rpc_mock

pltfm_mgr_rpc = type(sys)("pltfm_mgr_rpc")
pltfm_mgr_rpc.pltfm_mgr_rpc = pltfm_mgr_rpc_mock
sys.modules["pltfm_mgr_rpc"] = pltfm_mgr_rpc

tofino = type(sys)("tofino")
tofino.pal_rpc = type(sys)("pal_rpc")
tofino.pal_rpc.pal = pal_rpc_mock
sys.modules["tofino"] = tofino
sys.modules["tofino.pal_rpc"] = tofino.pal_rpc

thrift = type(sys)("thrift")
thrift.protocol = type(sys)("protocol")
thrift.protocol.TBinaryProtocol = mock.MagicMock()
thrift.protocol.TMultiplexedProtocol = mock.MagicMock()
thrift.transport = type(sys)("transport")
thrift.transport.TSocket = mock.MagicMock()
thrift.transport.TTransport = mock.MagicMock()
sys.modules["thrift"] = thrift
sys.modules["thrift.protocol"] = thrift.protocol
sys.modules["thrift.transport"] = thrift.transport
