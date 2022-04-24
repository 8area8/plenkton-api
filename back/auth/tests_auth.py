"""Test the authentication."""

from unittest.mock import patch

import pytest
from httpx import AsyncClient

from back.__main__ import app
from back.auth.admin import CheckAdminMiddleware
from back.db.base import database, metadata, settings, sqlalchemy
from back.db.models import Author

from .admin import install_admin_user

pytestmark = pytest.mark.asyncio


@pytest.fixture(scope="function")
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture(autouse=True, scope="module")
def create_test_database():
    engine = sqlalchemy.create_engine(settings.DB_DSN)
    metadata.drop_all(engine)
    metadata.create_all(engine)
    yield
    metadata.drop_all(engine)


async def test_install_admin_user():
    """Test the installation of the admin user."""
    async with database:
        async with database.transaction(force_rollback=True):
            assert await Author.objects.get_or_none(username="8area8") is None
            result = await install_admin_user()
            assert result
            assert await Author.objects.get_or_none(username="8area8") is not None


async def test_private_admin(async_client):
    """Test the access to the private admin query.

    1 - random user can't access to the query
    2 - admin can access to the query (need valid token)
    """

    async def mock_dispatch(request, call_next):
        """Assignate the admin to the request."""
        payload = dict(username="foo", email="bar@baz.fr", auth0_id="nop")
        async with database:
            async with database.transaction(force_rollback=True):
                user = await Author.objects.create(**payload)

        request.state.user = user
        request.state.is_admin = True
        response = await call_next(request)
        return response

    # 1
    data = {"query": "query isAdmin { privateAdmin }"}
    response = await async_client.post("/graphql", json=data)
    assert response.json()["errors"][0]["message"] == "Admin required."

    # 2
    with patch.object(CheckAdminMiddleware, "dispatch", side_effect=mock_dispatch):
        app.user_middleware = []
        app.add_middleware(CheckAdminMiddleware)
        data = {"query": "query isAdmin { privateAdmin }"}
        response = await async_client.post("/graphql", json=data)
        assert response.json()["data"]["privateAdmin"] == "Hello admin !"
