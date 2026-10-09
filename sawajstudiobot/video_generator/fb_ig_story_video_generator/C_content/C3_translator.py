# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      C3_translator.py                          ║
# ║  📁 PATH:      .../fb_ig_story_video_generator/          ║
# ║                C_content/C3_translator.py                ║
# ║  🎯 PURPOSE:   English → Hindi translation               ║
# ║  📖 FOLDER:    C_content                                 ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   🌐 TRANSLATOR MODULE                                   ║
║   ═══════════════════════                                ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      English hadith ko Hindi mein translate karna        ║
║                                                          ║
║   📖 Flow:                                               ║
║      1. Try DeepL API (best quality)                     ║
║      2. Fallback: AI providers                           ║
║      3. Last resort: hardcoded text                      ║
║                                                          ║
║   ⚠️  No Truncation:                                      ║
║      Poora translation — kuch nahi chhutega              ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

import os
from A_core.A2_logger import log_file_start, log_file_end, log_step, log_api


# ═══════════════════════════════════════════════════════════
# 🌐 TRANSLATOR CLASS
# ═══════════════════════════════════════════════════════════

class Translator:
    """Translate English hadith to Hindi."""

    # ─────────────────────────────────────────────────────
    # ① INIT
    # ─────────────────────────────────────────────────────
    def __init__(self, base, ai):
        log_file_start("C3_translator.py", "English → Hindi")
        self.base = base
        self.ai = ai
        log_file_end("C3_translator.py", "success", "Ready")

    # ─────────────────────────────────────────────────────
    # ② DEEPL — try DeepL API first
    # ─────────────────────────────────────────────────────
    def deepl(self, text):
        """
        Try DeepL API first.

        Args:
            text: English text

        Returns:
            Hindi text or None
        """
        key = os.environ.get("DEEPL_API_KEY")
        if not key:
            self.base.api_status["Translation"]["DeepL"] = "hold (no key)"
            log_api("C3_translator.py", "DeepL", "skipped", "no key")
            return None

        try:
            r = self.base.session.post(
                "https://api-free.deepl.com/v2/translate",
                headers={"Authorization": f"DeepL-Auth-Key {key}"},
                data={"text": text, "target_lang": "HI"},
                timeout=25)
            if r.status_code == 200:
                out = r.json()["translations"][0]["text"]
                self.base.api_status["Translation"]["DeepL"] = "success"
                log_api("C3_translator.py", "DeepL", "success", f"{len(out)} chars")
                return out
            self.base.api_status["Translation"]["DeepL"] = "failed"
            log_api("C3_translator.py", "DeepL", "failed", f"HTTP {r.status_code}")
        except Exception as e:
            self.base.api_status["Translation"]["DeepL"] = "failed"
            log_api("C3_translator.py", "DeepL", "failed", str(e)[:60])
        return None

    # ─────────────────────────────────────────────────────
    # ③ TO HINDI — get Hindi with fallback
    # ─────────────────────────────────────────────────────
    def to_hindi(self, english):
        """
        Get Hindi translation with fallback.

        Args:
            english: English text

        Returns:
            Hindi text
        """
        log_step("C3_translator.py", "to_hindi()", "ok")

        # ───────── Try DeepL ─────────
        hindi = self.deepl(english)
        if hindi:
            return hindi

        # ───────── Fallback: AI ─────────
        log_step("C3_translator.py", "DeepL failed → AI fallback", "warn")
        result = self.ai.call(
            f"Is English Hadith ka soft accurate Hindi tarjuma likho. "
            f"Sirf tarjuma. Koi extra baat mat likho. "
            f"Hadith ki har line ka tarjuma karo, kuch mat chhodo.\n\n{english}",
            task="hindi")
        if result:
            log_step("C3_translator.py", "AI translation done", "ok")
            return result

        # ───────── Last resort ─────────
        log_step("C3_translator.py", "Using hardcoded fallback", "warn")
        return "अमल का दारोमदार नीयतों पर है।"
