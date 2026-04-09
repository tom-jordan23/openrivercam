#!/usr/bin/env bash
#
# build_pdf.sh — Convert markdown documentation to PDF via LaTeX
#
# Usage:
#   ./build_pdf.sh                    # convert all docs
#   ./build_pdf.sh OPERATOR_GUIDE.md  # convert one doc
#   ./build_pdf.sh --list             # list available docs
#
# Prerequisites:
#   sudo apt install pandoc texlive-xetex texlive-latex-recommended texlive-latex-extra texlive-fonts-recommended
#
# Output: docs/pdf/<filename>.pdf
#
# Every page includes:
#   Header: document title (left), version (right)
#   Footer: project name (left), page X of Y (right)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DOCS_DIR="$SCRIPT_DIR"
PDF_DIR="$SCRIPT_DIR/pdf"

mkdir -p "$PDF_DIR"

# ─── Check dependencies ─────────────────────────────────────────
for cmd in pandoc xelatex; do
    if ! command -v "$cmd" &>/dev/null; then
        echo "ERROR: $cmd not found."
        echo "Install with: sudo apt install pandoc texlive-xetex texlive-latex-recommended texlive-latex-extra texlive-fonts-recommended"
        exit 1
    fi
done

# ─── Document list (ordered for printing) ────────────────────────
ALL_DOCS=(
    OPERATOR_GUIDE.md
    FIELD_SURVEY_GUIDE.md
    TROUBLESHOOTING.md
    DOOR_SHEET_JAKARTA.md
    DOOR_SHEET_SUKABUMI.md
    LED_STATUS_SPEC.md
    REBOOT_CHECKLIST.md
    REBOOT_CHECKLIST_JAKARTA.md
    ASSEMBLY_JAKARTA.md
    ASSEMBLY_SUKABUMI.md
    WIRING_JAKARTA.md
    WIRING_SUKABUMI.md
    MODEM_VERIFICATION_SUKABUMI.md
)

# ─── Per-document audience ───────────────────────────────────────
declare -A DOC_AUDIENCE=(
    [OPERATOR_GUIDE.md]="PMI field staff"
    [FIELD_SURVEY_GUIDE.md]="PMI field survey teams"
    [TROUBLESHOOTING.md]="Field technicians, PMI staff"
    [DOOR_SHEET_JAKARTA.md]="Field technicians (laminate for enclosure)"
    [DOOR_SHEET_SUKABUMI.md]="Field technicians (laminate for enclosure)"
    [LED_STATUS_SPEC.md]="Technical installers"
    [REBOOT_CHECKLIST.md]="Field technicians"
    [REBOOT_CHECKLIST_JAKARTA.md]="Field technicians"
    [ASSEMBLY_JAKARTA.md]="Technical installers"
    [ASSEMBLY_SUKABUMI.md]="Technical installers"
    [WIRING_JAKARTA.md]="Technical installers"
    [WIRING_SUKABUMI.md]="Technical installers"
    [MODEM_VERIFICATION_SUKABUMI.md]="Technical installers"
)

# ─── Extract metadata from markdown ─────────────────────────────

extract_version() {
    local md_file="$1"
    local version
    version=$(grep -m1 -oP '\*\*(Document )?Version:\*\*\s*\K.*' "$md_file" 2>/dev/null | sed 's/\*//g' | xargs) || true
    if [ -z "$version" ]; then
        version=$(grep -m1 -oP '\*\*Last Updated:\*\*\s*\K.*' "$md_file" 2>/dev/null | sed 's/\*//g' | xargs) || true
    fi
    if [ -z "$version" ]; then
        version=$(git log -1 --format="%as" -- "$md_file" 2>/dev/null) || true
    fi
    [ -z "$version" ] && version=$(date +%Y-%m-%d)
    echo "$version"
}

extract_title() {
    local md_file="$1"
    grep -m1 '^# ' "$md_file" | sed 's/^# //' || echo "${md_file%.md}"
}

# ─── Generate LaTeX header file ──────────────────────────────────

