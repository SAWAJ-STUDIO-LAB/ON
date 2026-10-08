"""A34_secrets_env_check.py — Sirf env check."""
import os


def check_env(*names):
    for name in names:
        val = os.environ.get(name, "").strip()
        if val and val not in ("your_token_here", "undefined"):
            return (True, name, len(val))
    return (False, names[0] if names else "", 0)
