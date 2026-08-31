#!/usr/bin/env python3
"""
build_deck.py — Companion slide deck for the replication recommendations report.

Derived from docs/REPLICATION_RECOMMENDATIONS.md. The report is the source of
record; this script holds only the slide-level summary of it. Scope matches the
report: technology only. How the output is applied is for IPB, BHLK and their
partners, and nothing here draws a hydrology conclusion.

Usage:
    ./build_deck.py                                  # neutral template
    ./build_deck.py --template /path/to/amcross.pptx # branded
    ./build_deck.py -o pdf/REPLICATION_BRIEFING.pptx

Requires python-pptx:
    uv pip install --python .venv-pdf/bin/python python-pptx
"""

import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PHOTOS = HERE.parent / "build_photos"
IMAGES = HERE / "images"

try:
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from pptx.enum.shapes import PP_PLACEHOLDER
except ImportError:
    sys.exit("python-pptx not installed. See the header of this script.")

DOC_TITLE = "Recommendations for Replication of the OpenRiverCam Station Design"
SUBTITLE = "Response to the PMI / IPB / BHLK meeting, Sukabumi, 21 August 2026"
PARTNERS = "Palang Merah Indonesia  ·  Institut Pertanian Bogor  ·  Balai Hidrologi dan Lingkungan Keairan"
FOOTER = "ORC Indonesia Deployment — PMI / IPB / BHLK"
STATUS = "Draft for internal review — not yet circulated"

INK = RGBColor(0x1A, 0x1A, 0x1A)
SECOND = RGBColor(0x42, 0x41, 0x3E)
MUTED = RGBColor(0x6B, 0x6A, 0x66)

# The Red Cross templates ship with example slides. Anything shipped in the
# repo alongside this script names the template it was built from.
DEFAULT_TEMPLATE = ("/home/tjordan/code/templates/AmCross/English PowerPoint "
                    "Templates/502201-04 Red Cross Classic Template FINAL.pptx")


# ── Slide content ────────────────────────────────────────────────
# Each entry is (kind, payload). Kinds: title, section, bullets, table.
# Bullet tuples are (level, text). Level 0 is a top-level point.

