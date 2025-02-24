# SKA Digital Signal PSI Prometheus Exporters

Custom Prometheus metrics exporters used to monitor SKA hardware in the Digital Signal PSI.

## User documentation

User documentation for this project can be found at https://developer.skao.int/projects/ska-ds-psi-prometheus-exporters/.

## Developer instructions

### Prerequisites

This project requires the following to be installed on the development machine:

- Python 3.10
- Poetry 1.8
- Make

### Cloning the repository

To clone the repository with all of its submodules:

    git clone --recursive git@gitlab.com:ska-telescope/ska-ds-psi-prometheus-exporters.git

### Set up Poetry environment

To set up a local virtual environment and install the Python dependencies:

    poetry install

To activate the virtual environment:

    poetry shell

> [!NOTE]
> All subsequent `make` targets in this README assume that they are run from within the virtual environment.

### Python development

#### Formatting and linting

This repository aims to follow the Python coding standards used by the SKAO, and therefore requires that the code is formatted and linted properly.

To auto-format the Python code according to the standards, run:

    make python-format

To lint the Python code, run:

    make python-lint

### Ansible development

This repository also contains an Ansible collection to automate the installation of the Prometheus exporters on SKA infrastructure, which can be found in [`ansible/`](./ansible/).

To lint the Ansible collection, run:

    make ansible-lint

### Documentation

The user documentation is built using Sphinx and can be found in [`docs/src/`](./docs/src/).

To build the documentation, run:

    make docs-build html

Note that documentation builds are incremental, to perform a full documentation build from scratch first clean the build directory with:

    make docs-build clean

### Creating a new release

Creating a new release largely follows the [SKAO software release procedure](https://developer.skao.int/en/latest/tutorial/release-management/automate-release-process.html#how-to-make-a-release).

#### Bump the release version

Bump the release version with:

    make bump-<major|minor|patch>-release

This should automatically update the version information in [`.release`](./.release) and [`pyproject.toml`](./pyproject.toml).

The following files should be updated **manually**:

- [`ansible/galaxy.yml`](./ansible/galaxy.yml)

#### Update the CHANGELOG.md

Manually update the [`CHANGELOG.md`](./CHANGELOG.md), replacing the "Unreleased" header with the version you're releasing.
Also add the release date to the section, see the previous releases for an example.

#### Commit and tag your changes

Commit your outstanding changes, and then create a git tag for the release using:

    make create-git-tag

Push the git tag using:

    make push-git-tag

## License information

See [LICENSE](./LICENSE).

## Support

For questions or remarks related to this project, contact [#team-topic](https://skao.slack.com/archives/C05CZKCM22U).
