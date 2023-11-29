import os


class TestConfig:
    TEST_CONNECTION_STRING: str = os.environ["infinity100_connection_string"]
    TEST_INVALID_CONNECTION_STRING: str = "invalid_connection_string"

    TEST_CONTAINER_NAME: str = "test"
    TEST_NOT_EXIST_CONTAINER: str = "not-exist-container"

    TEST_BLOB_NAME: str = "ariel_test_folder/misc/פתח תקווה.docx"
    TEST_NOT_EXIST_BLOB: str = "not exist blob"

    TEST_DIRECTORY = "ariel_test_folder/misc"

    TEST_DELETE_BLOB: str = "blob-test/blob"

    TEST_NOT_EMPTY_BLOB_NAME: str = "ariel_test_folder"
    TEST_EMPTY_BLOB_NAME: str = "Wecselman"
    TEST_CREATE_EMPTY_BLOB: str = "new-empty-directory"

    TEST_FROM_CONTAINER_NAME: str = "test"
    TEST_TO_CONTAINER_NAME: str = "input"

    TEST_FROM_DIRECTORY: str = "ariel_test_folder/misc"
    TEST_TO_DIRECTORY: str = "ariel_test_folder"



