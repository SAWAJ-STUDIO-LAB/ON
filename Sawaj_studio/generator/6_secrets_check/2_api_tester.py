"""
🌐 API Tester
"""
import requests


def test_url(url, headers=None, timeout=10):
    try:
        r = requests.get(url, headers=headers or {}, timeout=timeout)
        return r.status_code == 200
    except Exception:
        return False


def test_post(url, headers=None, data=None, timeout=10):
    try:
        r = requests.post(url, headers=headers or {}, json=data or {}, timeout=timeout)
        return r.status_code == 200
    except Exception:
        return False
