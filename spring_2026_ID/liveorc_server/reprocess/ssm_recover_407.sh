#!/usr/bin/env bash
# ssm_recover_407.sh — TODO-119 phase 01, one short command per stage.
#
# WHY A SCRIPT RATHER THAN A PASTE BLOCK
#   Every host step on this box is typed by hand into Session Manager, which is
#   a browser terminal: long paste sequences get mangled, and a mangled command
#   with --commit in it writes to production. So each stage below is one short
#   word, and the dangerous ones refuse to run until the harmless ones have.
#
# WHAT IT DOES
#   Recovers the 407 site-4 videos sitting in `error` state with their file
#   bytes intact. It is a SCOPED run: --ids overrides the site scan, so the
#   ~2,242 records that already finished are not touched. The full-site Fit 6
#   reprocess is a different, larger operation (TODO-113).
#
# STAGES
#   check    prerequisites only. Changes nothing, writes nothing.
#   smoke    dry-run over 5 videos. Proves the env and the --ids path.
#   dryrun   dry-run over all 407, then the impact report.
#   backup   pg_dump + api_timeseries baseline. Required before commit.
#   commit   the real write. Refuses unless a backup exists from today.
#
# ROLLBACK
#   --repoint and --recover change api_video, not just api_timeseries, so the
#   FULL restore is the correct rollback:
#       ./restore_liveorc_db.sh full liveorc-backups/<ts>
set -euo pipefail
cd "$(dirname "$0")"

IDS_FILE=sukabumi_error_video_ids.txt
EXPECT=407
STAGE=${1:-}

die(){ echo "ERROR: $*" >&2; exit 1; }
note(){ printf '\n== %s ==\n' "$*"; }

[ -f "$IDS_FILE" ] || die "$IDS_FILE missing — run 'git pull' in this checkout first."
IDS=$(tr -d '[:space:]' < "$IDS_FILE")
N=$(awk -F, '{print NF}' <<<"$IDS")

case "$STAGE" in
check)
  note "where this is running"
  echo "  checkout : $(cd ../../.. && pwd)"
  echo "  reprocess: $(pwd)"
  note "target list"
  echo "  ids file : $IDS_FILE"
  echo "  ids found: $N   (expected $EXPECT from the 2026-08-25 mirror)"
  [ "$N" = "$EXPECT" ] || echo "  NOTE: count differs from $EXPECT — the list was refreshed, or is stale."
  note "toolkit present"
  for f in prod_reprocess.sh prod_analytics.sh backup_liveorc_db.sh restore_liveorc_db.sh reprocess_fit6.py; do
    [ -f "$f" ] && echo "  ok   $f" || echo "  MISSING $f"
  done
  note "docker + webapp"
  D=docker; docker ps >/dev/null 2>&1 || D="sudo docker"
  $D ps --format '  {{.Names}}\t{{.Status}}' 2>&1 | grep -i liveorc || echo "  no liveorc container seen"
  note "disk — an SSM session that dies with 'Plugin with name Standard_Stream not found' is this, not a config fault"
  df -h / /var/lib/liveorc-media 2>/dev/null | sed 's/^/  /'
  note "existing backups"
  ls -1dt liveorc-backups/*/ 2>/dev/null | head -3 | sed 's/^/  /' || echo "  none yet"
  note "nothing was changed"
  ;;

smoke)
  note "dry-run over 5 of the $N — proves the environment and the --ids path"
  ./prod_reprocess.sh --ids "$IDS" --limit 5 --recover
  ;;

dryrun)
  note "dry-run over all $N — writes nothing"
  ./prod_reprocess.sh --ids "$IDS" --recover
  note "impact report on the newest log"
  ./prod_analytics.sh
  echo
  echo "Read the Outcomes table before going further. Night and low-light clips"
  echo "that fail optical WL are logged and LEFT INTACT — expect a real share of"
  echo "the $N to stay errored. Reprocessing does not add light."
  ;;

backup)
  note "pg_dump + api_timeseries baseline"
  ./backup_liveorc_db.sh
  ls -1dt liveorc-backups/*/ | head -1 | sed 's/^/  newest: /'
  ;;

commit)
  TODAY=$(date -u +%Y%m%d)
  LATEST=$(ls -1dt liveorc-backups/*/ 2>/dev/null | head -1 || true)
  [ -n "$LATEST" ] || die "no backup found. Run './ssm_recover_407.sh backup' first."
  case "$LATEST" in *"$TODAY"*) : ;; *)
    die "newest backup is $LATEST, not from today ($TODAY). Run 'backup' first." ;;
  esac
  note "backup present: $LATEST"
  echo "About to WRITE to production: $N videos, --commit --repoint --recover."
  echo "Rollback is:  ./restore_liveorc_db.sh full $LATEST"
  read -r -p "Type RECOVER to proceed: " a
  [ "$a" = "RECOVER" ] || die "not confirmed — nothing written."
  DETACH=1 ./prod_reprocess.sh --ids "$IDS" --commit --repoint --recover
  echo
  echo "Backgrounded. prod_reprocess.sh printed the commands to watch progress."
  ;;

*)
  sed -n '2,30p' "$0"
  echo
  echo "usage: ./ssm_recover_407.sh {check|smoke|dryrun|backup|commit}"
  exit 2 ;;
esac
