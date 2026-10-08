#!/usr/bin/env python3
"""
📄 FILE:      content.py
📁 PATH:      scripts/content.py
🎯 PURPOSE:   Content + Workers + Uploaders
"""

import os

ROOT = "Sawaj_studio"
CODE = {}

# ═══════════════════════════════════════════════════════════
# 📖 19_HADITH
# ═══════════════════════════════════════════════════════════

CODE[f"{ROOT}/generator/19_hadith/__init__.py"] = '"""Hadith Module"""\n'

CODE[f"{ROOT}/generator/19_hadith/1_hadith_fetch.py"] = '''"""
📖 Hadith Fetch
"""
import requests


def fetch_hadith(base_url, book_eng, number):
    try:
        url = base_url + "/editions/" + book_eng + "/" + str(number) + ".json"
        r = requests.get(url, timeout=15)
        if r.status_code != 200:
            return None
        data = r.json()
        hadiths = data.get("hadiths", [])
        if not hadiths:
            return None
        text = hadiths[0].get("text", "").strip()
        if len(text) < 30:
            return None
        return {"text": text, "number": hadiths[0].get("hadithnumber", number)}
    except Exception:
        return None
'''

CODE[f"{ROOT}/generator/19_hadith/2_word_filter.py"] = '''"""
🔍 Word Filter
"""


def count_words(text):
    if not text:
        return 0
    return len(text.split())


def matches_range(text, min_words, max_words):
    n = count_words(text)
    return min_words <= n <= max_words


def filter_hadith(text, ideal_min=50, ideal_max=100):
    n = count_words(text)
    if ideal_min <= n <= ideal_max:
        return "ideal"
    elif 30 <= n <= 150:
        return "fallback"
    return None
'''

CODE[f"{ROOT}/generator/19_hadith/3_arabic_fetch.py"] = '''"""
🇸🇦 Arabic Fetch
"""
import requests


def fetch_arabic(base_url, book_ara, number):
    try:
        url = base_url + "/editions/" + book_ara + "/" + str(number) + ".json"
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            return ""
        data = r.json()
        hadiths = data.get("hadiths", [])
        if not hadiths:
            return ""
        return hadiths[0].get("text", "").strip()
    except Exception:
        return ""
'''

CODE[f"{ROOT}/generator/19_hadith/4_fallback.py"] = '''"""
🔄 Fallback
"""
FALLBACK_HADITH = {
    "collection": "Sahih al-Bukhari",
    "number": "1",
    "english": ("Actions are judged by intentions, and every person will get "
                "what they intended."),
    "arabic": "إنما الأعمال بالنيات وإنما لكل امرئ ما نوى",
}


def get_fallback():
    return FALLBACK_HADITH.copy()
'''

CODE[f"{ROOT}/generator/19_hadith/5_api_rotator.py"] = '''"""
🔄 API Rotator
"""
API_BASES = [
    "https://cdn.jsdelivr.net/gh/fawazahmed0/hadith-api@1",
    "https://raw.githubusercontent.com/fawazahmed0/hadith-api/1",
]


def get_bases(custom_url=None):
    bases = []
    if custom_url:
        bases.append(custom_url.rstrip("/"))
    bases.extend(API_BASES)
    return bases


def rotate_bases(bases, current_idx):
    if not bases:
        return None
    return bases[current_idx % len(bases)]
'''

# ═══════════════════════════════════════════════════════════
# 🤖 20_AI_PROVIDER
# ═══════════════════════════════════════════════════════════

CODE[f"{ROOT}/generator/20_ai_provider/__init__.py"] = '"""AI Provider Module"""\n'

CODE[f"{ROOT}/generator/20_ai_provider/1_openrouter.py"] = '''"""
🌐 OpenRouter
"""
import os
import requests


def call_openrouter(prompt, max_tokens=800):
    key = os.environ.get("OPENROUTER_API_KEY", "").strip() or \\
          os.environ.get("OPENROUTER_API_KEY_AI", "").strip()
    if not key:
        return None
    try:
        r = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": "Bearer " + key,
                     "Content-Type": "application/json"},
            json={"model": "openai/gpt-4o-mini",
                  "messages": [{"role": "user", "content": prompt}],
                  "max_tokens": max_tokens},
            timeout=40)
        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"].strip()
    except Exception:
        pass
    return None
'''

CODE[f"{ROOT}/generator/20_ai_provider/2_groq.py"] = '''"""
⚡ Groq
"""
import os
import requests


def call_groq(prompt, max_tokens=800):
    key = os.environ.get("GROQ_API_KEY", "").strip() or \\
          os.environ.get("GROQ_API_KEY_AI", "").strip()
    if not key:
        return None
    try:
        r = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": "Bearer " + key,
                     "Content-Type": "application/json"},
            json={"model": "llama-3.3-70b-versatile",
                  "messages": [{"role": "user", "content": prompt}],
                  "max_tokens": max_tokens},
            timeout=40)
        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"].strip()
    except Exception:
        pass
    return None
'''

CODE[f"{ROOT}/generator/20_ai_provider/3_gemini.py"] = '''"""
✨ Gemini
"""
import os
import requests


def call_gemini(prompt, max_tokens=800):
    key = os.environ.get("GEMINI_API_KEY", "").strip() or \\
          os.environ.get("GEMINI_API_KEY_AI", "").strip()
    if not key:
        return None
    try:
        url = ("https://generativelanguage.googleapis.com/v1beta/"
               "models/gemini-1.5-flash:generateContent?key=" + key)
        r = requests.post(url,
                          json={"contents": [{"parts": [{"text": prompt}]}]},
                          timeout=40)
        if r.status_code == 200:
            return r.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
    except Exception:
        pass
    return None
'''

CODE[f"{ROOT}/generator/20_ai_provider/4_mistral.py"] = '''"""
🌪️ Mistral
"""
import os
import requests


def call_mistral(prompt, max_tokens=800):
    key = os.environ.get("MISTRAL_API_KEY", "").strip() or \\
          os.environ.get("MISTRAL_API_KEY_AI", "").strip()
    if not key:
        return None
    try:
        r = requests.post(
            "https://api.mistral.ai/v1/chat/completions",
            headers={"Authorization": "Bearer " + key,
                     "Content-Type": "application/json"},
            json={"model": "mistral-small-latest",
                  "messages": [{"role": "user", "content": prompt}],
                  "max_tokens": max_tokens},
            timeout=40)
        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"].strip()
    except Exception:
        pass
    return None
'''

CODE[f"{ROOT}/generator/20_ai_provider/5_cerebras.py"] = '''"""
🧠 Cerebras
"""
import os
import requests


def call_cerebras(prompt, max_tokens=800):
    key = (os.environ.get("CEREBRAS_API_KEY", "").strip() or
           os.environ.get("CEREBRAS_API_KEY_AI", "").strip() or
           os.environ.get("CELEBRAS_API_KEY_AI", "").strip())
    if not key:
        return None
    try:
        r = requests.post(
            "https://api.cerebras.ai/v1/chat/completions",
            headers={"Authorization": "Bearer " + key,
                     "Content-Type": "application/json"},
            json={"model": "llama3.1-8b",
                  "messages": [{"role": "user", "content": prompt}],
                  "max_tokens": max_tokens},
            timeout=40)
        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"].strip()
    except Exception:
        pass
    return None
'''

CODE[f"{ROOT}/generator/20_ai_provider/6_cohere.py"] = '''"""
🌊 Cohere
"""
import os
import requests


def call_cohere(prompt, max_tokens=800):
    key = os.environ.get("COHERE_API_KEY", "").strip() or \\
          os.environ.get("COHERE_API_KEY_AI", "").strip()
    if not key:
        return None
    try:
        r = requests.post(
            "https://api.cohere.com/v1/chat",
            headers={"Authorization": "Bearer " + key,
                     "Content-Type": "application/json"},
            json={"model": "command-r-plus", "message": prompt},
            timeout=40)
        if r.status_code == 200:
            return r.json()["text"].strip()
    except Exception:
        pass
    return None
'''

