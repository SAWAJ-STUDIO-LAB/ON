# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      C4_tts.py                                 ║
# ║  📁 PATH:      .../fb_ig_story_video_generator/          ║
# ║                C_content/C4_tts.py                       ║
# ║  🎯 PURPOSE:   Text-to-Speech generation                 ║
# ║  📖 FOLDER:    C_content                                 ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   🎙️  TTS MODULE                                         ║
║   ═══════════════                                        ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      Hindi text ko voice mein convert karna              ║
║                                                          ║
║   📖 Flow:                                               ║
║      1. Try ElevenLabs (best quality)                    ║
║      2. Fallback: edge-tts (free, reliable)              ║
║                                                          ║
║   🎙️  Voice Settings:                                     ║
║      • Voice:  hi-IN-MadhurNeural                        ║
║      • Rate:   -7% (slightly slower)                     ║
║      • Pitch:  -2Hz                                      ║
║      • Volume: +8%                                       ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

import os
from typing import Optional
from A_core.A2_logger import log_file_start, log_file_end, log_step, log_api
from A_core.A4_utils import sanitize


# ═══════════════════════════════════════════════════════════
# 🎙️  TTS CLASS
# ═══════════════════════════════════════════════════════════

class TTS:
    """
    Generate voice from text.

    Try ElevenLabs first, fallback to edge-tts.
    """

    DEFAULT_RATE: str = "-7%"

    # ─────────────────────────────────────────────────────
    # ① INIT
    # ─────────────────────────────────────────────────────
    def __init__(self, base: object) -> None:
        """
        Initialize TTS with base pipeline.

        Args:
            base: Base pipeline object
        """
        log_file_start("C4_tts.py", "Text-to-Speech generation")
        self.base = base
        log_file_end("C4_tts.py", "success", "Ready")

    # ─────────────────────────────────────────────────────
    # ② GENERATE — main generate function
    # ─────────────────────────────────────────────────────
    def generate(self, text: str, outfile: str, rate: Optional[str] = None) -> bool:
        """
        Generate voice from text.

        Args:
            text:    Text to speak
            outfile: Output MP3 path
            rate:    Speech rate (default -7%)

        Returns:
            True if successful, False otherwise
        """
        if rate is None:
            rate = self.DEFAULT_RATE

        log_step("C4_tts.py", f"generate({outfile})", "ok",
                 f"{len(text)} chars, rate={rate}")
        text = sanitize(text)

        # ═══════════ Try ElevenLabs ═══════════
        el_api_key = os.environ.get("ELEVENLABS_API_KEY")
        if el_api_key:
            try:
                log_step("C4_tts.py", "Trying ElevenLabs", "info")
                response = self.base.session.post(
                    "https://api.elevenlabs.io/v1/text-to-speech/pNInz6obpgDQGcFmaJgB",
                    headers={
                        "Accept": "audio/mpeg",
                        "Content-Type": "application/json",
                        "xi-api-key": el_api_key,
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
                    timeout=60)  # Increased timeout to 60 seconds

                if response.status_code == 200 and len(response.content) > 5000:
                    with open(outfile, "wb") as f:
                        f.write(response.content)
                    self.base.api_status["TTS"]["ElevenLabs"] = "success"
                    log_api("C4_tts.py", "ElevenLabs", "success",
                            f"{len(response.content)//1024} KB")
                    return True
                self.base.api_status["TTS"]["ElevenLabs"] = "failed"
                log_api("C4_tts.py", "ElevenLabs", "failed", f"HTTP {response.status_code}")
            except Exception as e:
                self.base.api_status["TTS"]["ElevenLabs"] = "failed"
                log_api("C4_tts.py", "ElevenLabs", "failed", str(e)[:60])

        # ═══════════ Fallback: edge-tts ═══════════
        try:
            log_step("C4_tts.py", f"Trying edge-tts (rate={rate})", "info")
            tmp_file = outfile + ".txt"
            with open(tmp_file, "w", encoding="utf-8") as f:
                f.write(text)
            
            # Run edge-tts command with proper quoting and error handling
            command = (
                f'edge-tts --file "{tmp_file}" --write-media "{outfile}" '
                f'--voice hi-IN-MadhurNeural --rate={rate} '
                f'--pitch=-2Hz --volume=+8%'
            )
            self.base.run_cmd(command)
            
            if os.path.exists(tmp_file):
                os.remove(tmp_file)
            self.base.api_status["TTS"]["edge-tts"] = "success"
            log_api("C4_tts.py", "edge-tts", "success",
                    f"{os.path.getsize(outfile)//1024} KB")
            return True
        except Exception as e:
            self.base.api_status["TTS"]["edge-tts"] = "failed"
            log_api("C4_tts.py", "edge-tts", "failed", str(e)[:60])
            return False
