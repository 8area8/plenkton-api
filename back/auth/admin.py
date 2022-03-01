"""Retrieve the admin from Auth0."""

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from back.db.models import Author

from .jwt import VerifyToken


class CheckAdminMiddleware(BaseHTTPMiddleware):
    """Check if the current user is the admin."""

    async def dispatch(self, request, call_next):
        request.state.is_admin = False
        request.state.user = None
        token = request.headers.get("Authorization")
        if token:
            result = VerifyToken(token).verify()

            if author := await Author.objects.get_or_none(id_auth0=result["id"]):
                request.state.is_admin = True
                request.state.user = author

        response = await call_next(request)
        return response
