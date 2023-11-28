from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator


class DatabaseConnectionConfig(BaseModel):
    mongo_db_config: Optional["MongoDBConfig"] = Field(
        default=None,
        title="MongoDB Configuration",
        description="MongoDB Configuration",
    )
    planetscale_db_config: Optional["PlanetScaleConfig"] = Field(
        default=None,
        title="PlanetScale Configuration",
        description="PlanetScale Configuration",
    )
    supabase_db_config: Optional["SupabaseConfig"] = Field(
        default=None,
        title="Supabase Configuration",
        description="Supabase Configuration",
    )

    model_config = ConfigDict(extra="forbid")

    @model_validator(mode="after")
    def validate_config(self):
        if (
            self.mongo_db_config is None
            and self.planetscale_db_config is None
            and self.supabase_db_config is None
        ):
            raise ValueError("Invalid Database Configuration")
        return self


class MongoDBConfig(BaseModel):
    host: str
    port: Optional[int] = Field(
        default=27017, description="Port number", title="Port number"
    )
    username: str
    password: str
    database: Optional[str] = Field(
        default=None, description="Database name", title="Database name"
    )
    collection: Optional[str] = Field(
        default=None,
        title="Table Name",
        description="Table name for SQL databases OR collection name for NoSQL databases",
    )


class PlanetScaleConfig(BaseModel):
    host: str
    port: Optional[int] = Field(
        default=3306, description="Port number", title="Port number"
    )
    username: str
    password: str
    database: Optional[str] = Field(
        default=None, description="Database name", alias="db", title="Database name"
    )
    collection: Optional[str] = Field(
        default=None,
        alias="table",
        title="Table Name",
        description="Table name for SQL databases OR collection name for NoSQL databases",
    )


class SupabaseConfig(BaseModel):
    url: str
    key: str
    table_name: str
