import pytest

from app.main import create_app


@pytest.fixture
def client():
    app = create_app()
    app.testing = True
    with app.test_client() as client:
        yield client


def test_index_returns_message(client):
    """Test that the root endpoint returns the expected greeting."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Hello, CI/CD!" in response.data


def test_info_returns_metadata(client, monkeypatch):
    """
    Test that the /info endpoint returns JSON with version and environment keys.

    The test temporarily sets environment variables to verify that the application
    correctly exposes their values. It relies on pytest's monkeypatch fixture
    to isolate changes to the environment for the duration of the test.
    """
    # Set temporary environment variables
    monkeypatch.setenv("APP_VERSION", "test-version")
    monkeypatch.setenv("ENVIRONMENT", "dev")
    response = client.get("/info")
    assert response.status_code == 200
    data = response.get_json()
    assert data["version"] == "test-version"
    assert data["environment"] == "dev"