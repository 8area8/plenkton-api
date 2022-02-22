"""Base types."""

import strawberry
from strawberry.fastapi import GraphQLRouter


@strawberry.type
class Query:
    """Base Query."""

    @strawberry.field
    def server(self) -> str:
        return "Is alive !"


schema = strawberry.Schema(Query)

graphql_app = GraphQLRouter(schema)
