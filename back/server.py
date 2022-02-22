"""Base server."""

from typing import Optional
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse, HTMLResponse
import httpx

from .config import settings
from .graphql import base

app = FastAPI()

app.include_router(base.graphql_app, prefix="/graphql")


if settings.DEBUG:
    app.mount("/static", StaticFiles(directory="front/dist"), name="static")


class HTMLIndex:
    """Used to retrieve the index.html file only one time."""

    html: Optional[bytes] = None
    url = f"{settings.CLOUD_STATIC_URL}/index.html"

    @classmethod
    async def load(cls):
        """Get the html content."""
        async with httpx.AsyncClient() as httpx_client:
            response = await httpx_client.get(cls.url)
            print("response from index class:", response.content)
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
    print(HTMLIndex.html)
    if not HTMLIndex.html:
        await HTMLIndex.load()
    return HTMLResponse(HTMLIndex.html)
