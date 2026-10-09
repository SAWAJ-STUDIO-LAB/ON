"""
A40_ping_groq.py — Module to check the status of the Groq API.

This module pings the Groq API to ensure it is accessible and functional.

Functions:
- ping(): Sends a request to the Groq API and returns a status dictionary.
"""

import os
import requests
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def ping() -> dict:
    """
    Sends a GET request to the Groq API and returns a status dictionary.

    Returns:
    - A dictionary with 'status' and 'code' or 'reason' keys. 'status' can be 'working', 'failed', 'error', or 'skipped'.

    Raises:
    - None
    """
    # Get the API key from environment variables
    api_key = os.environ.get("GROQ_API_KEY", "").strip() or os.environ.get("GROQ_API_KEY_AI", "").strip()

    if not api_key:
        logger.warning("No API key provided. Skipping Groq API ping.")
        return {"status": "skipped", "reason": "No API key provided."}

    try:
        # Send a GET request to the Groq API
        response = requests.get(
            "https://api.groq.com/openai/v1/models",
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=10
        )

        # Check the status code
        if response.status_code == 200:
            status = "working"
        else:
            status = "failed"

        return {"status": status, "code": response.status_code}

    except requests.RequestException as e:
        logger.error(f"Error occurred while pinging Groq API: {e}")
        return {"status": "error", "reason": str(e)[:60]}
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        return {"status": "error", "reason": str(e)[:60]}
