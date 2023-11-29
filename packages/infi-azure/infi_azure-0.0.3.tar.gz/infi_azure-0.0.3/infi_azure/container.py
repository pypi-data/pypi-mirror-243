import logging
from datetime import datetime, timedelta

from azure.storage.blob import (generate_container_sas, ContainerSasPermissions, BlobClient, ContainerClient,
                                _list_blobs_helper)

from infi_azure.storage_account import AzureStorageAccount


class AzureContainer(AzureStorageAccount):
    def __init__(self, connection_string: str, container_name: str):
        try:
            super().__init__(connection_string)
            self.container_name: str = container_name
            self.container_client: ContainerClient = (self.blob_service_client.get_container_client(container_name))
        except Exception as e:
            logging.error(f"Failed to connect container client - {str(e)}")

    def get_all_directories_in_container(self) -> list[str] or None:
        """
        Retrieves a list of all directory names within the specified container.
        """
        try:
            directories: list[_list_blobs_helper.BlobPrefix] = self.container_client.walk_blobs(name_starts_with='',
                                                                                                delimiter='/')
            directories_list: list[str] = []

            for directory in directories:
                directory_name: str = directory.name[:-1]
                if directory_name not in directories_list:
                    directories_list.append(directory_name)
            return directories_list

        except Exception as e:
            logging.error(f"Get all directories in container - {str(e)}")

    def generate_sas_token(self, permission: ContainerSasPermissions, expiry: datetime) -> str or None:
        """
        Generates a Shared Access Signature (SAS) token for a container.
        """
        try:
            if type(permission) is not ContainerSasPermissions:
                raise ValueError("Invalid permission")

            if type(expiry) is not datetime or expiry <= datetime.utcnow():
                raise ValueError("Invalid expiry")

            account_name, account_key = self.get_details_from_connection_string()

            sas_token: str = generate_container_sas(
                account_name=account_name,
                account_key=account_key,
                container_name=self.container_name,
                permission=permission,
                expiry=expiry
            )
            return sas_token
        except ValueError as e:
            logging.error(f"ValueError in generate sas token - {str(e)}")
        except Exception as e:
            logging.error(f"Failed to generate sas token to container - {str(e)}")

    def generate_sas_url(self, directory: str = "") -> str or None:
        """
        Generates url for a container or specific directory.
        """
        try:
            permission: ContainerSasPermissions = ContainerSasPermissions(read=True, write=True, delete=True, list=True,
                                                                          add=True, create=True)
            expiry: datetime = datetime.utcnow() + timedelta(days=365)
            sas_token: str = self.generate_sas_token(permission, expiry)
            sas_url: str = ('https://' + self.account_name + '.blob.core.windows.net/' +
                            self.container_name + "/" + directory + '?' + sas_token)
            return sas_url
        except Exception as e:
            logging.error(f"Failed to generate url to container - {str(e)}")

    def delete_directory(self, directory_name: str) -> None:
        """
        Delete all blobs in directory.
        """
        try:
            blobs_list: list[str] = self.container_client.list_blobs(name_starts_with=directory_name)
            for blob in blobs_list:
                blob_client: BlobClient = self.container_client.get_blob_client(blob)
                blob_client.delete_blob()
        except Exception as e:
            logging.error(f"Failed to delete blobs in directory - {str(e)}")

    def is_directory_exist(self, blob_name: str) -> bool or None:
        """
        Check if directory exist.
        """
        try:
            blob_list = list(self.container_client.list_blobs(name_starts_with=blob_name + "/"))
            return len(blob_list) >= 1
        except Exception as e:
            logging.error(f"Failed to check if blob exist - {str(e)}")
