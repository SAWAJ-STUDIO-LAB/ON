"""D16_frames_cleanup.py — Sirf cleanup."""
import os
import shutil


def cleanup(folder="s_frames"):
    if os.path.exists(folder):
        shutil.rmtree(folder, ignore_errors=True)
