#!/usr/bin/env python3
"""
Story Pipeline v62 — Ultimate Production Ready
- Har run par nayi clips (3 clips inside 1 video)
- 100% No Face / Islamic Safe
- Fixed Audio-Video Sync (No cut-off issues)
- VIP Colors (No black boxes, no borders)
"""
import os, re, time, random, subprocess, requests, sys, datetime, json
import base64, shlex, glob, pytz
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import quote as url_quote
from mutagen.mp3 import MP3
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# ─────────────────────────── ENV & CONFIG ───────────────────────────
IST = pytz.timezone("Asia/Kolkata")
NOW = datetime.datetime.now(IST)
DATE_STR = NOW.strftime("%d %B %Y")
RUN_TAG = NOW.strftime("%Y%m%d_%H%M%S")
DAY_NUM = NOW.timetuple().tm_yday
session = requests.Session()

def env(k, d=None): return os.environ.get(k, d)

TG_TOKEN = env("TELEGRAM_BOT_TOKEN")
TG_CHAT_ID = env("TELEGRAM_CHAT_ID")
GITHUB_SUMMARY = env("GITHUB_STEP_SUMMARY")
FFMPEG_LOGLEVEL = env("FFMPEG_LOGLEVEL", "error")
CHANNEL_HANDLE = env("CHANNEL_HANDLE", "@YourChannel")

SARVAM_API_KEY = env("SARVAM_API_KEY")
GEMINI_API_KEY_AI = env("GEMINI_API_KEY_AI")
GROQ_API_KEY_AI = env("GROQ_API_KEY_AI")
PEXELS_API_KEY = env("PEXELS_API_KEY")
PIXABAY_API_KEY = env("PIXABAY_API_KEY")
POLLINATIONS_API_URL = env("POLLINATIONS_API_URL")
HADITH_API_URL = env("HADITH_API_URL")
GDRIVE_STORY_VIDEO_FOLDER_ID = env("GDRIVE_STORY_VIDEO_FOLDER_ID")
GOOGLE_DRIVE_CLIENT_ID = env("GOOGLE_DRIVE_CLIENT_ID")
GOOGLE_DRIVE_CLIENT_SECRET = env("GOOGLE_DRIVE_CLIENT_SECRET")
GOOGLE_DRIVE_REFRESH_TOKEN = env("GOOGLE_DRIVE_REFRESH_TOKEN")

api_status = {}
HADITH_INFO = {}

# 🎨 VIP PREMIUM COLORS
C_GOLD   = "&H0000D7FF&" 
C_WHITE  = "&H00FFFFFF&" 
C_GREEN  = "&H0050C878&" 
C_CYAN   = "&H0000FFFF&" 
C_AMBER  = "&H0000AAFF&" 

# ─────────────────────────── HELPERS ───────────────────────────
def send_tg(msg, preview=False):
    print(msg)
    if not (TG_TOKEN and TG_CHAT_ID): return
    try:
        s = str(msg)
        for i in range(0, len(s), 4000):
            session.post(f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage",
                json={"chat_id": TG_CHAT_ID, "text": s[i:i+4000], "parse_mode": "HTML",
                      "disable_web_page_preview": not preview}, timeout=20)
    except Exception as e: print(f"[TG ERROR] {e}")

def run_cmd(cmd, check=True, timeout=900):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        if check: raise Exception("Command timed out")
        return None
    if r.returncode != 0:
        err = (r.stderr or "")[:600]
        if check: raise Exception(f"FFmpeg Error: {err[:200]}")
    return r

def sanitize(t):
    if not t: return ""
    t = re.sub(r"[\u200b-\u200f\ufeff\u202a-\u202e]", "", str(t))
    return t.replace('"', '').replace("'", "").replace("\n", " ").strip()

def sanitize_ass(t):
    if not t: return ""
    return sanitize(t).replace("\\", "\\\\").replace("{", "\\{").replace("}", "\\}")

def get_dur(path):
    if not os.path.exists(path): return 0.0
    try: return MP3(path).info.length
    except Exception: pass
    try:
        r = subprocess.run(f'ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "{path}"', shell=True, capture_output=True, text=True, timeout=30)
        v = r.stdout.strip()
        return float(v) if v else 0.0
    except Exception: return 0.0

