"""Text-to-speech engine"""
import os
from .utils import sanitize, run_cmd

def gen_tts(text, outfile, rate="-7%", api_status=None):
    if api_status is None: api_status = {"TTS": {}}
    text = sanitize(text)
    el = os.environ.get("ELEVENLABS_API_KEY")
    if el:
        try:
            import requests
            r = requests.post(
                "https://api.elevenlabs.io/v1/text-to-speech/pNInz6obpgDQGcFmaJgB",
                headers={"Accept": "audio/mpeg", "Content-Type": "application/json", "xi-api-key": el},
                json={"text": text, "model_id": "eleven_multilingual_v2",
                      "voice_settings": {"stability": 0.42, "similarity_boost": 0.82,
                                         "style": 0.35, "use_speaker_boost": True}},
                timeout=60)
            if r.status_code == 200 and len(r.content) > 5000:
                open(outfile, "wb").write(r.content)
                api_status["TTS"]["ElevenLabs"] = "success"
                return True
            api_status["TTS"]["ElevenLabs"] = "failed"
        except:
            api_status["TTS"]["ElevenLabs"] = "failed"
    try:
        tmp = outfile + ".txt"
        open(tmp, "w", encoding="utf-8").write(text)
        run_cmd(f'edge-tts --file "{tmp}" --write-media "{outfile}" --voice hi-IN-MadhurNeural --rate={rate} --pitch=-2Hz --volume=+8%')
        if os.path.exists(tmp): os.remove(tmp)
        api_status["TTS"]["edge-tts"] = "success"
        return True
    except:
        api_status["TTS"]["edge-tts"] = "failed"
        return False
