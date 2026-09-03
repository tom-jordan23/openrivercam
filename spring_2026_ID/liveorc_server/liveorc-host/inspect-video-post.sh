#!/usr/bin/env bash
# inspect-video-post.sh — what can make POST /api/video/ raise a 500?
#
# TODO-119. Established so far, 2026-09-03:
#   - POST /api/video/ 500s on 5.6% of uploads (68 x 201, 4 x 500 over 14 days)
#   - the traceback went NOWHERE and cannot be recovered. DEBUG=False with no
#     LOGGING block means Django's default console handler is gated behind
#     require_debug_true, and mail_admins needs ADMINS + SMTP, neither set.
#
# So instead of hunting a traceback that does not exist, this reads the code
# that ran and the rows it left behind. Zero production change: no restart, no
# settings edit, no DEBUG=True on an internet-facing service.
#
# THE FOUR FAILURES
#   02/Sep 07:31:52   02/Sep 09:31:52   03/Sep 07:31:58   03/Sep 10:31:56
#
# WHAT WE ARE LOOKING FOR
# The station posts the video only AFTER its time series has synced
# (orc-os video.py:388), so by the time POST /api/video/ runs the payload
# carries remote ids for time_series and video_config. The most common way a
# DRF create() 500s rather than returning a 400 is an IntegrityError at the
# database - a duplicate unique key, or a null in a NOT NULL column - because
# that escapes serializer validation and is not caught. Section 4 checks for
# exactly that shape by looking at the constraints and at whether a partial row
# was left behind.
#
# READ-ONLY. Reads source files, environment variables and runs SELECT queries.
# Starts nothing, restarts nothing, writes nothing, posts nothing.
#
# USAGE (on the LiveORC host, in ~/code/git/openrivercam after a git pull)
#   ./spring_2026_ID/liveorc_server/liveorc-host/inspect-video-post.sh
set -u
D=docker; docker ps >/dev/null 2>&1 || D="sudo docker"
C=liveorc_webapp
h(){ printf '\n\033[1m== %s ==\033[0m\n' "$*"; }

h "1. where the video API lives (LiveORC's own code, not site-packages)"
$D exec "$C" sh -c '
  find /liveorc -name "*.py" 2>/dev/null | grep -viE "site-packages|/migrations/|/tests?/" \
  | xargs grep -ln "class .*Video.*\(ViewSet\|APIView\|Serializer\)" 2>/dev/null | head -10' \
  2>&1 | sed 's/^/  /'

h "2. the video viewset and serializer, as they actually run"
$D exec "$C" sh -c '
  for f in $(find /liveorc -name "*.py" 2>/dev/null | grep -viE "site-packages|/migrations/|/tests?/" \
             | xargs grep -ln "class .*Video.*\(ViewSet\|APIView\|Serializer\)" 2>/dev/null | head -4); do
    echo "########## $f"
    sed -n "1,220p" "$f"
  done' 2>&1 | cut -c1-220 | sed 's/^/  /'

h "3. the video model — unique constraints and NOT NULLs are the 500 candidates"
$D exec "$C" sh -c '
  for f in $(find /liveorc -name "models.py" 2>/dev/null | grep -viE "site-packages" | head -4); do
    echo "########## $f"
    grep -n "class \|unique\|null=False\|blank=\|ForeignKey\|OneToOne\|UniqueConstraint" "$f" | head -60
  done' 2>&1 | cut -c1-220 | sed 's/^/  /'

h "4. did a row land anyway, at each of the four failure moments"
# DB credentials come from the app container's own environment; nothing is
# echoed that would print a password.
eval "$($D exec "$C" sh -c 'env | grep -E "^(LORC_)?(DB|POSTGRES|SQL)_" ' 2>/dev/null | sed 's/^/export /')" 2>/dev/null || true
DBC=$($D ps --format '{{.Names}}' | grep -E '^db$' | head -1)
echo "  db container: ${DBC:-none}   (querying as the app's configured user)"
if [ -n "${DBC:-}" ]; then
  PSQL="$D exec -i $DBC psql -U ${POSTGRES_USER:-${DB_USER:-postgres}} -d ${POSTGRES_DB:-${DB_NAME:-liveorc}} -At -F '|'"
  echo "  --- videos on site 4 created near each 500 (UTC) ---"
  for T in '2026-09-02 07:31' '2026-09-02 09:31' '2026-09-03 07:31' '2026-09-03 10:31'; do
    echo "    window $T:"
    $PSQL -c "select id, timestamp, created_at from video_video
              where created_at between timestamp '$T:00' - interval '3 minutes'
                                   and timestamp '$T:00' + interval '3 minutes'
              order by id;" 2>&1 | sed 's/^/      /'
  done
  echo "  --- table constraints, where an IntegrityError would come from ---"
  $PSQL -c "select conname, pg_get_constraintdef(oid) from pg_constraint
            where conrelid = 'video_video'::regclass order by contype;" 2>&1 | sed 's/^/    /'
  echo "  --- most recent 8 videos, for comparison with the failures ---"
  $PSQL -c "select id, timestamp, created_at from video_video order by id desc limit 8;" 2>&1 | sed 's/^/    /'
else
  echo "  no 'db' container matched; skipping the database half"
fi

h "done"
echo "  Read-only. Nothing was changed and nothing was posted."
echo "  A row present in section 4 means the 500 happened AFTER the insert,"
echo "  which points at serialization of the response. No row means it failed"
echo "  during the insert, which points at a constraint - and section 3 says"
echo "  which one."
