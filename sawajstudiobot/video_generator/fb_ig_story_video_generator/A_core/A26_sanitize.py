"""
A26_sanitize.py
Sirf text sanitize.
"""
import re


def sanitize(t):
    """Clean text — remove unicode, quotes, newlines."""
    if not t:
        return ""
    t = re.sub(r'[\u200b-\u200f\ufeff\u202a-\u202e]', '', str(t))
    return t.replace('"', '').replace("'", '').replace('\n', ' ').strip()
