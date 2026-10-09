"""D24_ease_cubic.py — Sirf cubic."""


def ease_cubic(x):
    x = max(0.0, min(1.0, x))
    if x < 0.5:
        return 4 * x * x * x
    return 1 - pow(-2 * x + 2, 3) / 2
