"""D29_compose_verify.py — Sirf verify."""
import json
import subprocess


def verify(video_path):
    try:
        result = subprocess.run(
            f'ffprobe -v error -show_entries format=duration,size -of json "{video_path}"',
            shell=True, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            return {"error": "ffprobe failed"}
        data = json.loads(result.stdout)
        fmt = data.get("format", {})
        return {"duration": float(fmt.get("duration", 0)),
                "size": int(fmt.get("size", 0)),
                "size_mb": int(fmt.get("size", 0)) / 1024 / 1024}
    except Exception as e:
        return {"error": str(e)[:100]}
