# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      B12_vignette.py                           ║
# ║  📁 PATH:      .../fb_ig_yt_short_video_generator/       ║
# ║                B_graphics/B12_vignette.py                ║
# ║  🎯 PURPOSE:   Vignette (soft dark edges with pulse)     ║
# ║  📖 FOLDER:    B_graphics                                ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   🌑 VIGNETTE MODULE                                     ║
║   ═══════════════════                                    ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      Soft dark edges (breathing pulse)                   ║
║                                                          ║
║   📖 Function:                                           ║
║      • draw_vignette() → Darken all 4 edges              ║
║                                                          ║
║   🎨 Effect:                                             ║
║      • Top / Bottom / Left / Right edges                 ║
║      • Breathing intensity (60 ± 20)                     ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

import math

# Constants for vignette effect
DEFAULT_INTENSITY = 60
PULSE_AMPLITUDE = 20
MIN_INTENSITY = 20
MAX_INTENSITY = 100

def draw_vignette(draw: object, t: float, intensity: int = DEFAULT_INTENSITY) -> None:
    """
    Draw a vignette effect with breathing intensity on the image.

    Args:
        draw (object): ImageDraw object to draw on.
        t (float): Time in seconds for the breathing effect.
        intensity (int, optional): Base intensity of the vignette. Defaults to DEFAULT_INTENSITY.

    Returns:
        None
    """
    # Calculate pulsating intensity
    pulse = int(intensity + PULSE_AMPLITUDE * math.sin(t * 0.8))
    pulse = max(MIN_INTENSITY, min(MAX_INTENSITY, pulse))

    # Define edges for vignette effect
    edges = [
        (0, 0, 1080, 200),        # Top
        (0, 1720, 1080, 1920),    # Bottom
        (0, 0, 150, 1920),        # Left
        (930, 0, 1080, 1920),     # Right
    ]
    
    # Draw rectangles for each edge with calculated intensity
    for (x1, y1, x2, y2) in edges:
        draw.rectangle([x1, y1, x2, y2], fill=(0, 0, 0, pulse))
