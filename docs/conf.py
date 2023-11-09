"""Sphinx configuration file."""
import os
import sys

# add example module to the python path
sys.path.insert(0, os.path.dirname(__file__))

extensions = ["sphinx_sqlalchemy"]

html_title = "sphinx-sqlalchemy documentation"
html_theme = "furo"
