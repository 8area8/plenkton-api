"""Base types."""

import datetime
import typing

import strawberry
from starlette.requests import Request
from starlette.websockets import WebSocket
from strawberry import types
from strawberry.fastapi import GraphQLRouter
from strawberry.permission import BasePermission

from back.db.models import Article as DBArticle
from back.db.models import Author as DBAuthor
from back.db.models import Tag as DBTag


class IsAdmin(BasePermission):
    """Check if the user is admin."""

    message = "Admin required."

    async def has_permission(
        self, source: typing.Any, info: types.Info, **kwargs
    ) -> bool:
        """Check if the user is admin."""
        request: typing.Union[Request, WebSocket] = info.context["request"]
        return request.state.is_admin


def query_server(self, info: types.Info) -> str:
    """Query the server status."""
    return "Is alive !"


def query_private_admin(self, info: types.Info) -> str:
    """Check for admin endpoint."""
    # check if admin otherwise raise error
    return "Hello admin !"


async def query_articles(self, info: types.Info) -> list["Article"]:
    """Query the articles."""
    result = []
    articles = await DBArticle.objects.all()  # type: ignore
    for article in articles:
        data = article.dict()

        author = await DBAuthor.objects.get(id=article.author.id)
        author = author.dict()
        author["articles"] = []  # HACK: to resolve
        data["author"] = Author(**author)

        tags = []
        for tag in article.tags:
            tag = await DBTag.objects.get(id=tag.id)
            tags.append(Tag(**tag.dict()))
        data["tags"] = tags

        result.append(Article(**data))
    return result


@strawberry.type(description="Base query.")
class Query:
    """Base Query."""

    private_admin = strawberry.field(
        query_private_admin,
        permission_classes=[IsAdmin],
        description="Ping the private endpoint.",
    )
    server = strawberry.field(query_server, description="Get the server status")

    articles = strawberry.field(query_articles, description="Query the articles.")


@strawberry.type(description="Article writer. The author is also the base user.")
class Author:
    """Author."""

    id: strawberry.ID
    auth0_id: str
    email: str
    username: str
    is_admin: bool
    articles: list["Article"]


@strawberry.type(description="Article tag.")
class Tag:
    """Tag."""

    id: strawberry.ID
    name: str


@strawberry.type(description="Article.")
class Article:
    """Article."""

    id: strawberry.ID
    name: str
    teaser: str
    body: str
    author: Author
    tags: list[Tag]
    created_at: datetime.datetime
    modified_at: datetime.datetime
    url: str
    reading_time: str


schema = strawberry.Schema(Query)

graphql_app = GraphQLRouter(schema)
