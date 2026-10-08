"""
A2_env_fallback.py
Sirf multi-name fallback.
"""
import os


def get_env_fallback(*names, default=""):
    """Try multiple env names, return first non-empty."""
    for name in names:
        val = os.environ.get(name, "").strip()
        if val:
            return val
    return default
