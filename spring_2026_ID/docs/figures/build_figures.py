#!/usr/bin/env python3
"""
build_figures.py — Figures for the replication recommendations report and deck.

Emits SVG (for the PDF, which renders vector) and PNG (for the PowerPoint deck,
which cannot embed SVG). Data figures are computed from the recorded data rather
than drawn by hand, so a figure cannot drift from the record:

  Figure 2  spring_2026_ID/docs/REPLICATION_RECOMMENDATIONS_APPENDIX.md  §A4
  Figure 3  spring_2026_ID/findings/ipb_optical_wl_s2n_2026-07-08_to_14.csv
  Figure A1 appendix §A1.3

Figures 1 and 4 are schematics and carry no measured values.

Colour follows the validated two-series palette (blue #2a78d6, orange #eb6834):
worst-pair CVD Delta E 24.7, all six checks pass on a white surface. Every use of
colour is doubled by a second channel — hatching on the orange series, direct
labels, and shape — so the figures survive greyscale printing and colour-vision
deficiency.

Usage:
    .venv-pdf/bin/python figures/build_figures.py
"""

import csv
import math
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
DOCS = HERE.parent
DATA = DOCS.parent / "findings" / "ipb_optical_wl_s2n_2026-07-08_to_14.csv"

W = 468.0                    # 6.5 in at 1 in margins, in points

# ── Palette ──────────────────────────────────────────────────────
INK       = "#0b0b0b"
SECOND    = "#52514e"
MUTED     = "#898781"
GRID      = "#e1e0d9"
AXIS      = "#c3c2b7"
SURFACE   = "#ffffff"
S1        = "#2a78d6"        # categorical slot 1 — blue
S2        = "#eb6834"        # categorical slot 2 — orange
S1_SOFT   = "#e5eefb"
S2_SOFT   = "#fdeae1"
BAND      = "#f4f3f0"

FONT = ("system-ui,-apple-system,'Segoe UI','DejaVu Sans',"
        "'Liberation Sans',Helvetica,Arial,sans-serif")


# ── SVG helpers ──────────────────────────────────────────────────

def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;"))


def txt(x, y, s, size=8, fill=INK, anchor="start", weight="normal",
        style="normal", spacing=None):
    extra = ' font-style="italic"' if style == "italic" else ""
    if spacing:
        extra += ' letter-spacing="%s"' % spacing
    return ('<text x="%.2f" y="%.2f" font-size="%.1f" fill="%s" '
            'text-anchor="%s" font-weight="%s"%s>%s</text>'
            % (x, y, size, fill, anchor, weight, extra, esc(s)))


def wrapped(x, y, s, width_chars, size=8, fill=INK, anchor="start",
            leading=None, weight="normal"):
    """Crude word wrap. Kept crude on purpose: every string here is authored,
    so the wrap points are checked by eye in the rendered output."""
    leading = leading or size * 1.25
    words, lines, cur = s.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if len(trial) > width_chars and cur:
            lines.append(cur)
            cur = w
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return "".join(txt(x, y + i * leading, ln, size, fill, anchor, weight)
                   for i, ln in enumerate(lines)), len(lines)


def rect(x, y, w, h, fill="none", stroke="none", sw=1, rx=0, extra=""):
    return ('<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" rx="%.1f" '
            'fill="%s" stroke="%s" stroke-width="%.2f"%s/>'
            % (x, y, max(w, 0), max(h, 0), rx, fill, stroke, sw,
               (" " + extra) if extra else ""))


def line(x1, y1, x2, y2, stroke=AXIS, sw=0.7, dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ""
    return ('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" '
            'stroke-width="%.2f"%s/>' % (x1, y1, x2, y2, stroke, sw, d))


def svg_open(height, title, desc):
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %.0f %.0f" '
        'width="%.0f" height="%.0f" role="img" '
        'aria-labelledby="figtitle figdesc" font-family="%s">'
        '<title id="figtitle">%s</title><desc id="figdesc">%s</desc>'
        '<rect width="100%%" height="100%%" fill="%s"/>'
        '<defs>'
        '<pattern id="hatch" width="4" height="4" patternUnits="userSpaceOnUse" '
        'patternTransform="rotate(45)">'
        '<rect width="4" height="4" fill="%s"/>'
        '<line x1="0" y1="0" x2="0" y2="4" stroke="%s" stroke-width="1.6"/>'
        '</pattern>'
        '<marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" '
        'markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
        '<path d="M 0 1 L 9 5 L 0 9 z" fill="%s"/></marker>'
        '</defs>'
        % (W, height, W, height, FONT, esc(title), esc(desc), SURFACE,
           S2_SOFT, S2, SECOND))


