"""C6_ai_get_key.py — Sirf key lena."""
import os


def get_key(*names):
    for name in names:
        val = os.environ.get(name, "").strip()
        if val:
            return val
    return ""
