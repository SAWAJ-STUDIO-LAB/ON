"""
🧹 Cleanup
"""
import os
import shutil


def cleanup_files(files):
    for f in files:
        if os.path.exists(f):
            try:
                os.remove(f)
            except Exception:
                pass


def cleanup_folder(folder):
    if os.path.exists(folder):
        shutil.rmtree(folder, ignore_errors=True)
