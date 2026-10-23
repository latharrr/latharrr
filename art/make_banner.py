"""
Builds the sketchbook banner at the top of the profile README:

    art/banner-light.svg          art/banner-dark.svg           (desktop, 1664 wide)
    art/banner-mobile-light.svg   art/banner-mobile-dark.svg    (phones, 860 wide)

It redraws the deepanshulathar.com hero in its resting state: the headline, the three
sticker cards from the site's sprite (site-art.svg), the box and the sparkles. Geometry
comes from the site's styles.css. Text is shaped with HarfBuzz and written as vector
paths, so GitHub never has to load a webfont. The background is transparent, so the dark
files only swap the ink colour.

    pip install fonttools brotli uharfbuzz && python art/make_banner.py
"""
import io
import re
from pathlib import Path

import uharfbuzz as hb
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

ART = Path(__file__).parent
SPRITE = (ART / 'site-art.svg').read_text()
UNDERLINE = re.search(r' d="([^"]+)"', (ART / 'underline.svg').read_text()).group(1)
UNDERLINE_BOX = (774.96, 42.6679)

INK = {'light': '#000000', 'dark': '#f0f6fc'}
CARD_INK = '#174652'
LIME, SKY = '#e7ff7d', '#afe3ff'

# Averia Serif Libre 300, decompressed once for HarfBuzz and fontTools.
_font = TTFont(ART / 'fonts' / 'averia-serif-libre-300.woff2')
_font.flavor = None
_buf = io.BytesIO()
_font.save(_buf)
FONT = TTFont(io.BytesIO(_buf.getvalue()))
GLYPHS = FONT.getGlyphSet()
UPM = FONT['head'].unitsPerEm
ASC, DESC = FONT['hhea'].ascent / UPM, -FONT['hhea'].descent / UPM
HB_FONT = hb.Font(hb.Face(_buf.getvalue()))


def num(v):
    return f'{v:.1f}'.rstrip('0').rstrip('.')


def shape(text):
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(HB_FONT, buf, {'kern': True, 'liga': True})
    names = FONT.getGlyphOrder()
    return [(names[i.codepoint], p.x_advance, p.x_offset, p.y_offset)
            for i, p in zip(buf.glyph_infos, buf.glyph_positions)]


def width(text, size, track=0.0):
    """Advance width in px, letter-spacing included, as the browser lays it out."""
    glyphs = shape(text)
    return sum(a for _, a, _, _ in glyphs) * size / UPM + track * size * len(glyphs)


def path_d(text, size, x, baseline, track=0.0):
    """One path for a run of text; x is the left edge, baseline the alphabetic baseline."""
    pen = SVGPathPen(GLYPHS, ntos=num)
    s = size / UPM
    for name, adv, dx, dy in shape(text):
        GLYPHS[name].draw(TransformPen(pen, (s, 0, 0, -s, x + dx * s, baseline - dy * s)))
        x += adv * s + track * size
    return pen.getCommands()


# ---------------------------------------------------------------- headline

def headline(lines, size, line_h, top, cx, ink):
    """lines: lists of (text, chip colour or None). Chips copy .chip-word on the desktop
    hero: an 84px inline-block, 20px padding, 8px margin, 14px radius (scaled to size)."""
    k = size / 62
    track = -0.025
    pad, margin, radius, chip_h = 20 * k, 8 * k, 14 * k, 84 * k
    space = width(' ', size, track)
    out, tail = [], None
    for row, parts in enumerate(lines):
        baseline = top + row * line_h + (line_h - (ASC + DESC) * size) / 2 + ASC * size
        runs, x = [], 0.0
        for i, (text, chip) in enumerate(parts):
            if i:
                x += space
            w = width(text, size, track)
            if chip:
                runs.append((text, chip, x + margin, w))
                x += w + 2 * (pad + margin)
            else:
                runs.append((text, None, x, w))
                x += w
        left = cx - x / 2
        for text, chip, rx, w in runs:
            if chip:
                chip_top = baseline - ASC * size - (chip_h - (ASC + DESC) * size) / 2
                out.append(f'<rect x="{num(left + rx)}" y="{num(chip_top)}" width="{num(w + 2 * pad)}" '
                           f'height="{num(chip_h)}" rx="{num(radius)}" fill="{chip}"/>')
                out.append(f'<path fill="#000" d="{path_d(text, size, left + rx + pad, baseline, track)}"/>')
            else:
                out.append(f'<path fill="{ink}" d="{path_d(text, size, left + rx, baseline, track)}"/>')
        tail = (left, row * line_h + top, x, line_h)
    # The hand-drawn underline hangs under the last line: right -3%, width 74%, 30px below.
    lx, ly, lw, lh = tail
    uw, uh = lw * 0.74, 28 * k
    ux, uy = lx + lw * 1.03 - uw, ly + lh + 30 * k - uh
    sx, sy = uw / UNDERLINE_BOX[0], uh / UNDERLINE_BOX[1]
    out.append(f'<path fill="{ink}" transform="translate({num(ux)} {num(uy)}) scale({sx:.4f} {sy:.4f})" '
               f'd="{UNDERLINE}"/>')
    return '\n'.join(out)