make_latex_header() {
    local title="$1"
    local version="$2"
    local build_date
    build_date=$(date +%Y-%m-%d)

    # Escape LaTeX special characters in title
    local safe_title
    safe_title=$(echo "$title" | sed 's/&/\\&/g; s/_/\\_/g; s/#/\\#/g; s/%/\\%/g')

    cat <<'LATEXEOF'
\usepackage{fancyhdr}
\usepackage{lastpage}
\usepackage{graphicx}
\usepackage{float}
\usepackage{etoolbox}
\usepackage{longtable}
\usepackage{booktabs}

% Use DejaVu Sans Mono for code blocks — has full Unicode box-drawing glyphs
\usepackage{fontspec}
\setmonofont{DejaVu Sans Mono}

% Break long URLs and paths
\usepackage[hyphens,spaces,obeyspaces]{url}
\usepackage{hyperref}
\hypersetup{breaklinks=true}

% Wrap text in code blocks — prevent overflow
\usepackage{fvextra}
\DefineVerbatimEnvironment{Highlighting}{Verbatim}{
  breaklines,
  breakanywhere,
  commandchars=\\\{\}
}

% Allow table columns to wrap
\usepackage{array}
\usepackage{tabularx}

% Prevent overfull hbox warnings — allow slightly loose lines
\tolerance=1000
\emergencystretch=3em
\setlength{\parskip}{0.5em}

% Keep images in place
\let\origfigure\figure
\let\endorigfigure\endfigure
\renewenvironment{figure}[1][H]{\origfigure[H]}{\endorigfigure}

% Title page style — no header, just footer with page number
\fancypagestyle{title}{
  \fancyhf{}
  \renewcommand{\headrulewidth}{0pt}
  \renewcommand{\footrulewidth}{0.4pt}
  \fancyfoot[R]{\small Page \thepage\ of \pageref{LastPage}}
}

% Content page style — full header and footer
\pagestyle{fancy}
\fancyhf{}
LATEXEOF

    echo "\\fancyhead[L]{\\small ${safe_title}}"
    echo "\\fancyhead[R]{\\small v${version} \\textbar{} Built ${build_date}}"
    echo "\\fancyfoot[L]{\\small\\textit{ORC Indonesia Deployment --- PMI / American Red Cross}}"
    echo "\\fancyfoot[R]{\\small Page \\thepage\\ of \\pageref{LastPage}}"

    cat <<'LATEXEOF'
\renewcommand{\headrulewidth}{0.4pt}
\renewcommand{\footrulewidth}{0.4pt}

% 'plain' style used by section starts — same as content
\fancypagestyle{plain}{
  \fancyhf{}
LATEXEOF

    echo "  \\fancyhead[L]{\\small ${safe_title}}"
    echo "  \\fancyhead[R]{\\small v${version} \\textbar{} Built ${build_date}}"
    echo "  \\fancyfoot[L]{\\small\\textit{ORC Indonesia Deployment --- PMI / American Red Cross}}"
    echo "  \\fancyfoot[R]{\\small Page \\thepage\\ of \\pageref{LastPage}}"

    cat <<'LATEXEOF'
  \renewcommand{\headrulewidth}{0.4pt}
  \renewcommand{\footrulewidth}{0.4pt}
}

% Apply title style to the title page, then switch to content style
\AtBeginDocument{\thispagestyle{title}}

% Force page break after title block
\makeatletter
\patchcmd{\maketitle}{\endgroup}{\endgroup\newpage}{}{}
\makeatother

% Page break after TOC
\AtBeginDocument{
  \let\oldtableofcontents\tableofcontents
  \renewcommand{\tableofcontents}{\oldtableofcontents\newpage}
}
LATEXEOF
}

# ─── Convert one document ────────────────────────────────────────

convert_one() {
    local md_file="$1"
    local basename="${md_file%.md}"
    local pdf_file="$PDF_DIR/${basename}.pdf"

    if [ ! -f "$DOCS_DIR/$md_file" ]; then
        echo "SKIP: $md_file not found"
        return 1
    fi

    local title version audience header_file build_date
    title=$(extract_title "$DOCS_DIR/$md_file")
    version=$(extract_version "$DOCS_DIR/$md_file")
    audience="${DOC_AUDIENCE[$md_file]:-}"
    build_date=$(date +%Y-%m-%d)

    echo "  Converting: $md_file (v${version}) → pdf/${basename}.pdf"

    header_file=$(mktemp /tmp/orc-latex-XXXXXX.tex)
    make_latex_header "$title" "$version" > "$header_file"

    # Escape LaTeX special characters for pandoc -V metadata
    local safe_title safe_audience
    safe_title=$(echo "$title" | sed 's/&/\\&/g; s/_/\\_/g; s/#/\\#/g; s/%/\\%/g')
    safe_audience=$(echo "$audience" | sed 's/&/\\&/g; s/_/\\_/g; s/#/\\#/g; s/%/\\%/g')

    pandoc "$DOCS_DIR/$md_file" \
        --from markdown \
        --to pdf \
        --resource-path="$DOCS_DIR" \
        --pdf-engine=xelatex \
        --include-in-header="$header_file" \
        --toc --toc-depth=2 \
        -V toc-title="Contents" \
        -V geometry:margin=1in \
        -V fontsize=11pt \
        -V colorlinks=true \
        -V linkcolor=blue \
        -V urlcolor=blue \
        -V documentclass=article \
        -V title="$safe_title" \
        -V subtitle="Indonesia ORC Deployment --- Spring 2026" \
        -V author="American Red Cross / Palang Merah Indonesia" \
        -V date="Version ${version} | Audience: ${safe_audience} | Built ${build_date}" \
        -o "$pdf_file" 2>/dev/null

    local rc=$?
    rm -f "$header_file"

    if [ $rc -ne 0 ]; then
        echo "    FAILED: $md_file (check LaTeX errors)"
        return 1
    fi
}

list_docs() {
    echo "Available documents:"
    printf "  %-45s %s\n" "Document" "Version"
    printf "  %-45s %s\n" "--------" "-------"
    for doc in "${ALL_DOCS[@]}"; do
        if [ -f "$DOCS_DIR/$doc" ]; then
            local ver
            ver=$(extract_version "$DOCS_DIR/$doc")
            printf "  %-45s %s\n" "$doc" "v${ver}"
        else
            printf "  %-45s %s\n" "$doc" "(NOT FOUND)"
        fi
    done
}

# ─── Main ────────────────────────────────────────────────────────

if [ "${1:-}" = "--list" ]; then
    list_docs
    exit 0
fi

echo "Building PDFs (LaTeX)..."
echo "Output: $PDF_DIR/"
echo ""

errors=0

if [ $# -gt 0 ]; then
    for arg in "$@"; do
        convert_one "$arg" || errors=$((errors + 1))
    done
else
    for doc in "${ALL_DOCS[@]}"; do
        convert_one "$doc" || errors=$((errors + 1))
    done
fi

echo ""
echo "Done. $errors error(s)."
echo "PDFs in: $PDF_DIR/"

if [ $errors -gt 0 ]; then
    exit 1
fi
