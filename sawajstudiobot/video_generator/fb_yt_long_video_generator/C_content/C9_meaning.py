# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      C9_meaning.py                             ║
# ║  📁 PATH:      .../fb_yt_long_video_generator/           ║
# ║                C_content/C9_meaning.py                   ║
# ║  🎯 PURPOSE:   ⭐ Extended Hindi Tashreeh (250-500 words)║
# ║  📖 FOLDER:    C_content                                 ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   📖 EXTENDED HINDI MEANING (TASHREEH) MODULE            ║
║   ═══════════════════════════════════════════            ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      Long video ke liye detailed Tashreeh                ║
║      (250-500 Hindi words) generate karna.               ║
║                                                          ║
║   📊 Output Sections:                                    ║
║      1. Simple Hindi Tarjuma                             ║
║      2. Detailed Tashreeh (explanation)                  ║
║      3. Life Lessons (daily routine)                     ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

from A_core.A2_logger import log_file_start, log_file_end, log_step
from A_core.A4_utils import sanitize


class Meaning:
    """Generate extended Hindi Tashreeh using AI (Long version)."""

    def __init__(self, base, ai):
        log_file_start("C9_meaning.py", "Extended Hindi meaning")
        self.base = base
        self.ai = ai
        log_file_end("C9_meaning.py", "success", "Ready")

    def generate(self, hadith_hindi, narrator="", book=""):
        """
        Generate detailed Hindi Tashreeh.

        Args:
            hadith_hindi: Hadith text in Hindi
            narrator:     Narrator name
            book:         Book name

        Returns:
            dict with hindi_translation + full_tashreeh
        """
        log_step("C9_meaning.py", "generate() starting", "ok",
                 f"hadith {len(hadith_hindi)} chars")

        if not hadith_hindi:
            return self._fallback()

        prompt = (
            f"Is Hadith ka mufassal (detailed) Hindi Tashreeh likho.\n\n"
            f"Format:\n"
            f"1. Simple Hindi Tarjuma (2-3 lines)\n"
            f"2. Detailed Tashreeh — 250 se 500 shabdon mein "
            f"(spiritual, practical, aur dilchasp)\n"
            f"3. Life Lessons — 3-5 practical sikh (aaj ke zamaane ke liye)\n\n"
            f"Rules:\n"
            f"- Sirf Hindi (Devanagari)\n"
            f"- Simple aur aam feham zubaan\n"
            f"- Soft, respectful tone\n"
            f"- Islamic terminology ka asaan matlab do\n\n"
            f"{'Narrator: ' + narrator if narrator else ''}\n"
            f"{'Book: ' + book if book else ''}\n\n"
            f"Hadith:\n{hadith_hindi}"
        )

        result = self.ai.call(prompt, max_tokens=1500, task="tashreeh")

        if result:
            cleaned = sanitize(result).replace("```", "").strip()
            if len(cleaned) > 100:
                log_step("C9_meaning.py", "Tashreeh generated", "ok",
                         f"{len(cleaned)} chars")
                self.base.api_status["AI"]["tashreeh"] = "success"
                return {
                    "hindi_translation": cleaned[:250] + "...",
                    "full_tashreeh": cleaned,
                }

        log_step("C9_meaning.py", "AI failed, using fallback", "warn")
        return self._fallback()

    def _fallback(self):
        """Fallback Tashreeh."""
        fb = (
            "इस हदीस का मफ़हूम यह है कि इंसान का हर अमल उसकी नियत पर निर्भर करता है। "
            "अल्लाह तआला सिर्फ़ ज़ाहिरी अमल नहीं देखता, बल्कि दिल का इख़लास और नियत देखता है। "
            "इसलिए हर नेक काम शुरू करने से पहले अपनी नियत सिर्फ़ अल्लाह की रज़ा के लिए "
            "ख़ालिस करें। जब नियत साफ़ होती है तो छोटा सा अमल भी अल्लाह के यहाँ बड़ा बन जाता है, "
            "और जब नियत ख़राब हो तो बड़ा अमल भी बेकार हो जाता है।\n\n"
            "Life Lessons:\n"
            "1. हर काम की शुरुआत नियत साफ़ करके करें।\n"
            "2. दिखावे से बचें, इख़लास पैदा करें।\n"
            "3. छोटे अमल को भी नज़रअंदाज़ न करें।\n"
            "4. दिल की सफ़ाई सबसे ज़रूरी है।"
        )
        return {
            "hindi_translation": fb[:250] + "...",
            "full_tashreeh": fb,
        }
