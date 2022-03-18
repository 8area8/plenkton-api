"""Retrieve the admin from Auth0."""

from dataclasses import dataclass

from fastapi.security import HTTPBearer
from starlette.middleware.base import BaseHTTPMiddleware

from back.db.models import Author

from .auth0 import AuthAPI
from .jwt import requires_auth

ADMIN_ID = "github|28759924"


@dataclass
class Token:
    scheme: bytes
    credentials: str


async def install_admin_user() -> bool:
    """Retrieve the admin from AUth0 and assign it to the Author."""
    api = AuthAPI()
    users = api.list_users()
    for user in users:
        if user.user_id == ADMIN_ID:
            await Author.objects.get_or_create(
                username="8area8", email=user.email, auth0_id=user.user_id
            )
            return True
    return False


class CheckAdminMiddleware(BaseHTTPMiddleware):
    """Check if the current user is the admin."""

    async def dispatch(self, request, call_next):
        request.state.is_admin = False
        request.state.user = None

        token = request.headers.get("Authorization")
        if token:
            scheme, credentials = token.split(" ")
            token = Token(scheme=scheme, credentials=credentials)
            result = await requires_auth(token)

            if not result.get("status") == "error":
                author = await Author.objects.get_or_none(auth0_id=result["sub"])
                if author:
                    request.state.user = author
                    if author.auth0_id == ADMIN_ID:
                        request.state.is_admin = True

        response = await call_next(request)
        return response
