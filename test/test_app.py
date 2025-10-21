"""Unit tests for the complex CI/CD demo application.

These tests exercise the various API endpoints to ensure that they behave as
expected.  The tests avoid touching network resources and instead use Flask's
built-in test client to make HTTP requests directly against the application.
"""

import json

from app.main import create_app


def test_root() -> None:
    app = create_app()
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200
        body = response.get_data(as_text=True)
        assert 'Complex CI/CD Demo' in body


def test_api_random() -> None:
    app = create_app()
    with app.test_client() as client:
        response = client.get('/api/random')
        assert response.status_code == 200
        data = json.loads(response.get_data(as_text=True))
        assert 'random' in data
        assert 0 <= data['random'] <= 100


def test_api_time() -> None:
    app = create_app()
    with app.test_client() as client:
        response = client.get('/api/time')
        assert response.status_code == 200
        data = json.loads(response.get_data(as_text=True))
        assert 'current_time' in data
        # ensure ISO format with trailing Z
        assert data['current_time'].endswith('Z')


def test_api_calc() -> None:
    app = create_app()
    with app.test_client() as client:
        response = client.get('/api/calc/2/3')
        assert response.status_code == 200
        data = json.loads(response.get_data(as_text=True))
        assert data['result'] == 5


def test_api_info_and_health() -> None:
    app = create_app()
    with app.test_client() as client:
        info_response = client.get('/api/info')
        assert info_response.status_code == 200
        info_data = json.loads(info_response.get_data(as_text=True))
        # Ensure metadata keys are present
        assert 'version' in info_data
        assert 'commit' in info_data
        assert 'environment' in info_data

        health_response = client.get('/api/health')
        assert health_response.status_code == 200
        health_data = json.loads(health_response.get_data(as_text=True))
        assert health_data['status'] == 'ok'