def write(name, body):
    path = HERE / name
    path.write_text(body + "</svg>\n", encoding="utf-8")
    return path


def panel_label(x, y, letter, text):
    return (txt(x, y, letter, 9, INK, weight="bold")
            + txt(x + 11, y, text, 9, INK, weight="bold"))


# ─────────────────────────────────────────────────────────────────
# Figure 1 — How a measurement is made (schematic, §3.1)
# ─────────────────────────────────────────────────────────────────

def fit(text, width_pt, size, em=0.52):
    """Wrap to a pixel width using an average advance, in em, per character.

    Approximate, but every string in these figures is authored and the result
    is checked in the rendered output, so an exact metric buys nothing. Bold
    runs wider than regular: pass em=0.60 for those.
    """
    chars = max(int(width_pt / (em * size)), 8)
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if len(trial) > chars and cur:
            lines.append(cur)
            cur = w
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines


def box(x, y, w, h, heading, body, accent=S1, fill=SURFACE, size=7.2):
    out = rect(x, y, w, h, fill=fill, stroke=accent, sw=1.2, rx=3)
    out += rect(x, y, w, 3, fill=accent, rx=1.5)
    out += txt(x + w / 2, y + 20, heading, 8.5, INK, "middle", weight="bold")
    for i, ln in enumerate(fit(body, w - 16, size)):
        out += txt(x + w / 2, y + 33 + i * (size * 1.35), ln, size, SECOND, "middle")
    return out


def chip(x, y, w, h, heading, body, size=7):
    out = rect(x, y, w, h, fill=BAND, rx=3)
    out += txt(x + 10, y + 14, heading, 7.6, INK, weight="bold")
    for i, ln in enumerate(fit(body, w - 20, size)):
        out += txt(x + 10, y + 25 + i * (size * 1.35), ln, size, SECOND)
    return out


def arrow_h(x1, x2, y, label=None, color=SECOND):
    out = line(x1, y, x2 - 4, y, color, 1.1)
    out += '<path d="M %.1f %.1f l -5 -3.2 l 0 6.4 z" fill="%s"/>' % (x2, y, color)
    if label:
        out += txt((x1 + x2) / 2, y - 6, label, 7, MUTED, "middle")
    return out


def fig1():
    H = 246
    s = svg_open(
        H, "How a measurement is made",
        "Flow diagram in three stages. A camera on a pole at the river sends "
        "video to a station computer, which works out a water level and a "
        "discharge figure. Both, and the video, travel over the mobile network "
        "to a central server that keeps the record. Three things the station "
        "computer depends on are shown beneath it: a solar panel and battery, a "
        "scheduler that wakes it every 30 minutes, and a rain gauge that keeps "
        "recording while the station sleeps. A note under the camera records "
        "that 30 to 60 seconds of every wake is spent waiting for the camera to "
        "boot, before any video exists.")

    s += txt(0, 14, "Figure 1  How a measurement is made", 10, INK, weight="bold")
    s += txt(0, 28, "The path a single five-second video takes, from the river "
             "to the record.", 8, SECOND)

    bw, bh, by = 128, 66, 46
    xs = [0, 170, 340]

    s += box(xs[0], by, bw, bh, "Camera",
             "On a pole, viewing the river section")
    s += box(xs[1], by, bw, bh, "Station computer",
             "Works out water level and discharge from the video")
    s += box(xs[2], by, bw, bh, "Central server",
             "Keeps the video and the measurement record")

    s += arrow_h(xs[0] + bw + 6, xs[1] - 6, by + bh / 2, "video")
    s += arrow_h(xs[1] + bw + 6, xs[2] - 6, by + bh / 2, "LTE")

    # A note against the camera, since the boot cost is a camera property.
    ny = by + bh + 12
    s += rect(xs[0], ny, bw, 42, fill=SURFACE, stroke=S2, sw=1.1, rx=3)
    for i, ln in enumerate(fit("30–60 s of every wake is spent booting the "
                               "camera, before any video exists.",
                               bw - 14, 6.9)):
        s += txt(xs[0] + 7, ny + 12 + i * 9.5, ln, 6.9, INK)

    # What the station computer depends on.
    dy = by + bh + 56
    s += line(xs[1] + bw / 2, by + bh, xs[1] + bw / 2, dy - 16, MUTED, 0.9, "3 2")
    s += txt(xs[1] + bw / 2, dy - 6, "depends on", 7, MUTED, "middle")

    cw, ch = 150, 40
    s += chip(0, dy, cw, ch, "Solar panel and battery",
              "200 W of panel and a 50 Ah battery at Sukabumi.")
    s += chip(159, dy, cw, ch, "Scheduler",
              "Wakes the station every 30 minutes, then powers it down.")
    s += chip(318, dy, cw, ch, "Rain gauge",
              "Keeps recording rainfall while the station sleeps.")

    fy = dy + ch + 16
    s += rect(0, fy, W, 26, fill=S1_SOFT, rx=3)
    s += txt(10, fy + 16,
             "The station is awake about two minutes in every thirty. "
             "Everything above happens inside that window.", 7.4, INK)

    return write("fig1_system.svg", s)


