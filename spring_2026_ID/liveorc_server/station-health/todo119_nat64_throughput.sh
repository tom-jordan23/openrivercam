set -u
H=openrivercam.endlessprojects.info
STATION=$(hostname | sed 's/^orc-//')
PAYLOAD=/tmp/orc_linkprobe.bin
BYTES=2000000          # 2 MB: ~12 s at the rate wake 1 measured, so it fits the wake
MAXT=35                # ceiling; wake 1 needed 26.7 s for 3 MB, so 30 was too tight
STAMP=$(date -u +%Y%m%dT%H%M%SZ)

echo "=== date ==="; date -u
echo "uptime at grab: $(cut -d' ' -f1 /proc/uptime)s"

# ---------------------------------------------------------------------------
# Phase 0 — path facts. Cheap, and it decides whether phase 1 means anything:
# if -4 cannot resolve, the "forced IPv4" arm is not actually a second path.
# ---------------------------------------------------------------------------
echo "=== P0: which path is the default, and is there a second one ==="
echo "  --- ip route get (default path) ---"
ip route get "$(getent hosts $H | awk '{print $1; exit}')" 2>&1 | head -2 | sed 's/^/  /'
echo "  --- A records (the forced-IPv4 arm depends on these existing) ---"
getent ahostsv4 $H 2>&1 | awk '{print "  v4: "$1}' | sort -u
echo "  --- AAAA records (synthesized by DNS64 if 64:ff9b::/96) ---"
getent ahostsv6 $H 2>&1 | awk '{print "  v6: "$1}' | sort -u

# Does forcing IPv4 actually bypass the translator, or only re-enter it?
# If wwan0 carries no global IPv4, the station is IPv6-only and any IPv4 the
# host emits is going through a local CLAT to the SAME NAT64 translator
# (464XLAT). In that case the two arms are not two paths and the reset
# comparison below means nothing. This decides whether P1 is interpretable.
echo "  --- is there a native IPv4 path at all, or is -4 going via CLAT ---"
echo "    wwan0 v4: $(ip -4 -o addr show wwan0 2>/dev/null | awk '{print $4}' | tr '\n' ' ')"
echo "    wwan0 v6: $(ip -6 -o addr show wwan0 2>/dev/null | awk '{print $4}' | grep -v '^fe80' | tr '\n' ' ')"
echo "    interfaces that look like a CLAT:"
ip -o link show 2>/dev/null | awk '{print $2}' | grep -iE "clat|xlat|464" | sed 's/^/      /' || true
echo "    route to the server's IPv4 literal (which interface carries it):"
ip route get 34.203.227.187 2>&1 | head -2 | sed 's/^/      /'

# ---------------------------------------------------------------------------
# Phase 1 — items B and C in one measurement.
#
# Each transfer is a real authenticated PUT to our own sensor-upload service,
# which streams the body to disk and returns the byte count it received. That
# gives an independent confirmation the bytes landed, which curl's own
# size_upload cannot provide on its own.
#
# B: alternate default (NAT64) and forced IPv4 so link drift biases neither
#    arm, and count how each transfer ends. Exit 56/55/52 are the connection
#    being torn down; 28 is a timeout; 35 is a TLS failure.
# C: time_appconnect is the handshake, speed_upload is the throughput. Those
#    two numbers are what the 7 s handshake and the 1.74 MB/s figure have to
#    be reconciled against, and one line here carries both.
#
# NOTE this writes to /var/orc/sensors/<station>/ on the server. sensor-ingest
# polls *.csv only, so a .bin is inert — but the files persist and want
# cleaning up afterwards.
# ---------------------------------------------------------------------------
TOKEN=""
for f in /home/pi/.orc_deploy_*; do
  [ -f "$f" ] || continue
  t=$(grep -E '^UPLOAD_TOKEN=' "$f" 2>/dev/null | tail -1 | cut -d= -f2- | tr -d '"'"'"' ')
  [ -n "$t" ] && TOKEN=$t
done
if [ -z "$TOKEN" ]; then
  echo "=== P1: SKIPPED — no UPLOAD_TOKEN found in /home/pi/.orc_deploy_* ==="
else
  echo "=== P1: 1 forced-IPv4 confirmation, then 5 x 2 MB on the default path ==="
  echo "  station=$STATION  payload=${BYTES}B  max-time=${MAXT}s  cacert=/etc/orc/sensor-upload-ca.pem"
  dd if=/dev/urandom of=$PAYLOAD bs=100000 count=$((BYTES/100000)) 2>/dev/null
  echo "  payload on disk: $(stat -c %s $PAYLOAD) bytes"
  echo
  printf "  %-4s %-8s %-22s %6s %6s %6s %6s %7s %9s %10s %5s %s\n" \
         run arm remote_ip dns tcp tls ttfb total sent speed_up code exit
  i=0
  for arm in ipv4 default default default default default; do
    i=$((i+1))
    case $arm in
      default) FLAG=""   ; CT=15 ;;
      ipv4)    FLAG="-4" ; CT=8  ;;   # 3/3 timed out at 15 s in wake 1; 8 is enough to confirm
    esac
      NAME="linkprobe-${arm}-${STAMP}.bin"   # same name each run: 2 files of litter, not 6
      err=/tmp/orc_linkprobe.err
      out=$(curl $FLAG \
              --cacert /etc/orc/sensor-upload-ca.pem \
              -H "Authorization: Bearer $TOKEN" \
              -H 'Expect:' \
              -T "$PAYLOAD" \
              --connect-timeout $CT --max-time $MAXT \
              -s -S -o /tmp/orc_linkprobe.resp \
              -w '%{time_namelookup} %{time_connect} %{time_appconnect} %{time_starttransfer} %{time_total} %{size_upload} %{speed_upload} %{http_code} %{remote_ip}' \
              "https://$H:8443/sensors/upload/$STATION/$NAME" 2>$err)
      rc=$?
      set -- $out
      if [ $# -ge 8 ]; then
        printf "  %-4s %-8s %-22s %6s %6s %6s %6s %7s %9s %10s %5s %s\n" \
               "$i" "$arm" "${9:-(none)}" "$1" "$2" "$3" "$4" "$5" "$6" "$7" "$8" "$rc"
      else
        printf "  %-4s %-8s exit=%s raw=[%s]\n" "$i" "$arm" "$rc" "$out"
      fi
      # The server echoes the byte count it actually received. If this
      # disagrees with size_upload, the transfer died between the two.
      echo "        server said: $(head -c 200 /tmp/orc_linkprobe.resp 2>/dev/null | tr -d '\n')"
    [ -s "$err" ] && echo "        curl stderr: $(head -c 200 $err | tr -d '\n')"
  done
  rm -f $PAYLOAD /tmp/orc_linkprobe.resp /tmp/orc_linkprobe.err
fi

echo
echo "=== P2: modem state at the end of the run (did the link change under us) ==="
mmcli -m 0 2>/dev/null | grep -iE "state|signal|access tech|operator|quality" | head -8 | sed 's/^/  /'
echo "=== END ==="
