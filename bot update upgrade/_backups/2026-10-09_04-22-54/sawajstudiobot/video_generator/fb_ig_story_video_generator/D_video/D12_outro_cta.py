"""D12_outro_cta.py — Sirf CTA."""


def draw_cta(draw, alpha, font):
    a = int(255 * alpha)
    if a < 5:
        return
    buttons = [("LIKE", 140), ("SUBSCRIBE", 420), ("SHARE", 780)]
    cy = 960
    btn_h = 60
    pad_x = 24
    for label, x_start in buttons:
        bbox = draw.textbbox((0, 0), label, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        btn_w = tw + pad_x * 2
        x1 = x_start
        y1 = cy - btn_h // 2
        x2 = x_start + btn_w
        y2 = cy + btn_h // 2
        draw.rounded_rectangle([x1, y1, x2, y2], radius=btn_h // 2,
                               fill=(255, 240, 200, int(a * 0.25)),
                               outline=(255, 220, 130, a), width=2)
        tx = x1 + pad_x
        ty = cy - th // 2 - bbox[1]
        draw.text((tx, ty), label, font=font, fill=(255, 240, 200, a))
