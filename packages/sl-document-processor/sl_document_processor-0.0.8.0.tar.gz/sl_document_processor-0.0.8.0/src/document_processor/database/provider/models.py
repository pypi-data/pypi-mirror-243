from typing import Optional

from pydantic import BaseModel, Field


class MongoDBConfig(BaseModel):
    host: str
    port: Optional[int] = Field(
        default=27017, description="Port number", title="Port number"
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
