# TODO — Indonesia Spring 2026 Deployment (post-trip)

**Last updated:** 2026-08-07

The pre-trip task list (departure schedule day-by-day, in-country
deferred items, etc.) was archived to `archive/` after the April 2026
trip. This file tracks what's actually open *now*, post-trip.

| Priority | Meaning |
|----------|---------|
| P0 | Active workstream — blocks station producing useful data |
| P1 | Important — should resolve before scaling or before the next trip |
| P2 | Nice to have — schedule when slack is available |

| Status | Meaning |
|--------|---------|
| OPEN | Not started |
| IN PROGRESS | Work underway |
| PARKED | Waiting on external dependency (IPB engagement, vendor, etc.) |
| DONE | Complete |

---

## P0 — Active workstreams

### TODO-101: Configure deployed Sukabumi station with the salvage CameraConfig

| Field | Value |
|-------|-------|
| **Status** | IN PROGRESS |
| **Site** | Sukabumi |

The auto-fit salvage pipeline produced a passing CameraConfig
(`spring_2026_ID/survey_data/sukabumi_handoff/sukabumi_autofit_camera_calibration.json`,
4.61 cm RMSE on the 6-GCP subset GCP7/8/10/13/14/3.2) and an end-to-end
ORC-OS run on the calibration video already produced
`q_50 = 0.51 m³/s`, `v_av = 0.49 m/s`, `fraction_velocimetry = 65.7 %`.
Remaining work is loading the same configuration onto the deployed
station (not just the local Docker harness) and verifying it processes
real captured video.

**Prerequisite — `h_ref` durability:**
Set `h_ref = 617.065` through the dashboard form for camera_config
"Sukabumi_A" (not via SQL — see ISS-FIELD-003). Verify by
`sqlite3 ~/.ORC-OS/orc-os.db "select json_extract(data,'$.gcps.h_ref') from camera_config where name='Sukabumi_A'"`.
Then exercise a dashboard save and re-check — the value must survive.

**Steps:**
- [ ] Import `sukabumi_autofit_camera_calibration.json` onto the
      deployed Sukabumi station (one-shot API import per
      `survey_data/sukabumi_handoff/README.md` § "One-shot API import",
      OR paste the 6-GCP subset and click GCPs in the dashboard).
- [ ] Set `h_ref = 617.065` through the dashboard form. Verify
      durability by saving once and re-querying the DB.
- [ ] Upload `cross_section.geojson` from the handoff folder via
      `POST /cross_section/from_geojson/` (CSV upload has no CRS
      parameter, ends up CRS-less).
- [ ] Wire `video_config.id=1` to the new camera_config and
      cross_section. Set `cross_section_wl_id` for optical fallback.
- [ ] Trigger Process on a real recent capture (not just the
      calibration video). Expected: end-to-end completes, produces
      `transect_*.nc`, `plot_quiver.jpg`, populates `time_series`.
- [ ] Inspect `plot_quiver.jpg` for flow direction. The 2026-04-22
      run on the calibration video showed vectors that *appeared* to
      oppose the true downstream direction — diagnosis was parked
      after a cross-section reversal turned out to be the wrong fix
      (see `survey_data/corrections.md` 2026-04-22 entries). This
      needs an unbiased look on a real capture, not the calibration
      video.

### TODO-102: Stand up Grafana on the AWS LiveORC server for sensor data

| Field | Value |
|-------|-------|
| **Status** | OPEN |
| **Site** | LiveORC server (AWS) |

The Sukabumi station uploads sensor CSVs (RG-15 rainfall, SHT40
temperature/humidity, DS18B20 temp probe) to the LiveORC server via
`orc-sensors-upload` on every boot / hourly. There's no visualization
of that data yet — it accumulates in CSV form on the server.

**Goal:** A Grafana instance on the LiveORC AWS host with dashboards
for each station's sensor stream, viewable via a public-but-auth'd URL
that PMI, IPB, and other stakeholders can reach.

**Steps:**
- [ ] Decide on data source backend: read CSVs directly, or import to
      InfluxDB / Postgres with a TimescaleDB extension first. CSV-direct
      via the Grafana CSV plugin is simplest for the current scale; a
      TSDB pays off once we have multi-station + multi-month data.
- [ ] Provision Grafana on the LiveORC host (Docker Compose alongside
      the existing LiveORC stack, or systemd direct install).
