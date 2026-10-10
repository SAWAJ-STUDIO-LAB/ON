# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      C4_tts.py                                 ║
# ║  📁 PATH:      .../fb_yt_long_video_generator/           ║
# ║                C_content/C4_tts.py                       ║
# ║  🎯 PURPOSE:   Multi-engine Voiceover TTS Generator      ║
# ║  📖 FOLDER:    C_content                                 ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   🎙️ TTS VOICE GENERATOR MODULE                          ║
║   ═════════════════════════════                          ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      ElevenLabs → Edge-TTS → gTTS multi-engine audio     ║
║      narration generator for Hindi, Arabic & English.    ║
╚══════════════════════════════════════════════════════════╝
"""

import os
import asyncio
import requests
from A_core.A1_config import Config
from A_core.A2_logger import log_file_start, log_file_end, log_api, log_step


class TTSManager:
    """Generates audio files using multiple TTS engines."""

    def __init__(self, session=None):
        log_file_start("C4_tts.py", "Init TTS Manager")
        self.cfg = Config()
        self.session = session or requests.Session()
        log_file_end("C4_tts.py", "success")

    def generate_audio(self, text: str, output_path: str, lang: str = "hi") -> bool:
        """Attempts ElevenLabs first, then Edge-TTS, then gTTS."""
        if not text or not text.strip():
            return False

        # 1. Try ElevenLabs
        if self.cfg.ELEVENLABS_API_KEY:
            if self._try_elevenlabs(text, output_path):
                return True

        # 2. Try Edge-TTS
        if self._try_edge_tts(text, output_path, lang):
            return True

        # 3. Fallback gTTS
        return self._try_gtts(text, output_path, lang)

    def _try_elevenlabs(self, text: str, output_path: str) -> bool:
        try:
            voice_id = "21m00Tcm4TlvDq8ikWAM"  # Default clear male voice
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
            headers = {
                "xi-api-key": self.cfg.ELEVENLABS_API_KEY,
                "Content-Type": "application/json",
            }
            body = {
                "text": text,
                "voice_settings": {"stability": 0.75, "similarity_boost": 0.85},
            }
            r = self.session.post(url, json=body, headers=headers, timeout=30)
            if r.status_code == 200:
                with open(output_path, "wb") as f:
                    f.write(r.content)
                log_api("C4_tts.py", "ElevenLabs TTS", "success")
                return True
        except Exception as e:
            log_api("C4_tts.py", "ElevenLabs TTS", "failed", str(e)[:50])
        return False

    def _try_edge_tts(self, text: str, output_path: str, lang: str) -> bool:
        try:
            import edge_tts

            voice_map = {
                "hi": "hi-IN-MadhurNeural",
                "ar": "ar-SA-HamedNeural",
                "en": "en-US-ChristopherNeural",
            }
            voice = voice_map.get(lang, "hi-IN-MadhurNeural")

            async def _run():
                communicate = edge_tts.Communicate(text, voice)
                await communicate.save(output_path)

            asyncio.run(_run())
            if os.path.exists(output_path) and os.path.getsize(output_path) > 1000:
                log_api("C4_tts.py", "Edge-TTS", "success")
                return True
        except Exception as e:
            log_api("C4_tts.py", "Edge-TTS", "failed", str(e)[:50])
        return False

    def _try_gtts(self, text: str, output_path: str, lang: str) -> bool:
        try:
            from gtts import gTTS
            tts = gTTS(text=text, lang=lang, slow=False)
            tts.save(output_path)
            log_api("C4_tts.py", "gTTS Fallback", "success")
            return True
        except Exception as e:
            log_api("C4_tts.py", "gTTS Fallback", "failed", str(e)[:50])
        return False
      
