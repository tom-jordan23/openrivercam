set -u
# TODO-119 / ISS-FIELD-013: follow-up to todo119_plot_orphan_grab.sh (11-13). READ-ONLY. Nothing is deleted,
# moved or written (stdout only). Run through todo119_wake_runner.py in one wake. Station times are UTC. NOT RUN YET.
#
# What the first grab found (data/station-forensics/orc-sukabumi-plotorphan1113-20261113T150041Z.txt):
#   * the disk manager measures free space in GiB and runs ~5 s after each ORC-OS start (every wake): 5.087 GiB at
#     15:00 against a 5.0 minimum, falling ~13 MiB per wake, so it first PURGES at about the 18:30 UTC wake;
#   * only 1,076 plots (2.85 GiB, all SYNCED, all July/August) are orphaned; 2,311 plots (6.18 GiB) still have their mp4;
#   * the DB `image` column of every row points at output/plot_quiver.jpg, and video.py serves it at /{id}/image/.
# QUESTIONS:
#   1 do the sync settings upload the plot (sync_image) and the mp4 (sync_file)? how does /image/ behave on a missing file?
#   2 what would the purge delete FIRST, and how much of that is not yet synced? (oldest mtime first, sync-blind)
#   3 how much synced mp4 is on the disk (the real lever), and are the January-dated offline videos synced?
#   4 is the 2 GiB swap file used, how is it configured, and has the box ever hit the OOM killer?
#   5 what is left in /var/log and the journal?
# Env overrides (tests only): ISS_V ISS_DB ISS_PKG ISS_SWAPCONF ISS_SAMPLE=0 ISS_SKIP_JOURNAL ISS_PURGE_BYTES.

