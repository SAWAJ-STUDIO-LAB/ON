"""C20_tts_main.py — Sirf TTS main."""
import os
from A_core.A9_log_step import log_step
from A_core.A11_log_error import log_error
from C_content.C17_tts_elevenlabs import generate as el_gen
from C_content.C18_tts_edge import generate as edge_gen
from C_content.C19_tts_gtts import generate as gtts_gen


def generate(session, text, outfile, rate=None):
    if rate is None:
        rate = "-7%"
    if not text or len(text) < 2:
        log_error("C20_tts_main.py", "Text empty")
        return False

    log_step("C20_tts_main.py", f"generate({os.path.basename(outfile)})", "ok")
    if os.environ.get("ELEVENLABS_API_KEY") and el_gen(session, text, outfile):
        return True
    if edge_gen(text, outfile, rate):
        return True
    if gtts_gen(text, outfile):
        return True
    log_error("C20_tts_main.py", "All TTS failed")
    return False
