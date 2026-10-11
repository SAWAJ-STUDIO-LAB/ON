"""
U22_weather.py — Weather Mood Selector
=======================================
Uses OpenWeather to pick a background video "mood".

Moods: serene | clear | cloudy | stormy

This mood is used by Background module to search relevant stock videos.
"""

import os
from universal.U1_logger import log_file_start, log_file_end, log_step, log_api


class WeatherMood:
    """Fetch current weather mood for a city."""

    MOOD_MAP = {
        "clear":   "clear",
        "clouds":  "cloudy",
        "rain":    "stormy",
        "drizzle": "stormy",
        "thunder": "stormy",
        "snow":    "serene",
        "mist":    "serene",
        "fog":     "serene",
        "haze":    "cloudy",
        "smoke":   "cloudy",
    }

    def __init__(self, base=None):
        log_file_start("U22_weather.py", "Weather mood fetcher")
        self.base = base
        log_file_end("U22_weather.py", "success", "Ready")

    def get(self, city="Mumbai"):
        """
        Return mood keyword: 'serene' | 'clear' | 'cloudy' | 'stormy'.
        """
        key = os.environ.get("OPENWEATHER_API_KEY")
        if not key or self.base is None:
            log_api("U22_weather.py", "Weather", "skipped",
                    "no key or session")
            return "serene"

        try:
            r = self.base.session.get(
                "https://api.openweathermap.org/data/2.5/weather",
                params={"q": city, "appid": key, "units": "metric"},
                timeout=15)

            if r.status_code == 200:
                data = r.json()
                weather_list = data.get("weather", [])
                if weather_list:
                    main = weather_list[0].get("main", "").lower()
                    mood = self.MOOD_MAP.get(main, "serene")
                    log_api("U22_weather.py", "Weather", "success",
                            f"{main} → {mood}")
                    return mood

            log_api("U22_weather.py", "Weather", "failed",
                    f"HTTP {r.status_code}")
        except Exception as e:
            log_api("U22_weather.py", "Weather", "failed", str(e)[:80])

        return "serene"

    def get_detailed(self, city="Mumbai"):
        """Return full weather dict or None."""
        key = os.environ.get("OPENWEATHER_API_KEY")
        if not key or self.base is None:
            return None
        try:
            r = self.base.session.get(
                "https://api.openweathermap.org/data/2.5/weather",
                params={"q": city, "appid": key, "units": "metric"},
                timeout=15)
            if r.status_code == 200:
                d = r.json()
                return {
                    "temp": d.get("main", {}).get("temp", 0),
                    "feels_like": d.get("main", {}).get("feels_like", 0),
                    "main": (d.get("weather", [{}])[0].get("main", "")
                             if d.get("weather") else ""),
                    "description": (d.get("weather", [{}])[0]
                                    .get("description", "")
                                    if d.get("weather") else ""),
                    "city": d.get("name", city),
                }
        except Exception:
            pass
        return None


# ═══════════════════════════════════════════════════════════
# COMBINED ENHANCER (convenience)
# ═══════════════════════════════════════════════════════════

class ExtrasEnhancer:
    """
    All 3 extras in one call — for use in G1 pipeline.

    Usage in G1:
        from universal.extras import U20_quran, U21_prayer, U22_weather
        extras = {
            "ayah":    U20_quran.QuranAyah(self).fetch_random(),
            "prayer":  U21_prayer.PrayerTimes(self).fetch("Mumbai"),
            "greeting":U21_prayer.PrayerTimes(self).greeting(),
            "mood":    U22_weather.WeatherMood(self).get("Mumbai"),
        }
    """

    def __init__(self, base):
        self.quran = QuranAyah(base)
        self.prayer = PrayerTimes(base)
        self.weather = WeatherMood(base)

    def gather(self, city="Mumbai"):
        return {
            "ayah":     self.quran.fetch_random(),
            "prayer":   self.prayer.fetch(city),
            "greeting": self.prayer.greeting(),
            "next_prayer": self.prayer.next_prayer(city),
            "mood":     self.weather.get(city),
        }


# Backward compat: import from C13_extras
__all__ = ["QuranAyah", "PrayerTimes", "WeatherMood", "ExtrasEnhancer"]
