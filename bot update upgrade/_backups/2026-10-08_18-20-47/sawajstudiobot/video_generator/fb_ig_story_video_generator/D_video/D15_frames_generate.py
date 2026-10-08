"""D15_frames_generate.py — Sirf frames."""
import os
import gc
import time
from PIL import Image, ImageDraw
from A_core.A9_log_step import log_step
from D_video.D3_intro_main import draw_intro
from D_video.D11_main_draw import draw_main
from D_video.D14_outro_main import draw_outro


def generate(voice_dur, has_logo, hindi, urdu, english,
             hadith_label="", out_dir="s_frames",
             intro_dur=2.0, outro_dur=2.0):
    fps = 25
    os.makedirs(out_dir, exist_ok=True)
    total = intro_dur + voice_dur + outro_dur
    count = int(total * fps)
    log_step("D15_frames_generate.py", f"Total {total:.1f}s ({count} frames)", "ok")
    canvas = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    start = time.time()
    try:
        for fi in range(count):
            t = fi / fps
            canvas.paste((0, 0, 0, 0), (0, 0, 1080, 1920))
            draw = ImageDraw.Draw(canvas)
            if t < intro_dur:
                draw_intro(canvas, draw, t, intro_dur, has_logo)
            elif t < intro_dur + voice_dur:
                mt = t - intro_dur
                draw_main(canvas, draw, mt, voice_dur, hindi, urdu,
                          english, hadith_label, has_logo)
            else:
                ot = t - (intro_dur + voice_dur)
                draw_outro(canvas, draw, ot, outro_dur, has_logo)
            canvas.convert("RGB").save(
                os.path.join(out_dir, f"frame_{fi:05d}.png"), "PNG")
            if fi > 0 and fi % 100 == 0:
                el = time.time() - start
                rate = fi / el if el > 0 else 0
                log_step("D15_frames_generate.py",
                         f"{fi}/{count}", "info", f"{rate:.1f} fps")
            if fi % 500 == 0:
                gc.collect()
    finally:
        try:
            canvas.close()
        except Exception:
            pass
        gc.collect()
    return total
