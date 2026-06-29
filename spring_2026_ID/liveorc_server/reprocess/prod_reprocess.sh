#!/usr/bin/env bash
# prod_reprocess.sh — run the Fit 6 reprocess against PROD LiveORC.
#
# It runs INSIDE the running webapp container via `docker exec`, so it inherits the
# webapp's real env (prod uses local FileSystemStorage, NOT S3), DB, and media volume.
#
# pyorc 0.9.4 needs an older xarray than the image ships, AND pyorc runs velocimetry in
# a `pyorc` CLI SUBPROCESS (system python) — so a venv pin wouldn't reach it. Instead we
# install the pinned xarray into an ISOLATED dir and put it first on PYTHONPATH, which
# the subprocess inherits. The webapp's installed packages are NOT modified.
#
# Defaults: --site-id 4 --video-config-id 3 (Sukabumi / "Sukabumi IPB"). Anything you
# pass is appended and can override. DRY-RUN unless you pass --commit. Logs are copied
# back to ./reprocess-logs/ on the host.
#
# Examples:
#   ./prod_reprocess.sh --limit 5                        # smoke dry-run (5 videos)
#   ./prod_reprocess.sh --recover                        # full dry-run (all site 4)
#   ./prod_reprocess.sh --commit --repoint --recover     # the real write (prompts first)
#   DETACH=1 ./prod_reprocess.sh --commit --repoint --recover   # long run, in background
#
# Throttle (the box gets sluggish under load): WORKERS parallel videos (default 2),
#   THREADS = number of CPUs the whole job is pinned to via taskset (default 2),
#   NICE cpu priority (default 15). Lower WORKERS/THREADS or raise NICE if still heavy.
# Progress: a PROGRESS line (% done + ETA) prints every 20 videos; per-video results
#   stream to ./reprocess-logs/*.jsonl as they finish, and *.progress holds the latest
#   status (both survive a crash). Foreground also tees console to ./reprocess-logs/*.out.
# Tunables (env): WEBAPP (liveorc_webapp), XARRAY_PIN (2024.9.0), SITE_ID (4), VC_ID (3),
#   WORKERS (2), THREADS (2), NICE (15), DETACH=1 (background), FORCE=1 (skip prompt).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
WEBAPP="${WEBAPP:-liveorc_webapp}"
XARRAY_PIN="${XARRAY_PIN:-2024.9.0}"
SITE_ID="${SITE_ID:-4}"
VC_ID="${VC_ID:-3}"
# Throttle (keep the box responsive): WORKERS parallel videos, each pyorc capped to
# THREADS cpu threads, whole job at low cpu/io priority (NICE). Tune via env.
WORKERS="${WORKERS:-2}"
THREADS="${THREADS:-2}"
NICE="${NICE:-15}"
XPIN_DIR="/tmp/orc-xarray-pin"          # isolated xarray install (shadows via PYTHONPATH)
CLOG="/tmp/orc-reprocess-logs"          # log dir inside the container

DOCKER="docker"
if ! docker ps >/dev/null 2>&1; then DOCKER="sudo docker"; fi

[ -f "$SCRIPT_DIR/reprocess_fit6.py" ] || { echo "reprocess_fit6.py not next to this script"; exit 1; }
$DOCKER inspect "$WEBAPP" >/dev/null 2>&1 || { echo "webapp container '$WEBAPP' not found ($DOCKER ps)"; exit 1; }

# Confirm before any write.
if printf '%s ' "$@" | grep -qw -- --commit && [ "${FORCE:-0}" != "1" ]; then
  echo "About to run with --commit (WRITES to prod DB) inside container '$WEBAPP'."
  echo "Make sure you ran backup_liveorc_db.sh first."
  read -r -p "Type COMMIT to proceed: " ans
  [ "$ans" = "COMMIT" ] || { echo "aborted."; exit 1; }
fi

# Stage the (latest) reprocessor into the container.
$DOCKER cp "$SCRIPT_DIR/reprocess_fit6.py" "$WEBAPP:/tmp/reprocess_fit6.py"

# Build the in-container command: install the pinned xarray into an isolated dir
# (--no-deps so numpy/pandas stay the system ones), prepend it to PYTHONPATH so both
# this process AND the pyorc CLI subprocess pick it up, then run the reprocessor.
CPUMAX=$(( THREADS > 0 ? THREADS - 1 : 0 ))
# Throttle by CAPPING cpus with taskset (+ low priority via nice). We deliberately do
# NOT set *_NUM_THREADS env — limiting NUMBA_NUM_THREADS while pyorc runs its internal
# multiprocessing caused SIGSEGV. taskset bounds total CPU without touching numba.
INNER='set -e
mkdir -p "'"$XPIN_DIR"'" "'"$CLOG"'"
if [ ! -d "'"$XPIN_DIR"'/xarray" ]; then pip install -q --target "'"$XPIN_DIR"'" --no-deps "xarray=='"$XARRAY_PIN"'"; fi
export PYTHONPATH="'"$XPIN_DIR"'${PYTHONPATH:+:$PYTHONPATH}"
RUN="nice -n '"$NICE"'"
command -v taskset >/dev/null 2>&1 && RUN="taskset -c 0-'"$CPUMAX"' $RUN"
exec $RUN python /tmp/reprocess_fit6.py "$@" --log-dir "'"$CLOG"'"'

# base args (WORKERS default; user args after can override). --log-dir is forced in INNER.
BASEARGS=(--site-id "$SITE_ID" --video-config-id "$VC_ID" --workers "$WORKERS")
echo "==> exec in $WEBAPP | xarray==$XARRAY_PIN (PYTHONPATH) | workers=$WORKERS cpus=$THREADS(0-$CPUMAX) nice=$NICE"
echo "    args: ${BASEARGS[*]} $*"

if [ "${DETACH:-0}" = "1" ]; then
  $DOCKER exec -d "$WEBAPP" bash -lc "$INNER" _ "${BASEARGS[@]}" "$@"
  echo "==> detached (first .progress appears after video #1 completes, ~15-30s)."
  echo "    Is it running:  $DOCKER exec $WEBAPP sh -c 'ps -eo pid,etime,cmd | grep [r]eprocess_fit6'"
  echo "    Live progress:  $DOCKER exec $WEBAPP sh -c 'cat $CLOG/*.progress 2>/dev/null || echo not-yet'"
  echo "    Tail results:   $DOCKER exec $WEBAPP sh -c 'tail -f $CLOG/*.jsonl'"
  echo "    When done, pull logs: $DOCKER cp $WEBAPP:$CLOG/. $SCRIPT_DIR/reprocess-logs/"
  exit 0
fi

# Foreground: mirror stdout to a host file live (so you have it even if it crashes).
mkdir -p "$SCRIPT_DIR/reprocess-logs"
HOST_OUT="$SCRIPT_DIR/reprocess-logs/run_$(date +%Y%m%d-%H%M%S).out"
set +e
$DOCKER exec "$WEBAPP" bash -lc "$INNER" _ "${BASEARGS[@]}" "$@" 2>&1 | tee "$HOST_OUT"
rc=${PIPESTATUS[0]}
set -e

# Pull the JSONL results + .progress files back to the host regardless of exit code.
$DOCKER cp "$WEBAPP:$CLOG/." "$SCRIPT_DIR/reprocess-logs/" 2>/dev/null || true
echo "==> console log: $HOST_OUT"
echo "==> results/progress in $SCRIPT_DIR/reprocess-logs/   (exit $rc)"
exit $rc
