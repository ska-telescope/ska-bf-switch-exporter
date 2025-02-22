This data has been obtained from actual Xilinx U55C Alveo FPGAs, using the runtime `pyxrt` library.

The directory structure is designed to work with `tests/xrt_fpga_exporter/pyxrt_mock.py`,
so that it can provide the same API to the exporter when performing unit tests.

The content of each file exactly matches the value returned by `pyxrt`,
to make sure the mocked library acts as a drop-in replacement.

Fields that might be considered sensitive (such as serial numbers) have been replaced with dummy values.
