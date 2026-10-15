"""Draws the social card html/images/og5.png (1200x630): the wordmark art from gen/assets/wordmark.png,
the home page headline with its gradient accent, and the address. Run with the system python3 (needs PIL)."""
from PIL import Image, ImageDraw, ImageFont, ImageChops
import math
import os
S = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
W, H = 1200, 630
BASE = (9, 15, 29); GLOW = (28, 48, 93); INK = (238, 243, 251); MUTED = (138, 154, 182)
BLUE = (77, 141, 255); TEAL = (45, 212, 191); RULE = (34, 44, 66)
FONT = "/System/Library/Fonts/HelveticaNeue.ttc"
bold = lambda s: ImageFont.truetype(FONT, s, index=1)
medium = lambda s: ImageFont.truetype(FONT, s, index=10)

# background: navy with a soft glow from the top-left corner
img = Image.new("RGB", (W, H), BASE)
px = img.load()
for y in range(H):
    for x in range(W):
        d = math.hypot(x / 1.25, y) / 560
        if d < 1:
            t = (1 - d) ** 1.7
            px[x, y] = tuple(round(b + (g - b) * t) for b, g in zip(BASE, GLOW))
# grid: 60px pitch, white at alpha 12
grid = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(grid)
for x in range(0, W, 60): gd.line([(x, 0), (x, H)], fill=(255, 255, 255, 12))
for y in range(0, H, 60): gd.line([(0, y), (W, y)], fill=(255, 255, 255, 12))
img = Image.alpha_composite(img.convert("RGBA"), grid)

# wordmark: the 1810x331 art, navy recoloured to ink, the slate "2o" kept
wm = Image.open(f"{S}/wordmark.png").convert("RGBA")
wp = wm.load()
for y in range(wm.height):
    for x in range(wm.width):
        r, g, b, a = wp[x, y]
        if a and r + g + b < 260:
            wp[x, y] = (*INK, a)
wm = wm.resize((440, round(331 * 440 / 1810)), Image.LANCZOS)
img.alpha_composite(wm, (97, 96))
d = ImageDraw.Draw(img)

# headline: line 1 in ink, line 2 in the blue-to-teal gradient, sized to fit the 1006px text width
lines = ["A platform to build, run, and use AI microagents", "through search."]
size = 60
while max(bold(size).getlength(l) for l in lines) > 1006: size -= 1
f = bold(size); pitch = round(size * 1.26)
n = len(lines); last = top = round((300 + 462) / 2 - n * pitch / 2)
for i, l in enumerate(lines[:-1]): d.text((97, top + i * pitch), l, font=f, fill=INK)
last = top + (n - 1) * pitch
mask = Image.new("L", (W, H), 0); md = ImageDraw.Draw(mask)
md.text((97, last), lines[-1], font=f, fill=255)
x0, x1 = 97, 97 + f.getlength(lines[-1])
grad = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gp = grad.load()
for x in range(W):
    t = min(1, max(0, (x - x0) / (x1 - x0)))
    c = tuple(round(a + (b - a) * t) for a, b in zip(BLUE, TEAL)) + (255,)
    for y in range(last - 10, last + pitch + 30): gp[x, y] = c
img.paste(grad, (0, 0), mask)

# rule and the address
d = ImageDraw.Draw(img)
d.line([(97, 530), (1103, 530)], fill=RULE, width=1)
d.text((97, 572), "search2o.com", font=bold(24), fill=INK, anchor="ls")
out = img.convert("RGB"); out.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "html", "images", "og5.png"), optimize=True)
print("saved", out.size, "line1 width", round(f.getlength(lines[0])), "right edge", 97 + round(f.getlength(lines[0])))
