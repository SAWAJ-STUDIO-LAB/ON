# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      E3_mastering.py                           ║
# ║  🎯 PURPOSE:   Voice mastering (Long tuning)             ║
# ║  ✅ FIXED:     Fallback filters (loudnorm-safe)          ║
# ╚══════════════════════════════════════════════════════════╝

import os
import subprocess
from A_core.A2_logger import log_file_start, log_file_end, log_step


class Mastering:
    """Master voice audio — Long (tempo 0.92, slightly less loud)."""

    def __init__(self, base):
        log_file_start("E3_mastering.py", "Audio mastering (Long)")
        self.base = base
        log_file_end("E3_mastering.py", "success", "Ready")

    def master_voice(self, in_file, out_file):
        log_step("E3_mastering.py", "master_voice()", "ok")

        primary = (
            f'ffmpeg -y -i "{in_file}" -af '
            f'"atempo=0.92,loudnorm=I=-16:TP=-1.5:LRA=11,volume=1.25" '
            f'"{out_file}"'
        )
        try:
            subprocess.run(primary, shell=True, check=True,
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL)
            if os.path.exists(out_file) and os.path.getsize(out_file) > 1000:
                return out_file
        except Exception as e:
            log_step("E3_mastering.py", "Primary failed",
                     "warn", str(e)[:60])

        fallback = (
            f'ffmpeg -y -i "{in_file}" -af '
            f'"atempo=0.92,volume=1.25" '
            f'"{out_file}"'
        )
        try:
            subprocess.run(fallback, shell=True, check=True,
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL)
            return out_file
        except Exception as e:
            log_step("E3_mastering.py", "Both failed", "fail",
                     str(e)[:80])
            import shutil
            shutil.copy(in_file, out_file)
            return out_file
