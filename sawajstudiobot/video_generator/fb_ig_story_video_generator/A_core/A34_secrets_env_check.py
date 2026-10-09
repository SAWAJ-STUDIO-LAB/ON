"""A34_secrets_env_check.py — Check environment variables for secrets and sensitive information.

This module provides a function to check if sensitive information is present in environment variables.
It is designed to ensure that sensitive data is not exposed in the environment, especially during development and testing.

Functions:
- check_env(*names): Checks the existence and validity of environment variables.
  Args:
    *names (str): Variable number of environment variable names to check.
  Returns:
    tuple: A tuple containing three elements:
    1. bool: True if any of the environment variables contain valid secrets, False otherwise.
    2. str: The name of the environment variable that contains valid secrets, or the first variable name if none are valid.
    3. int: The length of the valid secret found, or 0 if none are found.
"""

import os
import logging
from typing import Tuple


def check_env(*names: str) -> Tuple[bool, str, int]:
    """Check the existence and validity of environment variables.

    Args:
        *names (str): Variable number of environment variable names to check.

    Returns:
        Tuple[bool, str, int]: A tuple containing three elements:
        1. bool: True if any of the environment variables contain valid secrets, False otherwise.
        2. str: The name of the environment variable that contains valid secrets, or the first variable name if none are valid.
        3. int: The length of the valid secret found, or 0 if none are found.
    """
    try:
        for name in names:
            val = os.environ.get(name, "").strip()
            if val and val not in ("your_token_here", "undefined"):
                logging.info(f"Valid secret found in {name} with length {len(val)}")
                return (True, name, len(val))
        logging.warning("No valid secrets found in the provided environment variables.")
        return (False, names[0] if names else "", 0)
    except KeyError as e:
        logging.error(f"Environment variable not found: {e}")
        return (False, names[0] if names else "", 0)
    except Exception as e:
        logging.error(f"An error occurred while checking environment variables: {e}")
        return (False, names[0] if names else "", 0)
