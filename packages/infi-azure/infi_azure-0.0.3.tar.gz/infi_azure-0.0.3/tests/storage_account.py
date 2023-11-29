import pytest
import logging

from azure.storage.blob import BlobServiceClient

from infi_azure import AzureStorageAccount
from tests import TestConfig

CONNECTION_STRING = TestConfig.TEST_CONNECTION_STRING
LOGGER = logging.getLogger(__name__)


def test_init_valid_connection_string():
    azure_storage: AzureStorageAccount = AzureStorageAccount(CONNECTION_STRING)
    assert isinstance(azure_storage.blob_service_client, BlobServiceClient)


def test_init_invalid_connection_string(caplog):
    caplog.set_level(logging.ERROR)
    AzureStorageAccount(TestConfig.TEST_INVALID_CONNECTION_STRING)
    assert 'The connection string is incorrect' in caplog.text


def test_get_details_from_connection_string():
    azure_storage: AzureStorageAccount = AzureStorageAccount(CONNECTION_STRING)
    account_name, account_key = azure_storage.get_details_from_connection_string()
    assert account_name is not None
    assert account_key is not None


def test_is_account_exist():
    azure_storage: AzureStorageAccount = AzureStorageAccount(CONNECTION_STRING)
    assert azure_storage.is_account_exist() is True


def test_is_account_not_exist():
    azure_storage: AzureStorageAccount = AzureStorageAccount(TestConfig.TEST_INVALID_CONNECTION_STRING)
    assert azure_storage.is_account_exist() is False


def test_is_container_exist():
    azure_storage: AzureStorageAccount = AzureStorageAccount(TestConfig.TEST_CONNECTION_STRING)
    assert azure_storage.is_container_exist(TestConfig.TEST_CONTAINER_NAME) is True


def test_is_container_not_exist():
    azure_storage: AzureStorageAccount = AzureStorageAccount(TestConfig.TEST_CONNECTION_STRING)
    assert azure_storage.is_container_exist(TestConfig.TEST_NOT_EXIST_CONTAINER) is False


if __name__ == "__main__":
    pytest.main()
