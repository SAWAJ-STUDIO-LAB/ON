"""D23_ease_bounce.py — Sirf bounce."""


def ease_bounce(x):
    x = max(0.0, min(1.0, x))
    if x < 0.8:
        return x * 1.35
    return 1.08 - (x - 0.8) * 0.4
