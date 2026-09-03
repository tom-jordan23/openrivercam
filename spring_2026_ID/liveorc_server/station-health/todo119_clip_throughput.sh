set -u
H=openrivercam.endlessprojects.info
STATION=$(hostname | sed 's/^orc-//')
PAYLOAD=/tmp/orc_clipprobe.bin
BYTES=9200000          # one mean clip: 10.69 GB / 1,190 files = 8.98 MB, call it 9.2
STAMP=$(date -u +%Y%m%dT%H%M%SZ)

echo "=== date ==="; date -u
echo "uptime at grab: $(cut -d' ' -f1 /proc/uptime)s"

# THROUGHPUT, measured at clip size on a healthy link.
#
# This is TODO-119 item C, still unanswered. Three earlier attempts all landed
# inside the 2026-09-02 upload outage and measured nothing: 17 transfers, zero
# completions, and only 16,128 of 3,000,000 bytes ever reached the server.
# Delivery recovered ~2026-09-03 01:30 UTC, so this is the first chance to get
# a real number.
#
# It uses OUR sensor-upload service with the station's existing token. No
# database edit, no ORC-OS credentials, no change to any video record - which
# is why it is the cheapest way to get the number the trickle plan is blocked
# on. What it does NOT answer is whether ORC-OS's own sync completes inside a
# wake; that is a separate question and needs the re-drive path.
#
# The service streams the body to disk and returns the byte count it received,
# so a completed transfer is proved by the SERVER, not by curl's size_upload -
# which was wrong by a factor of 186 during the outage.

TOKEN=""
for f in /home/pi/.orc_deploy_*; do
  [ -f "$f" ] || continue
  t=$(grep -E '^UPLOAD_TOKEN=' "$f" 2>/dev/null | tail -1 | cut -d= -f2- | tr -d '"'"'"' ')
  [ -n "$t" ] && TOKEN=$t
done
if [ -z "$TOKEN" ]; then echo "=== SKIPPED - no UPLOAD_TOKEN ==="; exit 0; fi

dd if=/dev/urandom of=$PAYLOAD bs=100000 count=$((BYTES/100000)) 2>/dev/null
echo "payload: $(stat -c %s $PAYLOAD) bytes (one mean clip)"
echo

# ONE transfer, ceiling 60 s. The wake gives ~80 s of script time and ends on a
# timer an SSH session does not extend, so a longer ceiling would leave curl
# still running at shutdown and we would lose the timing line altogether -
# the one thing this grab exists to produce. A timeout at 60 s is not a failed
# measurement either: it says a clip cannot complete inside a wake, which is
# exactly what the trickle plan needs to know.
printf "  %-3s %6s %6s %7s %10s %10s %5s %s\n" "#" "tcp" "tls" "total" "sent" "speed_up" "code" "exit"
for i in 1; do
  err=/tmp/orc_clipprobe.err
  out=$(curl --cacert /etc/orc/sensor-upload-ca.pem \
          -H "Authorization: Bearer $TOKEN" \
          -H 'Expect:' \
          -T "$PAYLOAD" \
          --connect-timeout 15 --max-time 60 \
          -s -S -o /tmp/orc_clipprobe.resp \
          -w '%{time_connect} %{time_appconnect} %{time_total} %{size_upload} %{speed_upload} %{http_code}' \
          "https://$H:8443/sensors/upload/$STATION/clipprobe-${STAMP}.bin" 2>$err)
  rc=$?
  set -- $out
  if [ $# -ge 6 ]; then
    printf "  %-3s %6s %6s %7s %10s %10s %5s %s\n" "$i" "$1" "$2" "$3" "$4" "$5" "$6" "$rc"
  else
    printf "  %-3s exit=%s raw=[%s]\n" "$i" "$rc" "$out"
  fi
  # The ONLY proof bytes landed. {"ok":true,...,"size":9200000} means complete.
  echo "        server said: $(head -c 200 /tmp/orc_clipprobe.resp 2>/dev/null | tr -d '\n')"
  [ -s "$err" ] && echo "        curl stderr: $(head -c 160 $err | tr -d '\n')"
done
rm -f $PAYLOAD /tmp/orc_clipprobe.resp /tmp/orc_clipprobe.err

echo
echo "=== how much of the wake did that consume ==="
echo "  uptime now: $(cut -d' ' -f1 /proc/uptime)s   (the wake is ~116 s end to end,"
echo "   of which the sync task only gets ~21 s after its 60 s delay)"
mmcli -m 0 2>/dev/null | grep -iE "state|signal|access tech" | head -3 | sed 's/^/  /'
echo "=== END ==="
