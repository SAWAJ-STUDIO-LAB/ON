"""A31_cleanup.py — Handles file and folder cleanup operations.

This module provides a function to remove specified files and folders, ensuring a clean environment for subsequent operations.

Functions:
- cleanup(files, folder=None): Removes the provided files and optionally deletes the specified folder.
"""

import os
import shutil
import logging
from typing import List

from A_core.A9_log_step import log_step


def cleanup(files: List[str], folder: str = None) -> None:
    """Removes the specified files and optionally deletes the provided folder.

    Args:
        files (List[str]): A list of file paths to be removed.
        folder (str, optional): The folder path to be deleted. Defaults to None.

    Returns:
        None

    Raises:
        FileNotFoundError: If any specified file does not exist.
        PermissionError: If there is an issue with permissions during file/folder deletion.
    """
    log_step("A31_cleanup.py", "Initiating cleanup process", "info")

    # Attempt to remove each file
    for f in files:
        try:
            if os.path.exists(f):
                os.remove(f)
                logging.info(f"File {f} removed successfully.")
            else:
                logging.warning(f"File {f} does not exist. Skipping removal.")
        except PermissionError as e:
            logging.error(f"Permission error while removing file {f}: {e}")
            raise

    # Attempt to delete the folder if provided
    if folder:
        try:
            shutil.rmtree(folder, ignore_errors=True)
            logging.info(f"Folder {folder} deleted successfully.")
        except OSError as e:
            logging.error(f"Error deleting folder {folder}: {e}")
            raise

    log_step("A31_cleanup.py", "Cleanup process completed", "ok")
