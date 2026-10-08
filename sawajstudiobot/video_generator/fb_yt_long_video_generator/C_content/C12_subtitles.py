"""C12_subtitles.py"""
import os
from A_core.A9_log_step import log_step


def _fmt(sec):
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    ms = int((sec - int(sec)) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


class SubtitleGenerator:
    def create_srt(self, segments, output_path):
        if not segments:
            return False
        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                for i, seg in enumerate(segments, 1):
                    f.write(f"{i}\n{_fmt(seg['start'])} --> {_fmt(seg['end'])}")
                    f.write(f"\n{seg['text']}\n\n")
            return True
        except Exception:
            return False

    def from_text(self, text, total_duration, output_path, chunk_words=8):
        if not text or total_duration <= 0:
            return False
        words = text.split()
        chunks = [" ".join(words[i:i+chunk_words]) for i in range(0, len(words), chunk_words)]
        if not chunks:
            return False
        seg_dur = total_duration / len(chunks)
        segments = [{"start": i * seg_dur, "end": (i + 1) * seg_dur, "text": c}
                    for i, c in enumerate(chunks)]
        return self.create_srt(segments, output_path)
