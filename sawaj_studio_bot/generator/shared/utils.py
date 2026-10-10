"""Helper functions"""
import re
import subprocess

def sanitize(t):
    if not t: return ""
    t = re.sub(r'[\u200b-\u200f\ufeff\u202a-\u202e]', '', str(t))
    return t.replace('"', '').replace("'", '').replace('\n', ' ').strip()

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
