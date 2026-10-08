"""
🔍 Zoompan
"""


def build_zoompan_filter(target_w=1080, target_h=1920):
    return ('scale=1200:2140:force_original_aspect_ratio=increase,'
            'crop=' + str(target_w) + ':' + str(target_h) + ','
            "zoompan=z='min(zoom+0.0004,1.06)':d=1:"
            "x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
            's=' + str(target_w) + 'x' + str(target_h) + ',setsar=1')
