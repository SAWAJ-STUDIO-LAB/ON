"""D25_ease_smoothstep.py — Sirf smoothstep."""


def smoothstep(edge0, edge1, x):
    if edge0 == edge1:
        return 0.0 if x < edge0 else 1.0
    t = (x - edge0) / (edge1 - edge0)
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)
