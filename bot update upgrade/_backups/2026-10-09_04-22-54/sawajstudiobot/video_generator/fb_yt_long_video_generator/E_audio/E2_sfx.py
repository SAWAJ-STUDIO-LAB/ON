# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      E2_sfx.py                                 ║
# ║  📁 PATH:      .../fb_yt_long_video_generator/           ║
# ║                E_audio/E2_sfx.py                         ║
# ║  🎯 PURPOSE:   Sound effects (whoosh, ding, soft pad)    ║
# ║  📖 FOLDER:    E_audio                                   ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   🔊 SOUND EFFECTS MODULE (LONG)                         ║
║   ═══════════════════════                                ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      FFmpeg commands generate karna (long ke liye)       ║
║                                                          ║
║   📖 Functions:                                          ║
║      • whoosh_cmd()       → Transition whoosh            ║
║      • ding_cmd()         → CTA reveal ding              ║
║      • pad_cmd()          → Ambient pad (long)           ║
║      • section_chime_cmd()→ Section change chime         ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝


# ═══════════════════════════════════════════════════════════
# ① WHOOSH — soft whoosh for transitions
# ═══════════════════════════════════════════════════════════

def whoosh_cmd(outfile="whoosh.mp3"):
    """Return FFmpeg command for whoosh sound."""
    return (f'ffmpeg -y -f lavfi -i "anoisesrc=d=0.5:c=pink:a=0.5" '
            f'-af "afade=t=in:d=0.1,afade=t=out:st=0.3:d=0.2,volume=0.3" '
            f'{outfile}')


# ═══════════════════════════════════════════════════════════
# ② DING — soft bell for CTA reveal
# ═══════════════════════════════════════════════════════════

def ding_cmd(outfile="ding.mp3"):
    """Return FFmpeg command for ding sound."""
    return (f'ffmpeg -y -f lavfi -i "sine=frequency=880:duration=0.5" '
            f'-af "afade=t=out:st=0.2:d=0.3,volume=0.4" '
            f'{outfile}')


# ═══════════════════════════════════════════════════════════
# ③ PAD — ambient background pad (long only)
# ═══════════════════════════════════════════════════════════

def pad_cmd(outfile="pad.mp3", duration=900):
    """Return FFmpeg command for ambient pad (long video)."""
    return (f'ffmpeg -y -f lavfi -i "sine=frequency=110:duration={duration}" '
            f'-f lavfi -i "sine=frequency=165:duration={duration}" '
            f'-filter_complex "[0:a][1:a]amix=inputs=2:duration=longest,'
            f'volume=0.06,afade=t=in:st=0:d=3,afade=t=out:st={duration-8}:d=8" '
            f'{outfile}')


# ═══════════════════════════════════════════════════════════
# ④ SECTION CHIME — subtle chime for section change
# ═══════════════════════════════════════════════════════════

def section_chime_cmd(outfile="chime.mp3"):
    """Return FFmpeg command for section change chime."""
    return (f'ffmpeg -y -f lavfi -i "sine=frequency=523:duration=0.8" '
            f'-af "afade=t=in:d=0.05,afade=t=out:st=0.4:d=0.4,volume=0.25" '
            f'{outfile}')
