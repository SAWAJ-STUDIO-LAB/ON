"""A41_ping_pexels.py — Pings the Pexels API to check its status.

This module is responsible for sending a simple request to the Pexels API and evaluating its response.
It is used to ensure that the Pexels API is accessible and functioning correctly.

Functions:
- ping(): Sends a GET request to the Pexels API and returns a dictionary with the status and relevant information.
"""

import os
import requests
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def ping() -> dict:
    """
    Pings the Pexels API to check its status.

    Returns a dictionary with the status and relevant information.
    If the API key is not set, returns a 'skipped' status with a reason.
    If the request is successful, returns a 'working' status with the HTTP status code.
    If the request fails, returns an 'error' status with the exception message.

    Args:
        None

    Returns:
        dict: A dictionary containing the status and additional information.
    """
    # Get the Pexels API key from environment variables
    pexels_api_key = os.environ.get("PEXELS_API_KEY", "").strip()

    if not pexels_api_key:
        logger.warning("Pexels API key is not set. Skipping Pexels ping.")
        return {"status": "skipped", "reason": "No API key provided."}

    try:
        # Prepare the request parameters
        params = {"query": "test", "per_page": 1}
        headers = {"Authorization": pexels_api_key}

        # Send a GET request to the Pexels API
        response = requests.get("https://api.pexels.com/videos/search", params=params, headers=headers, timeout=10)

        # Check the status code of the response
        if response.status_code == 200:
            logger.info("Pexels API is working. Status code: %s", response.status_code)
            return {"status": "working", "code": response.status_code}
        else:
            logger.error("Pexels API request failed. Status code: %s", response.status_code)
            return {"status": "failed", "code": response.status_code}

    except requests.exceptions.RequestException as e:
        logger.error("An error occurred while pinging Pexels API: %s", str(e))
        return {"status": "error", "reason": str(e)[:60]}
    except Exception as e:
        logger.exception("Unexpected error while pinging Pexels API: %s", str(e))
        return {"status": "error", "reason": "Unexpected error: " + str(e)[:60]}
