# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import os
import sys

import django

# -- Path setup --------------------------------------------------------------
# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#

sys.path.insert(0, os.path.abspath(".."))


# -- Django setup -----------------------------------------------------------
# This is required to import Django code in Sphinx using autodoc.

os.environ["DJANGO_SETTINGS_MODULE"] = "dotfm.settings"
django.setup()

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'dotfm'
copyright = '2024, Tobi DEGNON'
author = 'Tobi DEGNON'
release = '2024'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "myst_parser",
    "sphinx_copybutton",
    "sphinx.ext.autodoc",
    "sphinx_design",
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_title = project
html_static_path = ['_static']

