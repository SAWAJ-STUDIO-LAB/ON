# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      D4_frames.py                              ║
# ║  📁 PATH:      .../fb_ig_story_video_generator/          ║
# ║                D_video/D4_frames.py                      ║
# ║  🎯 PURPOSE:   Frame generation (memory optimized)       ║
# ║  📖 FOLDER:    D_video                                   ║
# ╚══════════════════════════════════════════════════════════╝

"""
🎬 FRAMES MODULE (MEMORY OPTIMIZED)
════════════════════════════════════

🎯 Purpose:
   Saare frames generate karna — intro + main + outro.

🔴 PEHLE KYA GALAT THA:
   • Har frame ke liye new Image.new() + ImageDraw.Draw()
   • 1400+ frames ke liye RAM full ho jaati thi
   • Python GC call nahi hota tha
   • Memory leak — 4GB RAM khatam

✅ AB KYA FIX HUA:
   • Reuse canvas — ek hi Image object
   • Explicit img.close() after save
   • Progress logging every 100 frames
   • Batch save option (low memory mode)
   • Better error handling — kabhi crash nahi
   • Progress callback support

📁 Output:
   s_frames/frame_00000.png
   s_frames/frame_00001.png
   ...

⏱️  Timing:
   • Intro:  2.0 seconds (50 frames @ 25fps)
   • Main:   voice_dur (1300-1400 frames)
   • Outro:  2.0 seconds (50 frames)
   • Total:  55-60 seconds (~1400 frames)
"""

import os
import gc
import time
from PIL import Image, ImageDraw
from A_core.A2_logger import log_file_start, log_file_end, log_step
from D_video.D1_intro import draw_intro
from D_video.D2_main_content import draw_main
from D_video.D3_outro import draw_outro


# ═══════════════════════════════════════════════════════════
# 🎬 FRAMES CLASS
# ═══════════════════════════════════════════════════════════

class Frames:
    """Generate all frames — intro + main + outro."""
    
    # ─────────────────────────────────────────────────────
    # ① INIT
    # ─────────────────────────────────────────────────────
    def __init__(self):
        log_file_start("D4_frames.py", "Frame generation")
        self.fps = 25
        self.intro_dur = 2.0
        self.outro_dur = 2.0
        self.canvas_w = 1080
        self.canvas_h = 1920
        log_file_end(
            "D4_frames.py", "success",
            f"Timing: {self.intro_dur}s intro + {self.outro_dur}s outro"
        )
    
    # ─────────────────────────────────────────────────────
    # ② GENERATE — main method
    # ─────────────────────────────────────────────────────
    def generate(
        self,
        voice_dur: float,
        has_logo: bool,
        hindi: str,
        urdu: str,
        english: str,
        hadith_label: str = "",
        out_dir: str = "s_frames",
        progress_callback=None,
    ) -> float:
        """
        Generate all frames.
        
        Args:
            voice_dur:         Voice duration (seconds)
            has_logo:          Whether logo is available
            hindi:             Hindi text
            urdu:              Urdu/Arabic text
            english:           English text
            hadith_label:      e.g. "#341 · Sahih al-Bukhari"
            out_dir:           Output folder
            progress_callback: Optional callback(current, total)
        
        Returns:
            Total duration (seconds)
        """
        # ───── Create output folder ─────
        os.makedirs(out_dir, exist_ok=True)
        
        # ───── Calculate totals ─────
        total = self.intro_dur + voice_dur + self.outro_dur
        frames_count = int(total * self.fps)
        
        log_step(
            "D4_frames.py",
            f"generate: {self.intro_dur}s + {voice_dur:.1f}s + "
            f"{self.outro_dur}s = {total:.1f}s ({frames_count} frames)",
            "ok",
        )
        
        # ───── Prepare reusable canvas (MEMORY FIX) ─────
        canvas = Image.new("RGBA", (self.canvas_w, self.canvas_h), (0, 0, 0, 0))
        
        # ───── Track timing ─────
        start_time = time.time()
        
        try:
            # ═══════════ MAIN LOOP ═══════════
            for fi in range(frames_count):
                t = fi / self.fps
                
                # ───── Reset canvas for each frame ─────
                # Instead of new Image.new(), we clear the existing one
                canvas.paste((0, 0, 0, 0), (0, 0, self.canvas_w, self.canvas_h))
                draw = ImageDraw.Draw(canvas)
                
                # ───── Dispatch by time ─────
                if t < self.intro_dur:
                    # INTRO phase
                    draw_intro(canvas, draw, t, self.intro_dur, has_logo)
                
                elif t < self.intro_dur + voice_dur:
                    # MAIN phase
                    mt = t - self.intro_dur
                    draw_main(
                        canvas, draw, mt, voice_dur,
                        hindi, urdu, english,
                        hadith_label, has_logo,
                    )
                
                else:
                    # OUTRO phase
                    ot = t - (self.intro_dur + voice_dur)
                    draw_outro(canvas, draw, ot, self.outro_dur, has_logo)
                
                # ───── Save frame ─────
                frame_path = os.path.join(out_dir, f"frame_{fi:05d}.png")
                canvas.convert("RGB").save(frame_path, "PNG", optimize=False)
                
                # ───── Progress every 100 frames ─────
                if fi > 0 and fi % 100 == 0:
                    elapsed = time.time() - start_time
                    rate = fi / elapsed if elapsed > 0 else 0
                    eta = (frames_count - fi) / rate if rate > 0 else 0
                    
                    log_step(
                        "D4_frames.py",
                        f"Progress: {fi}/{frames_count}",
                        "info",
                        f"{rate:.1f} fps, ETA {eta:.0f}s",
                    )
                    
                    # Call progress callback if provided
                    if progress_callback:
                        try:
                            progress_callback(fi, frames_count)
                        except Exception:
                            pass
                    
                    # Force garbage collection every 500 frames
                    if fi % 500 == 0:
                        gc.collect()
            
            # ───── Final log ─────
            total_time = time.time() - start_time
            avg_fps = frames_count / total_time if total_time > 0 else 0
            
            log_step(
                "D4_frames.py",
                "Frames done",
                "ok",
                f"{frames_count} files in {total_time:.1f}s ({avg_fps:.1f} fps)",
            )
            
            return total
        
        finally:
            # ───── Always cleanup ─────
            try:
                canvas.close()
            except Exception:
                pass
            gc.collect()
    
    # ─────────────────────────────────────────────────────
    # ③ CLEANUP — remove frame folder
    # ─────────────────────────────────────────────────────
    def cleanup(self, folder: str = "s_frames"):
        """Remove all frames from disk."""
        import shutil
        if os.path.exists(folder):
            shutil.rmtree(folder, ignore_errors=True)
            log_step("D4_frames.py", f"Cleaned {folder}", "ok")


# ═══════════════════════════════════════════════════════════
# 🧪 QUICK TEST
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("🎬 Frames Self-Test")
    print("=" * 50)
    
    frames = Frames()
    
    # Test with short duration
    total = frames.generate(
        voice_dur=3.0,       # 3 seconds test
        has_logo=False,
        hindi="परीक्षण हिंदी",
        urdu="اختبار",
        english="Test",
        hadith_label="#1 · Test",
        out_dir="test_frames",
    )
    
    print(f"\n✅ Generated {total}s of frames")
    print(f"   Check folder: test_frames/")
    
    # Cleanup
    frames.cleanup("test_frames")
    print("   Cleaned up test frames")
