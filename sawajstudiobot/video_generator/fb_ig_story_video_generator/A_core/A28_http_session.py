"""
A28_http_session.py
Sirf HTTP session with retry.
"""
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def create_session():
    """Create HTTP session with retry."""
    session = requests.Session()
    retry = Retry(
        total=5, backoff_factor=1.5,
        status_forcelist=[429, 500, 502, 503, 504])
    session.mount("https://", HTTPAdapter(max_retries=retry))
    return session