DECK = [
    ("title", {}),

    ("bullets", {
        "title": "Scope of this briefing",
        "bullets": [
            (0, "The technology only: the station as built, what it did in the field, and "
                "what should change before duplicate units are constructed."),
            (0, "Not in scope: what the data is fit to support, or what accuracy any given "
                "application demands."),
            (1, "Those judgements are for IPB, BHLK and their federal partners."),
            (1, "Measurement requirements shown here are recorded from them, not proposed "
                "by us."),
            (0, "Source: the full report and its appendix, circulated with this deck."),
        ],
    }),

    ("bullets", {
        "title": "Three offers were made on 21 August. All three are welcomed.",
        "bullets": [
            (0, "Duplicate one to three ORC devices as a pilot."),
            (1, "Supported. This deck is what we would change first."),
            (0, "Provide server capacity for ORC data."),
            (1, "Well matched to the pilot, with a clear data-sovereignty benefit. Two "
                "operational constraints to plan for."),
            (0, "Relocate the present site to an open area free of obstruction."),
            (1, "Supported. The field record adds independent evidence for it."),
        ],
    }),

    ("bullets", {
        "title": "What is being offered for study",
        "bullets": [
            (0, "PoE camera on a pole, Raspberry Pi 5 in a weatherproof enclosure, "
                "on-station processing, LTE upload. Commodity parts throughout."),
            (0, "USD 1,340 in materials solar; approximately USD 1,030 mains-powered."),
            (1, "Materials only — excludes shipping, duty, labour, pole, civil works, survey."),
            (0, "Lowest-cost automatic water-level station on the INAPROC e-catalogue: "
                "approximately USD 3,600 ex-VAT, stage only."),
            (0, "Five constraints governed every part: commodity electronics, no soldering, "
                "no specialist skills, common tools, five-minute replacement."),
        ],
    }),

    ("photos", {
        "title": "Commodity parts, and no fabrication anywhere in the build",
        "photos": [
            (PHOTOS / "sukabumi" / "IMG_0048.png",
             "The parts for one station, before assembly.",
             "Components laid out on a workbench: enclosure mounting plate, two "
             "lengths of DIN rail, three fuse holders, the PoE camera, the rain "
             "gauge dome, a Raspberry Pi 5 with its GPIO terminal riser, a DC-DC "
             "converter, terminal blocks, a relay board, the LTE modem and its "
             "antenna."),
            (IMAGES / "sukabumi" / "complete-system-before-power.png",
             "The same parts wired onto the plate, under bench power at 12.08 V.",
             "The same components assembled onto the mounting plate and wired: "
             "Pi 5 and PoE switch on the upper DIN rail, relays, terminal blocks "
             "and DC-DC converter on the lower rail, with a bench power supply "
             "alongside reading 12.08 volts."),
        ],
        "note": "Every connection is a screw terminal, a plug or a header. That "
                "is what makes the design duplicable.",
    }),

    ("figure", {
        "title": "How a measurement is made",
        "image": "fig1_system.png",
        "alt": "Flow diagram. A camera on a pole at the river sends video to a "
               "station computer, which works out a water level and a discharge "
               "figure; both travel over LTE to a central server that keeps the "
               "record. Beneath the computer are the three things it depends on: "
               "a solar panel and battery, a scheduler that wakes it every 30 "
               "minutes, and a rain gauge that keeps recording while the station "
               "sleeps. A note records that 30 to 60 seconds of every wake is "
               "spent booting the camera before any video exists.",
    }),

    ("bullets", {
        "title": "The evidence base is narrow, and should be treated as such",
        "bullets": [
            (0, "One deployed station, at Sukabumi, on one river."),
            (0, "Part of one season — 133.5 days, 16 April to 28 August 2026."),
            (0, "A second station was built but never deployed."),
            (0, "The calibration now running is a salvage calibration recovered from a "
                "failed survey."),
            (0, "Sukabumi is a technology pilot. Its value to date is what it has revealed "
                "about the design, not the measurements it produced."),
        ],
    }),

    ("section", {"title": "What the pilot requires of the design",
                 "kicker": "Report §2"}),

    ("bullets", {
        "title": "Three properties of the technology constrain any duplicate unit",
        "bullets": [
            (0, "Surface velocimetry depends on trackable features on the water surface."),
            (1, "Performance follows surface state, not the camera. Not characterised at "
                "Sukabumi — measure it at the pilot sites."),
            (0, "The surveyed geometry is an input the processing chain cannot recover."),
            (1, "Nothing in the video constrains the bed, so survey error passes straight "
                "through to the result."),
            (0, "Reporting cadence is a design parameter, separate from measurement quality."),
            (1, "Set by the power architecture. Every wake pays a fixed 30–60 s camera boot."),
        ],
    }),

    ("section", {"title": "Field record, April to August 2026",
                 "kicker": "Report §4 — read as properties of the design"}),

    ("figure", {
        "title": "13 interruptions across 133.5 days. The distribution is the finding.",
        "image": "fig2_availability.png",
        "alt": "Two panels. The upper panel is a timeline of the 133.5-day "
               "observation window with each of the 13 interruptions drawn to "
               "its true length; nine coincide with maintenance mode and four do "
               "not. The lower panel places the same 13 on a logarithmic "
               "duration scale: nine fall under 24 hours, one at 38 hours, none "
               "at all between 2 and 5 days, and three at 5 days and over.",
        "note": "Nine under a day, three at five days or more, and nothing in "
                "between.",
    }),

    ("bullets", {
        "title": "The absent middle is the signature of a latch",
        "bullets": [
            (0, "A missed wake leaves the scheduler's next-startup alarm in the past, and "
                "nothing re-arms it."),
            (0, "So the station either catches the next cycle within a day, or stops until "
                "something external restarts it. The three long ones ran 5.4, 7.3 and 9.3 days."),
            (0, "Two separable faults:"),
            (1, "The trigger — whatever kills the individual wake. A power sizing question."),
            (1, "The latch — the failure to re-arm. A scheduler question."),
            (0, "Fixing the latch converts an open-ended interruption into a 30-minute one, "
                "whatever the trigger was. It is the cheaper half and the higher-value one."),
        ],
    }),

    ("bullets", {
        "title": "Maintenance mode coincides with nine of the thirteen",
        "bullets": [
            (0, "A remotely-set flag that suppresses capture and holds the processor awake "
                "for the full window — roughly 12× the energy of a normal wake, and no data."),
            (0, "Long-wake events: 1.59 per hour inside maintenance windows against 0.18 "
                "per hour outside. The nine include the two longest interruptions."),
            (0, "The design defect is that the mode has no expiry and no alarm."),
            (1, "It persists until explicitly cleared, indicates nowhere that it is set, and "
                "its energy cost is invisible."),
            (0, "Four interruptions are not associated with the mode. Two remain unexplained."),
        ],
    }),

    ("bullets", {
        "title": "Nothing in the design reported any of it",
        "bullets": [
            (0, "No mechanism existed by which an interruption could announce itself."),
            (0, "The record could only be reconstructed afterwards, by querying the database "
                "directly."),
            (0, "A fault the system does not report cannot be detected by monitoring it."),
            (0, "This is the common thread behind R4, R5 and R7, and it is the cheapest "
                "class of change in the whole set."),
        ],
    }),

    ("figure", {
        "title": "Optical water-level detection fails throughout daylight",
        "image": "fig3_optical.png",
        "alt": "Two panels from 200 sampled captures. The upper panel counts "
               "captures by hour of day, split into those that produced a water "
               "level and those rejected at the quality gate; every rejection "
               "falls between 06:00 and 19:00, with peaks mid-morning and "
               "mid-afternoon and a dip in the early afternoon. The lower panel "
               "shows the signal-to-noise ratio of all 200 captures against the "
               "gate of 2.0.",
        "note": "The two peaks and the midday dip are the shape a sun-angle "
                "effect produces. A general brightness effect would not.",
    }),

    ("bullets", {
        "title": "Optical water-level detection fails throughout daylight",
        "bullets": [
            (0, "Of 200 sampled captures, 8–14 July, every failure was rejected at the same "
                "quality gate."),
            (0, "Passing captures cluster at a signal-to-noise ratio of 3–5, failing ones at "
                "1.3–1.8, with almost nothing between."),
            (1, "The gate is separating good captures from bad. Lowering it would admit "
                "unreliable levels, not recover good ones."),
            (0, "Zero failures between 19:00 and 06:00 WIB. Within daylight, two peaks — "
                "mid-morning and mid-afternoon — with a dip at solar noon."),
        ],
    }),

    ("bullets", {
        "title": "What that costs, and what is not yet established",
        "bullets": [
            (0, "Water-level estimation aborts the entire processing run, so each daytime "
                "failure costs the whole discharge measurement, not only the level."),
            (0, "The failure is measured and not in doubt."),
            (0, "Its cause is a well-supported hypothesis, not a settled result: specular "
                "sun glint, indicated by the midday dip. Visual confirmation is pending."),
            (0, "The recommendation depends only on the failure, not on the mechanism."),
        ],
    }),

    ("bullets", {
        "title": "Half of all captured video never reached the server",
        "bullets": [
            (0, "Of 5,406 videos recorded 8 April to 27 August, 51% were never synchronised. "
                "Separately, 43% failed processing on the station."),
            (0, "The station disk sat pinned at its automatic purge threshold, so records "
                "were deleted before they could be retransmitted."),
            (0, "Nothing compared what was captured against what arrived, so this produced "
                "no symptom at either end."),
            (0, "Video and sensor data travel independent paths and fail independently. "
                "Neither confirms the other. Both have been observed here."),
        ],
    }),

    ("section", {"title": "What the cost ceiling bought",
                 "kicker": "Report §3 — the method, not the part"}),

    ("bullets_photo", {
        "title": "The camera met its specification. Three consequences followed.",
        "bullets": [
            (0, "USD 60 per unit against a professional alternative at about "
                "USD 1,268."),
            (0, "Recorded video cannot be retrieved over HTTP, so capture falls "
                "back to a live stream."),
            (0, "A white light fires at full brightness on every power-on and "
                "cannot be disabled."),
            (0, "Boot time is fixed and paid on every wake — 30–60 s."),
            (0, "All three are properties of the rebranded firmware, not of the "
                "optics or the sensor."),
        ],
        "photo": IMAGES / "components" / "annke_c1200_camera.png",
        "caption": "The camera as delivered: capable hardware, a reseller's "
                   "firmware.",
        "alt": "The PoE camera as delivered, on a workbench mat with its "
               "mounting hardware, waterproof cable boot and printed user "
               "manual.",
    }),

    ("figure", {
        "title": "What the firmware costs the capture path",
        "image": "figA1_capture_path.png",
        "alt": "Two paths compared. The intended path had the camera record to "
               "its own card at full bitrate and the station pull the finished "
               "file over Ethernet faster than real time; the single interface "
               "call that needs is absent from the rebranded firmware, so the "
               "path is blocked. The implemented path pulls a live stream "
               "instead, which carries 10 to 20 per cent transport overhead. A "
               "bar chart compares 20 Mbps recommended, 16 Mbps configured, and "
               "about 15.5 Mbps delivered.",
        "note": "The hardware could do it. The firmware will not expose it.",
    }),

    ("bullets", {
        "title": "The lesson is about method, not about the part",
        "bullets": [
            (0, "The ceiling was applied component by component: for each function, the "
                "cheapest part meeting the stated requirement."),
            (0, "That is defensible, and it produced a working station at USD 1,340."),
            (0, "It has one failure mode, which this deployment demonstrated: it prices each "
                "component against its datasheet, and not against what that component's "
                "limitations cost the rest of the system."),
            (0, "Keep the per-station ceiling — it is what makes network density achievable. "
                "Apply it to the station rather than to each part in isolation."),
        ],
    }),

    ("section", {"title": "Recommendations for the pilot units",
                 "kicker": "Report §5 — eleven, ordered by effect on reliability and data quality"}),

    ("table", {
        "title": "R1–R6",
        "columns": ["#", "Recommendation", "Cost of adoption"],
        "rows": [
            ["R1", "Fit an independent water-level reference",
             "Level sensor, or a staff gauge in view"],
            ["R2", "Commission a professional survey before installation",
             "Rp 5–15 million per site"],
            ["R3", "Build to interfaces, not to part numbers",
             "Documentation only"],
            ["R4", "Health telemetry and mode alarms as functional requirements",
             "Negligible"],
            ["R5", "Push diagnostics rather than requiring a login",
             "Small"],
            ["R6", "Instrument power; record voltage and current as pairs",
             "Current-sense module and logging"],
        ],
    }),

    ("table", {
        "title": "R7–R11",
        "columns": ["#", "Recommendation", "Cost of adoption"],
        "rows": [
            ["R7", "Reconcile captured against received data automatically",
             "Negligible"],
            ["R8", "Consider indoor compute for the pilot units",
             "Designed, not yet field tested"],
            ["R9", "Budget per station; check the control interface before buying",
             "Screening effort; higher per-camera price"],
            ["R10", "Use the native RTC instead of an external scheduling board",
             "Saves ~USD 50/station; keep the board on solar"],
            ["R11", "Where real-time monitoring is required, build always-on and mains-powered",
             "Cheaper — ~USD 1,030 against 1,340"],
        ],
    }),

    ("figure", {
        "title": "R8 — camera at the river, computer indoors",
        "image": "fig4_configurations.png",
        "alt": "Side-by-side comparison. On the left, the configuration as "
               "built: camera, computer, modem and power system all sit in an "
               "enclosure at the riverbank, so all of it is in the weather and "
               "service means opening the enclosure on site. On the right, the "
               "configuration proposed for the pilot units: only the camera "
               "stays at the river and the computer runs indoors at a BHLK or "
               "IPB facility over a network link.",
        "note": "Designed, not yet field tested. It is offered as the pilot's "
                "first experiment.",
    }),

    ("bullets", {
        "title": "The four with the greatest effect",
        "bullets": [
            (0, "R1 — without an independent water-level reference the station measures "
                "reliably only at night, and the same block of hours is missing every day."),
            (0, "R2 — two RTK surveys, consecutive days, same equipment and crew, reproduced "
                "spreads of ~99 cm horizontal and ~139 cm vertical. Roughly 30× tolerance."),
            (0, "R3 — BHLK will source in Indonesia under Indonesian procurement rules, so "
                "substitution is the expected case, not a risk to be managed."),
            (0, "R11 — the duty cycle is the common cause behind much of the field record, "
                "and the always-on configuration is the cheaper of the two."),
        ],
    }),

    ("bullets", {
        "title": "Data hosting",
        "bullets": [
            (0, "The server is a containerised deployment, straightforward to stand up on "
                "BHLK infrastructure."),
            (0, "Two constraints established in practice, to design for rather than discover:"),
            (1, "Video storage and the database must share a filesystem. Plan them as one volume."),
            (1, "Server and station software versions are coupled. A duty-cycled remote "
                "station cannot be upgraded on demand."),
            (0, "We would propose mirroring in parallel until the BHLK instance has completed "
                "a full operating cycle, including an upgrade."),
            (0, "Worth agreeing in writing: where the authoritative copy sits, who "
                "administers it, who has access, retention and backup."),
        ],
    }),

    ("bullets", {
        "title": "Site selection",
        "bullets": [
            (0, "An open site addresses three separate problems at once:"),
            (1, "GNSS multipath and sky obstruction — among the leading candidate causes of "
                "the survey noise at the present urban canal site."),
            (1, "Camera-to-sun geometry — a site free to choose azimuth can avoid the "
                "alignment through more of the day."),
            (1, "View geometry across the section, which sets how much of the flow the "
                "camera resolves."),
            (0, "A move costs a re-survey and a re-calibration. The survey is the expensive part."),
            (0, "Written site permission should be in hand before any unit is built for a "
                "specific site."),
        ],
    }),

    ("bullets", {
        "title": "Division of responsibility",
        "bullets": [
            (0, "BHLK — data processing, standards conformance, and the route to acceptance "
                "within PUPR data systems. Offers server capacity."),
            (0, "IPB — design, calibration methodology, training material, and the pipeline "
                "for future sensor types."),
            (0, "PMI — user of the derived information, and the operational side: "
                "installation, maintenance, incident response, spares at the local chapter."),
            (0, "Two suggestions: write the split into the collaboration agreement, and keep "
                "a lightweight joint forum for cases that do not sort into one role."),
            (0, "The commitments this implies for PMI have not been discussed with PMI "
                "National Headquarters."),
        ],
    }),

    ("bullets", {
        "title": "Open questions",
        "bullets": [
            (0, "The cause of the two unexplained interruptions."),
            (0, "Whether the recovery-voltage setting bounds interruption duration. One "
                "observation is not a result."),
            (0, "Whether a staff gauge can be read from the camera image to sufficient "
                "precision. If it can, R1 needs no separate sensor."),
            (0, "Absolute discharge accuracy at Sukabumi, unresolved pending the survey."),
            (0, "Velocimetry performance across the surface conditions the pilot sites present."),
        ],
    }),
]


