
# Use bash shell with pipefail option enabled so that the return status of a
# piped command is the value of the last (rightmost) command to exit with a
# non-zero status. This lets us pipe output into tee but still exit on test
# failures.
SHELL = /bin/bash
.SHELLFLAGS = -o pipefail -c

CI_JOB_ID ?= local

########################################################################
# BASE
########################################################################

PROJECT = ska-bf-switch-exporter
DOCS_SPHINXOPTS ?= -W

include .make/base.mk

########################################################################
# PYTHON
########################################################################

PYTHON_SRC = src

include .make/python.mk

########################################################################
# OCI
########################################################################

OCI_IMAGES_TO_PUBLISH = ska-bf-switch-exporter

include .make/oci.mk
