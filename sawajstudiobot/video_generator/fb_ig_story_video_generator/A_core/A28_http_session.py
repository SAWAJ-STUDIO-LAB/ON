"""A28_http_session.py — Create and manage HTTP sessions with retry mechanism.

This module provides a function to create a requests Session with retry capabilities,
useful for handling transient network errors and improving reliability.
"""

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def create_session():
    """Create a requests Session with retry settings.

    Returns:
        requests.Session: A session object with retry configured.
    """
    session = requests.Session()
    retry_strategy = Retry(
        total=5,
        backoff_factor=1.5,
        status_forcelist=[429, 500, 502, 503, 504],
        # Read more about retry strategies here: https://urllib3.readthedocs.io/en/latest/reference/urllib3.util.html#urllib3.util.retry.Retry
    )

    # Mount the session with the retry strategy
    session.mount("https://", HTTPAdapter(max_retries=retry_strategy))

    return session

# Example usage:
# session = create_session()
# response = session.get('https://api.example.com/data')
# print(response.text)