# ── Rendering ────────────────────────────────────────────────────
# Written against the American Red Cross Classic template, whose slides are
# 10 x 5.62 in with a 3.35 in body. Everything is positioned from the layout's
# own placeholders rather than from fixed offsets, so a different template's
# geometry is followed rather than overridden.

CHROME = (PP_PLACEHOLDER.FOOTER, PP_PLACEHOLDER.SLIDE_NUMBER, PP_PLACEHOLDER.DATE)


def find_layout(prs, *names, fallback=1):
    """Look a layout up by name across the template's masters, then by index."""
    wanted = [n.lower() for n in names]
    for master in prs.slide_masters:
        for layout in master.slide_layouts:
            if layout.name.lower() in wanted:
                return layout
    layouts = prs.slide_layouts
    return layouts[fallback] if fallback < len(layouts) else layouts[0]


def is_chrome(shape):
    """Footer, date and slide-number placeholders, which the template manages."""
    if not shape.is_placeholder:
        return False
    try:
        return shape.placeholder_format.type in CHROME
    except ValueError:
        return False


def body_placeholders(slide):
    """Content placeholders, in layout order, excluding title and chrome.

    python-pptx hands back a fresh proxy on each access, so the title has to be
    identified by its underlying element rather than by object identity.
    """
    title = slide.shapes.title
    title_el = title._element if title is not None else None
    out = []
    for ph in slide.placeholders:
        if ph._element is title_el or is_chrome(ph) or not ph.has_text_frame:
            continue
        out.append(ph)
    return out


