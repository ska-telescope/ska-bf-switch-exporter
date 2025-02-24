# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog][keepachangelog], and this project adheres to [Semantic Versioning][semver].

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
