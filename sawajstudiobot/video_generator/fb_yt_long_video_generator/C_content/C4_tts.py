# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      C4_tts.py                                 ║
# ║  📁 PATH:      .../fb_yt_long_video_generator/           ║
# ║                C_content/C4_tts.py                       ║
# ║  ✅ FIXED:     base interface + edge-tts primary         ║
# ╚══════════════════════════════════════════════════════════╝

import os
import subprocess
from A_core.A2_logger import log_file_start, log_file_end, log_step, log_api
from A_core.A4_utils import sanitize


class TTSManager:
    """Multi-engine TTS for Long videos."""

    VOICE_MAP = {
        "hi": "hi-IN-MadhurNeural",
        "ar": "ar-SA-HamedNeural",
        "en": "en-US-ChristopherNeural",
    }

    def __init__(self, base):
        log_file_start("C4_tts.py", "Init TTS Manager")
        self.base = base
        log_file_end("C4_tts.py", "success")

    def generate_audio(self, text, output_path, lang="hi"):
        """ElevenLabs → edge-tts → gTTS fallback."""
        if not text or not text.strip():
            return False

        text = sanitize(text)

        # 1. ElevenLabs (if key available)
        if os.environ.get("ELEVENLABS_API_KEY"):
            if self._try_elevenlabs(text, output_path):
                return True

        # 2. edge-tts (best free option)
        if self._try_edge_tts(text, output_path, lang):
            return True

        # 3. gTTS last resort
        return self._try_gtts(text, output_path, lang)

    def _try_elevenlabs(self, text, output_path):
        try:
            el = os.environ["ELEVENLABS_API_KEY"]
            r = self.base.session.post(
                "https://api.elevenlabs.io/v1/text-to-speech/pNInz6obpgDQGcFmaJgB",
                headers={
                    "Accept": "audio/mpeg",
                    "Content-Type": "application/json",
                    "xi-api-key": el,
                },
                json={
                    "text": text,
                    "model_id": "eleven_multilingual_v2",
                    "voice_settings": {
                        "stability": 0.42,
                        "similarity_boost": 0.82,
                        "style": 0.35,
                        "use_speaker_boost": True,
                    },
                },
                timeout=180)
            if r.status_code == 200 and len(r.content) > 5000:
                with open(output_path, "wb") as f:
                    f.write(r.content)
                self.base.api_status["TTS"]["ElevenLabs"] = "success"
                log_api("C4_tts.py", "ElevenLabs", "success",
                        f"{len(r.content)//1024} KB")
                return True
            self.base.api_status["TTS"]["ElevenLabs"] = "failed"
            log_api("C4_tts.py", "ElevenLabs", "failed", f"HTTP {r.status_code}")
        except Exception as e:
            self.base.api_status["TTS"]["ElevenLabs"] = "failed"
            log_api("C4_tts.py", "ElevenLabs", "failed", str(e)[:60])
        return False

    def _try_edge_tts(self, text, output_path, lang):
        try:
            voice = self.VOICE_MAP.get(lang, "hi-IN-MadhurNeural")
            tmp = output_path + ".txt"
            with open(tmp, "w", encoding="utf-8") as f:
                f.write(text)
            subprocess.run(
                f'edge-tts --file "{tmp}" --write-media "{output_path}" '
                f'--voice {voice} --rate=-7% --pitch=-2Hz --volume=+8%',
                shell=True, check=True)
            if os.path.exists(tmp):
                os.remove(tmp)
            if os.path.exists(output_path) and os.path.getsize(output_path) > 1000:
                self.base.api_status["TTS"]["edge-tts"] = "success"
                log_api("C4_tts.py", "edge-tts", "success",
                        f"{os.path.getsize(output_path)//1024} KB")
                return True
        except Exception as e:
            self.base.api_status["TTS"]["edge-tts"] = "failed"
            log_api("C4_tts.py", "edge-tts", "failed", str(e)[:60])
        return False

    def _try_gtts(self, text, output_path, lang):
        try:
            from gtts import gTTS
            tts = gTTS(text=text, lang=lang if lang in ("hi","ar","en") else "hi", slow=False)
            tts.save(output_path)
            self.base.api_status["TTS"]["gTTS"] = "success"
            log_api("C4_tts.py", "gTTS", "success")
            return True
        except Exception as e:
            self.base.api_status["TTS"]["gTTS"] = "failed"
            log_api("C4_tts.py", "gTTS", "failed", str(e)[:60])
            return False
