# pylint: disable=all

import importlib.metadata

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "ska-ds-psi-prometheus-exporters"
copyright = "2025 TOPIC Team"
author = "TOPIC Team"
release = importlib.metadata.version(project)

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    "sphinx.ext.autodoc",
    "myst_parser",
]

source_suffix = [".rst", ".md"]
exclude_patterns = []

pygments_style = "sphinx"

extlinks = {
    "jira": ("https://jira.skatelescope.org/browse/%s", "%s"),
}

intersphinx_mapping = {
    "ska-dev-portal": ("https://developer.skao.int/en/latest", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "ska_ser_sphinx_theme"

html_context = {
    "theme_logo_only": True,
    "display_gitlab": True,
    "gitlab_user": "ska-telescope",
    "gitlab_repo": project,
    "gitlab_version": "main",
    "conf_py_path": "/docs/src/",  # Path in the checkout to the docs root
    "theme_vcs_pageview_mode": "edit",
    "suffix": ".rst",
}