def layout_chrome(slide):
    """Footer and slide-number rectangles as the template's layout defines them.

    python-pptx does not clone footer, date or slide-number placeholders onto a
    new slide, so their geometry has to be read back off the layout in order to
    put anything in those positions.
    """
    footer = number = None
    for ph in slide.slide_layout.placeholders:
        try:
            kind = ph.placeholder_format.type
        except ValueError:
            continue
        rect = (ph.left, ph.top, ph.width, ph.height)
        if None in rect:
            continue
        if kind == PP_PLACEHOLDER.FOOTER:
            footer = rect
        elif kind == PP_PLACEHOLDER.SLIDE_NUMBER:
            number = rect
    return footer, number


def clear_empty_placeholders(slide):
    """Drop placeholders left untouched, so template prompt text is not printed.

    Chrome is left alone — removing the slide-number placeholder would take the
    template's numbering with it.
    """
    for shape in list(slide.placeholders):
        if is_chrome(shape) or not shape.has_text_frame:
            continue
        if shape.text_frame.text.strip() == "":
            shape._element.getparent().remove(shape._element)


def write(tf, lines, wrap=True):
    """Fill a text frame with (text, size, colour, level) tuples."""
    tf.word_wrap = wrap
    for i, (text, size, color, level) in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = text
        p.level = level
        for run in p.runs:
            run.font.size = Pt(size)
            run.font.color.rgb = color