# ─────────────────────────────────────────────────────────────────
# Figure 2 — The availability record (§4.1)
# ─────────────────────────────────────────────────────────────────

# Appendix §A4. Onset day counted from 2026-04-16; duration in hours;
# `maint` records whether the interruption coincides with a maintenance window.
INTERRUPTIONS = [
    # (label,        onset day, hours, maintenance-associated)
    ("04-17 06:23",    1.27,      4.7,  True),
    ("04-17 15:01",    1.63,      2.1,  True),
    ("04-18 11:33",    2.48,      0.9,  True),
    ("04-19 08:20",    3.35,      4.9,  True),
    ("04-19 14:09",    3.59,     18.3,  True),
    ("04-20 14:13",    4.59,     19.5,  True),
    ("05-02 06:31",   16.27,      1.0,  False),
    ("05-11 23:01",   25.96,     38.0,  True),
    ("05-16 00:47",   30.03,    223.2,  True),   # 9.3 d
    ("06-25 04:30",   70.19,    175.2,  True),   # 7.3 d
    ("07-02 10:43",   77.45,     23.1,  False),
    ("08-15 01:30",  121.06,    129.6,  False),  # 5.4 d
    ("08-20 10:39",  126.44,     21.6,  False),
]
SPAN_DAYS = 134.0


