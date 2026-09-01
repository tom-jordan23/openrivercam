#!/usr/bin/env python3
"""Wrap the artifact-format report in a real HTML document for printing.

The committed .html is artifact source: no doctype, no <html>/<head>/<body> -
those are supplied at publish time. It is also theme-aware, so a headless render
can pick up the OS dark palette. This wrapper pins the light theme, adds the
print rules the screen version has no need for, and changes nothing else.
"""
import sys
from pathlib import Path

src = Path(sys.argv[1]).read_text()

# The three headline-figure labels carry a hand-placed <br> tuned to the screen
# column. At print width it breaks in the wrong place, so let them wrap freely.
# A space, never display:none - that would join the words either side of it.
import re
src = re.sub(r'(<div class="l">[^<]*)<br>', r'\1 ', src)
out = Path(sys.argv[2])

PRINT_CSS = """
<style>
  @page { size: A4; margin: 15mm 14mm 16mm; }
  html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  html, body { background: #ffffff !important; }
  body { font-size: 10.6pt; line-height: 1.55; margin: 0; }
  .wrap { max-width: none; padding: 0; }
  header.masthead { padding-top: 0; }
  h1 { font-size: 20pt !important; }
  .standfirst { font-size: 12pt; }
  h2 { font-size: 16pt; }
  h3 { font-size: 11.5pt; }
  .fig .n { font-size: 21pt; }
  #tip { display: none !important; }

  /* shadows read as grey smudge in print */
  .figures, .panel, .callout, .ledger { box-shadow: none !important; }

  /* The ledger and the figure band draw hairlines as a 1px grid gap over a
     background. Across a page break that background paints as a grey band with
     no content in it, so print gets real borders instead. */
  .ledger, .figures { background: transparent !important; gap: 0 !important; }
  .claim { border-bottom: 1px solid var(--rule); }
  .claim:last-child { border-bottom: none; }
  .figures .fig + .fig { border-left: 1px solid var(--rule); }

  /* The figure labels' fixed line breaks are removed in the markup below, not
     here - display:none on a <br> joins the words with no space. */
  .fig .l { font-size: 8pt; letter-spacing: .06em; }

  /* keep atomic blocks whole - but let the day table flow, its header repeats */
  figure, .panel, .figures, .callout, .claim,
  ul.items li, tr { break-inside: avoid; }
  h1, h2, h3 { break-after: avoid; }
  section { break-inside: auto; }
  thead { display: table-header-group; }

  /* the chart and the ledger are the two things worth a clean page */
  section:nth-of-type(2) figure { break-before: auto; }

  a { color: inherit; text-decoration: none; }
  footer { break-inside: avoid; }
</style>
"""

out.write_text(
    '<!doctype html>\n<html lang="en" data-theme="light">\n<head>\n'
    '<meta charset="utf-8">\n'
    '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
    '<style>body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>\n'
    + src.split("<div class=\"wrap\">")[0]      # title, font links, page styles
    + PRINT_CSS
    + '</head>\n<body>\n'
    + '<div class="wrap">' + src.split("<div class=\"wrap\">", 1)[1]
    + '\n</body>\n</html>\n'
)
print(f"wrote {out} ({out.stat().st_size} bytes)")

# Render:
#   ./build_report_pdf.py sukabumi_duty_cycle_2026-08-28_outage.html /tmp/print.html
#   google-chrome --headless=new --disable-gpu --no-pdf-header-footer \
#       --virtual-time-budget=20000 --run-all-compositor-stages-before-draw \
#       --print-to-pdf=sukabumi_duty_cycle_2026-08-28_outage.pdf /tmp/print.html
