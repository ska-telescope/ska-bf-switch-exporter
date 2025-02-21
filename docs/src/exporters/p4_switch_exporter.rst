**********************
ska-p4-switch-exporter
**********************

The ``ska-p4-switch-exporter`` exposes metrics extracted from the LOW-CBF P4 switches.
It does so by connecting to the Barefoot RPC servers that come with the SDE.


Prerequisites
=============

- The Barefoot SDE needs to be installed and compiled.


Usage
=====

.. code-block:: console

  $ ska-p4-switch-exporter \
  --sde-lib-path /opt/intel/bf-sde/install/lib/python3.10/ \
  --rpc-host 192.168.0.1


Command-Line Options
====================

::

  $ ska-p4-switch-exporter --help
  Usage: ska-p4-switch-exporter [OPTIONS]

    Run the SKA P4 Switch Prometheus Exporter.

  Options:
    --version                       Show the version and exit.
    --sde-lib-path DIRECTORY        Path to the Barefoot SDE Python libraries
                                    [required]
    --rpc-host TEXT                 Hostname or IP address of the Barefoot RPC
                                    server  [required]
    --rpc-port INTEGER              Port number of the Barefoot RPC server
    --web-port INTEGER              Port number on which to expose metrics
    --log-level [DEBUG|INFO|WARNING|ERROR]
                                    Logging level used to configure the Python
                                    logger
    --help                          Show this message and exit.


Example output
==============