def style_title(slide, text, size=None):
    """Set the slide title, sized so it does not run into the body.

    Template title placeholders are laid out for a short line; these titles are
    sentences, so the size is chosen from the length.
    """
    title = slide.shapes.title
    if title is None:
        return None
    if size is None:
        size = 20 if len(text) <= 55 else (18 if len(text) <= 80 else 16)
    write(title.text_frame, [(text, size, INK, 0)])
    return title


def content_box(slide, prs):
    """Left, top, width and available height for a shape under the title."""
    title = slide.shapes.title
    left = Inches(0.5)
    top = Inches(1.31)
    width = prs.slide_width - Inches(1.0)
    if title is not None and title.top is not None:
        left = title.left
        width = title.width
        top = title.top + title.height + Inches(0.1)

    # Stop clear of the footer band, which the template puts at 5.10 in.
    bottom = prs.slide_height - Inches(0.62)
    return left, top, width, max(bottom - top, Inches(1.0))


def add_title_slide(prs):
    layout = find_layout(prs, "title slide", "title slide 1", "title", fallback=0)
    slide = prs.slides.add_slide(layout)

    lines = [
        (DOC_TITLE, 20, INK, 0),
        (SUBTITLE, 12, MUTED, 0),
        (PARTNERS, 10, MUTED, 0),
        ("2026-08-31  ·  " + STATUS, 9, MUTED, 0),
    ]

    title = style_title(slide, DOC_TITLE, size=20)
    bodies = body_placeholders(slide)

    if title is None:
        # The Classic template's title slide carries the logo plus a single text
        # placeholder and no title placeholder at all.
        if bodies:
            write(bodies[0].text_frame, lines)
        else:
            box = slide.shapes.add_textbox(Inches(1.5), Inches(2.6),
                                           prs.slide_width - Inches(3.0), Inches(2.0))
            write(box.text_frame, lines)
    elif bodies:
        write(bodies[0].text_frame, lines[1:])

    clear_empty_placeholders(slide)
    return slide


