import math
import random

COLORS = (
    "#b5a642",
    "#ffbf00",
    "#fff600",
    "#a4c639",
    "#1e4d2b",
    "#f2f3f4",
    "#00ffff",
    "#6699cc",
    "#0000ff",
    "#002e63",
    "#8a2be2",
    "#ffc1cc",
    "#c41e3a",
    "#a52a2a",
    "#6f4e37",
)


def hex_to_rgb(color):
    if color.startswith("#"):
        color = color.lstrip("#")
    return tuple(int(color[i : i + 2], 16) for i in (0, 2, 4))


def perceived_brightness(bg):
    r, g, b = hex_to_rgb(bg)
    brightness = math.sqrt(r**2 * 0.299 + g**2 * 0.587 + b**2 * 0.114)
    return int(brightness)


def get_foreground_color(brightness):
    if brightness > 130:
        return "#000000"
    return "#ffffff"


get_fg_color = get_foreground_color


def get_color():
    _colors = list(COLORS)
    random.shuffle(_colors)
    for bg_color in _colors:
        brightness = perceived_brightness(bg_color)
        yield bg_color, get_fg_color(brightness)
