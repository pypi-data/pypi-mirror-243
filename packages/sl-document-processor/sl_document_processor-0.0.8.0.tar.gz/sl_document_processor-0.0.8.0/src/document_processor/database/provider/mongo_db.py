from functools import wraps
from typing import Optional

from bson.objectid import ObjectId

from pymongo import MongoClient

from ._base_db import BaseDB, DatabaseConnectionConfig


def collection_required(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if self.is_collection_set():
            response = func(self, *args, **kwargs)
            return response

        print(
            f"No collection set. Please set a collection to perform this operation - {func.__name__}"
        )
        return None

    return wrapper


class MongoDB(BaseDB):
    configuration = None
    db = None
    collection = None

    def __init__(self, db_connection_config: DatabaseConnectionConfig) -> None:
        if db_connection_config.mongo_db_config is None:
            raise ValueError("MongoDB Configuration is required.")

        super().__init__(db_connection_config)
        self.configuration = db_connection_config.mongo_db_config
        self.connect()

    def ping(self):
        if self.client is None:
            self.connect()

        # Send a ping to confirm a successful connection
        try:
            self.client.admin.command("ping")
            return "Pinged your deployment. You successfully connected to MongoDB!"
        except Exception as e:
            print(e)
            return "Something went wrong. Unable to connect to MongoDB."

    def is_collection_set(self):
        return self.collection is not None

    def connect(self) -> MongoClient:
        if (
            self.db_connection_config is None
            or self.db_connection_config.mongo_db_config is None
        ):
            raise ValueError("MongoDB Client is required.")

        try:
            self.client = MongoClient(
                host=self.db_connection_config.mongo_db_config.host,
                port=self.db_connection_config.mongo_db_config.port,
                username=self.db_connection_config.mongo_db_config.username,
                password=self.db_connection_config.mongo_db_config.password,
            )

            if (
                self.db_connection_config.mongo_db_config.collection is not None
                and self.db_connection_config.mongo_db_config.collection != ""
                and self.db is None
            ):
                self.set_db(self.db_connection_config.mongo_db_config.collection)

            if (
                self.db_connection_config.mongo_db_config.collection is not None
                and self.db_connection_config.mongo_db_config.collection != ""
                and self.collection is None
            ):
                self.set_collection(
                    self.db_connection_config.mongo_db_config.collection
                )

            return self.client
        except TypeError as e:
            print(e)
            return None

    def set_db(self, db_name: str):
        if self.client is None:
            self.connect()

        self.db = self.client[db_name]

    def set_collection(self, collection_name: str):
        if self.db is None:
            self.set_db(self.db_connection_config.mongo_db_config.collection)

        try:
            self.collection = self.db[collection_name]
        except Exception as e:
            print(e)
            print(
                "Database cannot be None. Please set a database before setting a collection."
            )

    @collection_required
    def insert(self, data: dict):
        reponse = self.collection.insert_one(data)

        return str(reponse.inserted_id)

    @collection_required
    def update(self, document_id: str, data: dict):
        response = self.collection.update_one(
            {"_id": ObjectId(document_id)}, {"$set": data}
        )
        return response.modified_count

    @collection_required
    def delete(self, document_id: Optional[str] = None, data: Optional[dict] = None):
        if document_id is not None:
            response = self.collection.delete_one({"_id": ObjectId(document_id)})
        elif data is not None:
            response = self.collection.delete_many(data)

        return response.deleted_count

    @collection_required
    def get(self, document_id: str):
        response = self.collection.find_one({"_id": ObjectId(document_id)})
        return response

    @collection_required
    def list_all(self, query: dict = None, limit: int = 100):
        if query is None:
            query = {}
        response = self.collection.find(query).limit(limit)
        return list(response)

    @collection_required
    def exists(self, filters: dict):
        response = self.collection.find_one(filters)
        return response is not None
