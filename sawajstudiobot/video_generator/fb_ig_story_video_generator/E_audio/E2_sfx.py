# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      E2_sfx.py                                 ║
# ║  📁 PATH:      .../fb_ig_story_video_generator/          ║
# ║                E_audio/E2_sfx.py                         ║
# ║  🎯 PURPOSE:   Sound effects (whoosh, ding)              ║
# ║  📖 FOLDER:    E_audio                                   ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   🔊 SOUND EFFECTS MODULE (STORY)                        ║
║   ═══════════════════════                                ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      FFmpeg sound effects commands generate karna        ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

import os

def whoosh_cmd(outfile: str = "whoosh.mp3") -> str:
    """
    Return FFmpeg command for whoosh sound effect.

    Args:
        outfile (str): Output file path for the generated sound effect.
                       Defaults to 'whoosh.mp3'.

    Returns:
        str: FFmpeg command string to generate whoosh sound.
    """
    return (
        f'ffmpeg -y -f lavfi -i "anoisesrc=d=0.5:c=pink:a=0.5" '
        f'-af "afade=t=in:d=0.1,afade=t=out:st=0.3:d=0.2,volume=0.3" '
        f'{outfile}'
    )

def ding_cmd(outfile: str = "ding.mp3") -> str:
    """
    Return FFmpeg command for ding sound effect.

    Args:
        outfile (str): Output file path for the generated sound effect.
                       Defaults to 'ding.mp3'.

    Returns:
        str: FFmpeg command string to generate ding sound.
    """
    return (
        f'ffmpeg -y -f lavfi -i "sine=frequency=880:duration=0.5" '
        f'-af "afade=t=out:st=0.2:d=0.3,volume=0.4" '
        f'{outfile}'
    )

# Optional: Add error handling for file operations
def generate_sfx(cmd: str) -> None:
    """
    Execute FFmpeg command to generate sound effect.

    Args:
        cmd (str): FFmpeg command string.
    """
    try:
        os.system(cmd)
    except Exception as e:
        print(f"Error generating sound effect: {e}")

# Example usage (optional)
if __name__ == "__main__":
    whoosh_command = whoosh_cmd()
    ding_command = ding_cmd()
    generate_sfx(whoosh_command)
    generate_sfx(ding_command)
