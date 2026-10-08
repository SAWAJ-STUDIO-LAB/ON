"""
🌐 HTTP Session
"""
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def get_session():
    session = requests.Session()
    retry = Retry(total=5, backoff_factor=1.5,
                  status_forcelist=[429, 500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def get_headers(content_type="application/json"):
    return {"Content-Type": content_type}
