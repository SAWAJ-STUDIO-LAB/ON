# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      C6_background.py                          ║
# ║  📁 PATH:      .../fb_ig_story_video_generator/          ║
# ║                C_content/C6_background.py                ║
# ║  🎯 PURPOSE:   Background video (smooth zoompan)         ║
# ║  📖 FOLDER:    C_content                                 ║
# ╚══════════════════════════════════════════════════════════╝

"""
🎥 BACKGROUND MODULE (UPGRADED)
══════════════════════════════

🎯 Purpose:
   Islamic/nature background video fetch (1080x1920 portrait).

📖 Kya improve hua:
   ✅ Pehle: zoompan filter में d=1 — 1 frame पर zoom
   ✅ Ab: Smooth continuous zoom (d=1 with proper rate)
   ✅ Ab: Better crop math (no black bars)
   ✅ Ab: Better color grading (dark cinematic)
   ✅ Ab: Aspect ratio preserved with force_original_aspect_ratio
   ✅ Ab: Fallback gradient with animated colors
   ✅ Ab: CRF 20 (was 18) — smaller files

🎬 Video Queries:
   • islamic architecture night
   • mosque night
   • night sky stars
   • desert night
   • kaaba night

🎨 Effect:
   • Cinematic darken (contrast 1.10, brightness 0.02)
   • Vignette PI/5
   • Zoom slow (0.0004 per frame)
   • 1080x1920 final crop

📝 Note:
   zoompan rate 0.0004 × 25fps × 60s ≈ 0.6 zoom factor
   Perfect for subtle Ken Burns effect
"""

import os
import random
from A_core.A2_logger import (
    log_file_start,
    log_file_end,
    log_step,
    log_api,
)


# ═══════════════════════════════════════════════════════════
# ⚙️  CONSTANTS
# ═══════════════════════════════════════════════════════════

TARGET_W = 1080
TARGET_H = 1920

# ───── Color grading filter ─────
DARKEN_FILTER = (
    "eq=contrast=1.10:brightness=0.02:saturation=1.12,"
    "vignette=PI/5"
)

# ───── Scale + crop + zoom filter ─────
def _build_scale_filter() -> str:
    """
    Build FFmpeg filter for smooth background.
    
    Steps:
      1. Scale to fit 1080x1920 (preserve aspect)
      2. Crop to exact 1080x1920
      3. Apply smooth zoom (Ken Burns)
      4. Apply color grading
      5. Ensure SAR 1:1
    """
    return (
        # Scale to fit with overflow (avoids black bars)
        f"scale=1200:2140:force_original_aspect_ratio=increase,"
        # Crop center to exact target
        f"crop={TARGET_W}:{TARGET_H},"
        # Smooth zoom (Ken Burns effect)
        f"zoompan=z='min(zoom+0.0004,1.06)':d=1:"
        f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
        f"s={TARGET_W}x{TARGET_H},"
        # Ensure SAR 1:1 (no aspect ratio distortion)
        f"setsar=1,"
        # Color grading
        f"{DARKEN_FILTER}"
    )


# ═══════════════════════════════════════════════════════════
# 🎥 BACKGROUND CLASS
# ═══════════════════════════════════════════════════════════

