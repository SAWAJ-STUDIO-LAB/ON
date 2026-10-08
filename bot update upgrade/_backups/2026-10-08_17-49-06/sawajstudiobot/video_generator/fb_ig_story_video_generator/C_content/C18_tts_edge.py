"""C18_tts_edge.py — Sirf Edge-TTS."""
import os
import asyncio
from A_core.A10_log_api import log_api
from C_content.C16_tts_constants import (
    DEFAULT_VOICE, DEFAULT_PITCH, DEFAULT_VOLUME,
    MIN_AUDIO_SIZE, EDGE_TIMEOUT)


def generate(text, outfile, rate="-7%"):
    try:
        import edge_tts
    except ImportError:
        log_api("C18_tts_edge.py", "edge-tts", "failed", "not installed")
        return False

    async def _run():
        c = edge_tts.Communicate(text, DEFAULT_VOICE, rate=rate,
                                 pitch=DEFAULT_PITCH, volume=DEFAULT_VOLUME)
        await c.save(outfile)

    try:
        asyncio.run(asyncio.wait_for(_run(), timeout=EDGE_TIMEOUT))
    except asyncio.TimeoutError:
        log_api("C18_tts_edge.py", "edge-tts", "failed", "timeout")
        return False
    except Exception as e:
        log_api("C18_tts_edge.py", "edge-tts", "failed", str(e)[:60])
        return False

    if not os.path.exists(outfile) or os.path.getsize(outfile) < MIN_AUDIO_SIZE:
        return False
    log_api("C18_tts_edge.py", "edge-tts", "success",
            f"{os.path.getsize(outfile)//1024} KB")
    return True
