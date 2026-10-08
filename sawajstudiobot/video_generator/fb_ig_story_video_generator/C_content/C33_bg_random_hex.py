"""C33_bg_random_hex.py — Sirf hex."""
import random


def get():
    return (f"{random.randint(10,30):02x}"
            f"{random.randint(8,25):02x}"
            f"{random.randint(25,55):02x}")
