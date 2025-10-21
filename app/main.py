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
        version = os.getenv("APP_VERSION", "unknown")
        environment = os.getenv("ENVIRONMENT", "unknown")
        return jsonify({"version": version, "environment": environment})

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)