# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      C1_hadith.py                              ║
# ║  📁 PATH:      .../fb_yt_long_video_generator/           ║
# ║                C_content/C1_hadith.py                    ║
# ║  🎯 PURPOSE:   Fetch & parse long Hadith content         ║
# ║  📖 FOLDER:    C_content                                 ║
# ╚══════════════════════════════════════════════════════════╝

import os
import random
import requests
from A_core.A1_config import Config
from A_core.A2_logger import log_file_start, log_file_end, log_step, log_api
from A_core.A4_utils import sanitize


# ═══════════════════════════════════════════════════════════
# 📖 HARDCODED FALLBACK
# ═══════════════════════════════════════════════════════════

FALLBACK = {
    "collection": "Sahih al-Bukhari",
    "book": "Sahih al-Bukhari",
    "number": "1",
    "hadith_no": "1",
    "narrator": "Umar ibn Al-Khattab (R.A)",
    "chapter": "Book of Revelation",
    "english": (
        "Actions are judged by intentions, and every person will get "
        "what they intended. Whoever migrated for the sake of Allah and "
        "His Messenger, his migration is for Allah and His Messenger. "
        "And whoever migrated for worldly gain or to marry a woman, "
        "his migration is for that which he migrated for."
    ),
    "arabic": "إِنَّمَا الأَعْمَالُ بِالنِّيَّاتِ وَإِنَّمَا لِكُلِّ امْرِئٍ مَا نَوَى",
}


# ═══════════════════════════════════════════════════════════
# 📖 HADITH FETCHER CLASS
# ═══════════════════════════════════════════════════════════

class HadithFetcher:
    """Fetches detailed Hadith for Long videos."""

    BOOKS = [
        {"eng": "eng-bukhari", "ara": "ara-bukhari",
         "name": "Sahih al-Bukhari", "max": 7000},
        {"eng": "eng-muslim", "ara": "ara-muslim",
         "name": "Sahih Muslim", "max": 5000},
        {"eng": "eng-abudawud", "ara": "ara-abudawud",
         "name": "Sunan Abu Dawud", "max": 4000},
        {"eng": "eng-tirmidhi", "ara": "ara-tirmidhi",
         "name": "Jami at-Tirmidhi", "max": 3500},
    ]

    def __init__(self, base=None):
        log_file_start("C1_hadith.py", "Initialize Hadith fetcher")
        self.base = base
        self.cfg = Config()
        self.session = (base.session if base else requests.Session())
        log_file_end("C1_hadith.py", "success")

    # ─────────────────────────────────────────────────────
    # COUNT WORDS
    # ─────────────────────────────────────────────────────
    def _count_words(self, text):
        return len(text.split()) if text else 0

    # ─────────────────────────────────────────────────────
    # FETCH ONE — try to fetch one hadith
    # ─────────────────────────────────────────────────────
    def _fetch_one(self, base_url, book, num):
        try:
            url = f"{base_url}/editions/{book['eng']}/{num}.json"
            r = self.session.get(url, timeout=15)
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
                ar = self.session.get(
                    url.replace(book["eng"], book["ara"]), timeout=10)
                if ar.status_code == 200:
                    ad = ar.json().get("hadiths", [])
                    if ad:
                        ara = sanitize(ad[0].get("text", ""))
            except Exception:
                pass

            return {
                "collection": book["name"],
                "book": book["name"],
                "number": str(hs[0].get("hadithnumber") or num),
                "hadith_no": str(hs[0].get("hadithnumber") or num),
                "english": eng,
                "arabic": ara,
                "narrator": sanitize(hs[0].get("narrator", "")) or "Narrator",
                "chapter": sanitize(hs[0].get("chapter", "")) or "Chapter",
                "word_count": self._count_words(eng),
            }
        except Exception:
            return None

    # ═══════════════════════════════════════════════════════
    # ✅ PUBLIC fetch() — LONG pipeline ise call karta hai
    # ═══════════════════════════════════════════════════════
    def fetch(self):
        """Main fetch — Long video ke liye 400+ words dhoondhta hai."""
        return self.fetch_daily_hadith()

    def fetch_daily_hadith(self) -> dict:
        """Fetches detailed Hadith (Long video target: 400-1800 words)."""
        log_step("C1_hadith.py", "fetch() starting", "ok")

        # Try custom API first
        url = self.cfg.HADITH_API_URL
        if url:
            try:
                r = self.session.get(url, timeout=15)
                if r.status_code == 200:
                    data = r.json()
                    log_api("C1_hadith.py", "Hadith API", "success")
                    return {
                        "arabic": sanitize(data.get("arabic", "")),
                        "english": sanitize(data.get("english", "")),
                        "book": data.get("book", "Sahih Bukhari"),
                        "collection": data.get("book", "Sahih Bukhari"),
                        "hadith_no": str(data.get("hadith_no", "1")),
                        "number": str(data.get("hadith_no", "1")),
                        "narrator": sanitize(data.get("narrator", "Narrator")),
                        "chapter": sanitize(data.get("chapter", "Chapter")),
                    }
            except Exception as e:
                log_api("C1_hadith.py", "Hadith API", "failed", str(e)[:60])

        # API bases
        bases = []
        if os.environ.get("HADITH_API_URL"):
            bases.append(os.environ["HADITH_API_URL"].rstrip("/"))
        bases += [
            "https://cdn.jsdelivr.net/gh/fawazahmed0/hadith-api@1",
            "https://raw.githubusercontent.com/fawazahmed0/hadith-api/1",
        ]

        # ═══════════ PHASE 1: Ideal 400-1800 words ═══════════
        log_step("C1_hadith.py", "Phase 1: ideal 400-1800 words", "info")
        for _ in range(30):
            book = random.choice(self.BOOKS)
            num = random.randint(1, book["max"])
            for base in bases:
                h = self._fetch_one(base, book, num)
                if h and 400 <= h["word_count"] <= 1800:
                    log_api("C1_hadith.py", "Found ideal", "success",
                            f"{h['word_count']} words")
                    return {k: v for k, v in h.items() if k != "word_count"}

        # ═══════════ PHASE 2: Fallback 200-400 words ═══════════
        log_step("C1_hadith.py", "Phase 2: fallback 200-400 words", "warn")
        for _ in range(25):
            book = random.choice(self.BOOKS)
            num = random.randint(1, book["max"])
            for base in bases:
                h = self._fetch_one(base, book, num)
                if h and 200 <= h["word_count"] <= 400:
                    log_api("C1_hadith.py", "Found fallback", "fallback",
                            f"{h['word_count']} words")
                    return {k: v for k, v in h.items() if k != "word_count"}

        # ═══════════ PHASE 3: Any hadith ═══════════
        log_step("C1_hadith.py", "Phase 3: any hadith", "warn")
        for _ in range(15):
            book = random.choice(self.BOOKS)
            num = random.randint(1, book["max"])
            for base in bases:
                h = self._fetch_one(base, book, num)
                if h:
                    log_api("C1_hadith.py", "Found any", "fallback",
                            f"{h['word_count']} words")
                    return {k: v for k, v in h.items() if k != "word_count"}

        # ═══════════ PHASE 4: Hardcoded ═══════════
        log_api("C1_hadith.py", "Hardcoded-Fallback", "fallback")
        return FALLBACK
