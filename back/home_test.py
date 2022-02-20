"""Test the fastapi index."""

from fastapi.testclient import TestClient

from back.server import app, settings

client = TestClient(app)


def test_server_is_alive():
    """Home page returns HTML content."""
    response = client.get("/")
    assert response.status_code == 200
    assert "<!doctype html>" in str(response.content).lower()


def test_prod_server_is_alive():
    """Home page returns HTML content."""
    CLOUD_STATIC_URL = settings.CLOUD_STATIC_URL
    settings.DEBUG = False
    response = client.get("/")
    assert response.status_code == 200
    assert "<!doctype html>" in str(response.content).lower()
    assert CLOUD_STATIC_URL in str(response.content)
    settings.DEBUG = True
