#!/bin/bash
# export-media-to-s3.sh — stream LiveORC's media tree to S3, from the host.
#
# RUN THIS ON THE LIVEORC HOST (AWS EC2, via Session Manager).
# The local half is fetch-media-from-s3.sh, which runs on your workstation.
#
# WHY
#   TODO-114 needs an independent copy of the media, and the first attempt —
#   pulling 2630 videos through the REST API — put the host on the floor on
#   2026-08-25 after 773 files. Serving media through Django means DRF, the app
#   server and a request per file; sustained for an hour on a t3.large that was
#   already working a celery backlog, it took LiveORC down hard enough to need a
#   reboot.
#
#   Reading the same bytes with tar and streaming them to S3 costs plain I/O and
#   nothing else. EC2 -> S3 in-region is free and fast, and the download half
#   then puts ZERO load on this host.
#
#   It also captures what the API cannot. There is no /keyframe/ route on the
#   video detail endpoint, so ~1.3 GB of keyframes are unreachable over REST.
#   tar sees the whole tree, which turns the mirror from "the API-visible
#   subset" into an actual complete copy — which is what TODO-114 has to be if
#   it is going to gate TODO-112.
#
# WHAT IT TOUCHES
#   The LiveORC container: READ ONLY. `docker exec` + `tar -c` reads files and
#   writes nothing. No docker cp (that would land 26 GB on the host disk), no
#   package installs, no config edits. Verifiable afterwards with `docker diff`.
#
#   The host disk: nothing but a few small text files under /tmp. The tar is
#   never written to disk — it streams straight into `aws s3 cp -`.
#
#   Bandwidth: sets `default.s3.max_bandwidth` in the RUNNING user's AWS CLI
#   config — which is why this must be run entirely as one user. Setting it as
#   ssm-user and then running the export under sudo leaves root unthrottled. So
#   the upload cannot saturate the box the way the API pull did. Printed on every
#   run; --no-throttle skips it. Unset later with:
#     aws configure set default.s3.max_bandwidth ''
#
# WHAT IT WRITES TO S3, per directory
#   <prefix>/<dir>.filelist.txt   every file with its size — the ONLY thing that
#                                 detects a truncated tar (a sha matches happily
#                                 across a short stream; a missing file does not)
#   <prefix>/<dir>.tar            the data
#   <prefix>/<dir>.tar.sha256     checksum of the stream as it was uploaded
#
# USAGE
#   ./export-media-to-s3.sh --check              # discovery + validation only
#   ./export-media-to-s3.sh --dir videos         # one directory (start here)
#   ./export-media-to-s3.sh                      # all of them, in order
#
# Safe to re-run: each directory is re-exported and overwritten wholesale.

set -euo pipefail

CONTAINER="${CONTAINER:-liveorc_webapp}"
MEDIA_ROOT="${MEDIA_ROOT:-/liveorc/media}"
BUCKET="${BUCKET:-s3://openrivercam-video}"
PREFIX="${PREFIX:-media-mirror}"
RATE="${RATE:-8MB/s}"
THROTTLE=1
ONLY_DIR=""
CHECK=0

die() { echo "ERROR: $*" >&2; exit 1; }
say() { echo "$*"; }

while [[ $# -gt 0 ]]; do
  case "$1" in
    --check)       CHECK=1; shift ;;
    --dir)         ONLY_DIR="$2"; shift 2 ;;
    --rate)        RATE="$2"; shift 2 ;;
    --no-throttle) THROTTLE=0; shift ;;
    --bucket)      BUCKET="$2"; shift 2 ;;
    --prefix)      PREFIX="$2"; shift 2 ;;
    -h|--help)     sed -n '2,50p' "$0"; exit 0 ;;
    *)             die "unknown argument: $1" ;;
  esac
done

# ---------------------------------------------------------------- discovery ---
command -v docker >/dev/null || die "docker not found — is this the LiveORC host?"
command -v aws    >/dev/null || die "aws CLI not found"

# Session Manager's ssm-user is not in the docker group, so plain `docker` gets
# "permission denied ... /var/run/docker.sock". Never suppress that stderr: with
# 2>/dev/null it looks identical to an empty media tree, which cost us a round
# trip on 2026-08-25.
if docker info >/dev/null 2>&1; then
  DOCKER="docker"
elif sudo -n docker info >/dev/null 2>&1; then
  DOCKER="sudo docker"
else
  die "cannot reach the docker daemon as $(id -un).
     Re-run the whole script under sudo:  sudo -E ./export-media-to-s3.sh ...
     Run it ENTIRELY as one user — see the bandwidth note in the header."
fi
say "Docker via     $DOCKER"

$DOCKER inspect -f '{{.State.Running}}' "$CONTAINER" 2>/dev/null | grep -q true \
  || die "container $CONTAINER is not running"

say "Container      $CONTAINER"
say "Media root     $MEDIA_ROOT"
say "Destination    $BUCKET/$PREFIX/"

IDENTITY="$(aws sts get-caller-identity --query Arn --output text 2>&1)" \
  || die "no usable AWS credentials on this host: $IDENTITY"
say "AWS identity   $IDENTITY"