CODE[f"{ROOT}/generator/20_ai_provider/7_fallback_chain.py"] = '''"""
🔗 Fallback Chain
"""
from .1_openrouter import call_openrouter
from .2_groq import call_groq
from .3_gemini import call_gemini
from .4_mistral import call_mistral
from .5_cerebras import call_cerebras
from .6_cohere import call_cohere


def call_ai(prompt, max_tokens=800):
    providers = [
        ("OpenRouter", call_openrouter),
        ("Groq", call_groq),
        ("Gemini", call_gemini),
        ("Mistral", call_mistral),
        ("Cerebras", call_cerebras),
        ("Cohere", call_cohere),
    ]
    for name, func in providers:
        try:
            result = func(prompt, max_tokens)
            if result:
                return result
        except Exception:
            continue
    return None
'''

# ═══════════════════════════════════════════════════════════
# 🌍 21_TRANSLATOR
# ═══════════════════════════════════════════════════════════

CODE[f"{ROOT}/generator/21_translator/__init__.py"] = '"""Translator Module"""\n'

CODE[f"{ROOT}/generator/21_translator/1_deepl.py"] = '''"""
🌍 DeepL
"""
import os
import requests


def translate_deepl(text, target="HI"):
    key = os.environ.get("DEEPL_API_KEY", "").strip()
    if not key:
        return None
    try:
        r = requests.post(
            "https://api-free.deepl.com/v2/translate",
            headers={"Authorization": "DeepL-Auth-Key " + key},
            data={"text": text, "target_lang": target},
            timeout=60)
        if r.status_code == 200:
            return r.json()["translations"][0]["text"]
    except Exception:
        pass
    return None
'''

CODE[f"{ROOT}/generator/21_translator/2_ai_translator.py"] = '''"""
🤖 AI Translator
"""
from ..20_ai_provider.7_fallback_chain import call_ai


def translate_with_ai(text):
    prompt = ("Translate this English Islamic text to accurate Hindi. "
              "Only translation, nothing else.\\n\\n" + text)
    return call_ai(prompt, max_tokens=1500)
'''

CODE[f"{ROOT}/generator/21_translator/3_hindi_target.py"] = '''"""
🇮🇳 Hindi Target
"""
HINDI_FALLBACK = "अमल का दारोमदार नीयतों पर है।"


def get_hindi_fallback():
    return HINDI_FALLBACK
'''

CODE[f"{ROOT}/generator/21_translator/4_fallback.py"] = '''"""
🔄 Fallback
"""
from .1_deepl import translate_deepl
from .2_ai_translator import translate_with_ai
from .3_hindi_target import get_hindi_fallback


def translate_to_hindi(text):
    result = translate_deepl(text)
    if result:
        return result
    result = translate_with_ai(text)
    if result:
        return result
    return get_hindi_fallback()
'''

# ═══════════════════════════════════════════════════════════
# 🎙️ 22_TTS
# ═══════════════════════════════════════════════════════════

CODE[f"{ROOT}/generator/22_tts/__init__.py"] = '"""TTS Module"""\n'

CODE[f"{ROOT}/generator/22_tts/1_elevenlabs.py"] = '''"""
🎙️ ElevenLabs
"""
import os
import requests


def generate_elevenlabs(text, outfile):
    key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    if not key:
        return False
    try:
        url = "https://api.elevenlabs.io/v1/text-to-speech/pNInz6obpgDQGcFmaJgB"
        r = requests.post(url,
                          headers={"Accept": "audio/mpeg",
                                   "Content-Type": "application/json",
                                   "xi-api-key": key},
                          json={"text": text,
                                "model_id": "eleven_multilingual_v2",
                                "voice_settings": {
                                    "stability": 0.42,
                                    "similarity_boost": 0.82}},
                          timeout=90)
        if r.status_code == 200 and len(r.content) > 5000:
            with open(outfile, "wb") as f:
                f.write(r.content)
            return True
    except Exception:
        pass
    return False
'''

CODE[f"{ROOT}/generator/22_tts/2_edge_tts.py"] = '''"""
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
'''

CODE[f"{ROOT}/generator/22_tts/3_gtts.py"] = '''"""
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
'''

CODE[f"{ROOT}/generator/22_tts/4_voice_engine.py"] = '''"""
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
'''

CODE[f"{ROOT}/generator/22_tts/5_async_runner.py"] = '''"""
🎬 Async Runner
"""
import asyncio


def run_async(coro, timeout=120):
    try:
        return asyncio.run(asyncio.wait_for(coro, timeout=timeout))
    except Exception:
        return None
'''

CODE[f"{ROOT}/generator/22_tts/6_size_validator.py"] = '''"""
📏 Size Validator
"""
import os


def is_valid_audio(path, min_size=1000):
    if not os.path.exists(path):
        return False
    return os.path.getsize(path) >= min_size


def get_size_kb(path):
    if not os.path.exists(path):
        return 0
    return os.path.getsize(path) // 1024
'''

# ═══════════════════════════════════════════════════════════
# 🎵 23_MUSIC
# ═══════════════════════════════════════════════════════════

CODE[f"{ROOT}/generator/23_music/__init__.py"] = '"""Music Module"""\n'

CODE[f"{ROOT}/generator/23_music/1_freesound.py"] = '''"""
🎵 Freesound
"""
import os
import random
import requests


def fetch_freesound(outfile):
    key = os.environ.get("FREESOUND_API_KEY", "").strip()
    if not key:
        return False
    try:
        r = requests.get(
            "https://freesound.org/apiv2/search/text/",
            params={"query": "soft ambient meditation islamic peaceful",
                    "filter": "duration:[60 TO 400]",
                    "fields": "id,name,previews",
                    "page_size": 8, "token": key},
            timeout=14)
        if r.status_code != 200:
            return False
        results = r.json().get("results", [])
        if not results:
            return False
        track = random.choice(results)
        url = (track.get("previews", {}).get("preview-hq-mp3")
               or track.get("previews", {}).get("preview-lq-mp3"))
        if not url:
            return False
        r2 = requests.get(url, timeout=35)
        if r2.status_code == 200 and len(r2.content) > 100000:
            with open(outfile, "wb") as f:
                f.write(r2.content)
            return True
    except Exception:
        pass
    return False
'''

CODE[f"{ROOT}/generator/23_music/2_pixabay_cdn.py"] = '''"""
🎵 Pixabay CDN
"""
import requests
CDN_URLS = [
    "https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3?filename=soft-ambient-112191.mp3",
    "https://cdn.pixabay.com/download/audio/2022/03/24/audio_4f3b5c5e3d.mp3?filename=peaceful-background-112194.mp3",
]


def fetch_pixabay(outfile):
    for url in CDN_URLS:
        try:
            r = requests.get(url, timeout=35)
            if r.status_code == 200 and len(r.content) > 100000:
                with open(outfile, "wb") as f:
                    f.write(r.content)
                return True
        except Exception:
            continue
    return False
'''

CODE[f"{ROOT}/generator/23_music/3_bensound.py"] = '''"""
🎵 Bensound
"""
import requests
BENSOUND_URLS = [
    "https://www.bensound.com/bensound-music/bensound-relaxing.mp3",
    "https://www.bensound.com/bensound-music/bensound-slowmotion.mp3",
]


def fetch_bensound(outfile):
    for url in BENSOUND_URLS:
        try:
            r = requests.get(url, timeout=35)
            if r.status_code == 200 and len(r.content) > 100000:
                with open(outfile, "wb") as f:
                    f.write(r.content)
                return True
        except Exception:
            continue
    return False
'''

CODE[f"{ROOT}/generator/23_music/4_generated_sine.py"] = '''"""
🎵 Generated Sine
"""
import subprocess


def generate_sine(outfile, duration=60):
    try:
        cmd = ('ffmpeg -y -f lavfi -i "sine=frequency=110:duration=' + str(duration) + '" '
               '-f lavfi -i "sine=frequency=165:duration=' + str(duration) + '" '
               '-filter_complex "[0:a][1:a]amix=inputs=2:duration=longest,'
               'volume=0.12,afade=t=in:st=0:d=2.5,'
               'afade=t=out:st=' + str(duration - 10) + ':d=6" ' + outfile)
        subprocess.run(cmd, shell=True, check=True, timeout=120)
        return True
    except Exception:
        return False
'''

