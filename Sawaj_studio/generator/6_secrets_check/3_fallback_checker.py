"""
🔄 Fallback Checker
"""


def check_fallback(providers):
    return [p for p in providers if p]


def count_working(providers):
    return sum(1 for p in providers if p)


def has_any(providers):
    return any(providers)
