"""A38_ping_drive.py — Module to ping Google Drive and check credentials.

This module is responsible for sending a request to Google's OAuth2 endpoint to verify the provided Drive credentials.
It returns a dictionary with the status and relevant information.

Functions:
- ping(): Sends a request to Google's OAuth2 endpoint to refresh the access token and checks the response.

Usage:
    from A38_ping_drive import ping

    result = ping()
    if result["status"] == "working":
        # Proceed with Drive operations

Attributes:
    None

Methods:
    None
"""

import os
import requests
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def ping() -> dict:
    """
    Sends a request to Google's OAuth2 endpoint to refresh the access token and checks the response.

    Args:
        None

    Returns:
        dict: A dictionary containing the status and relevant information.
            - status (str): 'working' if successful, 'failed' if HTTP error, 'error' for exceptions, or 'skipped' if creds missing.
            - code (int): HTTP status code if 'failed', error message if 'error', or None otherwise.
            - reason (str): Error message if 'error', or None otherwise.

    Raises:
        None
    """
    # Get environment variables
    client_id = os.environ.get("GOOGLE_DRIVE_CLIENT_ID", "").strip()
    client_secret = os.environ.get("GOOGLE_DRIVE_CLIENT_SECRET", "").strip()
    refresh_token = os.environ.get("GOOGLE_DRIVE_REFRESH_TOKEN", "").strip()

    if not all([client_id, client_secret, refresh_token]):
        logger.warning("Missing Google Drive credentials. Skipping ping.")
        return {"status": "skipped", "reason": "missing creds"}

    try:
        # Prepare request data
        request_data = {
            "client_id": client_id,
            "client_secret": client_secret,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token"
        }

        # Send request to Google's OAuth2 endpoint
        response = requests.post("https://oauth2.googleapis.com/token", data=request_data, timeout=10)

        # Check response status code
        if response.status_code == 200:
            # Access token refresh was successful
            logger.info("Google Drive ping successful.")
            return {"status": "working", "code": 200}
        else:
            # HTTP error occurred
            logger.error("Google Drive ping failed with status code %s", response.status_code)
            return {"status": "failed", "code": response.status_code}

    except requests.RequestException as e:
        # Handle request exceptions
        logger.error("Google Drive ping failed: %s", str(e))
        return {"status": "error", "reason": str(e)[:60]}
    except Exception as e:
        # Handle unexpected exceptions
        logger.exception("Unexpected error during Google Drive ping: %s", str(e))
        return {"status": "error", "reason": str(e)[:60]}
