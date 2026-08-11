# TODO — Indonesia Spring 2026 Deployment (post-trip)

**Last updated:** 2026-08-11

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

Three parallel asks for IPB:

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

**Data access — LiveORC logins for IPB.** Ready to provision on
request: additional login links, account setup, and a walkthrough of
where the data lives. **Gated on PMI, not on us.** Dan was explicit on
the 2026-08-11 call that who gets access, and when, is PMI's decision —
do not provision ahead of that approval. Dan separately confirmed this
does *not* need to wait on the water-level adjustment, so the gate is
purely PMI's, not a technical readiness one.

**Steps:**
- [ ] Identify the right IPB contact(s) and make introductions
      through PMI.
- [ ] Send the survey SOW for Sukabumi.
- [ ] Send a separate brief for Jakarta site selection.
- [ ] Track responses; do not block other workstreams on them.
- [ ] **Data access — wait on PMI's approval.** Do not provision
      ahead of it.
- [ ] Once approved: create the LiveORC accounts, send login links,
      and confirm IPB can reach the data surfaces they actually need —
      the LiveORC web UI, Grafana (TODO-102), and the Sheet (TODO-111).

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

### TODO-113: Reprocess retained video under changed settings — and announce it

| Field | Value |
|-------|-------|
| **Status** | OPEN |
| **Site** | Sukabumi → LiveORC server |

Committed on the 2026-08-11 call: old video is retained, so a settings
change can be applied retroactively rather than only affecting future
captures. Two obligations follow.

**The experiment.** Swapping the cross sections was named specifically
— reprocess existing video with them swapped and see what it does to
the data. **Reconcile with TODO-101 first:** a cross-section reversal
was already tried on 2026-04-22 and turned out to be the wrong fix for
the apparent flow-direction problem (`survey_data/corrections.md`,
2026-04-22 entries). Either what was described on the call is a
different change than the one already tried, or that earlier finding
needs revisiting. Establish which before spending a reprocess run.

**The communication protocol.** Reprocessing changes numbers
stakeholders may already have seen, so each run gets announced to
PMI/IPB as it happens: what setting changed, which date range was
reprocessed, and that the prior figures are superseded. Silent
retroactive edits to a shared dataset are the failure mode.

**Blocked on TODO-112 in practice.** `prod_reprocess.sh` execs inside
`liveorc_webapp` to read local media, and that media currently exists
only in the container's ephemeral writable layer. Until the EBS
migration lands, any reprocess work on the server carries the same
risk the runbook already warns about — never `compose up` or
`--force-recreate` on that host.

**Steps:**
- [ ] Settle the cross-section question against the 2026-04-22
      correction before running anything.
- [ ] Confirm what video is retained and over what date range, on the
      station and on the server — this bounds the reprocess window.
- [ ] Sequence against TODO-112, or accept and document the writable-
      layer risk explicitly if a run can't wait.
- [ ] Run the reprocess per
      `liveorc_server/reprocess/REPROCESS_RUNBOOK.md`; compare outputs
      against the currently published figures.
- [ ] Announce the run and its effect on published data to PMI/IPB.

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
- [x] Create the spreadsheet (must be a human — a service account has no
      Drive storage quota). Done; the ID is server-side only, never
      committed, because this repo is public.
- [x] Create the GCP service account, enable the Sheets API, download the
      JSON key, share the sheet with its `client_email` as Editor.
- [x] Fix the `preview` gate (2026-08-10). `build_sheets_client()` returned
      `None` for every mode but `live`, and `check_sheet_access()` no-ops on a
      `None` client — so `preview`, the mode this deploy starts in precisely to
      prove auth and sharing, never loaded the key and never called the API. A
      bad share, a missed `chown 1001:1001`, or a non-UTC sheet would all have
      stayed silent until `live`, whose first act is the ~130k-row append. Now
      only `dry-run` gets a `None` client. Verified locally: preview reaches the
      access check and still appends nothing (`sensor_exports` flat across
      cycles, no `sheets append ok` lines).
- [ ] **Re-confirm the JSON key exists and locate it** — as of 2026-08-10 its
      whereabouts are unconfirmed, so treat the download as unverified. If it
      cannot be found, generate a new key and delete the old one in the console
      rather than hunting for it.
- [ ] Verify the sheet itself: tab named exactly `readings`, `A1:E1` =
      `ts,station,sensor,metric,value`, File → Settings → Time zone = UTC.
      `check_sheet_access()` warns on a non-UTC timezone at startup but
      does not fix it, and nothing creates the header row.
