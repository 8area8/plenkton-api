"""Base database.

https://collerek.github.io/ormar/install/
"""

import ormar
import databases
import sqlalchemy

from back.config import settings

database = databases.Database(settings.DB_DSN)
metadata = sqlalchemy.MetaData()


class MainMeta(ormar.ModelMeta):
    metadata = metadata
    database = database
