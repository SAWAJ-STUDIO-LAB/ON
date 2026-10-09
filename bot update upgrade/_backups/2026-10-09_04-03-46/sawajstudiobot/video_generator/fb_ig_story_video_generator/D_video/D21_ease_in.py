"""D21_ease_in.py — Sirf ease_in."""


def ease_in(x):
    x = max(0.0, min(1.0, x))
    return x * x