- [ ] Add the `G1` disclaimer cell mirroring the mandatory Grafana banner.
- [ ] Get the JSON key onto the host — **open question: where does it live
      now?** It must never transit chat. Target
      `/opt/orc-additions/secrets/sheets-sa.json`, `chown 1001:1001`,
      `chmod 0400` (the container drops to uid 1001 per its Dockerfile).
- [ ] Deploy via Session Manager (no SSH on that host): `git pull`,
      rsync into `/opt/orc-additions` (**no `--delete`**, and **exclude
      `.env`, `certs/`, `secrets/`**), run once with
      `EXPORT_MODE=preview`, then switch to `live`.
- [ ] Confirm the ~130k-row first backfill completes without rate-limit
      errors, and that the four pre-existing containers were not
      recreated.

**Unblocked 2026-08-10.** The root volume was repaired (`/` at 62%, 30 G
free), so this proceeds ahead of TODO-112. It is also safely separable:
sheets-export is a service in the `/opt/orc-additions` stack and never
touches `/opt/LiveORC` or the `liveorc_webapp` container.

**Ordering constraint:** put `SHEETS_SPREADSHEET_ID` into
`/opt/orc-additions/.env` **before** the rsync lands the new
`docker-compose.yml`. `${SHEETS_SPREADSHEET_ID:?…}` is evaluated for the
whole file, so without it every `docker compose` command against that
stack fails — including ones targeting the four healthy ORC containers.

**Start in `preview`.** The compose default is `EXPORT_MODE=${EXPORT_MODE:-live}`,
so an unset variable goes straight to live. `preview` neither appends nor
advances the ledger. Never set `dry-run` here: it advances the cursor
without writing, silently skipping real data.

### TODO-112: Move LiveORC media onto a dedicated EBS volume

| Field | Value |
|-------|-------|
| **Status** | PAUSED — resumes after the 2026-08-11 demo |
| **Site** | LiveORC server (AWS) |

**Paused 2026-08-10** with Phase 0 complete. The migration is destructive
by design and there is a demo on 2026-08-11, so the host stays on its
current configuration until there is slack. Until then the 26 GB of media
lives only in the container writable layer, so **`liveorc.service` must
stay disabled** and a root-volume snapshot is the standing safety net —
see the warning block at the top of the runbook.

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
- [x] Phase 0 — no `os.link`/`os.rename`/`shutil.move` anywhere in the
      application code, so `/liveorc/data` can stay on `/` and Phase 5b is
      not needed. The image ships `/liveorc/media/admin-interface`, making
      Phase 4's seed step mandatory. `liveorc.service` turned out to couple
      to the s3fs mount in five places, not one.
- [ ] **Snapshot the root EBS volume** — the 26 GB exists in exactly one
      place. Initiated 2026-08-10; **confirm it reached `completed`**, not
      `pending`, before relying on it.
- [x] `systemctl disable liveorc.service` (2026-08-10) — it runs
      `start-liveorc.sh` → `liveorc.sh start` → `docker compose up -d`,
      which recreates the webapp and destroys the writable layer, and the
      unit is `WantedBy=multi-user.target` so a reboot alone triggers it.
      Re-enable in Phase 6.
- [x] `docker update --restart unless-stopped rabbitmq` (2026-08-10). It
      was `restart=no` while `db` and `liveorc_webapp` were already
      `unless-stopped`, so a reboot would have brought the webapp up
      without its broker — video processing failing silently while the
      site looked healthy. `docker update` changes the policy in place
      and does not recreate the container.
- [x] Brought LiveORC up safely for the 2026-08-11 demo with
      `docker start db rabbitmq liveorc_webapp` (never `compose up`).
      Verified: video plays from the web UI.
- [ ] Phase 1: DB backup → `s3://openrivercam-video/backups/`.
- [ ] Phases 2–5: create/attach/format a 150 GiB gp3 volume at
      `/var/lib/liveorc-media`, seed image assets, copy the 26 GB,
      verify with a dry-run `rsync --itemize-changes`, snapshot.
- [ ] Phase 6: repoint **`start-liveorc.sh`'s `--storage-dir`** (the real
      control point — it overrides `.env`), the compose bind, and all five
      s3fs couplings in `liveorc.service`; retire the vestigial s3fs mount
      unit; re-enable the service.
- [ ] Phase 7: recreate, confirm the writable layer drops to MB and `/`
      falls to ~20 G; open an existing video and upload a new one.
- [ ] Add a disk-space alarm on `/` — its absence is why this ran
      undetected for ten weeks.
- [ ] Correct the false media-backup claim in
      `liveorc_server/reprocess/REPROCESS_RUNBOOK.md`.

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
