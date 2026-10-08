"""D27_ease_pulse.py — Sirf pulse."""
import math


def pulse(t, speed=1.0, min_val=0.0, max_val=1.0):
    mid = (min_val + max_val) / 2
    amp = (max_val - min_val) / 2
    return mid + amp * math.sin(t * speed)
