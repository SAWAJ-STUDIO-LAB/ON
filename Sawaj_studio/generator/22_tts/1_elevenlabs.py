"""
🎙️ ElevenLabs
"""
import os
import requests


def generate_elevenlabs(text, outfile):
    key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    if not key:
        return False
    try:
        url = "https://api.elevenlabs.io/v1/text-to-speech/pNInz6obpgDQGcFmaJgB"
        r = requests.post(url,
                          headers={"Accept": "audio/mpeg",
                                   "Content-Type": "application/json",
                                   "xi-api-key": key},
                          json={"text": text,
                                "model_id": "eleven_multilingual_v2",
                                "voice_settings": {
                                    "stability": 0.42,
                                    "similarity_boost": 0.82}},
                          timeout=90)
        if r.status_code == 200 and len(r.content) > 5000:
            with open(outfile, "wb") as f:
                f.write(r.content)
            return True
    except Exception:
        pass
    return False