CODE[f"{ROOT}/generator/23_music/5_volume_mixer.py"] = '''"""
🎵 Volume Mixer
"""
import subprocess


def apply_volume_and_fade(infile, outfile, duration=60,
                          volume=0.20, fade_in=2, fade_out=5):
    try:
        fade_out_start = duration - fade_out
        cmd = ('ffmpeg -y -stream_loop -1 -i "' + infile + '" -af '
               '"volume=' + str(volume) + ','
               'afade=t=in:st=0:d=' + str(fade_in) + ','
               'afade=t=out:st=' + str(fade_out_start) + ':d=' + str(fade_out) + '" '
               '-t ' + str(duration) + ' "' + outfile + '"')
        subprocess.run(cmd, shell=True, check=True, timeout=180)
        return True
    except Exception:
        return False
'''

# ═══════════════════════════════════════════════════════════
# 🎬 24_BACKGROUND
# ═══════════════════════════════════════════════════════════

CODE[f"{ROOT}/generator/24_background/__init__.py"] = '"""Background Module"""\n'

CODE[f"{ROOT}/generator/24_background/1_pexels.py"] = '''"""
🎬 Pexels
"""
import os
import random
import requests


def fetch_pexels(outfile, duration=60):
    key = os.environ.get("PEXELS_API_KEY", "").strip()
    if not key:
        return False
    queries = ["islamic architecture night", "mosque night",
               "night sky stars", "desert night"]
    for q in random.sample(queries, 3):
        try:
            r = requests.get(
                "https://api.pexels.com/videos/search",
                params={"query": q, "orientation": "portrait",
                        "per_page": 6, "size": "medium"},
                headers={"Authorization": key}, timeout=14)
            if r.status_code != 200:
                continue
            videos = r.json().get("videos", [])
            if not videos:
                continue
            v = random.choice(videos)
            files = sorted(v.get("video_files", []),
                           key=lambda x: x.get("width", 0), reverse=True)
            if not files:
                continue
            url = files[0].get("link")
            if not url:
                continue
            r2 = requests.get(url, timeout=35)
            if r2.status_code == 200 and len(r2.content) > 50000:
                with open(outfile, "wb") as f:
                    f.write(r2.content)
                return True
        except Exception:
            continue
    return False
'''

CODE[f"{ROOT}/generator/24_background/2_pixabay.py"] = '''"""
🎬 Pixabay
"""
import os
import random
import requests


def fetch_pixabay(outfile):
    key = os.environ.get("PIXABAY_API_KEY", "").strip()
    if not key:
        return False
    try:
        r = requests.get(
            "https://pixabay.com/api/videos/",
            params={"key": key, "q": "mosque night",
                    "orientation": "vertical", "per_page": 10,
                    "safesearch": "true"},
            timeout=14)
        if r.status_code != 200:
            return False
        hits = r.json().get("hits", [])
        if not hits:
            return False
        hit = random.choice(hits)
        videos = hit.get("videos", {})
        url = (videos.get("large", {}).get("url")
               or videos.get("medium", {}).get("url")
               or videos.get("small", {}).get("url"))
        if not url:
            return False
        r2 = requests.get(url, timeout=35)
        if r2.status_code == 200 and len(r2.content) > 50000:
            with open(outfile, "wb") as f:
                f.write(r2.content)
            return True
    except Exception:
        pass
    return False
'''

CODE[f"{ROOT}/generator/24_background/3_gradient_fallback.py"] = '''"""
🎨 Gradient Fallback
"""
import random
import subprocess


def generate_gradient(outfile, duration=60, width=1080, height=1920):
    try:
        c0 = "%02x%02x%02x" % (random.randint(10,30), random.randint(8,25), random.randint(25,55))
        c1 = "%02x%02x%02x" % (random.randint(10,30), random.randint(8,25), random.randint(25,55))
        cmd = ('ffmpeg -y -f lavfi -i "gradients=s=' + str(width) + 'x' + str(height) + ':'
               'c0=0x' + c0 + ':c1=0x' + c1 + ':speed=0.006" '
               '-t ' + str(duration) + ' -c:v libx264 -preset veryfast "' + outfile + '"')
        subprocess.run(cmd, shell=True, check=True, timeout=180)
        return True
    except Exception:
        return False
'''

CODE[f"{ROOT}/generator/24_background/4_zoompan.py"] = '''"""
🔍 Zoompan
"""


def build_zoompan_filter(target_w=1080, target_h=1920):
    return ('scale=1200:2140:force_original_aspect_ratio=increase,'
            'crop=' + str(target_w) + ':' + str(target_h) + ','
            "zoompan=z='min(zoom+0.0004,1.06)':d=1:"
            "x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
            's=' + str(target_w) + 'x' + str(target_h) + ',setsar=1')
'''

CODE[f"{ROOT}/generator/24_background/5_color_grade.py"] = '''"""
🎨 Color Grade
"""


def get_darken_filter():
    return "eq=contrast=1.10:brightness=0.02:saturation=1.12,vignette=PI/5"
'''

# ═══════════════════════════════════════════════════════════
# 🖼️ 25_LOGO_PROCESSOR
# ═══════════════════════════════════════════════════════════

CODE[f"{ROOT}/generator/25_logo_processor/__init__.py"] = '"""Logo Processor Module"""\n'

CODE[f"{ROOT}/generator/25_logo_processor/1_logo_finder.py"] = '''"""
🔍 Logo Finder
"""
import os
LOGO_PATHS = ["logo.png", "logo.jpg", "assets/logo.png",
              "assets/logo.jpg", "../../video_requirement/logo.png"]


def find_logo():
    for p in LOGO_PATHS:
        if os.path.exists(p):
            return p
    return None
'''

CODE[f"{ROOT}/generator/25_logo_processor/2_logo_resize.py"] = '''"""
📐 Logo Resize
"""
from PIL import Image


def resize_logo(path, max_width=400):
    img = Image.open(path).convert("RGBA")
    if img.width > max_width:
        ratio = max_width / img.width
        img = img.resize((max_width, int(img.height * ratio)),
                         Image.Resampling.LANCZOS)
    return img
'''

CODE[f"{ROOT}/generator/25_logo_processor/3_border_add.py"] = '''"""
🔲 Border Add
"""
from PIL import Image, ImageDraw


def add_border(img, border=12, bottom=26):
    w = img.width + border * 2
    h = img.height + border + bottom
    canvas = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle([0, 0, w - 1, h - 1],
                   outline=(212, 175, 55, 255), width=border)
    draw.rectangle([border, border, w - border - 1, h - bottom - 1],
                   outline=(255, 215, 100, 200), width=2)
    draw.rectangle([0, h - bottom, w - 1, h - 1], fill=(20, 15, 8, 245))
    canvas.paste(img, (border, border), img)
    return canvas
'''

CODE[f"{ROOT}/generator/25_logo_processor/4_glow_effect.py"] = '''"""
💫 Glow Effect
"""
from PIL import Image, ImageFilter


def add_glow(canvas):
    glow = canvas.filter(ImageFilter.GaussianBlur(6))
    return Image.alpha_composite(glow, canvas)
'''

CODE[f"{ROOT}/generator/25_logo_processor/5_avatar_save.py"] = '''"""
💾 Avatar Save
"""
from .1_logo_finder import find_logo
from .2_logo_resize import resize_logo
from .3_border_add import add_border
from .4_glow_effect import add_glow


def create_avatar(outfile="avatar.png"):
    logo_path = find_logo()
    if not logo_path:
        return False
    try:
        img = resize_logo(logo_path)
        canvas = add_border(img)
        final = add_glow(canvas)
        final.save(outfile)
        return True
    except Exception:
        return False
'''

# ═══════════════════════════════════════════════════════════
# 🖼️ 26_THUMBNAIL
# ═══════════════════════════════════════════════════════════

