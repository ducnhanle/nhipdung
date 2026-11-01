#!/usr/bin/env python3
"""Measure font glyph widths at the actual variable-font weights used in scenes.

Run with the engine Python environment after changing fonts:
  uv run --directory ENGINE python PROJECT/tools/measure_fonts.py

Writes assets/fonts/widths.json with measurements at 1000 px. Combining accents
and Unicode characters remain glyph data; widths exclude kerning. Vietnamese
letters a family lacks are measured in its companion font (the @font-face that
build.py declares for them with a unicode-range), as the browser draws them."""
import json
import os
import sys
HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(os.path.dirname(HERE), 'assets', 'fonts')
EM = 1000
MEASURE = {'Montserrat': ('Montserrat.ttf', (700, 800, 900)), 'Caveat': ('Caveat.ttf', (700,))}
COMPANIONS = {'Caveat': 'Sriracha-vietnamese.ttf'}
EXTRAS = '–—‘’“”…•€✓→×'
VIETNAMESE = ((0x0102, 0x0103), (0x0110, 0x0111), (0x0128, 0x0129), (0x0168, 0x0169), (0x01A0, 0x01A1),
              (0x01AF, 0x01B0), (0x1EA0, 0x1EF9), (0x20AB, 0x20AB))
NOTDEF = '\ue000'  # private use: no bundled font draws it, so it shows the .notdef glyph

def characters():
    cs = [chr(c) for c in range(32, 127)] + [chr(c) for c in range(160, 256)]
    return cs + list(EXTRAS) + [chr(c) for a, b in VIETNAMESE for c in range(a, b + 1)]

def draws(f, c):
    """Whether the font has a glyph for c (its mask and advance differ from .notdef)."""
    nd, m = f.getmask(NOTDEF), f.getmask(c)
    return not (m.size == nd.size and bytes(m) == bytes(nd) and abs(f.getlength(c) - f.getlength(NOTDEF)) < 0.01)

def main():
    if any((a in ('-h', '--help') for a in sys.argv[1:])):
        print(__doc__)
        return 0
    try:
        from PIL import ImageFont
    except ImportError:
        print('error: Pillow is missing. Run with the engine Python: uv run --directory <ENGINE> python ...', file=sys.stderr)
        return 2
    exit = {'at': EM, 'fonts': {}}
    for (name, (file, weights)) in MEASURE.items():
        path = os.path.join(FONTS, file)
        if not os.path.exists(path):
            print(f'warning: file not found: {path}', file=sys.stderr)
            continue
        by_weight = {}
        for weight in weights:
            f = ImageFont.truetype(path, EM)
            try:
                axes = f.get_variation_axes()
            except OSError:
                axes = []
            if axes:
                f.set_variation_by_axes([max(axes[0]['minimum'], min(axes[0]['maximum'], weight))])
            companion = COMPANIONS.get(name)
            companion = ImageFont.truetype(os.path.join(FONTS, companion), EM) if companion and os.path.exists(os.path.join(FONTS, companion)) else None
            by_weight[str(weight)] = {c: round((f if draws(f, c) or companion is None or not draws(companion, c) else companion).getlength(c))
                                      for c in characters()}
        exit['fonts'][name] = {'file': f'assets/fonts/{file}', 'weights': by_weight}
    destination = os.path.join(FONTS, 'widths.json')
    with open(destination, 'w', encoding='utf-8') as fh:
        json.dump(exit, fh, ensure_ascii=False, separators=(',', ':'))
    print(f'ok: {destination}')
    return 0
if __name__ == '__main__':
    sys.exit(main())
