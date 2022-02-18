"""Base server."""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse

app = FastAPI()

app.mount("/static", StaticFiles(directory="front/dist"), name="static")


@app.get("/{file_path:path}")
async def root():
    return FileResponse("front/dist/index.html")


@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    """Read Vue CLI files."""
    return {"file_path": file_path}