CODE[f"{ROOT}/generator/26_thumbnail/__init__.py"] = '"""Thumbnail Module"""\n'

CODE[f"{ROOT}/generator/26_thumbnail/1_thumb_draw.py"] = '''"""
🖼️ Thumb Draw
"""
from PIL import Image, ImageDraw


def create_thumbnail(hindi, arabic, english, hadith_label, outfile):
    W, H = 1080, 1920
    img = Image.new("RGB", (W, H), (18, 14, 8))
    draw = ImageDraw.Draw(img)
    for y in range(0, H, 4):
        r = int(18 + 30 * (y / H))
        g = int(14 + 20 * (y / H))
        b = int(8 + 15 * (y / H))
        draw.rectangle([0, y, W, y + 4], fill=(r, g, b))
    draw.rectangle([20, 20, W - 20, H - 20],
                   outline=(212, 175, 55), width=6)
    draw.rectangle([30, 30, W - 30, H - 30],
                   outline=(255, 215, 100), width=2)
    img.save(outfile, "JPEG", quality=92)
    return outfile
'''

CODE[f"{ROOT}/generator/26_thumbnail/2_gradient_bg.py"] = '''"""
🌈 Gradient Background
"""


def draw_gradient(draw, w, h):
    for y in range(0, h, 4):
        r = int(18 + 30 * (y / h))
        g = int(14 + 20 * (y / h))
        b = int(8 + 15 * (y / h))
        draw.rectangle([0, y, w, y + 4], fill=(r, g, b))
'''

CODE[f"{ROOT}/generator/26_thumbnail/3_title_text.py"] = '''"""
📝 Title Text
"""


def draw_title(draw, w, title="HADITH", y=300):
    draw.text(((w - 300) // 2, y), title, fill=(255, 240, 200))
'''

CODE[f"{ROOT}/generator/26_thumbnail/4_label_text.py"] = '''"""
🏷️ Label Text
"""


def draw_label(draw, w, label, y=100):
    if not label:
        return
    draw.text(((w - 300) // 2, y), label, fill=(230, 200, 130))
'''

CODE[f"{ROOT}/generator/26_thumbnail/5_lang_lines.py"] = '''"""
🌍 Language Lines
"""


def draw_lang_lines(draw, hindi, arabic, english, y_start=780):
    y = y_start
    if hindi:
        draw.ellipse([100, y + 20, 130, y + 50], fill=(240, 130, 200))
        draw.text((160, y), hindi[:30], fill=(255, 255, 255))
        y += 130
    if arabic:
        draw.ellipse([100, y + 20, 130, y + 50], fill=(90, 170, 255))
        draw.text((160, y), arabic[:30], fill=(255, 255, 255))
        y += 130
    if english:
        draw.ellipse([100, y + 20, 130, y + 50], fill=(255, 110, 110))
        draw.text((160, y), english[:40], fill=(255, 255, 255))
'''

CODE[f"{ROOT}/generator/26_thumbnail/6_logo_overlay.py"] = '''"""
🖼️ Logo Overlay
"""
import os
from PIL import Image


def overlay_logo(img, logo_path="avatar.png"):
    if not os.path.exists(logo_path):
        return img
    try:
        logo = Image.open(logo_path).convert("RGBA").resize(
            (260, 110), Image.Resampling.LANCZOS)
        img.paste(logo, ((img.width - 260) // 2, 1580), logo)
    except Exception:
        pass
    return img
'''

CODE[f"{ROOT}/generator/26_thumbnail/7_cta_text.py"] = '''"""
📢 CTA Text
"""


def draw_cta(draw, w, cta="Follow @sawajstudio", y=1780):
    draw.text(((w - 300) // 2, y), cta, fill=(255, 230, 180))
'''

# ═══════════════════════════════════════════════════════════
# 👷 WORKER_STORY
# ═══════════════════════════════════════════════════════════

CODE[f"{ROOT}/generator/worker_story/__init__.py"] = '"""Story Worker"""\n'
CODE[f"{ROOT}/generator/worker_story/1_pipeline/__init__.py"] = '"""Pipeline"""\n'
CODE[f"{ROOT}/generator/worker_story/1_pipeline/1_pipeline_steps.py"] = '''"""
📋 Pipeline Steps
"""
STEPS = ["1_fetch_hadith", "2_translate", "3_tts", "4_music", "5_background",
         "6_logo", "7_frames", "8_compose", "9_thumbnail", "10_drive",
         "11_social", "12_cleanup"]


def get_steps():
    return STEPS.copy()
'''
CODE[f"{ROOT}/generator/worker_story/1_pipeline/2_step_orchestrator.py"] = '''"""
🎯 Step Orchestrator
"""
from .1_pipeline_steps import get_steps


def run_pipeline(state):
    results = []
    for step in get_steps():
        try:
            results.append({"step": step, "ok": True})
        except Exception as e:
            results.append({"step": step, "ok": False, "error": str(e)})
    return results
'''
CODE[f"{ROOT}/generator/worker_story/2_config/__init__.py"] = '"""Config"""\n'
CODE[f"{ROOT}/generator/worker_story/2_config/1_story_settings.py"] = '''"""
⚙️ Story Settings
"""
WORKER_NAME = "story"
DURATION_TARGET = "50-60s"
WORDS_MIN = 50
WORDS_MAX = 100
MUSIC_DURATION = 60
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
FRAMES_FOLDER = "s_frames"
OUTPUT_FOLDER = "output/story"
PLATFORMS = ["facebook", "instagram"]
'''
CODE[f"{ROOT}/generator/worker_story/2_config/2_story_template.json"] = '{}\n'
CODE[f"{ROOT}/generator/worker_story/3_intro/__init__.py"] = '"""Intro"""\n'
CODE[f"{ROOT}/generator/worker_story/3_intro/1_intro_draw.py"] = '''"""
🎬 Intro Draw
"""


def draw_intro(img, draw, t, duration, has_logo):
    alpha = min(1.0, t / 0.5)
    p = t / duration if duration > 0 else 0
    if p > 0.5:
        draw.text((420, 980), "HADITH OF THE DAY",
                  fill=(230, 200, 130, int(255 * alpha)))
'''
CODE[f"{ROOT}/generator/worker_story/4_main_content/__init__.py"] = '"""Main"""\n'
CODE[f"{ROOT}/generator/worker_story/4_main_content/1_main_draw.py"] = '''"""
📝 Main Draw
"""


def draw_main(img, draw, mt, voice_dur, hindi, urdu, english,
              hadith_label, has_logo):
    alpha = min(1.0, mt / 0.5)
    if hadith_label:
        draw.text((60, 180), hadith_label,
                  fill=(230, 200, 130, int(255 * alpha)))
'''
CODE[f"{ROOT}/generator/worker_story/5_outro/__init__.py"] = '"""Outro"""\n'
CODE[f"{ROOT}/generator/worker_story/5_outro/1_outro_draw.py"] = '''"""
🎬 Outro Draw
"""


def draw_outro(img, draw, t, duration, has_logo):
    alpha = min(1.0, t / 0.5)
    draw.text((350, 780), "JazakAllah Khair",
              fill=(230, 200, 130, int(255 * alpha)))
'''
CODE[f"{ROOT}/generator/worker_story/6_frames/__init__.py"] = '"""Frames"""\n'
CODE[f"{ROOT}/generator/worker_story/6_frames/1_frame_generator.py"] = '''"""
🖼️ Frame Generator
"""
import os
from PIL import Image, ImageDraw


def generate_frames(voice_dur, has_logo, hindi, urdu, english,
                    hadith_label, out_dir="s_frames"):
    os.makedirs(out_dir, exist_ok=True)
    fps = 25
    total = 2.0 + voice_dur + 2.0
    frames_count = int(total * fps)
    for fi in range(frames_count):
        img = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        img.save(out_dir + "/frame_" + str(fi).zfill(5) + ".png")
    return total
'''
CODE[f"{ROOT}/generator/worker_story/7_composer/__init__.py"] = '"""Composer"""\n'
CODE[f"{ROOT}/generator/worker_story/7_composer/1_final_compose.py"] = '''"""
🎞️ Final Compose
"""
import os
import subprocess


def compose(bg, frames_dir, voice, total,
            outfile="output/story/final/Final_Story.mp4"):
    os.makedirs(os.path.dirname(outfile), exist_ok=True)
    cmd = ('ffmpeg -y -i ' + bg + ' -framerate 25 '
           '-i ' + frames_dir + '/frame_%05d.png '
           '-i ' + voice + ' '
           '-filter_complex "[0:v][1:v]overlay=0:0:shortest=1,'
           'format=yuv420p[outv]" '
           '-map "[outv]" -map 2:a '
           '-c:v libx264 -preset veryfast -crf 20 -b:v 4M '
           '-c:a aac -b:a 192k -t ' + str(total) + ' '
           '-movflags +faststart ' + outfile)
    subprocess.run(cmd, shell=True, check=True, timeout=1800)
    return outfile
'''
CODE[f"{ROOT}/generator/worker_story/8_run/__init__.py"] = '"""Run"""\n'
CODE[f"{ROOT}/generator/worker_story/8_run/1_main.py"] = '''"""
🚀 Story Worker Main
"""
import sys


def main():
    print("=" * 60)
    print("📖 STORY WORKER")
    print("=" * 60)
    try:
        from ..1_pipeline.1_pipeline_steps import get_steps
        from ..2_config.1_story_settings import WORKER_NAME, DURATION_TARGET
        print("✅ Worker: " + WORKER_NAME)
        print("✅ Duration: " + DURATION_TARGET)
        print("✅ Steps: " + str(len(get_steps())))
    except Exception as e:
        print("❌ Error: " + str(e))
        sys.exit(1)


if __name__ == "__main__":
    main()
'''