def fig2():
    H = 322
    s = svg_open(
        H, "The availability record, 16 April to 28 August 2026",
        "Two panels. The upper panel is a timeline of the 133.5-day observation "
        "window with each of the 13 interruptions drawn to its true length; nine "
        "coincide with maintenance mode and four do not. The lower panel places "
        "the same 13 on a logarithmic duration scale: nine fall under 24 hours, "
        "one at 38 hours, none at all between 2 and 5 days, and three at 5 days "
        "and over. The empty band between 2 and 5 days is the signature of a "
        "latch: a missed wake either recovers within a day or persists until "
        "something external restarts the station.")

    s += txt(0, 14, "Figure 2  The availability record, 16 April to 28 August 2026",
             10, INK, weight="bold")
    s += txt(0, 28, "13 interruptions across 133.5 days observed. "
             "The gap in the lower panel is the finding.", 8, SECOND)

    # Legend, shared by both panels.
    ly = 42
    s += rect(0, ly - 7, 9, 9, fill=S1, rx=1.5)
    s += txt(13, ly, "Coincides with maintenance mode  (9)", 7.5, INK)
    s += rect(200, ly - 7, 9, 9, fill="url(#hatch)", stroke=S2, sw=0.9, rx=1.5)
    s += txt(213, ly, "Not associated  (4)", 7.5, INK)

    def fill_for(maint):
        return S1 if maint else "url(#hatch)"

    def stroke_for(maint):
        return S1 if maint else S2

    # ── Panel A: timeline ───────────────────────────────────────
    ax0, ax1 = 8, W - 26
    ay, ah = 78, 32
    s += panel_label(0, 64, "A", "Timeline — each interruption drawn to length")
    s += txt(W, 64, "Bars mark when the station was not running.",
             7.2, SECOND, "end")

    s += rect(ax0, ay, ax1 - ax0, ah, fill=BAND, rx=2)

    def dx(day):
        return ax0 + (day / SPAN_DAYS) * (ax1 - ax0)

    # Month ticks. Day numbers are days after 16 April.
    for day, name in ((0, "16 Apr"), (15, "1 May"), (46, "1 Jun"),
                      (76, "1 Jul"), (107, "1 Aug"), (134, "28 Aug")):
        s += line(dx(day), ay, dx(day), ay + ah + 3, AXIS, 0.7)
        # Anchor the end labels inward so they are not clipped by the viewBox.
        anchor = "start" if day == 0 else ("end" if day == 134 else "middle")
        s += txt(dx(day), ay + ah + 13, name, 6.8, MUTED, anchor)

    for label, day, hours, maint in INTERRUPTIONS:
        x = dx(day)
        w = max((hours / 24.0 / SPAN_DAYS) * (ax1 - ax0), 1.6)
        s += rect(x, ay + 3, w, ah - 6, fill=fill_for(maint),
                  stroke=stroke_for(maint), sw=0.8, rx=1)

    # Direct labels on the three long interruptions.
    for label, day, hours, maint, cap in (
            ("", 30.03, 223.2, True, "9.3 d"),
            ("", 70.19, 175.2, True, "7.3 d"),
            ("", 121.06, 129.6, False, "5.4 d")):
        w = (hours / 24.0 / SPAN_DAYS) * (ax1 - ax0)
        s += txt(dx(day) + w / 2, ay - 4, cap, 7, INK, "middle", weight="bold")

    # ── Panel B: duration, log scale ────────────────────────────
    by0 = 150
    s += panel_label(0, by0, "B", "Duration — the same 13 on a logarithmic scale")

    bx0, bx1 = 22, W - 26
    plot_y, plot_h = by0 + 16, 96
    lo, hi = math.log10(0.7), math.log10(320)

    def lx(hours):
        return bx0 + (math.log10(hours) - lo) / (hi - lo) * (bx1 - bx0)

    # The empty band, which is what the panel exists to show.
    s += rect(lx(48), plot_y, lx(120) - lx(48), plot_h, fill=S2_SOFT, rx=2)
    s += txt((lx(48) + lx(120)) / 2, plot_y + 13,
             "no interruption", 6.6, INK, "middle", weight="bold")
    s += txt((lx(48) + lx(120)) / 2, plot_y + 22,
             "fell in this band", 6.6, INK, "middle", weight="bold")

    ticks = [(1, "1 h"), (2, "2 h"), (6, "6 h"), (12, "12 h"), (24, "1 day"),
             (48, "2 days"), (120, "5 days"), (240, "10 days")]
    for v, name in ticks:
        s += line(lx(v), plot_y, lx(v), plot_y + plot_h, GRID, 0.7)
        s += txt(lx(v), plot_y + plot_h + 12, name, 6.8, MUTED, "middle")
    s += line(bx0, plot_y + plot_h, bx1, plot_y + plot_h, AXIS, 0.8)

    # Dodge overlapping dots upward rather than jittering them randomly.
    placed = []
    r = 4.6
    base_y = plot_y + plot_h - 12
    for label, day, hours, maint in sorted(INTERRUPTIONS, key=lambda t: t[2]):
        x = lx(hours)
        row = 0
        while any(abs(x - px) < 2 * r + 1.5 and row == pr for px, pr in placed):
            row += 1
        placed.append((x, row))
        y = base_y - row * (2 * r + 2.5)
        s += ('<circle cx="%.2f" cy="%.2f" r="%.2f" fill="%s" stroke="%s" '
              'stroke-width="1.4"/>'
              % (x, y, r, fill_for(maint), stroke_for(maint) if not maint else S1))

    s += txt(bx0, plot_y + plot_h + 26,
             "9 interruptions under 24 hours   ·   1 at 38 hours   ·   "
             "0 between 2 and 5 days   ·   3 at 5 days and over",
             7.2, SECOND)
    s += txt(bx0, plot_y + plot_h + 37,
             "A missed wake leaves the next-startup alarm in the past and nothing "
             "re-arms it, so an interruption either", 7.2, SECOND)
    s += txt(bx0, plot_y + plot_h + 47,
             "clears within a day or runs until something external restarts the "
             "station.", 7.2, SECOND)

    return write("fig2_availability.svg", s)


