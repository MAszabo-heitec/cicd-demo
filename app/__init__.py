"""Package initialization for the Flask application.

Exposes the `create_app` factory for 
use by external tools and the command line.
"""

from .main import create_app  # noqa: F401

__all__ = ["create_app"]