# ═══════════════════════════════════════════════════════════
# 👷 WORKER_SHORT
# ═══════════════════════════════════════════════════════════

CODE[f"{ROOT}/generator/worker_short/__init__.py"] = '"""Short Worker"""\n'
CODE[f"{ROOT}/generator/worker_short/1_pipeline/__init__.py"] = '"""Pipeline"""\n'
CODE[f"{ROOT}/generator/worker_short/1_pipeline/1_pipeline_steps.py"] = '''"""
📋 Pipeline Steps
"""
STEPS = ["1_fetch_hadith", "2_translate", "3_meaning", "4_tts_hadith",
         "5_tts_meaning", "6_music", "7_background", "8_logo", "9_frames",
         "10_compose", "11_thumbnail", "12_drive", "13_social", "14_cleanup"]


def get_steps():
    return STEPS.copy()
'''
CODE[f"{ROOT}/generator/worker_short/1_pipeline/2_step_orchestrator.py"] = '''"""
🎯 Step Orchestrator
"""
from .1_pipeline_steps import get_steps


def run_pipeline(state):
    results = []
    for step in get_steps():
        try:
            results.append({"step": step, "ok": True})
        except Exception as e:
            results.append({"step": step, "ok": False, "error": str(e)})
    return results
'''
CODE[f"{ROOT}/generator/worker_short/2_config/__init__.py"] = '"""Config"""\n'
CODE[f"{ROOT}/generator/worker_short/2_config/1_short_settings.py"] = '''"""
⚙️ Short Settings
"""
WORKER_NAME = "short"
DURATION_TARGET = "1-3 min"
WORDS_MIN = 150
WORDS_MAX = 400
MUSIC_DURATION = 200
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
FRAMES_FOLDER = "p_frames"
OUTPUT_FOLDER = "output/short"
PLATFORMS = ["facebook", "instagram", "youtube"]
'''
CODE[f"{ROOT}/generator/worker_short/2_config/2_short_template.json"] = '{}\n'
CODE[f"{ROOT}/generator/worker_short/3_intro/__init__.py"] = '"""Intro"""\n'
CODE[f"{ROOT}/generator/worker_short/3_intro/1_intro_draw.py"] = '''"""
🎬 Intro Draw
"""


def draw_intro(img, draw, t, duration, has_logo):
    alpha = min(1.0, t / 0.5)
    p = t / duration if duration > 0 else 0
    if p > 0.5:
        draw.text((400, 980), "Islamic Shorts",
                  fill=(230, 200, 130, int(255 * alpha)))
'''
CODE[f"{ROOT}/generator/worker_short/4_main_content/__init__.py"] = '"""Main"""\n'
CODE[f"{ROOT}/generator/worker_short/4_main_content/1_main_draw.py"] = '''"""
📝 Main Draw
"""


def draw_main(img, draw, mt, voice_dur, hindi, urdu, english,
              hadith_label, has_logo):
    alpha = min(1.0, mt / 0.5)
    if hadith_label:
        draw.text((60, 180), hadith_label,
                  fill=(230, 200, 130, int(255 * alpha)))
'''
CODE[f"{ROOT}/generator/worker_short/5_outro/__init__.py"] = '"""Outro"""\n'
CODE[f"{ROOT}/generator/worker_short/5_outro/1_outro_draw.py"] = '''"""
🎬 Outro Draw
"""


def draw_outro(img, draw, t, duration, has_logo):
    alpha = min(1.0, t / 0.5)
    draw.text((350, 780), "JazakAllah Khair",
              fill=(230, 200, 130, int(255 * alpha)))
'''
CODE[f"{ROOT}/generator/worker_short/6_frames/__init__.py"] = '"""Frames"""\n'
CODE[f"{ROOT}/generator/worker_short/6_frames/1_frame_generator.py"] = '''"""
🖼️ Frame Generator
"""
import os
from PIL import Image, ImageDraw


def generate_frames(voice_dur, has_logo, hindi, urdu, english,
                    hadith_label, out_dir="p_frames"):
    os.makedirs(out_dir, exist_ok=True)
    fps = 25
    total = 2.0 + voice_dur + 2.0
    frames_count = int(total * fps)
    for fi in range(frames_count):
        img = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        img.save(out_dir + "/frame_" + str(fi).zfill(5) + ".png")
    return total
'''
CODE[f"{ROOT}/generator/worker_short/7_composer/__init__.py"] = '"""Composer"""\n'
CODE[f"{ROOT}/generator/worker_short/7_composer/1_final_compose.py"] = '''"""
🎞️ Final Compose
"""
import os
import subprocess


def compose(bg, frames_dir, voice, total,
            outfile="output/short/final/Final_Short.mp4"):
    os.makedirs(os.path.dirname(outfile), exist_ok=True)
    cmd = ('ffmpeg -y -i ' + bg + ' -framerate 25 '
           '-i ' + frames_dir + '/frame_%05d.png '
           '-i ' + voice + ' '
           '-filter_complex "[0:v][1:v]overlay=0:0:shortest=1,'
           'format=yuv420p[outv]" '
           '-map "[outv]" -map 2:a '
           '-c:v libx264 -preset veryfast -crf 18 -b:v 6M '
           '-c:a aac -b:a 192k -t ' + str(total) + ' '
           '-movflags +faststart ' + outfile)
    subprocess.run(cmd, shell=True, check=True, timeout=1800)
    return outfile
'''
CODE[f"{ROOT}/generator/worker_short/8_run/__init__.py"] = '"""Run"""\n'
CODE[f"{ROOT}/generator/worker_short/8_run/1_main.py"] = '''"""
🚀 Short Worker Main
"""
import sys


def main():
    print("=" * 60)
    print("🎬 SHORT WORKER")
    print("=" * 60)
    try:
        from ..1_pipeline.1_pipeline_steps import get_steps
        from ..2_config.1_short_settings import WORKER_NAME, DURATION_TARGET
        print("✅ Worker: " + WORKER_NAME)
        print("✅ Duration: " + DURATION_TARGET)
        print("✅ Steps: " + str(len(get_steps())))
    except Exception as e:
        print("❌ Error: " + str(e))
        sys.exit(1)


if __name__ == "__main__":
    main()
'''

# ═══════════════════════════════════════════════════════════
# 👷 WORKER_LONG
# ═══════════════════════════════════════════════════════════