def http_get(url, timeout=25, **kw):
    hdrs = {"User-Agent": "Mozilla/5.0"}
    if "headers" in kw: hdrs.update(kw.pop("headers"))
    try:
        r = session.get(url, timeout=timeout, headers=hdrs, **kw)
        if 200 <= r.status_code < 300: return r
    except Exception: pass
    return None

def http_post(url, timeout=30, **kw):
    hdrs = {"User-Agent": "Mozilla/5.0"}
    if "headers" in kw: hdrs.update(kw.pop("headers"))
    try:
        r = session.post(url, timeout=timeout, headers=hdrs, **kw)
        if 200 <= r.status_code < 300: return r
    except Exception: pass
    return None

def download(url, path, min_size=8000):
    try:
        r = session.get(url, timeout=60, stream=True, headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code == 200:
            written = 0
            with open(path, "wb") as f:
                for chunk in r.iter_content(1024 * 1024):
                    if chunk: f.write(chunk); written += len(chunk)
            if written > min_size: return True
    except Exception: pass
    return False

def report_status():
    lines = ["📊 <b>ENGINE STATUS</b>\n"]
    for sec, st in api_status.items():
        lines.append(f"<b>{sec}:</b>")
        for n, r in st.items(): lines.append(f"  {r} {n}")
    if len(lines) > 1: send_tg("\n".join(lines))

# ─────────────────────────── HADITH & TRANSLATION ───────────────────────────
def fetch_hadith():
    books = [{"eng": "eng-bukhari", "ara": "ara-bukhari", "name": "Sahih al-Bukhari", "max": 7563},
             {"eng": "eng-muslim", "ara": "ara-muslim", "name": "Sahih Muslim", "max": 7500}]
    base = HADITH_API_URL if HADITH_API_URL else "https://cdn.jsdelivr.net/gh/fawazahmed0/hadith-api@1"
    for _ in range(15):
        book = random.choice(books)
        num = random.randint(1, book["max"])
        try:
            r = http_get(f"{base}/editions/{book['eng']}/{num}.json", timeout=12)
            if r:
                hs = r.json().get("hadiths", [])
                if hs:
                    eng = sanitize(hs[0].get("text", ""))
                    if 45 <= len(eng) <= 480:
                        ara = ""
                        ar_r = http_get(f"{base}/editions/{book['ara']}/{num}.json", timeout=10)
                        if ar_r:
                            ad = ar_r.json().get("hadiths", [])
                            if ad: ara = sanitize(ad[0].get("text", ""))
                        api_status.setdefault("Data", {})["HADITH"] = "✅ Success"
                        return {"collection": book["name"], "number": str(hs[0].get("hadithnumber") or num), "english": eng, "arabic": ara}
        except Exception: pass
    return None

def translate_text(text):
    if SARVAM_API_KEY:
        try:
            r = http_post("https://api.sarvam.ai/translate", headers={"api-subscription-key": SARVAM_API_KEY},
                          json={"input": text, "source_language_code": "en-IN", "target_language_code": "hi-IN", "mode": "formal"}, timeout=20)
            if r and r.json().get("translated_text"): return r.json()["translated_text"]
        except Exception: pass
    if GEMINI_API_KEY_AI:
        try:
            r = http_post(f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY_AI}",
                          json={"contents": [{"parts": [{"text": f"Translate to Hindi:\n{text}"}]}]}, timeout=20)
            if r:
                cand = r.json().get("candidates", [])
                if cand: return cand[0].get("content", {}).get("parts", [{}])[0].get("text", "").strip()
        except Exception: pass
    return text

def generate_text_ai(prompt, default):
    if GROQ_API_KEY_AI:
        try:
            r = http_post("https://api.groq.com/openai/v1/chat/completions", headers={"Authorization": f"Bearer {GROQ_API_KEY_AI}"},
                          json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}], "temperature": 0.7}, timeout=20)
            if r and r.json().get("choices"): return r.json()["choices"][0]["message"]["content"].strip().strip('"')
        except Exception: pass
    return default

