"""Auth0 JWT validation.

Usage:

result = VerifyToken(token.credentials).verify()

if result.get("status"):
    response.status_code = status.HTTP_400_BAD_REQUEST
    return result
"""

import json
from typing import TYPE_CHECKING

import httpx
from fastapi import HTTPException
from jose import jwt

from back.config import settings

if TYPE_CHECKING:
    from .admin import Token


async def requires_auth(token: "Token"):
    """Determines if the Access Token is valid"""
    async with httpx.AsyncClient() as client:
        jsonurl = await client.get(
            f"https://{settings.AUTH0_DOMAIN}/.well-known/jwks.json"
        )
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token.credentials)
    rsa_key = {}
    for key in jwks["keys"]:
        if key["kid"] == unverified_header.get("kid"):
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"],
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token.credentials,
                rsa_key,
                algorithms=[settings.AUTH0_ALGORITHMS],
                audience=settings.AUTH0_AUDIENCE,
                issuer=f"https://{settings.AUTH0_DOMAIN}/",
            )
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="token is expired")
        except jwt.JWTClaimsError:
            raise HTTPException(
                status_code=401,
                detail="incorrect claims, please check the audience and issuer",
            )
        except Exception:
            raise HTTPException(
                status_code=401,
                detail="Unable to parse authentication",
            )

        return payload

    raise HTTPException(
        status_code=401,
        detail="Unable to find appropriate key",
    )
