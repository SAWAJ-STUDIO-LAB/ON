# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      C1_hadith.py                              ║
# ║  📁 PATH:      .../fb_yt_long_video_generator/           ║
# ║                C_content/C1_hadith.py                    ║
# ║  ✅ FIXED:     HadithFetcher(base) + fetch() method      ║
# ╚══════════════════════════════════════════════════════════╝

import os
from A_core.A2_logger import log_file_start, log_file_end, log_step, log_api
from A_core.A4_utils import sanitize


FALLBACK = {
    "collection": "Sahih Bukhari",
    "number": "1",
    "book": "Sahih Bukhari",
    "hadith_no": "1",
    "english": (
        "Actions are judged by intentions, and every person will get what they "
        "intended. Whoever migrated for the sake of Allah and His Messenger, his "
        "migration is for Allah and His Messenger. And whoever migrated for worldly "
        "gain or to marry a woman, his migration is for that which he migrated for."
    ),
    "arabic": "إِنَّمَا الأَعْمَالُ بِالنِّيَّاتِ، وَإِنَّمَا لِكُلِّ امْرِئٍ مَا نَوَى",
    "narrator": "Omar ibn Al-Khattab (R.A)",
    "chapter": "Book of Revelation",
}


class HadithFetcher:
    """Fetches long Hadith (400-1800 words) with Arabic, English, reference."""

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

    LONG_MIN = 400
    LONG_MAX = 1800

    def __init__(self, base):
        log_file_start("C1_hadith.py", "Initialize Hadith fetcher")
        self.base = base
        log_file_end("C1_hadith.py", "success")

    # ─────────────────────────────────────────────────────
    # PUBLIC — fetch() entry (pipeline uses this)
    # ─────────────────────────────────────────────────────
    def fetch(self):
        """Fetch one long hadith. Returns dict with collection/number/english/arabic."""
        import random

        log_step("C1_hadith.py", "fetch() starting", "ok")

        # ───────── Try custom API ─────────
        api_url = os.environ.get("HADITH_API_URL")
        if api_url:
            try:
                r = self.base.session.get(api_url, timeout=20)
                if r.status_code == 200:
                    data = r.json()
                    eng = sanitize(data.get("english", ""))
                    if len(eng.split()) >= 100:
                        log_api("C1_hadith.py", "Custom API", "success",
                                f"{len(eng.split())} words")
                        return {
                            "collection": data.get("book", "Sahih Bukhari"),
                            "number": str(data.get("hadith_no", "1")),
                            "book": data.get("book", "Sahih Bukhari"),
                            "hadith_no": str(data.get("hadith_no", "1")),
                            "english": eng,
                            "arabic": sanitize(data.get("arabic", "")),
                            "narrator": sanitize(data.get("narrator", "")),
                            "chapter": sanitize(data.get("chapter", "")),
                        }
            except Exception as e:
                log_api("C1_hadith.py", "Custom API", "failed", str(e)[:60])

        # ───────── Try fawazahmed0 CDN ─────────
        bases = [
            "https://cdn.jsdelivr.net/gh/fawazahmed0/hadith-api@1",
            "https://raw.githubusercontent.com/fawazahmed0/hadith-api/1",
        ]

        for phase_min, phase_max, label in [
            (self.LONG_MIN, self.LONG_MAX, "long"),
            (150, 400, "medium"),
            (100, 150, "short"),
            (0, 99999, "any"),
        ]:
            log_step("C1_hadith.py",
                     f"Phase {label}: {phase_min}-{phase_max} words", "info")
            for _ in range(20):
                book = random.choice(self.BOOKS)
                num = random.randint(1, book["max"])
                for base_url in bases:
                    h = self._fetch_one(base_url, book, num)
                    if not h:
                        continue
                    wc = len(h["english"].split())
                    if phase_min <= wc <= phase_max:
                        log_api("C1_hadith.py", f"Found ({label})", "success",
                                f"{wc} words")
                        return {
                            "collection": h["collection"],
                            "number": h["number"],
                            "book": h["collection"],
                            "hadith_no": h["number"],
                            "english": h["english"],
                            "arabic": h["arabic"],
                            "narrator": h.get("narrator", ""),
                            "chapter": h.get("chapter", ""),
                        }

        log_api("C1_hadith.py", "Hardcoded fallback", "fallback")
        return FALLBACK

    # ─────────────────────────────────────────────────────
    # INTERNAL — fetch one hadith from API
    # ─────────────────────────────────────────────────────
    def _fetch_one(self, base_url, book, num):
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
            }
        except Exception:
            return None

    # ─────────────────────────────────────────────────────
    # BACK-COMPAT alias (pipeline may also call this)
    # ─────────────────────────────────────────────────────
    def fetch_daily_hadith(self):
        return self.fetch()
