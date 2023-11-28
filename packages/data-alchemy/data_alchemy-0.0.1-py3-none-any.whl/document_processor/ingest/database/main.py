from typing import List, TypeVar

from pydantic import BaseModel

from .models import DatabaseConfig, DatabaseType
from .provider import MongoDB, SupabaseDB

T = TypeVar("T")


class DatabaseManager:
    database = None

    def __init__(self, database_config: DatabaseConfig) -> None:
        self.database_config = database_config

        if self.database_config.database == DatabaseType.MONGODB:
            self.database = MongoDB(
                db_connection_config=self.database_config.db_connection_config
            )
        elif self.database_config.database == DatabaseType.POSTGRESQL:
            pass
        elif self.database_config.database == DatabaseType.MYSQL:
            pass
        elif self.database_config.database == DatabaseType.SUPABASE:
            self.database = SupabaseDB(
                db_connection_config=self.database_config.db_connection_config
            )
        else:
            raise ValueError("Invalid Database Type")

    def insert_many(self, data: List[T]):
        if len(data) == 0:
            print("No data to insert")
            raise ValueError("No data to insert")

        dict_items = []
        for item in data:
            if not isinstance(item, BaseModel):
                raise ValueError("Invalid data type - must be a pydantic BaseModel")
            dict_items.append(item.model_dump())

        return self.database.insert_many(dict_items)
