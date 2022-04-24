"""Graphql tests.

https://strawberry.rocks/docs/operations/testing
"""

import pytest

from back.article.fixtures import ArticlesFixture
from back.auth.admin import install_admin_user
from back.db.base import database, metadata, settings, sqlalchemy

from .base import schema

pytestmark = pytest.mark.asyncio


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


async def test_query_async():
    """Be sure the graphql server run."""
    query = """
        query isServerAlive {
            server
        }
    """
    response = await schema.execute(query)
    assert response.errors is None
    assert response.data
    assert response.data["server"] == "Is alive !"


async def test_articles_query():
    """Check the articles queries."""
    await install_admin_user()
    await ArticlesFixture().add()
    query = """
        query getArticles {
            articles {
                id
                name
                createdAt
            }
        }
    """
    response = await schema.execute(query)
    assert response.errors is None
    assert response.data
    assert len(response.data["articles"]) == 5
    assert response.data["articles"][0]["name"] == "Super Python part one"
