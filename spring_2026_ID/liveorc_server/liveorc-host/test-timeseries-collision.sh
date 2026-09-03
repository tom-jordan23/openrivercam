#!/usr/bin/env bash
# test-timeseries-collision.sh — is the 500 a OneToOne collision on time_series?
#
# TODO-119. Two hypotheses have now died against this file. The 500 is not a
# truncated upload (the four errored files are full size) and it is not
# keyframe extraction (cv2 opens the errored clip and reads frame 0 exactly as
# it does a healthy one: opened=True, frame_count=64, read_ok=True).
#
# THE REMAINING CANDIDATE, and it is flagged in upstream's own comment.
# api/models/video.py save():
#
#     ts_at_site = TimeSeries.objects.filter(site = self.video_config.site)
#     # TODO: exclude time series records that are already used by another video
#     if len(ts_at_site) != 0:
#         ts_closest = get_closest_to_dt(ts_at_site, self.timestamp)
#         if dt < self.video_config.camera_config.allowed_dt:
#             self.time_series = ts_closest
#     super(Video, self).save()
#
# time_series is a OneToOneField. The candidate set is NOT filtered to exclude
# series already attached to another video. If get_closest_to_dt returns one
# that is taken, the save raises IntegrityError on the unique constraint, after
# the row has already been committed by the two earlier saves.
#
# WHY THE EMPTY KEYFRAME IS THE TEST. make_frames() calls img_field.save(...,
# save=False), which writes the image to storage but does NOT write the column.
# Only that final super().save() persists it. So if the collision theory is
# right, the keyframe and thumbnail FILES exist on disk while the database
# columns are empty - and that is a state nothing else in this code produces.
# Section 1 checks it. If the files are absent, the theory is wrong and the
# exception is earlier than I think.
#
# READ-ONLY. SELECT queries and directory listings. No writes, no API calls.
#
# USAGE (on the LiveORC host, in ~/code/git/openrivercam after a git pull)
#   ./spring_2026_ID/liveorc_server/liveorc-host/test-timeseries-collision.sh
set -u
D=docker; docker ps >/dev/null 2>&1 || D="sudo docker"
C=liveorc_webapp
h(){ printf '\n\033[1m== %s ==\033[0m\n' "$*"; }
DBU=$($D exec db sh -c 'printf %s "$POSTGRES_USER"' 2>/dev/null)
DBN=$($D exec db sh -c 'printf %s "${POSTGRES_DB:-$POSTGRES_USER}"' 2>/dev/null)
Q(){ $D exec -i db psql -U "$DBU" -d "$DBN" -At -F '|' -c "$1" 2>&1; }

h "1. THE TEST — do keyframe/thumbnail FILES exist for the four errored rows"
echo "  (DB columns are empty for all four. Files present = make_frames ran and"
echo "   the exception came later, which is the collision path.)"
for DAY in 20260902 20260903; do
  echo "  --- keyframe/$DAY ---"
  $D exec "$C" sh -c "ls -la /liveorc/media/keyframe/4/$DAY/ 2>/dev/null | head -20" 2>&1 | sed 's/^/    /'
  echo "  --- thumb/$DAY ---"
  $D exec "$C" sh -c "ls -la /liveorc/media/thumb/4/$DAY/ 2>/dev/null | head -20" 2>&1 | sed 's/^/    /'
done
echo "  Look for 20260902T073125, 20260902T093126, 20260903T073132, 20260903T103128."

h "2. the constraint that would raise"
Q "select conname, pg_get_constraintdef(oid) from pg_constraint
   where conrelid='api_video'::regclass and contype in ('u','p','f')
   order by contype;" | sed 's/^/  /'

h "3. for each errored clip, is the nearest time series already taken"
for ID in 3931 3935 3950 3956; do
  echo "  --- video $ID ---"
  Q "with v as (select id, timestamp, video_config_id from api_video where id=$ID),
          s as (select vc.site_id from api_videoconfig vc, v where vc.id=v.video_config_id)
     select ts.id, ts.timestamp,
            abs(extract(epoch from (ts.timestamp - v.timestamp))) as dt_sec,
            (select count(*) from api_video x where x.time_series_id = ts.id) as used_by
     from api_timeseries ts, v, s
     where ts.site_id = s.site_id
     order by abs(extract(epoch from (ts.timestamp - v.timestamp))) asc
     limit 3;" | sed 's/^/    /'
done
echo "  (used_by = 1 on the NEAREST series is the collision: the save would try"
echo "   to attach a series another video already owns.)"

h "4. the same look for four healthy rows, for contrast"
for ID in $(Q "select id from api_video where status=4 order by id desc limit 4;"); do
  echo "  --- video $ID (healthy) ---"
  Q "with v as (select id, timestamp, video_config_id, time_series_id from api_video where id=$ID),
          s as (select vc.site_id from api_videoconfig vc, v where vc.id=v.video_config_id)
     select ts.id, ts.timestamp,
            abs(extract(epoch from (ts.timestamp - v.timestamp))) as dt_sec,
            (select count(*) from api_video x where x.time_series_id = ts.id) as used_by
     from api_timeseries ts, v, s
     where ts.site_id = s.site_id
     order by abs(extract(epoch from (ts.timestamp - v.timestamp))) asc
     limit 2;" | sed 's/^/    /'
done

h "5. how many time series are shared-candidates across the whole site"
Q "select used_by, count(*) from (
     select ts.id, (select count(*) from api_video x where x.time_series_id=ts.id) as used_by
     from api_timeseries ts
     where ts.site_id = (select site_id from api_videoconfig where id=3)
   ) t group by 1 order by 1;" | sed 's/^/  /'
echo "  --- and the 90 keyframe-less errored rows: do they all lack time_series ---"
Q "select case when keyframe is null or keyframe='' then 'no keyframe' else 'has keyframe' end,
          case when time_series_id is null then 'no ts' else 'has ts' end,
          count(*)
   from api_video where status=5 group by 1,2 order by 3 desc;" | sed 's/^/  /'

h "done"
echo "  Read-only. Nothing was changed and nothing was posted."
echo "  Section 1 is the discriminator; section 3 is the mechanism."
