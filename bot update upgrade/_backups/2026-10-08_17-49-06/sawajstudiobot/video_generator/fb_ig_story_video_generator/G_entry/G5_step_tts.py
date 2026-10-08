"""G5_step_tts.py — Sirf tts."""
from A_core.A9_log_step import log_step
from C_content.C20_tts_main import generate
from E_audio.E4_master_voice import master


def run(base, hindi):
    generate(base.session, f"हदीस शरीफ। {hindi}", "s_raw.mp3")
    master(base, "s_raw.mp3", "s_v.mp3")
    from mutagen.mp3 import MP3
    d = MP3("s_v.mp3").info.length
    log_step("G5_step_tts.py", "Voice ready", "ok", f"{d:.1f}s")
    return d
