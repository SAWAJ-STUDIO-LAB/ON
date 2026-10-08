"""
⬆️ Rising Motion
"""
import math


def get_rising_y(base_y, t, speed=40, wrap=1920):
    return (base_y - int(t * speed)) % wrap


def get_drift_x(base_x, t, amplitude=15, speed=0.8):
    return base_x + int(amplitude * math.sin(t * speed))
