# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      C13_extras.py                             ║
# ║  📁 PATH:      .../fb_ig_story_video_generator/          ║
# ║                C_content/C13_extras.py                   ║
# ║  🎯 PURPOSE:   Quran + Prayer Times + Weather integrate  ║
# ║  ✅ NEW:       3 unused secrets अब use हो रहे हैं          ║
# ╚══════════════════════════════════════════════════════════╝

import os
from datetime import datetime
from A_core.A2_logger import log_file_start, log_file_end, log_step, log_api


# ═══════════════════════════════════════════════════════════
# 1. QURAN AYAH FETCHER
# ═══════════════════════════════════════════════════════════

class QuranAyah:
    """
    Fetch a related Quran Ayah for the hadith.

    Uses QURAN_API_URL env (e.g. https://api.alquran.cloud/v1/ayah/2:255)
    Falls back to a random popular ayah if API missing.
    """

    FALLBACK_AYAHS = [
        {"arabic": "إِنَّ اللَّهَ مَعَ الصَّابِرِينَ",
         "english": "Indeed, Allah is with the patient.",
         "reference": "Al-Baqarah 2:153"},
        {"arabic": "فَاذْكُرُونِي أَذْكُرْكُمْ",
         "english": "So remember Me; I will remember you.",
         "reference": "Al-Baqarah 2:152"},
        {"arabic": "وَمَن يَتَوَكَّلْ عَلَى اللَّهِ فَهُوَ حَسْبُهُ",
         "english": "And whoever relies upon Allah — He is sufficient for him.",
         "reference": "At-Talaq 65:3"},
    ]

    def __init__(self, base):
        log_file_start("C13_extras.py::QuranAyah", "Quran ayah fetcher")
        self.base = base
        log_file_end("C13_extras.py::QuranAyah", "success")

    def fetch_random(self):
        """Fetch a random ayah from API or fallback."""
        import random

        api = os.environ.get("QURAN_API_URL")
        if api:
            try:
                # random ayah: alquran.cloud style
                num = random.randint(1, 6236)
                url = api.rstrip("/") + f"/ayah/{num}/editions/quran-uthmani,en.sahih"
                log_step("C13_extras.py", f"Quran API: {url[:80]}", "info")
                r = self.base.session.get(url, timeout=15)
                if r.status_code == 200:
                    data = r.json().get("data", [])
                    if isinstance(data, list) and len(data) >= 2:
                        ar = data[0].get("text", "")
                        en = data[1].get("text", "")
                        ref = f"{data[0].get('surah', {}).get('englishName', '')} " \
                              f"{data[0].get('surah', {}).get('number', '')}:" \
                              f"{data[0].get('numberInSurah', '')}"
                        log_api("C13_extras.py", "QuranAPI", "success", ref)
                        return {"arabic": ar, "english": en, "reference": ref}
            except Exception as e:
                log_api("C13_extras.py", "QuranAPI", "failed", str(e)[:80])

        # Fallback
        log_api("C13_extras.py", "QuranFallback", "fallback")
        return random.choice(self.FALLBACK_AYAHS)


# ═══════════════════════════════════════════════════════════
# 2. PRAYER TIMES FETCHER
# ═══════════════════════════════════════════════════════════

class PrayerTimes:
    """
    Fetch today's prayer times for branding overlay.

    Uses PRAYER_TIMES_API_URL env.
    """

    def __init__(self, base):
        log_file_start("C13_extras.py::PrayerTimes", "Prayer times fetcher")
        self.base = base
        log_file_end("C13_extras.py::PrayerTimes", "success")

    def fetch(self, city="Mumbai", country="India"):
        """Fetch prayer times or return None on failure."""
        api = os.environ.get("PRAYER_TIMES_API_URL")
        if not api:
            log_api("C13_extras.py", "PrayerTimes", "skipped", "no URL")
            return None
        try:
            url = (api.rstrip("/") +
                   f"/timingsByCity?city={city}&country={country}&method=2")
            log_step("C13_extras.py", f"Prayer API: {url[:80]}", "info")
            r = self.base.session.get(url, timeout=15)
            if r.status_code == 200:
                data = r.json().get("data", {}).get("timings", {})
                if data:
                    out = {
                        "fajr": data.get("Fajr", ""),
                        "dhuhr": data.get("Dhuhr", ""),
                        "asr": data.get("Asr", ""),
                        "maghrib": data.get("Maghrib", ""),
                        "isha": data.get("Isha", ""),
                    }
                    log_api("C13_extras.py", "PrayerTimes", "success",
                            f"fajr={out['fajr']}")
                    return out
        except Exception as e:
            log_api("C13_extras.py", "PrayerTimes", "failed", str(e)[:80])
        return None

    def greeting(self):
        """Return time-based Islamic greeting."""
        h = datetime.now().hour
        if 4 <= h < 12:
            return "صَبَاحُ الْخَيْرِ — Good Morning"
        elif 12 <= h < 17:
            return "Good Afternoon"
        elif 17 <= h < 20:
            return "Good Evening"
        else:
            return "مَسَاءُ الْخَيْرِ — Good Evening"


# ═══════════════════════════════════════════════════════════
# 3. WEATHER MOOD (background tone selector)
# ═══════════════════════════════════════════════════════════

class WeatherMood:
    """
    Uses OpenWeather to pick a background video "mood".

    Returns one of: "serene" | "stormy" | "cloudy" | "clear"
    """

    def __init__(self, base):
        log_file_start("C13_extras.py::WeatherMood", "Weather mood")
        self.base = base
        log_file_end("C13_extras.py::WeatherMood", "success")

    def get(self, city="Mumbai"):
        """Return mood keyword for background search."""
        key = os.environ.get("OPENWEATHER_API_KEY")
        if not key:
            log_api("C13_extras.py", "Weather", "skipped", "no key")
            return "serene"

        try:
            r = self.base.session.get(
                "https://api.openweathermap.org/data/2.5/weather",
                params={"q": city, "appid": key, "units": "metric"},
                timeout=15)
            if r.status_code == 200:
                data = r.json()
                weather = data.get("weather", [{}])[0]
                main = weather.get("main", "").lower()

                mood = "serene"
                if "clear" in main:
                    mood = "clear"
                elif "cloud" in main:
                    mood = "cloudy"
                elif "rain" in main or "thunder" in main or "storm" in main:
                    mood = "stormy"

                log_api("C13_extras.py", "Weather", "success",
                        f"{main} → {mood}")
                return mood
        except Exception as e:
            log_api("C13_extras.py", "Weather", "failed", str(e)[:80])
        return "serene"


# ═══════════════════════════════════════════════════════════
# 4. COMBINED ENHANCER
# ═══════════════════════════════════════════════════════════

class ExtrasEnhancer:
    """Convenience wrapper — use all 3 in one call."""

    def __init__(self, base):
        self.quran = QuranAyah(base)
        self.prayer = PrayerTimes(base)
        self.weather = WeatherMood(base)

    def gather(self, city="Mumbai"):
        return {
            "ayah": self.quran.fetch_random(),
            "prayer": self.prayer.fetch(city),
            "greeting": self.prayer.greeting(),
            "mood": self.weather.get(city),
        }
