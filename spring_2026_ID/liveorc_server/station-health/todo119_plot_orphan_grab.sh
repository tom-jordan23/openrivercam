set -u
# TODO-119 / ISS-FIELD-013, Stage 1: can the quiver plots of videos that have lost their mp4
# ("orphaned plots") be deleted without harm? READ-ONLY. Nothing is deleted, moved, chmod'd or written
# (stdout only; no temp files). Run through todo119_wake_runner.py (bash -s over ssh) in one wake.
# Station times are UTC. NOT RUN YET: needs Tom's go.
#
# WHY: free space is ~5.1 GiB against ORC-OS's 5.0 purge threshold (11-13). The 10-14 census found ~8 GiB of
# quiver plots (8,132 .jpg vs 3,357 .mp4 now). ORC-OS's purge deletes oldest-first, so a plot outlives its
# mp4; a plot WITHOUT its mp4 leaves, when deleted, the state the disk manager already produces ("row exists,
# no files"). A plot WITH its mp4 left behind is a state ORC-OS never creates, so it is out of scope here.
#
# UNIT: one video = one directory uploads/videos/<YYYYMMDD>/<video id>/ (id = video.id in the ORC-OS DB).
# QUESTIONS (each section answers one):
#   1 what columns/paths does the DB hold (does anything point at a plot?) and what do file/image/thumbnail look like
#   2 does ORC-OS code reference plot_quiver, and what does serving a missing file do?
#   3 how many plots are orphaned (no mp4 in the dir), how big, how old, and what does the DB say about them?
#   4 what is the "disk manager" free-space unit (GB vs GiB)?
#   5 has ORC-OS already run with missing files (journal), and is swap in use?
# No sudo except a read-only retry of journalctl. Every step has a timeout and runs nice/ionice.
# Env overrides (tests only): ISS_V ISS_DB ISS_PKG ISS_WEB ISS_SKIP_JOURNAL.

