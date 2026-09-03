#!/usr/bin/env bash
# inspect-create-task.sh — is the 500 in create_task, and did the row commit anyway?
#
# TODO-119. inspect-video-post.sh gave us /liveorc/api/views/video.py:
#
#     serializer.is_valid(raise_exception=True)
#     self.perform_create(serializer)                 # row INSERTED here
#     instance = Video.objects.get(id=serializer.data["id"])
#     if instance.is_ready_for_task:
#         instance.create_task(request=request)       # conditional, AFTER the insert
#     return Response(serializer.data, status=201)
#
# TWO CONSEQUENCES, and each needs a different answer.
#
# 1. WHERE the 500 is. create_task runs only when is_ready_for_task is true.
#    A branch that fires for some videos and not others matches a 5.6% failure
#    rate; a fault in the insert path would fail everything. Section 1 reads
#    both members off the model to see what makes the branch true and what
#    inside it can raise.
#
# 2. WHETHER the row survived. perform_create commits before create_task runs,
#    so unless ATOMIC_REQUESTS wraps the request the video is already in the
#    database when the 500 is returned. The station saw a failure and marked
#    the clip FAILED, so the server may hold four videos the station believes
#    it never delivered - and Track 2's re-drive would send them again as
#    duplicates. Sections 2 and 3 settle it.
#
# The previous script's database half failed with 'role "postgres" does not
# exist' because it guessed the credentials. This runs psql inside the db
# container as that container's own POSTGRES_USER, which needs no password and
# echoes none.
#
# READ-ONLY. Reads source and settings, runs SELECT queries. Starts nothing,
# restarts nothing, writes nothing, posts nothing.
#
# USAGE (on the LiveORC host, in ~/code/git/openrivercam after a git pull)
#   ./spring_2026_ID/liveorc_server/liveorc-host/inspect-create-task.sh
set -u
D=docker; docker ps >/dev/null 2>&1 || D="sudo docker"
C=liveorc_webapp
h(){ printf '\n\033[1m== %s ==\033[0m\n' "$*"; }

h "1. the Video model — is_ready_for_task and create_task"
$D exec "$C" sh -c '
  F=$(find /liveorc/api/models -name "*.py" 2>/dev/null | xargs grep -ln "class Video\b\|is_ready_for_task" 2>/dev/null | head -2)
  echo "files: $F"
  for f in $F; do
    echo "########## $f"
    sed -n "1,260p" "$f"
  done' 2>&1 | cut -c1-220 | sed 's/^/  /'

h "2. is the request wrapped in a transaction (would the insert roll back)"
$D exec "$C" sh -c 'grep -n "ATOMIC_REQUESTS\|DATABASES\|ENGINE\|NAME\|USER" /liveorc/LiveORC/settings.py | head -25' \
  2>&1 | sed 's/^/  /'
echo "  (ATOMIC_REQUESTS absent or False = the insert COMMITTED before the 500)"

h "3. the database — did rows land at the four failure moments"
DBU=$($D exec db sh -c 'printf %s "$POSTGRES_USER"' 2>/dev/null)
DBN=$($D exec db sh -c 'printf %s "${POSTGRES_DB:-$POSTGRES_USER}"' 2>/dev/null)
echo "  connecting as: ${DBU:-<unset>} / db: ${DBN:-<unset>}   (no password echoed)"
if [ -z "${DBU:-}" ]; then
  echo "  POSTGRES_USER not set in the db container; run:"
  echo "    docker exec db env | grep -i postgres"
  echo "  and I will adjust."
else
  Q(){ $D exec -i db psql -U "$DBU" -d "$DBN" -At -F '|' -c "$1" 2>&1; }
  echo "  --- the video table's real name ---"
  Q "select table_name from information_schema.tables where table_name like '%video%' order by 1;" | sed 's/^/    /'
  T=$($D exec -i db psql -U "$DBU" -d "$DBN" -At -c "select table_name from information_schema.tables where table_name like '%video%' and table_name not like '%config%' order by length(table_name) limit 1;" 2>/dev/null)
  echo "  --- using table: ${T:-api_video} ---"
  T="${T:-api_video}"
  for S in '2026-09-02 07:31' '2026-09-02 09:31' '2026-09-03 07:31' '2026-09-03 10:31'; do
    echo "    window $S (+/- 3 min):"
    Q "select id, timestamp, status from $T
       where timestamp between timestamp '$S:00' - interval '3 minutes'
                           and timestamp '$S:00' + interval '3 minutes'
       order by id;" | sed 's/^/      /'
  done
  echo "  --- what is_ready_for_task depends on: do these rows have a time series ---"
  Q "select column_name from information_schema.columns where table_name='$T' order by ordinal_position;" \
    | tr '\n' ' ' | fold -w 200 | sed 's/^/    /'
  echo
  echo "  --- most recent 10, for comparison ---"
  Q "select id, timestamp, status from $T order by id desc limit 10;" | sed 's/^/    /'
fi

h "done"
echo "  Read-only. Nothing was changed and nothing was posted."
echo "  A row in a window means the server HAS a clip the station recorded as"
echo "  FAILED, and the re-drive would duplicate it. That changes what Track 2"
echo "  should send, so it is worth being sure before any bulk upload."
