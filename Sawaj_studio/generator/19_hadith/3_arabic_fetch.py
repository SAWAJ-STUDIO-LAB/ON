"""
🇸🇦 Arabic Fetch
"""
import requests


def fetch_arabic(base_url, book_ara, number):
    try:
        url = base_url + "/editions/" + book_ara + "/" + str(number) + ".json"
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            return ""
        data = r.json()
        hadiths = data.get("hadiths", [])
        if not hadiths:
            return ""
        return hadiths[0].get("text", "").strip()
    except Exception:
        return ""
