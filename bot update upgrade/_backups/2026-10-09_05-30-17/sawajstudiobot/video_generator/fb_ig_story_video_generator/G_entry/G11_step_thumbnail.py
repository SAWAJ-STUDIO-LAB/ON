"""G11_step_thumbnail.py — Sirf thumb."""
from C_content.C46_thumb_main import make


def run(hindi, arabic, english, label):
    return make(hindi, arabic, english, label, "output/final/thumbnail.jpg")
