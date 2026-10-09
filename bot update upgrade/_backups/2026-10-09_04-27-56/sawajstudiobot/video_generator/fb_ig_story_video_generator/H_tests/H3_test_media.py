# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      H3_test_media.py                          ║
# ║  📁 PATH:      .../fb_ig_story_video_generator/          ║
# ║                H_tests/H3_test_media.py                  ║
# ║  🎯 PURPOSE:   Media module import tests                 ║
# ║  📖 FOLDER:    H_tests                                   ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   🧪 MEDIA TESTS MODULE                                  ║
║   ═══════════════════════                                ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      Media modules import tests                          ║
║                                                          ║
║   📖 Tests:                                              ║
║      • test_music_import()      → Music class loads      ║
║      • test_background_import() → Background class loads ║
║      • test_tts_import()        → TTS class loads        ║
║                                                          ║
║   ▶️  Run:                                                ║
║      pytest H_tests/H3_test_media.py -v                  ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝


# ═══════════════════════════════════════════════════════════
# ① TEST: Music class imports
# ═══════════════════════════════════════════════════════════

def test_music_import():
    """Music class should import."""
    from C_content.C5_music import Music
    assert Music is not None


# ═══════════════════════════════════════════════════════════
# ② TEST: Background class imports
# ═══════════════════════════════════════════════════════════

def test_background_import():
    """Background class should import."""
    from C_content.C6_background import Background
    assert Background is not None


# ═══════════════════════════════════════════════════════════
# ③ TEST: TTS class imports
# ═══════════════════════════════════════════════════════════

def test_tts_import():
    """TTS class should import."""
    from C_content.C4_tts import TTS
    assert TTS is not None
