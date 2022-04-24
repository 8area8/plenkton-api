"""Base server."""

from typing import Optional

import httpx
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse, HTMLResponse

from .auth.admin import CheckAdminMiddleware, install_admin_user
from .config import settings
from .db import base as db
from .graphql import base as gql

app = FastAPI()
app.include_router(gql.graphql_app, prefix="/graphql")
app.state.database = db.database


@app.on_event("startup")
async def startup() -> None:
    database_ = app.state.database
    if not database_.is_connected:
        await database_.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    database_ = app.state.database
    if database_.is_connected:
        await database_.disconnect()


app.add_middleware(CheckAdminMiddleware)

if settings.DEBUG:
    app.mount("/static", StaticFiles(directory="front/dist"), name="static")
    app.mount("/public", StaticFiles(directory="front/src/public"), name="public")


class HTMLIndex:
    """Used to retrieve the index.html file only one time."""

    html: Optional[bytes] = None
    url = f"{settings.CLOUD_STATIC_URL}/index.html"

    @classmethod
    async def load(cls):
        """Get the html content."""
        async with httpx.AsyncClient() as httpx_client:
            response = await httpx_client.get(cls.url)
            cls.html = response.content


@app.get("/{file_path:path}")
async def root():
    """Return the vuecli index file.

    Note: catch all paths and returns the index.html, because of vue history mode.

    On dev mode, returns the local index file.
    On production, returns the cloud storage index file.
    """
    if settings.DEBUG:
        return FileResponse("front/dist/index.html")
    if not HTMLIndex.html:
        await HTMLIndex.load()
    return HTMLResponse(HTMLIndex.html)
