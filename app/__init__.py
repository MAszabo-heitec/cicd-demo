"""Initialize the app package.

This file marks the directory as a Python package so that tests and other modules
can import `app.main` without encountering a `ModuleNotFoundError`. It does not
need to contain any code.
"""

from .main import create_app  # Re-export for convenience