"""
A34_secrets_env_check.py
Sirf env var check.
"""
import os


def check_env(*names):
    """Check multiple env var names, return first found."""
    for name in names:
        val = os.environ.get(name, "").strip()
        if val and val not in ("your_token_here", "undefined"):
            return (True, name, len(val))
    return (False, names[0] if names else "", 0)
