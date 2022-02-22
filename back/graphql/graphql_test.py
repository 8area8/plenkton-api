"""Graphql tests.

https://strawberry.rocks/docs/operations/testing
"""

import pytest
from .base import schema

pytestmark = pytest.mark.anyio


@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_query_async():
    """Be sure the graphql server run."""
    query = """
        query isServerAlive {
            server
        }
    """
    response = await schema.execute(
        query, variable_values={"title": "The Great Gatsby"}
    )

    assert response.errors is None
    assert response.data
    assert response.data["server"] == "Is alive !"
