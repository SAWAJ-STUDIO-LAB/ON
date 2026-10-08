"""C3_hadith_fetch_one.py — Sirf fetch one."""
from A_core.A26_sanitize import sanitize
from C_content.C2_hadith_count import count


def fetch_one(session, base_url, book, num):
    try:
        url = f"{base_url}/editions/{book['eng']}/{num}.json"
        r = session.get(url, timeout=15)
        if r.status_code != 200:
            return None
        hs = r.json().get("hadiths", [])
        if not hs:
            return None
        eng = sanitize(hs[0].get("text", ""))
        if len(eng) < 30:
            return None
        ara = ""
        try:
            ar = session.get(url.replace(book["eng"], book["ara"]), timeout=10)
            if ar.status_code == 200:
                ad = ar.json().get("hadiths", [])
                if ad:
                    ara = sanitize(ad[0].get("text", ""))
        except Exception:
            pass
        return {"collection": book["name"], "number": str(hs[0].get("hadithnumber") or num),
                "english": eng, "arabic": ara, "word_count": count(eng)}
    except Exception:
        return None
