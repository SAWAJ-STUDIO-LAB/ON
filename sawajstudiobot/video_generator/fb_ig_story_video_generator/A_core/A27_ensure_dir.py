"""A27_ensure_dir.py — Sirf ensure_dir."""
import os


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)
    return path
