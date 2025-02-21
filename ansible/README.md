# SKA Digital Signal PSI Prometheus Exporters Ansible collection

This collection contains roles to automate the installation of the custom Prometheus exporters found in this repository.

## Installation

To install, add the following to your `requirements.yml` and then run `ansible-galaxy install -r requirements.yml`.


```yaml
collections:
  - name: https://gitlab.com/ska-telescope/ska-ds-psi-prometheus-exporters.git#/ansible/
    type: git
    version: 0.0.1
```

Update the `version` to match the Git tag you want to install, or set it to `main` to use a pre-release version of the collection.
