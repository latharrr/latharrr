"""
Turns a portrait photo into the ASCII art on the profile card.

Run it once when the photo changes; the daily workflow only reads the portrait.txt it writes.
Dense glyphs mark dark areas (hair, beard, suit) on both themes, which is what keeps the face readable.
    pip install pillow && python art/portrait.py path/to/portrait.webp
"""
import sys
from collections import deque
from pathlib import Path

from PIL import Image, ImageFilter, ImageOps

COLS = 56
CELL_ASPECT = 0.5            # monospace glyph width / line height on the card
RAMP = ' .,:;i1tfLCG08@'      # sparse -> dense
CROP = (80, 50, 640, 900)     # head and shoulders of the source photo
OUT = Path(__file__).parent


def background_mask(img, threshold=228):
    """Near-white pixels connected to the border are background (the studio wall)."""
    w, h = img.size
    px = img.load()
    bg = [[False] * w for _ in range(h)]
    queue = deque((x, y) for x in range(w) for y in (0, h - 1))
    queue.extend((x, y) for y in range(h) for x in (0, w - 1))
    while queue:
        x, y = queue.popleft()
        if 0 <= x < w and 0 <= y < h and not bg[y][x] and px[x, y] >= threshold:
            bg[y][x] = True
            queue.extend(((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)))
    return bg


def render(img, bg):
    w, h = img.size
    px = img.load()
    lines = []
    for y in range(h):
        row = ''
        for x in range(w):
            if bg[y][x]:
                row += ' '
                continue
            level = 1 - px[x, y] / 255
            # never drop a subject cell to a blank, so hair and suit keep their shape
            row += RAMP[1 + round(level * (len(RAMP) - 2))]
        lines.append(row.rstrip())
    return '\n'.join(lines) + '\n'


def main(src):
    photo = Image.open(src).convert('L').crop(CROP)
    photo = ImageOps.autocontrast(photo, cutoff=1).filter(ImageFilter.SHARPEN)
    rows = round(COLS * CELL_ASPECT * photo.height / photo.width)
    small = photo.resize((COLS, rows), Image.LANCZOS)
    bg = background_mask(small)
    (OUT / 'portrait.txt').write_text(render(small, bg))
    print(f'{COLS}x{rows} written to {OUT}')


if __name__ == '__main__':
    main(sys.argv[1])
