"""yt_long_chapters.py"""


def format_chapters(chapters):
    if not chapters:
        return ""
    lines = ["\n\n⏱️ Timestamps:"]
    for c in chapters:
        lines.append(f"{c} " if isinstance(c, str) else str(c))
    return "\n".join(lines)
