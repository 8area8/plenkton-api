"""Retrieve the admin from Auth0."""

from starlette.middleware.base import BaseHTTPMiddleware

from back.db.models import Author

from .auth0 import AuthAPI
from .jwt import VerifyToken


async def install_admin_user() -> bool:
    """Retrieve the admin from AUth0 and assign it to the Author."""
    ADMIN_ID = "github|28759924"
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
            result = VerifyToken(token).verify()

            if author := await Author.objects.get_or_none(id_auth0=result["id"]):
                request.state.is_admin = True
                request.state.user = author

        response = await call_next(request)
        return response
