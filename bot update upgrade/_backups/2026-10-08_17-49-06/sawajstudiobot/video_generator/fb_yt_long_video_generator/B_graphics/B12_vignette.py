# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      B12_vignette.py                           ║
# ║  📁 PATH:      .../fb_yt_long_video_generator/           ║
# ║                B_graphics/B12_vignette.py                ║
# ║  🎯 PURPOSE:   Dark radial edge vignette overlay         ║
# ║  📖 FOLDER:    B_graphics                                ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   🎬 VIGNETTE MODULE                                     ║
║   ═══════════════════                                    ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      Cinematic edge darkening to keep focus on center.   ║
╚══════════════════════════════════════════════════════════╝
"""

import numpy as np
from PIL import Image


def apply_vignette(image: Image.Image, amount: float = 0.6) -> Image.Image:
    """Applies a smooth radial dark vignette gradient around outer margins."""
    w, h = image.size
    x = np.linspace(-1, 1, w)
    y = np.linspace(-1, 1, h)
    xx, yy = np.meshgrid(x, y)
    radius = np.sqrt(xx**2 + yy**2)

    # Smooth step vignette gradient calculation
    vignette = 1 - np.clip((radius - 0.5) / (1.414 - 0.5), 0, 1) * amount
    vignette = np.stack([vignette] * 3, axis=-1)

    img_np = np.array(image.convert("RGB"), dtype=np.float32) / 255.0
    result = (img_np * vignette * 255.0).astype(np.uint8)

    return Image.fromarray(result).convert("RGBA")
  
