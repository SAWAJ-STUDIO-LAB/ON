# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      H3_test_media.py                          ║
# ║  📁 PATH:      .../fb_yt_long_video_generator/           ║
# ║                H_tests/H3_test_media.py                  ║
# ║  🎯 PURPOSE:   Media module import tests                 ║
# ║  📖 FOLDER:    H_tests                                   ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   🧪 MEDIA TESTS MODULE (LONG)                           ║
║   ═══════════════════════                                ║
║                                                          ║
║   ▶️  Run:                                                ║
║      pytest H_tests/H3_test_media.py -v                  ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""


def test_music_import():
    """Music class should import."""
    from C_content.C5_music import Music
    assert Music is not None


def test_background_import():
    """Background class should import."""
    from C_content.C6_background import Background
    assert Background is not None


def test_tts_import():
    """TTSManager class should import."""
    from C_content.C4_tts import TTSManager
    assert TTSManager is not None


def test_meaning_import():
    """Meaning class should import."""
    from C_content.C9_meaning import Meaning
    assert Meaning is not None


def test_bullets_import():
    """BulletGenerator class should import."""
    from C_content.C10_bullets import BulletGenerator
    assert BulletGenerator is not None


def test_chapters_import():
    """ChapterGenerator class should import."""
    from C_content.C11_chapters import ChapterGenerator
    assert ChapterGenerator is not None


def test_subtitles_import():
    """SubtitleGenerator class should import."""
    from C_content.C12_subtitles import SubtitleGenerator
    assert SubtitleGenerator is not None
