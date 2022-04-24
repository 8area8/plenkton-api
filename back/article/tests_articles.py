"""Test the articles."""

import pytest
from httpx import AsyncClient

from back.__main__ import app
from back.auth.admin import install_admin_user
from back.db.base import database, metadata, settings, sqlalchemy
from back.db.models import Article

from .fixtures import ArticlesFixture

pytestmark = pytest.mark.asyncio


@pytest.fixture(scope="function")
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture()
async def create_test_database():
    engine = sqlalchemy.create_engine(settings.DB_DSN)
    metadata.drop_all(engine)
    metadata.create_all(engine)
    yield
    metadata.drop_all(engine)


@pytest.fixture(autouse=True)
async def use_db(create_test_database):
    async with database:
        async with database.transaction(force_rollback=True):
            yield


async def test_articles_fixture():
    """We can add and remove article fixtures."""
    articles_fixture = ArticlesFixture()
    await install_admin_user()

    for data in articles_fixture.articles:
        assert await Article.objects.get_or_none(name=data["name"]) is None

    await articles_fixture.add()

    for data in articles_fixture.articles:
        assert await Article.objects.get_or_none(name=data["name"]) is not None

    await articles_fixture.remove()

    for data in articles_fixture.articles:
        assert await Article.objects.get_or_none(name=data["name"]) is None
