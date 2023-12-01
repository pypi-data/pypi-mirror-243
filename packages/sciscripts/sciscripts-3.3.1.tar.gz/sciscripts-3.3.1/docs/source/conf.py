# Configuration file for the Sphinx documentation builder.
import os
import sys
print('='*72)
print( 'CWD:', os.path.abspath('../..'))
print('='*72)
sys.path.insert(len(sys.path), os.path.abspath('../..'))


# -- Project information -----------------------------------------------------
project = 'SciScripts'
author = 'Thawann Malfatti and Barbara Ciralli'
copyright = f'2023, CC BY-NC 4.0, {author}'
release = '3.3.1'


# -- General configuration ---------------------------------------------------
extensions = [
    # 'sphinx.ext.autodoc',
    # 'sphinx.ext.autosummary',
    'numpydoc',
]

autosummary_generate = True

templates_path = ['_templates']
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
html_theme = 'alabaster'
html_static_path = ['_static']
