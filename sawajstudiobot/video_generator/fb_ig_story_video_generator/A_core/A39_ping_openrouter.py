"""A39_ping_openrouter.py — Module to ping OpenRouter API and check its status.

This module retrieves the API key from environment variables and sends a GET request to the OpenRouter API endpoint.
It returns a dictionary with the status and response code.

Functions:
- ping(): Sends a GET request to the OpenRouter API and returns the status and response code.
"""

import os
import requests
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def ping() -> dict:
    """
    Ping the OpenRouter API and return the status and response code.

    Returns:
    - dict: A dictionary containing the status and response code.
    """
    # Retrieve API key from environment variables
    openrouter_key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    openrouter_key_ai = os.environ.get("OPENROUTER_API_KEY_AI", "").strip()
    if not openrouter_key and not openrouter_key_ai:
        logger.warning("No API key found in environment variables.")
        return {"status": "skipped", "reason": "no key"}

    key = openrouter_key or openrouter_key_ai

    try:
        # Send a GET request to the OpenRouter API
        response = requests.get(
            "https://openrouter.ai/api/v1/models",
            headers={"Authorization": f"Bearer {key}"},
            timeout=10
        )
        response.raise_for_status()  # Raise an exception for non-2xx status codes

        # Return success status and response code
        return {"status": "working", "code": response.status_code}

    except requests.exceptions.RequestException as e:
        # Handle request exceptions
        logger.error(f"Request to OpenRouter API failed: {e}")
        return {"status": "error", "reason": str(e)[:60]}

    except Exception as e:
        # Handle other exceptions
        logger.error(f"Unexpected error: {e}")
        return {"status": "error", "reason": str(e)[:60]}
