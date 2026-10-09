# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      E1_voice_ducking.py                       ║
# ║  📁 PATH:      .../fb_ig_yt_short_video_generator/       ║
# ║                E_audio/E1_voice_ducking.py               ║
# ║  🎯 PURPOSE:   Mix voice + music with ducking            ║
# ║  📖 FOLDER:    E_audio                                   ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   🎚️  VOICE DUCKING MODULE (SHORT)                       ║
║   ═══════════════════════                                ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      Voice + music ko mix karna (music duck)             ║
║                                                          ║
║   📖 How it works:                                       ║
║      • Voice: 100% volume                                ║
║      • Music: 20% volume (auto-lowered)                  ║
║      • Music fade-in:  2s                                ║
║      • Music fade-out: 3s                                ║
║                                                          ║
║   🎯 Output:                                              ║
║      Single MP3 with voice + music mixed                 ║
║                                                          ║
║   📝 Note:                                                ║
║      Same as Story — same code                           ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

from A_core.A2_logger import log_file_start, log_file_end, log_step


class VoiceDucking:
    """Mix voice over music with volume ducking."""

    def __init__(self, base):
        log_file_start("E1_voice_ducking.py", "Voice + music mix")
        self.base = base
        log_file_end("E1_voice_ducking.py", "success", "Ready")

    def mix(self, voice_file, music_file, out_file, voice_dur,
            music_vol=0.20):
        """
        Mix voice over music with fade in/out.

        Args:
            voice_file: voice mp3 path
            music_file: music mp3 path
            out_file:   output mp3 path
            voice_dur:  voice duration (seconds)
            music_vol:  music volume (0.20 = 20%)

        Returns:
            out_file path
        """
        log_step("E1_voice_ducking.py", "mix() starting", "ok")

        # ═══════════ Fade out point ═══════════
        fade = max(voice_dur - 3.0, 1.0)

        # ═══════════ FFmpeg mix command ═══════════
        self.base.run_cmd(
            f'ffmpeg -y -i {voice_file} -i {music_file} '
            f'-filter_complex '
            f'"[1:a]volume={music_vol},afade=t=in:st=0:d=2,'
            f'afade=t=out:st={fade:.2f}:d=3[bg];'
            f'[0:a][bg]amix=inputs=2:duration=first:dropout_transition=2[aout]" '
            f'-map "[aout]" -c:a libmp3lame -b:a 192k {out_file}')

        log_step("E1_voice_ducking.py", "Mixed", "ok")
        return out_file