main() {
V="${ISS_V:-/home/pi/.ORC-OS/uploads/videos}"
DB="${ISS_DB:-/home/pi/.ORC-OS/orc-os.db}"
PKG="${ISS_PKG:-/home/pi/venv/orc-os/lib/python3.13/site-packages/orc_api}"
SWAPCONF="${ISS_SWAPCONF:-/etc/dphys-swapfile}"
N="nice -n 19 ionice -c3"
sec() { echo; echo "=== $1 ==="; }
t() { local s=$1 rc; shift; timeout "$s" "$@" 2>&1; rc=$?; [ "$rc" -eq 124 ] && echo "  (TIMED OUT after ${s}s; output above is partial)"; return 0; }
ro() { sqlite3 -separator '|' "file:$DB?mode=ro" "$@" 2>&1; }

echo "=== DISK FOLLOW-UP GRAB $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
echo "  free: $(df -B1M --output=avail,pcent / 2>/dev/null | tail -1)   (MiB avail, use%)   uptime s: $(cut -d' ' -f1 /proc/uptime | cut -d. -f1)"
command -v sqlite3 >/dev/null || { echo "REFUSED: sqlite3 not installed"; return 2; }
[ -r "$DB" ] || { echo "REFUSED: $DB not readable"; return 2; }

sec "1. sync settings and how the plot is served"
ro "SELECT * FROM pragma_table_info('settings');" | cut -d'|' -f2 | tr '\n' ' ' | sed 's|^|  settings columns: |'; echo
ro "SELECT 'sync_file='||ifnull(sync_file,'NULL')||'  sync_image='||ifnull(sync_image,'NULL')||'  video_file_fmt='||ifnull(video_file_fmt,'NULL') FROM settings;" | sed 's/^/  /'
echo "  code that reads sync_image / sync_file:"
t 25 $N grep -rIn "sync_image\|sync_file" "$PKG" --include=*.py | grep -v "schemas/\|alembic\|migrations" | head -14 | cut -c1-210 | sed 's/^/    /'
echo "  video.py: the /image/ and /thumbnail/ endpoints (missing-file handling):"
t 15 grep -n '/image/' -A26 "$PKG/routers/video.py" | cut -c1-170 | sed 's/^/    /'
echo "  video.py: the /thumbnail/ endpoint:"
t 15 grep -n '/thumbnail/' -A20 "$PKG/routers/video.py" | cut -c1-170 | sed 's/^/    /'

sec "2/3. one pass over uploads/videos (size, mtime, path) joined with the DB"
rows=$(ro "SELECT id||' '||ifnull(sync_status,'NULL') FROM video;")
echo "  (reading every file; max 90 s)"
L=$(t 90 $N find "$V" -xdev -type f -printf '%s|%T@|%P\n')
echo "  files listed: $(printf '%s\n' "$L" | grep -c '|')   DB rows: $(printf '%s\n' "$rows" | grep -c ' ')"
[ "$(printf '%s\n' "$L" | grep -c '|')" -gt 0 ] || { echo "  nothing listed; stopping"; return 1; }

echo "  -- the synced-mp4 lever: mp4 bytes by DB sync_status (mp4 present on disk)"
{ printf '%s\n' "$rows" | sed 's/^/D /'; printf '%s\n' "$L" | awk -F'|' '{ n=split($3,a,"/"); if (n>=3 && $3 ~ /\.mp4$/) print "M", a[2], $1+0, a[1] }'; } | awk '
  $1=="D" { ss[$2]=$3; next }
  $1=="M" { st = ($2 in ss) ? ss[$2] : "NO_DB_ROW"; c[st]++; b[st]+=$3 }
  END { G=1073741824; for (k in c) { printf "    mp4 / %-10s %5d clips %7.2f GiB\n", k, c[k], b[k]/G; tc+=c[k]; tb+=b[k] }
        printf "    mp4 / TOTAL      %5d clips %7.2f GiB\n", tc, tb/G }' | sort | sed 's/^/  /'

echo "  -- January-dated offline wakes (dirs 20260111 and 20260112): sync status and size"
{ printf '%s\n' "$rows" | sed 's/^/D /'; printf '%s\n' "$L" | awk -F'|' '{ n=split($3,a,"/"); if (n>=3 && (a[1]=="20260111" || a[1]=="20260112")) print "F", a[2], $1+0, a[1] }'; } | awk '
  $1=="D" { ss[$2]=$3; next }
  $1=="F" { st = ($2 in ss) ? ss[$2] : "NO_DB_ROW"; seen[$2]=1; idst[$2]=st; bytes[$2]+=$3 }
  END { G=1073741824; for (i in seen) { c[idst[i]]++; b[idst[i]]+=bytes[i] }
        for (k in c) printf "    Jan dirs / %-10s %4d videos %7.3f GiB\n", k, c[k], b[k]/G }' | sort | sed 's/^/  /'

echo "  -- PURGE PREVIEW: the 30 oldest files by mtime (what the disk manager deletes first; it ignores sync state)"
printf '%s\n' "$L" | sort -t'|' -k2,2n | head -30 | while IFS='|' read -r sz mt rp; do
  id=$(printf '%s' "$rp" | cut -d/ -f2); st=$(printf '%s\n' "$rows" | awk -v i="$id" '$1==i {print $2; exit}')
  printf '    %s %10s  %-9s %s\n' "$(date -u -d "@${mt%.*}" '+%F %T')" "$sz" "${st:-NO_DB_ROW}" "$rp"
done | cut -c1-200
echo "  -- if free space falls 1 GiB below the threshold, the purge removes the oldest files up to 1 GiB; of those videos:"
{ printf '%s\n' "$rows" | sed 's/^/D /'; printf '%s\n' "$L" | sort -t'|' -k2,2n | awk -F'|' -v lim="${ISS_PURGE_BYTES:-1073741824}" '{ cum+=$1; n=split($3,a,"/"); if (n>=3) print "F", a[2], $1+0, $3; if (cum>=lim) exit }'; } | awk '
  $1=="D" { ss[$2]=$3; next }
  $1=="F" { st = ($2 in ss) ? ss[$2] : "NO_DB_ROW"; if (!($2 in seen)) { seen[$2]=1; vids[st]++; nv++ } files++; fb+=$3; if (first=="") first=$4; last=$4 }
  END { printf "    %d files, %.3f GiB, in %d videos by status:", files, fb/1073741824, nv; for (k in vids) printf " %s=%d", k, vids[k]; printf "\n    first: %s\n    last : %s\n", first, last }' | sed 's/^/  /'

sec "4. swap, memory, and the OOM killer"
echo "  /proc/swaps:"; sed 's/^/    /' /proc/swaps 2>&1
echo "  swap file: $(ls -l /var/swap 2>&1)"
echo "  $SWAPCONF (non-comment lines):"; grep -v '^#\|^$' "$SWAPCONF" 2>&1 | sed 's/^/    /'
echo "  dphys-swapfile: enabled=$(systemctl is-enabled dphys-swapfile 2>&1) active=$(systemctl is-active dphys-swapfile 2>&1)   fstab swap lines: $(grep -c swap /etc/fstab 2>/dev/null)"
echo "  kernel OOM-killer lines in the whole persistent journal (boots listed: $(journalctl --list-boots 2>/dev/null | wc -l)):"
if [ -z "${ISS_SKIP_JOURNAL:-}" ]; then
  oom=$(timeout 40 journalctl -k --no-pager 2>/dev/null | grep -i "out of memory\|oom-kill\|oom_reaper\|invoked oom")
  echo "    count: $(printf '%s' "$oom" | grep -c .)"; printf '%s\n' "$oom" | tail -3 | cut -c1-200 | sed 's/^/    /'
fi
echo "  memory now:"; free -m | sed 's/^/    /'
if [ "${ISS_SAMPLE:-1}" = 1 ]; then
  echo "  processing-peak samples (ORC-OS runs pyorc ~1.5-2.5 min into the wake; waits until uptime >= 100 s, max 75 s):"
  for i in 1 2 3; do
    up=$(cut -d' ' -f1 /proc/uptime | cut -d. -f1)
    if [ "$i" = 1 ] && [ "$up" -lt 100 ]; then w=$((100 - up)); [ "$w" -gt 75 ] && w=75; sleep "$w"; fi
    [ "$i" -gt 1 ] && sleep 25
    echo "    sample $i at uptime $(cut -d' ' -f1 /proc/uptime | cut -d. -f1) s: $(free -m | awk '/Mem:/ {printf "mem used %d MiB avail %d MiB; ", $3, $7} /Swap:/ {printf "swap used %d MiB", $3}')"
    ps -eo rss,comm --sort=-rss 2>/dev/null | head -4 | awk 'NR>0 {printf "      %6.0f MiB  %s\n", $1/1024, $2}'
  done
fi

sec "5. logs"
t 20 du -xsb /var/log/* 2>/dev/null | sort -rn | head -6 | awk '{printf "    %7.1f MiB  %s\n", $1/1048576, $2}'
echo "  journal: $(journalctl --disk-usage 2>&1)"
echo; echo "=== END ==="
}
main </dev/null
