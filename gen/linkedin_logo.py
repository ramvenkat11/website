"""Draws the LinkedIn company page logo candidates (400x400 PNG) into content/: the wordmark art from
gen/assets/wordmark.png centred on navy (linkedin-logo-wordmark.png), and the favicon's search mark in
the brand blue on navy (linkedin-logo-mark.png). Drawn at 4x and downsampled. Run with the system python3
(needs PIL)."""
import math, os
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content")
S = 4; N = 400 * S
BASE = (9, 15, 29); GLOW = (28, 48, 93); INK = (238, 243, 251); BLUE = (37, 99, 235)


def background():
    img = Image.new("RGB", (N, N), BASE)
    px = img.load()
    for y in range(N):
        for x in range(N):
            d = math.hypot(x, y) / (N * 1.15)
            if d < 1:
                t = (1 - d) ** 1.7
                px[x, y] = tuple(round(b + (g - b) * t) for b, g in zip(BASE, GLOW))
    return img.convert("RGBA")


def wordmark_logo():
    img = background()
    wm = Image.open(os.path.join(HERE, "assets", "wordmark.png")).convert("RGBA")
    wp = wm.load()
    for y in range(wm.height):
        for x in range(wm.width):
            r, g, b, a = wp[x, y]
            if a and r + g + b < 260:
                wp[x, y] = (*INK, a)
    w = round(N * 0.80)
    wm = wm.resize((w, round(wm.height * w / wm.width)), Image.LANCZOS)
    img.alpha_composite(wm, (round((N - w) / 2), round((N - wm.height) / 2)))
    return img


def mark_logo():
    img = background(); d = ImageDraw.Draw(img)
    # the favicon geometry, in a 64-unit box: circle r18 at (25,25) stroke 8.5, handle (39,39)->(58,58) stroke 10
    u = N / 64 * 0.72; ox = oy = (N - 64 * u) / 2
    cx, cy, r, sw = ox + 25 * u, oy + 25 * u, 18 * u, 8.5 * u
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=BLUE, width=round(sw))
    d.line([(ox + 39 * u, oy + 39 * u), (ox + 58 * u, oy + 58 * u)], fill=BLUE, width=round(10 * u))
    hr = 5 * u
    for (x, y) in ((ox + 39 * u, oy + 39 * u), (ox + 58 * u, oy + 58 * u)):
        d.ellipse([x - hr, y - hr, x + hr, y + hr], fill=BLUE)
    return img


for name, fn in (("linkedin-logo-wordmark.png", wordmark_logo), ("linkedin-logo-mark.png", mark_logo)):
    out = fn().convert("RGB").resize((400, 400), Image.LANCZOS)
    path = os.path.join(OUT, name); out.save(path, optimize=True)
    print("saved", path, out.size, os.path.getsize(path), "bytes")
