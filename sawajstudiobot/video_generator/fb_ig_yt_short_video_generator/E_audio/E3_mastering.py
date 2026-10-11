# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      E3_mastering.py                           ║
# ║  🎯 PURPOSE:   Voice mastering — Story + Short tuning    ║
# ║  ✅ FIXED:     Fallback filters (loudnorm-safe)          ║
# ╚══════════════════════════════════════════════════════════╝

import os
import subprocess
from A_core.A2_logger import log_file_start, log_file_end, log_step


class Mastering:
    """Master voice audio — Story/Short (tempo 0.88, louder)."""

    def __init__(self, base):
        log_file_start("E3_mastering.py", "Audio mastering")
        self.base = base
        log_file_end("E3_mastering.py", "success", "Ready")

    def master_voice(self, in_file, out_file):
        """
        Apply mastering. Tries best filter first, then simple fallback.
        """
        log_step("E3_mastering.py", "master_voice()", "ok")

        # Primary: full chain
        primary = (
            f'ffmpeg -y -i "{in_file}" -af '
            f'"atempo=0.88,loudnorm=I=-16:TP=-1.5:LRA=11,volume=1.35" '
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

        # Fallback: simple tempo + volume (no loudnorm)
        fallback = (
            f'ffmpeg -y -i "{in_file}" -af '
            f'"atempo=0.88,volume=1.35" '
            f'"{out_file}"'
        )
        try:
            subprocess.run(fallback, shell=True, check=True,
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL)
            log_step("E3_mastering.py", "Fallback filter OK", "warn")
            return out_file
        except Exception as e:
            log_step("E3_mastering.py", "Both filters failed",
                     "fail", str(e)[:80])
            # Last resort: just copy
            import shutil
            shutil.copy(in_file, out_file)
            return out_file
