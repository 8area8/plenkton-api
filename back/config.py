"""FastAPI settings."""

from pydantic import BaseSettings
from starlette.config import Config
from starlette.datastructures import Secret

config = Config()


class Settings(BaseSettings):
    # Dev or Prod
    DEBUG: bool = True
    # path to your cloud bucket/dist
    CLOUD_STATIC_URL: str = "https://storage.googleapis.com/plenkton/dist"

    # Database part
    DB_DRIVER = config("DB_DRIVER", default="postgresql")
    DB_HOST = config("DB_HOST", default="db")
    DB_TEST_HOST = config("DB_HOST", default="test-db")
    DB_PORT = config("DB_PORT", cast=int, default=5432)
    DB_USER = config("DB_USER", default="postgres")
    DB_PASSWORD = config("DB_PASSWORD", cast=Secret, default="postgres")
    DB_DATABASE = config("DB_DATABASE", default="plenktondb")
    DB_PROD_DSN = config(
        "DB_DSN",
        default=f"{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_DATABASE}",
    )
    DB_TEST_DSN = f"{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_TEST_HOST}/{DB_DATABASE}"
    TESTING: str = config("PYTEST_CURRENT_TEST", default="")
    DB_DSN = DB_TEST_DSN if TESTING else DB_PROD_DSN

    # Auth0 part
    AUTH0_AUDIENCE = config("AUTH0_AUDIENCE", default="")
    AUTH0_ISSUER = config("AUTH0_ISSUER", default="")
    AUTH0_DOMAIN = config("AUTH0_DOMAIN", default="")
    AUTH0_ALGORITHMS = config("AUTH0_ALGORITHMS", default="RS256")
    AUTH0_CLIENT_ID = config("AUTH0_CLIENT_ID", default="")
    AUTH0_CLIENT_SECRET = config("AUTH0_CLIENT_SECRET", default="")


settings = Settings()
