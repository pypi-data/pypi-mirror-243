import pytest

from azure.storage.blob import ContainerClient, BlobClient

from infi_azure import AzureBlob
from tests import TestConfig


def instance_azure_blob(blob_name: str) -> AzureBlob:
    return AzureBlob(TestConfig.TEST_CONNECTION_STRING, TestConfig.TEST_CONTAINER_NAME, blob_name)


def test_init_valid():
    blob_name: str = TestConfig.TEST_BLOB_NAME
    blob = AzureBlob(TestConfig.TEST_CONNECTION_STRING, TestConfig.TEST_CONTAINER_NAME, blob_name)
    assert isinstance(blob.container_client, ContainerClient)
    assert isinstance(blob_name, str)
    assert isinstance(blob.blob_client, BlobClient)


def test_download_blob():
    azure_blob: AzureBlob = instance_azure_blob(TestConfig.TEST_BLOB_NAME)
    assert isinstance(azure_blob.download_blob(), bytes)


def test_is_not_empty_directory():
    azure_blob: AzureBlob = instance_azure_blob(TestConfig.TEST_NOT_EMPTY_BLOB_NAME)
    assert azure_blob.is_empty_directory() is False


def test_is_empty_directory():
    azure_blob: AzureBlob = instance_azure_blob(TestConfig.TEST_EMPTY_BLOB_NAME)
    assert azure_blob.is_empty_directory() is True


def test_create_empty_directory():
    azure_blob: AzureBlob = instance_azure_blob(TestConfig.TEST_CREATE_EMPTY_BLOB)
    azure_blob.create_empty_directory()
    assert azure_blob.is_empty_directory() is True
    azure_blob.delete_directory(TestConfig.TEST_CREATE_EMPTY_BLOB)


def test_count_blobs_in_directory():
    azure_blob: AzureBlob = instance_azure_blob(TestConfig.TEST_BLOB_NAME)
    assert isinstance(azure_blob.blobs_count_in_directory(), int)


if __name__ == "__main__":
    pytest.main()
