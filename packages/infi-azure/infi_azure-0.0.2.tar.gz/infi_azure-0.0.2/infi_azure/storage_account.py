import logging
import os

from azure.storage.blob import BlobServiceClient

from consts import Const


class AzureStorageAccount:
    def __init__(self, connection_string: str) -> None:
        try:
            self.connection_string: str = connection_string
            self.account_name, self.account_key = self.get_details_from_connection_string()
            if self.is_account_exist() is False:
                logging.error("The connection string is incorrect")
                return
            self.blob_service_client: BlobServiceClient = BlobServiceClient.from_connection_string(connection_string)
        except Exception as e:
            logging.error(f"Failed to connect the azure storage account - {str(e)}")

    def get_details_from_connection_string(self) -> tuple[str | None, str | None]:
        """
        Get account name and key from the connection string.
        """
        try:
            parts: list[str] = self.connection_string.split(";")
            account_name = None
            account_key = None

            for part in parts:
                if part.startswith(Const.PROTOCOL_PREFIX):
                    continue  # Skip the protocol part
                elif part.startswith(Const.ACCOUNT_NAME_PREFIX):
                    account_name = part.split("=", 1)[Const.ACCOUNT_NAME_INDEX]
                elif part.startswith(Const.ACCOUNT_KEY_PREFIX):
                    account_key = part.split("=", 1)[Const.ACCOUNT_KEY_INDEX]

            return account_name, account_key
        except Exception as e:
            logging.error(f"Failed to get details from connection string - {str(e)}")

    def is_account_exist(self):
        """
        Check if account exist.
        """
        try:
            account_name: str = self.account_name
            if f'{account_name}_connection_string' not in os.environ:
                return False
            return True
        except Exception as e:
            logging.error(f"Failed to get details from connection string - {str(e)}")
