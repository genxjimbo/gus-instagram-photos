"""Add meme-style text overlays to Gus's Instagram photos.

Usage: python3 scripts/add_text.py <calendar.csv> <Anton-Regular.ttf>
Reads scripts/overlay_lines.tsv (post#, top|bottom, lines separated by '|')
and writes photos_with_text/post-NNN_<photo>.jpg.
Anton font: https://fonts.google.com/specimen/Anton (SIL OFL).
"""
import csv, os, sys
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAL, FONT = sys.argv[1], sys.argv[2]
TAG = '@MRGUSTHEWONDERCAT'

def fit(draw, lines, maxw, start=112):
    s = start
    while s > 40:
        f = ImageFont.truetype(FONT, s)
        if max(draw.textlength(l, font=f) for l in lines) <= maxw:
            return f
        s -= 4
    return f

def render(src, dst, pos, lines):
    im = Image.open(src).convert('RGB'); W, H = im.size
    band = Image.new('L', (W, H), 0); bd = ImageDraw.Draw(band); bh = int(H * 0.36)
    for i in range(bh):
        y = i if pos == 'top' else H - 1 - i
        bd.line([(0, y), (W, y)], fill=int(150 * (1 - i / bh) ** 1.6))
    im = Image.composite(Image.new('RGB', (W, H), 'black'), im, band)
    d = ImageDraw.Draw(im)
    f = fit(d, lines, W - 120)
    lh = int(f.size * 1.12); th = lh * len(lines)
    y0 = 50 if pos == 'top' else H - th - 110
    for i, l in enumerate(lines):
        w = d.textlength(l, font=f)
        d.text(((W - w) / 2, y0 + i * lh), l, font=f, fill='white', stroke_width=7, stroke_fill='black')
    sf = ImageFont.truetype(FONT, 30); tw = d.textlength(TAG, font=sf)
    d.text((W - tw - 36, H - 60 if pos == 'top' else 40), TAG, font=sf, fill='white', stroke_width=3, stroke_fill='black')
    im.save(dst, quality=90, optimize=True)

photos = {r['Post #']: r['Photo file'] for r in csv.DictReader(open(CAL, encoding='utf-8'))}
for row in csv.reader(open(os.path.join(ROOT, 'scripts', 'overlay_lines.tsv'), encoding='utf-8'), delimiter='\t'):
    n, pos, text = row
    photo = photos[n]
    out = os.path.join(ROOT, 'photos_with_text', f'post-{int(n):03d}_{photo}')
    render(os.path.join(ROOT, 'photos', photo), out, pos, text.split('|'))
    print(out)
