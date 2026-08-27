#!/bin/bash
# orc_reclaim_nonvideo.sh — free station disk WITHOUT deleting any video.
# ISS-FIELD-009.
#
# WHY
#   The station sits below its 5 GB purge threshold, so ORC-OS purges every
#   300 s. Every synced video is already gone, so what it deletes now is
#   un-synced video — the only copy. The purge is actively destroying the
#   backlog while we discuss what to do with it.
#
#   Roughly 5.5 GB of NON-video space is recoverable. Taking it stops the purge
#   immediately at zero data cost, which is what makes every other option
#   possible: transferring the backlog off the station takes days at LTE speed
#   over 2-minute wake windows, and there is no point starting that while the
#   thing being transferred is being deleted underneath it.
#
#   So this runs first, always, whatever is decided about the video itself.
#
# WHAT IT TOUCHES
#   Tier 1 (--apply, no questions): pip/npm caches and __pycache__. Regenerable
#   by definition.
#   Tier 2 (--apply): files under .ORC-OS/tmp older than 24 h. Scratch space; a
#   day-old temp file belongs to a run that ended long ago. Anything newer is
#   left alone in case a job is mid-flight.
#   Never: /home/pi/.ORC-OS/uploads/** — no video is touched by this script at
#   all, by design.
#
#   /home/pi/code/git is 3.9 GB and the largest single win, but it is a git
#   working tree that may hold unpushed local commits. This script only REPORTS
#   on it — deciding that is not something to do inside a 2-minute window.
#
# USAGE
#   ssh pi@orc-sukabumi 'sudo bash -s'         < orc_reclaim_nonvideo.sh   # dry
#   ssh pi@orc-sukabumi 'sudo bash -s -- --apply' < orc_reclaim_nonvideo.sh

set -u
APPLY=0
[ "${1:-}" = "--apply" ] && APPLY=1

free_gib() { df -B1 --output=avail / | tail -1 | awk '{printf "%.2f", $1/1073741824}'; }

echo "free before : $(free_gib) GiB"
[ "$APPLY" = 1 ] && echo "MODE: APPLY" || echo "MODE: dry run"

sum() { du -sb "$@" 2>/dev/null | awk '{s+=$1} END {printf "%.2f", s/1073741824}'; }

echo
echo "=== tier 1: caches (regenerable) ==="
for d in /home/pi/.cache/pip /root/.cache/pip /home/pi/.npm; do
    [ -d "$d" ] && echo "  $d  $(sum "$d") GiB"
done
PYC=$(find /home/pi -xdev -type d -name __pycache__ 2>/dev/null | wc -l)
echo "  __pycache__ dirs: $PYC"
if [ "$APPLY" = 1 ]; then
    rm -rf /home/pi/.cache/pip /root/.cache/pip /home/pi/.npm 2>/dev/null
    find /home/pi -xdev -type d -name __pycache__ -prune -exec rm -rf {} + 2>/dev/null
    echo "  -> cleared"
fi

echo
echo "=== tier 2: .ORC-OS/tmp older than 24h ==="
T=/home/pi/.ORC-OS/tmp
if [ -d "$T" ]; then
    echo "  total tmp        : $(sum "$T") GiB"
    OLD=$(find "$T" -xdev -type f -mtime +1 2>/dev/null | wc -l)
    echo "  files older than 1 day: $OLD"
    if [ "$APPLY" = 1 ] && [ "$OLD" -gt 0 ]; then
        find "$T" -xdev -type f -mtime +1 -delete 2>/dev/null
        find "$T" -xdev -type d -empty -delete 2>/dev/null
        echo "  -> cleared"
    fi
else
    echo "  (no $T)"
fi

echo
echo "=== report only: /home/pi/code/git ==="
G=/home/pi/code/git
if [ -d "$G" ]; then
    echo "  size: $(sum "$G") GiB"
    for r in "$G"/*/; do
        [ -d "$r/.git" ] || continue
        echo "  repo $r"
        echo "    .git       : $(sum "$r/.git") GiB"
        echo "    unpushed   : $(git -C "$r" log --oneline @{u}..HEAD 2>/dev/null | wc -l) commits"
        echo "    dirty files: $(git -C "$r" status --porcelain 2>/dev/null | wc -l)"
    done
else
    echo "  (absent)"
fi

echo
echo "free after  : $(free_gib) GiB"
[ "$APPLY" = 0 ] && echo "DRY RUN — nothing deleted. Re-run with --apply."
