"""
🎙️ gTTS
"""
import os


def generate_gtts(text, outfile, lang="hi"):
    try:
        from gtts import gTTS
        tts = gTTS(text=text, lang=lang, slow=False)
        tts.save(outfile)
        if os.path.exists(outfile) and os.path.getsize(outfile) > 1000:
            return True
    except Exception:
        pass
    return False