# ─────────────────────────── TTS & AUDIO ───────────────────────────
def gen_tts(text, outfile):
    text = sanitize(text)
    if not text: return False
    if SARVAM_API_KEY:
        try:
            r = http_post("https://api.sarvam.ai/text-to-speech", headers={"api-subscription-key": SARVAM_API_KEY},
                          json={"inputs": [text], "target_language_code": "hi-IN", "speaker": "meera", "pace": 0.9}, timeout=30)
            if r and r.json().get("audios"):
                with open(outfile, "wb") as f: f.write(base64.b64decode(r.json()["audios"][0]))
                if os.path.getsize(outfile) > 4000: return True
        except Exception: pass
    
    # Edge TTS Fallback
    tmp = outfile + ".txt"
    with open(tmp, "w", encoding="utf-8") as f: f.write(text)
    run_cmd(f'edge-tts --file "{tmp}" --write-media "{outfile}" --voice hi-IN-MadhurNeural --rate="-5%"', check=False)
    if os.path.exists(tmp): os.remove(tmp)
    return os.path.exists(outfile) and os.path.getsize(outfile) > 4000

# ─────────────────────────── VIDEO (NO FACE, 3 CLIPS) ───────────────────────────
def get_multi_bg(dur):
    # Strictly safe keywords (No humans, pure nature & islamic art)
    topics = ["mosque architecture", "islamic calligraphy", "night sky stars", "desert sand dunes", 
              "mountain landscape", "flowing river nature", "kaaba mecca", "old islamic books", 
              "crescent moon", "islamic geometric patterns", "clouds timelapse", "forest trees"]
    random.shuffle(topics)
    
    urls = []
    if PEXELS_API_KEY:
        for q in topics[:5]:
            r = http_get(f"https://api.pexels.com/videos/search?query={url_quote(q)}&orientation=portrait&per_page=3", headers={"Authorization": PEXELS_API_KEY}, timeout=15)
            if r:
                for v in r.json().get("videos", []):
                    vf = v.get("video_files") or []
                    if vf:
                        vf.sort(key=lambda x: abs((x.get("width") or 0) - 1080))
                        urls.append(vf[0]["link"])
    
    if PIXABAY_API_KEY and len(urls) < 6:
        for q in topics[5:10]:
            r = http_get(f"https://pixabay.com/api/videos/?key={PIXABAY_API_KEY}&q={url_quote(q)}&per_page=3&video_type=film", timeout=15)
            if r:
                for h in r.json().get("hits", []):
                    v = h.get("videos", {}).get("large") or h.get("videos", {}).get("medium")
                    if v and v.get("url"): urls.append(v["url"])

    if len(urls) < 5:
        urls.extend(["https://assets.mixkit.co/videos/preview/mixkit-stars-in-space-1610-large.mp4",
                     "https://assets.mixkit.co/videos/preview/mixkit-white-clouds-in-a-blue-sky-2408-large.mp4"])

    random.shuffle(urls)
    vids = []
    seg = dur / 2.5 + 1 # 3 clips time
    
    for i, u in enumerate(urls):
        if len(vids) >= 3: break
        path = f"vid_{i}.mp4"
        if not download(u, path, 400_000): continue
        proc = f"proc_{i}.mp4"
        run_cmd(
            f"ffmpeg -y -loglevel {FFMPEG_LOGLEVEL} -stream_loop -1 -i {shlex.quote(path)} "
            f"-vf \"scale=1200:2140:force_original_aspect_ratio=increase,crop=1080:1920,setpts=1.5*PTS,"
            f"zoompan=z='min(zoom+0.0001,1.05)':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920,"
            f"setsar=1,colorbalance=rs=-0.1:gs=0.0:bs=0.1,eq=contrast=1.25:brightness=-0.1,vignette=PI/4,noise=alls=8:allf=t\" "
            f"-t {seg:.2f} -an -r 30 -c:v libx264 -preset veryfast -crf 18 {shlex.quote(proc)}",
            check=False, timeout=600)
        if os.path.exists(proc) and os.path.getsize(proc) > 100_000: vids.append(proc)

    if not vids:
        run_cmd(f"ffmpeg -y -loglevel {FFMPEG_LOGLEVEL} -f lavfi -i \"color=c=0x101828:s=1080x1920:d={dur+2}\" -vf \"noise=alls=6:allf=t\" -c:v libx264 -preset veryfast -crf 20 -r 30 bg_final.mp4")
        return "bg_final.mp4"

    if len(vids) == 1:
        run_cmd(f"ffmpeg -y -loglevel {FFMPEG_LOGLEVEL} -stream_loop -1 -i {vids[0]} -c:v libx264 -preset veryfast -crf 18 -t {dur:.2f} -r 30 bg_final.mp4")
    elif len(vids) == 2:
        off = max(0.5, seg - 2.0)
        run_cmd(f"ffmpeg -y -loglevel {FFMPEG_LOGLEVEL} -i {vids[0]} -i {vids[1]} -filter_complex \"[0:v][1:v]xfade=transition=fade:duration=2.0:offset={off:.2f}[outv]\" -map \"[outv]\" -t {dur:.2f} -r 30 -c:v libx264 -preset veryfast -crf 18 bg_final.mp4")
    else:
        off1 = max(0.5, seg - 2.0)
        off2 = max(off1 + 1.0, (seg * 2) - 4.0)
        run_cmd(f"ffmpeg -y -loglevel {FFMPEG_LOGLEVEL} -i {vids[0]} -i {vids[1]} -i {vids[2]} -filter_complex \"[0:v][1:v]xfade=transition=fade:duration=2.0:offset={off1:.2f}[x1];[x1][2:v]xfade=transition=fade:duration=2.0:offset={off2:.2f}[outv]\" -map \"[outv]\" -t {dur:.2f} -r 30 -c:v libx264 -preset veryfast -crf 18 bg_final.mp4")
    return "bg_final.mp4"

