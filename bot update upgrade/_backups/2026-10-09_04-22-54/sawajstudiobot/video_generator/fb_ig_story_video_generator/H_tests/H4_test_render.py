# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      H4_test_render.py                         ║
# ║  📁 PATH:      .../fb_ig_story_video_generator/          ║
# ║                H_tests/H4_test_render.py                 ║
# ║  🎯 PURPOSE:   Render module import tests                ║
# ║  📖 FOLDER:    H_tests                                   ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   🧪 RENDER TESTS MODULE                                 ║
║   ═══════════════════════                                ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      Render modules import tests                         ║
║                                                          ║
║   📖 Tests:                                              ║
║      • test_frames_import()   → Frames class loads       ║
║      • test_composer_import() → Composer class loads     ║
║      • test_fonts_import()    → FontLoader loads         ║
║                                                          ║
║   ▶️  Run:                                                ║
║      pytest H_tests/H4_test_render.py -v                 ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝


# ═══════════════════════════════════════════════════════════
# ① TEST: Frames class imports
# ═══════════════════════════════════════════════════════════

def test_frames_import():
    """Frames class should import."""
    from D_video.D4_frames import Frames
    assert Frames is not None


# ═══════════════════════════════════════════════════════════
# ② TEST: Composer class imports
# ═══════════════════════════════════════════════════════════

def test_composer_import():
    """Composer class should import."""
    from D_video.D6_composer import Composer
    assert Composer is not None


# ═══════════════════════════════════════════════════════════
# ③ TEST: FontLoader class imports
# ═══════════════════════════════════════════════════════════

def test_fonts_import():
    """FontLoader class should import."""
    from B_graphics.B1_fonts import FontLoader
    assert FontLoader is not None
