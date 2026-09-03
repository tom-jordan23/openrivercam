#!/usr/bin/env bash
# inspect-error-rows.sh — how many clips does the server already hold, and why did they error?
#
# TODO-119. Settled 2026-09-03 by inspect-create-task.sh: all four clips whose
# upload returned 500 ARE on the server, with timestamps matching the station's
# rows exactly, at status 5 (ERROR) where successful uploads sit at 4 (DONE).
#
#   3931 | 2026-09-02 07:31:25 | 5      3950 | 2026-09-03 07:31:32 | 5
#   3935 | 2026-09-02 09:31:26 | 5      3956 | 2026-09-03 10:31:28 | 5
#
# So FAILED on the station does not mean absent from the server. That is a
# Track 2 problem before it is a bug: Tom's answer is that the 1,190 backlog
# clips need uploading, and that assumes the server does not have them.
#
# TWO QUESTIONS, in priority order.
#
# 1. HOW BIG IS THE OVERLAP? If the station's FAILED set and the server's rows
#    intersect, the re-drive would re-send clips already held - overwriting the
#    files (get_video_path is deterministic and OverwriteFileSystemStorage
#    replaces same-named files) while creating DUPLICATE rows, because nothing
#    constrains timestamp. Section 1 counts by status; section 2 lists what the
#    server holds per day so it can be joined against the station's list.
#
# 2. WHY DID IT ERROR? Video.save() commits the row, saves again with the file,
#    then raises a bare Exception if make_frames() fails. add_frame_to_model
#    reads frame 0 with cv2.VideoCapture and calls cv2.cvtColor on the result;
#    a truncated or unreadable file returns res=False and image=None, and
#    cvtColor(None) raises. Section 3 tests that directly: an errored row with
#    an EMPTY keyframe means extraction never produced one. Section 4 compares
#    the stored file sizes against healthy rows - a short file is a truncated
#    upload, which would make this a transport fault surfacing as a server
#    error rather than a server bug.
#
#    Note status 5 is also what the STATION posts: orc-os sends
#    "status": self.status.value in the payload. So status alone does not prove
#    where the error happened. The keyframe and file size do.
#
# READ-ONLY. SELECT queries and file stats. Writes nothing, posts nothing.
#
# USAGE (on the LiveORC host, in ~/code/git/openrivercam after a git pull)
#   ./spring_2026_ID/liveorc_server/liveorc-host/inspect-error-rows.sh
set -u
D=docker; docker ps >/dev/null 2>&1 || D="sudo docker"
C=liveorc_webapp
h(){ printf '\n\033[1m== %s ==\033[0m\n' "$*"; }
DBU=$($D exec db sh -c 'printf %s "$POSTGRES_USER"' 2>/dev/null)
DBN=$($D exec db sh -c 'printf %s "${POSTGRES_DB:-$POSTGRES_USER}"' 2>/dev/null)
Q(){ $D exec -i db psql -U "$DBU" -d "$DBN" -At -F '|' -c "$1" 2>&1; }
echo "  db: ${DBU:-<unset>}/${DBN:-<unset>}"

h "1. every video row by status — how big is the errored population"
Q "select status, count(*) from api_video group by status order by status;" | sed 's/^/  /'
echo "  (1=NEW 2=QUEUE 3=TASK 4=DONE 5=ERROR)"

h "2. what the server holds per day, for joining against the station's FAILED list"
Q "select date(timestamp) as day, count(*) filter (where status=4) as done,
          count(*) filter (where status=5) as error, count(*) as total
   from api_video group by 1 order by 1 desc limit 30;" | sed 's/^/  /'
echo "  --- overall span and totals ---"
Q "select min(timestamp), max(timestamp), count(*) from api_video;" | sed 's/^/  /'

h "3. THE DISCRIMINATOR — do the errored rows have a keyframe"
echo "  --- the four known 500s ---"
Q "select id, timestamp, status,
          case when file is null or file='' then 'NO FILE' else 'file' end,
          case when keyframe is null or keyframe='' then 'NO KEYFRAME' else 'keyframe' end,
          case when thumbnail is null or thumbnail='' then 'NO THUMB' else 'thumb' end,
          time_series_id, video_config_id
   from api_video where id in (3931,3935,3950,3956) order by id;" | sed 's/^/    /'
echo "  --- four healthy rows, for contrast ---"
Q "select id, timestamp, status,
          case when file is null or file='' then 'NO FILE' else 'file' end,
          case when keyframe is null or keyframe='' then 'NO KEYFRAME' else 'keyframe' end,
          case when thumbnail is null or thumbnail='' then 'NO THUMB' else 'thumb' end,
          time_series_id, video_config_id
   from api_video where status=4 order by id desc limit 4;" | sed 's/^/    /'
echo "  --- keyframe presence across ALL errored rows ---"
Q "select case when keyframe is null or keyframe='' then 'no keyframe' else 'has keyframe' end,
          count(*) from api_video where status=5 group by 1;" | sed 's/^/    /'
echo "  (errored rows without a keyframe = make_frames() raised = the 500 path)"

h "4. are the stored files short — is this a truncated upload"
for ID in 3931 3935 3950 3956; do
  P=$(Q "select file from api_video where id=$ID;")
  echo "  id $ID -> ${P:-<none>}"
  [ -n "$P" ] && $D exec "$C" sh -c "ls -la /liveorc/media/$P 2>/dev/null || find /liveorc -path '*$P' -exec ls -la {} + 2>/dev/null" \
    2>&1 | head -2 | sed 's/^/      /'
done
echo "  --- healthy files, for size comparison (station mean clip is 9.2 MB) ---"
for ID in $(Q "select id from api_video where status=4 order by id desc limit 3;"); do
  P=$(Q "select file from api_video where id=$ID;")
  echo "  id $ID -> ${P:-<none>}"
  [ -n "$P" ] && $D exec "$C" sh -c "ls -la /liveorc/media/$P 2>/dev/null || find /liveorc -path '*$P' -exec ls -la {} + 2>/dev/null" \
    2>&1 | head -2 | sed 's/^/      /'
done

h "5. the rest of the model — make_frames, is_ready_for_task, create_task"
$D exec "$C" sh -c 'sed -n "260,420p" /liveorc/api/models/video.py' 2>&1 | cut -c1-200 | sed 's/^/  /'

h "done"
echo "  Read-only. Nothing was changed and nothing was posted."
echo "  Section 1 sizes the duplicate risk for Track 2. Section 3 says whether"
echo "  the 500 is a truncated upload (transport) or a server-side bug."
