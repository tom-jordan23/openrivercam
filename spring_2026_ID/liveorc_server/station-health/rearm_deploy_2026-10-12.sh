set -u
echo "=== REARM-DEPLOY $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
echo "uptime at grab: $(cut -d' ' -f1 /proc/uptime)s"

# 2026-10-12, test 3: deploy orc-wp5-rearm and orc-wake-ceiling (9b2e78f, with
# the 32cb6b0 timeout-message fix) and run the re-arm once by hand in the same
# wake. Tom approved.
#
# WRITES, in order:
#   1. git pull --ff-only (clean checkout on main only)
#   2. deploy.sh sukabumi --yes --skip-packages: the 9 FAILs from the 15:00 UTC
#      --check (motd file, 6 new files, 2 enables) plus the RTC sync every fix
#      pass does. Stops before deploy.sh if the pull did not land 32cb6b0.
#   3. systemctl start orc-wp5-rearm.service: one activation of prod_30.wpi.
# The wake-ceiling TIMER is never started here (it would fire at once on a Pi
# up longer than 12 min); it is checked to be enabled and inactive.

REPO=/home/pi/code/git/openrivercam
PI="$REPO/spring_2026_ID/pi"
export GIT_TERMINAL_PROMPT=0
export GIT_SSH_COMMAND="ssh -o BatchMode=yes -o ConnectTimeout=10"
hdr() { printf '14\n' | sudo -n timeout 20 wp5 2>&1 | sed 's/\x1b\[[0-9;]*m//g' \
          | grep -E 'Version|Schedule next|schedule script' | sed 's/^/  /'; }
stamp() { awk '{printf "%.1f", $1}' /proc/uptime; }

echo
echo "=== 0. Witty Pi header before ==="
hdr

echo
echo "=== 1. git pull ==="
DIRTY=$(git -C "$REPO" status --porcelain --untracked-files=no 2>&1)
BR=$(git -C "$REPO" rev-parse --abbrev-ref HEAD 2>&1)
if [ -n "$DIRTY" ] || [ "$BR" != main ]; then
  echo "  STOP: branch=$BR dirty=[$DIRTY]"; echo "=== END ==="; exit 0
fi
timeout 90 git -C "$REPO" pull --ff-only 2>&1 | tail -4 | sed 's/^/  /'
echo "  HEAD: $(git -C "$REPO" log -1 --format='%h %s' 2>&1)"
if ! git -C "$REPO" merge-base --is-ancestor 32cb6b0 HEAD 2>/dev/null; then
  echo "  STOP: 32cb6b0 not present — not deploying"; echo "=== END ==="; exit 0
fi

echo
echo "=== 2. deploy.sh sukabumi --yes --skip-packages (t=$(stamp)s) ==="
cd "$PI" || exit 0
timeout 150 bash ./deploy.sh sukabumi --yes --skip-packages </dev/null 2>&1 \
  | sed 's/\x1b\[[0-9;]*m//g' > /tmp/orc-deploy-fix-last.txt
echo "  exit: ${PIPESTATUS[0]}  (t=$(stamp)s)"
grep -E 'FIXD|FAIL|PASS: ' /tmp/orc-deploy-fix-last.txt | sed 's/^/  /' | head -40
echo "  --- installed? ---"
for f in /usr/local/bin/orc-wp5-rearm /usr/local/bin/orc-wake-ceiling /etc/orc-wp5-rearm.conf; do
  echo "  $f: $(sudo cmp -s "$f" "$PI/sukabumi$f" && echo matches-repo || echo DIFFERS/MISSING)"
done
for u in orc-wp5-rearm.service orc-wake-ceiling.timer; do
  echo "  $u: enabled=$(systemctl is-enabled $u 2>&1) active=$(systemctl is-active $u 2>&1)"
done

if [ "$(systemctl is-enabled orc-wp5-rearm.service 2>&1)" != enabled ]; then
  echo "  STOP: re-arm unit not enabled — not running it"; echo "=== END ==="; exit 0
fi

echo
echo "=== 3. one manual re-arm (t=$(stamp)s) ==="
t0=$(date +%s.%N)
sudo -n timeout 160 systemctl start orc-wp5-rearm.service 2>&1 | sed 's/^/  /'
echo "  start exit: ${PIPESTATUS[0]}  elapsed: $(awk -v a="$t0" -v b="$(date +%s.%N)" 'BEGIN{printf "%.1f", b-a}')s  (t=$(stamp)s)"
echo "  result: $(systemctl show -p Result --value orc-wp5-rearm.service)"
echo "  --- /var/log/orc/wp5-rearm.last ---"
sudo cat /var/log/orc/wp5-rearm.last 2>&1 | sed 's/^/  /'

echo
echo "=== 4. Witty Pi header after ==="
hdr
echo "  wake-ceiling timer (must be inactive): $(systemctl is-active orc-wake-ceiling.timer 2>&1)"
echo "=== END (t=$(stamp)s) ==="
