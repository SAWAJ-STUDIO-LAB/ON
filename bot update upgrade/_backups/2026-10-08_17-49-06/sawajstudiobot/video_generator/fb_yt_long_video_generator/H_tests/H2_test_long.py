# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      H2_test_long.py                           ║
# ║  📁 PATH:      .../fb_yt_long_video_generator/           ║
# ║                H_tests/H2_test_long.py                   ║
# ║  🎯 PURPOSE:   Config + Utils tests                      ║
# ║  📖 FOLDER:    H_tests                                   ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   🧪 LONG TESTS MODULE                                   ║
║   ═══════════════════════                                ║
║                                                          ║
║   ▶️  Run:                                                ║
║      pytest H_tests/H2_test_long.py -v                   ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

from A_core.A1_config import Config
from A_core.A4_utils import sanitize


def test_config_import():
    """Config class should load."""
    assert Config is not None


def test_sanitize_basic():
    """Sanitize should trim whitespace and newlines."""
    assert sanitize("  hello\nworld  ") == "hello world"


def test_sanitize_quotes():
    """Sanitize should remove quotes."""
    assert sanitize("it's a 'test'") == "its a test"


def test_sanitize_empty():
    """Sanitize should handle empty input."""
    assert sanitize("") == ""
    assert sanitize(None) == ""
