"""F4_drive_links.py — Sirf links."""


def build_links(did):
    return (f"https://drive.google.com/file/d/{did}/view",
            f"https://drive.google.com/uc?export=download&id={did}")
