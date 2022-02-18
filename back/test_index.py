"""Test the fastapi index."""

from fastapi.testclient import TestClient

from back.server import app

client = TestClient(app)


def test_server_is_alive():
    """Home page returns HTML content."""
    response = client.get("/")
    assert response.status_code == 200
    assert "<!doctype html>" in str(response.content)
