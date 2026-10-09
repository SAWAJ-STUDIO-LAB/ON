"""A31_cleanup.py — Sirf cleanup."""
import os
import shutil
from A_core.A9_log_step import log_step


def cleanup(files, folder=None):
    log_step("A31_cleanup.py", "Cleanup", "ok")
    for f in files:
        if os.path.exists(f):
            os.remove(f)
    if folder:
        shutil.rmtree(folder, ignore_errors=True)
    log_step("A31_cleanup.py", "Done", "ok")
