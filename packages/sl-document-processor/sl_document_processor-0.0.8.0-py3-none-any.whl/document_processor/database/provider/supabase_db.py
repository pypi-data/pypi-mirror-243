from supabase import Client, create_client

from ._base_db import BaseDB, DatabaseConnectionConfig


class SupabaseDB(BaseDB):
    configuration = None

    def __init__(self, db_connection_config: DatabaseConnectionConfig) -> None:
        if db_connection_config.supabase_db_config is None:
            raise ValueError("Supabase Configuration is required.")

        super().__init__(db_connection_config)
        self.configuration = self.db_connection_config.supabase_db_config

        self.connect()

    def connect(self):
        url: str = self.configuration.url
        key: str = self.configuration.key
        self.client: Client = create_client(url, key)

    def ping(self):
        pass

    def insert(self, data: dict):
        data = self.client.table(self.configuration.table_name).insert(data).execute()
        return len(data.data) > 0

    def update(self, document_id: str, data: dict):
        data = (
            self.client.table(self.configuration.table_name)
            .update(data)
            .eq("id", document_id)
            .execute()
        )

    def delete(self, document_id: str):
        data = (
            self.client.table(self.configuration.table_name)
            .delete()
            .eq("id", document_id)
            .execute()
        )
        return data

    def get(self, document_id: str):
        data = (
            self.client.table(self.configuration.table_name)
            .select("*")
            .eq("id", document_id)
            .execute()
        )
        return data

    def list_all(self, query: dict = None, limit: int = 100):
        request_builder = self.client.table(self.configuration.table_name).select("*")
        if query is not None:
            for key, value in query.items():
                request_builder = request_builder.eq(key, value)
        data = request_builder.limit(limit).execute()
        return data

    def exists(self, filters: dict):
        print(filters)
        response_builder = self.client.table(self.configuration.table_name).select("*")
        for key, value in filters.items():
            response_builder = response_builder.eq(key, value)
        data = response_builder.execute()
        return len(data.data) > 0