CODE[f"{ROOT}/generator/worker_long/__init__.py"] = '"""Long Worker"""\n'
CODE[f"{ROOT}/generator/worker_long/1_pipeline/__init__.py"] = '"""Pipeline"""\n'
CODE[f"{ROOT}/generator/worker_long/1_pipeline/1_pipeline_steps.py"] = '''"""
📋 Pipeline Steps
"""
STEPS = ["1_fetch_hadith", "2_translate", "3_tashreeh", "4_bullets",
         "5_tts_hadith", "6_tts_tashreeh", "7_tts_bullets", "8_concat_voice",
         "9_music", "10_background", "11_logo", "12_frames", "13_compose",
         "14_thumbnail", "15_subtitles", "16_chapters", "17_drive",
         "18_social", "19_cleanup"]


def get_steps():
    return STEPS.copy()
'''
CODE[f"{ROOT}/generator/worker_long/1_pipeline/2_step_orchestrator.py"] = '''"""
🎯 Step Orchestrator
"""
from .1_pipeline_steps import get_steps


def run_pipeline(state):
    results = []
    for step in get_steps():
        try:
            results.append({"step": step, "ok": True})
        except Exception as e:
            results.append({"step": step, "ok": False, "error": str(e)})
    return results
'''
CODE[f"{ROOT}/generator/worker_long/2_config/__init__.py"] = '"""Config"""\n'
CODE[f"{ROOT}/generator/worker_long/2_config/1_long_settings.py"] = '''"""
⚙️ Long Settings
"""
WORKER_NAME = "long"
DURATION_TARGET = "5-15 min"
WORDS_MIN = 400
WORDS_MAX = 1800
MUSIC_DURATION = 900
VIDEO_WIDTH = 1920
VIDEO_HEIGHT = 1080
FRAMES_FOLDER = "l_frames"
OUTPUT_FOLDER = "output/long"
PLATFORMS = ["facebook", "youtube"]
'''
CODE[f"{ROOT}/generator/worker_long/2_config/2_long_template.json"] = '{}\n'
CODE[f"{ROOT}/generator/worker_long/3_intro/__init__.py"] = '"""Intro"""\n'
CODE[f"{ROOT}/generator/worker_long/3_intro/1_intro_draw.py"] = '''"""
🎬 Intro Draw
"""


def draw_intro(img, draw, t, duration, has_logo):
    alpha = min(1.0, t / 0.7)
    p = t / duration if duration > 0 else 0
    if p > 0.5:
        draw.text((700, 720), "HADITH OF THE DAY",
                  fill=(230, 200, 130, int(255 * alpha)))
'''
CODE[f"{ROOT}/generator/worker_long/4_main_content/__init__.py"] = '"""Main"""\n'
CODE[f"{ROOT}/generator/worker_long/4_main_content/1_main_draw.py"] = '''"""
📝 Main Draw
"""


def draw_main(img, draw, mt, voice_dur, sections, hadith_label, has_logo):
    alpha = min(1.0, mt / 0.5)
    if hadith_label:
        draw.text((60, 60), hadith_label,
                  fill=(230, 200, 130, int(255 * alpha)))
'''
CODE[f"{ROOT}/generator/worker_long/5_outro/__init__.py"] = '"""Outro"""\n'
CODE[f"{ROOT}/generator/worker_long/5_outro/1_outro_draw.py"] = '''"""
🎬 Outro Draw
"""


def draw_outro(img, draw, t, duration, has_logo):
    alpha = min(1.0, t / 0.7)
    draw.text((700, 300), "JazakAllah Khair",
              fill=(230, 200, 130, int(255 * alpha)))
'''
CODE[f"{ROOT}/generator/worker_long/6_frames/__init__.py"] = '"""Frames"""\n'
CODE[f"{ROOT}/generator/worker_long/6_frames/1_frame_generator.py"] = '''"""
🖼️ Frame Generator
"""
import os
from PIL import Image, ImageDraw


def generate_frames(voice_dur, has_logo, sections,
                    hadith_label, out_dir="l_frames"):
    os.makedirs(out_dir, exist_ok=True)
    fps = 25
    total = 3.0 + voice_dur + 3.0
    frames_count = int(total * fps)
    for fi in range(frames_count):
        img = Image.new("RGBA", (1920, 1080), (0, 0, 0, 255))
        draw = ImageDraw.Draw(img)
        img.save(out_dir + "/frame_" + str(fi).zfill(5) + ".png")
    return total
'''
CODE[f"{ROOT}/generator/worker_long/7_composer/__init__.py"] = '"""Composer"""\n'
CODE[f"{ROOT}/generator/worker_long/7_composer/1_final_compose.py"] = '''"""
🎞️ Final Compose
"""
import os
import subprocess


def compose(bg, frames_dir, voice, total,
            outfile="output/long/final/Final_Long.mp4"):
    os.makedirs(os.path.dirname(outfile), exist_ok=True)
    cmd = ('ffmpeg -y -i ' + bg + ' -framerate 25 '
           '-i ' + frames_dir + '/frame_%05d.png '
           '-i ' + voice + ' '
           '-filter_complex "[0:v]scale=1920:1080,setsar=1[bgv];'
           '[bgv][1:v]overlay=0:0:shortest=1,format=yuv420p[outv]" '
           '-map "[outv]" -map 2:a '
           '-c:v libx264 -preset medium -crf 20 -b:v 4M '
           '-c:a aac -b:a 192k -t ' + str(total) + ' '
           '-movflags +faststart ' + outfile)
    subprocess.run(cmd, shell=True, check=True, timeout=2400)
    return outfile
'''
CODE[f"{ROOT}/generator/worker_long/8_run/__init__.py"] = '"""Run"""\n'
CODE[f"{ROOT}/generator/worker_long/8_run/1_main.py"] = '''"""
🚀 Long Worker Main
"""
import sys


def main():
    print("=" * 60)
    print("🎥 LONG WORKER")
    print("=" * 60)
    try:
        from ..1_pipeline.1_pipeline_steps import get_steps
        from ..2_config.1_long_settings import WORKER_NAME, DURATION_TARGET
        print("✅ Worker: " + WORKER_NAME)
        print("✅ Duration: " + DURATION_TARGET)
        print("✅ Steps: " + str(len(get_steps())))
    except Exception as e:
        print("❌ Error: " + str(e))
        sys.exit(1)


if __name__ == "__main__":
    main()
'''

# ═══════════════════════════════════════════════════════════
# 📺 UPLOADERS
# ═══════════════════════════════════════════════════════════

CODE[f"{ROOT}/uploader/__init__.py"] = '"""Uploader Package"""\n'

