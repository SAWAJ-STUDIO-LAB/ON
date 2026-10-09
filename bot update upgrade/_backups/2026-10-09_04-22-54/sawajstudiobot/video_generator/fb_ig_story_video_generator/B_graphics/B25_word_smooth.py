"""B25_word_smooth.py — Sirf smooth."""


def smooth(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)
