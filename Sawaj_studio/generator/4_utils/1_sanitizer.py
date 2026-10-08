"""
🧹 Sanitizer
"""
import re


def sanitize(text):
    if not text:
        return ""
    text = re.sub(r"[\u200b-\u200f\ufeff\u202a-\u202e]", "", str(text))
    return text.replace(chr(34), "").replace(chr(39), "").replace("\n", " ").strip()


def remove_quotes(text):
    if not text:
        return ""
    return str(text).replace('"', "").replace("'", "").strip()
