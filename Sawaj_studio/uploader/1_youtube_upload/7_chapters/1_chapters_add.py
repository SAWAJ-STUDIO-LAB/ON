"""
⏱️ YouTube Chapters Add
"""


def format_chapters(chapters):
    if not chapters:
        return ""
    lines = ["⏱️ Timestamps:"]
    for c in chapters:
        lines.append(c)
    return "\n".join(lines)


def build_chapters(section_durations):
    chapters = []
    current = 0.0
    for title, dur in section_durations.items():
        mins = int(current // 60)
        secs = int(current % 60)
        chapters.append("%02d:%02d - %s" % (mins, secs, title))
        current += dur
    return chapters
