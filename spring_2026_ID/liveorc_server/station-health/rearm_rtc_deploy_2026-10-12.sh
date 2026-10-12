set -u
echo "=== REARM-DAILY-DEPLOY $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
echo "uptime at grab: $(cut -d' ' -f1 /proc/uptime)s"

# 2026-10-12: deploy eb7c7b0 (orc-wp5-rearm measures the re-arm age on the
# Witty Pi RTC, not the stale boot-time system clock). Tom approved.
#
# WRITES, in order:
#   1. git pull --ff-only (clean checkout on main only; stops without eb7c7b0)
#   2. deploy.sh --check first; stops unless the ONLY failures are the two
#      changed files (script + unit). Then --yes --skip-packages (2 files + RTC sync).
#   3. orc-wp5-rearm.service started twice: the 19:00 boot stamped March, so it
#      re-arms (~33 s) and writes /var/lib/orc-wp5-rearm/last-ok; the second
#      must log "not due" in well under a second.

REPO=/home/pi/code/git/openrivercam
PI="$REPO/spring_2026_ID/pi"
export GIT_TERMINAL_PROMPT=0
export GIT_SSH_COMMAND="ssh -o BatchMode=yes -o ConnectTimeout=10"
stamp() { awk '{printf "%.1f", $1}' /proc/uptime; }
stop() { echo "  STOP: $*"; echo "=== END (t=$(stamp)s) ==="; exit 0; }

echo
echo "=== 0. boot re-arm (old script) ==="
cat /var/log/orc/wp5-rearm.last 2>&1 | sed 's/^/  /'

echo
echo "=== 1. git pull ==="
DIRTY=$(git -C "$REPO" status --porcelain --untracked-files=no 2>&1)
BR=$(git -C "$REPO" rev-parse --abbrev-ref HEAD 2>&1)
{ [ -z "$DIRTY" ] && [ "$BR" = main ]; } || stop "branch=$BR dirty=[$DIRTY]"
timeout 90 git -C "$REPO" pull --ff-only 2>&1 | tail -4 | sed 's/^/  /'
echo "  HEAD: $(git -C "$REPO" log -1 --format='%h %s' 2>&1)"
git -C "$REPO" merge-base --is-ancestor eb7c7b0 HEAD 2>/dev/null || stop "eb7c7b0 not present"

echo
echo "=== 2a. deploy.sh --check (t=$(stamp)s) ==="
cd "$PI" || stop "no $PI"
timeout 150 bash ./deploy.sh sukabumi --check --skip-packages </dev/null 2>&1 \
  | sed 's/\x1b\[[0-9;]*m//g' > /tmp/orc-deploy-check-last.txt
F=$(grep '\[FAIL\]' /tmp/orc-deploy-check-last.txt | sort -u)
echo "$F" | sed 's/^/  /'
UNEXPECTED=$(echo "$F" | grep -v -e '/usr/local/bin/orc-wp5-rearm' -e '/etc/systemd/system/orc-wp5-rearm.service' | grep .)
[ -z "$UNEXPECTED" ] || stop "unexpected failures above — not applying"
[ -n "$F" ] || stop "no failures — files already match?"

echo
echo "=== 2b. deploy.sh --yes --skip-packages (t=$(stamp)s) ==="
timeout 150 bash ./deploy.sh sukabumi --yes --skip-packages </dev/null 2>&1 \
  | sed 's/\x1b\[[0-9;]*m//g' > /tmp/orc-deploy-fix-last.txt
echo "  exit: ${PIPESTATUS[0]}"
grep -E '\[FIXD\]|\[FAIL\]|FIXD: ' /tmp/orc-deploy-fix-last.txt | sort -u | sed 's/^/  /'
for f in /usr/local/bin/orc-wp5-rearm /etc/systemd/system/orc-wp5-rearm.service; do
  echo "  $f: $(sudo cmp -s "$f" "$PI/sukabumi$f" && echo matches-repo || echo DIFFERS)"
done

echo
echo "=== 3a. re-arm run 1: stamp from the stale March clock, must re-arm (t=$(stamp)s) ==="
t0=$(date +%s.%N)
sudo -n timeout 160 systemctl start orc-wp5-rearm.service 2>&1 | sed 's/^/  /'
echo "  elapsed: $(awk -v a="$t0" -v b="$(date +%s.%N)" 'BEGIN{printf "%.1f", b-a}')s result: $(systemctl show -p Result --value orc-wp5-rearm.service)"
cat /var/log/orc/wp5-rearm.last 2>&1 | sed 's/^/  /'
echo "  stamp: $(sudo cat /var/lib/orc-wp5-rearm/last-ok 2>&1)"

echo
echo "=== 3b. re-arm run 2: must be 'not due' (t=$(stamp)s) ==="
t0=$(date +%s.%N)
sudo -n timeout 60 systemctl start orc-wp5-rearm.service 2>&1 | sed 's/^/  /'
echo "  elapsed: $(awk -v a="$t0" -v b="$(date +%s.%N)" 'BEGIN{printf "%.1f", b-a}')s result: $(systemctl show -p Result --value orc-wp5-rearm.service)"
cat /var/log/orc/wp5-rearm.last 2>&1 | sed 's/^/  /'
echo "=== END (t=$(stamp)s) ==="
