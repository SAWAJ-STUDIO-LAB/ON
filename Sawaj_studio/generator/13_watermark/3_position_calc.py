"""
📍 Position Calc
"""


def calc_position(img_width, img_height, w, h,
                  pos="top-right", margin=30):
    if pos == "top-right":
        return img_width - w - margin, 180
    elif pos == "top-left":
        return margin, 180
    elif pos == "bottom-right":
        return img_width - w - margin, img_height - h - 250
    elif pos == "bottom-left":
        return margin, img_height - h - 250
    return img_width - w - margin, 180
