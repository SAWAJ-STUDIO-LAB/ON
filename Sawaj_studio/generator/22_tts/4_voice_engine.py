"""
🎙️ Voice Engine
"""
from .1_elevenlabs import generate_elevenlabs
from .2_edge_tts import generate_edge_tts
from .3_gtts import generate_gtts


def generate_voice(text, outfile):
    if generate_elevenlabs(text, outfile):
        return True
    if generate_edge_tts(text, outfile):
        return True
    if generate_gtts(text, outfile):
        return True
    return False
