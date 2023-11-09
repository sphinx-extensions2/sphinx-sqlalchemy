"""Sphinx extension for documenting SQLAlchemy ORMs"""
from typing import TYPE_CHECKING

__version__ = "0.2.0"

if TYPE_CHECKING:
    from sphinx.application import Sphinx


def setup(app: "Sphinx") -> dict:
    """Sphinx extension setup function."""
    from .main import setup_extension

    setup_extension(app)
    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
