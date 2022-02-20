"""Base server."""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse, HTMLResponse
import requests

from .config import settings

app = FastAPI()


if settings.DEBUG:
    app.mount("/static", StaticFiles(directory="front/dist"), name="static")


@app.get("/{file_path:path}")
async def root():
    """Return the vuecli index file.

    Note: catch all paths and returns the index.html, because of vue history mode.

    On dev mode, returns the local index file.
    On production, returns the cloud storage index file.
    """
    if settings.DEBUG:
        return FileResponse("front/dist/index.html")
    response = requests.get(f"{settings.CLOUD_STATIC_URL}/index.html")
    return HTMLResponse(response.content)
