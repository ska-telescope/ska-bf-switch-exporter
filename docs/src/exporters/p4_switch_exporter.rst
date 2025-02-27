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

  # HELP ska_p4_switch_exporter_info Information about the ska-p4-switch-exporter
  # TYPE ska_p4_switch_exporter_info gauge
  ska_p4_switch_exporter_info{version="0.0.4"} 1.0
  # HELP p4_switch_system_temperature_celsius Temperature of the system
  # TYPE p4_switch_system_temperature_celsius gauge
  p4_switch_system_temperature_celsius{id="motherboard1"} 37.0
  p4_switch_system_temperature_celsius{id="motherboard2"} 32.0
  p4_switch_system_temperature_celsius{id="motherboard3"} 30.0
  p4_switch_system_temperature_celsius{id="motherboard4"} 28.0
  p4_switch_system_temperature_celsius{id="motherboard5"} 24.0
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
  p4_switch_qsfp_channel_rx_power{channel="1",port="1"} 0.9918
  p4_switch_qsfp_channel_rx_power{channel="2",port="1"} 1.0265
  p4_switch_qsfp_channel_rx_power{channel="3",port="1"} 1.0098
  p4_switch_qsfp_channel_rx_power{channel="4",port="1"} 1.0159
  # HELP p4_switch_qsfp_channel_tx_power TX power on the QSFP channel
  # TYPE p4_switch_qsfp_channel_tx_power gauge
  p4_switch_qsfp_channel_tx_power{channel="1",port="1"} 0.9254000000000001
  p4_switch_qsfp_channel_tx_power{channel="2",port="1"} 0.9125
  p4_switch_qsfp_channel_tx_power{channel="3",port="1"} 0.9247000000000001
  p4_switch_qsfp_channel_tx_power{channel="4",port="1"} 0.9189
  # HELP p4_switch_qsfp_channel_count Number of channels active on the QSFP
  # TYPE p4_switch_qsfp_channel_count gauge
  p4_switch_qsfp_channel_count{port="1"} 4.0
  # HELP p4_switch_qsfp_info QSFP information
  # TYPE p4_switch_qsfp_info gauge
  p4_switch_qsfp_info{date_code="000000",part_number="0000000000",port="1",revision="1A",serial="0000000000",vendor="Example"} 1.0
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
  p4_switch_qsfp_temperature_celsius{port="1"} 21.8671875
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
  p4_switch_port_up{port="1/0"} 1.0
  # HELP p4_switch_port_stats_frames_received_ok_total The total number of frames received without errors on the port
  # TYPE p4_switch_port_stats_frames_received_ok_total counter
  p4_switch_port_stats_frames_received_ok_total{port="1/0"} 2.381558e+06
  # HELP p4_switch_port_stats_frames_received_total The total number of frames received on the port
  # TYPE p4_switch_port_stats_frames_received_total counter
  p4_switch_port_stats_frames_received_total{port="1/0"} 2.381558e+06
  # HELP p4_switch_port_stats_frames_received_nok_total The total number of frames received with errors on the port
  # TYPE p4_switch_port_stats_frames_received_nok_total counter
  p4_switch_port_stats_frames_received_nok_total{port="1/0"} 0.0
  # HELP p4_switch_port_stats_bytes_received_ok_total The total number of bytes received in OK frames on the port
  # TYPE p4_switch_port_stats_bytes_received_ok_total counter
  p4_switch_port_stats_bytes_received_ok_total{port="1/0"} 1.67862914e+08
  # HELP p4_switch_port_stats_bytes_received_total The total number of bytes received on the port
  # TYPE p4_switch_port_stats_bytes_received_total counter
  p4_switch_port_stats_bytes_received_total{port="1/0"} 1.67862914e+08
  # HELP p4_switch_port_stats_frames_received_unicast_total The total number of unicast frames received on the port
  # TYPE p4_switch_port_stats_frames_received_unicast_total counter
  p4_switch_port_stats_frames_received_unicast_total{port="1/0"} 9.0
  # HELP p4_switch_port_stats_frames_received_multicast_total The total number of multicast frames received on the port
  # TYPE p4_switch_port_stats_frames_received_multicast_total counter
  p4_switch_port_stats_frames_received_multicast_total{port="1/0"} 2.381549e+06
  # HELP p4_switch_port_stats_frames_received_broadcast_total The total number of broadcast frames received on the port
  # TYPE p4_switch_port_stats_frames_received_broadcast_total counter
  p4_switch_port_stats_frames_received_broadcast_total{port="1/0"} 0.08.0
  # HELP p4_switch_port_stats_frames_received_length_less_than_64_total The total number of frames with a length of less than 64 bytes received on the port
  # TYPE p4_switch_port_stats_frames_received_length_less_than_64_total counter
  p4_switch_port_stats_frames_received_length_less_than_64_total{port="1/0"} 0.00
  # HELP p4_switch_port_stats_frames_received_length_64_total The total number of frames with a length of exactly 64 bytes received on the port
  # TYPE p4_switch_port_stats_frames_received_length_64_total counter
  p4_switch_port_stats_frames_received_length_64_total{port="1/0"} 508716.0
  # HELP p4_switch_port_stats_frames_received_length_65_127_total The total number of frames with a length of 65 to 127 bytes received on the port
  # TYPE p4_switch_port_stats_frames_received_length_65_127_total counter
  p4_switch_port_stats_frames_received_length_65_127_total{port="1/0"} 1.871844e+06
  # HELP p4_switch_port_stats_frames_received_length_128_255_total The total number of frames with a length of 128 to 255 bytes received on the port
  # TYPE p4_switch_port_stats_frames_received_length_128_255_total counter
  p4_switch_port_stats_frames_received_length_128_255_total{port="1/0"} 0.00
  # HELP p4_switch_port_stats_frames_received_length_256_511_total The total number of frames with a length of 256 to 511 bytes received on the port
  # TYPE p4_switch_port_stats_frames_received_length_256_511_total counter
  p4_switch_port_stats_frames_received_length_256_511_total{port="1/0"} 998.00
  # HELP p4_switch_port_stats_frames_received_length_512_1023_total The total number of frames with a length of 512 to 1023 bytes received on the port
  # TYPE p4_switch_port_stats_frames_received_length_512_1023_total counter
  p4_switch_port_stats_frames_received_length_512_1023_total{port="1/0"} 0.00
  # HELP p4_switch_port_stats_frames_received_length_1024_1518_total The total number of frames with a length of 1024 to 1518 bytes received on the port
  # TYPE p4_switch_port_stats_frames_received_length_1024_1518_total counter
  p4_switch_port_stats_frames_received_length_1024_1518_total{port="1/0"} 0.00
  # HELP p4_switch_port_stats_frames_received_length_1519_2047_total The total number of frames with a length of 1519 to 2047 bytes received on the port
  # TYPE p4_switch_port_stats_frames_received_length_1519_2047_total counter
  p4_switch_port_stats_frames_received_length_1519_2047_total{port="1/0"} 0.00
  # HELP p4_switch_port_stats_frames_received_length_2048_4095_total The total number of frames with a length of 2048 to 4095 bytes received on the port
  # TYPE p4_switch_port_stats_frames_received_length_2048_4095_total counter
  p4_switch_port_stats_frames_received_length_2048_4095_total{port="1/0"} 0.0
  # HELP p4_switch_port_stats_frames_received_length_4096_8191_total The total number of frames with a length of 4096 to 8191 bytes received on the port
  # TYPE p4_switch_port_stats_frames_received_length_4096_8191_total counter
  p4_switch_port_stats_frames_received_length_4096_8191_total{port="1/0"} 0.0
  # HELP p4_switch_port_stats_frames_received_length_8192_9215_total The total number of frames with a length of 8192 to 9215 bytes received on the port
  # TYPE p4_switch_port_stats_frames_received_length_8192_9215_total counter
  p4_switch_port_stats_frames_received_length_8192_9215_total{port="1/0"} 0.00
  # HELP p4_switch_port_stats_frames_received_length_9216_total The total number of frames with a length of 9216 bytes received on the port
  # TYPE p4_switch_port_stats_frames_received_length_9216_total counter
  p4_switch_port_stats_frames_received_length_9216_total{port="1/0"} 0.00
  # HELP p4_switch_port_stats_frames_transmitted_ok_total The total number of frames transmitted without errors on the port
  # TYPE p4_switch_port_stats_frames_transmitted_ok_total counter
  p4_switch_port_stats_frames_transmitted_ok_total{port="1/0"} 4.465161e+06
  # HELP p4_switch_port_stats_frames_transmitted_total The total number of frames transmitted on the port
  # TYPE p4_switch_port_stats_frames_transmitted_total counter
  p4_switch_port_stats_frames_transmitted_total{port="1/0"} 4.465161e+06
  # HELP p4_switch_port_stats_frames_transmitted_nok_total The total number of frames transmitted with errors on the port
  # TYPE p4_switch_port_stats_frames_transmitted_nok_total counter
  p4_switch_port_stats_frames_transmitted_nok_total{port="1/0"} 0.00
  # HELP p4_switch_port_stats_bytes_transmitted_ok_total The total number of bytes transmitted without error on the port
  # TYPE p4_switch_port_stats_bytes_transmitted_ok_total counter
  p4_switch_port_stats_bytes_transmitted_ok_total{port="1/0"} 1.6638732864e+010
  # HELP p4_switch_port_stats_bytes_transmitted_total The total number of bytes transmitted on the port
  # TYPE p4_switch_port_stats_bytes_transmitted_total counter
  p4_switch_port_stats_bytes_transmitted_total{port="1/0"} 1.6638732864e+010
  # HELP p4_switch_port_stats_frames_transmitted_unicast_total The total number of unicast frames transmitted on the port
  # TYPE p4_switch_port_stats_frames_transmitted_unicast_total counter
  p4_switch_port_stats_frames_transmitted_unicast_total{port="1/0"} 2.608128e+06
  # HELP p4_switch_port_stats_frames_transmitted_multicast_total The total number of multicast frames transmitted on the port
  # TYPE p4_switch_port_stats_frames_transmitted_multicast_total counter
  p4_switch_port_stats_frames_transmitted_multicast_total{port="1/0"} 1.856655e+06
  # HELP p4_switch_port_stats_frames_transmitted_broadcast_total The total number of broadcast frames transmitted on the port
  # TYPE p4_switch_port_stats_frames_transmitted_broadcast_total counter
  p4_switch_port_stats_frames_transmitted_broadcast_total{port="1/0"} 378.0344.0
  # HELP p4_switch_port_stats_frames_transmitted_length_less_than_64_total The total number of frames with a length of less than 64 bytes transmitted on the port
  # TYPE p4_switch_port_stats_frames_transmitted_length_less_than_64_total counter
  p4_switch_port_stats_frames_transmitted_length_less_than_64_total{port="1/0"} 0.00
  # HELP p4_switch_port_stats_frames_transmitted_length_64_total The total number of frames with a length of exactly 64 bytes transmitted on the port
  # TYPE p4_switch_port_stats_frames_transmitted_length_64_total counter
  p4_switch_port_stats_frames_transmitted_length_64_total{port="1/0"} 1.857033e+06
  # HELP p4_switch_port_stats_frames_transmitted_length_65_127_total The total number of frames with a length of 65 to 127 bytes transmitted on the port
  # TYPE p4_switch_port_stats_frames_transmitted_length_65_127_total counter
  p4_switch_port_stats_frames_transmitted_length_65_127_total{port="1/0"} 0.0
  # HELP p4_switch_port_stats_frames_transmitted_length_128_255_total The total number of frames with a length of 128 to 255 bytes transmitted on the port
  # TYPE p4_switch_port_stats_frames_transmitted_length_128_255_total counter
  p4_switch_port_stats_frames_transmitted_length_128_255_total{port="1/0"} 0.0344.0
  # HELP p4_switch_port_stats_frames_transmitted_length_256_511_total The total number of frames with a length of 256 to 511 bytes transmitted on the port
  # TYPE p4_switch_port_stats_frames_transmitted_length_256_511_total counter
  p4_switch_port_stats_frames_transmitted_length_256_511_total{port="1/0"} 0.00
  # HELP p4_switch_port_stats_frames_transmitted_length_512_1023_total The total number of frames with a length of 512 to 1023 bytes transmitted on the port
  # TYPE p4_switch_port_stats_frames_transmitted_length_512_1023_total counter
  p4_switch_port_stats_frames_transmitted_length_512_1023_total{port="1/0"} 0.00
  # HELP p4_switch_port_stats_frames_transmitted_length_1024_1518_total The total number of frames with a length of 1024 to 1518 bytes transmitted on the port
  # TYPE p4_switch_port_stats_frames_transmitted_length_1024_1518_total counter
  p4_switch_port_stats_frames_transmitted_length_1024_1518_total{port="1/0"} 0.00
  # HELP p4_switch_port_stats_frames_transmitted_length_1519_2047_total The total number of frames with a length of 1519 to 2047 bytes transmitted on the port
  # TYPE p4_switch_port_stats_frames_transmitted_length_1519_2047_total counter
  p4_switch_port_stats_frames_transmitted_length_1519_2047_total{port="1/0"} 0.00
  # HELP p4_switch_port_stats_frames_transmitted_length_2048_4095_total The total number of frames with a length of 2048 to 4095 bytes transmitted on the port
  # TYPE p4_switch_port_stats_frames_transmitted_length_2048_4095_total counter
  p4_switch_port_stats_frames_transmitted_length_2048_4095_total{port="1/0"} 0.00
  # HELP p4_switch_port_stats_frames_transmitted_length_4096_8191_total The total number of frames with a length of 4096 to 8191 bytes transmitted on the port
  # TYPE p4_switch_port_stats_frames_transmitted_length_4096_8191_total counter
  p4_switch_port_stats_frames_transmitted_length_4096_8191_total{port="1/0"} 2.608128e+060
  # HELP p4_switch_port_stats_frames_transmitted_length_8192_9215_total The total number of frames with a length of 8192 to 9215 bytes transmitted on the port
  # TYPE p4_switch_port_stats_frames_transmitted_length_8192_9215_total counter
  p4_switch_port_stats_frames_transmitted_length_8192_9215_total{port="1/0"} 0.0
  # HELP p4_switch_port_stats_frames_transmitted_length_9216_total The total number of frames with a length of 9216 bytes transmitted on the port
  # TYPE p4_switch_port_stats_frames_transmitted_length_9216_total counter
  p4_switch_port_stats_frames_transmitted_length_9216_total{port="1/0"} 0.00
