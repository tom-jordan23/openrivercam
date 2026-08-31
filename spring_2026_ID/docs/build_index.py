#!/usr/bin/env python3
"""
build_index.py — Rebuild the recommendation index in the report from the source
list, so the two cannot drift apart.

Reads RECOMMENDATIONS.md, extracts every "- **Rn — statement.**" bullet with its
group heading, and writes a table into REPLICATION_RECOMMENDATIONS.md between the
INDEX markers.

    .venv-pdf/bin/python build_index.py
"""

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "RECOMMENDATIONS.md"
DST = HERE / "REPLICATION_RECOMMENDATIONS.md"
BEGIN = "<!-- INDEX:BEGIN -->"
END = "<!-- INDEX:END -->"

SKIP_GROUPS = {"Acknowledgement — for the report, not a recommendation",
               "Notes for you"}


def collapse(text):
    """One line, no markdown emphasis, no trailing full stop."""
    text = re.sub(r"\s+", " ", text).strip()
    text = text.replace("**", "").replace("*", "")
    return text.rstrip(".")


def parse(md):
    """Pull every recommendation out with its group heading.

    A bullet's bold statement often wraps across lines, so bullets are gathered
    whole before the statement is matched. Matching line by line silently drops
    the wrapped ones.
    """
    group, rows = None, []
    bullets = []                                  # (group, full bullet text)
    current = None

    for line in md.split("\n"):
        h = re.match(r"^## (.+)$", line)
        if h:
            if current:
                bullets.append(current)
                current = None
            group = h.group(1).strip()
            continue
        if re.match(r"^- \*\*R\d+", line):
            if current:
                bullets.append(current)
            current = [group, line]
        elif current is not None:
            if line.startswith("- ") or re.match(r"^#{1,6} ", line):
                bullets.append(current)
                current = None
            else:
                current[1] += " " + line.strip()
    if current:
        bullets.append(current)

    for grp, text in bullets:
        if grp in SKIP_GROUPS:
            continue
        b = re.match(r"^- \*\*(R\d+)\s*—\s*(.+?)\*\*", text)
        if b:
            rows.append((b.group(1), collapse(b.group(2)), grp))
        else:
            sys.stderr.write("WARNING: could not parse: %s\n" % text[:70])
    return rows


def render(rows):
    out = []
    current = None
    for num, text, group in rows:
        if group != current:
            current = group
            out.append("")
            out.append("**%s**" % group)
            out.append("")
            out.append("| | Recommendation |")
            out.append("|---|---|")
        out.append("| **%s** | %s |" % (num, text))
    return "\n".join(out).strip()


def main():
    rows = parse(SRC.read_text(encoding="utf-8"))
    if not rows:
        sys.exit("no recommendations parsed from %s" % SRC.name)

    doc = DST.read_text(encoding="utf-8")
    if BEGIN not in doc or END not in doc:
        sys.exit("index markers not found in %s" % DST.name)

    head = doc.split(BEGIN)[0]
    tail = doc.split(END)[1]
    DST.write_text(head + BEGIN + "\n\n" + render(rows) + "\n\n" + END + tail,
                   encoding="utf-8")

    groups = len({g for _, _, g in rows})
    print("index rebuilt: %d recommendations in %d groups" % (len(rows), groups))


if __name__ == "__main__":
    main()