# ─────────────────────────────────────────────────────────────────
# Figure 3 — Optical water-level detection (§4.3)
# ─────────────────────────────────────────────────────────────────

GATE = 2.0


def load_optical():
    rows = list(csv.DictReader(open(DATA)))
    by_hour = {h: [0, 0] for h in range(24)}
    values = []
    for r in rows:
        h = int(r["local_hour_wib"])
        ok = r["s2n_passed"] == "1"
        by_hour[h][0 if ok else 1] += 1
        values.append((float(r["s2n"]), ok))
    return by_hour, values


def fig3():
    by_hour, values = load_optical()
    H = 344
    s = svg_open(
        H, "Optical water-level detection at Sukabumi, 8 to 14 July 2026",
        "Two panels, from 200 sampled captures. The upper panel counts captures "
        "by hour of day, split into those that produced a water level and those "
        "rejected at the quality gate. Every rejection falls between 06:00 and "
        "19:00; there are none at night. Within daylight the rejections peak in "
        "mid-morning and again in mid-afternoon, with a dip in the early "
        "afternoon. The lower panel shows the signal-to-noise ratio of all 200 "
        "captures against the gate of 2.0. The rejected captures sit below the "
        "gate with a median of 1.63; the accepted ones spread above it with a "
        "median of 4.01, though 36 of the 100 fall between 2.0 and 3.0, close to "
        "the gate.")

    s += txt(0, 14, "Figure 3  Optical water-level detection, 8 to 14 July 2026",
             10, INK, weight="bold")
    s += txt(0, 28, "200 sampled captures. Each rejection costs the whole "
             "discharge measurement, not only the water level.", 8, SECOND)

    ly = 42
    s += rect(0, ly - 7, 9, 9, fill=S1, rx=1.5)
    s += txt(13, ly, "Water level produced  (100)", 7.5, INK)
    s += rect(180, ly - 7, 9, 9, fill="url(#hatch)", stroke=S2, sw=0.9, rx=1.5)
    s += txt(193, ly, "Rejected at the quality gate  (100)", 7.5, INK)

    # ── Panel A: counts by hour ─────────────────────────────────
    s += panel_label(0, 64, "A", "By hour of day (local time, WIB)")
    ax0, ax1 = 22, W - 8
    ay, ah = 76, 78
    ymax = 14
    step = (ax1 - ax0) / 24.0
    barw = step - 5

    # Shade the hours in which no capture was rejected, so the day/night split
    # is visible without relying on reading bar colours.
    s += rect(ax0, ay, 6 * step, ah, fill=S1_SOFT)
    s += rect(ax0 + 19 * step, ay, 5 * step, ah, fill=S1_SOFT)

    for v in (0, 5, 10):
        yy = ay + ah - (v / ymax) * ah
        s += line(ax0, yy, ax1, yy, GRID, 0.7)
        s += txt(ax0 - 4, yy + 2.5, str(v), 6.5, MUTED, "end")

    for h in range(24):
        p, f = by_hour[h]
        x = ax0 + h * step + 2.5
        hp = (p / ymax) * ah
        hf = (f / ymax) * ah
        if p:
            s += rect(x, ay + ah - hp, barw, hp, fill=S1, rx=1.5)
        if f:
            # 2 pt surface gap between stacked segments, per the mark spec.
            s += rect(x, ay + ah - hp - hf - 2, barw, hf,
                      fill="url(#hatch)", stroke=S2, sw=0.8, rx=1.5)
    s += line(ax0, ay + ah, ax1, ay + ah, AXIS, 0.8)

    for h in range(0, 24, 3):
        s += txt(ax0 + h * step + step / 2, ay + ah + 11, "%02d" % h,
                 6.5, MUTED, "middle")

    s += txt(ax0 + 3 * step, ay + 10, "night", 6.8, S1, "middle", weight="bold")
    s += txt(ax0 + 21.5 * step, ay + 10, "night", 6.8, S1, "middle",
             weight="bold")
    s += txt(ax0, ay + ah + 22,
             "Shaded hours carry no rejection at all. Every rejection falls "
             "between 06:00 and 19:00.", 7.2, SECOND)

    # ── Panel B: the signal-to-noise distribution ───────────────
    s += panel_label(0, 196, "B", "Signal-to-noise ratio of all 200 captures")
    bx0, bx1 = 22, W - 8
    by0, bhh = 210, 82
    lo_v, hi_v = 1.0, 5.75
    binw = 0.25
    bins = {}
    for v, ok in values:
        b = int(v / binw)
        bins.setdefault(b, [0, 0])
        bins[b][0 if ok else 1] += 1
    cmax = 55

    def vx(v):
        return bx0 + (v - lo_v) / (hi_v - lo_v) * (bx1 - bx0)

    for c in (0, 25, 50):
        yy = by0 + bhh - (c / cmax) * bhh
        s += line(bx0, yy, bx1, yy, GRID, 0.7)
        s += txt(bx0 - 4, yy + 2.5, str(c), 6.5, MUTED, "end")

    bw_px = (vx(lo_v + binw) - vx(lo_v)) - 1.5
    for b, (p, f) in sorted(bins.items()):
        x = vx(b * binw)
        if p:
            s += rect(x, by0 + bhh - (p / cmax) * bhh, bw_px,
                      (p / cmax) * bhh, fill=S1, rx=1)
        if f:
            s += rect(x, by0 + bhh - (f / cmax) * bhh, bw_px,
                      (f / cmax) * bhh, fill="url(#hatch)", stroke=S2,
                      sw=0.7, rx=1)
    s += line(bx0, by0 + bhh, bx1, by0 + bhh, AXIS, 0.8)

    for v in (1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5):
        s += txt(vx(v), by0 + bhh + 11, "%.1f" % v, 6.5, MUTED, "middle")
    s += txt(bx1, by0 + bhh + 22, "signal-to-noise ratio", 6.8, MUTED, "end")

    s += line(vx(GATE), by0, vx(GATE), by0 + bhh, INK, 1.1)
    s += txt(vx(GATE) + 5, by0 + 11, "quality gate 2.0", 7, INK, "start",
             weight="bold")
    s += txt(vx(GATE) + 5, by0 + 21, "below it, no water level is reported",
             6.8, SECOND, "start")

    s += txt(bx0, by0 + bhh + 34,
             "Rejected captures are not marginal: median 1.63, and only 23 of "
             "the 100 reach 1.8. Accepted captures", 7.2, SECOND)
    s += txt(bx0, by0 + bhh + 44,
             "spread above the gate with a median of 4.01, though 36 of them "
             "sit between 2.0 and 3.0.", 7.2, SECOND)

    return write("fig3_optical.svg", s)


