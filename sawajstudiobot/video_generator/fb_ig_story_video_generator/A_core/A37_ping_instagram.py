"""A37_ping_instagram.py — Module to ping Instagram and retrieve account information.

This module is designed to check the Instagram account status and fetch the username.

Functions:
- ping(): Sends a request to the Instagram Graph API and returns a dictionary with status and related information.

Usage:
    from A37_ping_instagram import ping

    result = ping()
    if result['status'] == 'working':
        print(f"Instagram account is active with username: {result['username']}")
"""

import os
import requests
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def ping() -> dict:
    """
    Sends a request to Instagram's Graph API to check the account status and fetch the username.

    Returns a dictionary with the following keys:
        - status: 'working' if successful, 'failed' or 'error' otherwise.
        - username: Instagram username if status is 'working', otherwise a placeholder.
        - code: HTTP status code if status is 'failed', error message length if 'error'.

    Raises:
        None

    """
    # Retrieve Instagram credentials from environment variables
    token = os.environ.get("FACEBOOK_INSTAGRAM_META_TOKEN", "").strip()
    ig_id = os.environ.get("INSTAGRAM_BUSINESS_ACCOUNT_ID", "").strip()

    if not token or not ig_id:
        logger.warning("Instagram credentials not found. Skipping Instagram ping.")
        return {"status": "skipped", "reason": "no creds"}

    try:
        # Send a GET request to Instagram Graph API
        response = requests.get(
            f"https://graph.facebook.com/v21.0/{ig_id}",
            params={"access_token": token, "fields": "username"},
            timeout=10
        )

        # Check the response status code
        if response.status_code == 200:
            data = response.json()
            return {"status": "working", "username": data.get("username", "?"), "code": 200}
        else:
            return {"status": "failed", "code": response.status_code}

    except requests.exceptions.RequestException as e:
        logger.error(f"Error occurred while pinging Instagram: {e}")
        return {"status": "error", "reason": str(e)[:60]}
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        return {"status": "error", "reason": str(e)[:60]}
