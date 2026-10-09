"""C19_tts_gtts.py — Sirf gTTS."""
import os
from A_core.A10_log_api import log_api
from C_content.C16_tts_constants import MIN_AUDIO_SIZE


def generate(text, outfile):
    try:
        from gtts import gTTS
    except ImportError:
        log_api("C19_tts_gtts.py", "gTTS", "failed", "not installed")
        return False
    try:
        gTTS(text=text, lang="hi", slow=False).save(outfile)
        if os.path.getsize(outfile) < MIN_AUDIO_SIZE:
            return False
        log_api("C19_tts_gtts.py", "gTTS", "success")
        return True
    except Exception as e:
        log_api("C19_tts_gtts.py", "gTTS", "failed", str(e)[:60])
        return False
