"""C11_chapters.py"""
from A_core.A9_log_step import log_step


class ChapterGenerator:
    def build(self, section_durations):
        log_step("C11_chapters.py", "build()", "ok")
        chapters = []
        current = 0.0
        for title, dur in section_durations.items():
            mins = int(current // 60)
            secs = int(current % 60)
            chapters.append({"time_str": f"{mins:02d}:{secs:02d}",
                             "seconds": current, "title": title})
            current += dur
        return chapters

    def format_list(self, chapters):
        return [f"{c['time_str']} - {c['title']}" for c in chapters]
