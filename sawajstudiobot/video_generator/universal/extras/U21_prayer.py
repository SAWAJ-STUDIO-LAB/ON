"""
U21_prayer.py — Prayer Times + Islamic Greeting
================================================
Fetch today's prayer times for overlay branding.

Fallback: greeting only (no times).
"""

import os
from datetime import datetime
from universal.U1_logger import log_file_start, log_file_end, log_step, log_api


class PrayerTimes:
    """Fetch prayer times via PRAYER_TIMES_API_URL."""

    def __init__(self, base=None):
        log_file_start("U21_prayer.py", "Prayer times fetcher")
        self.base = base
        log_file_end("U21_prayer.py", "success", "Ready")

    def fetch(self, city="Mumbai", country="India"):
        """
        Fetch prayer times for city.

        Returns dict {fajr, dhuhr, asr, maghrib, isha} or None.
        """
        api = os.environ.get("PRAYER_TIMES_API_URL")
        if not api or self.base is None:
            log_api("U21_prayer.py", "PrayerTimes", "skipped",
                    "no URL or session")
            return None

        try:
            url = (api.rstrip("/") +
                   f"/timingsByCity?city={city}"
                   f"&country={country}&method=2")
            log_step("U21_prayer.py", f"GET {url[:70]}", "info")
            r = self.base.session.get(url, timeout=15)

            if r.status_code == 200:
                timings = r.json().get("data", {}).get("timings", {})
                if timings:
                    out = {
                        "fajr":    self._clean(timings.get("Fajr", "")),
                        "dhuhr":   self._clean(timings.get("Dhuhr", "")),
                        "asr":     self._clean(timings.get("Asr", "")),
                        "maghrib": self._clean(timings.get("Maghrib", "")),
                        "isha":    self._clean(timings.get("Isha", "")),
                        "city":    city,
                    }
                    log_api("U21_prayer.py", "PrayerTimes", "success",
                            f"fajr={out['fajr']}")
                    return out

            log_api("U21_prayer.py", "PrayerTimes", "failed",
                    f"HTTP {r.status_code}")
        except Exception as e:
            log_api("U21_prayer.py", "PrayerTimes", "failed", str(e)[:80])

        return None

    def _clean(self, t):
        """Strip timezone suffix like ' (IST)'."""
        if not t:
            return ""
        return t.split(" ")[0].strip()

    def greeting(self):
        """Time-based Islamic greeting."""
        h = datetime.now().hour
        if 4 <= h < 12:
            return "صَبَاحُ الْخَيْرِ — Good Morning"
        elif 12 <= h < 17:
            return "Good Afternoon"
        elif 17 <= h < 20:
            return "Good Evening"
        else:
            return "مَسَاءُ الْخَيْرِ — Good Evening"

    def next_prayer(self, city="Mumbai", country="India"):
        """
        Return (name, time_str) of the next upcoming prayer.
        """
        times = self.fetch(city, country)
        if not times:
            return None
        try:
            now = datetime.now()
            current_min = now.hour * 60 + now.minute

            ordered = ["fajr", "dhuhr", "asr", "maghrib", "isha"]
            for name in ordered:
                t = times.get(name, "")
                if not t or ":" not in t:
                    continue
                h, m = map(int, t.split(":")[:2])
                if h * 60 + m > current_min:
                    return name.capitalize(), t
            # After isha → next is fajr tomorrow
            return "Fajr (tomorrow)", times.get("fajr", "")
        except Exception:
            return None