main() {
V="${ISS_V:-/home/pi/.ORC-OS/uploads/videos}"
DB="${ISS_DB:-/home/pi/.ORC-OS/orc-os.db}"
PKG="${ISS_PKG:-/home/pi/venv/orc-os/lib/python3.13/site-packages/orc_api}"
WEB="${ISS_WEB:-/var/www}"
N="nice -n 19 ionice -c3"
sec() { echo; echo "=== $1 ==="; }
# Only a real timeout (rc 124) is reported; grep finding nothing (rc 1) is not "stopped".
t() { local s=$1 rc; shift; timeout "$s" "$@" 2>&1; rc=$?; [ "$rc" -eq 124 ] && echo "  (TIMED OUT after ${s}s; output above is partial)"; return 0; }
ro() { sqlite3 -separator '|' "file:$DB?mode=ro" "$@" 2>&1; }

echo "=== PLOT ORPHAN GRAB $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
echo "  free: $(df -B1M --output=avail,pcent / 2>/dev/null | tail -1)   (MiB avail, use%)   uptime s: $(cut -d' ' -f1 /proc/uptime | cut -d. -f1)"
command -v sqlite3 >/dev/null || { echo "REFUSED: sqlite3 not installed"; return 2; }
[ -r "$DB" ] || { echo "REFUSED: $DB not readable"; return 2; }

sec "1. DB: columns that could point at a plot or output file, and what file/image/thumbnail hold"
ro "SELECT m.name, p.name FROM sqlite_master m, pragma_table_info(m.name) p
    WHERE m.type='table' AND (p.name LIKE '%plot%' OR p.name LIKE '%jpg%' OR p.name LIKE '%output%' OR p.name LIKE '%image%'
          OR p.name LIKE '%path%' OR p.name LIKE '%file%' OR p.name LIKE '%thumb%') ORDER BY 1,2;" | sed 's/^/  /'
echo "  video rows by sync_status: $(ro "SELECT ifnull(sync_status,'NULL')||'='||count(*) FROM video GROUP BY 1;" | tr '\n' ' ')"
echo "  3 newest rows (id|timestamp|status|sync_status|file|image|thumbnail):"
ro "SELECT id,timestamp,status,ifnull(sync_status,'NULL'),file,image,thumbnail FROM video ORDER BY id DESC LIMIT 3;" | cut -c1-230 | sed 's/^/    /'
echo "  3 oldest rows:"
ro "SELECT id,timestamp,status,ifnull(sync_status,'NULL'),file,image,thumbnail FROM video ORDER BY id ASC LIMIT 3;" | cut -c1-230 | sed 's/^/    /'
echo "  any column anywhere mentioning 'plot_quiver' (text columns of video/time_series/video_config):"
ro "SELECT count(*) FROM video WHERE file LIKE '%plot%' OR image LIKE '%plot%' OR thumbnail LIKE '%plot%';" | sed 's/^/    video rows with plot in file/image/thumbnail: /'

sec "2. code: who references plot_quiver, and how a missing file is handled"
echo "  orc_api python files mentioning plot_quiver:"; t 25 $N grep -rIn "plot_quiver" "$PKG" --include=*.py | head -12 | cut -c1-200 | sed 's/^/    /'
echo "  web assets mentioning plot_quiver (names only):"; t 25 $N grep -rIl "plot_quiver" "$WEB" /home/pi/.ORC-OS/static 2>/dev/null | head -8 | sed 's/^/    /'
echo "  routes that serve files from uploads (FileResponse / StaticFiles / mount):"
t 25 $N grep -rIn "FileResponse\|StaticFiles\|\.mount(" "$PKG" --include=*.py | head -12 | cut -c1-200 | sed 's/^/    /'
echo "  what the video sync uploads (files=, open(, plot, thumbnail) in the sync/queue code:"
t 25 $N grep -rIn "files=\|\"file\"\|'file'\|thumbnail\|plot" "$PKG/utils/queue.py" "$PKG/utils/sync.py" "$PKG/db/video.py" 2>/dev/null | head -14 | cut -c1-200 | sed 's/^/    /'
echo "  delete_file in the disk manager (how it removes a file and whether it touches the DB row):"
t 15 grep -n "def delete_file" -A14 "$PKG/utils/disk_management.py" | cut -c1-170 | sed 's/^/    /'

sec "4. disk manager free-space unit (GB vs GiB)"
t 15 grep -n "def get_free_space" -A10 "$PKG/utils/disk_management.py" | cut -c1-170 | sed 's/^/  /'
echo "  configured min_free_space: $(ro "SELECT min_free_space FROM disk_management ORDER BY id DESC LIMIT 1;")   (table disk_management)"

sec "3. orphaned plots: one pass over uploads/videos, grouped by video directory"
echo "  layout samples (newest dir, and the oldest dir that still has files):"
days=$(ls -1 "$V" 2>/dev/null | grep -E '^[0-9]{8}$' | sort); newest=$(printf '%s\n' "$days" | tail -1); oldest=$(printf '%s\n' "$days" | head -1)
for dd in "$newest" "$oldest"; do
  [ -n "$dd" ] || continue
  vd=$(ls -1 "$V/$dd" 2>/dev/null | sort -n | tail -1)
  echo "    $dd/$vd:"; t 10 find "$V/$dd/$vd" -maxdepth 3 -printf '      %P  %s\n' | head -14
done
echo "  (reading every file's size and mtime; max 90 s)"
L=$(t 90 $N find "$V" -xdev -type f -printf '%s|%T@|%P\n')
nlines=$(printf '%s\n' "$L" | grep -c '|')
echo "  files listed: $nlines"
[ "$nlines" -gt 0 ] || { echo "  nothing listed; stopping"; return 1; }

echo "  -- per-directory classification (a dir with any .mp4 = has video):"
printf '%s\n' "$L" | awk -F'|' '
  { sz=$1+0; rp=$3; n=split(rp, a, "/"); if (n < 3) { loose++; loose_b+=sz; next }
    key=a[1] "/" a[2]; rest=rp; sub("^[^/]*/[^/]*/", "", rest)
    seen[key]=1; dirb[key]+=sz
    if (rest ~ /\.mp4$/) { mp4n[key]++; mp4b[key]+=sz }
    else if (rest == "output/plot_quiver.jpg") { plot[key]=sz }
    else if (rest ~ /\.jpg$/) { jpgo[key]+=sz }
  }
  END { G=1073741824
    for (k in seen) { dirs++; hv=(k in mp4n)
      if (hv) { dv++; mp4_total+=mp4b[k] } else { dn++; dn_b+=dirb[k] }
      if (k in plot) { if (hv) { pw++; pw_b+=plot[k] } else { po++; po_b+=plot[k]; split(k, p, "/"); ym=substr(p[1],1,6); pom[ym]++; pomb[ym]+=plot[k] } }
      if (k in jpgo) { jo+=jpgo[k] } }
    printf "    video dirs: %d  (with mp4: %d, without mp4: %d)   files not under a video dir: %d (%.3f GiB)\n", dirs, dv, dn, loose, loose_b/G
    printf "    all bytes in dirs WITHOUT an mp4 (plots, nc, hash, yml...): %.2f GiB\n", dn_b/G
    printf "    plot_quiver.jpg  WITH mp4 present : %5d files %7.2f GiB   (out of scope for round 1)\n", pw, pw_b/G
    printf "    plot_quiver.jpg  ORPHANED (no mp4): %5d files %7.2f GiB   <- the candidate set\n", po, po_b/G
    printf "    other .jpg bytes (not plot_quiver): %.2f GiB\n", jo/G
    print "    orphaned plots by month of the video date (YYYYMM files GiB):"
    for (m in pom) printf "      %s %5d %7.3f\n", m, pom[m], pomb[m]/G }' | sed 's/^/  /'

echo "  -- join with the DB: id, plot bytes, has_mp4 (from the filesystem) x sync_status (from the DB)"
rows=$(ro "SELECT id||' '||ifnull(sync_status,'NULL') FROM video;")
# join in awk: first input = DB rows, second = the filesystem summary produced above
join_in=$(printf '%s\n' "$L" | awk -F'|' '
  { rp=$3; n=split(rp, a, "/"); if (n < 3) next; key=a[1] "/" a[2]; id=a[2]; rest=rp; sub("^[^/]*/[^/]*/", "", rest)
    if (rest ~ /\.mp4$/) hv[key]=1
    if (rest == "output/plot_quiver.jpg") { pb[key]=$1+0; pid[key]=id } }
  END { for (k in pb) print "F", pid[k], pb[k], ((k in hv) ? "mp4" : "NOMP4") }')
{ printf '%s\n' "$rows" | sed 's/^/D /'; printf '%s\n' "$join_in"; } | awk '
  $1=="D" { ss[$2]=$3; next }
  $1=="F" { st = ($2 in ss) ? ss[$2] : "NO_DB_ROW"; k=$4 " / " st; c[k]++; b[k]+=$3 }
  END { G=1073741824; for (k in c) printf "    %-24s %5d plots %7.3f GiB\n", k, c[k], b[k]/G }' | sort | sed 's/^/  /'
echo "  (NOMP4 / SYNCED = plot of a video that reached LiveORC and has lost its mp4: the safest set;"
echo "   NOMP4 / FAILED or LOCAL = the mp4 is gone AND it never synced: these plots are the last trace; keep for now)"

sec "5. natural experiment and memory"
echo "  ORC-OS journal, last 3 days: lines about missing files (ORC-OS has already run with deleted files):"
if [ -z "${ISS_SKIP_JOURNAL:-}" ]; then
  jl=$(timeout 25 journalctl -u orc-api --since "3 days ago" --no-pager 2>&1)
  case "$jl" in *"insufficient permissions"*|*"No journal files"*) jl=$(timeout 25 sudo -n journalctl -u orc-api --since "3 days ago" --no-pager 2>&1) ;; esac
  printf '%s\n' "$jl" | grep -ci "no such file\|filenotfound\|not found" | sed 's/^/    count: /'
  printf '%s\n' "$jl" | grep -i "no such file\|filenotfound" | tail -4 | cut -c1-220 | sed 's/^/    /'
  printf '%s\n' "$jl" | grep -i "purg\|free space\|disk" | tail -6 | cut -c1-220 | sed 's/^/    disk-manager: /'
fi
echo "  memory/swap:"; free -m | sed 's/^/    /'; swapon --show 2>&1 | sed 's/^/    /'
echo "  memory pressure (psi):"; cat /proc/pressure/memory 2>&1 | sed 's/^/    /'

echo; echo "=== END ==="
}
main </dev/null
