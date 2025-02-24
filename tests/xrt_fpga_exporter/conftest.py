"""
Pytest configuration for this test module.
"""

import sys

from . import pyxrt_mock

sys.modules["pyxrt"] = pyxrt_mock
