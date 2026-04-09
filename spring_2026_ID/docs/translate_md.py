#!/usr/bin/env python3
"""translate_md.py — Translate markdown documentation to Bahasa Indonesia.

Uses Google Translate (free, no API key needed). Preserves markdown
formatting by splitting on block boundaries and skipping code blocks.

Usage:
    python3 translate_md.py INPUT.md                    # output to stdout
    python3 translate_md.py INPUT.md -o OUTPUT.id.md    # output to file
    python3 translate_md.py INPUT.md --verify           # dry run

Requires:
    pip install googletrans==4.0.0-rc1
"""

import argparse
import os
import re
import sys
import time

DISCLAIMER_ID = """> **PERINGATAN: Terjemahan Otomatis**
>
> Dokumen ini diterjemahkan secara otomatis dari bahasa Inggris menggunakan
> Google Translate. Terjemahan ini belum ditinjau oleh penerjemah manusia
> dan mungkin mengandung kesalahan. Untuk informasi yang akurat, silakan
> merujuk ke dokumen asli berbahasa Inggris.
>
> *This document was automatically translated from English using*
> *Google Translate. It has not been reviewed by a human translator*
> *and may contain errors. For accurate information, refer to the*
> *original English document.*

---

"""

# Terms to preserve untranslated (replaced with placeholders before
# translation, restored after)
PRESERVE_TERMS = [
    # Product names
    "Raspberry Pi", "Witty Pi", "Geekworm G469", "Pi-EzConnect",
    "ANNKE C1200", "Hydreon RG-15", "Mean Well", "LINOVISION",
    "Proxicast", "Pangolin", "Tailscale", "LiveORC", "ORC-OS",
    "NodeORC", "DejaVu Sans Mono", "Samsung FIT Plus",
    "Electronics-Salon", "Heschen", "OONO", "EXVIST",
    # Organization names
    "American Red Cross", "Palang Merah Indonesia",
    # Technical terms that should stay English
    "fail-safe", "Gore vent", "GORE vent",
    "orc-capture", "orc-sensors", "orc-led-status",
    "orc-maintenance-check", "orc-api",
    "deploy.sh", "build_pdf.sh", "camtool.py",
]


def translate_text(translator, text, retries=3):
    """Translate a text chunk with retries."""
    if not text.strip():
        return text

    for attempt in range(retries):
        try:
            result = translator.translate(text, src="en", dest="id")
            return result.text
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
            else:
                print(f"    WARNING: translation failed: {e}",
                      file=sys.stderr)
                return text  # return original on failure


def protect_terms(text):
    """Replace preserve terms with placeholders."""
    replacements = {}
    for i, term in enumerate(PRESERVE_TERMS):
        placeholder = f"XPRESERVEX{i:03d}X"
        if term in text:
            text = text.replace(term, placeholder)
            replacements[placeholder] = term
    return text, replacements


def restore_terms(text, replacements):
    """Restore preserved terms from placeholders."""
    for placeholder, term in replacements.items():
        text = text.replace(placeholder, term)
    return text


def translate_document(input_path, output_path=None, verify=False):
    """Translate a markdown file to Bahasa Indonesia."""
    try:
        from googletrans import Translator
    except ImportError:
        print("ERROR: pip install googletrans==4.0.0-rc1", file=sys.stderr)
        sys.exit(1)

    with open(input_path) as f:
        lines = f.readlines()

    if verify:
        translatable = sum(1 for l in lines
                          if l.strip() and not l.strip().startswith("```"))
        print(f"Would translate: {input_path}")
        print(f"  Total lines: {len(lines)}")
        print(f"  Translatable lines: ~{translatable}")
        if output_path:
            print(f"  Output: {output_path}")
        else:
            print(f"  Output: stdout")
        return

    translator = Translator()
    translated_lines = []
    in_code_block = False
    batch = []
    batch_indices = []

    print(f"  Translating: {os.path.basename(input_path)} ...",
          file=sys.stderr, end=" ", flush=True)

    def flush_batch():
        """Translate accumulated batch of lines."""
        if not batch:
            return
        combined = "\n".join(batch)
        protected, replacements = protect_terms(combined)
        result = translate_text(translator, protected)
        result = restore_terms(result, replacements)
        result_lines = result.split("\n")

        # If line count matches, map 1:1; otherwise take whole block
        if len(result_lines) == len(batch):
            for idx, translated in zip(batch_indices, result_lines):
                translated_lines[idx] = translated + "\n"
        else:
            # Rejoin and replace entire batch
            for i, idx in enumerate(batch_indices):
                if i == 0:
                    translated_lines[idx] = result + "\n"
                else:
                    translated_lines[idx] = ""

    # First pass: identify what to translate
    for i, line in enumerate(lines):
        translated_lines.append(line)  # default: keep original

        stripped = line.strip()

        # Track code blocks
        if stripped.startswith("```"):
            if in_code_block:
                in_code_block = False
            else:
                in_code_block = True
            continue

        # Skip code block contents
        if in_code_block:
            continue

        # Skip empty lines, image paths, horizontal rules
        if not stripped:
            flush_batch()
            batch = []
            batch_indices = []
            continue

        if stripped == "---":
            flush_batch()
            batch = []
            batch_indices = []
            continue

        # Skip lines that are purely markdown table separators
        if re.match(r"^\|[-:|  ]+\|$", stripped):
            flush_batch()
            batch = []
            batch_indices = []
            continue

        # Skip image path lines (but translate alt text separately)
        if stripped.startswith("!["):
            # Extract and translate alt text
            match = re.match(r"^(!\[)(.*?)(\]\(.+\))(.*)$", stripped)
            if match:
                prefix, alt_text, path_part, suffix = match.groups()
                if alt_text:
                    protected, replacements = protect_terms(alt_text)
                    translated_alt = translate_text(translator, protected)
                    translated_alt = restore_terms(translated_alt, replacements)
                    translated_lines[i] = f"{prefix}{translated_alt}{path_part}{suffix}\n"
            flush_batch()
            batch = []
            batch_indices = []
            continue

        # Accumulate translatable lines
        batch.append(stripped)
        batch_indices.append(i)

        # Flush on paragraph boundaries (translate in reasonable chunks)
        if len(batch) >= 10:
            flush_batch()
            batch = []
            batch_indices = []

    # Final flush
    flush_batch()

    print("done.", file=sys.stderr)

    # Assemble output
    output = DISCLAIMER_ID + "".join(translated_lines)

    if output_path:
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        with open(output_path, "w") as f:
            f.write(output)
    else:
        print(output)


def main():
    parser = argparse.ArgumentParser(
        description="Translate markdown to Bahasa Indonesia via Google Translate")
    parser.add_argument("input", help="Input markdown file")
    parser.add_argument("-o", "--output", help="Output file (default: stdout)")
    parser.add_argument("--verify", action="store_true",
                        help="Dry run — show what would be translated")
    args = parser.parse_args()

    translate_document(args.input, args.output, args.verify)


if __name__ == "__main__":
    main()