def add_section_slide(prs, title, kicker=""):
    layout = find_layout(prs, "subsection", "section header", "divider slide: text only",
                         "title only", fallback=2)
    slide = prs.slides.add_slide(layout)
    style_title(slide, title, size=20)

    if kicker:
        bodies = body_placeholders(slide)
        if bodies:
            write(bodies[0].text_frame, [(kicker, 11, MUTED, 0)])
        else:
            left, top, width, _ = content_box(slide, prs)
            box = slide.shapes.add_textbox(left, top, width, Inches(0.4))
            write(box.text_frame, [(kicker, 11, MUTED, 0)])

    clear_empty_placeholders(slide)
    return slide


def add_bullets_slide(prs, title, bullets):
    layout = find_layout(prs, "title and content", "content", "title and body", fallback=1)
    slide = prs.slides.add_slide(layout)
    style_title(slide, title)

    bodies = body_placeholders(slide)
    if bodies:
        body = bodies[0]
    else:
        left, top, width, height = content_box(slide, prs)
        body = slide.shapes.add_textbox(left, top, width, height)

    # The body is 3.35 in on this template. Size from the volume of text so a
    # long slide shrinks rather than overflowing the placeholder.
    weight = sum(1 + len(text) // 88 for _, text in bullets)
    top_size = 15 if weight <= 9 else (14 if weight <= 12 else 12.5)

    write(body.text_frame,
          [(text, top_size if level == 0 else top_size - 1.5,
            INK if level == 0 else MUTED, level)
           for level, text in bullets])

    clear_empty_placeholders(slide)
    return slide


def add_table_slide(prs, title, columns, rows, notes=None):
    layout = find_layout(prs, "title only", "title and content", fallback=5)
    slide = prs.slides.add_slide(layout)
    style_title(slide, title)
    left, top, width, avail = content_box(slide, prs)
    clear_empty_placeholders(slide)

    note_height = Inches(0.8) if notes else 0
    row_h = min(Inches(0.34), (avail - note_height) / (len(rows) + 1))
    height = row_h * (len(rows) + 1)

    shape = slide.shapes.add_table(len(rows) + 1, len(columns), left, top, width, height)
    table = shape.table
    for r in range(len(rows) + 1):
        table.rows[r].height = row_h

    # A narrow first column where it carries only a short key.
    if columns and columns[0] == "#":
        key = Inches(0.5)
        table.columns[0].width = key
        rest = (width - key) // (len(columns) - 1)
        for i in range(1, len(columns)):
            table.columns[i].width = rest

    def fill(cell, text, size, bold):
        cell.margin_top = Inches(0.03)
        cell.margin_bottom = Inches(0.03)
        cell.text = text
        for p in cell.text_frame.paragraphs:
            for run in p.runs:
                run.font.size = Pt(size)
                run.font.bold = bold
                run.font.color.rgb = INK

    for c, name in enumerate(columns):
        fill(table.cell(0, c), name, 10, True)
    for r, row in enumerate(rows, start=1):
        for c, value in enumerate(row):
            fill(table.cell(r, c), value, 9, False)

    if notes:
        box = slide.shapes.add_textbox(left, top + height + Inches(0.15),
                                       width, note_height)
        write(box.text_frame, [(n, 10, MUTED, 0) for n in notes])
    return slide


def set_alt_text(shape, text):
    """Alternate text for a picture, read by screen readers in PowerPoint.

    python-pptx has no accessor for this, so it is written straight onto the
    non-visual drawing properties.
    """
    shape._element._nvXxPr.cNvPr.set("descr", text)


def place_image(slide, prs, path, box, alt):
    """Fit an image inside (left, top, width, height), preserving aspect and
    centring it in whichever direction has slack."""
    from PIL import Image
    left, top, width, height = box
    with Image.open(path) as im:
        iw, ih = im.size
    scale = min(width / iw, height / ih)
    w, h = int(iw * scale), int(ih * scale)
    pic = slide.shapes.add_picture(
        str(path), int(left + (width - w) / 2), int(top + (height - h) / 2),
        width=w, height=h)
    set_alt_text(pic, alt)
    return pic


def content_area(slide, prs):
    """The rectangle between the title and the template's footer band.

    The Classic template puts its footer rule at 5.10 in on a 5.62 in slide,
    so anything below about 4.95 in collides with it.
    """
    left, top, width, _ = content_box(slide, prs)
    bottom = prs.slide_height - Inches(0.80)
    return left, top, width, max(bottom - top, Inches(1.0))


def add_figure_slide(prs, title, image, alt, note=None):
    layout = find_layout(prs, "title only", "title and content", fallback=5)
    slide = prs.slides.add_slide(layout)
    t = style_title(slide, title)
    left, top, width, height = content_area(slide, prs)

    # The template sizes its title placeholder for two lines; these titles are
    # one. Reclaim the unused half by starting the image higher, rather than
    # resizing the placeholder — writing an explicit size onto an inheriting
    # placeholder also writes an offset of (0, 0) and moves the title.
    if t is not None and t.top is not None:
        gained = top - (t.top + Inches(0.78))
        if gained > 0:
            top -= gained
            height += gained

    clear_empty_placeholders(slide)

    note_h = Inches(0.32) if note else 0
    place_image(slide, prs, HERE / "figures" / "png" / image,
                (left, top, width, height - note_h), alt)
    if note:
        box = slide.shapes.add_textbox(left, top + height - note_h, width,
                                       note_h)
        write(box.text_frame, [(note, 10, MUTED, 0)])
    return slide


def add_photos_slide(prs, title, photos, note=None):
    """Two photographs side by side, each with its own short caption."""
    layout = find_layout(prs, "title only", "title and content", fallback=5)
    slide = prs.slides.add_slide(layout)
    style_title(slide, title)
    left, top, width, height = content_area(slide, prs)
    clear_empty_placeholders(slide)

    note_h = Inches(0.3) if note else 0
    cap_h = Inches(0.5)
    gap = Inches(0.3)
    cell_w = int((width - gap * (len(photos) - 1)) / len(photos))
    img_h = height - note_h - cap_h

    for i, (path, caption, alt) in enumerate(photos):
        x = left + i * (cell_w + gap)
        place_image(slide, prs, Path(path), (x, top, cell_w, img_h), alt)
        box = slide.shapes.add_textbox(x, top + img_h + Inches(0.04), cell_w,
                                       cap_h)
        tf = box.text_frame
        tf.word_wrap = True
        write(tf, [(caption, 10, SECOND, 0)])

    if note:
        box = slide.shapes.add_textbox(left, top + height - note_h, width,
                                       note_h)
        write(box.text_frame, [(note, 10, MUTED, 0)])
    return slide


def add_bullets_photo_slide(prs, title, bullets, photo, caption, alt):
    """Bullets on the left, one photograph on the right.

    The text goes into the layout's own body placeholder, narrowed, rather than
    into a new textbox — a textbox inherits neither the master's bullet glyphs
    nor its sans face, and the difference shows next to the other bullet slides.
    """
    layout = find_layout(prs, "title and content", "content", fallback=1)
    slide = prs.slides.add_slide(layout)
    style_title(slide, title)
    left, top, width, height = content_area(slide, prs)

    text_w = int(width * 0.58)
    img_x = left + text_w + Inches(0.25)
    img_w = width - text_w - Inches(0.25)

    bodies = body_placeholders(slide)
    if bodies:
        box = bodies[0]
        # Set all four, so python-pptx writes a complete xfrm rather than
        # inventing an offset of (0, 0) alongside a size.
        box.left, box.top, box.width, box.height = left, top, text_w, height
    else:
        box = slide.shapes.add_textbox(left, top, text_w, height)

    weight = sum(1 + len(t) // 55 for _, t in bullets)
    size = 13 if weight <= 9 else 12
    write(box.text_frame,
          [(t, size if lv == 0 else size - 1.5,
            INK if lv == 0 else MUTED, lv) for lv, t in bullets])
    clear_empty_placeholders(slide)

    cap_h = Inches(0.6)
    place_image(slide, prs, Path(photo), (img_x, top, img_w, height - cap_h),
                alt)
    cbox = slide.shapes.add_textbox(img_x, top + height - cap_h, img_w, cap_h)
    cbox.text_frame.word_wrap = True
    write(cbox.text_frame, [(caption, 9.5, SECOND, 0)])
    return slide


def add_footers(prs, skip_first=True):
    """Place the footer line and slide number where the template puts them.

    Where the layout defines no footer position, nothing is added: the master
    already carries its own bottom chrome, and a textbox guessed at the bottom
    left would land on top of the logo.
    """
    total = len(prs.slides._sldIdLst)
    for i, slide in enumerate(prs.slides, start=1):
        if skip_first and i == 1:
            continue

        footer_rect, number_rect = layout_chrome(slide)

        if footer_rect is not None:
            box = slide.shapes.add_textbox(*footer_rect)
            write(box.text_frame, [(FOOTER, 8, MUTED, 0)])
            box.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER

        if number_rect is not None:
            box = slide.shapes.add_textbox(*number_rect)
            write(box.text_frame, [("%d / %d" % (i, total), 8, MUTED, 0)])
            box.text_frame.paragraphs[0].alignment = PP_ALIGN.RIGHT


def build(template=None, out_path="pdf/REPLICATION_RECOMMENDATIONS_BRIEFING.pptx"):
    prs = Presentation(template) if template else Presentation()

    # The templates ship with example slides. Start from an empty deck, dropping
    # the relationship as well as the list entry so no orphan part is left.
    for sld_id in list(prs.slides._sldIdLst):
        rid = sld_id.rId
        prs.slides._sldIdLst.remove(sld_id)
        prs.part.drop_rel(rid)

    for kind, payload in DECK:
        if kind == "title":
            add_title_slide(prs)
        elif kind == "section":
            add_section_slide(prs, payload["title"], payload.get("kicker", ""))
        elif kind == "bullets":
            add_bullets_slide(prs, payload["title"], payload["bullets"])
        elif kind == "table":
            add_table_slide(prs, payload["title"], payload["columns"],
                            payload["rows"], payload.get("notes"))
        elif kind == "figure":
            add_figure_slide(prs, payload["title"], payload["image"],
                             payload["alt"], payload.get("note"))
        elif kind == "photos":
            add_photos_slide(prs, payload["title"], payload["photos"],
                             payload.get("note"))
        elif kind == "bullets_photo":
            add_bullets_photo_slide(prs, payload["title"], payload["bullets"],
                                    payload["photo"], payload["caption"],
                                    payload["alt"])
        else:
            raise ValueError("unknown slide kind: %s" % kind)

    add_footers(prs)

    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    prs.save(out)
    return out, len(prs.slides._sldIdLst)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--template", default=DEFAULT_TEMPLATE,
                    help="Base .pptx or .potx to inherit theme and layouts from. "
                         "Defaults to the American Red Cross Classic template.")
    ap.add_argument("--no-template", action="store_true",
                    help="Build on python-pptx's neutral template instead.")
    ap.add_argument("-o", "--output",
                    default="pdf/REPLICATION_RECOMMENDATIONS_BRIEFING.pptx")
    args = ap.parse_args()

    template = None if args.no_template else args.template
    if template and not Path(template).is_file():
        sys.exit("Template not found: %s" % template)

    out, n = build(template, args.output)
    print("Wrote %s (%d slides) — %s" % (
        out, n, Path(template).name if template else "neutral template"))


if __name__ == "__main__":
    main()
