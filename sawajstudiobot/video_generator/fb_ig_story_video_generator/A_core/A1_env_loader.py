"""
A1_env_loader.py
Sirf env var load karna.
"""
import os


def get_env(name, default=""):
    """Get env var and strip whitespace."""
    return os.environ.get(name, default).strip()
