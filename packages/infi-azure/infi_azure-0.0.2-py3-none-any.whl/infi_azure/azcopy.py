import subprocess
import logging


def azcopy_action(azcopy_path: str, source_folder: str, destination_container: str) -> None:
    """
    Copies the contents of a source folder to a destination container in Azure Blob Storage using AzCopy.
    """
    azcopy_command: list = [
        azcopy_path,
        "copy",
        "--recursive",
        "--overwrite=false",
        source_folder,
        destination_container
    ]
    try:
        subprocess.run(azcopy_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                       encoding='utf-8', check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Azcopy action failed - {str(e)}")
    except FileNotFoundError as e:
        logging.error(f"Azcopy - FileNotFoundError - {str(e)}")
