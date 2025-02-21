*********************
Install using Ansible
*********************

Installing the Ansible collection
=================================

First, add the ``ska_collections.ds_psi_exporters`` Ansible collection to your ``requirements.yml``:

.. code-block:: yaml
  :caption: requirements.yml

  collections:
    - name: https://gitlab.com/ska-telescope/ska-ds-psi-prometheus-exporters.git#/ansible/
      type: git
      version: 0.0.1

Update the ``version`` to match the Git tag you want to install,
or set it to ``main`` to use a pre-release version of the collection.

Then, install the collection by running:

.. code-block:: console
    
  $ ansible-galaxy install -r requirements.yml

Deploying the exporters
=======================

Each Prometheus exporter can be deployed using their respective Ansible role.
For example, to deploy :doc:`../exporters/p4_switch_exporter`, add the following to a playbook:

.. code-block:: yaml
  :caption: playbook.yml

  - name: Deploy ska-p4-switch-exporter
    hosts: target_hosts
    roles:
      - ska_collections.ds_psi_exporters.p4_switch_exporter

Running this playbook will:

- Create a Python virtual environment on the target hosts;
- Install the ``ska-ds-psi-prometheus-exporters`` package in the virtual environment;
- Create a ``ska-p4-switch-exporter.service`` systemd unit to run the exporter as a service.

Exporter configuration
======================

Each exporter can be configured by overriding the Ansible vars in the respective roles.
Check out the project repository to see the vars available for each role.
