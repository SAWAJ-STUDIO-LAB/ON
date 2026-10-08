"""G15_pipeline_run.py — Sirf pipeline."""
import traceback
from A_core.A5_platform_checker import available_platforms
from A_core.A9_log_step import log_step
from A_core.A11_log_error import log_error
from G_entry.G1_step_init import run as s_init
from G_entry.G2_step_secrets import run as s_sec
from G_entry.G3_step_hadith import run as s_had
from G_entry.G4_step_translate import run as s_tr
from G_entry.G5_step_tts import run as s_tts
from G_entry.G6_step_music import run as s_mus
from G_entry.G7_step_background import run as s_bg
from G_entry.G8_step_logo import run as s_logo
from G_entry.G9_step_frames import run as s_frames
from G_entry.G10_step_compose import run as s_comp
from G_entry.G11_step_thumbnail import run as s_thumb
from G_entry.G12_step_drive import run as s_drive
from G_entry.G13_step_socials import run as s_soc
from G_entry.G14_step_cleanup import run as s_clean


def run_pipeline(base):
    try:
        s_init(base)
        s_sec(base)
        h = s_had(base)
        hindi = s_tr(base, h["english"])
        voice_dur = s_tts(base, hindi)
        s_mus(base, voice_dur)
        bg_file = s_bg(base, voice_dur)
        has_logo = s_logo()
        label = f"#{h['number']} · {h['collection']}"
        total = s_frames(voice_dur, has_logo, hindi, h.get("arabic", ""),
                         h["english"], label)
        final = s_comp(base, bg_file, total)
        s_thumb(hindi, h.get("arabic", ""), h["english"], label)
        s_drive(base, final)
        s_soc(final, hindi, h)
        s_clean()
        log_step("G15_pipeline_run.py", "Pipeline complete", "ok")
        return True
    except Exception as e:
        log_error("G15_pipeline_run.py", str(e), traceback.format_exc())
        raise
