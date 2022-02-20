"""FastAPI settings."""

from pydantic import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool = True
    CLOUD_STATIC_URL: str = "https://storage.googleapis.com/plenkton/dist"


settings = Settings()
