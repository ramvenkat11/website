"""Draws content/linkedin-banner2.png, the LinkedIn company page cover (4200x700, 6:1): the tagline as
the title with the home page heading beneath it. LinkedIn shows it at 1128x191 and overlays the page logo on the bottom-left corner, so the
content starts right of the logo (LOGO_END) and is centred in the space that remains. Run with the system python3 (needs PIL)."""
import math, os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "content", "linkedin-banner2.png")
W, H = 4200, 700
BASE = (9, 15, 29); GLOW = (28, 48, 93); INK = (238, 243, 251); SOFT = (176, 190, 214)
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

# tagline as the title with the home page heading as a one-line subtitle, centred as one block in
# the space right of the logo. The name is left to the logo (gen/linkedin_logo.py).
LOGO_END = 1097  # x where the overlaid page logo stops covering the banner, as seen on the live page
TITLE = "Agent server built around search"; TITLE_SIZE = 160
SUB = "Transform your enterprise AI with hundreds of task-focused agents"; SUB_SIZE = 82
SUB_GAP = 64
title_font = bold(TITLE_SIZE); sub_font = medium(SUB_SIZE)
content_w = max(title_font.getlength(TITLE), sub_font.getlength(SUB))
x0 = LOGO_END + round((W - LOGO_END - content_w) / 2)
block_h = TITLE_SIZE + SUB_GAP + SUB_SIZE
top = round((H - block_h) / 2) - 14
d = ImageDraw.Draw(img)
d.text((x0, top), TITLE, font=title_font, fill=INK)
d.text((x0, top + TITLE_SIZE + SUB_GAP), SUB, font=sub_font, fill=SOFT)
x1 = x0 + content_w

out = img.convert("RGB"); out.save(OUT, optimize=True)
print("saved", OUT, out.size, "content from", x0, "to", round(x1), "of", W, "bytes", os.path.getsize(OUT))
