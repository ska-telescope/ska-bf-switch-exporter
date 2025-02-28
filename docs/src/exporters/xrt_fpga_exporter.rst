*********************
ska-xrt-fpga-exporter
*********************

The ``ska-xrt-fpga-exporter`` exposes metrics extracted from the LOW-CBF Alveo U55C FPGAs.
It does so by utilizing the Python bindings that come with the Xilinx XRT.


Prerequisites
=============

- The Xilinx XRT needs to be installed


Usage
=====

.. code-block:: console

  $ ska-xrt-fpga-exporter

.. note::

  Before starting the exporter, make sure the system environment is prepared for use with the XRT.
  Use the ``setup.sh`` script that comes with the XRT to do this:

  .. code-block:: console

    $ source /opt/xilinx/xrt/setup.sh


Command-line options
====================

:: 

  $ ska-xrt-fpga-exporter --help
  Usage: ska-xrt-fpga-exporter [OPTIONS]

    Run the SKA XRT FPGA Prometheus Exporter.

  Options:
    --version                       Show the version and exit.
    --web-port INTEGER              Port number on which to expose metrics
    --log-level [DEBUG|INFO|WARNING|ERROR]
                                    Logging level used to configure the Python
                                    logger
    --help                          Show this message and exit.

Example output
==============

::

  # HELP ska_xrt_fpga_exporter_info Information about the ska-xrt-fpga-exporter
  # TYPE ska_xrt_fpga_exporter_info gauge
  ska_xrt_fpga_exporter_info{python_version="3.10.2",xrt_branch="2022.2",xrt_build_date="2022-10-08 09:49:53",xrt_hash="43926231f7183688add2dccfd391b36a1f000bea",xrt_version="2.14.354",version="0.0.6"} 1.0
  # HELP xrt_fpga_info Information about the Xilinx XRT FPGA device
  # TYPE xrt_fpga_info gauge
  xrt_fpga_info{bdf="0000:d1:00.1",name="xilinx_u55c_gen3x16_xdma_base_3",serial="000000000000",xclbin_uuid="d0020813-8158-5f43-dbcd-7b7a7bfe44c8"} 1.0
  # HELP xrt_fpga_temperature_celsius Temperature of the Xilinx XRT FPGA device
  # TYPE xrt_fpga_temperature_celsius gauge
  xrt_fpga_temperature_celsius{bdf="0000:d1:00.1",description="PCB Top Front",location="pcb_top_front"} 26.0
  xrt_fpga_temperature_celsius{bdf="0000:d1:00.1",description="PCB Top Rear",location="pcb_top_rear"} 23.0
  xrt_fpga_temperature_celsius{bdf="0000:d1:00.1",description="Cage0",location="cage_temp_0"} 23.0
  xrt_fpga_temperature_celsius{bdf="0000:d1:00.1",description="FPGA",location="fpga0"} 28.0
  xrt_fpga_temperature_celsius{bdf="0000:d1:00.1",description="Int Vcc",location="int_vcc"} 31.0
  # HELP xrt_fpga_current_amps Current of the Xilinx XRT FPGA device
  # TYPE xrt_fpga_current_amps gauge
  xrt_fpga_current_amps{bdf="0000:d1:00.1",description="12 Volts Auxillary",location="12v_aux"} 0.336
  xrt_fpga_current_amps{bdf="0000:d1:00.1",description="12 Volts PCI Express",location="12v_pex"} 0.681
  xrt_fpga_current_amps{bdf="0000:d1:00.1",description="3.3 Volts PCI Express",location="3v3_pex"} 0.952
  xrt_fpga_current_amps{bdf="0000:d1:00.1",description="Internal FPGA Vcc",location="vccint"} 4.6
  xrt_fpga_current_amps{bdf="0000:d1:00.1",description="Internal FPGA Vcc IO",location="vccint_io"} 0.7
  # HELP xrt_fpga_voltage_volts Voltage of the Xilinx XRT FPGA device
  # TYPE xrt_fpga_voltage_volts gauge
  xrt_fpga_voltage_volts{bdf="0000:d1:00.1",description="12 Volts Auxillary",location="12v_aux"} 12.208
  xrt_fpga_voltage_volts{bdf="0000:d1:00.1",description="12 Volts PCI Express",location="12v_pex"} 12.2
  xrt_fpga_voltage_volts{bdf="0000:d1:00.1",description="3.3 Volts PCI Express",location="3v3_pex"} 3.288
  xrt_fpga_voltage_volts{bdf="0000:d1:00.1",description="Internal FPGA Vcc",location="vccint"} 0.851
  xrt_fpga_voltage_volts{bdf="0000:d1:00.1",description="Internal FPGA Vcc IO",location="vccint_io"} 0.851
  xrt_fpga_voltage_volts{bdf="0000:d1:00.1",description="5.5 Volts System",location="5v5_system"} 5.01
  xrt_fpga_voltage_volts{bdf="0000:d1:00.1",description="1.8 Volts Top",location="1v8_top"} 1.805
  xrt_fpga_voltage_volts{bdf="0000:d1:00.1",description="0.9 Volts Vcc",location="0v9_vcc"} 0.901
  xrt_fpga_voltage_volts{bdf="0000:d1:00.1",description="Mgt Vtt",location="mgt_vtt"} 1.2
  xrt_fpga_voltage_volts{bdf="0000:d1:00.1",description="3.3 Volts Vcc",location="3v3_vcc"} 3.359
  xrt_fpga_voltage_volts{bdf="0000:d1:00.1",description="1.2 Volts HBM",location="hbm_1v2"} 1.202
  xrt_fpga_voltage_volts{bdf="0000:d1:00.1",description="Vpp 2.5 Volts",location="vpp2v5"} 2.488
  # HELP xrt_fpga_power_watts Power consumption of the Xilinx XRT FPGA device
  # TYPE xrt_fpga_power_watts gauge
  xrt_fpga_power_watts{bdf="0000:d1:00.1"} 15.540264
  # HELP xrt_fpga_max_power_watts Maximum power consumption of the Xilinx XRT FPGA device
  # TYPE xrt_fpga_max_power_watts gauge
  xrt_fpga_max_power_watts{bdf="0000:d1:00.1"} 225.0
  # HELP xrt_fpga_power_warning Whether the power consumption of the Xilinx XRT FPGA device is raising a warning
  # TYPE xrt_fpga_power_warning gauge
  xrt_fpga_power_warning{bdf="0000:d1:00.1"} 1.0
