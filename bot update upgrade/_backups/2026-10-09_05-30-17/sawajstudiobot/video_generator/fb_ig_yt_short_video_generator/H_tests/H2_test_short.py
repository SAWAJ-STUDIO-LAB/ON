# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      H2_test_short.py                          ║
# ║  📁 PATH:      .../fb_ig_yt_short_video_generator/       ║
# ║                H_tests/H2_test_short.py                  ║
# ║  🎯 PURPOSE:   Config + Utils tests                      ║
# ║  📖 FOLDER:    H_tests                                   ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   🧪 SHORT TESTS MODULE                                  ║
║   ═══════════════════════                                ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      Config + Utils ke basic tests                       ║
║                                                          ║
║   📖 Tests:                                              ║
║      • test_config_import()  → Config loads              ║
║      • test_sanitize_basic() → Whitespace clean          ║
║      • test_sanitize_quotes()→ Quote remove              ║
║      • test_sanitize_empty() → Empty returns empty       ║
║                                                          ║
║   ▶️  Run:                                                ║
║      pytest H_tests/H2_test_short.py -v                  ║
║                                                          ║
║   📝 Difference from Story:                               ║
║      Filename: H2_test_short.py (Story: _story)          ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

from A_core.A1_config import Config
from A_core.A4_utils import sanitize


# ═══════════════════════════════════════════════════════════
# ① TEST: Config class loads
# ═══════════════════════════════════════════════════════════

def test_config_import():
    """Config class should load."""
    assert Config is not None


# ═══════════════════════════════════════════════════════════
# ② TEST: Sanitize basic
# ═══════════════════════════════════════════════════════════

def test_sanitize_basic():
    """Sanitize should trim whitespace and newlines."""
    assert sanitize("  hello\nworld  ") == "hello world"


# ═══════════════════════════════════════════════════════════
# ③ TEST: Sanitize quotes
# ═══════════════════════════════════════════════════════════

def test_sanitize_quotes():
    """Sanitize should remove quotes."""
    assert sanitize("it's a 'test'") == "its a test"


# ═══════════════════════════════════════════════════════════
# ④ TEST: Sanitize empty
# ═══════════════════════════════════════════════════════════

def test_sanitize_empty():
    """Sanitize should handle empty input."""
    assert sanitize("") == ""
    assert sanitize(None) == ""
