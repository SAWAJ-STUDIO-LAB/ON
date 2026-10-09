# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      C4_tts.py                                 ║
# ║  📁 PATH:      .../fb_yt_long_video_generator/           ║
# ║                C_content/C4_tts.py                       ║
# ║  🎯 PURPOSE:   Multi-engine Voiceover TTS Generator      ║
# ╚══════════════════════════════════════════════════════════╝

import os
import asyncio
import requests
from A_core.A1_config import Config
from A_core.A2_logger import log_file_start, log_file_end, log_api, log_step


class TTSManager:
    """Generates audio files using multiple TTS engines."""

    def __init__(self, base=None):
        log_file_start("C4_tts.py", "Init TTS Manager")
        self.base = base
        self.cfg = Config()
        self.session = (base.session if base else requests.Session())
        log_file_end("C4_tts.py", "success")

    def generate_audio(self, text, output_path, lang="hi"):
        """Attempts ElevenLabs → Edge-TTS → gTTS."""
        if not text or not text.strip():
            return False

        # 1. ElevenLabs
        if os.environ.get("ELEVENLABS_API_KEY"):
            if self._try_elevenlabs(text, output_path):
                return True

        # 2. Edge-TTS
        if self._try_edge_tts(text, output_path, lang):
            return True

        # 3. gTTS
        return self._try_gtts(text, output_path, lang)

    def _try_elevenlabs(self, text, output_path):
        try:
            voice_id = "pNInz6obpgDQGcFmaJgB"
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
            headers = {
                "xi-api-key": os.environ["ELEVENLABS_API_KEY"],
                "Content-Type": "application/json",
            }
            body = {
                "text": text,
                "model_id": "eleven_multilingual_v2",
                "voice_settings": {"stability": 0.42, "similarity_boost": 0.82},
            }
            r = self.session.post(url, json=body, headers=headers, timeout=90)
            if r.status_code == 200 and len(r.content) > 5000:
                with open(output_path, "wb") as f:
                    f.write(r.content)
                log_api("C4_tts.py", "ElevenLabs TTS", "success")
                return True
        except Exception as e:
            log_api("C4_tts.py", "ElevenLabs TTS", "failed", str(e)[:50])
        return False

    def _try_edge_tts(self, text, output_path, lang):
        try:
            import edge_tts
            voice_map = {
                "hi": "hi-IN-MadhurNeural",
                "ar": "ar-SA-HamedNeural",
                "en": "en-US-ChristopherNeural",
            }
            voice = voice_map.get(lang, "hi-IN-MadhurNeural")

            async def _run():
                c = edge_tts.Communicate(text, voice)
                await c.save(output_path)

            asyncio.run(_run())
            if os.path.exists(output_path) and os.path.getsize(output_path) > 1000:
                log_api("C4_tts.py", "Edge-TTS", "success")
                return True
        except Exception as e:
            log_api("C4_tts.py", "Edge-TTS", "failed", str(e)[:50])
        return False

    def _try_gtts(self, text, output_path, lang):
        try:
            from gtts import gTTS
            gTTS(text=text, lang=lang, slow=False).save(output_path)
            log_api("C4_tts.py", "gTTS Fallback", "success")
            return True
        except Exception as e:
            log_api("C4_tts.py", "gTTS Fallback", "failed", str(e)[:50])
        return False


# ✅ Alias — pipeline `TTS` naam se import karta hai
TTS = TTSManager
