# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      E2_sfx.py                                 ║
# ║  📁 PATH:      .../fb_ig_yt_short_video_generator/       ║
# ║                E_audio/E2_sfx.py                         ║
# ║  🎯 PURPOSE:   Sound effects (whoosh, ding)              ║
# ║  📖 FOLDER:    E_audio                                   ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   🔊 SOUND EFFECTS MODULE (SHORT)                        ║
║   ═══════════════════════                                ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      FFmpeg sound effects commands generate karna        ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""


def whoosh_cmd(outfile="whoosh.mp3"):
    """Return FFmpeg command for whoosh sound."""
    return (
        f'ffmpeg -y -f lavfi -i "anoisesrc=d=0.5:c=pink:a=0.5" '
        f'-af "afade=t=in:d=0.1,afade=t=out:st=0.3:d=0.2,volume=0.3" '
        f'{outfile}'
    )


def ding_cmd(outfile="ding.mp3"):
    """Return FFmpeg command for ding sound."""
    return (
        f'ffmpeg -y -f lavfi -i "sine=frequency=880:duration=0.5" '
        f'-af "afade=t=out:st=0.2:d=0.3,volume=0.4" '
        f'{outfile}'
    )