# ─────────────────────────────────────────────────────────────────
# Figure 4 — Two configurations (schematic, §5 R8)
# ─────────────────────────────────────────────────────────────────

def fig4():
    H = 308
    s = svg_open(
        H, "Two configurations of the same design",
        "Side-by-side comparison. On the left, the configuration as built: "
        "camera, computer, modem and power system all sit in an enclosure at the "
        "riverbank, so all of it is exposed to heat, humidity and dust and "
        "service means opening the enclosure on site. On the right, the "
        "configuration proposed for the pilot units: only the camera stays at "
        "the river, and the computer runs indoors at a BHLK or IPB facility over "
        "a network link, where temperature, humidity, dust and access are "
        "controlled. The right-hand configuration is designed but has not been "
        "field tested.")

    s += txt(0, 14, "Figure 4  Two configurations of the same design", 10, INK,
             weight="bold")
    s += txt(0, 28, "Recommendation R8. The right-hand configuration is "
             "designed but not yet field tested.", 8, SECOND)

    colw = 222
    x2 = W - colw
    top = 48
    colh = 126

    for x, title, sub, band, accent in (
            (0, "As built at Sukabumi", "Everything at the river", BAND, AXIS),
            (x2, "Proposed for the pilot units",
             "Camera at the river, computer indoors", S1_SOFT, S1)):
        s += rect(x, top, colw, 34, fill=band, rx=3)
        s += txt(x + 10, top + 14, title, 8.5, INK, weight="bold")
        s += txt(x + 10, top + 27, sub, 7.2, SECOND)

    ly = top + 42

    # Left column — one enclosure holding everything.
    s += rect(0, ly, colw, colh, fill=SURFACE, stroke=AXIS, sw=1, rx=3)
    s += txt(10, ly + 15, "At the riverbank", 7.4, INK, weight="bold")
    iy = ly + 25
    for it in ("Camera", "Station computer", "Modem",
               "Solar panel, battery and charge controller"):
        lines = fit(it, colw - 32, 6.9)
        hgt = 11 + 9.5 * (len(lines) - 1)
        s += rect(10, iy, colw - 20, hgt + 6, fill=BAND, rx=2)
        for i, ln in enumerate(lines):
            s += txt(16, iy + 11 + i * 9.5, ln, 6.9, INK)
        iy += hgt + 12

    # Right column — the field node and the indoor computer.
    s += rect(x2, ly, colw, 46, fill=SURFACE, stroke=S1, sw=1, rx=3)
    s += txt(x2 + 10, ly + 16, "At the riverbank", 7.4, INK, weight="bold")
    s += txt(x2 + 10, ly + 30, "Camera only, on a network path.", 6.9, SECOND)

    s += line(x2 + 24, ly + 48, x2 + 24, ly + 62, SECOND, 1.1)
    s += ('<path d="M %.1f %.1f l -3.2 -5 l 6.4 0 z" fill="%s"/>'
          % (x2 + 24, ly + 62, SECOND))
    s += txt(x2 + 32, ly + 59, "network link", 6.8, MUTED)

    s += rect(x2, ly + 64, colw, 46, fill=S1_SOFT, stroke=S1, sw=1, rx=3)
    s += txt(x2 + 10, ly + 80, "Indoors, at a BHLK or IPB facility", 7.4, INK,
             weight="bold")
    s += txt(x2 + 10, ly + 94, "Station computer, on mains power.", 6.9, SECOND)

    # One note per column, so nothing has to span the gutter.
    ny = ly + colh + 12
    for x, note, accent in (
            (0, "All of it is in the weather. Service means opening the "
                "enclosure on site.", AXIS),
            (x2, "Only the camera is in the weather. The computer sits at a "
                 "desk.", S1)):
        lines = fit(note, colw - 20, 7)
        s += rect(x, ny, colw, 14 + 10 * len(lines), fill=SURFACE,
                  stroke=accent, sw=0.9, rx=3)
        for i, ln in enumerate(lines):
            s += txt(x + 10, ny + 14 + i * 10, ln, 7, INK)

    fy = ny + 46
    s += rect(0, fy, W, 26, fill=BAND, rx=3)
    s += txt(10, fy + 16,
             "Site permission asked for: an enclosure, a battery, a modem and a "
             "pole  —  against a camera and a network path.", 7.2, INK)

    return write("fig4_configurations.svg", s)


