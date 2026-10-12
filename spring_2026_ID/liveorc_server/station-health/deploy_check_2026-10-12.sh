set -u
echo "=== DEPLOY-CHECK $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
echo "uptime at grab: $(cut -d' ' -f1 /proc/uptime)s"

# 2026-10-12: get 9b2e78f (orc-wp5-rearm, orc-wake-ceiling) onto the station's
# checkout, then list what deploy.sh would change. Tom approved the git pull.
#
# WRITES: only the git pull, and only if the checkout is clean, on main, and the
# pull is a fast-forward. A dirty or diverged checkout is reported, not touched.
# deploy.sh runs with --check --skip-packages: every fix in it is guarded by
# FIXING=1, which --check never sets; it writes only its report under /tmp.

export GIT_TERMINAL_PROMPT=0
export GIT_SSH_COMMAND="ssh -o BatchMode=yes -o ConnectTimeout=10"

echo
echo "=== A. locate the checkout ==="
# The 14:30 run used -maxdepth 5, one short of /home/pi/code/git/openrivercam/
# spring_2026_ID/pi/deploy.sh (depth 6), and reported no checkout. Check Tom's
# path first, then search deeper.
DEPLOY=$( { ls -d /home/pi/code/git/openrivercam/spring_2026_ID/pi/deploy.sh 2>/dev/null;
            find /home/pi /opt /srv -maxdepth 8 -path '*spring_2026_ID/pi/deploy.sh' 2>/dev/null; } | awk '!seen[$0]++' | head -5)
echo "$DEPLOY" | sed 's/^/  /'
DEPLOY=$(echo "$DEPLOY" | head -1)
[ -n "$DEPLOY" ] || { echo "  no checkout found — stopping"; echo "=== END ==="; exit 0; }
REPO=$(git -C "$(dirname "$DEPLOY")" rev-parse --show-toplevel 2>&1)
echo "  repo: $REPO"

echo
echo "=== B. checkout state before ==="
git -C "$REPO" remote -v 2>&1 | head -2 | sed 's/^/  /'
echo "  branch: $(git -C "$REPO" rev-parse --abbrev-ref HEAD 2>&1)"
echo "  HEAD:   $(git -C "$REPO" log -1 --format='%h %ad %s' --date=short 2>&1)"
DIRTY=$(git -C "$REPO" status --porcelain --untracked-files=no 2>&1)
echo "  tracked changes: $( [ -z "$DIRTY" ] && echo none || echo "$DIRTY" | wc -l )"
echo "$DIRTY" | head -20 | sed 's/^/    /'

echo
echo "=== C. git pull --ff-only ==="
BR=$(git -C "$REPO" rev-parse --abbrev-ref HEAD 2>/dev/null)
if [ -n "$DIRTY" ]; then
  echo "  SKIPPED: checkout has tracked changes"
elif [ "$BR" != "main" ]; then
  echo "  SKIPPED: on branch '$BR', not main"
else
  timeout 90 git -C "$REPO" pull --ff-only 2>&1 | tail -15 | sed 's/^/  /'
  echo "  exit: ${PIPESTATUS[0]}"
fi
echo "  HEAD after: $(git -C "$REPO" log -1 --format='%h %ad %s' --date=short 2>&1)"
echo "  9b2e78f present: $(git -C "$REPO" merge-base --is-ancestor 9b2e78f HEAD 2>/dev/null && echo yes || echo no)"

echo
echo "=== D. deploy.sh sukabumi --check --skip-packages (FAIL/WARN lines and summary) ==="
cd "$(dirname "$DEPLOY")" || exit 0
timeout 150 bash ./deploy.sh sukabumi --check --skip-packages </dev/null 2>&1 \
  | sed 's/\x1b\[[0-9;]*m//g' > /tmp/orc-deploy-check-last.txt
echo "  exit: ${PIPESTATUS[0]}"
grep -nE 'FAIL|WARN|PASS: |^ *[0-9]+\. |Report:' /tmp/orc-deploy-check-last.txt | sed 's/^/  /'
echo "  --- PASS count: $(grep -c 'PASS' /tmp/orc-deploy-check-last.txt) ---"
echo "  --- last 20 lines ---"
tail -20 /tmp/orc-deploy-check-last.txt | sed 's/^/  /'
echo "=== END ==="
