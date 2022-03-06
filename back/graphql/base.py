"""Base types."""

import typing

import strawberry
from starlette.requests import Request
from starlette.websockets import WebSocket
from strawberry import types
from strawberry.fastapi import GraphQLRouter
from strawberry.permission import BasePermission


class IsAdmin(BasePermission):
    """Check if the user is admin."""

    message = "Admin required."

    async def has_permission(
        self, source: typing.Any, info: types.Info, **kwargs
    ) -> bool:
        """Check if the user is admin."""
        request: typing.Union[Request, WebSocket] = info.context["request"]
        return request.state.is_admin


def query_private_admin(self, info: types.Info) -> str:
    """Check for admin endpoint."""
    # check if admin otherwise raise error
    return "Hello admin !"


@strawberry.type
class Query:
    """Base Query."""

    private_admin = strawberry.field(query_private_admin, permission_classes=[IsAdmin])

    @strawberry.field
    def server(self) -> str:
        """Check if the server is alive."""
        return "Is alive !"


schema = strawberry.Schema(Query)

graphql_app = GraphQLRouter(schema)
