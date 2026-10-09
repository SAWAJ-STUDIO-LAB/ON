# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      C1_hadith.py                              ║
# ║  📁 PATH:      .../fb_ig_yt_short_video_generator/       ║
# ║                C_content/C1_hadith.py                    ║
# ║  🎯 PURPOSE:   Fetch Hadith (150-400 words for Short)    ║
# ║  📖 FOLDER:    C_content                                 ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   📖 HADITH FETCH MODULE (SHORT)                         ║
║   ═══════════════════════════                            ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      Hadith fetch karna (Short ke liye badi)             ║
║                                                          ║
║   📊 Word Filter (3 Phases):                             ║
║      • Phase 1: 150-400 words (ideal for 1-3 min)        ║
║      • Phase 2: 100-150 words (chhoti fallback)          ║
║      • Phase 3: 400-700 words (badi fallback)            ║
║      • Phase 4: Any hadith (last resort)                 ║
║                                                          ║
║   📚 Books:                                              ║
║      • Sahih al-Bukhari                                  ║
║      • Sahih Muslim                                      ║
║      • Sunan Abu Dawud                                   ║
║      • Jami at-Tirmidhi                                  ║
║                                                          ║
║   ⚠️  No Truncation:                                      ║
║      Hadith poori dikhegi, kabhi nahi kategi             ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

import os
import random
from A_core.A2_logger import log_file_start, log_file_end, log_step, log_api
from A_core.A4_utils import sanitize


# ═══════════════════════════════════════════════════════════
# ① HARDCODED FALLBACK
# ═══════════════════════════════════════════════════════════

FALLBACK = {
    "collection": "Sahih al-Bukhari",
    "number": "1",
    "english": "The reward of deeds depends upon the intentions and every person will get the reward according to what he has intended.",
    "arabic": "إِنَّمَا الأَعْمَالُ بِالنِّيَّاتِ وَإِنَّمَا لِكُلِّ امْرِئٍ مَا نَوَى",
}


# ═══════════════════════════════════════════════════════════
# 📖 HADITH CLASS
# ═══════════════════════════════════════════════════════════

class Hadith:
    """
    Fetch hadith with word count filter (SHORT).

    Target: 150-400 words (English) = ~90-170 seconds voice.
    NO TRUNCATION — full hadith always.
    """

    # ═══════════ Word Count Ranges ═══════════
    IDEAL_MIN = 150
    IDEAL_MAX = 400
    SHORT_MIN = 100
    SHORT_MAX = 150
    LONG_MIN = 400
    LONG_MAX = 700

    def __init__(self, base):
        log_file_start("C1_hadith.py", "Fetch Hadith (150-400 words)")
        self.base = base
        log_file_end("C1_hadith.py", "success", "Ready")

    def _count_words(self, text):
        """Count words in text."""
        return len(text.split()) if text else 0

    def _fetch_one(self, base_url, book, num):
        """Try to fetch one hadith."""
        try:
            url = f"{base_url}/editions/{book['eng']}/{num}.json"
            r = self.base.session.get(url, timeout=15)
            if r.status_code != 200:
                return None

            data = r.json()
            hs = data.get("hadiths", [])
            if not hs:
                return None

            eng = sanitize(hs[0].get("text", ""))
            if len(eng) < 30:
                return None

            # Try Arabic
            ara = ""
            try:
                ar = self.base.session.get(
                    url.replace(book["eng"], book["ara"]), timeout=10)
                if ar.status_code == 200:
                    ad = ar.json().get("hadiths", [])
                    if ad:
                        ara = sanitize(ad[0].get("text", ""))
            except Exception:
                pass

            return {
                "collection": book["name"],
                "number": str(hs[0].get("hadithnumber") or num),
                "english": eng,
                "arabic": ara,
                "word_count": self._count_words(eng),
            }
        except Exception:
            return None

    def fetch(self):
        """Fetch hadith with 4-phase filter."""
        log_step("C1_hadith.py", "fetch() starting", "ok")

        books = [
            {"eng": "eng-bukhari", "ara": "ara-bukhari",
             "name": "Sahih al-Bukhari", "max": 7000},
            {"eng": "eng-muslim", "ara": "ara-muslim",
             "name": "Sahih Muslim", "max": 5000},
            {"eng": "eng-abudawud", "ara": "ara-abudawud",
             "name": "Sunan Abu Dawud", "max": 4000},
            {"eng": "eng-tirmidhi", "ara": "ara-tirmidhi",
             "name": "Jami at-Tirmidhi", "max": 3500},
        ]

        bases = []
        if os.environ.get("HADITH_API_URL"):
            bases.append(os.environ["HADITH_API_URL"].rstrip("/"))
        bases += [
            "https://cdn.jsdelivr.net/gh/fawazahmed0/hadith-api@1",
            "https://raw.githubusercontent.com/fawazahmed0/hadith-api/1",
        ]

        # ═══════════ PHASE 1: Ideal 150-400 words ═══════════
        log_step("C1_hadith.py",
                 f"Phase 1: ideal {self.IDEAL_MIN}-{self.IDEAL_MAX} words", "info")
        for _ in range(25):
            book = random.choice(books)
            num = random.randint(1, book["max"])
            for base in bases:
                h = self._fetch_one(base, book, num)
                if h and self.IDEAL_MIN <= h["word_count"] <= self.IDEAL_MAX:
                    log_api("C1_hadith.py", "Found", "success",
                            f"{h['word_count']} words, #{h['number']}")
                    self.base.api_status["Hadith"]["filtered"] = "success"
                    return {k: v for k, v in h.items() if k != "word_count"}

        # ═══════════ PHASE 2: Short 100-150 words ═══════════
        log_step("C1_hadith.py",
                 f"Phase 2: short {self.SHORT_MIN}-{self.SHORT_MAX} words", "warn")
        for _ in range(25):
            book = random.choice(books)
            num = random.randint(1, book["max"])
            for base in bases:
                h = self._fetch_one(base, book, num)
                if h and self.SHORT_MIN <= h["word_count"] <= self.SHORT_MAX:
                    log_api("C1_hadith.py", "Found (short)", "fallback",
                            f"{h['word_count']} words")
                    self.base.api_status["Hadith"]["fallback"] = "success"
                    return {k: v for k, v in h.items() if k != "word_count"}

        # ═══════════ PHASE 3: Long 400-700 words ═══════════
        log_step("C1_hadith.py",
                 f"Phase 3: long {self.LONG_MIN}-{self.LONG_MAX} words", "warn")
        for _ in range(25):
            book = random.choice(books)
            num = random.randint(1, book["max"])
            for base in bases:
                h = self._fetch_one(base, book, num)
                if h and self.LONG_MIN <= h["word_count"] <= self.LONG_MAX:
                    log_api("C1_hadith.py", "Found (long)", "fallback",
                            f"{h['word_count']} words")
                    return {k: v for k, v in h.items() if k != "word_count"}

        # ═══════════ PHASE 4: Any ═══════════
        log_step("C1_hadith.py", "Phase 4: any hadith", "warn")
        for _ in range(10):
            book = random.choice(books)
            num = random.randint(1, book["max"])
            for base in bases:
                h = self._fetch_one(base, book, num)
                if h:
                    log_api("C1_hadith.py", "Found (any)", "fallback",
                            f"{h['word_count']} words")
                    return {k: v for k, v in h.items() if k != "word_count"}

        log_api("C1_hadith.py", "Hardcoded-Fallback", "fallback")
        return FALLBACK
