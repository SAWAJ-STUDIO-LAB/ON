# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      E3_mastering.py                           ║
# ║  📁 PATH:      .../fb_yt_long_video_generator/           ║
# ║                E_audio/E3_mastering.py                   ║
# ║  🎯 PURPOSE:   Audio mastering (normalize, tempo)        ║
# ║  📖 FOLDER:    E_audio                                   ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   🎚️  MASTERING MODULE (LONG)                            ║
║   ═══════════════════════                                ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      Voice audio ko master karna                         ║
║                                                          ║
║   📖 Settings:                                            ║
║      • Tempo:     0.92 (slightly slower)                 ║
║      • Loudnorm:  I=-16 LUFS                             ║
║      • Volume:    1.25x                                  ║
║                                                          ║
║   📝 Long mein tempo 0.92 (Story: 0.88) —                 ║
║      Kyunki long video mein zyada words hain             ║
║      Toh thoda faster rakhna better hai                  ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

from A_core.A2_logger import log_file_start, log_file_end, log_step


class Mastering:
    """Master voice audio (tempo + loudnorm + volume)."""

    def __init__(self, base):
        log_file_start("E3_mastering.py", "Audio mastering")
        self.base = base
        log_file_end("E3_mastering.py", "success", "Ready")

    def master_voice(self, in_file, out_file):
        """
        Apply mastering to voice (Long tuned).

        Args:
            in_file:  input mp3 path
            out_file: output mp3 path

        Returns:
            out_file path
        """
        log_step("E3_mastering.py", "master_voice()", "ok")

        self.base.run_cmd(
            f'ffmpeg -y -i {in_file} -af '
            f'"atempo=0.92,loudnorm=I=-16:TP=-1.5:LRA=11,volume=1.25" '
            f'{out_file}')

        return out_file
