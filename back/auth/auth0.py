"""AUth0 SDK."""

from dataclasses import dataclass
from typing import Optional

from auth0.v3.authentication import GetToken
from auth0.v3.management import Auth0

from back.config import settings


@dataclass
class User:
    blog: Optional[str]
    email: str
    user_id: str


class AuthAPI:
    """Auth0 API."""

    def __init__(self):
        """Init the API."""
        domain = settings.AUTH0_DOMAIN
        non_interactive_client_id = settings.AUTH0_CLIENT_ID
        non_interactive_client_secret = settings.AUTH0_CLIENT_SECRET

        get_token = GetToken(domain)
        token = get_token.client_credentials(
            non_interactive_client_id,
            non_interactive_client_secret,
            f"https://{domain}/api/v2/",
        )
        mgmt_api_token = token["access_token"]
        self.auth0 = Auth0(domain, mgmt_api_token)

    def list_users(self):
        """List all users."""
        users = [
            User(blog=user.get("blog"), email=user["email"], user_id=user["user_id"])
            for user in self.auth0.users.list()["users"]
        ]
        return users
