# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      C12_subtitles.py                          ║
# ║  📁 PATH:      .../fb_yt_long_video_generator/           ║
# ║                C_content/C12_subtitles.py                ║
# ║  🎯 PURPOSE:   SRT Subtitle File Generator               ║
# ║  📖 FOLDER:    C_content                                 ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   📜 SUBTITLE GENERATOR (LONG)                           ║
║   ═══════════════════════════                            ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      Timed .srt files generate karna for YouTube         ║
║      and Facebook closed captions.                       ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

import os
from A_core.A2_logger import log_file_start, log_file_end, log_step


def _format_ts(seconds):
    """Format seconds → SRT timestamp HH:MM:SS,mmm."""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds - int(seconds)) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


class SubtitleGenerator:
    """Generate SRT subtitles for long videos."""

    def __init__(self):
        log_file_start("C12_subtitles.py", "Subtitle generator")
        log_file_end("C12_subtitles.py", "success", "Ready")

    def create_srt(self, segments, output_path):
        """
        Create SRT file from segments.

        Args:
            segments: list of {start, end, text}
            output_path: srt file path

        Returns:
            True if successful
        """
        log_step("C12_subtitles.py", f"create_srt({len(segments)} segments)", "ok")

        if not segments:
            return False

        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                for i, seg in enumerate(segments, 1):
                    start = _format_ts(seg.get("start", 0.0))
                    end = _format_ts(seg.get("end", 0.0))
                    text = seg.get("text", "").strip()
                    f.write(f"{i}\n{start} --> {end}\n{text}\n\n")

            log_step("C12_subtitles.py", f"Saved {output_path}", "ok")
            return True
        except Exception as e:
            log_step("C12_subtitles.py", "Failed", "fail", str(e)[:60])
            return False

    def from_text(self, text, total_duration, output_path, chunk_words=8):
        """
        Auto-split long text into timed segments.

        Args:
            text:           full text
            total_duration: total video duration
            output_path:    srt file path
            chunk_words:    words per segment (default 8)

        Returns:
            True if successful
        """
        if not text or total_duration <= 0:
            return False

        words = text.split()
        chunks = [" ".join(words[i:i+chunk_words])
                  for i in range(0, len(words), chunk_words)]

        if not chunks:
            return False

        seg_dur = total_duration / len(chunks)
        segments = []
        for i, chunk in enumerate(chunks):
            segments.append({
                "start": i * seg_dur,
                "end": (i + 1) * seg_dur,
                "text": chunk,
            })

        return self.create_srt(segments, output_path)
