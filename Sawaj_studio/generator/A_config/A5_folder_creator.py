# ═══════════════════════════════════════════════════════════
# 📄 FILE:      A5_folder_creator.py
# 🎯 PURPOSE:   Runtime folders create karna
# ═══════════════════════════════════════════════════════════

"""
📁 FOLDER CREATOR
══════════════════

🎯 Purpose:
   Runtime pe zaroori folders banana.

📖 Creates:
   • output/story
   • output/short
   • output/long
   • output/temp
   • output/logs
   • s_frames (story)
   • p_frames (short)
   • l_frames (long)
"""

import os

from A_config.A3_path_builder import (
    STORY_OUTPUT_DIR, SHORT_OUTPUT_DIR, LONG_OUTPUT_DIR,
    TEMP_DIR, LOGS_DIR, ensure_path
)


# ═══════════════════════════════════════════════════════════
# ① CREATE ALL
# ═══════════════════════════════════════════════════════════

def create_all_folders() -> dict:
    """
    Create all runtime folders.

    Returns:
        dict with folder paths
    """
    folders = {
        "story_output": ensure_path(STORY_OUTPUT_DIR),
        "short_output": ensure_path(SHORT_OUTPUT_DIR),
        "long_output": ensure_path(LONG_OUTPUT_DIR),
        "temp": ensure_path(TEMP_DIR),
        "logs": ensure_path(LOGS_DIR),
    }
    return folders


# ═══════════════════════════════════════════════════════════
# ② CREATE WORKER FOLDERS
# ═══════════════════════════════════════════════════════════

def create_worker_folders(worker: str) -> dict:
    """
    Create folders for specific worker.

    Args:
        worker: "story" | "short" | "long"

    Returns:
        dict with folder paths
    """
    folder_map = {
        "story": ("s_frames", STORY_OUTPUT_DIR),
        "short": ("p_frames", SHORT_OUTPUT_DIR),
        "long": ("l_frames", LONG_OUTPUT_DIR),
    }

    if worker not in folder_map:
        raise ValueError(f"Unknown worker: {worker}")

    frames_name, output_dir = folder_map[worker]

    return {
        "frames": ensure_path(frames_name),
        "final": ensure_path(os.path.join(output_dir, "final")),
        "temp": ensure_path(os.path.join(output_dir, "temp")),
    }


# ═══════════════════════════════════════════════════════════
# ③ QUICK TEST
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("📁 Folder Creator Self-Test")
    print("=" * 50)
    folders = create_all_folders()
    for k, v in folders.items():
        print(f"  ✅ {k}: {v}")

    worker_folders = create_worker_folders("story")
    for k, v in worker_folders.items():
        print(f"  ✅ story.{k}: {v}")

    print("✅ Done")# -*- coding: utf-8 -*-
