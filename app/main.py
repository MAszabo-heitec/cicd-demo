"""Main module for the Flask application.

This module defines a factory function ``create_app`` which constructs and returns
a Flask application instance.  The application includes multiple API endpoints
and a simple web page served via the Jinja2 templating engine.  It uses
environment variables to expose metadata (commit SHA, version, environment) to
both the API and the rendered HTML, enabling the CI/CD pipeline to insert
commit information at build time.
"""

from __future__ import annotations

import datetime
import os
import random

from flask import Flask, jsonify, render_template


def create_app() -> Flask:
    """Application factory for the Flask app.

    Reads certain environment variables to embed metadata into the web page and
    API responses.  Defines several routes including:

    - ``/``: Renders a simple HTML page showing version and commit information.
    - ``/api/random``: Returns a random integer between 0 and 100 inclusive.
    - ``/api/time``: Returns the current UTC timestamp in ISO‑8601 format.
    - ``/api/calc/<int:a>/<int:b>``: Adds two integers and returns the result.
    - ``/api/info``: Returns a JSON object with version, commit and environment.
    - ``/api/health``: Returns a health check status.

    Returns:
        A configured ``Flask`` application instance.
    """

    app = Flask(__name__, template_folder=os.path.join(
        os.path.dirname(__file__), "templates"))

    # Pull metadata from the environment.  Defaults ensure the app works locally
    # without requiring CI/CD injection.
    commit_sha = os.environ.get("COMMIT_SHA", "unknown")
    app_version = os.environ.get("APP_VERSION", "0.1.0")
    environment = os.environ.get("ENVIRONMENT", "development")

    @app.route("/")
    def index() -> str:
        """Render the main page with embedded metadata."""
        return render_template("index.html", commit=commit_sha, version=app_version)

    @app.route("/api/random")
    def random_api():  # type: ignore[no-untyped-def]
        """Return a random integer between 0 and 100."""
        return jsonify({"random": random.randint(0, 100)})

    @app.route("/api/time")
    def time_api():  # type: ignore[no-untyped-def]
        """Return the current UTC time in ISO 8601 format with Z suffix."""
        now = datetime.datetime.utcnow().replace(microsecond=0)
        return jsonify({"current_time": f"{now.isoformat()}Z"})

    @app.route("/api/calc/<int:a>/<int:b>")
    def calc_api(a: int, b: int):  # type: ignore[no-untyped-def]
        """Add two integers and return the result."""
        return jsonify({"result": a + b})

    @app.route("/api/info")
    def info_api():  # type: ignore[no-untyped-def]
        """Return application metadata."""
        return jsonify({"version": app_version, "commit": commit_sha, "environment": environment})

    @app.route("/api/health")
    def health_api():  # type: ignore[no-untyped-def]
        """Health check endpoint."""
        return jsonify({"status": "ok"})

    return app


if __name__ == "__main__":
    # When executed directly, create an app instance and run it.  The host and
    # port are configurable via environment variables.
    app_instance = create_app()
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", "5000"))
    app_instance.run(host=host, port=port)
