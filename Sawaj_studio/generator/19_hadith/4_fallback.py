"""
🔄 Fallback
"""
FALLBACK_HADITH = {
    "collection": "Sahih al-Bukhari",
    "number": "1",
    "english": ("Actions are judged by intentions, and every person will get "
                "what they intended."),
    "arabic": "إنما الأعمال بالنيات وإنما لكل امرئ ما نوى",
}


def get_fallback():
    return FALLBACK_HADITH.copy()
