# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog][keepachangelog], and this project adheres to [Semantic Versioning][semver].

## Unreleased

### Added

The following metrics were added to the `ska-p4-switch-exporter`:

| Name                                                                | Description                                                                            |
| ------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| `p4_switch_port_stats_bytes_received_ok_total`                      | The total number of bytes received in OK frames on the port                            |
| `p4_switch_port_stats_bytes_received_total`                         | The total number of bytes received on the port                                         |
| `p4_switch_port_stats_bytes_transmitted_ok_total`                   | The total number of bytes transmitted without error on the port                        |
| `p4_switch_port_stats_bytes_transmitted_total`                      | The total number of bytes transmitted on the port                                      |
| `p4_switch_port_stats_frames_received_unicast_total`                | The total number of unicast frames received on the port                                |
| `p4_switch_port_stats_frames_received_multicast_total`              | The total number of multicast frames received on the port                              |
| `p4_switch_port_stats_frames_received_broadcast_total`              | The total number of broadcast frames received on the port                              |
| `p4_switch_port_stats_frames_received_length_less_than_64_total`    | The total number of frames with a length of less than 64 bytes received on the port    |
| `p4_switch_port_stats_frames_received_length_64_total`              | The total number of frames with a length of exactly 64 bytes received on the port      |
| `p4_switch_port_stats_frames_received_length_65_127_total`          | The total number of frames with a length of 65 to 127 bytes received on the port       |
| `p4_switch_port_stats_frames_received_length_128_255_total`         | The total number of frames with a length of 128 to 255 bytes received on the port      |
| `p4_switch_port_stats_frames_received_length_256_511_total`         | The total number of frames with a length of 256 to 511 bytes received on the port      |
| `p4_switch_port_stats_frames_received_length_512_1023_total`        | The total number of frames with a length of 512 to 1023 bytes received on the port     |
| `p4_switch_port_stats_frames_received_length_1024_1518_total`       | The total number of frames with a length of 1024 to 1518 bytes received on the port    |
| `p4_switch_port_stats_frames_received_length_1519_2047_total`       | The total number of frames with a length of 1519 to 2047 bytes received on the port    |
| `p4_switch_port_stats_frames_received_length_2048_4095_total`       | The total number of frames with a length of 2048 to 4095 bytes received on the port    |
| `p4_switch_port_stats_frames_received_length_4096_8191_total`       | The total number of frames with a length of 4096 to 8191 bytes received on the port    |
| `p4_switch_port_stats_frames_received_length_8192_9215_total`       | The total number of frames with a length of 8192 to 9215 bytes received on the port    |
| `p4_switch_port_stats_frames_received_length_9216_total`            | The total number of frames with a length of 9216 bytes received on the port            |
| `p4_switch_port_stats_frames_transmitted_unicast_total`             | The total number of unicast frames transmitted on the port                             |
| `p4_switch_port_stats_frames_transmitted_multicast_total`           | The total number of multicast frames transmitted on the port                           |
| `p4_switch_port_stats_frames_transmitted_broadcast_total`           | The total number of broadcast frames transmitted on the port                           |
| `p4_switch_port_stats_frames_transmitted_length_less_than_64_total` | The total number of frames with a length of less than 64 bytes transmitted on the port |
| `p4_switch_port_stats_frames_transmitted_length_64_total`           | The total number of frames with a length of exactly 64 bytes transmitted on the port   |
| `p4_switch_port_stats_frames_transmitted_length_65_127_total`       | The total number of frames with a length of 65 to 127 bytes transmitted on the port    |
| `p4_switch_port_stats_frames_transmitted_length_128_255_total`      | The total number of frames with a length of 128 to 255 bytes transmitted on the port   |
| `p4_switch_port_stats_frames_transmitted_length_256_511_total`      | The total number of frames with a length of 256 to 511 bytes transmitted on the port   |
| `p4_switch_port_stats_frames_transmitted_length_512_1023_total`     | The total number of frames with a length of 512 to 1023 bytes transmitted on the port  |
| `p4_switch_port_stats_frames_transmitted_length_1024_1518_total`    | The total number of frames with a length of 1024 to 1518 bytes transmitted on the port |
| `p4_switch_port_stats_frames_transmitted_length_1519_2047_total`    | The total number of frames with a length of 1519 to 2047 bytes transmitted on the port |
| `p4_switch_port_stats_frames_transmitted_length_2048_4095_total`    | The total number of frames with a length of 2048 to 4095 bytes transmitted on the port |
| `p4_switch_port_stats_frames_transmitted_length_4096_8191_total`    | The total number of frames with a length of 4096 to 8191 bytes transmitted on the port |
| `p4_switch_port_stats_frames_transmitted_length_8192_9215_total`    | The total number of frames with a length of 8192 to 9215 bytes transmitted on the port |
| `p4_switch_port_stats_frames_transmitted_length_9216_total`         | The total number of frames with a length of 9216 bytes transmitted on the port         |

### Changed

The following `ska-p4-switch-exporter` metrics have been renamed:

| Old name                                      | New name                                            |
| --------------------------------------------- | --------------------------------------------------- |
| `p4_switch_port_frames_received_total`        | `p4_switch_port_stats_frames_received_total`        |
| `p4_switch_port_frames_received_ok_total`     | `p4_switch_port_stats_frames_received_ok_total`     |
| `p4_switch_port_frames_received_nok_total`    | `p4_switch_port_stats_frames_received_nok_total`    |
| `p4_switch_port_frames_transmitted_total`     | `p4_switch_port_stats_frames_transmitted_total`     |
| `p4_switch_port_frames_transmitted_ok_total`  | `p4_switch_port_stats_frames_transmitted_ok_total`  |
| `p4_switch_port_frames_transmitted_nok_total` | `p4_switch_port_stats_frames_transmitted_nok_total` |

### Fixed

- `ska-p4-switch-exporter`: Fixed a small typo in the help text of the `ska_p4_switch_exporter_info` metric.
- The temperature metrics were suffixed with `_degrees`, which is technically not a unit and is ambiguous.
  These have been renamed to end with `_celsius` instead.

## 0.0.4

Release date: 2025-02-25

### Fixed

- The default versions for the `ska_collections.ds_psi_exporters.p4_switch_exporter`
  and `ska_collections.ds_psi_exporters.xrt_fpga_exporter` Ansible roles have been
  updated to match the current release version.
- The release process instructions in the repository `README.md` have been updated to
  make sure the Ansible role defaults are updated as well.

## 0.0.3

Release date: 2025-02-25

### Fixed

- The Ansible collection metadata was not updated to reflect the version change, so installing it would make it look like it was installing version `0.0.1` instead of `0.0.2`.
  The release process is now documented in the repository `README.md` so that manually updating the Ansible collection version is not forgotten.

## 0.0.2

Release date 2025-02-24

### Fixed

- The Ansible roles no longer fail due to an undefined role variable, which was only set when overriding the
  PyPi index for the `ska-ds-psi-prometheus-exporter` Python package.

## 0.0.1

Release date: 2025-02-24

### Added

- `ska-p4-switch-exporter`: Prometheus exporter that exposes metrics from P4 switches used in LOW-CBF.
- `ska-xrt-fpga-exporter`: Prometheus exporter that exposes metrics from Xilinx FPGAs, most notably the Alveo U55C used in LOW-CBF.

[keepachangelog]: https://keepachangelog.com/en/1.1.0/
[semver]: https://semver.org/spec/v2.0.0.html
