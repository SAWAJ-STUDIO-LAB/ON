"""
📁 File Helper
"""
import os
import shutil


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)
    return path


def delete_file(path):
    if os.path.exists(path):
        os.remove(path)


def delete_folder(path):
    if os.path.exists(path):
        shutil.rmtree(path, ignore_errors=True)


def file_size_mb(path):
    if not os.path.exists(path):
        return 0
    return os.path.getsize(path) / 1024 / 1024


def file_exists(path):
    return os.path.exists(path)
