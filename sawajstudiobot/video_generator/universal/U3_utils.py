"""
U3_utils.py — Universal Sanitize + Helpers
"""

import os
import re


def sanitize(t):
    """Clean text: unicode invisibles, quotes, newlines."""
    if not t:
        return ""
    t = re.sub(r'[\u200b-\u200f\ufeff\u202a-\u202e]', '', str(t))
    return t.replace('"', '').replace("'", '').replace('\n', ' ').strip()


def ensure_dir(path):
    """Create folder if missing."""
    os.makedirs(path, exist_ok=True)
    return path
