"""
🇮🇳 Hindi Bullet
"""
C_HINDI = (240, 130, 200)


def draw_hindi_bullet(draw, x, y, size=40, alpha=255):
    color = (C_HINDI[0], C_HINDI[1], C_HINDI[2], alpha)
    draw.ellipse([x, y, x + size, y + size], fill=color)


def draw_hindi_word(draw, word, x, y, font, alpha=255):
    a = int(255 * alpha)
    if a <= 5:
        return
    draw.text((x + 3, y + 4), word, font=font, fill=(0, 0, 0, a))
    draw.text((x, y), word, font=font,
              fill=(C_HINDI[0], C_HINDI[1], C_HINDI[2], a))
