"""A2_env_fallback.py — Retrieve environment variables with multi-name fallback.

This module provides a function to retrieve environment variables with a fallback mechanism.
It allows specifying multiple environment variable names and returns the value of the first
non-empty variable found. If none are set, it returns a default value.

Functions:
- get_env_fallback: Retrieves environment variable values with fallback and default.

Example:
    >>> get_env_fallback('VAR1', 'VAR2', default='default_value')
    'Value of VAR1 or VAR2, or "default_value" if both are empty'

Attributes:
    None

"""

import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_env_fallback(*names: str, default: str = "") -> str:
    """Retrieve environment variable values with fallback and default.

    Args:
        *names (str): Variable number of environment variable names to check.
        default (str, optional): Default value to return if all names are empty. Defaults to "".

    Returns:
        str: Value of the first non-empty environment variable found, or the default.

    Raises:
        TypeError: If any of the names provided is not a string.

    """
    for name in names:
        if not isinstance(name, str):
            raise TypeError(f"Expected string for environment variable name, got {type(name)}")
        val = os.environ.get(name, "").strip()
        if val:
            logger.info(f"Using value '{val}' for environment variable '{name}'")
            return val
    logger.info(f"All environment variables are empty, returning default: {default}")
    return default