::

  # HELP ska_p4_switch_exporter_info Information about the ska-p4-switch_exporter
  # TYPE ska_p4_switch_exporter_info gauge
  ska_p4_switch_exporter_info{version="0.0.1"} 1.0
  # HELP p4_switch_system_temperature_degrees Temperature of the system
  # TYPE p4_switch_system_temperature_degrees gauge
  p4_switch_system_temperature_degrees{id="motherboard1"} 33.0
  p4_switch_system_temperature_degrees{id="motherboard2"} 28.5
  p4_switch_system_temperature_degrees{id="motherboard3"} 27.0
  p4_switch_system_temperature_degrees{id="motherboard4"} 25.0
  p4_switch_system_temperature_degrees{id="motherboard5"} 22.399999618530273
  p4_switch_system_temperature_degrees{id="tofino"} 46.0
  # HELP p4_switch_qsfp_present Whether a QSFP is connected to the port
  # TYPE p4_switch_qsfp_present gauge
  p4_switch_qsfp_present{port="1"} 1.0
  p4_switch_qsfp_present{port="2"} 0.0
  p4_switch_qsfp_present{port="3"} 0.0
  p4_switch_qsfp_present{port="4"} 0.0
  p4_switch_qsfp_present{port="5"} 0.0
  p4_switch_qsfp_present{port="6"} 0.0
  p4_switch_qsfp_present{port="7"} 0.0
  p4_switch_qsfp_present{port="8"} 0.0
  p4_switch_qsfp_present{port="9"} 0.0
  p4_switch_qsfp_present{port="10"} 0.0
  p4_switch_qsfp_present{port="11"} 0.0
  p4_switch_qsfp_present{port="12"} 0.0
  p4_switch_qsfp_present{port="13"} 0.0
  p4_switch_qsfp_present{port="14"} 0.0
  p4_switch_qsfp_present{port="15"} 0.0
  p4_switch_qsfp_present{port="16"} 0.0
  p4_switch_qsfp_present{port="17"} 0.0
  p4_switch_qsfp_present{port="18"} 0.0
  p4_switch_qsfp_present{port="19"} 0.0
  p4_switch_qsfp_present{port="20"} 0.0
  p4_switch_qsfp_present{port="21"} 0.0
  p4_switch_qsfp_present{port="22"} 0.0
  p4_switch_qsfp_present{port="23"} 0.0
  p4_switch_qsfp_present{port="24"} 0.0
  p4_switch_qsfp_present{port="25"} 0.0
  p4_switch_qsfp_present{port="26"} 0.0
  p4_switch_qsfp_present{port="27"} 0.0
  p4_switch_qsfp_present{port="28"} 0.0
  p4_switch_qsfp_present{port="29"} 0.0
  p4_switch_qsfp_present{port="30"} 0.0
  p4_switch_qsfp_present{port="31"} 0.0
  p4_switch_qsfp_present{port="32"} 0.0
  # HELP p4_switch_qsfp_channel_rx_power RX power on the QSFP channel
  # TYPE p4_switch_qsfp_channel_rx_power gauge
  p4_switch_qsfp_channel_rx_power{channel="1",port="1"} 1.2245
  p4_switch_qsfp_channel_rx_power{channel="2",port="1"} 1.2283
  p4_switch_qsfp_channel_rx_power{channel="3",port="1"} 1.1373
  p4_switch_qsfp_channel_rx_power{channel="4",port="1"} 1.105
  # HELP p4_switch_qsfp_channel_tx_power TX power on the QSFP channel
  # TYPE p4_switch_qsfp_channel_tx_power gauge
  p4_switch_qsfp_channel_tx_power{channel="1",port="1"} 0.0001
  p4_switch_qsfp_channel_tx_power{channel="2",port="1"} 0.0001
  p4_switch_qsfp_channel_tx_power{channel="3",port="1"} 0.0001
  p4_switch_qsfp_channel_tx_power{channel="4",port="1"} 0.0001
  # HELP p4_switch_qsfp_channel_count Number of channels active on the QSFP
  # TYPE p4_switch_qsfp_channel_count gauge
  p4_switch_qsfp_channel_count{port="1"} 4.0
  # HELP p4_switch_qsfp_info QSFP information
  # TYPE p4_switch_qsfp_info gauge
  p4_switch_qsfp_info{date_code="000000",part_number="QSFP28-SR4-100G",port="1",revision="1A",serial="S0000000000",vendor="FS"} 1.0
  # HELP p4_switch_qsfp_rx_power_alarm_max Maximum RX power on the QSFP channel above which an alarm should be raised
  # TYPE p4_switch_qsfp_rx_power_alarm_max gauge
  p4_switch_qsfp_rx_power_alarm_max{port="1"} 2.1878
  # HELP p4_switch_qsfp_rx_power_alarm_min Minimum RX power on the QSFP channel below which an alarm should be raised
  # TYPE p4_switch_qsfp_rx_power_alarm_min gauge
  p4_switch_qsfp_rx_power_alarm_min{port="1"} 0.0631
  # HELP p4_switch_qsfp_rx_power_warning_max Maximum RX power on the QSFP channel above which a warning should be raised
  # TYPE p4_switch_qsfp_rx_power_warning_max gauge
  p4_switch_qsfp_rx_power_warning_max{port="1"} 1.7378000000000002
  # HELP p4_switch_qsfp_rx_power_warning_min Minimum RX power on the QSFP channel below which a warning should be raised
  # TYPE p4_switch_qsfp_rx_power_warning_min gauge
  p4_switch_qsfp_rx_power_warning_min{port="1"} 0.1259
  # HELP p4_switch_qsfp_temperature_degrees Temperature of the QSFP
  # TYPE p4_switch_qsfp_temperature_degrees gauge
  p4_switch_qsfp_temperature_degrees{port="1"} 19.7734375
  # HELP p4_switch_qsfp_temperature_alarm_max_degrees Maximum temperature of the QSFP above which an alarm should be raised
  # TYPE p4_switch_qsfp_temperature_alarm_max_degrees gauge
  p4_switch_qsfp_temperature_alarm_max_degrees{port="1"} 75.0
  # HELP p4_switch_qsfp_temperature_alarm_min_degrees Minimum temperature of the QSFP below which an alarm should be raised
  # TYPE p4_switch_qsfp_temperature_alarm_min_degrees gauge
  p4_switch_qsfp_temperature_alarm_min_degrees{port="1"} -5.0
  # HELP p4_switch_qsfp_temperature_warning_max_degrees Maximum temperature of the QSFP above which a warning should be raised
  # TYPE p4_switch_qsfp_temperature_warning_max_degrees gauge
  p4_switch_qsfp_temperature_warning_max_degrees{port="1"} 70.0
  # HELP p4_switch_qsfp_temperature_warning_min_degrees Minimum temperature of the QSFP below which a warning should be raised
  # TYPE p4_switch_qsfp_temperature_warning_min_degrees gauge
  p4_switch_qsfp_temperature_warning_min_degrees{port="1"} 0.0
  # HELP p4_switch_qsfp_tx_power_alarm_max Maximum TX power on the QSFP channel above which an alarm should be raised
  # TYPE p4_switch_qsfp_tx_power_alarm_max gauge
  # HELP p4_switch_qsfp_tx_power_alarm_min Minimum TX power on the QSFP channel below which an alarm should be raised
  # TYPE p4_switch_qsfp_tx_power_alarm_min gauge
  # HELP p4_switch_qsfp_tx_power_warning_max Maximum TX power on the QSFP channel above which a warning should be raised
  # TYPE p4_switch_qsfp_tx_power_warning_max gauge
  # HELP p4_switch_qsfp_tx_power_warning_min Minimum TX power on the QSFP channel below which a warning should be raised
  # TYPE p4_switch_qsfp_tx_power_warning_min gauge
  # HELP p4_switch_qsfp_voltage_volts Voltage on the QSFP
  # TYPE p4_switch_qsfp_voltage_volts gauge
  p4_switch_qsfp_voltage_volts{port="1"} 3.2908
  # HELP p4_switch_qsfp_voltage_alarm_max_volts Maximum voltage of the QSFP above which an alarm should be raised
  # TYPE p4_switch_qsfp_voltage_alarm_max_volts gauge
  p4_switch_qsfp_voltage_alarm_max_volts{port="1"} 3.63
  # HELP p4_switch_qsfp_voltage_alarm_min_volts Minimum voltage of the QSFP below which an alarm should be raised
  # TYPE p4_switch_qsfp_voltage_alarm_min_volts gauge
  p4_switch_qsfp_voltage_alarm_min_volts{port="1"} 2.97
  # HELP p4_switch_qsfp_voltage_warning_max_volts Maximum voltage of the QSFP above which a warning should be raised
  # TYPE p4_switch_qsfp_voltage_warning_max_volts gauge
  p4_switch_qsfp_voltage_warning_max_volts{port="1"} 3.465
  # HELP p4_switch_qsfp_voltage_warning_min_volts Minimum voltage of the QSFP below which a warning should be raised
  # TYPE p4_switch_qsfp_voltage_warning_min_volts gauge
  p4_switch_qsfp_voltage_warning_min_volts{port="1"} 3.135
  # HELP p4_switch_port_up Operational status of the port
  # TYPE p4_switch_port_up gauge
  # HELP p4_switch_port_frames_received_total The total number of frames received on the port
  # TYPE p4_switch_port_frames_received_total counter
  # HELP p4_switch_port_frames_received_ok_total The number of frames received OK on the port
  # TYPE p4_switch_port_frames_received_ok_total counter
  # HELP p4_switch_port_frames_received_nok_total The number of frames received NOK on the port
  # TYPE p4_switch_port_frames_received_nok_total counter
  # HELP p4_switch_port_frames_transmitted_total The total number of frames transmitted on the port
  # TYPE p4_switch_port_frames_transmitted_total counter
  # HELP p4_switch_port_frames_transmitted_ok_total The number of frames transmitted OK on the port
  # TYPE p4_switch_port_frames_transmitted_ok_total counter
  # HELP p4_switch_port_frames_transmitted_nok_total The number of frames transmitted NOK on the port
  # TYPE p4_switch_port_frames_transmitted_nok_total counter
