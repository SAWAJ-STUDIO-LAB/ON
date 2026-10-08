"""
Code3 — Long Generator code transfer.
"""
import os

BASE = "sawajstudiobot/video_generator/fb_yt_long_video_generator"

FILES = {
    "A_core/__init__.py": '"""A_core package."""\n',
    "B_graphics/__init__.py": '"""B_graphics package."""\n',
    "C_content/__init__.py": '"""C_content package."""\n',
    "D_video/__init__.py": '"""D_video package."""\n',
    "E_audio/__init__.py": '"""E_audio package."""\n',
    "F_drive/__init__.py": '"""F_drive package."""\n',
    "G_entry/__init__.py": '"""G_entry package."""\n',
    "H_tests/__init__.py": '"""H_tests package."""\n',
    "__init__.py": '"""Long generator package."""\n',

    "A_core/A1_env_loader.py": '"""A1_env_loader.py"""\nimport os\n\n\ndef get_env(name, default=""):\n    return os.environ.get(name, default).strip()\n',
    "A_core/A6_print_logger.py": '"""A6_print_logger.py"""\nfrom datetime import datetime\n\n\ndef log(msg, level="INFO"):\n    ts = datetime.now().strftime("%H:%M:%S")\n    print(f"[{ts}] [{level}] {msg}", flush=True)\n',

    "C_content/C10_bullets.py": '"""C10_bullets.py"""\nfrom A_core.A9_log_step import log_step\n\n\nclass BulletGenerator:\n    def __init__(self, base, ai):\n        self.base = base\n        self.ai = ai\n\n    def generate(self, hindi, english, arabic=""):\n        log_step("C10_bullets.py", "generate()", "ok")\n        return {"hindi": [], "arabic": [], "english": []}\n',

    "C_content/C11_chapters.py": '"""C11_chapters.py"""\nfrom A_core.A9_log_step import log_step\n\n\nclass ChapterGenerator:\n    def build(self, section_durations):\n        log_step("C11_chapters.py", "build()", "ok")\n        chapters = []\n        current = 0.0\n        for title, dur in section_durations.items():\n            mins = int(current // 60)\n            secs = int(current % 60)\n            chapters.append({"time_str": f"{mins:02d}:{secs:02d}",\n                             "seconds": current, "title": title})\n            current += dur\n        return chapters\n\n    def format_list(self, chapters):\n        return [f"{c[\'time_str\']} - {c[\'title\']}" for c in chapters]\n',

    "C_content/C12_subtitles.py": '"""C12_subtitles.py"""\nimport os\nfrom A_core.A9_log_step import log_step\n\n\ndef _fmt(sec):\n    h = int(sec // 3600)\n    m = int((sec % 3600) // 60)\n    s = int(sec % 60)\n    ms = int((sec - int(sec)) * 1000)\n    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"\n\n\nclass SubtitleGenerator:\n    def create_srt(self, segments, output_path):\n        if not segments:\n            return False\n        try:\n            os.makedirs(os.path.dirname(output_path), exist_ok=True)\n            with open(output_path, "w", encoding="utf-8") as f:\n                for i, seg in enumerate(segments, 1):\n                    f.write(f"{i}\\n{_fmt(seg[\'start\'])} --> {_fmt(seg[\'end\'])}")\n                    f.write(f"\\n{seg[\'text\']}\\n\\n")\n            return True\n        except Exception:\n            return False\n\n    def from_text(self, text, total_duration, output_path, chunk_words=8):\n        if not text or total_duration <= 0:\n            return False\n        words = text.split()\n        chunks = [" ".join(words[i:i+chunk_words]) for i in range(0, len(words), chunk_words)]\n        if not chunks:\n            return False\n        seg_dur = total_duration / len(chunks)\n        segments = [{"start": i * seg_dur, "end": (i + 1) * seg_dur, "text": c}\n                    for i, c in enumerate(chunks)]\n        return self.create_srt(segments, output_path)\n',
}


def main():
    total = 0
    for rel_path, content in FILES.items():
        full = os.path.join(BASE, rel_path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w", encoding="utf-8") as f:
            f.write(content)
        total += 1
    print(f"🎉 Long: {total} files written!")


if __name__ == "__main__":
    main()
