"""H5_test_render.py — Sirf render test."""
from D_video.D15_frames_generate import generate
from B_graphics.B2_font_load import load


def test_frames_import():
    assert generate is not None


def test_font_import():
    assert load is not None
