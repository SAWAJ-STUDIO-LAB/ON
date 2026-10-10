"""Hadith fetcher"""
import random
from .utils import sanitize

def fetch_hadith(session, long=False):
    books = [
        {"eng": "eng-bukhari", "ara": "ara-bukhari", "name": "Sahih al-Bukhari", "max": 7000},
        {"eng": "eng-muslim", "ara": "ara-muslim", "name": "Sahih Muslim", "max": 5000},
        {"eng": "eng-abudawud", "ara": "ara-abudawud", "name": "Sunan Abu Dawud", "max": 4000},
        {"eng": "eng-tirmidhi", "ara": "ara-tirmidhi", "name": "Jami at-Tirmidhi", "max": 3500},
    ]
    bases = [
        "https://cdn.jsdelivr.net/gh/fawazahmed0/hadith-api@1",
        "https://raw.githubusercontent.com/fawazahmed0/hadith-api/1"
    ]
    min_len = 200 if long else 30
    for _ in range(30 if long else 1):
        book = random.choice(books)
        num = random.randint(1, book["max"])
        for base in bases:
            try:
                url = f"{base}/editions/{book['eng']}/{num}.json"
                r = session.get(url, timeout=15)
                if r.status_code != 200: continue
                hs = r.json().get("hadiths", [])
                if not hs: continue
                eng = sanitize(hs[0].get("text", ""))
                if len(eng) < min_len: continue
                ara = ""
                try:
                    ar = session.get(url.replace(book["eng"], book["ara"]), timeout=10)
                    if ar.status_code == 200:
                        ad = ar.json().get("hadiths", [])
                        if ad: ara = sanitize(ad[0].get("text", ""))
                except: pass
                return {"collection": book["name"],
                        "number": str(hs[0].get("hadithnumber") or num),
                        "english": eng, "arabic": ara}
            except: pass
    return {"collection": "Sahih al-Bukhari", "number": "1",
            "english": "The reward of deeds depends upon the intentions and every person will get the reward according to what he has intended.",
            "arabic": "إِنَّمَا الأَعْمَالُ بِالنِّيَّاتِ وَإِنَّمَا لِكُلِّ امْرِئٍ مَا نَوَى"}