# ---------------------------------------------------------------- cards, box, sparkles

CARDS = [  # sprite id, title, desktop (x, y, w, h), mobile (x, y, w, h); DOM order = paint order
    ('card-products', 'Building products', (265, 542, 351, 203), (30, 0, 470, 272)),
    ('card-growth', 'Growth + attribution', (1025, 542, 412, 203), (30, 570, 500, 246)),
    ('card-ai', 'Shipping AI tools', (576, 607, 492, 203), (250, 300, 590, 243)),
]


def card(i, sprite_id, title, x, y, w, h, radius):
    size = 0.14 * h
    baseline = 0.05 * h + (1.1 * size - (ASC + DESC) * size) / 2 + ASC * size
    return f'''<g transform="translate({x} {y})">
<g filter="url(#card-shadow)"><g clip-path="url(#card-clip-{i})"><use href="#{sprite_id}" width="{w}" height="{h}"/></g></g>
<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="{radius}" fill="none" stroke="#000" stroke-opacity=".04"/>
<path fill="{CARD_INK}" d="{path_d(title, size, 0.07 * h, baseline, -0.01)}"/>
</g>'''


def box_back():
    return '''<ellipse cx="500" cy="420" rx="500" ry="22" fill="url(#box-shadow)"/>
<path transform="translate(392 0)" d="M0 0H544.38L624 149H85.44Z" fill="#1d3e9e"/>'''


def box_front():
    return '''<path transform="translate(43 0)" d="M35.8 0H581L545.2 413H0Z" fill="url(#panel-left)"/>
<path transform="translate(588 0)" d="M35.72 0H347L311.28 413H0Z" fill="url(#panel-right)"/>
<path d="M724 38H839V51A20 20 0 0 1 819 71H744A20 20 0 0 1 724 51Z" fill="#1b3a9e"/>
<path d="M79.62 0H624L538.56 182.93L0 185Z" fill="url(#flap-front)"/>'''


SPARKLES = [  # resting positions on the 1664x1180 hero field (site.js)
    ('ember', 215, 660), ('ember', 1500, 330), ('ember', 1530, 530), ('ember', 110, 300),
    ('ember', 1170, 1000), ('ember', 905, 1060), ('cobalt', 200, 140), ('cobalt', 455, 960),
    ('cobalt', 1465, 855), ('cobalt', 128, 1012), ('lime', 168, 872), ('lime', 150, 470),
    ('lime', 1315, 915), ('lime', 1480, 170), ('lime', 1560, 700),
]
TINTS = {'ember': ('#ff3535', '#ff6b2c'), 'cobalt': ('#3556ff', '#2c76ff'), 'lime': ('#becf3b', '#e8ff3c')}


def sparkles(place):
    out = []
    for tint, fx, fy in SPARKLES:
        x, y = place(fx, fy)
        r = 10 if tint == 'lime' else 8
        out.append(f'<circle cx="{num(x)}" cy="{num(y)}" r="{r}" fill="url(#tint-{tint})" filter="url(#blur-{r})"/>')
    return '\n'.join(out)


