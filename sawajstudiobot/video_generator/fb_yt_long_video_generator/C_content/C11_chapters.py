# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      C11_chapters.py                           ║
# ║  📁 PATH:      .../fb_yt_long_video_generator/           ║
# ║                C_content/C11_chapters.py                 ║
# ║  🎯 PURPOSE:   ⭐ YouTube Chapters & Timestamps          ║
# ║  📖 FOLDER:    C_content                                 ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   🏷️ YOUTUBE CHAPTERS MODULE                             ║
║   ═══════════════════════════════════════                ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      Long video ke sections ka timestamp bana kar        ║
║      YouTube description mein chapters add karna.        ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

from A_core.A2_logger import log_file_start, log_file_end, log_step


class ChapterGenerator:
    """Builds YouTube chapter timestamps for long videos."""

    def __init__(self):
        log_file_start("C11_chapters.py", "Chapter generator")
        log_file_end("C11_chapters.py", "success", "Ready")

    def build(self, section_durations):
        """
        Build chapters from section durations.

        Args:
            section_durations: dict {title: duration_seconds}

        Returns:
            list of dicts: [{time_str, seconds, title}, ...]
        """
        log_step("C11_chapters.py", "build() starting", "ok")
        chapters = []
        current = 0.0

        for title, dur in section_durations.items():
            mins = int(current // 60)
            secs = int(current % 60)
            chapters.append({
                "time_str": f"{mins:02d}:{secs:02d}",
                "seconds": current,
                "title": title,
            })
            current += dur

        log_step("C11_chapters.py", f"{len(chapters)} chapters built", "ok")
        return chapters

    def format_description(self, chapters):
        """Format chapters as YouTube description block."""
        lines = ["⏱️ Timestamps:"]
        for c in chapters:
            lines.append(f"{c['time_str']} - {c['title']}")
        return "\n".join(lines)

    def format_list(self, chapters):
        """Format as simple list of strings for uploader."""
        return [f"{c['time_str']} - {c['title']}" for c in chapters]
