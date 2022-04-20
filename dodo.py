"""Python doit module."""

import asyncio

import sqlalchemy

from back.article.fixtures import ArticlesFixture
from back.auth.admin import install_admin_user
from back.config import settings
from back.db.base import database
from back.db.models import MainMeta


def task_install_fixtures():
    """Install the fixtures."""

    def add_articles_fixtures(targets):
        async def async_add_articles():
            async with database:
                fixtures = ArticlesFixture()
                await fixtures.add()

        asyncio.run(async_add_articles())
        print("articles installed !")

    return {
        "actions": [add_articles_fixtures],
        "verbosity": 2,
    }


def task_migrate():
    """Migrate to the latest changes."""
    return {
        "actions": ["alembic upgrade head"],
    }


def task_add_admin():
    """Add the admin user."""

    def add_admin(targets):
        async def async_add_admin():
            async with database:
                await install_admin_user()

        asyncio.run(async_add_admin())
        print("admin installed !")

    return {
        "actions": [add_admin],
        "verbosity": 2,
    }


def task_dropdb():
    """Drop the database."""

    def drop_db(targets):
        engine = sqlalchemy.create_engine(settings.DB_DSN)
        MainMeta.metadata.drop_all(engine)
        try:
            engine.execute("drop table alembic_version")
        except Exception:
            pass

        print("Database purged !")

    return {
        "actions": [drop_db],
        "verbosity": 2,
    }
