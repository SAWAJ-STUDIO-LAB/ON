# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      C4_tts.py                                 ║
# ║  🎯 PURPOSE:   Multi-engine TTS — 4-level fallback       ║
# ║  ✅ FIXED:     Deepgram Aura added (no secret unused)    ║
# ╚══════════════════════════════════════════════════════════╝

import os
import subprocess
from A_core.A2_logger import log_file_start, log_file_end, log_step, log_api
from A_core.A4_utils import sanitize


class TTSManager:
    """
    Multi-engine TTS with 4-level fallback chain:

      1. ElevenLabs  (best quality, paid)
      2. Deepgram Aura (excellent, ⭐ NEW)
      3. edge-tts    (free Microsoft)
      4. gTTS        (Google Translate, last resort)
    """

    VOICE_MAP = {
        "hi": "hi-IN-MadhurNeural",
        "ar": "ar-SA-HamedNeural",
        "en": "en-US-ChristopherNeural",
    }

    DEEPGRAM_VOICE = {
        "hi": "aura-asteria-en",     # Deepgram Hindi limited → fallback EN voice
        "ar": "aura-asteria-en",
        "en": "aura-asteria-en",
    }

    def __init__(self, base):
        log_file_start("C4_tts.py", "Init TTS Manager")
        self.base = base
        log_file_end("C4_tts.py", "success")

    # ─────────────────────────────────────────────────────
    # PUBLIC
    # ─────────────────────────────────────────────────────
    def generate(self, text, outfile, rate=None):
        """Story/Short interface."""
        return self.generate_audio(text, outfile, lang="hi")

    def generate_audio(self, text, output_path, lang="hi"):
        """Long interface (alias)."""
        if not text or not text.strip():
            return False

        text = sanitize(text)
        log_step("C4_tts.py", f"generate_audio({output_path})", "ok",
                 f"{len(text)} chars, lang={lang}")

        # 1. ElevenLabs
        if os.environ.get("ELEVENLABS_API_KEY"):
            if self._try_elevenlabs(text, output_path):
                return True

        # 2. Deepgram Aura ⭐ NEW
        if os.environ.get("DEEPGRAM_API_KEY"):
            if self._try_deepgram(text, output_path, lang):
                return True

        # 3. edge-tts
        if self._try_edge_tts(text, output_path, lang):
            return True

        # 4. gTTS
        return self._try_gtts(text, output_path, lang)

    # ─────────────────────────────────────────────────────
    # 1. ElevenLabs
    # ─────────────────────────────────────────────────────
    def _try_elevenlabs(self, text, output_path):
        try:
            log_step("C4_tts.py", "Trying ElevenLabs", "info")
            r = self.base.session.post(
                "https://api.elevenlabs.io/v1/text-to-speech/"
                "pNInz6obpgDQGcFmaJgB",
                headers={
                    "Accept": "audio/mpeg",
                    "Content-Type": "application/json",
                    "xi-api-key": os.environ["ELEVENLABS_API_KEY"],
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
            log_api("C4_tts.py", "ElevenLabs", "failed",
                    f"HTTP {r.status_code}")
        except Exception as e:
            self.base.api_status["TTS"]["ElevenLabs"] = "failed"
            log_api("C4_tts.py", "ElevenLabs", "failed", str(e)[:60])
        return False

    # ─────────────────────────────────────────────────────
    # 2. Deepgram Aura ⭐ NEW
    # ─────────────────────────────────────────────────────
    def _try_deepgram(self, text, output_path, lang):
        try:
            log_step("C4_tts.py", "Trying Deepgram Aura", "info")
            voice = self.DEEPGRAM_VOICE.get(lang, "aura-asteria-en")
            key = os.environ["DEEPGRAM_API_KEY"]
            r = self.base.session.post(
                f"https://api.deepgram.com/v1/speak"
                f"?model={voice}&encoding=mp3",
                headers={
                    "Authorization": f"Token {key}",
                    "Content-Type": "application/json",
                },
                json={"text": text},
                timeout=180)
            if r.status_code == 200 and len(r.content) > 5000:
                with open(output_path, "wb") as f:
                    f.write(r.content)
                self.base.api_status["TTS"]["Deepgram"] = "success"
                log_api("C4_tts.py", "Deepgram", "success",
                        f"{len(r.content)//1024} KB")
                return True
            self.base.api_status["TTS"]["Deepgram"] = "failed"
            log_api("C4_tts.py", "Deepgram", "failed",
                    f"HTTP {r.status_code}")
        except Exception as e:
            self.base.api_status["TTS"]["Deepgram"] = "failed"
            log_api("C4_tts.py", "Deepgram", "failed", str(e)[:60])
        return False

    # ─────────────────────────────────────────────────────
    # 3. edge-tts (free)
    # ─────────────────────────────────────────────────────
    def _try_edge_tts(self, text, output_path, lang):
        try:
            voice = self.VOICE_MAP.get(lang, "hi-IN-MadhurNeural")
            log_step("C4_tts.py", f"Trying edge-tts ({voice})", "info")

            tmp = output_path + ".txt"
            with open(tmp, "w", encoding="utf-8") as f:
                f.write(text)

            subprocess.run(
                f'edge-tts --file "{tmp}" --write-media "{output_path}" '
                f'--voice {voice} --rate=-7% --pitch=-2Hz --volume=+8%',
                shell=True, check=True,
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

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

    # ─────────────────────────────────────────────────────
    # 4. gTTS (last resort)
    # ─────────────────────────────────────────────────────
    def _try_gtts(self, text, output_path, lang):
        try:
            from gtts import gTTS
            safe_lang = lang if lang in ("hi", "ar", "en") else "hi"
            tts = gTTS(text=text, lang=safe_lang, slow=False)
            tts.save(output_path)
            self.base.api_status["TTS"]["gTTS"] = "success"
            log_api("C4_tts.py", "gTTS", "success")
            return True
        except Exception as e:
            self.base.api_status["TTS"]["gTTS"] = "failed"
            log_api("C4_tts.py", "gTTS", "failed", str(e)[:60])
            return False
