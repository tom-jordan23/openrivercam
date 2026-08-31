#!/usr/bin/env bash
#
# build_pdf.sh — Convert markdown documentation to PDF via LaTeX
#
# Usage:
#   ./build_pdf.sh                    # convert all docs (English)
#   ./build_pdf.sh OPERATOR_GUIDE.md  # convert one doc (English)
#   ./build_pdf.sh --lang id          # convert all docs (Bahasa Indonesia)
#   ./build_pdf.sh --lang id OPERATOR_GUIDE.md  # one doc, Indonesian
#   ./build_pdf.sh --list             # list available docs
#   ./build_pdf.sh --engine html      # force the HTML/WeasyPrint path
#
# Engines:
#   latex  pandoc + xelatex. Preferred where a TeX installation is present.
#   html   pandoc + WeasyPrint, styled by pdf_print.css. No TeX needed.
#   Selection is automatic: xelatex if found, otherwise WeasyPrint.
#
# Prerequisites (either engine):
#   LaTeX: sudo apt install pandoc texlive-xetex texlive-latex-recommended \
#          texlive-latex-extra texlive-fonts-recommended
#   HTML:  no root needed. Create the toolchain venv once with:
#          uv venv .venv-pdf --python 3.12
#          uv pip install --python .venv-pdf/bin/python pypandoc_binary weasyprint
#          ln -sf ../lib/python3.12/site-packages/pypandoc/files/pandoc .venv-pdf/bin/pandoc
#   For Indonesian: pip install googletrans==4.0.0-rc1 (in docs/.venv)
#
# Output:
#   English:    docs/pdf/<filename>.pdf
#   Indonesian: docs/pdf/id/<filename>.id.pdf
#
# Every page includes:
#   Header: document title (left), version (right)
#   Footer: project name (left), page X of Y (right)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DOCS_DIR="$SCRIPT_DIR"
PDF_DIR="$SCRIPT_DIR/pdf"
LANG="en"
ENGINE="auto"

# Parse flags
args=()
while [[ $# -gt 0 ]]; do
    case "$1" in
        --lang)
            LANG="$2"
            shift 2
            ;;
        --engine)
            ENGINE="$2"
            shift 2
            ;;
        *)
            args+=("$1")
            shift
            ;;
    esac
done
set -- "${args[@]+"${args[@]}"}"

if [ "$LANG" = "id" ]; then
    PDF_DIR="$SCRIPT_DIR/pdf/id"
fi

mkdir -p "$PDF_DIR"

# ─── Resolve the toolchain ──────────────────────────────────────
# Prefer anything on PATH; fall back to the local .venv-pdf toolchain, which
# needs no root to install. See the header comment for how to create it.

PANDOC=""
if command -v pandoc &>/dev/null; then
    PANDOC="$(command -v pandoc)"
elif [ -x "$SCRIPT_DIR/.venv-pdf/bin/pandoc" ]; then
    PANDOC="$SCRIPT_DIR/.venv-pdf/bin/pandoc"
fi

WEASYPRINT=""
if command -v weasyprint &>/dev/null; then
    WEASYPRINT="$(command -v weasyprint)"
elif [ -x "$SCRIPT_DIR/.venv-pdf/bin/weasyprint" ]; then
    WEASYPRINT="$SCRIPT_DIR/.venv-pdf/bin/weasyprint"
fi

if [ -z "$PANDOC" ]; then
    echo "ERROR: pandoc not found on PATH or in $SCRIPT_DIR/.venv-pdf/bin/."
    echo "See the Prerequisites block at the top of this script."
    exit 1
fi

# Pick an engine if one was not forced.
if [ "$ENGINE" = "auto" ]; then
    if command -v xelatex &>/dev/null; then
        ENGINE="latex"
    elif [ -n "$WEASYPRINT" ]; then
        ENGINE="html"
    else
        echo "ERROR: no PDF engine available — neither xelatex nor weasyprint."
        echo "See the Prerequisites block at the top of this script."
        exit 1
    fi
