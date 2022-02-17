"""Test the fastapi index."""

from fastapi.testclient import TestClient

from back.server import app

client = TestClient(app)


def test_server_is_alive():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "alive"}
