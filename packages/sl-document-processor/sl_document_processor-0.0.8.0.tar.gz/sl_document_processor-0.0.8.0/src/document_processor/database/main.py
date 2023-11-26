from enum import Enum

from pydantic import BaseModel

from .provider import DatabaseConnectionConfig, MongoDB, SupabaseDB


class DatabaseType(str, Enum):
    MONGODB = "mongodb"
    POSTGRESQL = "postgresql"
    MYSQL = "mysql"
    SUPABASE = "supabase"


class DatabaseConfig(BaseModel):
    database: DatabaseType
    db_connection_config: DatabaseConnectionConfig


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
