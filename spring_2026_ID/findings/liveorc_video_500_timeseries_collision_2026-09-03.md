# LiveORC returns 500 on video upload when a clip has no time series of its own

**Date:** 2026-09-03
**Site:** Sukabumi City (site 4, video_config 3)
**Evidence:** host-side, read-only, via Session Manager. Scripts in
`liveorc_server/liveorc-host/`: `inspect-refusals.sh`, `inspect-500s.sh`,
`find-500-traceback.sh`, `inspect-video-post.sh`, `inspect-create-task.sh`,
`inspect-error-rows.sh`, `site4-inventory.sh`,
`test-timeseries-collision.sh`, `confirm-collision.sh`.
Nothing was written, restarted or posted at any point.

## Summary

LiveORC returns HTTP 500 on `POST /api/video/` for about 5.6% of uploads from
Sukabumi. The cause is in LiveORC, not the link, and it is marked in the
upstream source as a known gap.

When a video arrives with no time series at its own timestamp, `Video.save()`
attaches the *nearest* one instead. `time_series` is a `OneToOneField`, the
candidate set is not filtered to exclude series already attached to another
video, and `allowed_dt` is exactly 30 minutes — the same as the station's wake
interval. So the neighbouring wake's series sits 1790–1799 s away, just inside
the window, and is already owned. The save raises `IntegrityError` on
`UNIQUE (time_series_id)`.

**The video file is not lost.** The row and the file are committed before the
exception, so the server holds the clip. It is marked ERROR, has no keyframe or
thumbnail column, and no time series — while the station records the upload as
FAILED and believes the clip never arrived.

**62 rows on site 4 are in this state.**

## The mechanism

`api/models/video.py`, `Video.save()`:

```python
super(Video, self).save(*args, **kwargs)     # (1) row committed
if new_file:
    self.file = file
    super(Video, self).save(*(), **{})       # (2) committed again, with the file
    if not(self.make_frames()):              # (3) writes keyframe/thumb FILES,
        raise Exception(...)                 #     columns set with save=False
    ...
    ts_at_site = TimeSeries.objects.filter(site = self.video_config.site)
    # TODO: exclude time series records that are already used by another video
    if len(ts_at_site) != 0:
        ts_closest = get_closest_to_dt(ts_at_site, self.timestamp)
        dt = np.abs(self.timestamp - ts_closest.timestamp)
        if dt < self.video_config.camera_config.allowed_dt:
            self.time_series = ts_closest    # (4) may already be owned
    super(Video, self).save(*(), **{})       # (5) raises IntegrityError here
```

Steps 1 and 2 commit. Step 3 writes the images to storage but, because
`img_field.save(..., save=False)`, does not write the columns — only step 5
would. Step 5 raises, so the columns never persist. That produces a state
nothing else in this path produces: **keyframe and thumbnail files present on
disk, their database columns empty.**

`api/views/video.py` does not catch it, `settings.py` defines no
`ATOMIC_REQUESTS`, so nothing rolls back and DRF returns a 500 with Django's
145-byte HTML error page.

## The evidence

| claim | evidence |
|---|---|
| The requests arrive and we answer 500 | `POST /api/video/ HTTP/1.0" 500 145`, exact timestamp match on all four |
| Not a size cap | `client_max_body_size 512M`, clips are ~9–10 MB |
| Not a proxy timeout | `proxy_read_timeout 300000s` |
| Not blocking | no fail2ban, no `limit_req`/`limit_conn` |
| Not truncation | errored files 10308381 / 9307256 / 9315078 / 10276292 B vs healthy 9.7–9.8 MB |
| Not keyframe extraction | cv2 on the errored clip: `opened=True frame_count=64.0 read_ok=True img=(1080,1920,3)` — identical to healthy |
| Exception is after `make_frames` | keyframe/thumb **files** on disk, columns empty |
| The constraint exists | `api_video_time_series_id_key | UNIQUE (time_series_id)` |
| The window is exactly the wake interval | `allowed_dt = 00:30:00`; station wakes every 30 min |
| The whole population fits | 62 rows, Δt **1790–1799 s**, nearest already owned **62/62** |
| Healthy rows differ | Δt = 0 across 200 sampled |

The nine-second band is the result. It is the 1800 s wake interval minus
capture jitter, and it is not something a competing explanation produces.

## What is upstream's to fix

`get_closest_to_dt` should exclude time series already attached to a video —
the TODO in the source says so. Failing that, the assignment should be guarded,
or the `IntegrityError` caught and the video saved without a time series.

