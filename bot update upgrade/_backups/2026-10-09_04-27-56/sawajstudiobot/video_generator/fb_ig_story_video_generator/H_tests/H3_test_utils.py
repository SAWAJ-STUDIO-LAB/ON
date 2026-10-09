"""H3_test_utils.py — Sirf utils test."""
from A_core.A26_sanitize import sanitize


def test_sanitize_basic():
    assert sanitize("  hello\nworld  ") == "hello world"


def test_sanitize_empty():
    assert sanitize("") == ""
    assert sanitize(None) == ""