# ─── YouTube ───
CODE[f"{ROOT}/uploader/1_youtube_upload/__init__.py"] = '"""YouTube Upload"""\n'
CODE[f"{ROOT}/uploader/1_youtube_upload/1_auth/__init__.py"] = '"""Auth"""\n'
CODE[f"{ROOT}/uploader/1_youtube_upload/1_auth/1_oauth.py"] = '''"""
🔐 YouTube OAuth
"""
import os


def get_credentials():
    from google.oauth2.credentials import Credentials
    return Credentials(
        None,
        refresh_token=os.environ.get("YOUTUBE_REFRESH_TOKEN"),
        client_id=os.environ.get("YOUTUBE_CLIENT_ID"),
        client_secret=os.environ.get("YOUTUBE_CLIENT_SECRET"),
        token_uri="https://oauth2.googleapis.com/token")


def get_youtube_client():
    from googleapiclient.discovery import build
    creds = get_credentials()
    return build("youtube", "v3", credentials=creds, cache_discovery=False)
'''
CODE[f"{ROOT}/uploader/1_youtube_upload/2_client/__init__.py"] = '"""Client"""\n'
CODE[f"{ROOT}/uploader/1_youtube_upload/2_client/1_client_builder.py"] = '''"""
🛠️ YouTube Client Builder
"""
from ..1_auth.1_oauth import get_youtube_client


def build_client():
    try:
        return get_youtube_client()
    except Exception:
        return None
'''
CODE[f"{ROOT}/uploader/1_youtube_upload/3_short/__init__.py"] = '"""Short"""\n'
CODE[f"{ROOT}/uploader/1_youtube_upload/3_short/1_short_uploader.py"] = '''"""
📺 YouTube Short Uploader
"""


def upload_short(video_path, title="", description="", tags=None):
    try:
        from googleapiclient.http import MediaFileUpload
        from ..2_client.1_client_builder import build_client
        yt = build_client()
        if not yt:
            return False
        body = {
            "snippet": {
                "title": title[:100], "description": description,
                "tags": tags or ["Shorts", "Hadith", "Islamic"],
                "categoryId": "22",
            },
            "status": {"privacyStatus": "public",
                       "selfDeclaredMadeForKids": False},
        }
        req = yt.videos().insert(
            part="snippet,status", body=body,
            media_body=MediaFileUpload(video_path, chunksize=-1,
                                       resumable=True,
                                       mimetype="video/mp4"))
        response = None
        while response is None:
            _, response = req.next_chunk()
        return bool(response.get("id"))
    except Exception:
        return False
'''
CODE[f"{ROOT}/uploader/1_youtube_upload/4_long/__init__.py"] = '"""Long"""\n'
CODE[f"{ROOT}/uploader/1_youtube_upload/4_long/1_long_uploader.py"] = '''"""
📺 YouTube Long Uploader
"""


def upload_long(video_path, title="", description="", tags=None,
                chapters=None):
    try:
        from googleapiclient.http import MediaFileUpload
        from ..2_client.1_client_builder import build_client
        yt = build_client()
        if not yt:
            return False
        if chapters:
            description += "\\n\\n⏱️ Timestamps:\\n" + "\\n".join(chapters)
        body = {
            "snippet": {
                "title": title[:100], "description": description,
                "tags": tags or ["Hadith", "Long Hadith", "Islamic"],
                "categoryId": "22",
            },
            "status": {"privacyStatus": "public",
                       "selfDeclaredMadeForKids": False},
        }
        req = yt.videos().insert(
            part="snippet,status", body=body,
            media_body=MediaFileUpload(video_path, chunksize=-1,
                                       resumable=True,
                                       mimetype="video/mp4"))
        response = None
        while response is None:
            _, response = req.next_chunk()
        return bool(response.get("id"))
    except Exception:
        return False
'''
CODE[f"{ROOT}/uploader/1_youtube_upload/5_thumbnail/__init__.py"] = '"""Thumb"""\n'
CODE[f"{ROOT}/uploader/1_youtube_upload/5_thumbnail/1_thumbnail_set.py"] = '''"""
🖼️ YouTube Thumbnail Set
"""


def set_thumbnail(video_id, image_path):
    try:
        from ..2_client.1_client_builder import build_client
        yt = build_client()
        if not yt:
            return False
        yt.thumbnails().set(videoId=video_id,
                            media_body=image_path).execute()
        return True
    except Exception:
        return False
'''
CODE[f"{ROOT}/uploader/1_youtube_upload/6_playlist/__init__.py"] = '"""Playlist"""\n'
CODE[f"{ROOT}/uploader/1_youtube_upload/6_playlist/1_playlist_add.py"] = '''"""
📋 YouTube Playlist Add
"""
import os


def add_to_playlist(video_id):
    try:
        from ..2_client.1_client_builder import build_client
        playlist_id = os.environ.get("DAILY_HADEES_YT_PLAYLIST_ID", "").strip()
        if not playlist_id:
            return False
        yt = build_client()
        if not yt:
            return False
        yt.playlistItems().insert(
            part="snippet",
            body={"snippet": {
                "playlistId": playlist_id,
                "resourceId": {"kind": "youtube#video", "videoId": video_id}}}).execute()
        return True
    except Exception:
        return False
'''
CODE[f"{ROOT}/uploader/1_youtube_upload/7_chapters/__init__.py"] = '"""Chapters"""\n'
CODE[f"{ROOT}/uploader/1_youtube_upload/7_chapters/1_chapters_add.py"] = '''"""
⏱️ YouTube Chapters Add
"""


def format_chapters(chapters):
    if not chapters:
        return ""
    lines = ["⏱️ Timestamps:"]
    for c in chapters:
        lines.append(c)
    return "\\n".join(lines)


def build_chapters(section_durations):
    chapters = []
    current = 0.0
    for title, dur in section_durations.items():
        mins = int(current // 60)
        secs = int(current % 60)
        chapters.append("%02d:%02d - %s" % (mins, secs, title))
        current += dur
    return chapters
'''

# ─── Facebook ───
CODE[f"{ROOT}/uploader/2_facebook_upload/__init__.py"] = '"""Facebook Upload"""\n'
CODE[f"{ROOT}/uploader/2_facebook_upload/1_auth/__init__.py"] = '"""Auth"""\n'
CODE[f"{ROOT}/uploader/2_facebook_upload/1_auth/1_auth.py"] = '''"""
🔐 Facebook Auth
"""
import os


def get_fb_credentials():
    token = (os.environ.get("FACEBOOK_META_TOKEN", "").strip() or
             os.environ.get("FACEBOOK_INSTAGRAM_META_TOKEN", "").strip())
    page_id = os.environ.get("FACEBOOK_PAGE_ID", "").strip()
    return token, page_id


def has_fb_credentials():
    token, page_id = get_fb_credentials()
    return bool(token and page_id)
'''
CODE[f"{ROOT}/uploader/2_facebook_upload/2_story/__init__.py"] = '"""FB Story"""\n'
CODE[f"{ROOT}/uploader/2_facebook_upload/2_story/1_story_uploader.py"] = '''"""
📖 Facebook Story Upload
"""
import os
import requests


def upload_story(video_path):
    try:
        from ..1_auth.1_auth import get_fb_credentials
        token, page_id = get_fb_credentials()
        if not token or not page_id:
            return False
        f_size = os.path.getsize(video_path)
        session = requests.Session()
        start = session.post(
            "https://graph.facebook.com/v21.0/" + page_id + "/video_stories",
            data={"upload_phase": "start", "file_size": f_size,
                  "access_token": token}, timeout=30).json()
        v_id = start.get("video_id")
        v_url = start.get("upload_url")
        if not v_id or not v_url:
            return False
        with open(video_path, "rb") as f:
            session.post(v_url,
                         headers={"Authorization": "OAuth " + token,
                                  "offset": "0", "file_size": str(f_size)},
                         data=f.read(), timeout=180)
        finish = session.post(
            "https://graph.facebook.com/v21.0/" + page_id + "/video_stories",
            data={"upload_phase": "finish", "video_id": v_id,
                  "access_token": token}, timeout=30).json()
        return bool(finish.get("success") or finish.get("post_id"))
    except Exception:
        return False
'''
CODE[f"{ROOT}/uploader/2_facebook_upload/3_short/__init__.py"] = '"""FB Short"""\n'
CODE[f"{ROOT}/uploader/2_facebook_upload/3_short/1_short_uploader.py"] = '''"""
📘 Facebook Short Upload
"""
import requests


def upload_short(video_path, caption=""):
    try:
        from ..1_auth.1_auth import get_fb_credentials
        token, page_id = get_fb_credentials()
        if not token or not page_id:
            return False
        with open(video_path, "rb") as f:
            res = requests.post(
                "https://graph.facebook.com/v21.0/" + page_id + "/videos",
                data={"access_token": token, "description": caption,
                      "published": "true"},
                files={"source": f}, timeout=1800).json()
        return bool(res.get("id"))
    except Exception:
        return False
'''
CODE[f"{ROOT}/uploader/2_facebook_upload/4_long/__init__.py"] = '"""FB Long"""\n'
CODE[f"{ROOT}/uploader/2_facebook_upload/4_long/1_long_uploader.py"] = '''"""
📘 Facebook Long Upload
"""
import requests


def upload_long(video_path, caption=""):
    try:
        from ..1_auth.1_auth import get_fb_credentials
        token, page_id = get_fb_credentials()
        if not token or not page_id:
            return False
        with open(video_path, "rb") as f:
            res = requests.post(
                "https://graph.facebook.com/v21.0/" + page_id + "/videos",
                data={"access_token": token, "description": caption,
                      "published": "true"},
                files={"source": f}, timeout=3600).json()
        return bool(res.get("id"))
    except Exception:
        return False
'''
CODE[f"{ROOT}/uploader/2_facebook_upload/5_video_stories/__init__.py"] = '"""FB Video Stories"""\n'
CODE[f"{ROOT}/uploader/2_facebook_upload/5_video_stories/1_video_stories.py"] = '''"""
📹 Facebook Video Stories
"""
import os
import requests


def upload_video_story(video_path):
    try:
        from ..1_auth.1_auth import get_fb_credentials
        token, page_id = get_fb_credentials()
        if not token or not page_id:
            return False
        f_size = os.path.getsize(video_path)
        session = requests.Session()
        start = session.post(
            "https://graph.facebook.com/v21.0/" + page_id + "/video_stories",
            data={"upload_phase": "start", "file_size": f_size,
                  "access_token": token}, timeout=30).json()
        return bool(start.get("video_id"))
    except Exception:
        return False
'''

