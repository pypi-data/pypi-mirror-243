from enum import Enum

from pydantic import BaseModel, ConfigDict

from .provider import DatabaseConnectionConfig


class DatabaseType(str, Enum):
    MONGODB = "mongodb"
    POSTGRESQL = "postgresql"
    MYSQL = "mysql"
    SUPABASE = "supabase"


class DatabaseConfig(BaseModel):
    database: DatabaseType
    db_connection_config: DatabaseConnectionConfig
    model_config = ConfigDict(extra="forbid")
