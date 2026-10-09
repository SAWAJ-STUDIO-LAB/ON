"""A29_http_download.py — A module for downloading files via HTTP requests.

This module provides a function to download files from a given URL and save them to a specified path.
It includes error handling and logging for a robust download process.

Functions:
- download(session, url, path, min_size=12000): Attempts to download a file from the URL and save it to the path.
  - session: The requests session object.
  - url: The URL of the file to be downloaded.
  - path: The path where the downloaded file will be saved.
  - min_size: The minimum size (in bytes) the downloaded file should have to be considered valid. Default is 12000 bytes.
  Returns: True if the download was successful, False otherwise.
"""

import logging
from typing import BinaryIO, Optional

from A_core.A9_log_step import log_step


def download(session, url: str, path: str, min_size: int = 12000) -> bool:
    """Attempts to download a file from the URL and save it to the specified path.

    Args:
        session (requests.Session): The requests session object.
        url (str): The URL of the file to download.
        path (str): The path where the downloaded file will be saved.
        min_size (int, optional): The minimum size in bytes for a valid download. Defaults to 12000 bytes.

    Returns:
        bool: True if the download was successful, False otherwise.
    """
    try:
        response = session.get(url, timeout=35)
        response.raise_for_status()  # Raise an exception for non-200 status codes

        if len(response.content) > min_size:
            with open(path, "wb") as file:
                file.write(response.content)
            log_step("A29_http_download.py", f"Downloaded {path} successfully", "ok", f"{len(response.content) // 1024} KB")
            return True
        else:
            log_step("A29_http_download.py", f"Downloaded file size is less than {min_size} bytes", "warning")
            return False

    except requests.exceptions.RequestException as e:
        log_step("A29_http_download.py", f"Error downloading file: {e}", "fail")
        return False
    except Exception as e:
        log_step("A29_http_download.py", f"Unexpected error: {e}", "fail")
        return False
