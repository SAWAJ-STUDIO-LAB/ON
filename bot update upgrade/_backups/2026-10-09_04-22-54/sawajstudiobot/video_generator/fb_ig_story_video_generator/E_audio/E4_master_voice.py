"""E4_master_voice.py — Sirf mastering."""
from A_core.A9_log_step import log_step


def master(base, in_file, out_file):
    log_step("E4_master_voice.py", "master()", "ok")
    base.run_cmd(
        f'ffmpeg -y -i {in_file} -af '
        f'"atempo=0.88,loudnorm=I=-16:TP=-1.5:LRA=11,volume=1.35" '
        f'{out_file}')
    return out_file
