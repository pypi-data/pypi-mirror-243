import logging

from azure.storage.blob import BlobClient

from infi_azure.container import AzureContainer


class AzureBlob(AzureContainer):
    def __init__(self, connection_string: str, container_name: str, blob_name: str):
        try:
            super().__init__(connection_string, container_name)
            self.blob_client: BlobClient = self.container_client.get_blob_client(blob_name)
            self.blob_name: str = blob_name
        except Exception as e:
            logging.error(f"Failed to connect blob client - {str(e)}")

    def download_blob(self) -> bytes or None:
        """
        Download a blob from the container and return its content as bytes.
        """
        try:
            blob_data = self.blob_client.download_blob()
            return blob_data.readall()
        except Exception as e:
            logging.error(f"Failed to download blob - {str(e)}")
            return None

    def is_empty_directory(self) -> bool:
        """
        Check if directory is empty.
        """
        try:
            blobs = self.container_client.list_blobs(name_starts_with=self.blob_name+"/")
            empty_blob: str = f"{self.blob_name}/"
            for blob in blobs:
                if blob.name != empty_blob:
                    return False
            return True
        except Exception as e:
            logging.error(f"Failed to check if blob is empty - {str(e)}")

    def create_empty_directory(self) -> None:
        """
        Create empty directory.
        """
        try:
            directory_name = self.blob_name + "/"
            directory_client = self.container_client.get_blob_client(directory_name)
            data = b""  # Empty content
            directory_client.upload_blob(data, overwrite=True)
        except Exception as e:
            logging.error(f"Failed to create empty directory - {str(e)}")

    def blobs_count_in_directory(self) -> int or None:
        """
        Return the amount of blobs inside directory.
        """
        try:
            blob_list = self.container_client.list_blobs(name_starts_with=self.blob_name)
            blob_count = len(list(blob_list))
            return blob_count
        except Exception as e:
            logging.error(f"Failed to count blobs in directory - {str(e)}")
            return None