- [ ] Configure auth — at minimum a non-default admin password; ideally
      reverse-proxied behind the same auth as LiveORC's web UI.
- [ ] Build dashboards: rainfall (RG-15 cumulative + interval),
      enclosure temperature/humidity (SHT40), water/air temp (DS18B20),
      uptime / capture cadence (derived from upload timestamps).
- [ ] Document the URL, credentials handoff, and refresh cadence in
      `reference_liveorc_server.md` (in user memory) and a public-facing
      doc.

### TODO-103: Verify LiveORC video and sensor uploads from Sukabumi

| Field | Value |
|-------|-------|
| **Status** | RESOLVED 2026-07-07 (alerting follow-up remains — see below) |
| **Site** | Sukabumi → LiveORC server |

End-to-end verification done. Videos/hydrology were uploading fine.
**Sensor CSV uploads were silently failing** — and had been for weeks:
`orc-sensors-upload` fires ~5 s after boot, before the LTE modem
registers, so its PUTs failed (`curl 6/7`); the old fail-fast +
all-or-nothing watermark then never advanced, and alphabetical upload
order starved sht40. The server had stalled at sht40≤05-15, rg15≤06-15,
ds18b20≤07-03 while the sensors kept logging locally.

**Resolution:** fixed in commit 966d327 (curl `--retry` +
oldest-mtime-first + per-file resumable watermark), deployed to the
station 2026-07-07. Backlog recovered with `pi/tools/orc_flush_one.sh`;
all three sensors now current on the server. Permanently lost: sht40
2026-05-16 → 06-07 (the 30-day CSV rotation deleted it before recovery —
see `pi/tools/README.md`).

**Steps:**
- [x] Confirm recent Sukabumi video uploads on LiveORC (videos were flowing).
- [x] Inspect sensor CSV ingest — root-caused the stall, fixed, rows now
      landing for the current date.
- [x] Verify Pi side: `orc-sensors-upload` now rides the boot-race and
      advances its watermark (it's invoked from orc-capture each wake
      cycle, not a boot+hourly timer).
- [ ] **Alerting (still open):** add a low-rate detector so the next
      upload gap is caught in hours, not weeks — e.g. a Grafana "no
      sensor rows in N hours" alert on the TimescaleDB, or a daily
      server-side scrape. This gap went undetected precisely because
      nothing watched for staleness.

### TODO-104: Coordinate IPB engagement (site + survey)

| Field | Value |
|-------|-------|
| **Status** | OPEN |
| **Sites** | Both |

Two parallel asks for IPB:

**Sukabumi — total station re-survey.** Use
`survey/outsourced_survey_brief.md` as the SOW template, scoped to
total station (not RTK). Section 2 deliverables stand; section 5
checklist needs the RTK-specific items replaced with total-station
equivalents (instrument model + serial, control point coordinates and
how they were established, traverse closure error, vertical
adjustment method).

**Jakarta — site selection.** Need IPB's hydrological judgment on
candidate sites that are (a) in PMI's flood-warning catchments of
interest, (b) have a clear permission/installation path, and
(c) are not subject to the same urban RF / sky-view problems that
appear to have hurt RTK at the Sukabumi canal site.

**Steps:**
- [ ] Identify the right IPB contact(s) and make introductions
      through PMI.
- [ ] Send the survey SOW for Sukabumi.
- [ ] Send a separate brief for Jakarta site selection.
- [ ] Track responses; do not block other workstreams on them.

---

## P1 — Important, but not blocking the active workstreams

### TODO-105: Document `h_ref` durability problem upstream

| Field | Value |
|-------|-------|
| **Status** | OPEN |
| **Site** | Both (ORC-OS general issue) |

ISS-FIELD-003: ORC-OS dashboard "save" overwrites SQL-edited
camera_config fields. File a clear repro upstream so the
ORC-OS team can scope a fix (partial PATCH vs full-blob clobber on
save). Until then, the workaround is "always go through the dashboard
form."

### TODO-106: Re-evaluate camera-only / split-architecture deployment

| Field | Value |
|-------|-------|
| **Status** | OPEN |
| **Site** | Future deployments |

Per LESSONS_LEARNED #4, a camera-only field node with remote compute
would have made the Jakarta permission situation much easier (the
permission ask is "mount an IP camera" not "build a full enclosure").
The `docs/SPLIT_ARCHITECTURE_DESIGN.md` doc was written pre-trip but
not field-tested. Pick this up before the next site selection round.

