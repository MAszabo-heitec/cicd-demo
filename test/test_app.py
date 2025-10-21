import os
import pytest

from app.main import create_app


@pytest.fixture
def client(monkeypatch):
    """
    Pytest fixture to create a test client. Uses monkeypatch to ensure
    environment variables are isolated per test.
    """
    # Ensure default environment variables for each test
    monkeypatch.setenv("APP_VERSION", "test")
    monkeypatch.setenv("ENVIRONMENT", "test")
    app = create_app()
    app.testing = True
    with app.test_client() as client:
        yield client


def test_index_returns_message(client):
    """Test that the root endpoint returns the expected greeting."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Hello, CI/CD!" in response.data


def test_info_returns_version_and_environment(client):
    """Test that the /info endpoint returns JSON with version and environment."""
    response = client.get("/info")
    assert response.status_code == 200
    data = response.get_json()
    # Use the monkeypatched environment variables
    assert data["version"] == "test"
    assert data["environment"] == "test"