"""D4_main_alpha.py — Sirf alpha."""


def get_alpha(mt):
    return min(1.0, mt / 0.5) if mt > 0 else 0.0
