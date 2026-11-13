set -u
# TODO-119 / ISS-FIELD-013: verification before any deletion (2026-11-13). READ-ONLY. Nothing is deleted, moved, renamed or
# written (stdout only). Run through todo119_wake_runner.py in one wake. Station times are UTC. NOT RUN YET.
#
# PART A: is /var/swap (2.0 GiB, dated 2026-03-26) really unused, and can anything bring it back?
#   /proc/swaps lists only /dev/zram0 and there is no dphys-swapfile config or fstab swap line (11-13 grab). Still unchecked:
#   the zram / rpi-swap configuration, any unit or script that mentions /var/swap, whether any process holds the file open,
#   whether a package owns it, and how many blocks it really occupies (a sparse file would free less than 2 GiB).
# PART B: the orphaned quiver plots. Prints one line per orphan (a video dir with output/plot_quiver.jpg and no .mp4) with the
#   DB id, size, sync_status and DB timestamp, so that the workstation can match every orphan one-to-one against the LiveORC
#   listing (match_orphans_to_server.py) before anything is deleted.
# sudo is used only for `lsof` (read-only). Env overrides (tests only): ISS_V ISS_DB ISS_SWAP ISS_SKIP_SYS.

main() {
V="${ISS_V:-/home/pi/.ORC-OS/uploads/videos}"
DB="${ISS_DB:-/home/pi/.ORC-OS/orc-os.db}"
SWAP="${ISS_SWAP:-/var/swap}"
N="nice -n 19 ionice -c3"
sec() { echo; echo "=== $1 ==="; }
t() { local s=$1 rc; shift; timeout "$s" "$@" 2>&1; rc=$?; [ "$rc" -eq 124 ] && echo "  (TIMED OUT after ${s}s; output above is partial)"; return 0; }
ro() { sqlite3 -separator '|' "file:$DB?mode=ro" "$@" 2>&1; }

echo "=== SWAP + ORPHAN VERIFY $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
echo "  free: $(df -B1M --output=avail,pcent / 2>/dev/null | tail -1)   (MiB avail, use%)   uptime s: $(cut -d' ' -f1 /proc/uptime | cut -d. -f1)"

if [ -z "${ISS_SKIP_SYS:-}" ]; then
sec "A1. the file itself, and what it really occupies"
ls -l "$SWAP" "$SWAP".* 2>&1 | sed 's/^/  /'
stat -c '  size %s bytes, %b blocks of %B bytes = %b*%B allocated (a sparse file would show far fewer than size)' "$SWAP" 2>&1
echo "  allocated bytes (du): $(du --block-size=1 "$SWAP" 2>&1 | cut -f1)"
echo "  on the root filesystem: $(df --output=target "$SWAP" 2>&1 | tail -1)   owned by a package? $(dpkg -S "$SWAP" 2>&1 | head -1)"
echo "  open by any process (sudo -n lsof, read-only): $(sudo -n lsof "$SWAP" 2>&1 | head -3 | tr '\n' ' ')"
echo "  fuser: $(sudo -n fuser -v "$SWAP" 2>&1 | head -2 | tr '\n' ' ')"

sec "A2. what the kernel is using for swap"
sed 's/^/  /' /proc/swaps; grep -i "^Swap" /proc/meminfo | sed 's/^/  /'
echo "  swapon --show: $( (command -v swapon || ls /usr/sbin/swapon /sbin/swapon 2>/dev/null | head -1) >/dev/null 2>&1 && /usr/sbin/swapon --show 2>&1 | tr '\n' ';')"
echo "  kernel swap messages this boot:"; t 15 journalctl -k -b --no-pager 2>&1 | grep -i "swap" | head -6 | cut -c1-200 | sed 's/^/    /'

sec "A3. units and configs that could use or recreate /var/swap"
echo "  swap/zram unit files:"; systemctl list-unit-files --no-legend 2>/dev/null | grep -i "swap\|zram" | sed 's/^/    /'
echo "  swap/zram units (all, including inactive):"; systemctl list-units --all --no-legend 2>/dev/null | grep -i "swap\|zram" | cut -c1-170 | sed 's/^/    /'
echo "  failed units now: $(systemctl --failed --no-legend 2>/dev/null | wc -l)"; systemctl --failed --no-legend 2>/dev/null | cut -c1-160 | sed 's/^/    /'
for f in /etc/rpi /etc/systemd/zram-generator.conf /etc/systemd/zram-generator.conf.d /usr/lib/systemd/zram-generator.conf; do
  [ -e "$f" ] || continue
  echo "  -- $f"; t 10 find "$f" -maxdepth 3 -type f | head -12 | sed 's/^/     file: /'
  t 10 find "$f" -maxdepth 3 -type f -exec grep -v '^[[:space:]]*#\|^[[:space:]]*$' {} + | head -30 | cut -c1-170 | sed 's/^/     /'
done
echo "  packages mentioning swap or zram:"; dpkg -l 2>/dev/null | awk '/swap|zram/ {print "    "$2" "$3}' | head -10
SG=""; sudo -n true 2>/dev/null && SG="sudo -n"
echo "  files that mention /var/swap (config dirs, systemd, rpi, init scripts, cron); searched as: ${SG:-pi (some files unreadable!)}"
timeout 40 $N $SG grep -rIn "/var/swap" /etc /usr/lib/systemd /lib/systemd /usr/lib/rpi* /usr/libexec /usr/share/rpi* /var/spool/cron /home/pi/.config /usr/local 2>/dev/null | head -20 | cut -c1-200 | sed 's/^/    /'
echo "    (end of matches; none above means no file under those paths mentions /var/swap)"
echo "  scripts under /usr/bin /usr/sbin that mention /var/swap (names only):"; timeout 40 $N $SG grep -rIl "/var/swap" /usr/bin /usr/sbin 2>/dev/null | head -8 | sed 's/^/    /'
echo "    (end)"
echo "  boot-time hooks: rc.local=$(ls -l /etc/rc.local 2>&1 | head -1)   crontabs: $(${SG:-sudo -n} ls /var/spool/cron/crontabs 2>&1 | tr '\n' ' ')"
echo "  swap-related boot messages from the journal of this boot (units):"; t 20 journalctl -b --no-pager 2>&1 | grep -i "swap" | grep -v "kernel:" | head -8 | cut -c1-200 | sed 's/^/    /'
fi

sec "B. orphaned quiver plots (video dir with output/plot_quiver.jpg and no .mp4): ORPHAN|id|date|plot_bytes|sync_status|db_timestamp"
command -v sqlite3 >/dev/null || { echo "REFUSED: sqlite3 not installed"; return 2; }
[ -r "$DB" ] || { echo "REFUSED: $DB not readable"; return 2; }
rows=$(ro "SELECT id||'|'||ifnull(sync_status,'NULL')||'|'||ifnull(timestamp,'') FROM video;")
echo "  DB rows: $(printf '%s\n' "$rows" | grep -c '|')"
L=$(t 90 $N find "$V" -xdev -type f -printf '%s|%T@|%P\n')
echo "  files listed: $(printf '%s\n' "$L" | grep -c '|')"
[ "$(printf '%s\n' "$L" | grep -c '|')" -gt 0 ] || { echo "  nothing listed; stopping"; return 1; }
{ printf '%s\n' "$rows" | sed 's/^/D|/'; printf '%s\n' "$L" | awk -F'|' '{ n=split($3,a,"/"); if (n>=3) { rest=$3; sub("^[^/]*/[^/]*/","",rest); print "F|" a[1] "|" a[2] "|" $1+0 "|" rest } }'; } | awk -F'|' '
  $1=="D" { ss[$2]=$3; ts[$2]=$4; next }
  $1=="F" { key=$2 "/" $3; if ($5 ~ /\.mp4$/) hv[key]=1; if ($5 == "output/plot_quiver.jpg") { pb[key]=$4; pd[key]=$2; pid[key]=$3 } }
  END { for (k in pb) if (!(k in hv)) { i=pid[k]; st=(i in ss)?ss[i]:"NO_DB_ROW"; print "ORPHAN|" i "|" pd[k] "|" pb[k] "|" st "|" ts[i] } }' | sort -t'|' -k2,2n
echo "  (end of orphan list)"
echo; echo "=== END ==="
}
main </dev/null
