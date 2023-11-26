import tempfile
import uuid
from typing import Optional

import yaml

from document_processor.cloud_storage import CloudConfig, CloudStorageManager

from document_processor.database import DatabaseConfig, DatabaseManager

from .models import CloudProvider, ConfigurationSettings, ExtractionConfig, HTML


class HTMLConfigurer:
    """
    This class is used to process a given URL.
    This class can be used to interact with the underlying database to store the scraping configuration files.
    It will check if the URL exists in the database, if not it will add it.
    """

    def __init__(
        self, url_details: HTML, db_config: DatabaseConfig, cloud_cofig: CloudConfig
    ):
        self.url = url_details.url

        self.db_config = db_config
        self.database_manager = DatabaseManager(db_config)
        self.db_record = self.get_database_record()

        self.cloud_cofig = cloud_cofig
        self.cloud_store_manager = CloudStorageManager(cloud_cofig)
        self.cloud_record = self.get_cloud_storage_configuration()

    def get_database_record(self):
        if not self.url_exists_in_database():
            self.add_url_to_database()

        return self.database_manager.database.list_all({"url": self.url})

    def get_cloud_storage_configuration(self) -> Optional[ExtractionConfig]:
        yaml_file_name: str = self.db_record.data[0]["yaml_file_name"]
        if not self.file_exists_in_cloud_storage(yaml_file_name=yaml_file_name):
            return None

        if self.cloud_store_manager.cloud_storage is None:
            raise ValueError("Cloud storage is not configured.")

        response = self.cloud_store_manager.cloud_storage.get(key=yaml_file_name)

        # load the yaml file into a dictionary
        configuration = yaml.safe_load(response["Body"].read())

        return ExtractionConfig(**configuration)

    def url_exists_in_database(self) -> bool:
        return self.database_manager.database.exists({"url": self.url})

    def file_exists_in_cloud_storage(self, yaml_file_name: str = None) -> bool:
        if self.cloud_store_manager.cloud_storage is None:
            raise ValueError("Cloud storage is not configured.")

        return self.cloud_store_manager.cloud_storage.file_exists(yaml_file_name)

    def add_url_to_database(self) -> None:
        random_uuid = uuid.uuid5(uuid.NAMESPACE_DNS, self.url)
        url_metadata = ConfigurationSettings(
            url=self.url,
            yaml_file_name=f"{random_uuid}.yaml",
            cloud_provider=CloudProvider.AWS,
        )

        if self.database_manager.database is None:
            raise ValueError("Database is not configured.")

        self.database_manager.database.insert(url_metadata.model_dump(mode="json"))

    def write_configuration_to_cloud_storage(
        self, configuration: ExtractionConfig, overwrite: bool = False
    ) -> None:
        yaml_file_name = self.db_record.data[0]["yaml_file_name"]

        if (
            not self.file_exists_in_cloud_storage(yaml_file_name=yaml_file_name)
        ) or overwrite:
            print("Writing to cloud storage")
            with tempfile.NamedTemporaryFile("w+") as tmp:
                yaml.dump(configuration.model_dump(mode="json"), tmp)
                tmp.seek(0)

                if self.cloud_store_manager.cloud_storage is None:
                    raise ValueError("Cloud storage is not configured.")

                self.cloud_store_manager.cloud_storage.put(
                    file_path=tmp.name, key=yaml_file_name
                )

            document_id: str = self.db_record.data[0]["id"]

            if self.database_manager.database is None:
                raise ValueError("Database is not configured.")

            self.database_manager.database.update(
                document_id=document_id, data={"processed": True}
            )

            self.cloud_record = self.get_cloud_storage_configuration()