# ─────────────────────────── THUMBNAIL & UPLOAD ───────────────────────────
def upload_drive(path):
    folder, rid, cid, cs = GDRIVE_STORY_VIDEO_FOLDER_ID, GOOGLE_DRIVE_REFRESH_TOKEN, GOOGLE_DRIVE_CLIENT_ID, GOOGLE_DRIVE_CLIENT_SECRET
    if not (rid and cid and cs): return False
    try:
        creds = Credentials(token=None, refresh_token=rid, client_id=cid, client_secret=cs, token_uri="https://oauth2.googleapis.com/token")
        service = build("drive", "v3", credentials=creds, cache_discovery=False)
        meta = {"name": f"Day{DAY_NUM:03d}_Hadith_{HADITH_INFO.get('number', '0')}_{RUN_TAG}.mp4"}
        if folder: meta["parents"] = [folder.strip()]
        up = service.files().create(body=meta, media_body=MediaFileUpload(path, mimetype="video/mp4", resumable=True), fields="webViewLink").execute()
        service.permissions().create(fileId=up["id"], body={"type": "anyone", "role": "reader"}).execute()
        if up.get("webViewLink"): send_tg(f'🎬 <b>DONE!</b>\n👁️ <a href="{up["webViewLink"]}">Download</a>', preview=True)
        return True
    except Exception: return False

