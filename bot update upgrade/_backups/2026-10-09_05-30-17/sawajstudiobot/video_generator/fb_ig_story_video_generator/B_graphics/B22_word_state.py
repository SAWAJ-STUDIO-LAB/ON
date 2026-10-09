"""B22_word_state.py — Sirf word state."""
from B_graphics.B23_word_empty import empty
from B_graphics.B24_word_alphas import calc

FADE_IN_END, FADE_OUT_START = 0.30, 0.70


def get_state(text, elapsed, total_dur):
    if not text:
        return empty()
    words = text.split()
    if not words:
        return empty()
    n = len(words)
    if total_dur <= 0:
        total_dur = 1.0
    wd = total_dur / n
    idx_f = elapsed / wd
    idx = int(idx_f)
    if idx < 0:
        idx, progress = 0, 0.0
    elif idx >= n:
        idx, progress = n - 1, 1.0
    else:
        progress = idx_f - idx
    current = words[idx]
    prev_w = words[idx-1] if idx > 0 else None
    next_w = words[idx+1] if idx < n-1 else None
    ca, pa, na = calc(progress)
    return {"word": current, "prev_word": prev_w, "next_word": next_w,
            "alpha": ca, "prev_alpha": pa, "next_alpha": na,
            "progress": progress, "idx": idx, "total": n}