fi

case "$ENGINE" in
    latex)
        if ! command -v xelatex &>/dev/null; then
            echo "ERROR: --engine latex requested but xelatex not found."
            exit 1
        fi
        ;;
    html)
        if [ -z "$WEASYPRINT" ]; then
            echo "ERROR: --engine html requested but weasyprint not found."
            exit 1
        fi
        if [ ! -f "$SCRIPT_DIR/pdf_print.css" ]; then
            echo "ERROR: --engine html requires pdf_print.css alongside this script."
            exit 1
        fi
        ;;
    *)
        echo "ERROR: unknown engine '$ENGINE'. Use 'latex' or 'html'."
        exit 1
        ;;
esac

# ─── Document list (ordered for printing) ────────────────────────
ALL_DOCS=(
    REPLICATION_RECOMMENDATIONS.md
    REPLICATION_RECOMMENDATIONS_APPENDIX.md
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
    [REPLICATION_RECOMMENDATIONS.md]="IPB and BHLK leadership"
    [REPLICATION_RECOMMENDATIONS_APPENDIX.md]="IPB and BHLK — technical staff"
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

# The full version string may carry a parenthetical status note. The running
# header wants the leading date only; the title page keeps the whole thing.
short_version() {
    echo "$1" | sed 's/ *(.*//' | xargs
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
    echo "\\fancyfoot[L]{\\small\\textit{ORC Indonesia --- PMI \\textperiodcentered{} IPB \\textperiodcentered{} BHLK \\textperiodcentered{} American Red Cross}}"
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
    echo "  \\fancyfoot[L]{\\small\\textit{ORC Indonesia --- PMI \\textperiodcentered{} IPB \\textperiodcentered{} BHLK \\textperiodcentered{} American Red Cross}}"
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

# ─── Render via HTML + WeasyPrint ────────────────────────────────

render_html() {
    local source_md="$1" pdf_file="$2" title="$3" version="$4"
    local audience="$5" subtitle="$6" toc_title="$7" build_date="$8"

    local body_md html_file
    body_md=$(mktemp /tmp/orc-body-XXXXXX.md)
    html_file=$(mktemp /tmp/orc-html-XXXXXX.html)

    # Hidden carriers for the running header, read through string-set in
    # pdf_print.css. They go at the top of the body rather than before it, so
    # the strings are still unset on the title and contents pages and those two
    # come out without a running header.
    {
        printf '<h1 class="hidden-title">%s</h1>\n\n' "$title"
        printf '<p class="hidden-version">v%s | Built %s</p>\n\n' \
            "$(short_version "$version")" "$build_date"
        # Drop the leading H1: the generated title page already carries it, and
        # leaving it in duplicates the title in the body and in the contents.
        awk 'NR==1 && /^# / { next } { print }' "$source_md"
    } > "$body_md"

    "$PANDOC" "$body_md" \
        --from markdown \
        --to html5 \
        --standalone \
        --resource-path="$DOCS_DIR" \
        --toc --toc-depth=2 \
        --css pdf_print.css \
        --metadata title="$title" \
        --metadata subtitle="$subtitle" \
        --metadata author="PMI · IPB · BHLK · American Red Cross" \
        --metadata date="Version ${version} | Audience: ${audience} | Built ${build_date}" \
        --metadata toc-title="$toc_title" \
        -o "$html_file"

    local rc=$?
    if [ $rc -ne 0 ]; then
        rm -f "$body_md" "$html_file"
        return $rc
    fi

    # -u sets the base URL so pdf_print.css and images resolve from docs/.
    "$WEASYPRINT" -u "$DOCS_DIR/" "$html_file" "$pdf_file" 2>/dev/null
    rc=$?

    rm -f "$body_md" "$html_file"
    return $rc
}

# ─── Convert one document ────────────────────────────────────────

convert_one() {
    local md_file="$1"
    local basename="${md_file%.md}"
    local pdf_file
    local source_md="$DOCS_DIR/$md_file"
    local translated_tmp=""

    if [ "$LANG" = "id" ]; then
        pdf_file="$PDF_DIR/${basename}.id.pdf"
    else
        pdf_file="$PDF_DIR/${basename}.pdf"
    fi

    if [ ! -f "$DOCS_DIR/$md_file" ]; then
        echo "SKIP: $md_file not found"
        return 1
    fi

    local title version audience header_file build_date
    title=$(extract_title "$DOCS_DIR/$md_file")
    version=$(extract_version "$DOCS_DIR/$md_file")
    audience="${DOC_AUDIENCE[$md_file]:-}"
    build_date=$(date +%Y-%m-%d)

    # Translate if Indonesian
    if [ "$LANG" = "id" ]; then
        echo "  Translating: $md_file → Bahasa Indonesia..."
        translated_tmp=$(mktemp /tmp/orc-translate-XXXXXX.md)
        # Use venv python if available
        local py="python3"
        [ -x "$SCRIPT_DIR/.venv/bin/python3" ] && py="$SCRIPT_DIR/.venv/bin/python3"
        if ! "$py" "$SCRIPT_DIR/translate_md.py" "$DOCS_DIR/$md_file" -o "$translated_tmp"; then
            echo "    FAILED: translation error"
            rm -f "$translated_tmp"
            return 1
        fi
        source_md="$translated_tmp"
        # Extract title from translated doc (first H1)
        title=$(grep -m1 '^# ' "$source_md" | sed 's/^# //' || echo "$title")
    fi

    echo "  Converting: $md_file (v${version}, ${LANG}, ${ENGINE}) → $(basename "$pdf_file")"

    local toc_title="Contents"
    local subtitle="Indonesia ORC Deployment --- Spring 2026"
    if [ "$LANG" = "id" ]; then
        toc_title="Daftar Isi"
        subtitle="Penempatan ORC Indonesia --- Musim Semi 2026"
    fi

    if [ "$ENGINE" = "html" ]; then
        local html_subtitle="${subtitle//---/—}"
        render_html "$source_md" "$pdf_file" "$title" "$version" \
            "$audience" "$html_subtitle" "$toc_title" "$build_date"
        local rc=$?
        [ -n "$translated_tmp" ] && rm -f "$translated_tmp"
        if [ $rc -ne 0 ]; then
            echo "    FAILED: $md_file"
            return 1
        fi
        return 0
    fi

    header_file=$(mktemp /tmp/orc-latex-XXXXXX.tex)
    make_latex_header "$title" "$version" > "$header_file"

    # Escape LaTeX special characters for pandoc -V metadata
    local safe_title safe_audience
    safe_title=$(echo "$title" | sed 's/&/\\&/g; s/_/\\_/g; s/#/\\#/g; s/%/\\%/g')
    safe_audience=$(echo "$audience" | sed 's/&/\\&/g; s/_/\\_/g; s/#/\\#/g; s/%/\\%/g')

    "$PANDOC" "$source_md" \
        --from markdown \
        --to pdf \
        --resource-path="$DOCS_DIR" \
        --pdf-engine=xelatex \
        --include-in-header="$header_file" \
        --toc --toc-depth=2 \
        -V toc-title="$toc_title" \
        -V geometry:margin=1in \
        -V fontsize=11pt \
        -V colorlinks=true \
        -V linkcolor=blue \
        -V urlcolor=blue \
        -V documentclass=article \
        -V title="$safe_title" \
        -V subtitle="$subtitle" \
        -V author="PMI · IPB · BHLK · American Red Cross" \
        -V date="Version ${version} | Audience: ${safe_audience} | Built ${build_date}" \
        -o "$pdf_file" 2>/dev/null

    local rc=$?
    rm -f "$header_file"
    [ -n "$translated_tmp" ] && rm -f "$translated_tmp"

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

LANG_LABEL="English"
[ "$LANG" = "id" ] && LANG_LABEL="Bahasa Indonesia"

echo "Building PDFs (${ENGINE}, ${LANG_LABEL})..."
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
