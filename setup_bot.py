"""
SAWAJ STUDIO BOT - Complete Structure Generator
Ye script pura folder structure + saari files + code generate karti hai
"""

import os

# ============================================================
# FOLDER STRUCTURE
# ============================================================
FOLDERS = [
    ".github/workflows",
    "sawaj_studio_bot/uploader/fb_ig_story",
    "sawaj_studio_bot/uploader/fb_yt_long",
    "sawaj_studio_bot/uploader/fb_ig_yt_short",
    "sawaj_studio_bot/uploader/shared",
    "sawaj_studio_bot/generator/story",
    "sawaj_studio_bot/generator/short",
    "sawaj_studio_bot/generator/long",
    "sawaj_studio_bot/generator/shared",
    "sawaj_studio_bot/assets",
    "sawaj_studio_bot/output",
    "sawaj_studio_bot/temp",
]

# ============================================================
# FILE CONTENTS - Har file ka code yahan hai
# ============================================================

FILES = {

    # ---------- ROOT ----------
    ".gitignore": """# Python
__pycache__/
*.py[cod]
.venv/
venv/

# Generated media
sawaj_studio_bot/output/*
sawaj_studio_bot/temp/*
*.mp3
*.mp4
*.ass
*.png
!sawaj_studio_bot/assets/logo.png

# Secrets
.env
secrets.json
token.json

# OS
.DS_Store
Thumbs.db
""",

    "README.md": """# 🤖 SAWAJ STUDIO BOT

Islamic Hadith videos auto-generate + upload to YouTube, Facebook, Instagram.

## 📅 Schedule (IST)
- 5:00 AM → Story Video
- 6:00 AM & 12:00 PM → Short Video
- 7:00 PM → Long Hadith Video

## 📁 Structure
- `uploader/` → Social media upload
- `generator/` → Video generation
- `.github/workflows/` → GitHub Actions

## 🚀 Manual Run
GitHub → Actions → Select workflow → Run workflow
""",

    # ---------- WORKFLOWS ----------
    ".github/workflows/story_video.yml": """name: "🟢Story Video"

on:
  workflow_dispatch:
    inputs:
      upload_to_social:
        description: 'Upload to Social Media?'
        required: true
        type: boolean
        default: false
  schedule:
    - cron: '30 23 * * *'

permissions:
  contents: write
  actions: write

jobs:
  story:
    runs-on: ubuntu-latest
    timeout-minutes: 90
    steps:
      - uses: actions/checkout@v4
        with:
          token: ${{ secrets.TOKEN_GITHUB }}
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install Dependencies
        run: |
          sudo apt-get update -q
          sudo apt-get install -y -q ffmpeg fonts-noto fonts-noto-extra fontconfig
          pip install -r sawaj_studio_bot/requirements.txt
      - name: Run Story Pipeline
        env:
          TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
          TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
          FACEBOOK_INSTAGRAM_META_TOKEN: ${{ secrets.FACEBOOK_INSTAGRAM_META_TOKEN }}
          FACEBOOK_PAGE_ID: ${{ secrets.FACEBOOK_PAGE_ID }}
          INSTAGRAM_BUSINESS_ACCOUNT_ID: ${{ secrets.INSTAGRAM_BUSINESS_ACCOUNT_ID }}
          OPENROUTER_API_KEY: ${{ secrets.OPENROUTER_API_KEY_AI }}
          GROQ_API_KEY: ${{ secrets.GROQ_API_KEY_AI }}
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY_AI }}
          GOOGLE_DRIVE_CLIENT_ID: ${{ secrets.GOOGLE_DRIVE_CLIENT_ID }}
          GOOGLE_DRIVE_CLIENT_SECRET: ${{ secrets.GOOGLE_DRIVE_CLIENT_SECRET }}
          GOOGLE_DRIVE_REFRESH_TOKEN: ${{ secrets.GOOGLE_DRIVE_REFRESH_TOKEN }}
          GDRIVE_STORY_VIDEO_FOLDER_ID: ${{ secrets.GDRIVE_STORY_VIDEO_FOLDER_ID }}
          GITHUB_EVENT_NAME: ${{ github.event_name }}
          UPLOAD_TO_SOCIAL: ${{ inputs.upload_to_social || github.event.inputs.upload_to_social }}
        run: python sawaj_studio_bot/generator/story/pipeline.py
      - uses: actions/upload-artifact@v4
        with:
          name: morning-story
          path: Final_Story.mp4
          retention-days: 5
""",

    ".github/workflows/short_video.yml": """name: "🟢SHORT VIDEO"

on:
  workflow_dispatch:
    inputs:
      upload_to_social:
        description: 'Upload to Social Media?'
        required: true
        type: boolean
        default: false
  schedule:
    - cron: '30 0 * * *'
    - cron: '30 6 * * *'

permissions:
  contents: write
  actions: write

jobs:
  short-video:
    runs-on: ubuntu-latest
    timeout-minutes: 120
    steps:
      - uses: actions/checkout@v4
        with:
          token: ${{ secrets.TOKEN_GITHUB }}
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install Dependencies
        run: |
          sudo apt-get update -q
          sudo apt-get install -y -q ffmpeg fonts-noto fonts-noto-extra fontconfig
          pip install -r sawaj_studio_bot/requirements.txt
      - name: Run Short Pipeline
        env:
          TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
          TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
          FACEBOOK_INSTAGRAM_META_TOKEN: ${{ secrets.FACEBOOK_INSTAGRAM_META_TOKEN }}
          FACEBOOK_PAGE_ID: ${{ secrets.FACEBOOK_PAGE_ID }}
          INSTAGRAM_BUSINESS_ACCOUNT_ID: ${{ secrets.INSTAGRAM_BUSINESS_ACCOUNT_ID }}
          YOUTUBE_CLIENT_ID: ${{ secrets.YOUTUBE_CLIENT_ID }}
          YOUTUBE_CLIENT_SECRET: ${{ secrets.YOUTUBE_CLIENT_SECRET }}
          YOUTUBE_REFRESH_TOKEN: ${{ secrets.YOUTUBE_REFRESH_TOKEN }}
          DAILY_HADEES_YT_PLAYLIST_ID: ${{ secrets.DAILY_HADEES_YT_PLAYLIST_ID }}
          OPENROUTER_API_KEY: ${{ secrets.OPENROUTER_API_KEY_AI }}
          GROQ_API_KEY: ${{ secrets.GROQ_API_KEY_AI }}
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY_AI }}
          GOOGLE_DRIVE_CLIENT_ID: ${{ secrets.GOOGLE_DRIVE_CLIENT_ID }}
          GOOGLE_DRIVE_CLIENT_SECRET: ${{ secrets.GOOGLE_DRIVE_CLIENT_SECRET }}
          GOOGLE_DRIVE_REFRESH_TOKEN: ${{ secrets.GOOGLE_DRIVE_REFRESH_TOKEN }}
          GDRIVE_SHORT_VIDEO_FOLDER_ID: ${{ secrets.GDRIVE_SHORT_VIDEO_FOLDER_ID }}
          GITHUB_EVENT_NAME: ${{ github.event_name }}
          UPLOAD_TO_SOCIAL: ${{ inputs.upload_to_social || github.event.inputs.upload_to_social }}
        run: python sawaj_studio_bot/generator/short/pipeline.py
      - uses: actions/upload-artifact@v4
        with:
          name: short-video
          path: Final_Short_Video.mp4
          retention-days: 5
""",

    ".github/workflows/long_video.yml": """name: "🟢LONG_video"

on:
  workflow_dispatch:
    inputs:
      upload_to_social:
        description: 'Upload to Social Media?'
        required: true
        type: boolean
        default: false
  schedule:
    - cron: '30 13 * * *'

permissions:
  contents: write
  actions: write

jobs:
  long-hadith:
    runs-on: ubuntu-latest
    timeout-minutes: 180
    steps:
      - uses: actions/checkout@v4
        with:
          token: ${{ secrets.TOKEN_GITHUB }}
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install Dependencies
        run: |
          sudo apt-get update -q
          sudo apt-get install -y -q ffmpeg fonts-noto fonts-noto-extra fontconfig
          pip install -r sawaj_studio_bot/requirements.txt
      - name: Run Long Pipeline
        env:
          TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
          TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
          FACEBOOK_INSTAGRAM_META_TOKEN: ${{ secrets.FACEBOOK_INSTAGRAM_META_TOKEN }}
          FACEBOOK_PAGE_ID: ${{ secrets.FACEBOOK_PAGE_ID }}
          INSTAGRAM_BUSINESS_ACCOUNT_ID: ${{ secrets.INSTAGRAM_BUSINESS_ACCOUNT_ID }}
          YOUTUBE_CLIENT_ID: ${{ secrets.YOUTUBE_CLIENT_ID }}
          YOUTUBE_CLIENT_SECRET: ${{ secrets.YOUTUBE_CLIENT_SECRET }}
          YOUTUBE_REFRESH_TOKEN: ${{ secrets.YOUTUBE_REFRESH_TOKEN }}
          DAILY_HADEES_YT_PLAYLIST_ID: ${{ secrets.DAILY_HADEES_YT_PLAYLIST_ID }}
          OPENROUTER_API_KEY: ${{ secrets.OPENROUTER_API_KEY_AI }}
          GROQ_API_KEY: ${{ secrets.GROQ_API_KEY_AI }}
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY_AI }}
          GOOGLE_DRIVE_CLIENT_ID: ${{ secrets.GOOGLE_DRIVE_CLIENT_ID }}
          GOOGLE_DRIVE_CLIENT_SECRET: ${{ secrets.GOOGLE_DRIVE_CLIENT_SECRET }}
          GOOGLE_DRIVE_REFRESH_TOKEN: ${{ secrets.GOOGLE_DRIVE_REFRESH_TOKEN }}
          GDRIVE_LONG_VIDEO_FOLDER_ID: ${{ secrets.GDRIVE_LONG_VIDEO_FOLDER_ID }}
          GITHUB_EVENT_NAME: ${{ github.event_name }}
          UPLOAD_TO_SOCIAL: ${{ inputs.upload_to_social || github.event.inputs.upload_to_social }}
        run: python sawaj_studio_bot/generator/long/pipeline.py
      - uses: actions/upload-artifact@v4
        with:
          name: long-hadith-post
          path: Final_Long_Hadith.mp4
          retention-days: 7
""",

    # ---------- REQUIREMENTS ----------
    "sawaj_studio_bot/requirements.txt": """requests>=2.31.0
edge-tts>=6.1.10
mutagen>=1.47.0
Pillow>=10.0.0
google-api-python-client>=2.100.0
google-auth-httplib2>=0.1.1
google-auth-oauthlib>=1.1.0
urllib3>=2.0.0
""",

    # ---------- READMEs ----------
    "sawaj_studio_bot/README.md": "# SAWAJ STUDIO BOT\n\nMain bot folder.\n",

    "sawaj_studio_bot/uploader/README.md": "# Uploader\n\nSocial media pe video upload karne ka kaam.\n",

    "sawaj_studio_bot/uploader/fb_ig_story/README.md": "# FB + IG Story Upload\n\nFacebook aur Instagram Story pe video upload.\n",

    "sawaj_studio_bot/uploader/fb_yt_long/README.md": "# FB + YT Long Upload\n\nFacebook aur YouTube pe long video upload.\n",

    "sawaj_studio_bot/uploader/fb_ig_yt_short/README.md": "# FB + IG + YT Short Upload\n\nFacebook, Instagram Reels, YouTube Shorts pe video upload.\n",

    "sawaj_studio_bot/uploader/shared/README.md": "# Uploader Shared\n\nCommon upload helpers.\n",

    "sawaj_studio_bot/generator/README.md": "# Generator\n\nVideo banane ka kaam.\n",

    "sawaj_studio_bot/generator/story/README.md": "# Story Video Generator\n\nMorning Story video banata hai.\n",

    "sawaj_studio_bot/generator/short/README.md": "# Short Video Generator\n\n60s Short video banata hai.\n",

    "sawaj_studio_bot/generator/long/README.md": "# Long Video Generator\n\nLong Hadith video banata hai.\n",

    "sawaj_studio_bot/generator/shared/README.md": "# Generator Shared\n\nCommon code: AI, TTS, Music, Background, Hadith, Video Builder.\n",

    # ---------- __init__.py FILES ----------
    "sawaj_studio_bot/uploader/__init__.py": "",
    "sawaj_studio_bot/uploader/fb_ig_story/__init__.py": "",
    "sawaj_studio_bot/uploader/fb_yt_long/__init__.py": "",
    "sawaj_studio_bot/uploader/fb_ig_yt_short/__init__.py": "",
    "sawaj_studio_bot/uploader/shared/__init__.py": "",
    "sawaj_studio_bot/generator/__init__.py": "",
    "sawaj_studio_bot/generator/story/__init__.py": "",
    "sawaj_studio_bot/generator/short/__init__.py": "",
    "sawaj_studio_bot/generator/long/__init__.py": "",
    "sawaj_studio_bot/generator/shared/__init__.py": "",

    # ---------- .gitkeep FILES ----------
    "sawaj_studio_bot/assets/.gitkeep": "",
    "sawaj_studio_bot/output/.gitkeep": "",
    "sawaj_studio_bot/temp/.gitkeep": "",

    # ---------- GENERATOR SHARED MODULES ----------

    "sawaj_studio_bot/generator/shared/config.py": '''"""Configuration constants"""
import os

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")
META_TOKEN = os.environ.get("FACEBOOK_INSTAGRAM_META_TOKEN", "").strip()

FPS = 25
INTRO_DUR = 1.5
OUTRO_DUR = 1.7
MUSIC_VOL = 0.20
VIDEO_W = 1080
VIDEO_H = 1920
''',

    "sawaj_studio_bot/generator/shared/utils.py": '''"""Helper functions"""
import re
import subprocess

def sanitize(t):
    if not t: return ""
    t = re.sub(r'[\\u200b-\\u200f\\ufeff\\u202a-\\u202e]', '', str(t))
    return t.replace('"', '').replace("'", '').replace('\\n', ' ').strip()

def run_cmd(cmd):
    print(f"[CMD] {cmd[:140]}...")
    subprocess.run(cmd, shell=True, check=True)

def download(session, url, path):
    try:
        r = session.get(url, timeout=35)
        if r.status_code == 200 and len(r.content) > 12000:
            open(path, "wb").write(r.content)
            return True
    except: pass
    return False
''',

    "sawaj_studio_bot/generator/shared/telegram.py": '''"""Telegram notifier"""
import requests

def send_tg(msg, token=None, chat_id=None):
    if not token or not chat_id:
        import os
        token = os.environ.get("TELEGRAM_BOT_TOKEN")
        chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if token and chat_id:
        try:
            requests.post(
                f"https://api.telegram.org/bot{token}/sendMessage",
                json={"chat_id": chat_id, "text": msg, "parse_mode": "HTML",
                      "disable_web_page_preview": True},
                timeout=12
            )
        except: pass
    print(msg)

def report_api_status(api_status):
    lines = ["📊 <b>API STATUS REPORT</b>\\n"]
    for section, status in api_status.items():
        if not status: continue
        lines.append(f"<b>{section}:</b>")
        for name, result in status.items():
            icon = "✅" if result == "success" else "❌" if "failed" in str(result) else "⏸️"
            lines.append(f"  {icon} {name} → {result}")
    send_tg("\\n".join(lines))
''',

    "sawaj_studio_bot/generator/shared/hadith.py": '''"""Hadith fetcher"""
import random
from .utils import sanitize

def fetch_hadith(session, long=False):
    books = [
        {"eng": "eng-bukhari", "ara": "ara-bukhari", "name": "Sahih al-Bukhari", "max": 7000},
        {"eng": "eng-muslim", "ara": "ara-muslim", "name": "Sahih Muslim", "max": 5000},
        {"eng": "eng-abudawud", "ara": "ara-abudawud", "name": "Sunan Abu Dawud", "max": 4000},
        {"eng": "eng-tirmidhi", "ara": "ara-tirmidhi", "name": "Jami at-Tirmidhi", "max": 3500},
    ]
    bases = [
        "https://cdn.jsdelivr.net/gh/fawazahmed0/hadith-api@1",
        "https://raw.githubusercontent.com/fawazahmed0/hadith-api/1"
    ]
    min_len = 200 if long else 30
    for _ in range(30 if long else 1):
        book = random.choice(books)
        num = random.randint(1, book["max"])
        for base in bases:
            try:
                url = f"{base}/editions/{book['eng']}/{num}.json"
                r = session.get(url, timeout=15)
                if r.status_code != 200: continue
                hs = r.json().get("hadiths", [])
                if not hs: continue
                eng = sanitize(hs[0].get("text", ""))
                if len(eng) < min_len: continue
                ara = ""
                try:
                    ar = session.get(url.replace(book["eng"], book["ara"]), timeout=10)
                    if ar.status_code == 200:
                        ad = ar.json().get("hadiths", [])
                        if ad: ara = sanitize(ad[0].get("text", ""))
                except: pass
                return {"collection": book["name"],
                        "number": str(hs[0].get("hadithnumber") or num),
                        "english": eng, "arabic": ara}
            except: pass
    return {"collection": "Sahih al-Bukhari", "number": "1",
            "english": "The reward of deeds depends upon the intentions and every person will get the reward according to what he has intended.",
            "arabic": "إِنَّمَا الأَعْمَالُ بِالنِّيَّاتِ وَإِنَّمَا لِكُلِّ امْرِئٍ مَا نَوَى"}
''',

    "sawaj_studio_bot/generator/shared/ai.py": '''"""AI multi-provider with fallbacks"""
import os
from .utils import sanitize

def call_ai(session, prompt, max_tokens=420, task="general", api_status=None):
    if api_status is None: api_status = {"AI": {}}
    providers = []
    if os.environ.get("OPENROUTER_API_KEY"):
        providers.append(("OpenRouter", "https://openrouter.ai/api/v1/chat/completions",
                          {"Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}"}, "openai/gpt-4o-mini"))
    if os.environ.get("GROQ_API_KEY"):
        providers.append(("Groq", "https://api.groq.com/openai/v1/chat/completions",
                          {"Authorization": f"Bearer {os.environ['GROQ_API_KEY']}"}, "llama-3.3-70b-versatile"))
    if os.environ.get("GEMINI_API_KEY"):
        providers.append(("Gemini", None, None, None))
    if os.environ.get("MISTRAL_API_KEY"):
        providers.append(("Mistral", "https://api.mistral.ai/v1/chat/completions",
                          {"Authorization": f"Bearer {os.environ['MISTRAL_API_KEY']}"}, "mistral-small-latest"))
    if os.environ.get("CEREBRAS_API_KEY"):
        providers.append(("Cerebras", "https://api.cerebras.ai/v1/chat/completions",
                          {"Authorization": f"Bearer {os.environ['CEREBRAS_API_KEY']}"}, "llama3.1-8b"))
    if os.environ.get("COHERE_API_KEY"):
        providers.append(("Cohere", "https://api.cohere.com/v1/chat",
                          {"Authorization": f"Bearer {os.environ['COHERE_API_KEY']}"}, "command-r-plus"))
    if os.environ.get("HUGGINGFACE_API_KEY"):
        providers.append(("HuggingFace",
                          "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct",
                          {"Authorization": f"Bearer {os.environ['HUGGINGFACE_API_KEY']}"}, None))

    for name, url, headers, model in providers:
        try:
            if name == "Gemini":
                r = session.post(
                    f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={os.environ['GEMINI_API_KEY']}",
                    json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=45)
                if r.status_code == 200:
                    text = r.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
                    api_status["AI"][f"{name}({task})"] = "success"
                    return text
            elif name == "Cohere":
                r = session.post(url, headers={**headers, "Content-Type": "application/json"},
                                 json={"model": model, "message": prompt}, timeout=45)
                if r.status_code == 200:
                    api_status["AI"][f"{name}({task})"] = "success"
                    return r.json()["text"].strip()
            elif name == "HuggingFace":
                r = session.post(url, headers={**headers, "Content-Type": "application/json"},
                                 json={"inputs": prompt, "parameters": {"max_new_tokens": max_tokens, "temperature": 0.7}},
                                 timeout=50)
                if r.status_code == 200:
                    data = r.json()
                    if isinstance(data, list) and data:
                        text = data[0].get("generated_text", "").replace(prompt, "").strip()
                        if text:
                            api_status["AI"][f"{name}({task})"] = "success"
                            return text
            else:
                payload = {"model": model, "messages": [{"role": "user", "content": prompt}],
                           "temperature": 0.7, "max_tokens": max_tokens}
                r = session.post(url, headers={**headers, "Content-Type": "application/json"},
                                 json=payload, timeout=45)
                if r.status_code == 200:
                    api_status["AI"][f"{name}({task})"] = "success"
                    return r.json()["choices"][0]["message"]["content"].strip()
            api_status["AI"][f"{name}({task})"] = "failed"
        except Exception as e:
            api_status["AI"][f"{name}({task})"] = f"failed ({str(e)[:35]})"
    return None


def deepl(session, text, api_status=None):
    if api_status is None: api_status = {"Translation": {}}
    key = os.environ.get("DEEPL_API_KEY")
    if not key:
        api_status["Translation"]["DeepL"] = "hold (no key)"
        return None
    try:
        r = session.post("https://api-free.deepl.com/v2/translate",
                         headers={"Authorization": f"DeepL-Auth-Key {key}"},
                         data={"text": text, "target_lang": "HI"}, timeout=30)
        if r.status_code == 200:
            api_status["Translation"]["DeepL"] = "success"
            return r.json()["translations"][0]["text"]
        api_status["Translation"]["DeepL"] = "failed"
    except:
        api_status["Translation"]["DeepL"] = "failed"
    return None
''',

    "sawaj_studio_bot/generator/shared/tts.py": '''"""Text-to-speech engine"""
import os
from .utils import sanitize, run_cmd

def gen_tts(text, outfile, rate="-7%", api_status=None):
    if api_status is None: api_status = {"TTS": {}}
    text = sanitize(text)
    el = os.environ.get("ELEVENLABS_API_KEY")
    if el:
        try:
            import requests
            r = requests.post(
                "https://api.elevenlabs.io/v1/text-to-speech/pNInz6obpgDQGcFmaJgB",
                headers={"Accept": "audio/mpeg", "Content-Type": "application/json", "xi-api-key": el},
                json={"text": text, "model_id": "eleven_multilingual_v2",
                      "voice_settings": {"stability": 0.42, "similarity_boost": 0.82,
                                         "style": 0.35, "use_speaker_boost": True}},
                timeout=60)
            if r.status_code == 200 and len(r.content) > 5000:
                open(outfile, "wb").write(r.content)
                api_status["TTS"]["ElevenLabs"] = "success"
                return True
            api_status["TTS"]["ElevenLabs"] = "failed"
        except:
            api_status["TTS"]["ElevenLabs"] = "failed"
    try:
        tmp = outfile + ".txt"
        open(tmp, "w", encoding="utf-8").write(text)
        run_cmd(f'edge-tts --file "{tmp}" --write-media "{outfile}" --voice hi-IN-MadhurNeural --rate={rate} --pitch=-2Hz --volume=+8%')
        if os.path.exists(tmp): os.remove(tmp)
        api_status["TTS"]["edge-tts"] = "success"
        return True
    except:
        api_status["TTS"]["edge-tts"] = "failed"
        return False
''',

    "sawaj_studio_bot/generator/shared/media.py": '''"""Music + Background fetcher"""
import os, random
from .utils import run_cmd, download

def get_music(session, dur=110, music_vol=0.20, api_status=None):
    if api_status is None: api_status = {"Music": {}}
    fs = os.environ.get("FREESOUND_API_KEY")
    if fs:
        try:
            r = session.get("https://freesound.org/apiv2/search/text/", params={
                "query": "soft ambient meditation islamic peaceful",
                "filter": f"duration:[{dur//3} TO {dur*2}]",
                "fields": "id,name,previews", "page_size": 8, "token": fs}, timeout=14)
            if r.status_code == 200 and r.json().get("results"):
                s = random.choice(r.json()["results"])
                p = s.get("previews", {}).get("preview-hq-mp3") or s.get("previews", {}).get("preview-lq-mp3")
                if p and download(session, p, "music_raw.mp3"):
                    run_cmd(f'ffmpeg -y -i music_raw.mp3 -af "volume={music_vol},afade=t=in:st=0:d=2,afade=t=out:st=90:d=5" -t {dur} music_soft.mp3')
                    api_status["Music"]["Freesound"] = "success"
                    return
            api_status["Music"]["Freesound"] = "failed"
        except:
            api_status["Music"]["Freesound"] = "failed"
    for u in [
        "https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3?filename=soft-ambient-112191.mp3",
        "https://cdn.pixabay.com/download/audio/2022/03/24/audio_4f3b5c5e3d.mp3?filename=peaceful-background-112194.mp3"
    ]:
        if download(session, u, "music_raw.mp3"):
            run_cmd(f'ffmpeg -y -i music_raw.mp3 -af "volume={music_vol},afade=t=in:st=0:d=2,afade=t=out:st=90:d=5" -t {dur} music_soft.mp3')
            api_status["Music"]["Pixabay-CDN"] = "success"
            return
    run_cmd(f'ffmpeg -y -f lavfi -i "sine=frequency=110:duration={dur}" -af "afade=t=in:st=0:d=2.5,afade=t=out:st={dur-10}:d=6,volume=0.12" music_soft.mp3')
    api_status["Music"]["Generated-Sine"] = "success (fallback)"


def get_bg(session, dur, api_status=None):
    if api_status is None: api_status = {"Background": {}}
    DARKEN = "eq=contrast=1.10:brightness=0.02:saturation=1.12,vignette=PI/5"
    out = "bg.mp4"
    pk = os.environ.get("PEXELS_API_KEY")
    if pk:
        for q in random.sample(["islamic architecture night", "mosque night", "night sky stars", "desert night", "kaaba night"], 4):
            try:
                r = session.get(f"https://api.pexels.com/videos/search?query={q}&orientation=portrait&per_page=6",
                                headers={"Authorization": pk}, timeout=14)
                if r.status_code == 200 and r.json().get("videos"):
                    v = random.choice(r.json()["videos"])
                    files = sorted(v.get("video_files", []), key=lambda x: x.get("width", 0), reverse=True)
                    if files and download(session, files[0]["link"], "tmp.mp4"):
                        run_cmd(f'ffmpeg -y -stream_loop -1 -i tmp.mp4 -vf "scale=1200:2140:force_original_aspect_ratio=increase,crop=1080:1920,zoompan=z=\\'min(zoom+0.0004,1.06)\\':d=1:x=\\'iw/2-(iw/zoom/2)\\':y=\\'ih/2-(ih/zoom/2)\\':s=1080x1920,setsar=1,{DARKEN}" -t {dur:.2f} -an -c:v libx264 -preset veryfast -crf 18 {out}')
                        api_status["Background"]["Pexels"] = "success"
                        return out
            except: pass
        api_status["Background"]["Pexels"] = "failed"
    px = os.environ.get("PIXABAY_API_KEY")
    if px:
        try:
            r = session.get(f"https://pixabay.com/api/videos/?key={px}&q=mosque+night&orientation=vertical&per_page=8", timeout=14)
            if r.status_code == 200 and r.json().get("hits"):
                h = random.choice(r.json()["hits"])
                u = h.get("videos", {}).get("large", {}).get("url") or h.get("videos", {}).get("medium", {}).get("url")
                if u and download(session, u, "tmp.mp4"):
                    run_cmd(f'ffmpeg -y -stream_loop -1 -i tmp.mp4 -vf "scale=1200:2140:force_original_aspect_ratio=increase,crop=1080:1920,zoompan=z=\\'min(zoom+0.0004,1.06)\\':d=1:x=\\'iw/2-(iw/zoom/2)\\':y=\\'ih/2-(ih/zoom/2)\\':s=1080x1920,setsar=1,{DARKEN}" -t {dur:.2f} -an -c:v libx264 -preset veryfast -crf 18 {out}')
                    api_status["Background"]["Pixabay"] = "success"
                    return out
            api_status["Background"]["Pixabay"] = "failed"
        except:
            api_status["Background"]["Pixabay"] = "failed"
    c0 = f"{random.randint(10,30):02x}{random.randint(8,25):02x}{random.randint(25,55):02x}"
    c1 = f"{random.randint(10,30):02x}{random.randint(8,25):02x}{random.randint(25,55):02x}"
    run_cmd(f'ffmpeg -y -f lavfi -i "gradients=s=1080x1920:c0=0x{c0}:c1=0x{c1}:speed=0.006" -t {dur:.2f} -c:v libx264 -preset veryfast {out}')
    api_status["Background"]["Generated-Gradient"] = "success (fallback)"
    return out
''',

    "sawaj_studio_bot/generator/shared/video.py": '''"""Video builder - frames, subtitles, ffmpeg"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from .utils import sanitize, run_cmd

def make_logo():
    for src in ["logo.png", "logo.jpg", "sawaj_studio_bot/assets/logo.png", "sawaj_studio_bot/assets/logo.jpg"]:
        if os.path.exists(src):
            try:
                img = Image.open(src).convert("RGBA")
                border, bottom = 10, 22
                nw, nh = img.width + border*2, img.height + border + bottom
                canvas = Image.new("RGBA", (nw, nh), (0,0,0,0))
                draw = ImageDraw.Draw(canvas)
                draw.rectangle([0,0,nw-1,nh-1], outline=(212,175,55,255), width=border)
                draw.rectangle([0, nh-bottom, nw-1, nh-1], fill=(20,15,8,240))
                canvas.paste(img, (border, border), img)
                glow = canvas.filter(ImageFilter.GaussianBlur(4))
                Image.alpha_composite(glow, canvas).save("avatar.png")
                return True
            except: pass
    try:
        canvas = Image.new("RGBA", (400, 170), (0,0,0,0))
        draw = ImageDraw.Draw(canvas)
        draw.rounded_rectangle([6,6,394,164], radius=16, fill=(16,12,6,245), outline=(212,175,55,255), width=5)
        try: fnt = ImageFont.truetype(os.path.expanduser("~/.fonts/NotoSans-Bold.ttf"), 44)
        except: fnt = ImageFont.load_default()
        draw.text((200, 65), "SAWAJ", fill=(230,200,130,255), font=fnt, anchor="mm")
        draw.text((200, 115), "STUDIO", fill=(200,170,110,255), font=fnt, anchor="mm")
        canvas.save("avatar.png")
        return True
    except: return False


def build_subtitles(h, hindi, english, meaning, sawal, jawab, d1, d2, dsawal, dtick, djawab, outfile="subs.ass"):
    ass = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Arabic,Noto Naskh Arabic,86,&H00F0E6D2,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,6,2,2,40,40,140,1
Style: Hindi,Noto Sans Devanagari,72,&H00FFFFFF,&H0000FFFF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,5,2,2,40,40,420,1
Style: English,Noto Sans,58,&H00D0D0D0,&H0000FFFF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,4,2,2,40,40,620,1
[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
"""
    def ts(t): return f"0:{int(t//60):02d}:{t%60:05.2f}"
    def typed(text, style, start, end):
        words = sanitize(text).split()
        if not words: return ""
        wd = (end - start) / max(len(words), 1)
        out, t = "", start
        for w in words:
            out += f"Dialogue: 0,{ts(t)},{ts(t+wd)},{style},,0,0,0,,{w}\\n"
            t += wd
        return out
    with open(outfile, "w", encoding="utf-8") as f:
        f.write(ass)
        f.write(typed(h.get("arabic", ""), "Arabic", 1.4, 1.4 + d1 - 0.25))
        f.write(typed(hindi, "Hindi", 1.4, 1.4 + d1 - 0.25))
        f.write(typed(english, "English", 1.4, 1.4 + d1 - 0.25))
        if meaning:
            f.write(typed(meaning, "Hindi", 1.4 + d1 + 0.1, 1.4 + d1 + d2 - 0.25))
        if sawal:
            f.write(typed(sawal, "Hindi", 1.4 + d1 + d2 + 0.1, 1.4 + d1 + d2 + dsawal - 0.25))
        if jawab:
            f.write(typed(jawab, "Hindi", 1.4 + d1 + d2 + dsawal + dtick + 0.1,
                          1.4 + d1 + d2 + dsawal + dtick + djawab - 0.25))
    return outfile
''',

    # ---------- PIPELINES (Placeholder - yahan aap pura code daalenge) ----------

    "sawaj_studio_bot/generator/story/pipeline.py": '''"""Story Video Pipeline
Yahan story video ka pura code aayega.
Abhi placeholder hai.
"""
import os, sys, time, random, requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from generator.shared import telegram, hadith, ai, tts, media, video
from generator.shared.utils import run_cmd

# TODO: Pura story pipeline code yahan aayega
print("Story pipeline placeholder")
''',

    "sawaj_studio_bot/generator/short/pipeline.py": '''"""Short Video Pipeline
Yahan short video ka pura code aayega.
Abhi placeholder hai.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
print("Short pipeline placeholder")
''',

    "sawaj_studio_bot/generator/long/pipeline.py": '''"""Long Video Pipeline
Yahan long video ka pura code aayega.
Abhi placeholder hai.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
print("Long pipeline placeholder")
''',

    # ---------- UPLOADER FILES (Placeholders) ----------

    "sawaj_studio_bot/uploader/fb_ig_story/fb_story.py": '"""FB Story upload - placeholder"""\n',
    "sawaj_studio_bot/uploader/fb_ig_story/ig_story.py": '"""IG Story upload - placeholder"""\n',
    "sawaj_studio_bot/uploader/fb_yt_long/fb_long.py": '"""FB Long upload - placeholder"""\n',
    "sawaj_studio_bot/uploader/fb_yt_long/yt_long.py": '"""YT Long upload - placeholder"""\n',
    "sawaj_studio_bot/uploader/fb_ig_yt_short/fb_short.py": '"""FB Short upload - placeholder"""\n',
    "sawaj_studio_bot/uploader/fb_ig_yt_short/ig_short.py": '"""IG Short upload - placeholder"""\n',
    "sawaj_studio_bot/uploader/fb_ig_yt_short/yt_short.py": '"""YT Short upload - placeholder"""\n',
    "sawaj_studio_bot/uploader/shared/drive.py": '"""Drive upload - placeholder"""\n',
    "sawaj_studio_bot/uploader/shared/meta.py": '"""Meta helper - placeholder"""\n',
    "sawaj_studio_bot/uploader/shared/telegram.py": '"""Telegram - placeholder"""\n',
}


# ============================================================
# MAIN EXECUTION
# ============================================================

def main():
    print("🚀 SAWAJ STUDIO BOT - Structure Generator")
    print("=" * 50)

    # 1. Create folders
    print("\\n📁 Creating folders...")
    for folder in FOLDERS:
        os.makedirs(folder, exist_ok=True)
        print(f"  ✅ {folder}")

    # 2. Create files with content
    print("\\n📄 Creating files...")
    for filepath, content in FILES.items():
        os.makedirs(os.path.dirname(filepath), exist_ok=True) if os.path.dirname(filepath) else None
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  ✅ {filepath}")

    # 3. Summary
    print("\\n" + "=" * 50)
    print(f"✅ Done! {len(FOLDERS)} folders + {len(FILES)} files created.")
    print("=" * 50)


if __name__ == "__main__":
    main()
