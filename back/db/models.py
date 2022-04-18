"""Base models."""

import datetime
from typing import Type, cast

import ormar
import readtime
from slugify import slugify

from .base import MainMeta


class Author(ormar.Model):
    """Created each time we get a new user.

    NOTE: no password because we use auth0.
    """

    class Meta(MainMeta):
        pass

    id = cast(int, ormar.Integer(primary_key=True))
    auth0_id: str = cast(str, ormar.String(max_length=255, nullable=False, unique=True))

    email: str = cast(str, ormar.String(max_length=255, nullable=False))
    username: str = cast(str, ormar.String(max_length=255))

    is_admin: bool = ormar.Boolean(default=False)

    @classmethod
    async def get_admins(cls):
        """Return the admins."""
        return await Author.objects.filter(is_admin=True).all()


class Tag(ormar.Model):
    """Categorize the articles."""

    class Meta(MainMeta):
        pass

    id: int = cast(int, ormar.Integer(primary_key=True))

    name: str = cast(str, ormar.String(max_length=255, nullable=False, unique=True))


@ormar.pre_save(Tag)
async def slugify_name(sender: Type[Tag], instance: Tag, **kwargs) -> None:
    """Slugify the name."""
    instance.name = slugify(instance.name)


class Article(ormar.Model):
    """Article in the database."""

    class Meta(MainMeta):
        pass

    id = ormar.Integer(primary_key=True)

    name = cast(str, ormar.String(max_length=100, unique=True))
    teaser = cast(str, ormar.String(max_length=500))
    body = cast(str, ormar.Text())

    tags = ormar.ManyToMany(to=Tag, nullable=True)
    author = ormar.ForeignKey(to=Author, nullable=False)

    created_at = cast(datetime.datetime, ormar.DateTime(default=datetime.datetime.now))
    modified_at = cast(datetime.datetime, ormar.DateTime(default=datetime.datetime.now))

    @ormar.property_field
    def url(self) -> str:
        """Return a valid url from the name."""
        return slugify(self.name)

    @ormar.property_field
    def reading_time(self) -> int:
        """Get the average reading time in seconds."""
        return readtime.of_text(self.body).seconds
