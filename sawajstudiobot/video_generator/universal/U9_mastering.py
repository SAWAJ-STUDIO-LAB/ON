"""
U9_mastering.py — Universal Voice Mastering
============================================
Parametrized via tempo/volume. Falls back to simple filter if loudnorm fails.
"""

import os
import subprocess
from universal.U1_logger import log_file_start, log_file_end, log_step


class Mastering:

    TEMPO = 0.88      # override per generator
    VOLUME = 1.35

    def __init__(self, base, tempo=None, volume=None):
        log_file_start("E3_mastering.py", "Audio mastering")
        self.base = base
        if tempo is not None:
            self.TEMPO = tempo
        if volume is not None:
            self.VOLUME = volume
        log_file_end("E3_mastering.py", "success", "Ready")

    def master_voice(self, in_file, out_file):
        log_step("E3_mastering.py", "master_voice()", "ok")

        primary = (
            f'ffmpeg -y -i "{in_file}" -af '
            f'"atempo={self.TEMPO},'
            f'loudnorm=I=-16:TP=-1.5:LRA=11,volume={self.VOLUME}" '
            f'"{out_file}"'
        )
        try:
            subprocess.run(primary, shell=True, check=True,
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL)
            if os.path.exists(out_file) and os.path.getsize(out_file) > 1000:
                return out_file
        except Exception as e:
            log_step("E3_mastering.py", "Primary filter failed",
                     "warn", str(e)[:60])

        fallback = (
            f'ffmpeg -y -i "{in_file}" -af '
            f'"atempo={self.TEMPO},volume={self.VOLUME}" '
            f'"{out_file}"'
        )
        try:
            subprocess.run(fallback, shell=True, check=True,
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL)
            return out_file
        except Exception as e:
            log_step("E3_mastering.py", "Both filters failed", "fail",
                     str(e)[:80])
            import shutil
            shutil.copy(in_file, out_file)
            return out_file