# `find -printf` is GNU-specific; fail loudly rather than silently producing an
# empty filelist, which would make a truncated tar look complete.
$DOCKER exec "$CONTAINER" find "$MEDIA_ROOT" -maxdepth 0 -printf '' 2>/dev/null \
  || die "find -printf unsupported in $CONTAINER — the filelist check cannot run"

mapfile -t DIRS < <($DOCKER exec "$CONTAINER" sh -c "ls -1 $MEDIA_ROOT" 2>/dev/null | tr -d '\r')
[[ ${#DIRS[@]} -gt 0 ]] || die "no directories under $MEDIA_ROOT"

say ""
say "Directories under $MEDIA_ROOT:"
for d in "${DIRS[@]}"; do
  size="$($DOCKER exec "$CONTAINER" du -sh "$MEDIA_ROOT/$d" 2>/dev/null | cut -f1)"
  count="$($DOCKER exec "$CONTAINER" sh -c "find '$MEDIA_ROOT/$d' -type f | wc -l" 2>/dev/null | tr -d ' \r')"
  printf '  %-20s %-8s %s files\n' "$d" "${size:-?}" "${count:-?}"
done
say ""

df -h / | tail -1 | awk '{printf "Host disk /    %s used of %s (%s), %s free\n", $3, $2, $5, $4}'
say ""

if [[ $CHECK -eq 1 ]]; then
  say "Check only — nothing uploaded."
  say "Run with --dir <name> to export one directory, or with no arguments for all."
  exit 0
fi

# ----------------------------------------------------------------- throttle ---
if [[ $THROTTLE -eq 1 ]]; then
  # Written to THIS user's ~/.aws/config. If you set it by hand as ssm-user and
  # then run this under sudo, root's config has no limit and the upload runs
  # unthrottled. Setting it here, as the running user, keeps the two in step.
  aws configure set default.s3.max_bandwidth "$RATE"
  say "Upload throttled to $RATE (unset later: aws configure set default.s3.max_bandwidth '')"
else
  say "WARNING: --no-throttle. This is what put the host on the floor last time."
fi
say ""

# ------------------------------------------------------------------ export ----
TARGETS=("${DIRS[@]}")
if [[ -n "$ONLY_DIR" ]]; then
  printf '%s\n' "${DIRS[@]}" | grep -qx "$ONLY_DIR" || die "$ONLY_DIR not found under $MEDIA_ROOT"
  TARGETS=("$ONLY_DIR")
fi

for dir in "${TARGETS[@]}"; do
  say "=== $dir ==="
  tmp_list="$(mktemp)"; tmp_sha="$(mktemp)"
  trap 'rm -f "$tmp_list" "$tmp_sha"' EXIT

  # 1. filelist first — the thing that proves the tar is complete
  say "  building file list ..."
  $DOCKER exec "$CONTAINER" find "$MEDIA_ROOT/$dir" -type f -printf '%P\t%s\n' > "$tmp_list"
  files="$(wc -l < "$tmp_list" | tr -d ' ')"
  bytes="$(awk -F'\t' '{s+=$2} END {print s+0}' "$tmp_list")"
  say "  $files files, $bytes bytes"

  if [[ "$files" -eq 0 ]]; then
    say "  empty — skipping"
    rm -f "$tmp_list" "$tmp_sha"; trap - EXIT
    continue
  fi

  aws s3 cp "$tmp_list" "$BUCKET/$PREFIX/$dir.filelist.txt" --only-show-errors
  say "  uploaded $dir.filelist.txt"

  # 2. the data. tar streams into aws; nothing lands on the host disk. tee
  #    fingerprints the exact bytes that go up, so the download can prove it
  #    received what was sent.
  #    --expected-size only sizes the multipart chunks; a rough figure is fine.
  expected=$(( bytes + files * 1024 + 10485760 ))
  say "  streaming to $BUCKET/$PREFIX/$dir.tar ..."
  set +e
  $DOCKER exec "$CONTAINER" tar -cf - -C "$MEDIA_ROOT" "$dir" \
    | tee >(sha256sum | cut -d' ' -f1 > "$tmp_sha") \
    | aws s3 cp - "$BUCKET/$PREFIX/$dir.tar" \
        --expected-size "$expected" --only-show-errors
  rc=("${PIPESTATUS[@]}")
  set -e
  # Both ends must succeed. A tar that dies mid-stream still gives aws a valid
  # (short) object, and its sha would match on download — only this check and
  # the filelist catch it.
  [[ "${rc[0]}" -eq 0 ]] || die "tar failed (exit ${rc[0]}) — $dir.tar is INCOMPLETE, do not trust it"
  [[ "${rc[2]}" -eq 0 ]] || die "aws s3 cp failed (exit ${rc[2]}) for $dir"

  sha="$(cat "$tmp_sha")"
  printf '%s  %s.tar\n' "$sha" "$dir" | aws s3 cp - "$BUCKET/$PREFIX/$dir.tar.sha256" --only-show-errors
  say "  sha256 $sha"
  say "  done"
  say ""

  rm -f "$tmp_list" "$tmp_sha"; trap - EXIT
done

say "Export complete. On your workstation:"
say "  ./mirror/fetch-media-from-s3.sh --site 4"
