"""D18_ease_inout.py — Sirf ease_in_out."""


def ease_in_out(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)
