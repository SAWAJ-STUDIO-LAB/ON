# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      C3_translator.py                          ║
# ║  📁 PATH:      .../fb_yt_long_video_generator/           ║
# ║                C_content/C3_translator.py                ║
# ║  🎯 PURPOSE:   Multilingual Translation Engine           ║
# ╚══════════════════════════════════════════════════════════╝

import os
import requests
from A_core.A1_config import Config
from A_core.A2_logger import log_file_start, log_file_end, log_api, log_step
from C_content.C2_ai_provider import AIProvider


class Translator:
    """Translates text between English, Hindi, and Arabic."""

    def __init__(self, base=None, ai=None):
        log_file_start("C3_translator.py", "Init Translator")
        self.base = base
        self.cfg = Config()
        self.session = (base.session if base else requests.Session())
        self.ai = ai or AIProvider(base)
        log_file_end("C3_translator.py", "success")

    # ═══════════════════════════════════════════════════════
    # ✅ PUBLIC to_hindi() — pipeline ise use karta hai
    # ═══════════════════════════════════════════════════════
    def to_hindi(self, english):
        return self.translate_to_hindi(english)

    # ═══════════════════════════════════════════════════════
    # PUBLIC translate_to_hindi() — original method
    # ═══════════════════════════════════════════════════════
    def translate_to_hindi(self, text):
        """Translates text to authentic Hindi."""
        if not text:
            return ""

        # 1. Try DeepL
        key = os.environ.get("DEEPL_API_KEY")
        if key:
            try:
                r = self.session.post(
                    "https://api-free.deepl.com/v2/translate",
                    headers={"Authorization": f"DeepL-Auth-Key {key}"},
                    data={"text": text, "target_lang": "HI"},
                    timeout=60)
                if r.status_code == 200:
                    log_api("C3_translator.py", "DeepL Hindi", "success")
                    return r.json()["translations"][0]["text"].strip()
            except Exception as e:
                log_api("C3_translator.py", "DeepL Hindi", "failed", str(e)[:50])

        # 2. AI Fallback
        log_step("C3_translator.py", "Using AI for Hindi Translation", "info")
        prompt = (
            f"Is English Islamic text ka soft, accurate, COMPLETE Hindi tarjuma likho. "
            f"Sirf tarjuma. Kuch mat chhodo.\n\n{text}"
        )
        res = self.ai.call(prompt, max_tokens=1500, task="hindi")
        return res if res else text