# ─── Instagram ───
CODE[f"{ROOT}/uploader/3_instagram_upload/__init__.py"] = '"""Instagram Upload"""\n'
CODE[f"{ROOT}/uploader/3_instagram_upload/1_auth/__init__.py"] = '"""Auth"""\n'
CODE[f"{ROOT}/uploader/3_instagram_upload/1_auth/1_auth.py"] = '''"""
🔐 Instagram Auth
"""
import os


def get_ig_credentials():
    token = os.environ.get("FACEBOOK_INSTAGRAM_META_TOKEN", "").strip()
    ig_id = os.environ.get("INSTAGRAM_BUSINESS_ACCOUNT_ID", "").strip()
    return token, ig_id


def has_ig_credentials():
    token, ig_id = get_ig_credentials()
    return bool(token and ig_id)
'''
CODE[f"{ROOT}/uploader/3_instagram_upload/2_story/__init__.py"] = '"""IG Story"""\n'
CODE[f"{ROOT}/uploader/3_instagram_upload/2_story/1_story_uploader.py"] = '''"""
📖 Instagram Story Upload
"""
import os
import time
import requests


def upload_story(video_path):
    try:
        from ..1_auth.1_auth import get_ig_credentials
        token, ig_id = get_ig_credentials()
        if not token or not ig_id:
            return False
        f_size = os.path.getsize(video_path)
        session = requests.Session()
        cont = session.post(
            "https://graph.facebook.com/v21.0/" + ig_id + "/media",
            data={"media_type": "STORIES", "upload_type": "resumable",
                  "access_token": token}, timeout=40).json()
        c_id = cont.get("id")
        if not c_id:
            return False
        upload_url = (cont.get("uri")
                      or "https://rupload.facebook.com/ig-api-upload/v21.0/" + c_id)
        with open(video_path, "rb") as f:
            video_bytes = f.read()
        session.post(upload_url,
                     headers={"Authorization": "OAuth " + token,
                              "offset": "0", "file_size": str(f_size),
                              "Content-Type": "application/octet-stream"},
                     data=video_bytes, timeout=180)
        for _ in range(40):
            time.sleep(5)
            st = session.get(
                "https://graph.facebook.com/v21.0/" + c_id,
                params={"fields": "status_code", "access_token": token},
                timeout=15).json()
            if st.get("status_code") == "FINISHED":
                break
            if st.get("status_code") == "ERROR":
                return False
        pub = session.post(
            "https://graph.facebook.com/v21.0/" + ig_id + "/media_publish",
            data={"creation_id": c_id, "access_token": token},
            timeout=20).json()
        return bool(pub.get("id"))
    except Exception:
        return False
'''

CODE[f"{ROOT}/uploader/3_instagram_upload/3_reel/__init__.py"] = '"""IG Reel"""\n'
CODE[f"{ROOT}/uploader/3_instagram_upload/3_reel/1_reel_uploader.py"] = '''"""
🎬 Instagram Reel Upload
"""
import time
import requests


def upload_reel(video_url, caption=""):
    try:
        from ..1_auth.1_auth import get_ig_credentials
        token, ig_id = get_ig_credentials()
        if not token or not ig_id or not video_url:
            return False
        session = requests.Session()
        cont = session.post(
            "https://graph.facebook.com/v21.0/" + ig_id + "/media",
            data={"media_type": "REELS", "video_url": video_url,
                  "caption": caption, "access_token": token},
            timeout=30).json()
        c_id = cont.get("id")
        if not c_id:
            return False
        for _ in range(45):
            time.sleep(6)
            st = session.get(
                "https://graph.facebook.com/v21.0/" + c_id,
                params={"fields": "status_code", "access_token": token},
                timeout=12).json()
            if st.get("status_code") == "FINISHED":
                break
            if st.get("status_code") == "ERROR":
                return False
        pub = session.post(
            "https://graph.facebook.com/v21.0/" + ig_id + "/media_publish",
            data={"creation_id": c_id, "access_token": token},
            timeout=18).json()
        return bool(pub.get("id"))
    except Exception:
        return False
'''
CODE[f"{ROOT}/uploader/3_instagram_upload/4_container/__init__.py"] = '"""IG Container"""\n'
CODE[f"{ROOT}/uploader/3_instagram_upload/4_container/1_container.py"] = '''"""
📦 Instagram Container
"""
import requests


def create_container(ig_id, token, media_type="REELS",
                     video_url="", caption=""):
    try:
        r = requests.post(
            "https://graph.facebook.com/v21.0/" + ig_id + "/media",
            data={"media_type": media_type, "video_url": video_url,
                  "caption": caption, "access_token": token},
            timeout=30).json()
        return r.get("id")
    except Exception:
        return None
'''
CODE[f"{ROOT}/uploader/3_instagram_upload/5_publish/__init__.py"] = '"""IG Publish"""\n'
CODE[f"{ROOT}/uploader/3_instagram_upload/5_publish/1_publish.py"] = '''"""
📤 Instagram Publish
"""
import requests


def publish_container(ig_id, token, creation_id):
    try:
        r = requests.post(
            "https://graph.facebook.com/v21.0/" + ig_id + "/media_publish",
            data={"creation_id": creation_id, "access_token": token},
            timeout=20).json()
        return r.get("id")
    except Exception:
        return None
'''
CODE[f"{ROOT}/uploader/3_instagram_upload/6_status_poll/__init__.py"] = '"""IG Status"""\n'
CODE[f"{ROOT}/uploader/3_instagram_upload/6_status_poll/1_status_poll.py"] = '''"""
⏳ Instagram Status Poll
"""
import time
import requests


def wait_for_finish(container_id, token, max_tries=40, delay=5):
    session = requests.Session()
    for _ in range(max_tries):
        time.sleep(delay)
        try:
            r = session.get(
                "https://graph.facebook.com/v21.0/" + container_id,
                params={"fields": "status_code", "access_token": token},
                timeout=12).json()
            status = r.get("status_code")
            if status == "FINISHED":
                return True
            if status == "ERROR":
                return False
        except Exception:
            continue
    return False
'''

# ═══════════════════════════════════════════════════════════
# 🏗️ WRITE ALL
# ═══════════════════════════════════════════════════════════

def write_all():
    written = 0
    skipped = 0
    for path, code in CODE.items():
        folder = os.path.dirname(path)
        if folder:
            os.makedirs(folder, exist_ok=True)
        if os.path.exists(path):
            try:
                size = os.path.getsize(path)
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                if size > 100 and "Sawaj Studio Module" not in content:
                    skipped += 1
                    continue
            except Exception:
                pass
        with open(path, "w", encoding="utf-8") as f:
            f.write(code.strip() + "\n")
        written += 1
    print("=" * 60)
    print(f"💻 content.py — Written: {written} | Skipped: {skipped}")
    print("=" * 60)
    return written, skipped


if __name__ == "__main__":
    print("=" * 60)
    print("🏗️  SAWAJ STUDIO — CONTENT")
    print("=" * 60)
    write_all()
    print("🎉 CONTENT COMPLETE")
