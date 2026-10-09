"""A27_ensure_dir.py — Ensure the existence of a directory and create it if it doesn't exist.

This module provides a simple function to ensure a directory path exists.
It uses the 'os' module to create the directory if it doesn't exist, and handles any potential exceptions.

Functions:
- ensure_dir(path: str) -> str: Creates the directory at the given path if it doesn't exist and returns the path.
"""

import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def ensure_dir(path: str) -> str:
    """
    Ensure the existence of a directory and create it if it doesn't exist.

    Args:
        path (str): The directory path to ensure and create.

    Returns:
        str: The input path, with the directory created if it didn't exist.

    Raises:
        TypeError: If the input path is not a string.
        OSError: If there is an issue with creating the directory.
    """
    try:
        # Check if the input is a string
        if not isinstance(path, str):
            raise TypeError("Input path must be a string.")

        # Create the directory if it doesn't exist
        os.makedirs(path, exist_ok=True)
        logger.info(f"Directory '{path}' created or already exists.")

        return path

    except OSError as e:
        logger.error(f"Error creating directory '{path}': {e}")
        raise
