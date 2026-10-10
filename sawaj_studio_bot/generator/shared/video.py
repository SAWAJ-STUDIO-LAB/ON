"""Video builder - frames, subtitles, ffmpeg"""
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
            out += f"Dialogue: 0,{ts(t)},{ts(t+wd)},{style},,0,0,0,,{w}\n"
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
