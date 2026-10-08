"""
🎙️ Edge TTS
"""
import asyncio
import os


async def _generate_edge(text, outfile, voice, rate, pitch, volume):
    import edge_tts
    communicate = edge_tts.Communicate(
        text=text, voice=voice, rate=rate, pitch=pitch, volume=volume)
    await communicate.save(outfile)


def generate_edge_tts(text, outfile,
                      voice="hi-IN-MadhurNeural",
                      rate="-7%", pitch="-2Hz", volume="+8%"):
    try:
        asyncio.run(asyncio.wait_for(
            _generate_edge(text, outfile, voice, rate, pitch, volume),
            timeout=120))
        if os.path.exists(outfile) and os.path.getsize(outfile) > 1000:
            return True
    except Exception:
        pass
    return False
