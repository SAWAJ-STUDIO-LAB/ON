# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      C3_translator.py                          ║
# ║  📁 PATH:      .../fb_yt_long_video_generator/           ║
# ║                C_content/C3_translator.py                ║
# ║  🎯 PURPOSE:   Multilingual Translation Engine           ║
# ║  📖 FOLDER:    C_content                                 ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   🌐 TRANSLATOR MODULE                                   ║
║   ════════════════════                                   ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      DeepL / AI based high accuracy English to Hindi     ║
║      and Arabic translation.                             ║
╚══════════════════════════════════════════════════════════╝
"""

import requests
from A_core.A1_config import Config
from A_core.A2_logger import log_file_start, log_file_end, log_api, log_step
from C_content.C2_ai_provider import AIProvider


class Translator:
    """Translates text between English, Hindi, and Arabic."""

    def __init__(self, session=None):
        log_file_start("C3_translator.py", "Init Translator")
        self.cfg = Config()
        self.session = session or requests.Session()
        self.ai = AIProvider(session=self.session)
        log_file_end("C3_translator.py", "success")

    def translate_to_hindi(self, text: str) -> str:
        """Translates text to authentic Hindi."""
        if not text:
            return ""

        # 1. Try DeepL
        if self.cfg.DEEPL_API_KEY:
            try:
                url = "https://api-free.deepl.com/v2/translate"
                data = {
                    "auth_key": self.cfg.DEEPL_API_KEY,
                    "text": text,
                    "target_lang": "HI",
                }
                r = self.session.post(url, data=data, timeout=15)
                if r.status_code == 200:
                    log_api("C3_translator.py", "DeepL Hindi", "success")
                    return r.json()["translations"][0]["text"].strip()
            except Exception as e:
                log_api("C3_translator.py", "DeepL Hindi", "failed", str(e)[:50])

        # 2. AI Fallback
        log_step("C3_translator.py", "Using AI for Hindi Translation", "info")
        prompt = f"Translate the following English Islamic text into clear, respectful, natural Hindi in Devanagari script:\n\n{text}"
        res = self.ai.generate(prompt, "You are a professional translator fluent in Hindi and Islamic terminology.")
        return res if res else text
      
