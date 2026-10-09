"""C17_tts_elevenlabs.py — Sirf ElevenLabs."""
import os
from A_core.A10_log_api import log_api
from C_content.C16_tts_constants import MIN_AUDIO_SIZE, ELEVEN_TIMEOUT


def generate(session, text, outfile):
    key = os.environ.get("ELEVENLABS_API_KEY")
    if not key:
        return False
    try:
        r = session.post(
            "https://api.elevenlabs.io/v1/text-to-speech/pNInz6obpgDQGcFmaJgB",
            headers={"Accept": "audio/mpeg",
                     "Content-Type": "application/json",
                     "xi-api-key": key},
            json={"text": text, "model_id": "eleven_multilingual_v2",
                  "voice_settings": {"stability": 0.42, "similarity_boost": 0.82,
                                     "style": 0.35, "use_speaker_boost": True}},
            timeout=ELEVEN_TIMEOUT)
        if r.status_code == 200 and len(r.content) > MIN_AUDIO_SIZE:
            with open(outfile, "wb") as f:
                f.write(r.content)
            log_api("C17_tts_elevenlabs.py", "ElevenLabs", "success",
                    f"{len(r.content)//1024} KB")
            return True
        log_api("C17_tts_elevenlabs.py", "ElevenLabs", "failed",
                f"HTTP {r.status_code}")
    except Exception as e:
        log_api("C17_tts_elevenlabs.py", "ElevenLabs", "failed", str(e)[:60])
    return False