class Background:
    """Fetch background video with multiple fallbacks."""
    
    # ─────────────────────────────────────────────────────
    # ① INIT
    # ─────────────────────────────────────────────────────
    def __init__(self, base):
        log_file_start("C6_background.py", "Background video fetch")
        self.base = base
        log_file_end("C6_background.py", "success", "Ready")
    
    # ─────────────────────────────────────────────────────
    # ② GET — main method
    # ─────────────────────────────────────────────────────
    def get(self, duration: float, outfile: str = "bg.mp4") -> str:
        """
        Fetch background video.
        
        Args:
            duration: Total duration needed (will add 5s buffer)
            outfile:  Output MP4 path
        
        Returns:
            outfile path
        """
        total_dur = duration + 5
        log_step("C6_background.py", f"get(dur={total_dur:.1f}s)", "ok")
        
        # ═══════════ Try Pexels ═══════════
        if os.environ.get("PEXELS_API_KEY"):
            if self._try_pexels(total_dur, outfile):
                return outfile
        
        # ═══════════ Try Pixabay ═══════════
        if os.environ.get("PIXABAY_API_KEY"):
            if self._try_pixabay(total_dur, outfile):
                return outfile
        
        # ═══════════ Fallback: generated gradient ═══════════
        self._generate_gradient(total_dur, outfile)
        return outfile
    
    # ─────────────────────────────────────────────────────
    # ③ PEXELS — best quality
    # ─────────────────────────────────────────────────────
    def _try_pexels(self, total_dur: float, outfile: str) -> bool:
        """Try Pexels API for portrait videos."""
        api_key = os.environ.get("PEXELS_API_KEY")
        if not api_key:
            return False
        
        queries = [
            "islamic architecture night",
            "mosque night",
            "night sky stars",
            "desert night",
            "kaaba night",
        ]
        
        # ───── Try 4 random queries ─────
        for q in random.sample(queries, min(4, len(queries))):
            try:
                log_step("C6_background.py", f"Pexels query: {q}", "info")
                
                r = self.base.session.get(
                    "https://api.pexels.com/videos/search",
                    params={
                        "query": q,
                        "orientation": "portrait",
                        "per_page": 6,
                        "size": "medium",
                    },
                    headers={"Authorization": api_key},
                    timeout=14,
                )
                
                if r.status_code != 200:
                    continue
                
                videos = r.json().get("videos", [])
                if not videos:
                    continue
                
                # ───── Pick best quality ─────
                video = random.choice(videos)
                files = sorted(
                    video.get("video_files", []),
                    key=lambda x: x.get("width", 0),
                    reverse=True,
                )
                
                if not files:
                    continue
                
                video_url = files[0].get("link")
                if not video_url:
                    continue
                
                # ───── Download ─────
                if not self.base.download(video_url, "tmp_bg.mp4", min_size=50000):
                    continue
                
                # ───── Process ─────
                self._process_video("tmp_bg.mp4", outfile, total_dur)
                
                self.base.api_status["Background"]["Pexels"] = "success"
                log_api("C6_background.py", "Pexels", "success", q)
                return True
            
            except Exception as e:
                log_step(
                    "C6_background.py",
                    f"Pexels err: {q}",
                    "fail",
                    str(e)[:50],
                )
                continue
        
        self.base.api_status["Background"]["Pexels"] = "failed"
        log_api("C6_background.py", "Pexels", "failed")
        return False
    
    # ─────────────────────────────────────────────────────
    # ④ PIXABAY — fallback
    # ─────────────────────────────────────────────────────
    def _try_pixabay(self, total_dur: float, outfile: str) -> bool:
        """Try Pixabay API for vertical videos."""
        api_key = os.environ.get("PIXABAY_API_KEY")
        if not api_key:
            return False
        
        try:
            log_step("C6_background.py", "Trying Pixabay", "info")
            
            r = self.base.session.get(
                "https://pixabay.com/api/videos/",
                params={
                    "key": api_key,
                    "q": "mosque night",
                    "orientation": "vertical",
                    "per_page": 10,
                    "safesearch": "true",
                },
                timeout=14,
            )
            
            if r.status_code != 200:
                log_api("C6_background.py", "Pixabay", "failed", f"HTTP {r.status_code}")
                return False
            
            hits = r.json().get("hits", [])
            if not hits:
                log_api("C6_background.py", "Pixabay", "failed", "no hits")
                return False
            
            hit = random.choice(hits)
            videos = hit.get("videos", {})
            
            # ───── Try large → medium → small ─────
            video_url = (
                videos.get("large", {}).get("url")
                or videos.get("medium", {}).get("url")
                or videos.get("small", {}).get("url")
            )
            
            if not video_url:
                return False
            
            # ───── Download ─────
            if not self.base.download(video_url, "tmp_bg.mp4", min_size=50000):
                return False
            
            # ───── Process ─────
            self._process_video("tmp_bg.mp4", outfile, total_dur)
            
            self.base.api_status["Background"]["Pixabay"] = "success"
            log_api("C6_background.py", "Pixabay", "success")
            return True
        
        except Exception as e:
            self.base.api_status["Background"]["Pixabay"] = "failed"
            log_api("C6_background.py", "Pixabay", "failed", str(e)[:60])
            return False
    
    # ─────────────────────────────────────────────────────
    # ⑤ PROCESS VIDEO
    # ─────────────────────────────────────────────────────
    def _process_video(self, infile: str, outfile: str, duration: float):
        """Process downloaded video with scale + zoom + color grade."""
        filter_str = _build_scale_filter()
        
        cmd = (
            f'ffmpeg -y '
            f'-stream_loop -1 -i "{infile}" '
            f'-vf "{filter_str}" '
            f'-t {duration:.2f} '
            f'-an '
            f'-c:v libx264 -preset veryfast -crf 20 '
            f'"{outfile}"'
        )
        
        self.base.run_cmd(cmd)
        
        # ───── Cleanup temp ─────
        try:
            if os.path.exists(infile):
                os.remove(infile)
        except Exception:
            pass
    
    # ─────────────────────────────────────────────────────
    # ⑥ GENERATE GRADIENT — last resort
    # ─────────────────────────────────────────────────────
    def _generate_gradient(self, duration: float, outfile: str):
        """Generate animated gradient as last resort."""
        log_step("C6_background.py", "Gradient fallback", "warn")
        
        # ───── Random dark colors ─────
        c0 = self._random_dark_hex()
        c1 = self._random_dark_hex()
        
        cmd = (
            f'ffmpeg -y '
            f'-f lavfi -i "gradients=s={TARGET_W}x{TARGET_H}:'
            f'c0=0x{c0}:c1=0x{c1}:speed=0.006" '
            f'-t {duration:.2f} '
            f'-c:v libx264 -preset veryfast -crf 20 '
            f'"{outfile}"'
        )
        
        self.base.run_cmd(cmd)
        
        self.base.api_status["Background"]["Generated-Gradient"] = "success (fallback)"
        log_api("C6_background.py", "Generated-Gradient", "fallback")
    
    # ─────────────────────────────────────────────────────
    # ⑦ HELPER: random dark hex color
    # ─────────────────────────────────────────────────────
    def _random_dark_hex(self) -> str:
        """Generate random dark color hex (RGB)."""
        r = random.randint(10, 30)
        g = random.randint(8, 25)
        b = random.randint(25, 55)
        return f"{r:02x}{g:02x}{b:02x}"


# ═══════════════════════════════════════════════════════════
# 🧪 QUICK TEST
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("🎥 Background Self-Test")
    print("=" * 50)
    print("Note: Full test requires network. Testing structure only.")
    print("\n✅ Background module loaded successfully!")
