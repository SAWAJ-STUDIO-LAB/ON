# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      E1_voice_ducking.py                       ║
# ║  📁 PATH:      .../fb_yt_long_video_generator/           ║
# ║                E_audio/E1_voice_ducking.py               ║
# ║  🎯 PURPOSE:   Mix voice + music with ducking (LONG)     ║
# ║  📖 FOLDER:    E_audio                                   ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   🎚️  VOICE DUCKING MODULE (LONG)                        ║
║   ═══════════════════════                                ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      Voice + music ko mix karna (music auto-duck)        ║
║                                                          ║
║   📖 How it works:                                       ║
║      • Voice: 100% volume                                ║
║      • Music: 18% volume (softer for long)               ║
║      • Music fade-in:  3s                                ║
║      • Music fade-out: 8s                                ║
║                                                          ║
║   🎯 Output:                                              ║
║      Single MP3 with voice + music mixed                 ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

from A_core.A2_logger import log_file_start, log_file_end, log_step


class VoiceDucking:
    """Mix voice over music with volume ducking (Long version)."""

    def __init__(self, base):
        log_file_start("E1_voice_ducking.py", "Voice + music mix")
        self.base = base
        log_file_end("E1_voice_ducking.py", "success", "Ready")

    def mix(self, voice_file, music_file, out_file, voice_dur,
            music_vol=0.18):
        """
        Mix voice over music with fade in/out.

        Args:
            voice_file: voice mp3 path
            music_file: music mp3 path
            out_file:   output mp3 path
            voice_dur:  voice duration (seconds)
            music_vol:  music volume (0.18 = 18%)

        Returns:
            out_file path
        """
        log_step("E1_voice_ducking.py", "mix() starting", "ok")

        fade = max(voice_dur - 8.0, 1.0)

        self.base.run_cmd(
            f'ffmpeg -y -i {voice_file} -i {music_file} '
            f'-filter_complex '
            f'"[1:a]volume={music_vol},afade=t=in:st=0:d=3,'
            f'afade=t=out:st={fade:.2f}:d=8[bg];'
            f'[0:a][bg]amix=inputs=2:duration=first:dropout_transition=2[aout]" '
            f'-map "[aout]" -c:a libmp3lame -b:a 192k {out_file}')

        log_step("E1_voice_ducking.py", "Mixed", "ok")
        return out_file
