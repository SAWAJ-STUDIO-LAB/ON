"""
A27_ensure_dir.py
Sirf directory ensure.
"""
import os


def ensure_dir(path):
    """Create folder if missing."""
    os.makedirs(path, exist_ok=True)
    return path
