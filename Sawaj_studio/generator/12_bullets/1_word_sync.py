"""
🔄 Word Sync
"""


def get_word_state(text, elapsed, total_dur):
    if not text:
        return {"word": "", "alpha": 0, "prev_alpha": 0, "next_alpha": 0}
    words = text.split()
    if not words:
        return {"word": "", "alpha": 0, "prev_alpha": 0, "next_alpha": 0}
    n = len(words)
    word_dur = max(total_dur / n, 0.1)
    idx = int(elapsed / word_dur)
    idx = max(0, min(idx, n - 1))
    progress = (elapsed / word_dur) - idx
    if progress < 0.3:
        current_alpha = progress / 0.3
        prev_alpha = 1 - (progress / 0.3)
    elif progress > 0.7:
        p = (progress - 0.7) / 0.3
        current_alpha = 1 - p
        prev_alpha = 0
    else:
        current_alpha = 1.0
        prev_alpha = 0.0
    return {
        "word": words[idx],
        "prev_word": words[idx - 1] if idx > 0 else None,
        "next_word": words[idx + 1] if idx < n - 1 else None,
        "alpha": current_alpha,
        "prev_alpha": prev_alpha,
        "next_alpha": 0,
        "idx": idx,
        "total": n,
    }
