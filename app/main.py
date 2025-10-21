from flask import Flask, jsonify
import os


def create_app() -> Flask:
    """Factory function to create the Flask application."""
    app = Flask(__name__)

    @app.route("/")
    def index():
        """
        Returns a simple greeting to verify that the application is running.
        """
        return "Hello, CI/CD!"

    @app.route("/info")
    def info():
        """
        Returns basic metadata about the running application. The version and
        environment values are derived from environment variables set during
        container build or at runtime. If not provided, sensible defaults are
        used. This can help verify that build arguments were correctly passed
        into the Docker image.
        """
        version = os.getenv("APP_VERSION", "unknown")
        environment = os.getenv("ENVIRONMENT", "unknown")
        return jsonify({"version": version, "environment": environment})

    return app


if __name__ == "__main__":
    app = create_app()
    # Listen on all interfaces so the app is accessible when containerized
    app.run(host="0.0.0.0", port=5000)