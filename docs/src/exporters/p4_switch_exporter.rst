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
      --sde-install-path /opt/intel/bf-sde/install/ \
      --rpc-host 192.168.0.1


Command-Line Options
====================

::

  $ ska-p4-switch-exporter --help
  Usage: ska-p4-switch-exporter [OPTIONS]

    Run the SKA P4 Switch Prometheus Exporter.

  Options:
    --version                       Show the version and exit.
    --sde-install-path DIRECTORY    Path to the Barefoot SDE installation
                                    directory  [required]
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

  # HELP ska_p4_switch_exporter_info Information about the ska-p4-switch-exporter
  # TYPE ska_p4_switch_exporter_info gauge
  ska_p4_switch_exporter_info{python_version="3.10.2",sde_version="9.13.2",version="0.0.5"} 1.0
  # HELP p4_switch_system_temperature_celsius Temperature of the system
  # TYPE p4_switch_system_temperature_celsius gauge
  p4_switch_system_temperature_celsius{id="motherboard1"} 37.5
  p4_switch_system_temperature_celsius{id="motherboard2"} 33.0
  p4_switch_system_temperature_celsius{id="motherboard3"} 30.5
  p4_switch_system_temperature_celsius{id="motherboard4"} 28.5
  p4_switch_system_temperature_celsius{id="motherboard5"} 23.700000762939453
  p4_switch_system_temperature_celsius{id="tofino"} 52.0
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
  p4_switch_qsfp_channel_rx_power{channel="1",port="1"} 0.9897
  p4_switch_qsfp_channel_rx_power{channel="2",port="1"} 1.0321000000000002
  p4_switch_qsfp_channel_rx_power{channel="3",port="1"} 1.0055
  p4_switch_qsfp_channel_rx_power{channel="4",port="1"} 1.0115
  # HELP p4_switch_qsfp_channel_tx_power TX power on the QSFP channel
  # TYPE p4_switch_qsfp_channel_tx_power gauge
  p4_switch_qsfp_channel_tx_power{channel="1",port="1"} 0.9309000000000001
  p4_switch_qsfp_channel_tx_power{channel="2",port="1"} 0.9105
  p4_switch_qsfp_channel_tx_power{channel="3",port="1"} 0.9272
  p4_switch_qsfp_channel_tx_power{channel="4",port="1"} 0.9219
  # HELP p4_switch_qsfp_channel_count Number of channels active on the QSFP
  # TYPE p4_switch_qsfp_channel_count gauge
  p4_switch_qsfp_channel_count{port="1"} 4.0
  # HELP p4_switch_qsfp_info QSFP information
  # TYPE p4_switch_qsfp_info gauge
  p4_switch_qsfp_info{date_code="000000",part_number="00000000",port="1",revision="00",serial="0000000000",vendor="Example"} 1.0
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
  # HELP p4_switch_qsfp_temperature_celsius Temperature of the QSFP
  # TYPE p4_switch_qsfp_temperature_celsius gauge
  p4_switch_qsfp_temperature_celsius{port="1"} 22.8046875
  # HELP p4_switch_qsfp_temperature_alarm_max_celsius Maximum temperature of the QSFP above which an alarm should be raised
  # TYPE p4_switch_qsfp_temperature_alarm_max_celsius gauge
  p4_switch_qsfp_temperature_alarm_max_celsius{port="1"} 75.0
  # HELP p4_switch_qsfp_temperature_alarm_min_celsius Minimum temperature of the QSFP below which an alarm should be raised
  # TYPE p4_switch_qsfp_temperature_alarm_min_celsius gauge
  p4_switch_qsfp_temperature_alarm_min_celsius{port="1"} -5.0
  # HELP p4_switch_qsfp_temperature_warning_max_celsius Maximum temperature of the QSFP above which a warning should be raised
  # TYPE p4_switch_qsfp_temperature_warning_max_celsius gauge
  p4_switch_qsfp_temperature_warning_max_celsius{port="1"} 70.0
  # HELP p4_switch_qsfp_temperature_warning_min_celsius Minimum temperature of the QSFP below which a warning should be raised
  # TYPE p4_switch_qsfp_temperature_warning_min_celsius gauge
  p4_switch_qsfp_temperature_warning_min_celsius{port="1"} 0.0
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
  p4_switch_qsfp_voltage_volts{port="1"} 3.2972
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
  p4_switch_port_up{channel="0",port="1"} 1.0
  # HELP p4_switch_port_stats_rx_bytes_total Number of bytes received on the port
  # TYPE p4_switch_port_stats_rx_bytes_total counter
  p4_switch_port_stats_rx_bytes_total{channel="0",port="1"} 1.3886922e+09
  # HELP p4_switch_port_stats_tx_bytes_total Number of bytes received on the port
  # TYPE p4_switch_port_stats_tx_bytes_total counter
  p4_switch_port_stats_tx_bytes_total{channel="0",port="1"} 1.28657587776e+011
  # HELP p4_switch_port_stats_rx_frames_total Number of frames received on the port, grouped by frame length in bytes
  # TYPE p4_switch_port_stats_rx_frames_total counter
  p4_switch_port_stats_rx_frames_total{channel="0",length="<64",port="1"} 0.0
  p4_switch_port_stats_rx_frames_total{channel="0",length="64",port="1"} 4.12202e+06
  p4_switch_port_stats_rx_frames_total{channel="0",length="65-127",port="1"} 1.5563303e+07
  p4_switch_port_stats_rx_frames_total{channel="0",length="128-255",port="1"} 0.0
  p4_switch_port_stats_rx_frames_total{channel="0",length="256-511",port="1"} 8083.0
  p4_switch_port_stats_rx_frames_total{channel="0",length="512-1023",port="1"} 0.0
  p4_switch_port_stats_rx_frames_total{channel="0",length="1024-1518",port="1"} 0.0
  p4_switch_port_stats_rx_frames_total{channel="0",length="1519-2047",port="1"} 0.0
  p4_switch_port_stats_rx_frames_total{channel="0",length="2048-4095",port="1"} 0.0
  p4_switch_port_stats_rx_frames_total{channel="0",length="4096-8191",port="1"} 0.0
  p4_switch_port_stats_rx_frames_total{channel="0",length="8192-9215",port="1"} 0.0
  p4_switch_port_stats_rx_frames_total{channel="0",length="9216",port="1"} 0.0
  # HELP p4_switch_port_stats_tx_frames_total Number of frames transmitted on the port, grouped by frame length in bytes
  # TYPE p4_switch_port_stats_tx_frames_total counter
  p4_switch_port_stats_tx_frames_total{channel="0",length="<64",port="1"} 0.0
  p4_switch_port_stats_tx_frames_total{channel="0",length="64",port="1"} 1.5440091e+07
  p4_switch_port_stats_tx_frames_total{channel="0",length="65-127",port="1"} 0.0
  p4_switch_port_stats_tx_frames_total{channel="0",length="128-255",port="1"} 13824.0
  p4_switch_port_stats_tx_frames_total{channel="0",length="256-511",port="1"} 0.0
  p4_switch_port_stats_tx_frames_total{channel="0",length="512-1023",port="1"} 0.0
  p4_switch_port_stats_tx_frames_total{channel="0",length="1024-1518",port="1"} 0.0
  p4_switch_port_stats_tx_frames_total{channel="0",length="1519-2047",port="1"} 0.0
  p4_switch_port_stats_tx_frames_total{channel="0",length="2048-4095",port="1"} 1152.0
  p4_switch_port_stats_tx_frames_total{channel="0",length="4096-8191",port="1"} 2.0155392e+07
  p4_switch_port_stats_tx_frames_total{channel="0",length="8192-9215",port="1"} 0.0
  p4_switch_port_stats_tx_frames_total{channel="0",length="9216",port="1"} 0.0
  # HELP p4_switch_port_stats_rx_errors_total The total number of receive errors on the port
  # TYPE p4_switch_port_stats_rx_errors_total counter
  p4_switch_port_stats_rx_errors_total{channel="0",port="1"} 0.0
  # HELP p4_switch_port_stats_tx_errors_total The total number of transmit errors on the port
  # TYPE p4_switch_port_stats_tx_errors_total counter
  p4_switch_port_stats_tx_errors_total{channel="0",port="1"} 0.0
  # HELP p4_switch_port_stats_rx_unicast_frames_total The total number of unicast frames received on the port
  # TYPE p4_switch_port_stats_rx_unicast_frames_total counter
  p4_switch_port_stats_rx_unicast_frames_total{channel="0",port="1"} 172.0
  # HELP p4_switch_port_stats_rx_multicast_frames_total The total number of multicast frames received on the port
  # TYPE p4_switch_port_stats_rx_multicast_frames_total counter
  p4_switch_port_stats_rx_multicast_frames_total{channel="0",port="1"} 1.96932e+07
  # HELP p4_switch_port_stats_rx_broadcast_frames_total The total number of broadcast frames received on the port
  # TYPE p4_switch_port_stats_rx_broadcast_frames_total counter
  p4_switch_port_stats_rx_broadcast_frames_total{channel="0",port="1"} 34.0
  # HELP p4_switch_port_stats_tx_unicast_frames_total The total number of unicast frames transmitted on the port
  # TYPE p4_switch_port_stats_tx_unicast_frames_total counter
  p4_switch_port_stats_tx_unicast_frames_total{channel="0",port="1"} 2.0170368e+07
  # HELP p4_switch_port_stats_tx_multicast_frames_total The total number of multicast frames transmitted on the port
  # TYPE p4_switch_port_stats_tx_multicast_frames_total counter
  p4_switch_port_stats_tx_multicast_frames_total{channel="0",port="1"} 1.5439365e+07
  # HELP p4_switch_port_stats_tx_broadcast_frames_total The total number of broadcast frames transmitted on the port
  # TYPE p4_switch_port_stats_tx_broadcast_frames_total counter
  p4_switch_port_stats_tx_broadcast_frames_total{channel="0",port="1"} 726.0
  