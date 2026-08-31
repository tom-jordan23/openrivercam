# Partner logos

Movement convention: **all parties get equal billing.** PMI, IPB, BHLK and the
American Red Cross appear at the same size, in the same row, with the same spacing
on every deliverable.

## What is needed here

Drop the four files in, named exactly as below. `build_deck.py` and the report
build pick them up automatically; when a file is missing, that organisation is
carried by name only and the row is still laid out equally for whoever is present.

| File | Organisation |
|---|---|
| `pmi.png` | Palang Merah Indonesia |
| `ipb.png` | Institut Pertanian Bogor |
| `bhlk.png` | Balai Hidrologi dan Lingkungan Keairan |
| `amcross.png` | American Red Cross |

## Specification

- **PNG with transparency**, or SVG. Height at least 400 px; width whatever the
  mark needs.
- **Trimmed to the artwork** — no built-in padding. The layout adds its own
  spacing, and baked-in margins make one logo look smaller than its neighbours,
  which is the thing the convention exists to prevent.
- Horizontal lockups where the organisation has one. Marks with very different
  aspect ratios are normalised by height, so a tall stacked mark will read as
  smaller than a wide one.
- Use the **official asset from each organisation**. Do not redraw or trace a
  mark. The PMI emblem in particular is a Red Cross national society emblem,
  protected under the Geneva Conventions and the Indonesian implementing law;
  only the official artwork, used with PMI's permission, is appropriate.

## Where they appear

- Report: title page, above the document title.
- Deck: title slide, and the footer band of every content slide.

The American Red Cross template supplies its own logo on the slide master and
centres it alone on the title slide. Both are replaced by the four-logo row so
that no single organisation is given the primary position.
