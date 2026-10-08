"""
📖 Hadith Fetch
"""
import requests


def fetch_hadith(base_url, book_eng, number):
    try:
        url = base_url + "/editions/" + book_eng + "/" + str(number) + ".json"
        r = requests.get(url, timeout=15)
        if r.status_code != 200:
            return None
        data = r.json()
        hadiths = data.get("hadiths", [])
        if not hadiths:
            return None
        text = hadiths[0].get("text", "").strip()
        if len(text) < 30:
            return None
        return {"text": text, "number": hadiths[0].get("hadithnumber", number)}
    except Exception:
        return None
