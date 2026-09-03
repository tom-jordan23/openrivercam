#!/usr/bin/env bash
# find-500-traceback.sh — where did LiveORC's 500 traceback go?
#
# TODO-119. Established 2026-09-03 by inspect-500s.sh:
#
#   POST /api/video/ over 14 days:  68 x 201,  4 x 500   (5.6% fail)
#     02/Sep 07:31:52   02/Sep 09:31:52   03/Sep 07:31:58   03/Sep 10:31:56
#
# Flat at two a day across both days, so it is a property of the upload rather
# than an incident with a start and an end. At that rate the 1,190-clip
# re-drive meets it about 66 times, having spent the metered bytes each time.
#
# But `docker logs liveorc_webapp` carries ONLY the access line for each 500 -
# no traceback, no exception class. Django with DEBUG=False returns the
# 145-byte error page and, with no LOGGING config, routes django.request
# errors to mail_admins rather than the console. Gunicorn would normally put
# the traceback on stderr, and stderr is not arriving either. So the traceback
# exists somewhere; this finds where.
#
# ORDER MATTERS. Section 1 is the cheapest and most likely answer (a log file
# inside the container). Section 4 is the fallback that works even if nothing
# was ever written: ask Django itself what its logging config is.
#
# READ-ONLY. Reads process arguments, config and log files. Starts nothing,
# restarts nothing, sends no request to the application.
#
# USAGE (on the LiveORC host, in ~/code/git/openrivercam after a git pull)
#   ./spring_2026_ID/liveorc_server/liveorc-host/find-500-traceback.sh
set -u
D=docker; docker ps >/dev/null 2>&1 || D="sudo docker"
C=liveorc_webapp
STAMPS='02/Sep/2026:07:31 02/Sep/2026:09:31 03/Sep/2026:07:31 03/Sep/2026:10:31'
ISO='2026-09-02 07:31 2026-09-02 09:31 2026-09-03 07:31 2026-09-03 10:31'
h(){ printf '\n\033[1m== %s ==\033[0m\n' "$*"; }

h "1. log files inside the container"
$D exec "$C" sh -c '
  find / -xdev -name "*.log" -size +0 2>/dev/null | grep -viE "^/proc|^/sys" | head -40
  echo "--- and anything under a logs/ dir ---"
  ls -la /liveorc/logs /app/logs /var/log 2>/dev/null | head -40' 2>&1 | sed 's/^/  /'

h "2. grep every one of those for the four 500 timestamps"
$D exec "$C" sh -c '
  for f in $(find / -xdev -name "*.log" -size +0 2>/dev/null | grep -viE "^/proc|^/sys"); do
    for s in 02/Sep/2026:07:31 02/Sep/2026:09:31 03/Sep/2026:07:31 03/Sep/2026:10:31 \
             "2026-09-02 07:31" "2026-09-02 09:31" "2026-09-03 07:31" "2026-09-03 10:31"; do
      if grep -q "$s" "$f" 2>/dev/null; then
        echo "### HIT in $f for $s"
        grep -A40 "$s" "$f" 2>/dev/null | head -60
      fi
    done
  done' 2>&1 | cut -c1-300 | sed 's/^/  /'
echo "  (no HIT lines above means nothing on disk recorded them either)"

h "3. how is gunicorn actually invoked — where is it told to send errors"
$D exec "$C" sh -c 'ps auxww 2>/dev/null | grep -iE "gunicorn|uwsgi|runserver" | grep -v grep' \
  2>&1 | cut -c1-400 | sed 's/^/  /'
echo "  --- gunicorn config files ---"
$D exec "$C" sh -c 'find / -xdev -name "gunicorn*.py" -o -xdev -name "gunicorn*.conf*" 2>/dev/null | head -10' \
  2>&1 | sed 's/^/  /'
$D exec "$C" sh -c 'for f in $(find / -xdev -name "gunicorn*.py" -o -xdev -name "gunicorn*.conf*" 2>/dev/null | head -5); do echo "--- $f"; grep -iE "errorlog|accesslog|capture_output|loglevel" "$f"; done' \
  2>&1 | sed 's/^/  /'

h "4. what Django is configured to do with an unhandled exception"
$D exec "$C" sh -c 'grep -rn "LOGGING\|DEBUG *=\|ADMINS" --include="settings*.py" / 2>/dev/null | grep -v node_modules | head -20' \
  2>&1 | cut -c1-300 | sed 's/^/  /'

h "5. the docker log driver — is stderr even being kept"
$D inspect "$C" --format '{{json .HostConfig.LogConfig}}' 2>&1 | sed 's/^/  /'
$D inspect "$C" --format 'Cmd: {{json .Config.Cmd}}{{"\n"}}Entrypoint: {{json .Config.Entrypoint}}' 2>&1 | sed 's/^/  /'

h "6. last resort — 500s are 5.6% of uploads, so the app may still be erroring"
echo "  --- anything exception-shaped anywhere in 14 days of container log ---"
$D logs --since "$(date -u -d '-14 days' '+%Y-%m-%dT%H:%M:%SZ')" "$C" 2>&1 \
  | grep -iE "traceback|error|exception|integrity|does not exist|null value|duplicate key" \
  | grep -vE '" (2[0-9]{2}|3[0-9]{2}|4[0-9]{2}) ' \
  | head -40 | cut -c1-300 | sed 's/^/    /'
echo "  (the filter drops ordinary access lines so only real log output remains)"

h "done"
echo "  Read-only. Nothing was changed."
echo "  What is wanted is one exception class and one file/line. If sections"
echo "  1-6 are all empty, the traceback was never written anywhere and the"
echo "  next step is a Django settings change, which is a separate decision."
