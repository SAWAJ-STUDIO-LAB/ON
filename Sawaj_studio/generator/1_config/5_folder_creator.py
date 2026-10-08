"""
📁 Folder Creator
"""
import os


def create_all_folders():
    folders = ["output/story", "output/short", "output/long",
               "output/temp", "output/logs"]
    result = {}
    for f in folders:
        os.makedirs(f, exist_ok=True)
        result[f] = f
    return result


def create_worker_folders(worker):
    frames = {"story": "s_frames", "short": "p_frames", "long": "l_frames"}.get(worker, "s_frames")
    out = {"story": "output/story", "short": "output/short", "long": "output/long"}.get(worker, "output/story")
    os.makedirs(frames, exist_ok=True)
    os.makedirs(os.path.join(out, "final"), exist_ok=True)
    os.makedirs(os.path.join(out, "temp"), exist_ok=True)
    return {"frames": frames, "output": out}
