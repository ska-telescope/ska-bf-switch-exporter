# pylint: disable=invalid-name # Names have to match the pyxrt module

"""
Mock for the ``pyxrt`` module.
"""

import enum
import pathlib

test_data_path = pathlib.Path("tests/test_data/xrt_devices")


class xrt_info_device(str, enum.Enum):
    """
    Mock for the ``pyxrt.xrt_info_device`` attribute.

    The enum values correspond with the files in
    ``tests/test_data/xrt_devices/*/``, so that
    :py:meth:`FakeXrtDevice.get_info` can return the correct information
    based on the given selector.
    """

    bdf = "bdf"
    dynamic_regions = "dynamic_regions"
    electrical = "electrical"
    host = "host"
    interface_uuid = "interface_uuid"
    kdma = "kdma"
    m2m = "m2m"
    max_clock_frequency_mhz = "max_clock_frequency_mhz"
    mechanical = "mechanical"
    memory = "memory"
    name = "name"
    nodma = "nodma"
    offline = "offline"
    pcie_info = "pcie_info"
    platform = "platform"
    thermal = "thermal"
    vmr = "vmr"


class uuid:  # pylint: disable=too-few-public-methods
    """
    Mock for the ``pyxrt.uuid`` class.
    """

    def __init__(self, uuid_file_path: pathlib.Path) -> None:
        self._uuid_file_path = uuid_file_path

    def to_string(self):
        """
        Retrieve the uuid as a string.
        """
        return self._uuid_file_path.read_text(encoding="utf-8").strip()


class FakeXrtDevice:
    """
    Fake XRT device returned by :py:func:`device`.
    """

    def __init__(self, device_info_path: pathlib.Path):
        self._info_path = device_info_path

    def get_info(self, info_device: xrt_info_device) -> str:
        """
        Retrieve hard-coded device information for the given selector.
        """
        info_file = self._info_path / info_device.value
        return info_file.read_text(encoding="utf-8").strip()

    def get_xclbin_uuid(self) -> uuid:
        """
        Retrieve the hard-coded xclbin uuid.
        """
        return uuid(self._info_path / "xclbin_uuid")


def device(device_num: int):
    """
    Mock for the ``pyxrt.device`` function.

    The way the original function works is that it returns a device handle
    for the given ``device_num``, as long as ``device_num < len(devices)``.
    After that, it raises a :py:class:`RuntimeError`.

    This mechanism is relied on by the exporter, so the behavior is replicated
    in the mock function.
    """
    device_info_path = test_data_path / str(device_num)
    if device_info_path.exists():
        return FakeXrtDevice(device_info_path)

    raise RuntimeError(f"No device for device_num {device_num}")
