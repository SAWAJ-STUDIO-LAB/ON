"""
〰️ Sine Wave
"""
import math


def sine_value(t, frequency=1.0, amplitude=1.0, phase=0.0):
    return amplitude * math.sin(t * frequency + phase)


def sine_normalized(t, frequency=1.0, phase=0.0):
    return (math.sin(t * frequency + phase) + 1) / 2
