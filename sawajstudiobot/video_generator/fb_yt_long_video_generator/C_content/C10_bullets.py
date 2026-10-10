# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      C10_bullets.py                            ║
# ║  📁 PATH:      .../fb_yt_long_video_generator/           ║
# ║                C_content/C10_bullets.py                  ║
# ║  🎯 PURPOSE:   3-Language Key Bullet Points              ║
# ║  📖 FOLDER:    C_content                                 ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   📌 KEY BULLETS MODULE (LONG)                           ║
║   ═══════════════════════                                ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      Hadith se 3 key lessons extract karke               ║
║      3 languages mein bullets generate karna.            ║
║                                                          ║
║   📊 Languages:                                           ║
║      🟣 Hindi   (pink)                                    ║
║      🔵 Arabic  (blue)                                   ║
║      🔴 English (red)                                    ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

from A_core.A2_logger import log_file_start, log_file_end, log_step


class BulletGenerator:
    """Extract key bullet points in 3 languages."""

    def __init__(self, base, ai):
        log_file_start("C10_bullets.py", "Bullet generator")
        self.base = base
        self.ai = ai
        log_file_end("C10_bullets.py", "success", "Ready")

    def generate(self, hadith_hindi, hadith_english, hadith_arabic=""):
        """
        Generate 3 bullets in 3 languages.

        Returns:
            dict with 'hindi', 'arabic', 'english' lists
        """
        log_step("C10_bullets.py", "generate() starting", "ok")

        prompt = (
            f"Is Hadith se 3 sabse ahem spiritual/moral lessons nikaalo.\n"
            f"Har language mein alag-alag 3 short lines likho.\n\n"
            f"Format EXACT is tarah:\n"
            f"HINDI:\n"
            f"- <lesson 1>\n"
            f"- <lesson 2>\n"
            f"- <lesson 3>\n\n"
            f"ENGLISH:\n"
            f"- <lesson 1>\n"
            f"- <lesson 2>\n"
            f"- <lesson 3>\n\n"
            f"Hadith:\n{hadith_hindi}\n\n{hadith_english}"
        )

        res = self.ai.call(prompt, max_tokens=500, task="bullets")

        hindi, english = self._parse(res)
        if not hindi:
            hindi = [
                "नियत की पाकीज़गी सबसे अहम है।",
                "अमल का बदला नियत पर मुनहसिर है।",
                "अल्लाह दिलों के हाल जानता है।",
            ]
        if not english:
            english = [
                "Purity of intention is paramount.",
                "Rewards depend directly on intent.",
                "Allah knows what's in the hearts.",
            ]

        # Arabic — hadith se short snippets (fallback)
        arabic = self._extract_arabic(hadith_arabic, 3)

        log_step("C10_bullets.py", "Bullets generated", "ok")
        return {"hindi": hindi[:3], "arabic": arabic, "english": english[:3]}

    def _parse(self, text):
        """Parse AI response into hindi/english lists."""
        if not text:
            return [], []
        hindi, english = [], []
        mode = None
        for line in text.split("\n"):
            l = line.strip()
            if not l:
                continue
            if "HINDI" in l.upper():
                mode = "hi"
                continue
            if "ENGLISH" in l.upper():
                mode = "en"
                continue
            if l.startswith("-") or l.startswith("•"):
                item = l.lstrip("-•").strip()
                if mode == "hi":
                    hindi.append(item)
                elif mode == "en":
                    english.append(item)
        return hindi[:3], english[:3]

    def _extract_arabic(self, arabic_text, count):
        """Extract Arabic short phrases."""
        if not arabic_text:
            return ["إِنَّمَا الأَعْمَالُ بِالنِّيَّاتِ"] * count
        parts = arabic_text.split("،")
        return [p.strip()[:50] for p in parts[:count]]
