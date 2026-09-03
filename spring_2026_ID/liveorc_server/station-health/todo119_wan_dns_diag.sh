set -u
H=openrivercam.endlessprojects.info
IP=34.203.227.187
echo "=== date ==="; date -u
echo "uptime at grab: $(cut -d' ' -f1 /proc/uptime)s"

# NOT ARMED BY DEFAULT. Written 2026-09-02 while the outage was live, ready for
# whenever the WAN lead is picked up.
#
# The lead: the station's journal shows DNS on [::1]:53 "server misbehaving",
# tailscaled unable to resolve controlplane, and "network is unreachable" on
# BOTH address families - while mmcli reports LTE attached at 100%. Power and
# capture are excluded (powercapture119s), so delivery is the whole fault.
#
# This separates the two things that look alike from the application's side:
# a resolver that cannot answer, and a route that cannot carry.
#
# READ-ONLY. Queries and route inspection. Changes no config, restarts nothing.

echo "=== A. who is [::1]:53, and is it healthy ==="
echo "  --- resolv.conf as the apps see it ---"
cat /etc/resolv.conf 2>/dev/null | grep -vE "^#|^$" | sed 's/^/    /'
echo "  --- what is listening on :53 ---"
(ss -lunp 2>/dev/null || netstat -lunp 2>/dev/null) | grep -E ":53\b" | sed 's/^/    /'
echo "  --- systemd-resolved status, if that is what it is ---"
resolvectl status 2>/dev/null | head -25 | sed 's/^/    /' || echo "    (resolvectl not present)"

echo
echo "=== B. does resolution work, and by which path ==="
for q in "$H" controlplane.tailscale.com pangolin.openrivercam.com; do
  echo "  --- $q ---"
  echo "    getent ahostsv4: $(getent ahostsv4 $q 2>&1 | awk '{print $1}' | sort -u | tr '\n' ' ')"
  echo "    getent ahostsv6: $(getent ahostsv6 $q 2>&1 | awk '{print $1}' | sort -u | tr '\n' ' ')"
done

echo
echo "=== C. resolver vs route: ask a PUBLIC resolver directly ==="
# If the local resolver fails but 8.8.8.8 answers, the fault is the resolver.
# If neither answers, DNS is a symptom and the route is the fault.
for r in 8.8.8.8 1.1.1.1; do
  if command -v dig >/dev/null 2>&1; then
    echo "  dig @$r $H A: $(timeout 8 dig +short +tries=1 +time=5 @$r $H A 2>&1 | tr '\n' ' ')"
  elif command -v nslookup >/dev/null 2>&1; then
    echo "  nslookup @$r:"; timeout 8 nslookup $H $r 2>&1 | tail -4 | sed 's/^/    /'
  else
    echo "  (no dig or nslookup on the station)"
    break
  fi
done

echo
echo "=== D. the route itself, which needs no DNS at all ==="
echo "  --- default routes ---"
ip -4 route show default 2>/dev/null | sed 's/^/    v4: /'
ip -6 route show default 2>/dev/null | head -3 | sed 's/^/    v6: /'
echo "  --- can we reach the server by IP, no name involved ---"
timeout 12 ping -c 3 -W 3 $IP 2>&1 | tail -3 | sed 's/^/    /'
echo "  --- can we open a TCP socket to :443 by IP ---"
timeout 12 sh -c "echo > /dev/tcp/$IP/443" 2>&1 && echo "    tcp/443 by IP: OPEN" || echo "    tcp/443 by IP: FAILED"
echo "  --- and :8443 ---"
timeout 12 sh -c "echo > /dev/tcp/$IP/8443" 2>&1 && echo "    tcp/8443 by IP: OPEN" || echo "    tcp/8443 by IP: FAILED"

echo
echo "=== E. modem's own view, in more detail than mmcli's one-liner ==="
mmcli -m 0 2>/dev/null | grep -iE "state|signal|access tech|operator|packet|bearer" | sed 's/^/    /'
echo "  --- the bearer's assigned addressing, which is what actually routes ---"
mmcli -m 0 --output-keys 2>/dev/null | grep -iE "bearer" | head -3 | sed 's/^/    /'
mmcli -b 0 2>/dev/null | grep -iE "address|prefix|gateway|dns|mtu|interface" | sed 's/^/    /'
echo "=== END ==="
