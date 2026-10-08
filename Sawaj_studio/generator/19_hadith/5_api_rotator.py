"""
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
