"""A36_ping_facebook.py — Module to ping Facebook and retrieve page information.

This module is responsible for sending a GET request to the Facebook Graph API to check the status and retrieve the name of a Facebook page.

Functions:
- ping(): Sends a GET request to the Facebook Graph API to fetch page information.

Usage:
    from A36_ping_facebook import ping

    result = ping()
    if result['status'] == 'working':
        print(f"Facebook page '{result['page_name']}' is accessible.")
"""

import os
import requests
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def ping() -> dict:
    """
    Send a GET request to the Facebook Graph API to check the status and retrieve the name of a Facebook page.

    Returns:
    - dict: A dictionary containing the status, page name, and HTTP status code.
    """
    # Retrieve tokens and page ID from environment variables
    token = (os.environ.get("FACEBOOK_META_TOKEN", "").strip()
             or os.environ.get("FACEBOOK_INSTAGRAM_META_TOKEN", "").strip())
    page_id = os.environ.get("FACEBOOK_PAGE_ID", "").strip()

    # Check if tokens and page ID are provided
    if not token or not page_id:
        logger.warning("Facebook credentials not provided. Skipping...")
        return {"status": "skipped", "reason": "no creds"}

    try:
        # Send a GET request to the Facebook Graph API
        response = requests.get(
            f"https://graph.facebook.com/v21.0/{page_id}",
            params={"access_token": token, "fields": "name"},
            timeout=10
        )

        # Check the status code of the response
        if response.status_code == 200:
            page_name = response.json().get("name", "Unknown")
            logger.info(f"Facebook page '{page_name}' is accessible.")
            return {"status": "working", "page_name": page_name, "code": 200}
        else:
            logger.error(f"Failed to access Facebook page. Status code: {response.status_code}")
            return {"status": "failed", "code": response.status_code}

    except requests.exceptions.RequestException as e:
        logger.error(f"An error occurred while pinging Facebook: {e}")
        return {"status": "error", "reason": str(e)[:60]}
