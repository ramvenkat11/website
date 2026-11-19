"""Draws the Tactet wordmark from gen/assets/Figtree-wght.ttf (SIL Open Font License, see Figtree-OFL.txt).
Run it to write html/images/logo.png (light pages) and html/images/logo-dark.png (dark pages);
gen/ogcard.py imports draw_wordmark for the social card. Run with the system python3 (needs PIL)."""
from PIL import Image, ImageDraw, ImageFont
import os

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_FILE = os.path.join(HERE, "assets", "Figtree-wght.ttf")
NAME = "Tactet"
WEIGHT = 600
LETTER_SPACING_EM = -0.02
NAVY = (15, 38, 68)      # on light pages
INK = (240, 244, 251)    # on dark pages
LOGO_HEIGHT = 61         # pixels, twice the largest height the header shows
DRAW_SIZE = 400          # drawn at this font size, then reduced, for smooth edges


def _font(size):
    font = ImageFont.truetype(FONT_FILE, size)
    font.set_variation_by_axes([WEIGHT])
    return font


def draw_wordmark(height, colour):
    """The wordmark as an RGBA image cropped to its ink, exactly `height` pixels tall."""
    font = _font(DRAW_SIZE)
    spacing = LETTER_SPACING_EM * DRAW_SIZE
    width = int(font.getlength(NAME) + DRAW_SIZE)
    mask = Image.new("L", (width, DRAW_SIZE * 2), 0)
    pen = ImageDraw.Draw(mask)
    x = DRAW_SIZE / 4
    for index, letter in enumerate(NAME):
        pen.text((x, DRAW_SIZE / 2), letter, font=font, fill=255)
        following = NAME[index + 1] if index + 1 < len(NAME) else ""
        x += font.getlength(letter + following) - font.getlength(following) + spacing
    mask = mask.crop(mask.getbbox())
    scaled_width = round(mask.width * height / mask.height)
    mask = mask.resize((scaled_width, height), Image.LANCZOS)
    image = Image.new("RGBA", mask.size, colour + (0,))
    image.putalpha(mask)
    return image


if __name__ == "__main__":
    images = os.path.join(HERE, "..", "html", "images")
    for file_name, colour in (("logo.png", NAVY), ("logo-dark.png", INK)):
        logo = draw_wordmark(LOGO_HEIGHT, colour)
        logo.save(os.path.join(images, file_name), optimize=True)
        print(file_name, logo.size)
