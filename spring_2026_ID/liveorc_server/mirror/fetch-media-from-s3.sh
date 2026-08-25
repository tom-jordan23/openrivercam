#!/bin/bash
# fetch-media-from-s3.sh — download the media export from S3 and prove it is good.
#
# RUN THIS ON YOUR WORKSTATION. The host half is export-media-to-s3.sh.
#
# WHY
#   The export puts LiveORC's media in S3 as one tar per top-level directory.
#   Pulling from S3 touches the LiveORC host not at all — which is the entire
#   point after the API pull took it down on 2026-08-25.
#
# WHAT IT VERIFIES, and why each check exists
#   1. sha256 of the downloaded tar vs what the host recorded as it uploaded.
#      Proves the bytes survived S3 and the network.
#   2. Extracted files vs the host's filelist, by name AND size. This is the
#      check that matters: if tar died mid-stream on the host, the object is a
#      valid but SHORT tar, and its sha256 matches perfectly on both ends. Only
#      the filelist notices the missing files.
#   3. A sample re-checksummed against manifest.json, where orc_mirror.py already
#      recorded sha256 for the 773 files it pulled through the API. Two entirely
#      independent paths — REST/DRF and tar/S3 — agreeing on the same bytes is
#      much stronger evidence than either alone.
#
# WHAT IT TOUCHES
#   Downloads to data/liveorc-mirror/, gitignored at the repo root. This repo is
#   public: no media is ever committed. Extraction OVERWRITES files already
#   there — intended, since the tar is the more complete copy.
#
# USAGE
#   ./fetch-media-from-s3.sh --site 4 --check     # what is in S3, download nothing
#   ./fetch-media-from-s3.sh --site 4             # fetch, extract, verify
#   ./fetch-media-from-s3.sh --site 4 --dir videos
#   ./fetch-media-from-s3.sh --site 4 --verify-only
#
# Safe to re-run. Tars are kept until verified, then removed unless --keep-tars.

set -euo pipefail

PROFILE="${AWS_PROFILE_LIVEORC:-liveorc}"
BUCKET="${BUCKET:-s3://openrivercam-video}"
PREFIX="${PREFIX:-media-mirror}"
SITE=""
ONLY_DIR=""
CHECK=0
VERIFY_ONLY=0
KEEP_TARS=0

die() { echo "ERROR: $*" >&2; exit 1; }

while [[ $# -gt 0 ]]; do
  case "$1" in
    --site)        SITE="$2"; shift 2 ;;
    --dir)         ONLY_DIR="$2"; shift 2 ;;
    --check)       CHECK=1; shift ;;
    --verify-only) VERIFY_ONLY=1; shift ;;
    --keep-tars)   KEEP_TARS=1; shift ;;
    --profile)     PROFILE="$2"; shift 2 ;;
    --bucket)      BUCKET="$2"; shift 2 ;;
    --prefix)      PREFIX="$2"; shift 2 ;;
    -h|--help)     sed -n '2,40p' "$0"; exit 0 ;;
    *)             die "unknown argument: $1" ;;
  esac
done

[[ -n "$SITE" ]] || die "--site is required (the mirror is laid out per site)"

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
ROOT="$REPO_ROOT/data/liveorc-mirror"
SITE_DIR="$ROOT/$SITE"
MEDIA_DIR="$SITE_DIR/media"
TAR_DIR="$SITE_DIR/s3-tars"
MANIFEST="$SITE_DIR/manifest.json"

mkdir -p "$MEDIA_DIR" "$TAR_DIR"

echo
echo "Media fetch from S3"
echo "  source    $BUCKET/$PREFIX/"
echo "  profile   $PROFILE"
echo "  extract   $MEDIA_DIR"
echo

aws --profile "$PROFILE" sts get-caller-identity >/dev/null 2>&1 \
  || die "AWS profile '$PROFILE' has no usable credentials"

echo "In S3:"
aws --profile "$PROFILE" s3 ls "$BUCKET/$PREFIX/" || die "cannot list $BUCKET/$PREFIX/"
echo

mapfile -t DIRS < <(aws --profile "$PROFILE" s3 ls "$BUCKET/$PREFIX/" \
  | awk '{print $4}' | grep '\.tar$' | sed 's/\.tar$//' | sort -u)