**This must go upstream, not into the running container.** The rule stands:
never change what a version upgrade would overwrite.

Two secondary defects worth reporting alongside it:

1. **Frame extraction runs inline inside `save()`**, so any failure there
   becomes a 500 on upload rather than a handled error.
2. **`schemas/base.py:47` on the ORC-OS side destroys the diagnosis.** It
   formats its error with `r.json()['detail']`; on a non-JSON error body
   `r.json()` raises and the status code is lost. That is why a 5.6%
   server-side error rate has been invisible from the station for as long as
   anyone has looked at these failures — every previous tally recorded them as
   transport faults, or missed them.

## Consequences for TODO-119

**FAILED on the station does not mean absent from the server.** Four confirmed
cases, 62 rows in the class. Any re-drive scoped from the station's `FAILED`
set will re-send clips the server already holds. `get_video_path` is
deterministic and `OverwriteFileSystemStorage` replaces same-named files, so
the file would be overwritten — but nothing constrains `timestamp`, so a
**duplicate row** would be created.

**These 62 do not need re-uploading at all.** The bytes are on the server. What
they need is the time-series association repaired, which is a server-side
operation costing no metered station data.

**Track 2, now that the per-day join is done.** The pairing is committed at
`station-health/joins/station_vs_server_by_day_2026-09-03.txt` (station
`failedbyday119aa`, 19:00:43Z; server `site4-inventory.sh`).

- Station: 5,740 video rows, **3,013 FAILED**, 2,601 SYNCED, 126 LOCAL.
- Server, site 4: 2,715 rows over 80 days; the station has rows on 126 days.
- **Summed per-day gap: 3,025 against 3,013 FAILED — agreement to 0.4%.**

So at day granularity the FAILED backlog really is absent from the server, and
the concern that it might already be held does not survive contact with the
numbers. The 62 present-but-errored rows sit inside that 0.4%; separating them
exactly needs a timestamp-level join, not a day-level one.

**Correction to an earlier claim in this document.** I wrote that the absent
days "sum to roughly the record's 1,190 clips". They do not — they sum to
**3,025**. The 1,190 figure is not the number missing from the server; it is
the number of FAILED clips whose **files still exist on the station's disk**
and can therefore be re-driven. The remaining ~1,825 are FAILED rows whose
files the disk manager has already purged. They are gone, and no re-drive
recovers them. The two numbers were never the same quantity and I conflated
them.

Contiguous spans the server has nothing for, where the station did capture:

| span | clips |
|---|---|
| 2026-04-22 → 05-11 | 938 |
| 2026-07-30 → 08-09 | 527 |
| 2026-05-17 → 05-21 | 240 |
| 2026-08-28 → 08-31 | 192 |
| 2026-06-21 → 06-22 | 96 |
| 2026-07-23 | 48 |
| 2026-04-08 → 04-20 | 15 |
| **total** | **2,056** |

The rest of the 3,025 is scattered partial-day loss, heaviest on 08-23→08-27
(39–42/day missing against a 48/day capture rate).

**An open question this raised, not previously in the record.** Five spans have
no station rows at all — the station captured nothing:
2026-04-09→04-13, 04-15→04-19, 05-12, **06-25→07-01 (7 days)**, and
**08-15→08-19 (5 days)**. These are capture outages, not sync failures, and
they are a different class from everything TODO-119 has been chasing. The
06-25→07-01 and 08-15→08-19 spans are not explained by anything in the record I
have read.

## Corrections made along the way

Three of my hypotheses died against this evidence, and the sequence is worth
keeping:

1. **A refusal — 413/502/504.** Wrong; it is a 500 from our own application.
2. **A truncated upload.** Wrong; the files are full size, two of them larger
   than healthy ones.
3. **Keyframe extraction failing on an unreadable file.** Wrong; cv2 reads the
   errored clip exactly as it reads a healthy one.

Also two analysis bugs of mine, both of which produced confident wrong output:
`inspect-refusals.sh` section 3 read `/var/log/nginx/access.log` when the
container logs to Docker's json driver, and printed "the requests never
arrived" — the exact opposite of the truth, in a form indistinguishable from a
real negative finding. And an earlier station-side script capped its traceback
search at 80 lines, reporting `frame=none` for 8 of 9 failures and nearly
retiring a correct conclusion.

The pattern in all five: the output looked like a finding. Only the ones that
made a falsifiable prediction — the keyframe files, the nine-second band —
turned out to be worth anything.
