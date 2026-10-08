"""B30_bullets_sync.py — Sirf sync info."""
from B_graphics.B22_word_state import get_state


def get_info(hindi, urdu, english, elapsed, voice_dur):
    return {
        "elapsed": round(elapsed, 2), "voice_dur": round(voice_dur, 2),
        "progress_pct": round(100 * elapsed / max(voice_dur, 0.01), 1),
        "hindi": {"word_count": len(hindi.split()) if hindi else 0,
                  "current_idx": get_state(hindi, elapsed, voice_dur)["idx"]},
        "urdu": {"word_count": len(urdu.split()) if urdu else 0,
                 "current_idx": get_state(urdu, elapsed, voice_dur)["idx"]},
        "english": {"word_count": len(english.split()) if english else 0,
                    "current_idx": get_state(english, elapsed, voice_dur)["idx"]},
    }