def defs(card_sizes, radius):
    symbols = '\n'.join(re.search(rf'<symbol id="{sid}".*?</symbol>', SPRITE, re.S).group(0)
                        for sid, *_ in CARDS)
    clips = '\n'.join(f'<clipPath id="card-clip-{i}"><rect width="{w}" height="{h}" rx="{radius}"/></clipPath>'
                      for i, (w, h) in enumerate(card_sizes))
    tints = '\n'.join(f'<radialGradient id="tint-{t}"><stop offset="0" stop-color="{a}"/>'
                      f'<stop offset=".59" stop-color="{b}"/></radialGradient>' for t, (a, b) in TINTS.items())
    return f'''<defs>
{symbols}
{clips}
{tints}
<filter id="blur-8" x="-1" y="-1" width="3" height="3"><feGaussianBlur stdDeviation="3.2"/></filter>
<filter id="blur-10" x="-1" y="-1" width="3" height="3"><feGaussianBlur stdDeviation="4"/></filter>
<filter id="card-shadow" x="-20%" y="-20%" width="140%" height="160%"><feDropShadow dx="0" dy="10" stdDeviation="15" flood-color="#000" flood-opacity=".06"/></filter>
<radialGradient id="box-shadow"><stop offset="0" stop-color="#000" stop-opacity=".12"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>
<linearGradient id="panel-left" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1b3a9e"/><stop offset="1" stop-color="#4c7bff"/></linearGradient>
<linearGradient id="panel-right" x1="0" y1="0" x2="0" y2="1"><stop offset=".087" stop-color="#8ec5ff"/><stop offset="1" stop-color="#dcedff"/></linearGradient>
<linearGradient id="flap-front" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#dcedff"/><stop offset="1" stop-color="#8ec5ff"/></linearGradient>
</defs>'''


TITLE = "Hi, I’m Deepanshu, a full-stack and AI engineer at PicaPool, and here’s what I’ve built."


def svg(view, body):
    x, y, w, h = view
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x} {y} {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-labelledby="t">\n<title id="t">{TITLE}</title>\n{body}\n</svg>\n')


# ---------------------------------------------------------------- layouts

def desktop(ink):
    # The hero stage is 1664x1180. The site's buttons are left out, so the art moves up
    # into their place (LIFT) and the banner crops to what is drawn.
    lift = 64
    head = headline([[("Hi, I’m Deepanshu", None)],
                     [('a', None), ('Full-stack & AI engineer', LIME), ('at', None), ('PicaPool', SKY)],
                     [('and here’s what I’ve built', None)]], 62, 92, 92, 832, ink)
    cards = '\n'.join(card(i, sid, title, x, y - lift, w, h, 12)
                      for i, (sid, title, (x, y, w, h), _) in enumerate(CARDS))
    box = f'translate(539 {864 - lift}) scale(.535)'
    body = '\n'.join([
        defs([d[2:] for *_, d, _ in CARDS], 12),
        head,
        f'<g transform="{box}">{box_back()}</g>',
        cards,
        f'<g transform="{box}">{box_front()}</g>',
        sparkles(lambda x, y: (x, y if y < 480 else y - lift)),
    ])
    return svg((0, 64, 1664, 1004), body)


def mobile(ink):
    # Phones: the headline wraps to four lines above the 860x1160 mobile art stage.
    head = headline([[("Hi, I’m Deepanshu", None)],
                     [('a', None), ('Full-stack & AI engineer', LIME)],
                     [('at', None), ('PicaPool', SKY)],
                     [('and here’s what I’ve built', None)]], 62, 92, 0, 430, ink)
    stage = 92 * 4 + 90
    cards = '\n'.join(card(i, sid, title, x, y, w, h, 16)
                      for i, (sid, title, _, (x, y, w, h)) in enumerate(CARDS))
    box = 'translate(138 856) scale(.6)'
    body = '\n'.join([
        defs([m[2:] for *_, m in CARDS], 16),
        head,
        f'<g transform="translate(0 {stage})">',
        f'<g transform="{box}">{box_back()}</g>',
        cards,
        f'<g transform="{box}">{box_front()}</g>',
        sparkles(lambda x, y: (x * 860 / 1664, y * 1160 / 1180)),
        '</g>',
    ])
    return svg((0, -24, 860, stage + 1130 + 24), body)


if __name__ == '__main__':
    for theme, ink in INK.items():
        for name, build in (('banner', desktop), ('banner-mobile', mobile)):
            out = ART / f'{name}-{theme}.svg'
            out.write_text(build(ink))
            print(f'{out.name}: {out.stat().st_size // 1024} KB')
