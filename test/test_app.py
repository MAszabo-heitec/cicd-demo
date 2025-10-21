import pytest
from app.main import create_app


@pytest.fixture
def client(monkeypatch):
    # Set default env variables for the duration of the test
    monkeypatch.setenv("APP_VERSION", "test")
    monkeypatch.setenv("ENVIRONMENT", "test")
    app = create_app()
    app.testing = True
    with app.test_client() as client:
        yield client


def test_index_returns_message(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Hello, CI/CD!" in response.data


def test_info_returns_version_and_environment(client):
    response = client.get("/info")
    assert response.status_code == 200
    data = response.get_json()
    assert data["version"] == "test"
    assert data["environment"] == "test"