# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      E1_voice_ducking.py                       ║
# ║  📁 PATH:      .../fb_ig_story_video_generator/          ║
# ║                E_audio/E1_voice_ducking.py               ║
# ║  🎯 PURPOSE:   Mix voice + music with ducking (STORY)    ║
# ║  📖 FOLDER:    E_audio                                   ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   🎚️  VOICE DUCKING MODULE (STORY)                       ║
║   ═══════════════════════                                ║
║                                                          ║
║   📖 Settings:                                            ║
║      • Voice: 100% | Music: 20%                          ║
║      • Fade in: 2s | Fade out: 3s                        ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

from A_core.A2_logger import log_file_start, log_file_end, log_step
from A_core.A5_base_pipeline import BasePipeline
from typing import Optional


class VoiceDucking:
    """Mix voice over music with volume ducking (Story version)."""

    def __init__(self, base: BasePipeline):
        log_file_start("E1_voice_ducking.py", "Voice + music mix")
        self.base = base
        log_file_end("E1_voice_ducking.py", "success", "Ready")

    def mix(self, voice_file: str, music_file: str, out_file: str, voice_dur: float,
            music_vol: float = 0.20) -> str:
        """
        Mix voice over music with fade in/out.

        Args:
            voice_file (str): Path to the voice file.
            music_file (str): Path to the music file.
            out_file (str): Path to the output file.
            voice_dur (float): Duration of the voice file in seconds.
            music_vol (float, optional): Volume of the music. Defaults to 0.20.

        Returns:
            str: Path to the output file.
        """
        log_step("E1_voice_ducking.py", "mix() starting", "ok")

        fade = max(voice_dur - 3.0, 1.0)

        self.base.run_cmd(
            f'ffmpeg -y -i {voice_file} -i {music_file} '
            f'-filter_complex '
            f'"[1:a]volume={music_vol},afade=t=in:st=0:d=2,'
            f'afade=t=out:st={fade:.2f}:d=3[bg];'
            f'[0:a][bg]amix=inputs=2:duration=first:dropout_transition=2[aout]" '
            f'-map "[aout]" -c:a libmp3lame -b:a 192k {out_file}')

        log_step("E1_voice_ducking.py", "Mixed", "ok")
        return out_file
