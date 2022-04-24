"""Test the fastapi index."""

from unittest.mock import Mock, patch

import pytest
from httpx import AsyncClient

from back.__main__ import HTMLIndex, app, settings

pytestmark = pytest.mark.asyncio


@pytest.fixture(scope="function")
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


async def test_server_is_alive(async_client):
    """Home page returns HTML content."""
    response = await async_client.get("/")
    assert response.status_code == 200
    assert "<!doctype html>" in str(response.content).lower()


async def test_prod_server_is_alive(async_client):
    """Home page returns HTML content."""
    CLOUD_STATIC_URL = settings.CLOUD_STATIC_URL
    settings.DEBUG = False
    response = await async_client.get("/")
    assert response.status_code == 200
    assert "<!doctype html>" in str(response.content).lower()
    assert CLOUD_STATIC_URL in str(response.content)
    settings.DEBUG = True


async def test_home_page_does_not_have_undefined_values(async_client):
    """Be sure the generated dist works without missing env variables."""
    response = await async_client.get("/")
    assert response.status_code == 200
    assert "undefined" not in str(response.content).lower()


async def test_backend_env_var(async_client):
    """Be sure the backend env var are set."""
    # GCloud
    assert settings.CLOUD_STATIC_URL
    # auth0
    assert settings.AUTH0_ALGORITHMS
    assert settings.AUTH0_AUDIENCE
    assert settings.AUTH0_CLIENT_ID
    assert settings.AUTH0_CLIENT_SECRET
    assert settings.AUTH0_DOMAIN
    assert settings.AUTH0_ISSUER


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

    with patch("back.__main__.HTMLIndex") as mock:
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
