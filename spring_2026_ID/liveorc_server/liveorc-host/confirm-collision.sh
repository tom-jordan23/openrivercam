#!/usr/bin/env bash
# confirm-collision.sh — the last link, and a test across all 90 rows
#
# TODO-119. Where this stands after test-timeseries-collision.sh:
#
#   ESTABLISHED
#   - keyframe/thumbnail FILES exist on disk for the errored clips while their
#     DB columns are empty, so the exception lands after make_frames() and
#     before the final super().save() could persist them. This was a stated
#     prediction of the collision theory and it held.
#   - api_video carries UNIQUE (time_series_id).
#   - all four errored clips have NO time series at their own timestamp; the
#     nearest is ~1795 s away (the adjacent wake) and is already owned.
#   - healthy clips sit at dt = 0 against a series that belongs to them.
#
#   NOT ESTABLISHED
#   - whether camera_config.allowed_dt exceeds ~1800 s. If it does not, the
#     assignment is never attempted and the whole theory fails. One value.
#
# SECTION 2 IS THE REAL TEST, and it is why this is worth one more run. The
# theory makes a prediction about the WHOLE population, not just four rows:
#
#   - the 90 rows with an empty keyframe column should have their nearest
#     time series INSIDE allowed_dt and already owned  -> assignment attempted
#     -> IntegrityError -> 500, columns never persisted
#   - the 364 rows with a keyframe but no time series should have their
#     nearest series OUTSIDE allowed_dt -> no assignment -> clean save
#
# If those two populations do not separate that way, the theory is wrong even
# though the four-row sample fit it. Four rows can fit almost anything.
#
# READ-ONLY. SELECT queries only.
#
# USAGE (on the LiveORC host, in ~/code/git/openrivercam after a git pull)
#   ./spring_2026_ID/liveorc_server/liveorc-host/confirm-collision.sh
set -u
D=docker; docker ps >/dev/null 2>&1 || D="sudo docker"
h(){ printf '\n\033[1m== %s ==\033[0m\n' "$*"; }
DBU=$($D exec db sh -c 'printf %s "$POSTGRES_USER"' 2>/dev/null)
DBN=$($D exec db sh -c 'printf %s "${POSTGRES_DB:-$POSTGRES_USER}"' 2>/dev/null)
Q(){ $D exec -i db psql -U "$DBU" -d "$DBN" -At -F '|' -c "$1" 2>&1; }

h "1. THE MISSING VALUE — allowed_dt on the camera config"
Q "select cc.id, cc.site_id, cc.allowed_dt
   from api_cameraconfig cc order by cc.id;" | sed 's/^/  /'
echo "  --- which camera_config the station's video_config points at ---"
Q "select vc.id as video_config, vc.site_id, vc.camera_config_id, cc.allowed_dt
   from api_videoconfig vc left join api_cameraconfig cc on cc.id = vc.camera_config_id
   order by vc.id;" | sed 's/^/  /'
echo "  (allowed_dt > 1800s means the ~1795s neighbour IS assigned, and the"
echo "   UNIQUE constraint then raises. Under 1800s the theory is dead.)"

h "2. THE POPULATION TEST — do the two groups separate as predicted"
echo "  For every status-5 row on the site: distance to its nearest time series,"
echo "  whether that series is already owned, split by keyframe column."
Q "with site as (select site_id from api_videoconfig where id = 3),
        v as (select av.id, av.timestamp, av.keyframe, av.time_series_id
              from api_video av
              join api_videoconfig vc on vc.id = av.video_config_id
              where av.status = 5 and vc.site_id = (select site_id from site)),
        n as (select v.id, v.keyframe, v.time_series_id,
                     (select ts.id from api_timeseries ts
                      where ts.site_id = (select site_id from site)
                      order by abs(extract(epoch from (ts.timestamp - v.timestamp))) asc limit 1) as near_id,
                     (select abs(extract(epoch from (ts.timestamp - v.timestamp))) from api_timeseries ts
                      where ts.site_id = (select site_id from site)
                      order by abs(extract(epoch from (ts.timestamp - v.timestamp))) asc limit 1) as near_dt
              from v)
   select case when keyframe is null or keyframe='' then 'no keyframe col' else 'has keyframe col' end as grp,
          count(*) as rows,
          round(min(near_dt))||'..'||round(max(near_dt)) as dt_range,
          round(avg(near_dt)) as dt_avg,
          count(*) filter (where (select count(*) from api_video x where x.time_series_id = n.near_id) > 0) as nearest_already_owned
   from n group by 1 order by 1;" | sed 's/^/  /'
echo "  PREDICTED: 'no keyframe col' ~90 rows, small dt, nearest owned."
echo "             'has keyframe col' ~364 rows, LARGER dt (outside allowed_dt)."

h "3. the same split as a distance histogram, which is harder to fool"
Q "with site as (select site_id from api_videoconfig where id = 3),
        v as (select av.id, av.timestamp, av.keyframe
              from api_video av join api_videoconfig vc on vc.id = av.video_config_id
              where av.status = 5 and vc.site_id = (select site_id from site)),
        n as (select v.id, v.keyframe,
                     (select abs(extract(epoch from (ts.timestamp - v.timestamp))) from api_timeseries ts
                      where ts.site_id = (select site_id from site)
                      order by abs(extract(epoch from (ts.timestamp - v.timestamp))) asc limit 1) as near_dt
              from v)
   select case when keyframe is null or keyframe='' then 'no keyframe col' else 'has keyframe col' end,
          width_bucket(near_dt, 0, 7200, 4) as bucket, count(*)
   from n group by 1,2 order by 1,2;" | sed 's/^/  /'
echo "  (buckets over 0-7200s in 4 steps: 1=0-1800 2=1800-3600 3=3600-5400 4=5400-7200, 5=over)"

h "4. sanity — healthy rows should sit at dt 0"
Q "with site as (select site_id from api_videoconfig where id = 3),
        v as (select av.id, av.timestamp from api_video av
              join api_videoconfig vc on vc.id = av.video_config_id
              where av.status = 4 and vc.site_id = (select site_id from site)
              order by av.id desc limit 200),
        n as (select v.id, (select abs(extract(epoch from (ts.timestamp - v.timestamp)))
                            from api_timeseries ts where ts.site_id = (select site_id from site)
                            order by abs(extract(epoch from (ts.timestamp - v.timestamp))) asc limit 1) as near_dt
              from v)
   select round(min(near_dt)), round(avg(near_dt)), round(max(near_dt)), count(*) from n;" | sed 's/^/  /'

h "done"
echo "  Read-only. Nothing was changed."
echo "  Section 1 either completes the mechanism or kills it outright."
echo "  Section 2 decides whether it explains 90 rows or only the 4 I picked."
