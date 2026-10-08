"""C5_hadith_main.py — Sirf main fetch."""
import os
import random
from A_core.A9_log_step import log_step
from A_core.A10_log_api import log_api
from C_content.C1_hadith_fallback import FALLBACK
from C_content.C3_hadith_fetch_one import fetch_one
from C_content.C4_hadith_books import BOOKS

TARGET_MIN, TARGET_MAX = 50, 100
FALLBACK_MIN, FALLBACK_MAX = 30, 150


def fetch(session):
    bases = []
    if os.environ.get("HADITH_API_URL"):
        bases.append(os.environ["HADITH_API_URL"].rstrip("/"))
    bases += ["https://cdn.jsdelivr.net/gh/fawazahmed0/hadith-api@1",
              "https://raw.githubusercontent.com/fawazahmed0/hadith-api/1"]

    log_step("C5_hadith_main.py", f"Phase 1: {TARGET_MIN}-{TARGET_MAX}", "info")
    for _ in range(25):
        book = random.choice(BOOKS)
        num = random.randint(1, book["max"])
        for base in bases:
            h = fetch_one(session, base, book, num)
            if h and TARGET_MIN <= h["word_count"] <= TARGET_MAX:
                log_api("C5_hadith_main.py", "Found", "success", f"{h['word_count']}w")
                return {k: v for k, v in h.items() if k != "word_count"}

    log_step("C5_hadith_main.py", f"Phase 2: {FALLBACK_MIN}-{FALLBACK_MAX}", "warn")
    for _ in range(25):
        book = random.choice(BOOKS)
        num = random.randint(1, book["max"])
        for base in bases:
            h = fetch_one(session, base, book, num)
            if h and FALLBACK_MIN <= h["word_count"] <= FALLBACK_MAX:
                log_api("C5_hadith_main.py", "Fallback", "fallback", f"{h['word_count']}w")
                return {k: v for k, v in h.items() if k != "word_count"}

    log_step("C5_hadith_main.py", "Phase 3: any", "warn")
    for _ in range(10):
        book = random.choice(BOOKS)
        num = random.randint(1, book["max"])
        for base in bases:
            h = fetch_one(session, base, book, num)
            if h:
                log_api("C5_hadith_main.py", "Any", "fallback", f"{h['word_count']}w")
                return {k: v for k, v in h.items() if k != "word_count"}

    log_api("C5_hadith_main.py", "Hardcoded", "fallback")
    return FALLBACK
