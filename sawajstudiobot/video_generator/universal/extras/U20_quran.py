"""
U20_quran.py — Quran Ayah Fetcher
==================================
Fetch a random Quran ayah for hadith pairing.

Fallback: 5 hardcoded ayahs if API fails or URL missing.
"""

import os
import random
from universal.U1_logger import log_file_start, log_file_end, log_step, log_api


class QuranAyah:
    """Fetch random Quran ayah via QURAN_API_URL."""

    FALLBACK_AYAHS = [
        {
            "arabic": "إِنَّ اللَّهَ مَعَ الصَّابِرِينَ",
            "english": "Indeed, Allah is with the patient.",
            "reference": "Al-Baqarah 2:153",
        },
        {
            "arabic": "فَاذْكُرُونِي أَذْكُرْكُمْ",
            "english": "So remember Me; I will remember you.",
            "reference": "Al-Baqarah 2:152",
        },
        {
            "arabic": "وَمَن يَتَوَكَّلْ عَلَى اللَّهِ فَهُوَ حَسْبُهُ",
            "english": "And whoever relies upon Allah — He is sufficient for him.",
            "reference": "At-Talaq 65:3",
        },
        {
            "arabic": "إِنَّ مَعَ الْعُسْرِ يُسْرًا",
            "english": "Indeed, with hardship comes ease.",
            "reference": "Ash-Sharh 94:6",
        },
        {
            "arabic": "وَقُل رَّبِّ زِدْنِي عِلْمًا",
            "english": "And say: My Lord, increase me in knowledge.",
            "reference": "Ta-Ha 20:114",
        },
    ]

    def __init__(self, base=None):
        log_file_start("U20_quran.py", "Quran ayah fetcher")
        self.base = base
        log_file_end("U20_quran.py", "success", "Ready")

    def fetch_random(self):
        """Fetch random ayah or fallback."""
        api = os.environ.get("QURAN_API_URL")
        if not api or self.base is None:
            log_api("U20_quran.py", "Quran", "skipped", "no URL or session")
            return random.choice(self.FALLBACK_AYAHS)

        try:
            # Try alquran.cloud style endpoint
            num = random.randint(1, 6236)
            url = (api.rstrip("/") +
                   f"/ayah/{num}/editions/quran-uthmani,en.sahih")
            log_step("U20_quran.py", f"GET {url[:70]}", "info")
            r = self.base.session.get(url, timeout=15)

            if r.status_code == 200:
                data = r.json().get("data", [])
                if isinstance(data, list) and len(data) >= 2:
                    ar = data[0].get("text", "")
                    en = data[1].get("text", "")
                    surah = data[0].get("surah", {})
                    ref = (f"{surah.get('englishName', '')} "
                           f"{surah.get('number', '')}:"
                           f"{data[0].get('numberInSurah', '')}")
                    log_api("U20_quran.py", "QuranAPI", "success", ref)
                    return {"arabic": ar, "english": en, "reference": ref}

            log_api("U20_quran.py", "QuranAPI", "failed",
                    f"HTTP {r.status_code}")
        except Exception as e:
            log_api("U20_quran.py", "QuranAPI", "failed", str(e)[:80])

        return random.choice(self.FALLBACK_AYAHS)

    def fetch_by_reference(self, surah, ayah):
        """Fetch specific ayah. Returns dict or None."""
        api = os.environ.get("QURAN_API_URL")
        if not api or self.base is None:
            return None
        try:
            url = (api.rstrip("/") +
                   f"/ayah/{surah}:{ayah}/editions/quran-uthmani,en.sahih")
            r = self.base.session.get(url, timeout=15)
            if r.status_code == 200:
                data = r.json().get("data", [])
                if isinstance(data, list) and len(data) >= 2:
                    return {
                        "arabic": data[0].get("text", ""),
                        "english": data[1].get("text", ""),
                        "reference": f"{surah}:{ayah}",
                    }
        except Exception:
            pass
        return None
