"""Music + Background fetcher"""
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
                        run_cmd(f'ffmpeg -y -stream_loop -1 -i tmp.mp4 -vf "scale=1200:2140:force_original_aspect_ratio=increase,crop=1080:1920,zoompan=z=\'min(zoom+0.0004,1.06)\':d=1:x=\'iw/2-(iw/zoom/2)\':y=\'ih/2-(ih/zoom/2)\':s=1080x1920,setsar=1,{DARKEN}" -t {dur:.2f} -an -c:v libx264 -preset veryfast -crf 18 {out}')
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
                    run_cmd(f'ffmpeg -y -stream_loop -1 -i tmp.mp4 -vf "scale=1200:2140:force_original_aspect_ratio=increase,crop=1080:1920,zoompan=z=\'min(zoom+0.0004,1.06)\':d=1:x=\'iw/2-(iw/zoom/2)\':y=\'ih/2-(ih/zoom/2)\':s=1080x1920,setsar=1,{DARKEN}" -t {dur:.2f} -an -c:v libx264 -preset veryfast -crf 18 {out}')
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
