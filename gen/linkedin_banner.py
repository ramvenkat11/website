"""Draws content/linkedin-banner.png, the LinkedIn company page cover (4200x700, 6:1): the wordmark
art from gen/assets/wordmark.png with the tagline, and the home page headline with its gradient
accent. LinkedIn shows it at 1128x191 and overlays the page logo on the bottom-left corner, so the
content sits in the middle band with wide margins. Run with the system python3 (needs PIL)."""
import math, os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "linkedin-banner.png")
W, H = 4200, 700
BASE = (9, 15, 29); GLOW = (28, 48, 93); INK = (238, 243, 251); MUTED = (138, 154, 182)
BLUE = (77, 141, 255); TEAL = (45, 212, 191); HAIR = (58, 74, 110)
FONT = "/System/Library/Fonts/HelveticaNeue.ttc"
bold = lambda s: ImageFont.truetype(FONT, s, index=1)
medium = lambda s: ImageFont.truetype(FONT, s, index=10)

# background: navy, a soft glow from the top-left, a faint grid
img = Image.new("RGB", (W, H), BASE)
px = img.load()
for y in range(H):
    for x in range(W):
        d = math.hypot(x / 2.2, y) / 900
        if d < 1:
            t = (1 - d) ** 1.7
            px[x, y] = tuple(round(b + (g - b) * t) for b, g in zip(BASE, GLOW))
grid = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(grid)
for x in range(0, W, 120): gd.line([(x, 0), (x, H)], fill=(255, 255, 255, 12))
for y in range(0, H, 120): gd.line([(0, y), (W, y)], fill=(255, 255, 255, 12))
img = Image.alpha_composite(img.convert("RGBA"), grid)

# wordmark, navy recoloured to ink, the slate "2o" kept; tagline beneath
wm = Image.open(os.path.join(HERE, "assets", "wordmark.png")).convert("RGBA")
wp = wm.load()
for y in range(wm.height):
    for x in range(wm.width):
        r, g, b, a = wp[x, y]
        if a and r + g + b < 260:
            wp[x, y] = (*INK, a)
WM_W = 600
wm = wm.resize((WM_W, round(wm.height * WM_W / wm.width)), Image.LANCZOS)
left = 760
block_h = wm.height + 26 + 52
wm_top = round((H - block_h) / 2)
img.alpha_composite(wm, (left, wm_top))
d = ImageDraw.Draw(img)
d.text((left + 4, wm_top + wm.height + 26), "Search that executes", font=medium(52), fill=MUTED, anchor="lt")

# vertical hairline between the wordmark and the headline
xh = left + WM_W + 120
d.rectangle([xh, wm_top - 10, xh + 3, wm_top + block_h + 10], fill=HAIR)

# headline: line 1 in ink, line 2 in the blue-to-teal gradient
size = 88; f = bold(size); pitch = 112
lines = ["Build hundreds of task-specific AI agents.", "Search runs the right agent for each request."]
x0 = xh + 120
top = round((H - (pitch + size * 1.0)) / 2) - 4
d.text((x0, top), lines[0], font=f, fill=INK)
mask = Image.new("L", (W, H), 0); ImageDraw.Draw(mask).text((x0, top + pitch), lines[1], font=f, fill=255)
x1 = x0 + f.getlength(lines[1])
grad = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gp = grad.load()
for x in range(W):
    t = min(1, max(0, (x - x0) / (x1 - x0)))
    c = tuple(round(a + (b - a) * t) for a, b in zip(BLUE, TEAL)) + (255,)
    for y in range(top + pitch - 20, top + pitch + size + 40): gp[x, y] = c
img.paste(grad, (0, 0), mask)

out = img.convert("RGB"); out.save(OUT, optimize=True)
print("saved", OUT, out.size, "headline right edge", round(x1), "of", W, "bytes", os.path.getsize(OUT))
