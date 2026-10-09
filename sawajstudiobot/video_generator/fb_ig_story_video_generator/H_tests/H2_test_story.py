# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      H2_test_story.py                          ║
# ║  📁 PATH:      .../fb_ig_story_video_generator/          ║
# ║                H_tests/H2_test_story.py                  ║
# ║  🎯 PURPOSE:   Config + Utils tests                      ║
# ║  📖 FOLDER:    H_tests                                   ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   🧪 STORY TESTS MODULE                                  ║
║   ═══════════════════════                                ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      Config + Utils के बेसिक टेस्ट्स                    ║
║                                                          ║
║   📖 Tests:                                              ║
║      • test_config_import()  → Config लोड होना चाहिए    ║
║      • test_sanitize_basic() → व्हाइटस्पेस और न्यूलाइन्स क्लीन होने चाहिए  ║
║      • test_sanitize_quotes()→ कोट्स हटाए जाने चाहिए    ║
║      • test_sanitize_empty() → खाली इनपुट को खाली रिटर्न करना चाहिए  ║
║                                                          ║
║   ▶️  Run:                                                ║
║      pytest H_tests/H2_test_story.py -v                  ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

from A_core.A1_config import Config
from A_core.A4_utils import sanitize


# ═══════════════════════════════════════════════════════════
# ① TEST: Config class loads
# ═══════════════════════════════════════════════════════════

def test_config_import():
    """Config क्लास लोड होना चाहिए और इंस्टेंस बनाया जाना चाहिए."""
    config = Config()
    assert isinstance(config, Config)


# ═══════════════════════════════════════════════════════════
# ② TEST: Sanitize basic
# ═══════════════════════════════════════════════════════════

def test_sanitize_basic():
    """sanitize फ़ंक्शन को व्हाइटस्पेस और न्यूलाइन्स को ट्रिम करना चाहिए."""
    assert sanitize("  hello\nworld  ") == "hello world"
    assert sanitize("   multiple   \n  lines  ") == "multiple lines"


# ═══════════════════════════════════════════════════════════
# ③ TEST: Sanitize quotes
# ═══════════════════════════════════════════════════════════

def test_sanitize_quotes():
    """sanitize फ़ंक्शन को कोट्स हटाने चाहिए."""
    assert sanitize("it's a 'test'") == "its a test"
    assert sanitize("'single' and \"double\" quotes") == "single and double quotes"


# ═══════════════════════════════════════════════════════════
# ④ TEST: Sanitize empty
# ═══════════════════════════════════════════════════════════

def test_sanitize_empty():
    """sanitize फ़ंक्शन को खाली इनपुट को खाली स्ट्रिंग रिटर्न करना चाहिए."""
    assert sanitize("") == ""
    assert sanitize(None) == ""
