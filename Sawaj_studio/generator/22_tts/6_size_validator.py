"""
📏 Size Validator
"""
import os


def is_valid_audio(path, min_size=1000):
    if not os.path.exists(path):
        return False
    return os.path.getsize(path) >= min_size


def get_size_kb(path):
    if not os.path.exists(path):
        return 0
    return os.path.getsize(path) // 1024