# ─────────────────────────── MAIN PIPELINE ───────────────────────────
def main():
    send_tg(f"🎬 <b>STARTING (NO FACE, 3 CLIPS)</b>\nDay {DAY_NUM}")
    
    h = fetch_hadith()
    if not h: raise Exception("Hadith fetch failed")
    HADITH_INFO.update(h)

    hindi = translate_text(h["english"])
    hook_text = generate_text_ai(f"Generate 1 viral Hindi hook (max 6 words) for this Hadith:\n{h['english'][:200]}", "Ye hadith aapki zindagi badal degi")
    takeaway_text = generate_text_ai(f"Write 1 short Hindi takeaway (max 10 words):\n{h['english'][:200]}", "Aaj se ye amal shuru karein")

    if not gen_tts(hook_text, "hook.mp3"): raise Exception("Hook TTS failed")
    if not gen_tts("Bismillah. Assalamu Alaikum.", "intro.mp3"): raise Exception("Intro TTS failed")
    if not gen_tts(f"हदीस शरीफ। {hindi}", "main.mp3"): raise Exception("Main TTS failed")
    if not gen_tts(takeaway_text, "takeaway.mp3"): raise Exception("Takeaway TTS failed")

    # ── 1. AUDIO SYNC ENGINE ──
    hook_d = get_dur("hook.mp3"); intro_d = get_dur("intro.mp3")
    main_d = get_dur("main.mp3"); take_d = get_dur("takeaway.mp3")
    
    current_total = hook_d + intro_d + main_d + take_d + 2.0
    atempo = ""
    if current_total > 60.0:
        ratio = current_total / 58.0
        rem = ratio
        parts = []
        while rem > 2.0: parts.append("atempo=2.0"); rem /= 2.0
        if abs(rem - 1.0) > 0.001: parts.append(f"atempo={rem:.4f}")
        atempo = ",".join(parts) + ","

    for src, dst in [("hook.mp3", "hook_v.mp3"), ("intro.mp3", "intro_v.mp3"), ("main.mp3", "main_v.mp3"), ("takeaway.mp3", "takeaway_v.mp3")]:
        run_cmd(f'ffmpeg -y -loglevel {FFMPEG_LOGLEVEL} -i {src} -af "{atempo}loudnorm=I=-16:TP=-1.5:LRA=11,volume=1.15" -c:a libmp3lame {dst}')

    hook_d = get_dur("hook_v.mp3"); intro_d = get_dur("intro_v.mp3"); main_d = get_dur("main_v.mp3"); take_d = get_dur("takeaway_v.mp3")
    
    run_cmd(f"ffmpeg -y -loglevel {FFMPEG_LOGLEVEL} -i hook_v.mp3 -i intro_v.mp3 -i main_v.mp3 -i takeaway_v.mp3 -filter_complex \"[0:a][1:a][2:a][3:a]concat=n=4:v=0:a=1[out]\" -map \"[out]\" full_voice.mp3")

    # Natural Music (Sufi/Ambient)
    run_cmd(f"ffmpeg -y -loglevel {FFMPEG_LOGLEVEL} -f lavfi -i \"anullsrc=r=44100:cl=stereo\" -t 90 -c:a libmp3lame ambient.mp3")

    # Mix Voice + Music
    run_cmd(f"ffmpeg -y -loglevel {FFMPEG_LOGLEVEL} -i full_voice.mp3 -i ambient.mp3 -filter_complex \"[0:a]volume=1.0[voice];[1:a]volume=0.15,afade=t=out:st={max(0, get_dur('full_voice.mp3')-5)}:d=5[bg];[bg][voice]amix=inputs=2:duration=first:normalize=1[out]\" -map \"[out]\" -c:a libmp3lame final_audio.mp3")

    total = get_dur("final_audio.mp3") # ✅ Exact truth source

    # ── 2. VIDEO ENGINE ──
    bg_vid = get_multi_bg(total + 1.5)

    # ── 3. SUBTITLES & VIP COLORS ──
    fonts_dir = os.path.abspath(os.path.expanduser("~/.fonts"))
    ass = [
        "[Script Info]", "ScriptType: v4.00+", "PlayResX: 1080", "PlayResY: 1920", "WrapStyle: 0", "ScaledBorderAndShadow: yes", "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
        f"Style: Badge,Hind,48,{C_WHITE},&H000000FF,&H00000000,&HFF000000,-1,0,0,0,105,105,1.0,0,1,4,2,7,30,30,0,1",
        f"Style: Hook,Noto Serif,115,{C_AMBER},&H000000FF,&H00000000,&HFF000000,-1,0,0,0,105,105,1.5,0,1,8,5,5,40,40,0,1",
        f"Style: Arabic,Amiri,95,{C_GOLD},&H000000FF,&H00000000,&HFF000000,-1,0,0,0,105,105,1.0,0,1,7,4,2,4,80,0,1",
        f"Style: Hindi,Hind,105,{C_WHITE},&H000000FF,&H00000000,&HFF000000,-1,0,0,0,105,105,1.5,0,1,7,4,2,4,80,0,1",
        f"Style: English,Noto Serif,75,{C_GREEN},&H000000FF,&H00000000,&HFF000000,-1,0,0,0,105,105,1.0,0,1,6,3,2,4,80,0,1",
        f"Style: Takeaway,Hind,105,{C_CYAN},&H000000FF,&H00000000,&HFF000000,-1,0,0,0,105,105,1.5,0,1,8,5,5,40,40,0,1",
        f"Style: CTA,Noto Serif,85,{C_GOLD},&H000000FF,&H00000000,&HFF000000,-1,0,0,0,105,105,1.0,0,1,7,5,5,40,40,0,1",
        "[Events]", "Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text",
    ]
    
    def ts(t): return f"0:{int(t//60):02d}:{int(t%60):02d}.{min(99, int((t%1)*100)):02d}"

    ass.append(f"Dialogue: 1,{ts(0)},{ts(total)},Badge,,0,0,0,,{{\\an7\\pos(40,40)\\1c{C_WHITE}}}Day {DAY_NUM} / 365")
    ass.append(f"Dialogue: 1,{ts(0)},{ts(total)},Badge,,0,0,0,,{{\\an7\\pos(40,100)\\fs35\\1c{C_GOLD}}}Hadith #{h['number']}")
    ass.append(f"Dialogue: 0,{ts(0)},{ts(hook_d)},Hook,,0,0,0,,{{\\fad(300,300)\\pos(540,340)\\1c{C_AMBER}\\bord8\\shad5\\blur4}}{sanitize_ass(hook_text)}")

    intro_s = hook_d; subs_s = intro_s + intro_d; subs_e = subs_s + main_d
    
    if h.get("arabic"): ass.append(f"Dialogue: 0,{ts(subs_s)},{ts(subs_e)},Arabic,,0,0,0,,{{\\fad(300,300)\\an6\\pos(1000,1250)\\blur3}}{sanitize_ass(h['arabic'])}")
    ass.append(f"Dialogue: 0,{ts(subs_s)},{ts(subs_e)},Hindi,,0,0,0,,{{\\fad(300,300)\\an4\\pos(80,1450)\\blur3}}{sanitize_ass(hindi)}")
    ass.append(f"Dialogue: 0,{ts(subs_s)},{ts(subs_e)},English,,0,0,0,,{{\\fad(300,300)\\an4\\pos(80,1620)\\blur3}}{sanitize_ass(h['english'])}")
    
    take_s = subs_e
    ass.append(f"Dialogue: 0,{ts(take_s)},{ts(take_s + take_d)},Takeaway,,0,0,0,,{{\\fad(300,300)\\pos(540,780)\\blur3}}{sanitize_ass(takeaway_text)}")
    ass.append(f"Dialogue: 0,{ts(total-3)},{ts(total)},CTA,,0,0,0,,{{\\fad(300,300)\\pos(540,700)}}👍 Save & Follow\n{{\\fs58\\1c{C_WHITE}}}{CHANNEL_HANDLE}")

    with open("s_subs.ass", "w", encoding="utf-8") as f: f.write("\n".join(ass))

    # ── 4. FINAL RENDER ──
    final = "Final_Video.mp4"
    progress = f"drawbox=x=0:y=ih-8:w='iw*t/{total:.2f}':h=8:color=0xFFD700@0.9:t=fill"
    
    filters = (f"[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,"
               f"colorbalance=rs=-0.1:gs=0.0:bs=0.1,eq=contrast=1.25:brightness=-0.1,vignette=PI/4[bg];"
               f"[bg]subtitles=s_subs.ass:fontsdir={shlex.quote(fonts_dir)},{progress},format=yuv420p,fade=t=in:st=0:d=0.5,fade=t=out:st={total-1.5:.2f}:d=1.5[outv]")

    run_cmd(f"ffmpeg -y -loglevel {FFMPEG_LOGLEVEL} -i {bg_vid} -i final_audio.mp3 -filter_complex \"{filters}\" -map \"[outv]\" -map 1:a -c:v libx264 -preset fast -crf 20 -pix_fmt yuv420p -r 30 -c:a aac -b:a 192k -t {total:.2f} -movflags +faststart {final}")

    upload_drive(final)
    report_status()

if __name__ == "__main__":
    try: main()
    except Exception as e:
        send_tg(f"❌ <b>FAILED:</b> {str(e)[:400]}")
        sys.exit(1)
