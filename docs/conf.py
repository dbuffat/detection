# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os, sys, re
sys.path.insert(0, os.path.abspath('..'))

project = 'TP1_DBuffat_MThomeer'
copyright = '2024, D. Buffat & M. Thomeer'
author = 'D. Buffat & M. Thomeer'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'nbsphinx']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

language = 'fr'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']

autodoc_default_options = {
    'members': True,            # Document all members
    'undoc-members': False,      # ... including undocumented ones
    'private-members': True,
}
autoclass_content = "both"              # Insert class and __init__ docstrings
autodoc_member_order = "bysource"       # Keep source order
