set -u
H=openrivercam.endlessprojects.info
STATION=$(hostname | sed 's/^orc-//')
STAMP=$(date -u +%Y%m%dT%H%M%SZ)

echo "=== date ==="; date -u
echo "uptime at grab: $(cut -d' ' -f1 /proc/uptime)s"

# ---------------------------------------------------------------------------
# WHAT THIS SEPARATES
#   Two wakes on 2026-09-02 put 12 multi-MB PUTs on the wire and every one
#   failed. The two that pushed a full body were reset at a near-identical
#   ~17 s after the handshake despite payloads differing by 50% (3 MB / 17.51 s,
#   2 MB / 17.04 s). That is time-bounded behaviour, not rate-limited - so
#   dividing payload by window gives an artifact, not a throughput.
#
#   But size and duration were confounded in those runs: the bigger payload was
#   also the longer connection. This separates them.
#
#     row 2 holds SIZE constant and stretches DURATION (--limit-rate)
#     row 4 holds DURATION roughly constant and raises SIZE
#
#   fast 256K ok + slow 256K fails  -> duration-bound (a middlebox idle/age cap)
#   both 256K ok  + 2M fails        -> size-bound (a byte cap somewhere)
#   all fail                        -> neither; the fault is not about the body
#
# ORDERED BY INFORMATION VALUE. The wake is ~85 s and ends on a timer that an
# active SSH does not extend (orc-capture fires `shutdown -h +1` regardless), so
# later rows may be cut off. The discriminator is rows 1-3.
# ---------------------------------------------------------------------------
TOKEN=""
for f in /home/pi/.orc_deploy_*; do
  [ -f "$f" ] || continue
  t=$(grep -E '^UPLOAD_TOKEN=' "$f" 2>/dev/null | tail -1 | cut -d= -f2- | tr -d '"'"'"' ')
  [ -n "$t" ] && TOKEN=$t
done
if [ -z "$TOKEN" ]; then
  echo "=== SKIPPED — no UPLOAD_TOKEN found ==="
  exit 0
fi

echo "=== size/duration ladder on :8443 ==="
printf "  %-3s %-22s %6s %6s %6s %7s %9s %10s %5s %s\n" \
       "#" "label" "tcp" "tls" "ttfb" "total" "sent" "speed_up" "code" "exit"

# label  bytes    limit-rate ("-" for none)  max-time
LADDER="
256Kfast|262144|-|25
256Kslow~17s|262144|15k|32
2Mfast|2000000|-|32
1Mfast|1000000|-|30
64Kfast|65536|-|22
"

n=0
for row in $LADDER; do
  [ -z "$row" ] && continue
  n=$((n+1))
  label=$(echo "$row" | cut -d'|' -f1)
  bytes=$(echo "$row" | cut -d'|' -f2)
  rate=$(echo  "$row" | cut -d'|' -f3)
  maxt=$(echo  "$row" | cut -d'|' -f4)

  PAY=/tmp/orc_ladder.bin
  head -c "$bytes" /dev/urandom > $PAY 2>/dev/null

  RL=""
  [ "$rate" != "-" ] && RL="--limit-rate $rate"

  err=/tmp/orc_ladder.err
  out=$(curl $RL \
          --cacert /etc/orc/sensor-upload-ca.pem \
          -H "Authorization: Bearer $TOKEN" \
          -H 'Expect:' \
          -T "$PAY" \
          --connect-timeout 12 --max-time "$maxt" \
          -s -S -o /tmp/orc_ladder.resp \
          -w '%{time_connect} %{time_appconnect} %{time_starttransfer} %{time_total} %{size_upload} %{speed_upload} %{http_code}' \
          "https://$H:8443/sensors/upload/$STATION/ladder-${label%%~*}-${STAMP}.bin" 2>$err)
  rc=$?
  set -- $out
  if [ $# -ge 7 ]; then
    printf "  %-3s %-22s %6s %6s %6s %7s %9s %10s %5s %s\n" \
           "$n" "$label" "$1" "$2" "$3" "$4" "$5" "$6" "$7" "$rc"
  else
    printf "  %-3s %-22s exit=%s raw=[%s]\n" "$n" "$label" "$rc" "$out"
  fi
  # The service returns {"ok":true,...,"size":N} only on a COMPLETED write.
  # This is the only proof bytes actually landed; curl's size_upload is not.
  echo "        server said: $(head -c 160 /tmp/orc_ladder.resp 2>/dev/null | tr -d '\n')"
  [ -s "$err" ] && echo "        curl stderr: $(head -c 160 $err | tr -d '\n')"
  rm -f $PAY /tmp/orc_ladder.resp /tmp/orc_ladder.err
done

echo
echo "=== modem state at the end ==="
mmcli -m 0 2>/dev/null | grep -iE "state|signal|access tech" | head -5 | sed 's/^/  /'
echo "=== END ==="
