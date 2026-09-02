set -u
H=openrivercam.endlessprojects.info
echo "=== date ==="; date -u
echo "uptime at grab: $(cut -d' ' -f1 /proc/uptime)s"

echo "=== P1: interface MTU vs the REAL path MTU ==="
# A path-MTU blackhole fits the evidence: the handshake completes, then the
# first full-size data packet vanishes and the connection stalls or resets.
# It would NOT explain the 75 ConnectionResets, so this can support the theory
# but cannot carry it alone.
ip -o link show 2>/dev/null | awk '{print "  "$2" mtu="$5}' | grep -vE "lo:|docker|veth" | head -5
echo "  --- route MTU to the server ---"
ip route get $(getent hosts $H | awk '{print $1; exit}') 2>&1 | head -2 | sed 's/^/  /'
echo "  --- largest payload that survives DF, binary search 1200..1500 ---"
lo=1200; hi=1500; best=0
while [ $lo -le $hi ]; do
  mid=$(( (lo+hi)/2 ))
  if ping -c1 -W2 -M do -s $mid "$H" >/dev/null 2>&1; then best=$mid; lo=$((mid+1)); else hi=$((mid-1)); fi
done
if [ "$best" -gt 0 ]; then
  echo "  largest ICMP payload passing DF: $best  => path MTU $((best+28))"
else
  echo "  no DF-set ping of any size got through (ICMP may simply be filtered — not conclusive)"
fi

echo "=== P2: timed TLS handshake to :443 — the port that fails ==="
for i in 1 2 3; do
  s=$(date +%s.%N)
  out=$(timeout 20 openssl s_client -connect $H:443 -servername $H </dev/null 2>&1)
  e=$(date +%s.%N)
  code=$(printf '%s' "$out" | grep -oE "Verify return code: [0-9]+" | head -1)
  proto=$(printf '%s' "$out" | grep -oE "Protocol *: *TLSv[0-9.]+" | head -1)
  echo "  attempt $i: $(awk -v a=$s -v b=$e 'BEGIN{printf "%.2fs", b-a}')  ${proto:-no-proto}  ${code:-no-code}"
done

echo "=== P3: the same to :8443 — the port that has never had this problem ==="
# Same host, same address, same SIM. The only difference is the port and the
# client. If :443 stalls and :8443 does not, that is the sharpest discriminator
# available and points at per-flow treatment rather than the path.
for i in 1 2 3; do
  s=$(date +%s.%N)
  out=$(timeout 20 openssl s_client -connect $H:8443 -servername $H </dev/null 2>&1)
  e=$(date +%s.%N)
  proto=$(printf '%s' "$out" | grep -oE "Protocol *: *TLSv[0-9.]+" | head -1)
  echo "  attempt $i: $(awk -v a=$s -v b=$e 'BEGIN{printf "%.2fs", b-a}')  ${proto:-no-proto}"
done

echo "=== P4: does a large upload survive at all, and how fast ==="
# ~1 MB, about a ninth of a clip. Enough to see a stall; small enough not to
# matter on the SIM.
dd if=/dev/zero of=/tmp/orc_probe.bin bs=1024 count=1024 2>/dev/null
s=$(date +%s.%N)
code=$(timeout 60 curl -k -s -o /dev/null -w '%{http_code} %{size_upload} %{speed_upload}' \
       -X POST --data-binary @/tmp/orc_probe.bin https://$H/api/video/ 2>&1)
e=$(date +%s.%N)
echo "  1 MB POST to :443 -> $code  in $(awk -v a=$s -v b=$e 'BEGIN{printf "%.1fs", b-a}')"
echo "  (401/403 is fine - it proves the BYTES arrived. A stall or 000 does not.)"
rm -f /tmp/orc_probe.bin

echo "=== P5: what the modem thinks the link is ==="
mmcli -m 0 2>/dev/null | grep -iE "state|signal|access tech|operator|quality" | head -8 | sed 's/^/  /'
echo "=== END ==="
