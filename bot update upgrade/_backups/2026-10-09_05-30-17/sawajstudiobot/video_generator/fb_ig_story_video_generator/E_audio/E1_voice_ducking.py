# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      E1_voice_ducking.py                       ║
# ║  📁 PATH:      .../fb_ig_yt_short_video_generator/       ║
# ║                E_audio/E1_voice_ducking.py               ║
# ║  🎯 PURPOSE:   Mix voice + music with ducking (SHORT)    ║
# ║  📖 FOLDER:    E_audio                                   ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   🎚️  VOICE DUCKING MODULE (SHORT)                       ║
║   ═══════════════════════                                ║
║                                                          ║
║   📖 Settings:                                            ║
║      • Voice: 100% | Music: 20%                          ║
║      • Fade in: 2s | Fade out: 3s                        ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

from A_core.A2_logger import log_file_start, log_file_end, log_step


class VoiceDucking:
    """Mix voice over music with volume ducking (Short version)."""

    def __init__(self, base):
        log_file_start("E1_voice_ducking.py", "Voice + music mix")
        self.base = base
        log_file_end("E1_voice_ducking.py", "success", "Ready")

    def mix(self, voice_file, music_file, out_file, voice_dur,
            music_vol=0.20):
        """Mix voice over music with fade in/out."""
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
