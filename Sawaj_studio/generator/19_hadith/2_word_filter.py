"""
🔍 Word Filter
"""


def count_words(text):
    if not text:
        return 0
    return len(text.split())


def matches_range(text, min_words, max_words):
    n = count_words(text)
    return min_words <= n <= max_words


def filter_hadith(text, ideal_min=50, ideal_max=100):
    n = count_words(text)
    if ideal_min <= n <= ideal_max:
        return "ideal"
    elif 30 <= n <= 150:
        return "fallback"
    return None
