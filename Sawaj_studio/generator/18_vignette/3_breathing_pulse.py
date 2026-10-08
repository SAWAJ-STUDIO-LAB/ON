"""
💓 Breathing Pulse
"""
import math


def breathing_pulse(t, base=60, amount=12, speed=0.8):
    pulse = int(amount * math.sin(t * speed))
    val = base + pulse
    return max(20, min(100, val))


def soft_pulse(t, base=50, amount=8, speed=0.5):
    return base + int(amount * math.sin(t * speed))
