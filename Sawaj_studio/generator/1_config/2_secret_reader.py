"""
🔑 Secret Reader
"""
import os


def read_secret(*names, default=""):
    for name in names:
        val = os.environ.get(name, "").strip()
        if val and val.lower() not in ("none", "null", "undefined"):
            return val
    return default


def has_secret(*names):
    return bool(read_secret(*names))


def mask_secret(value):
    if not value:
        return "(empty)"
    if len(value) <= 8:
        return "***"
    return value[:4] + "***" + value[-4:]
