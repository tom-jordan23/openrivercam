#!/usr/bin/env bash
# site4-inventory.sh — what does the server already hold for Sukabumi, per day?
#
# TODO-119 Track 2. Tom's answer is that the 1,190 backlog clips need
# uploading. That answer assumes the server does not already have them, and
# inspect-create-task.sh showed the assumption is not safe in general: four
# clips the station recorded as FAILED are on the server, with matching
# timestamps, at status 5.
#
# The per-day counts from inspect-error-rows.sh looked reassuring - 43-48 rows
# a day for ordinary days, collapsing to 6-9 exactly on the outage windows,
# with whole spans absent - and the gaps sum to roughly 1,150 against the
# record's 1,190. But that query counted EVERY SITE on the server, not
# Sukabumi, so it is suggestive and not evidence. This filters to site 4.
#
# Output is deliberately compact: one line per day. Paired against the
# station's own per-day FAILED counts it says exactly which days need
# re-driving and which are already held - which is the difference between
# sending 10.69 GB and sending a fraction of it, over a SIM whose postpaid
# status is still unconfirmed.
#
# Section 3 is a separate question: why cv2 cannot read those four files. They
# are full size, so this is not truncation. Reading one with cv2 in the
# container reproduces the failure and names the error. It opens a file for
# reading and prints a result - no database access, no API call, no write.
#
# READ-ONLY throughout.
#
# USAGE (on the LiveORC host, in ~/code/git/openrivercam after a git pull)
#   ./spring_2026_ID/liveorc_server/liveorc-host/site4-inventory.sh
set -u
D=docker; docker ps >/dev/null 2>&1 || D="sudo docker"
C=liveorc_webapp
h(){ printf '\n\033[1m== %s ==\033[0m\n' "$*"; }
DBU=$($D exec db sh -c 'printf %s "$POSTGRES_USER"' 2>/dev/null)
DBN=$($D exec db sh -c 'printf %s "${POSTGRES_DB:-$POSTGRES_USER}"' 2>/dev/null)
Q(){ $D exec -i db psql -U "$DBU" -d "$DBN" -At -F '|' -c "$1" 2>&1; }

h "1. confirm which video_config/site the station posts to"
Q "select vc.id as video_config, vc.site_id, s.name, count(v.id)
   from api_videoconfig vc
   left join api_video v on v.video_config_id = vc.id
   left join api_site s on s.id = vc.site_id
   group by 1,2,3 order by 4 desc;" | sed 's/^/  /'
echo "  (the four known 500s all carry video_config_id = 3)"

h "2. SUKABUMI ONLY — one line per day: day|done|error|total"
Q "select date(v.timestamp), count(*) filter (where v.status=4),
          count(*) filter (where v.status=5), count(*)
   from api_video v
   join api_videoconfig vc on vc.id = v.video_config_id
   where vc.site_id = (select site_id from api_videoconfig where id = 3)
   group by 1 order by 1;" | sed 's/^/  /'

h "2b. totals and span for that site"
Q "select min(v.timestamp), max(v.timestamp), count(*)
   from api_video v join api_videoconfig vc on vc.id = v.video_config_id
   where vc.site_id = (select site_id from api_videoconfig where id = 3);" | sed 's/^/  /'
echo "  --- and the days with NO rows at all, inside the covered span ---"
Q "select d::date from generate_series(
       (select min(date(v.timestamp)) from api_video v join api_videoconfig vc on vc.id=v.video_config_id
        where vc.site_id=(select site_id from api_videoconfig where id=3)),
       (select max(date(v.timestamp)) from api_video v join api_videoconfig vc on vc.id=v.video_config_id
        where vc.site_id=(select site_id from api_videoconfig where id=3)),
       interval '1 day') d
   where d::date not in (
     select date(v.timestamp) from api_video v join api_videoconfig vc on vc.id=v.video_config_id
     where vc.site_id=(select site_id from api_videoconfig where id=3))
   order by 1;" | tr '\n' ' ' | fold -w 180 | sed 's/^/  /'

h "3. why can cv2 not read those four files"
echo "  Reading one file and reporting what OpenCV says. No write, no DB, no API."
$D exec "$C" python3 -c "
import cv2, os
for p in ['/liveorc/media/videos/4/20260903/20260903T073132.mp4',
          '/liveorc/media/videos/4/20260903/20260903T180132.mp4']:
    ok = os.path.exists(p)
    sz = os.path.getsize(p) if ok else -1
    cap = cv2.VideoCapture(p)
    opened = cap.isOpened()
    frames = cap.get(cv2.CAP_PROP_FRAME_COUNT) if opened else -1
    res, img = cap.read() if opened else (False, None)
    cap.release()
    print(f'{os.path.basename(p)}  exists={ok} size={sz} opened={opened} frame_count={frames} read_ok={res} img={\"None\" if img is None else img.shape}')
" 2>&1 | sed 's/^/    /'
echo "    (first is an errored clip, second a healthy one from the same day."
echo "     read_ok=False with img=None is the cv2.cvtColor(None) crash path.)"

h "done"
echo "  Read-only. Nothing was changed and nothing was posted."
echo "  Section 2 is the one to paste back - it is what the re-drive should be"
echo "  scoped against."
