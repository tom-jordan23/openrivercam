#!/usr/bin/env python3
"""
prepare_logos.py — Normalise partner logos to the spec in README.md.

Records where each mark came from, so provenance is not lost. Run from docs/:

    .venv-pdf/bin/python logos/prepare_logos.py

Each source is trimmed to its artwork and given a transparent background, so the
layout's own spacing is the only spacing. Marks are NOT redrawn, recoloured or
altered in shape — only background removal and cropping.
"""

import sys
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
DOWNLOADS = Path.home() / "Downloads"
TEMPLATE = Path("/home/tjordan/code/templates/AmCross/English PowerPoint "
                "Templates/502201-04 Red Cross Classic Template FINAL.pptx")


def trim(im, threshold=250):
    """Crop to the artwork, treating near-white as background where there is no
    usable alpha channel."""
    im = im.convert("RGBA")
    alpha = im.split()[3]
    if alpha.getextrema()[0] == 255:            # fully opaque: derive from white
        rgb = im.convert("RGB")
        mask = rgb.point(lambda v: 0 if v >= threshold else 255).convert("L")
        im.putalpha(mask)
        alpha = mask
    box = alpha.getbbox()
    return im.crop(box) if box else im


def circular_alpha(im, inset=2):
    """Keep the inscribed circle and drop everything outside it.

    For a circular mark supplied on a solid square background — cropping to the
    circle is the only way to remove that background without touching the mark
    itself.
    """
    from PIL import ImageDraw
    im = im.convert("RGBA")
    w, h = im.size
    d = min(w, h) - inset * 2
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).ellipse(
        [(w - d) // 2, (h - d) // 2, (w + d) // 2, (h + d) // 2], fill=255)
    im.putalpha(mask)
    return im.crop(mask.getbbox())


def arc_from_template():
    """The American Red Cross horizontal lockup, from the template we build on.

    ppt/media/image1.png is the mark plus wordmark; image2.png is the mark alone.
    The lockup is the one that matches how PMI and IPB supply theirs.
    """
    import io, zipfile
    with zipfile.ZipFile(TEMPLATE) as z:
        return Image.open(io.BytesIO(z.read("ppt/media/image1.png")))


SOURCES = [
    ("pmi.png",     lambda: Image.open(DOWNLOADS / "pmi.png"),  trim,
     "supplied by tjordan"),
    ("ipb.png",     lambda: Image.open(DOWNLOADS / "ipb.png"),  trim,
     "supplied by tjordan"),
    ("bhlk.png",    lambda: Image.open(DOWNLOADS / "bhlk.jpeg"), circular_alpha,
     "supplied by tjordan; circular mark on a black square, cropped to the circle"),
    ("amcross.png", arc_from_template,                          trim,
     "ppt/media/image1.png from the Red Cross Classic template"),
]


def main():
    for name, load, clean, note in SOURCES:
        try:
            im = load()
        except FileNotFoundError as exc:
            print("SKIP %-12s %s" % (name, exc))
            continue
        out = clean(im)
        out.save(HERE / name)
        print("%-12s %-12s %s" % (name, "%dx%d" % out.size, note))


if __name__ == "__main__":
    main()
