# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      C1_hadith.py                              ║
# ║  📁 PATH:      .../fb_yt_long_video_generator/           ║
# ║                C_content/C1_hadith.py                    ║
# ║  🎯 PURPOSE:   Fetch & parse long Hadith content         ║
# ║  📖 FOLDER:    C_content                                 ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   📖 HADITH FETCHER MODULE (LONG)                        ║
║   ═══════════════════════════════                        ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      API ya AI se detailed (400-1800 words) Hadith       ║
║      fetch karna along with reference & narrator.        ║
╚══════════════════════════════════════════════════════════╝
"""

import random
import requests
from A_core.A1_config import Config
from A_core.A2_logger import log_file_start, log_file_end, log_step, log_api
from A_core.A4_utils import sanitize


class HadithFetcher:
    """Fetches long Hadith text with Arabic, English, and reference data."""

    BOOKS = ["bukhari", "muslim", "tirmidhi", "abudawud", "nasai", "ibnmajah"]

    def __init__(self, session=None):
        log_file_start("C1_hadith.py", "Initialize Hadith fetcher")
        self.cfg = Config()
        self.session = session or requests.Session()
        log_file_end("C1_hadith.py", "success")

    def fetch_daily_hadith(self) -> dict:
        """Fetches detailed Hadith from API with fallback structure."""
        url = self.cfg.HADITH_API_URL
        if url:
            try:
                r = self.session.get(url, timeout=15)
                if r.status_code == 200:
                    data = r.json()
                    log_api("C1_hadith.py", "Hadith API", "success", "Fetched successfully")
                    return {
                        "arabic": sanitize(data.get("arabic", "")),
                        "english": sanitize(data.get("english", "")),
                        "book": data.get("book", "Sahih Bukhari"),
                        "hadith_no": str(data.get("hadith_no", "1")),
                        "narrator": sanitize(data.get("narrator", "Abu Hurairah (R.A)")),
                        "chapter": sanitize(data.get("chapter", "Faith & Practice")),
                    }
            except Exception as e:
                log_api("C1_hadith.py", "Hadith API", "failed", str(e)[:60])

        # Default fallback long Hadith structure
        log_step("C1_hadith.py", "Using fallback long Hadith dataset", "info")
        return self._get_fallback_hadith()

    def _get_fallback_hadith(self) -> dict:
        return {
            "arabic": "إِنَّمَا الأَعْمَالُ بِالنِّيَّاتِ، وَإِنَّمَا لِكُلِّ امْرِئٍ مَا نَوَى",
            "english": (
                "Actions are judged by intentions, and every person will get what they intended. "
                "Whoever migrated for the sake of Allah and His Messenger, his migration is for "
                "Allah and His Messenger. And whoever migrated for worldly gain or to marry a woman, "
                "his migration is for that which he migrated for."
            ),
            "book": "Sahih Bukhari",
            "hadith_no": "1",
            "narrator": "Omar ibn Al-Khattab (R.A)",
            "chapter": "Book of Revelation",
        }
      
