# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      H4_test_render.py                         ║
# ║  📁 PATH:      .../fb_yt_long_video_generator/           ║
# ║                H_tests/H4_test_render.py                 ║
# ║  🎯 PURPOSE:   Render module import tests                ║
# ║  📖 FOLDER:    H_tests                                   ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   🧪 RENDER TESTS MODULE (LONG)                          ║
║   ═══════════════════════                                ║
║                                                          ║
║   ▶️  Run:                                                ║
║      pytest H_tests/H4_test_render.py -v                 ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""


def test_frames_import():
    """Frames class should import."""
    from D_video.D4_frames import Frames
    assert Frames is not None


def test_composer_import():
    """Composer class should import."""
    from D_video.D6_composer import Composer
    assert Composer is not None


def test_fonts_import():
    """FontManager class should import."""
    from B_graphics.B1_fonts import FontManager
    assert FontManager is not None
