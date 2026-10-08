"""D22_ease_out.py — Sirf ease_out."""


def ease_out(x):
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) * (1 - x)
