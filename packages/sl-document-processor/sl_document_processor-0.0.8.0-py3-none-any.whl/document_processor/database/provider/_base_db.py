import abc

from typing import Optional

from pydantic import BaseModel, Field

from .models import MongoDBConfig, PlanetScaleConfig, SupabaseConfig


class DatabaseConnectionConfig(BaseModel):
    mongo_db_config: Optional[MongoDBConfig] = Field(
        default=None,
        alias="mongodb",
        title="MongoDB Configuration",
        description="MongoDB Configuration",
    )
    planetscale_db_config: Optional[PlanetScaleConfig] = Field(
        default=None,
        alias="planetscale",
        title="PlanetScale Configuration",
        description="PlanetScale Configuration",
    )
    supabase_db_config: Optional[SupabaseConfig] = Field(
        default=None,
        alias="supabase",
        title="Supabase Configuration",
        description="Supabase Configuration",
    )


class BaseDB(abc.ABC):
    db_connection_config = None
    client = None

    def __init__(self, db_connection_config: DatabaseConnectionConfig) -> None:
        self.db_connection_config = db_connection_config

    @abc.abstractmethod
    def insert(self, data: dict):
        pass

    @abc.abstractmethod
    def update(self, document_id: str, data: dict):
        pass

    @abc.abstractmethod
    def delete(self, document_id: str):
        pass

    @abc.abstractmethod
    def get(self, document_id: str):
        pass

    @abc.abstractmethod
    def list_all(self, query: dict = None, limit: int = 100):
        pass

    @abc.abstractmethod
    def exists(self, filters: dict):
        pass