### TODO-107: Sukabumi station — outstanding small issues

| Field | Value |
|-------|-------|
| **Status** | OPEN |
| **Site** | Sukabumi |

Carried over from pre-trip TODO. Now that the station is on-site and
remote-accessible:

- [ ] **TODO-019** (was P2): `getty@tty1` cycling auto-login for
      non-existent `hcwinsemius` user. Fix the autologin override.
- [ ] **TODO-020**: Document unprovisioned-SIM diagnostic state in
      `docs/TROUBLESHOOTING.md` (full symptom signature is in this
      file's prior version, archived in git history).
- [ ] **TODO-021**: Tailscale persistent-login `deploy.sh` integration
      — auth key is staged at `/home/pi/.tailscale_nodekey` on
      Sukabumi but `deploy.sh` doesn't yet wire it up.
- [ ] **TODO-022**: Verify RG-15 rain gauge response and polling-mode
      configuration (gauge went silent on UART 2026-04-17). Field
      check on next site visit.
- [ ] **TODO-012** (rev): Verify DDR-60G quiescent power draw against
      the 0.5 W estimate. Update power budget if the measured value
      diverges.
- [ ] **TODO-012b**: Re-export `circuit_diagram.pdf` from the updated
      drawio source.

### TODO-108: Jakarta station — bench soak rather than warehouse

| Field | Value |
|-------|-------|
| **Status** | OPEN |
| **Site** | Jakarta (currently in US) |

The built Jakarta station is back in the US. While IPB site selection
is in flight, run it on a bench as an extended soak rig:

- [ ] Power on, run on continuous capture against any RTSP source
      (a webcam pointed at a window is fine for soak).
- [ ] Verify all sensors (RG-15, DS18B20, SHT40), capture daemon,
      sensor logger, upload, LED status all run reliably for weeks.
- [ ] Track any failures that emerge on long soak — these are the
      thermal/humidity issues that would otherwise show up first in
      the field.

---

## P2 — Schedule when slack allows

### TODO-109: Indonesia trip retrospective writeup

| Field | Value |
|-------|-------|
| **Status** | OPEN |

`LESSONS_LEARNED.md` has the structured outcomes; a more narrative
trip retrospective (timeline, what worked, what didn't, photos) would
be useful for funder reporting and as input for the next trip plan.

### TODO-110: Spares inventory reconciliation

| Field | Value |
|-------|-------|
| **Status** | OPEN |

`BOM_Spares.md` was the pre-trip plan. After the trip, the actual
spares left at the PMI office (and what came back to the US with the
Jakarta kit) need reconciling. Do this before the next trip plan.

### TODO-111: Google Sheets export of sensor data

| Field | Value |
|-------|-------|
| **Status** | IN PROGRESS |
| **Site** | LiveORC server (AWS) |

Grafana (TODO-102) covers people who will log into Grafana. Stakeholders
who won't — PMI, IPB — need the sensor data somewhere they can filter
and chart it themselves, without a login or a self-signed-cert warning.
A Google Sheet is that surface.

The `sheets-export` service is written, wired into the compose stack, and
verified locally against a seeded TimescaleDB. What remains is the
Google-side setup and the deploy, both of which need a human in a browser.

**Design note — why there is no `ts` watermark:** sensor CSVs backfill
(that is exactly what the TODO-103 recovery did), so a `max(ts)` cursor
would silently skip replayed rows. Instead a `sensor_exports` ledger
table is anti-joined against `sensor_readings`. Verified locally: after
a backfill the naive query finds 0 rows while the anti-join finds all
1,440. `sensor_readings` is never altered. **Never prune
`sensor_exports` — it is the cursor.**

**Steps:**
- [x] Write the exporter, matching `sensor-ingest` conventions.
- [x] Validate the cursor against a local TimescaleDB, including the
      backfill case and a fault-injected crash in the append/mark window
      (0 rows lost; the batch re-appends, by design).
- [x] Document setup, deploy, dedupe, and rollover in
      `liveorc_server/README.md`.
- [ ] Create the spreadsheet (must be a human — a service account has no
      Drive storage quota). Decide Shared Drive vs personal Drive; the
      target is one `.env` variable, so this is repointable later.
- [ ] Add the `G1` disclaimer cell mirroring the mandatory Grafana
      banner, and set the sheet timezone to UTC.
- [ ] Create the GCP service account, enable the Sheets API, download the
      JSON key, share the sheet with its `client_email` as Editor.
- [ ] Deploy via Session Manager (no SSH on that host): `git pull`,
      rsync into `/opt/orc-additions` (**no `--delete`**), install the
      key as `1001:1001` mode `0400`, run once with
      `EXPORT_MODE=preview`, then switch to `live`.
- [ ] Confirm the ~130k-row first backfill completes without rate-limit
      errors, and that the four pre-existing containers were not
      recreated.

**Blocked** on TODO-112 — the LiveORC host had no free disk on 2026-08-10.
Nothing from this workstream reached the server, so it resumes unchanged
once the host is healthy.

### TODO-112: Move LiveORC media onto a dedicated EBS volume

| Field | Value |
|-------|-------|
| **Status** | IN PROGRESS |
| **Site** | LiveORC server (AWS) |

On 2026-08-10 the root filesystem hit 100% and took the host down —
LiveORC dead, Session Manager refusing to open a shell, Run Command
returning exit 1 with zero bytes on both streams, CPU pinned at ~98% for
a week.

The cause was a **path mismatch**. `MEDIA_ROOT` is `/liveorc/media`
(`settings.py:126`), but the compose bind targeted `/liveorc/data/media`
— a path Django never writes to. So 26 GB of video, 1.3 GB of keyframes
and 9.5 MB of thumbnails accumulated in the webapp container's
**ephemeral writable layer** between 2026-05-14 and 2026-07-29, with no
persistence, no backup, and no error ever raised. The mismatch is residue
from an abandoned S3 migration whose mount was left pointing somewhere
inert rather than removed.

S3 is not the fix and was correctly abandoned: LiveORC's storage backend
is all-or-nothing (prod runs `FileSystemStorage`, and `prod_reprocess.sh`
execs inside the webapp precisely to read local media), and `rename`/
`link` fail with `EXDEV` across a mount boundary — s3fs has no hardlink
support at all.

Full incident analysis and the phased procedure are in
[`liveorc_server/MEDIA_VOLUME_RUNBOOK.md`](liveorc_server/MEDIA_VOLUME_RUNBOOK.md).

**Two landmines this exposed**, both worth fixing regardless: the
reprocess runbook asserted a media backup was unnecessary "because the
video bytes live in MinIO/S3" — they did not, so any `--force-recreate`
during those runs would have destroyed 26 GB silently; and nothing
guarded the mount, so the one condition that mattered went unchecked.

**Steps:**
- [x] Diagnose: disk full, not compromise or runaway process.
- [x] Repair the root volume — it had been grown 50→80 GiB but
      `growpart` died at boot with `ENOSPC`, so partition and filesystem
      were expanded by hand. `/` now 77 G at 62%.
- [x] Confirm the database is safe (`db` → named volume
      `liveorc_lorc_data`, writable layer 0 B).
- [ ] Phase 0: determine whether LiveORC does `os.link`/`os.rename` into
      `MEDIA_ROOT` — decides whether `/liveorc/data` must share the new
      filesystem.
- [ ] Phase 1: DB backup → `s3://openrivercam-video/backups/`.
- [ ] Phases 2–5: create/attach/format a 150 GiB gp3 volume at
      `/var/lib/liveorc-media`, seed image assets, copy the 26 GB,
      verify with a dry-run `rsync --itemize-changes`, snapshot.
- [ ] Phase 6: repoint `.env`, compose, and `liveorc.service`
      (`RequiresMountsFor`); retire the vestigial s3fs mount unit.
- [ ] Phase 7: recreate, confirm the writable layer drops to MB and `/`
      falls to ~20 G; open an existing video and upload a new one.
- [ ] Add a disk-space alarm on `/` — its absence is why this ran
      undetected for ten weeks.
- [ ] Correct the false media-backup claim in
      `reprocess/REPROCESS_RUNBOOK.md`.

---

## DONE — post-trip

(Completed work since returning from Indonesia goes here. Use the
`Last updated` date at the top of the file as the reference point.)

*(none yet — file just rebuilt)*

---

## Pre-trip TODO history

The pre-trip task list (TODO-001 through TODO-022, all the day-by-day
hardware/software/integration items, and the build-week checklists)
is preserved in git history. Run
`git log --follow -p spring_2026_ID/TODO.md` to read it. Anything from
that list that's still open post-trip is mentioned by reference under
TODO-107 above.
