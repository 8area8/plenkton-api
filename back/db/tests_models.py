"""Test thedatabase.

"""

import pytest
from pydantic import ValidationError
from asyncpg.exceptions import UniqueViolationError

from .models import Author, Article, Tag
from .base import database, sqlalchemy, metadata, settings

pytestmark = pytest.mark.anyio


AUTHOR_PAYLOAD = dict(username="pseudo", email="test@test.fr", auth0_id="fake_id")
ARTICLE_PAYLOAD = dict(name="article-I", teaser="So fun", body="long body")
BODY_PAYLOAD = dict(
    body="N’aie pas pitié des morts Harry, aie pitié des vivants "
    "et en particulier de tous ceux qui vivent sans amour."
)
BODY_PALOAD_LONG = dict(
    body="Dans le monde il n’y a pas d’un côté le bien et le mal, "
    "il y a une part de lumière et d’ombre en chacun de nous. Ce qui"
    " compte c’est celle que l’on choisit de montrer dans nos actes, "
    "ça c’est ce que l’on est vraiment."
)


@pytest.fixture(autouse=True, scope="module")
def create_test_database():
    engine = sqlalchemy.create_engine(settings.DB_DSN)
    metadata.create_all(engine)
    yield
    metadata.drop_all(engine)


@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_author_creation():
    """We can create an author."""
    async with database:
        async with database.transaction(force_rollback=True):
            author = await Author.objects.create(**AUTHOR_PAYLOAD)
            assert author.username == "pseudo"
            assert await Author.objects.get(username="pseudo") == author


@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_article_creation():
    """We can create an article.

    1 - an article must have an author defined.
    2 - the article is created with author
    """
    async with database:
        async with database.transaction(force_rollback=True):
            # 1
            with pytest.raises(ValidationError):
                article = await Article.objects.create(**ARTICLE_PAYLOAD)

            # 2
            author = await Author.objects.create(**AUTHOR_PAYLOAD)
            article = await Article.objects.create(**ARTICLE_PAYLOAD, author=author)
            assert article.author == author


@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_article_has_slug_url():
    """The slug url correspond to the name."""
    async with database:
        async with database.transaction(force_rollback=True):
            author = await Author.objects.create(**AUTHOR_PAYLOAD)
            payload = {**ARTICLE_PAYLOAD, **dict(name="My nâme ìs not a SlUg.")}
            article = await Article.objects.create(**payload, author=author)
            assert article.url == "my-name-is-not-a-slug"


@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_article_has_reading_time():
    """The reading time correspond to the body."""
    async with database:
        async with database.transaction(force_rollback=True):
            author = await Author.objects.create(**AUTHOR_PAYLOAD)
            payload = {**ARTICLE_PAYLOAD, **BODY_PAYLOAD}
            article = await Article.objects.create(**payload, author=author)
            assert article.reading_time == 5

            article.body = BODY_PALOAD_LONG["body"]
            await article.update()
            assert article.reading_time == 13


@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_article_can_have_tags():
    """An article can have many tags."""
    async with database:
        async with database.transaction(force_rollback=True):
            author = await Author.objects.create(**AUTHOR_PAYLOAD)
            article = await Article.objects.create(**ARTICLE_PAYLOAD, author=author)
            assert article.tags == []

            python = await Tag.objects.create(name="python")
            javascript = await Tag.objects.create(name="javascript")
            await article.tags.add(python)
            await article.tags.add(javascript)
            assert article.tags == [python, javascript]


@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_tag_creation():
    """We can create tags.

    1 - we can create tag with a name
    2 - the name must be unique.
    """
    async with database:
        async with database.transaction(force_rollback=True):
            # 1
            tag = await Tag.objects.create(name="tag1")
            assert tag.name == "tag1"

            # 2
            with pytest.raises(UniqueViolationError):
                await Tag.objects.create(name="tag1")


@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_tag_slugify():
    """Tag names are slugified by default."""
    async with database:
        async with database.transaction(force_rollback=True):
            tag = await Tag.objects.create(name="tag 1 $python")
            assert tag.name == "tag-1-python"