[[ ${#DIRS[@]} -gt 0 ]] || die "no .tar objects under $BUCKET/$PREFIX/ — has the host export run?"

if [[ -n "$ONLY_DIR" ]]; then
  printf '%s\n' "${DIRS[@]}" | grep -qx "$ONLY_DIR" || die "$ONLY_DIR.tar not in S3"
  DIRS=("$ONLY_DIR")
fi

if [[ $CHECK -eq 1 ]]; then
  echo "Would fetch: ${DIRS[*]}"
  echo "Check only — nothing downloaded."
  exit 0
fi

FAILED=0

for dir in "${DIRS[@]}"; do
  echo "=== $dir ==="
  tar_path="$TAR_DIR/$dir.tar"
  list_path="$TAR_DIR/$dir.filelist.txt"

  aws --profile "$PROFILE" s3 cp "$BUCKET/$PREFIX/$dir.filelist.txt" "$list_path" --only-show-errors
  expect_sha="$(aws --profile "$PROFILE" s3 cp "$BUCKET/$PREFIX/$dir.tar.sha256" - 2>/dev/null | cut -d' ' -f1 || true)"

  if [[ $VERIFY_ONLY -eq 0 ]]; then
    echo "  downloading $dir.tar ..."
    aws --profile "$PROFILE" s3 cp "$BUCKET/$PREFIX/$dir.tar" "$tar_path"
  fi
  [[ -f "$tar_path" ]] || die "$tar_path missing — run without --verify-only first"

  # 1. transport integrity
  if [[ -n "$expect_sha" ]]; then
    echo "  checksumming ..."
    got_sha="$(sha256sum "$tar_path" | cut -d' ' -f1)"
    if [[ "$got_sha" == "$expect_sha" ]]; then
      echo "  sha256 OK"
    else
      echo "  SHA256 MISMATCH"
      echo "    host said $expect_sha"
      echo "    we have   $got_sha"
      FAILED=1; continue
    fi
  else
    echo "  WARNING: no .sha256 in S3 — transport integrity unverified"
  fi

  # 2. extract
  if [[ $VERIFY_ONLY -eq 0 ]]; then
    echo "  extracting ..."
    tar -xf "$tar_path" -C "$MEDIA_DIR"
  fi

  # 3. completeness — the check a matching sha cannot make
  echo "  verifying against the host's file list ..."
  missing=0; wrong=0; ok=0
  while IFS=$'\t' read -r rel size; do
    [[ -n "$rel" ]] || continue
    f="$MEDIA_DIR/$dir/$rel"
    if [[ ! -f "$f" ]]; then
      missing=$((missing+1))
      [[ $missing -le 5 ]] && echo "    MISSING $dir/$rel"
    elif [[ "$(stat -c%s "$f")" != "$size" ]]; then
      wrong=$((wrong+1))
      [[ $wrong -le 5 ]] && echo "    SIZE    $dir/$rel"
    else
      ok=$((ok+1))
    fi
  done < "$list_path"

  echo "  $ok ok, $missing missing, $wrong wrong size"
  if [[ $missing -gt 0 || $wrong -gt 0 ]]; then
    echo "  INCOMPLETE — the tar was probably truncated on the host. Re-export $dir."
    FAILED=1
  elif [[ $KEEP_TARS -eq 0 && $VERIFY_ONLY -eq 0 ]]; then
    rm -f "$tar_path"
    echo "  verified; removed local tar (--keep-tars to retain)"
  fi
  echo
done

# 4. cross-check the two independent paths against each other
if [[ -f "$MANIFEST" ]] && command -v python3 >/dev/null; then
  echo "=== cross-check vs manifest.json (API-pulled checksums) ==="
  python3 - "$MANIFEST" "$MEDIA_DIR" <<'PY'
import hashlib, json, sys
from pathlib import Path

manifest, media = Path(sys.argv[1]), Path(sys.argv[2])
# manifest.json records asset paths relative to the MIRROR ROOT
# (e.g. "4/media/videos/4/<date>/<file>.mp4"), which is media/../..
root = media.parents[1]
data = json.loads(manifest.read_text())

known = []
for rec in data.get("videos", []):
    a = (rec.get("assets") or {}).get("file")
    if a and a.get("sha256") and a.get("path"):
        known.append((rec["id"], a["path"], a["sha256"]))

if not known:
    print("  no API-pulled checksums recorded yet — nothing to cross-check")
    sys.exit(0)

# spread the sample across the whole range rather than taking the first N,
# so a failure confined to one date window still shows up
step = max(1, len(known) // 20)
sample = known[::step][:20]
match = mismatch = absent = 0
for vid, path, sha in sample:
    f = root / path
    if not f.exists():
        absent += 1
        continue
    h = hashlib.sha256()
    with open(f, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    if h.hexdigest() == sha:
        match += 1
    else:
        mismatch += 1
        print(f"  MISMATCH video {vid}: {path}")

print(f"  {match} match, {mismatch} mismatch, {absent} not found (of {len(sample)} sampled)")
if mismatch:
    print("  The REST path and the tar path disagree. Investigate before trusting either.")
    sys.exit(1)
if match:
    print("  Two independent paths agree on the same bytes.")
PY
  echo
fi

if [[ $FAILED -ne 0 ]]; then
  echo "One or more directories failed verification."
  exit 1
fi
echo "All directories fetched and verified."
echo