# ─────────────────────────────────────────────────────────────────
# Figure A1 — The capture path (appendix §A1)
# ─────────────────────────────────────────────────────────────────

def figA1():
    H = 282
    s = svg_open(
        H, "The capture path: intended against implemented",
        "Two paths compared. The intended path had the camera record to its own "
        "card at full bitrate and the station pull the finished file over "
        "Ethernet faster than real time; the single interface call that needs is "
        "absent from the rebranded firmware, so the path is blocked. The "
        "implemented path pulls a live stream instead, which carries 10 to 20 "
        "per cent transport overhead. A bar chart compares the three bitrates: "
        "20 Mbps recommended by the processing chain, 16 Mbps configured on the "
        "camera, and about 15.5 Mbps actually delivered.")

    s += txt(0, 14, "Figure A1  The capture path: intended against implemented",
             10, INK, weight="bold")
    s += txt(0, 28, "The limitation is in the firmware, not in the optics or "
             "the sensor.", 8, SECOND)

    bw, bh = 136, 40
    gap = 30

    def stage(x, y, label, sub, accent=S1, fill=SURFACE):
        out = rect(x, y, bw, bh, fill=fill, stroke=accent, sw=1.1, rx=3)
        out += txt(x + 8, y + 15, label, 7.4, INK, weight="bold")
        for i, ln in enumerate(fit(sub, bw - 16, 6.7)):
            out += txt(x + 8, y + 26 + i * 9, ln, 6.7, SECOND)
        return out

    # Intended path.
    y1 = 48
    s += txt(0, y1 - 4, "Intended — record to card, then pull the file", 7.8,
             INK, weight="bold")
    xs = [0, bw + gap, 2 * (bw + gap)]
    s += stage(xs[0], y1 + 6, "Camera records", "to its own card at full bitrate")
    s += stage(xs[1], y1 + 6, "Station pulls the file",
               "over Ethernet, faster than real time", accent=S2, fill=S2_SOFT)
    s += stage(xs[2], y1 + 6, "20 Mbps to disk", "no transport overhead")
    for x in xs[:2]:
        s += arrow_h(x + bw + 4, x + bw + gap - 4, y1 + 6 + bh / 2)

    s += ('<path d="M %.1f %.1f l %.1f %.1f M %.1f %.1f l %.1f %.1f" '
          'stroke="%s" stroke-width="2.2" stroke-linecap="round"/>'
          % (xs[1] + bw - 16, y1 + 12, 10, 10, xs[1] + bw - 6, y1 + 12, -10, 10,
             S2))
    blocked = ("Blocked: the one interface call this needs is absent from the "
               "rebranded firmware.")
    for i, ln in enumerate(fit(blocked, W - xs[1], 6.9, em=0.60)):
        s += txt(xs[1], y1 + bh + 20 + i * 9.5, ln, 6.9, S2, "start",
                 weight="bold")

    # Implemented path.
    y2 = 132
    s += txt(0, y2 - 4, "Implemented — pull a live stream", 7.8, INK,
             weight="bold")
    s += stage(xs[0], y2 + 6, "Camera streams", "live, 16 Mbps configured")
    s += stage(xs[1], y2 + 6, "Transport overhead", "10–20% of the configured rate")
    s += stage(xs[2], y2 + 6, "15.5 Mbps to disk", "against 20 Mbps recommended")
    for x in xs[:2]:
        s += arrow_h(x + bw + 4, x + bw + gap - 4, y2 + 6 + bh / 2)

    # The three rates, on one axis.
    cy = y2 + bh + 26
    s += line(0, cy - 6, W, cy - 6, GRID, 0.8)
    s += txt(0, cy + 6, "Delivered bitrate", 7.6, INK, weight="bold")
    bars = [("Recommended by the processing chain", 20.0, MUTED),
            ("Configured on the camera", 16.0, MUTED),
            ("Actually delivered", 15.5, S1)]
    bx = 160
    bwidth = W - bx - 62
    by = cy + 14
    for label, v, col in bars:
        s += txt(0, by + 8, label, 6.9, SECOND)
        s += rect(bx, by, bwidth * v / 20.0, 11, fill=col, rx=2)
        s += txt(bx + bwidth * v / 20.0 + 5, by + 8.5, "%.1f Mbps" % v, 6.9,
                 INK, weight="bold" if col == S1 else "normal")
        by += 17

    return write("figA1_capture_path.svg", s)


