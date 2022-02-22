"""Test the fastapi index."""

from unittest.mock import Mock, patch

import pytest
from httpx import AsyncClient

from back.server import app, settings, HTMLIndex


pytestmark = pytest.mark.anyio


@pytest.fixture(scope="function")
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_server_is_alive(async_client):
    """Home page returns HTML content."""
    response = await async_client.get("/")
    assert response.status_code == 200
    assert "<!doctype html>" in str(response.content).lower()


@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_prod_server_is_alive(async_client):
    """Home page returns HTML content."""
    CLOUD_STATIC_URL = settings.CLOUD_STATIC_URL
    settings.DEBUG = False
    response = await async_client.get("/")
    assert response.status_code == 200
    assert "<!doctype html>" in str(response.content).lower()
    assert CLOUD_STATIC_URL in str(response.content)
    settings.DEBUG = True


@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_requests_get_is_called_only_once(async_client):
    """Avoid multiple requests calls to retrieve the index.html on production."""

    def mock_load(mock, call_mock):
        """Decorator that pass the the IndexHTML mock and a "call_mock"."""

        async def func(*args, **kwargs):
            """Fake HTMLIndex.load and call the "call_mock" object."""
            mock.html = "fake content"
            call_mock()

        return func

    settings.DEBUG = False
    HTMLIndex.html = None

    with patch("back.server.HTMLIndex") as mock:
        called_in_load = Mock()
        mock.html = None
        mock.load = mock_load(mock, called_in_load)
        response = await async_client.get("/")
        assert response.status_code == 200
        response = await async_client.get("/")
        assert response.status_code == 200
        response = await async_client.get("/")
        assert response.status_code == 200
        called_in_load.assert_called_once()

    settings.DEBUG = True
