"""H4_test_media.py — Sirf media test."""
from C_content.C5_hadith_main import fetch
from C_content.C20_tts_main import generate


def test_hadith_import():
    assert fetch is not None


def test_tts_import():
    assert generate is not None