def main():
    for fn in (fig1, fig2, fig3, fig4, figA1):
        print("wrote", fn().name)
    for png in rasterise():
        print("wrote", png.parent.name + "/" + png.name)


# Every figure reserves the same band at the top for its drawn heading and
# subtitle: the title baseline sits at y=14, the subtitle at y=28, and no
# content begins above y=42.
HEADER_BAND = 36


def rasterise(scale=3.0, drop_header=True):
    """PNG copies for the slide deck, which cannot embed SVG.

    Scale 3 puts a 468 pt figure at 1404 px, which is over 200 dpi at the 5 to
    7 inch widths the slides use.

    The drawn heading is cropped off by default. In the report the heading is
    the figure's label; on a slide the slide title already says it, and two
    headings a centimetre apart read as a mistake.
    """
    import cairosvg
    from PIL import Image

    out = HERE / "png"
    out.mkdir(exist_ok=True)
    made = []
    for svg in sorted(HERE.glob("*.svg")):
        png = out / (svg.stem + ".png")
        cairosvg.svg2png(url=str(svg), write_to=str(png), scale=scale,
                         background_color="white")
        if drop_header:
            with Image.open(png) as im:
                im.crop((0, int(HEADER_BAND * scale), im.width,
                         im.height)).save(png)
        made.append(png)
    return made


if __name__ == "__main__":
    main()
