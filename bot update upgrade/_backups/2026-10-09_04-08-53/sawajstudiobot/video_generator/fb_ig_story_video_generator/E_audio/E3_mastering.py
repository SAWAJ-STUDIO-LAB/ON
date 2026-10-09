# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      E3_mastering.py                           ║
# ║  📁 PATH:      .../fb_ig_yt_short_video_generator/       ║
# ║                E_audio/E3_mastering.py                   ║
# ║  🎯 PURPOSE:   Audio mastering (normalize, tempo)        ║
# ║  📖 FOLDER:    E_audio                                   ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   🎚️  MASTERING MODULE (SHORT)                           ║
║   ═══════════════════════                                ║
║                                                          ║
║   📖 Settings:                                            ║
║      • Tempo: 0.88 | Loudnorm: -16 LUFS | Volume: 1.35x  ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

from A_core.A2_logger import log_file_start, log_file_end, log_step


class Mastering:
    """Master voice audio (Short: slower tempo 0.88)."""

    def __init__(self, base):
        log_file_start("E3_mastering.py", "Audio mastering")
        self.base = base
        log_file_end("E3_mastering.py", "success", "Ready")

    def master_voice(self, in_file, out_file):
        """Apply tempo + loudnorm + volume."""
        log_step("E3_mastering.py", "master_voice()", "ok")

        self.base.run_cmd(
            f'ffmpeg -y -i {in_file} -af '
            f'"atempo=0.88,loudnorm=I=-16:TP=-1.5:LRA=11,volume=1.35" '
            f'{out_file}')

        return out_file
