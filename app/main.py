from flask import Flask, jsonify
import os


def create_app() -> Flask:
    """Factory function to create the Flask application."""
    app = Flask(__name__)

    @app.route("/")
    def index():
        return "Hello, CI/CD!"

    @app.route("/info")
    def info():
        """
        Returns basic metadata about the running application. This endpoint exposes
        the application version and the environment in which the service is
        running. These values are derived from environment variables set during
        the container build or at runtime. If no environment variables are
        provided, sensible defaults are used. Such metadata can be invaluable
        when debugging deployment issues or verifying that a new version has
        successfully rolled out in different environments.
        """
        version = os.getenv("APP_VERSION", "unknown")
        environment = os.getenv("ENVIRONMENT", "unknown")
        return jsonify({"version": version, "environment": environment})

    return app


if __name__ == "__main__":
    app = create_app()
    # Az alkalmazás indítása a 0.0.0.0 címen, hogy Docker konténerben is elérhető legyen
    app.run(host="0.0.0.0", port=5000)