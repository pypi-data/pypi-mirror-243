"""Module to communicating with file storage
"""

import os

from nazca4sdk.datahandling.open_data_client import OpenDataClient
from dependency_injector.wiring import inject


class FileStorage:
    """Communicate with file storage
    """

    @inject
    def __init__(self, opendata_client: OpenDataClient):
        self.opendata = opendata_client

    def download_file(self, path: str, local_path: str, override=False):
        """download file from file storage

        Args:
            path: path to file on file storage
            local_path: Path to save the file
            override: True - override existing file
        Returns:
            True - file download and saved , False - download error
        """

        if os.path.exists(local_path) and not override:
            print(f"File {local_path} already exist. Set override=True to override file.")
            return False
        if local_path.endswith("\\") or local_path.endswith("/"):
            print(f"local_path should be a file")
            return False
        return self.opendata.download_file(path, local_path)

    def send_file(self, path: str, local_path: str):
        """send file to file storage

        Args:
            path: path where file will be store
            local_path: file to send

        Returns:
            True when file store to file storage
            False when something bad happen
        """
        if not os.path.exists(local_path):
            print(f"file {local_path} not exist")
            return False
        file = open(local_path, 'rb')

        return self.opendata.send_file(path, file)
