"""A29_http_download.py — Sirf download."""
from A_core.A9_log_step import log_step


def download(session, url, path, min_size=12000):
    try:
        r = session.get(url, timeout=35)
        if r.status_code == 200 and len(r.content) > min_size:
            with open(path, "wb") as f:
                f.write(r.content)
            log_step("A29_http_download.py", f"OK: {path}", "ok", f"{len(r.content)//1024} KB")
            return True
    except Exception as e:
        log_step("A29_http_download.py", "err", "fail", str(e)[:60])
    return False
