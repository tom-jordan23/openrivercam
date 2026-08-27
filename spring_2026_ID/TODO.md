# TODO — Indonesia Spring 2026 Deployment (post-trip)

**Last updated:** 2026-08-24

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
      ahead of it. The *technical* side is TODO-115: read-only API
      access is achievable natively (institute membership, no LiveORC
      changes), and that account model can be built and proven while
      this gate is still closed.
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

### TODO-115: Read-only LiveORC API access — the account model

| Field | Value |
|-------|-------|
| **Status** | **MODEL PROVEN 2026-08-25** (14 PASS / 0 FAIL) — partner provisioning still gated |
| **Site** | LiveORC server (AWS) |

**Verified against production 2026-08-25** with `verify-api-access.sh` and the
mirror account (`user_id 18`, institute **1**). Everything below that was read
from upstream source has now been observed on the running server:

- Reads resolve for an institute member; bare `GET /api/site/` really does
  return `[]` with a valid token, and `?institute=1` is mandatory.
- `PATCH` → **403**. `POST /api/video/` with an invalid payload → **400**,
  so the permission layer passes the request to validation without creating
  anything — the CREATE gap is confirmed by observation, not just by reading.
- `/api/recipe/` and `/api/device/` return `[]` as predicted.
- Access token lifetime is **360 minutes**; `/api/token/refresh/` works.
- Sites **2, 3 and 4 all belong to institute 1**, so one membership covers
  everything and the partner doc needs one id, not two.
- `creator` is **user 1** at site 4 and **user 3** at site 2 — two accounts,
  not one. Neither is the mirror account, which is what makes it read-only
  *by construction* rather than by policy.

**The DELETE probe is deliberately still unrun.** `PATCH` and `DELETE` share
one branch of `has_object_permission`, so the observed 403 on an empty-body
PATCH exercises the same predicate without being able to destroy a production
video. Now that the mirror exists it is safe to run:
`./verify-api-access.sh --institute 1 --site 4 --probe-delete --video-id <id>`.

IPB needs programmatic access to the data, and we need an account to pull
the backup mirror with (TODO-114). Both want the same thing: an account
that can **read everything and change nothing**. This TODO establishes
that account model, proves it against the running server, and writes down
what a partner needs to actually use it.

**The answer is yes, and it needs no change to LiveORC** — which matters,
because the standing rule is that nothing a version upgrade would
overwrite gets modified.

#### How LiveORC's permissions actually work

Read from the upstream source at tag **v0.3.0** (the deployed version;
`/api/version/` confirms 0.3.0 on Django 6.0.3 / Python 3.14.3). Upstream
has since tagged v0.3.1 — re-check this section on any upgrade.

`api/permissions.py` defines a single custom class, and
`api/views/base.py` applies it to every API viewset:

```python
class BaseModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrReadOnlyAsInstitute, IsAuthenticated]
```

`IsOwnerOrReadOnlyAsInstitute.has_object_permission`:

- **Safe methods** (`GET`/`HEAD`/`OPTIONS`) — allowed if
  `request.user.is_institute_member(obj.institute)` **or**
  `request.user == obj.creator`.
- **Everything else** (`PATCH`, `DELETE`) — allowed **only** if
  `obj.creator == request.user`.

So an account that is an institute member but did not create the records
gets read on the whole institute's data and **403 on every write**. That
is exactly the required behaviour, enforced upstream, for free.

`BaseModelViewSet.list()` adds a second gate: any nested `site_pk` route
returns **403** unless the caller is an institute member of that site (or
a superuser). So membership is what unlocks data, and non-membership is a
hard wall rather than an empty list.

#### The gap: CREATE is not covered

DRF invokes `has_object_permission` only from `get_object()` — i.e. on
**detail** routes. `IsOwnerOrReadOnlyAsInstitute` defines no
`has_permission`, so it defaults to `True`, and `POST` to a **collection**
is gated by `IsAuthenticated` alone. Any authenticated account can create:

| Route | Effect of a POST |
|---|---|
| `/api/video/` | **Uploads a video file and can enqueue a celery task** — `VideoViewSet.create()` calls `instance.create_task()` when the record is ready |
| `/api/site/` | Creates a site |
| `/api/site/{pk}/timeseries/` | Injects rows into the analytics series |
| `/api/site/{pk}/cameraconfig/`, `/crosssection/`, `/videoconfig/` | Creates calibration objects |
| `/api/recipe/`, `/api/device/` | Creates recipes / registers devices |

They still cannot **modify or delete** anything they did not create, so
existing data is safe. The exposure is additive: clutter, junk timeseries
rows, and — the sharp one — **disk writes plus celery load from
`POST /api/video/`**.

**Decision (2026-08-24): accept the gap, control it by timing.** Adding a
gateway to close it would mean another internet-facing service with its
own TLS and token rotation to own, for a partner-integrity risk rather
than a data-loss one. Instead, hand credentials to IPB only **after
TODO-112 lands**, so an accidental upload cannot threaten the root disk.
Revisit if the partner list grows beyond IPB.

#### Two traps

- **The `viewers` group does nothing.** `manage.py creategroups` builds
  `viewers`/`editors` groups carrying Django **model** permissions. These
  viewsets use `IsOwnerOrReadOnlyAsInstitute`, **not**
  `DjangoModelPermissions`, so group membership has **zero effect on the
  REST API**. It only affects `/admin/`, and only for `is_staff` users.
  Putting IPB in `viewers` looks like read-only access and grants nothing.
- **Never hand over the station credential.** The `creator` of every
  existing video is whichever account ORC-OS authenticated as at
  `/callback_url`. That account *can* delete them. IPB gets fresh users,
  always.

#### Onboarding gotchas to put in the partner doc

- `GET /api/site/` returns an **empty list** for a non-superuser unless
  `?institute=<id>` is supplied. A partner's first call looks like "there
  is no data". Give them the institute id up front.
- `/api/recipe/` and `/api/device/` return **empty / 404** for any
  non-superuser: both `get_queryset()` methods filter on `institute` and
  then fall through to `return queryset.none()`, so the filter branch is
  dead code upstream. Fail-safe, but it means recipe and device metadata
  are simply unavailable over the API. Camera configs and video configs
  are reachable per-site and carry the calibration that matters.
- Auth is JWT: `POST /api/token/` with email + password returns access +
  refresh; `POST /api/token/refresh/` renews. Confirm the access lifetime
  — a long pull will outlive one token.
- `/api/schema/` serves the full OpenAPI spec and needs no auth, so a
  partner can explore the surface before they have credentials.

**Steps:**

*Establish and prove the model — do this now*
- [ ] In `/admin/`, identify the institute that owns sites **2**, **3**
      and **4**, and record its id. Confirm sites 2/3/4 all belong to the
      same institute — if they do not, membership has to be granted per
      institute and the partner doc needs both ids.
- [ ] Find out which account is `creator` on the existing videos (the
      ORC-OS callback account) and confirm it is **not** shared with
      anyone. Note it in the password manager as station-only.
- [ ] Create the **mirror service account** for TODO-114: own user, not
      staff, not superuser, added as a `Member` of that institute.
      This is ours, not IPB's — it proves the model before any partner
      touches it.
- [ ] Run the verification matrix below against that account and record
      the actual results.

*Verification matrix — run against the mirror account, not an admin*

| Request | Expect | Proves |
|---|---|---|
| `POST /api/token/` | 200 + access/refresh | credential works |
| `GET /api/site/` | `[]` | the no-`?institute` gotcha is real |
| `GET /api/site/?institute=<id>` | the sites | membership resolves |
| `GET /api/site/4/video/` | 200, full list | `list()` institute gate passes |
| `GET /api/site/4/video/{id}/` | 200 | safe method + member |
| `GET /api/site/4/video/{id}/playback/` | video bytes | media is reachable |
| `PATCH /api/site/4/video/{id}/` | **403** | not creator |
| `DELETE /api/site/4/video/{id}/` | **403** | **the finding that matters** |
| `GET /api/site/4/timeseries/` | 200 | analytics readable |
| `DELETE /api/site/4/timeseries/{id}/` | **403** | not creator |
| `GET /api/recipe/` | `[]` | `queryset.none()` fall-through |
| `GET /api/site/{foreign}/video/` | 403 | non-member wall, if a foreign site exists |

- [ ] **Do not POST a real video to production to test the gap.** It is
      confirmed by source reading, and a test upload writes to the very
      disk this whole workstream is about. If you want it confirmed
      empirically, `POST /api/video/` with a deliberately **invalid**
      payload: a **400** proves the permission layer let you through
      without creating anything, a **403** would mean it did not.
- [ ] Record the matrix results in `liveorc_server/README.md` under a new
      "API access" section, alongside the permission explanation above.
      This is the durable artefact — the next person should not have to
      re-read upstream source to know what a partner account can do.

*Partner provisioning — gated, do not run early*
- [ ] Write the IPB-facing doc: base URL, token flow, the institute id,
      the endpoint list, the `?institute=` gotcha, and a worked `curl`
      example. Keep it in the repo; it contains no secrets.
- [ ] **Wait for both gates.** PMI approval (TODO-104 — Dan was explicit
      on the 2026-08-11 call that who gets access is PMI's decision) and
      TODO-112 complete (so `POST /api/video/` cannot threaten the root
      disk).
- [ ] Once both clear: create one user per IPB person — never a shared
      login — each `is_staff=False`, `is_superuser=False`, added as
      `Member` of the institute. Send credentials out of band.
- [ ] Re-run the verification matrix against **one real IPB account**
      before announcing access. Membership is the only thing standing
      between read-only and nothing, and it is set by hand.

---

### TODO-114: Pull an independent copy of LiveORC's data over the REST API

| Field | Value |
|-------|-------|
| **Status** | **DONE 2026-08-25** — complete media copy verified locally; TODO-112 gate released |
| **Sites** | LiveORC server (AWS) + workstation |

The 26 GB of media exists in exactly one place — `liveorc_webapp`'s
writable layer — and the only thing standing behind it is the root-volume
EBS snapshot from 2026-08-10. That snapshot is a real safety net, but a
*bad* one to have to use: recovering a single video from it means
launching an instance from the snapshot and digging through
`overlay2/<hash>/diff` to find files Django named. It is insurance you
cannot inspect, cannot test, and cannot restore from selectively.

> **Superseded approach.** The REST pull described below was replaced on
> 2026-08-25 after it took production down. Media is now exported host-side
> with `mirror/export-media-to-s3.sh`. See "What actually happened" further
> down before acting on anything in this section.

This TODO builds the copy you *can* inspect: pull site data down over
LiveORC's REST API to the workstation, where the files have names, the
inventory is a manifest you can diff, and nothing about the retrieval can
touch the container. Then TODO-112 runs against a known-good, verified
baseline instead of against nerve.

**It also does double duty.** IPB needs programmatic access to this data
anyway (TODO-104). Standing up API access properly — accounts, token
flow, what a non-admin account can and cannot do — is work that has to
happen regardless, and doing it first means the mirror *is* the test of
the access path IPB will later use.

**Why this is safe to run before TODO-112 — PARTLY WRONG, corrected
2026-08-25.** The claim below was that every step is an authenticated HTTP
GET, so it carries no risk to the writable layer. The *data* reasoning held:
reads never recreated a container, never invoked `docker compose`, never
touched `liveorc.service`, and nothing was lost. What it missed is that
"read-only" says nothing about **availability**. Bulk-reading media through
Django is expensive per byte, and running it against production took the host
down for ~90 minutes (ISS-FIELD-004). Safe for the writable layer is not the
same as safe for the service. Original reasoning follows:

> Every step is an authenticated HTTP GET against the running container.
> Reads do not recreate containers, do not invoke `docker compose`, and do
> not touch `liveorc.service` — the three things the runbook's warning block
> is about. This is the one substantial piece of TODO-112 preparation that
> carries no risk to the writable layer. See the hazard note on `/` below
> for the one thing that does need watching.

**What the API exposes** — verified 2026-08-24 by unauthenticated probe
against `https://openrivercam.endlessprojects.info`. Public HTTPS is up,
LE cert valid (expires 2026-11-08, see TODO-102 notes), version
**0.3.0** on Django 6.0.3 / Python 3.14.3.

| Endpoint | Gives you |
|---|---|
| `/api/schema/` | Full OpenAPI 3.0.3 spec, **readable without auth** |
| `/api/version/` | Version; the only anonymous data endpoint |
| `/api/token/`, `/api/token/refresh/` | JWT access + refresh pair from username/password |
| `/api/site/` | Site list — id, name, coordinates |
| `/api/site/{pk}/video/` | **The manifest.** Each `Video` carries `file`, `keyframe`, `image`, `thumbnail` as URIs, plus `timestamp`, `status`, `video_config`, `time_series` |
| `/api/site/{pk}/video/{id}/playback|image|thumbnail/` | The bytes |
| `/api/site/{pk}/timeseries/` | `h`, `q_05`/`q_25`/`q_50`/`q_75`/`q_95` per timestamp — the analytics output |
| `/api/site/{pk}/cameraconfig/`, `/crosssection/`, `/videoconfig/` | The calibration that makes the numbers reproducible |
| `/api/recipe/`, `/api/device/` | Processing recipes; registered devices |

`/api/site/`, `/api/site/4/video/` and `/api/site/4/timeseries/` all
return **401** unauthenticated — the API is not leaking, and the mirror
needs a real credential.

**Known site ids** (from the reprocess work, LiveORC 0.3.0): Sukabumi =
**4** ("Sukabumi City", 1165 videos), Jakarta = **3**, and site **2**
("Test site", 1255 videos) which is *probably* early Sukabumi captures.
Mirror all of them — the whole point is not having to decide later what
mattered.

**`DELETE` on the same URL as `GET` — resolved, see TODO-115.** The
schema declares `delete` on `/api/site/{site_pk}/video/{id}/` under the
same security block as the read, which looked alarming. Reading the
v0.3.0 source settled it: writes require `obj.creator == request.user`,
so a non-creator account gets 403. The mirror account creates nothing and
is therefore structurally incapable of deleting anything. The mirror
script should still issue no verb but `GET` — belt and braces, and it
keeps the script honest if the permission model ever changes upstream.

**Hazard — watch `/` during the pull.** The failure being guarded against
here is a full root disk, and the mirror pulls 26 GB through Django and
nginx on a host whose `/` sits at 62% with ~30 G free. Streaming
responses should not spool to disk, but "should not" is exactly the
assumption that produced this incident. Keep a `df -h /` running in a
second Session Manager pane for the first site, throttle the client, and
stop if free space moves. The instance is a t3.large — sustained transfer
will also draw down CPU credits, so pace it rather than saturating.

#### What actually happened — read this before the design notes below

The REST pull in this TODO **took production down** on 2026-08-25 after 773 of
2630 files (see ISS-FIELD-004). It was replaced by a host-side export. The
design notes that follow are kept for the reasoning, but several of their
premises were wrong:

| Assumed | Measured 2026-08-25 |
|---|---|
| ~1165 video records | **3176** across sites 2/3/4 — 2630 at site 4, 546 at site 2, 0 at site 3 |
| media fetched from the serializer's `file` URL | those URLs **404 with and without a JWT** — media is in MinIO behind Django's storage API, never on the nginx filesystem |
| all assets reachable over REST | **no `/keyframe/` action exists** — 1.4 GB of keyframes are unreachable by REST at any effort |
| site 2 holds media | site 2 has **no video files at all** (`file` null for all 546); all 29 GB is site 4 |

Bytes are served by the DRF actions `/playback/`, `/image/` and `/thumbnail/`.
The dead `file` URLs remain useful as **identifiers**: their paths give the
storage-relative layout the reprocessor needs on disk locally.

**The route that worked** — `mirror/export-media-to-s3.sh` on the host streams
`docker exec … tar -cf -` straight into `aws s3 cp -`, throttled, touching
neither Django nor host disk; `mirror/fetch-media-from-s3.sh` then pulls from
S3 with no load on LiveORC at all. 30 GB moved in 61 minutes.

It is also **more complete than this TODO's original design could have been**:
it captures the 1.4 GB of keyframes REST cannot serve, and 88 keyframe + 88
thumbnail files that exist on disk with a null database field.

#### Reconciliation — the question this TODO existed to answer

`videos/` holds **4463** files against 2630 records. Fully explained: LiveORC
stores velocimetry analysis images under `videos/` alongside the mp4s, and
exactly **1833** records have a non-null `image`. 2630 + 1833 = 4463, and
2630 × 9.2 MB + 1833 × 2.8 MB ≈ 29 GB against the measured 29 G.

**So the API accounts for everything of substance on disk.** The only real gap
is the 88 orphaned keyframe/thumbnail files noted above.

**Local mirror, verified 2026-08-25** — `data/liveorc-mirror/4/media`:

| Directory | Files | Size |
|---|---|---|
| `videos` | 4463 (2630 mp4 + 1833 jpg) | 29 G |
| `keyframe` | 2630 | 1.4 G |
| `thumb` | 2630 | 11 M |

Every file was checked against a host-generated list by name **and size** —
the check that catches a truncated tar, which a matching sha256 cannot, since
a short stream produces a valid tar whose checksum agrees at both ends. A
sample was then re-checksummed against the API-pulled hashes from the partial
REST pull: two independent transports agreeing on the same bytes.

**Still outstanding:** a fresh DB dump. `backup_liveorc_db.sh` has not been run
since the S3 copies of 2026-06-26/29, and without it these videos cannot be
reprocessed — `build_staging_local.sh` needs the Fit 6 `VideoConfig`,
camera_config and both cross-sections including `cross_section_wl`.

**Design notes:**

- **No pagination, no filters.** `site_video_list` declares no `page`,
  `limit`, or date parameters and returns a bare `array` of `Video`. So
  the list call may return all 1165 records in one response, and
  resumability has to be **client-side**: write the manifest to disk
  first, then work down it, skipping what already exists with a matching
  size. Never re-list to resume.
- **`file` is nullable.** Both stations run "LiveORC sync: time series +
  analysis images", with full-video upload disabled, so some records will
  legitimately have no video. Record them as null in the manifest rather
  than treating them as failures — the count of nulls is itself a result.
- **The manifest is the deliverable, not just the bytes.** A per-site
  JSON of every video id, timestamp, status, asset URLs and byte sizes is
  what makes TODO-112 Phase 5's `rsync --itemize-changes` checkable
  against something external. Right now that verification only compares
  the host to itself.
- **The mirror does not cover everything.** Be explicit about this in the
  README so it is never mistaken for a full backup: it captures media and
  the API-visible records, **not** the Postgres database (TODO-112
  Phase 1 does that, to `s3://openrivercam-video/backups/`), not
  `/liveorc/media/admin-interface`, and not the TimescaleDB sensor data,
  which is a separate stack entirely and reachable via Grafana.
- **Land it in `data/`,** which is already gitignored at the repo root.
  This repo is public — no manifest, token, or media file gets committed.
  610 G free on the workstation, so 26 GB is not a constraint.
- **The mirror account is ours, not IPB's.** See the ordering constraint
  below.

**Steps:**

*Phase 0 — access, before any bytes move*
- [ ] **Done in TODO-115**: create the mirror service account and run the
      verification matrix. The mirror runs as that account — an institute
      member that created nothing, so upstream's
      `IsOwnerOrReadOnlyAsInstitute` makes it read-only by construction.
      Do not start the pull until that matrix has actually been run.
- [ ] Confirm the access token's lifetime and that `/api/token/refresh/`
      works — a 26 GB pull will outlive one token, so the client needs
      refresh built in from the start rather than bolted on after a
      mid-pull 401.
- [ ] Note the institute id; `GET /api/site/` returns `[]` without
      `?institute=<id>`, which would otherwise look like an empty server.

*Phase 1 — inventory, no downloads*
- [ ] `GET /api/site/` and record every site id, not just 2/3/4.
- [ ] For each site, pull the video list and the timeseries list and
      write `data/liveorc-mirror/<site>/manifest.json`.
- [ ] Summarise: video count, how many have a null `file`, total bytes
      by asset type. **Reconcile against the runbook's 26 GB video /
      1.3 GB keyframe / 9.5 MB thumb figures.** A large gap here is
      information, not an error — it would mean the API does not see
      everything on disk, which changes what the mirror is worth.

*Phase 2 — the pull*
- [ ] Write `liveorc_server/mirror/orc_mirror.py` and commit it. Follow
      the repo conventions: `--check`/dry-run default, resumable,
      rate-limited, `--site` scoping, structured log. Read-only by
      construction — it issues **no** verb but `GET` and the one `POST`
      to `/api/token/`.
- [ ] Run it against the smallest site first, verify, then the rest.
      Watch `df -h /` on the host throughout the first site.
- [ ] Record per-file size and a checksum in the manifest as each file
      lands.

*Phase 3 — prove the copy is good*
- [ ] Re-run in `--check` mode: every manifest entry present, sizes
      match, nothing missing.
- [ ] Spot-check playability — open several mirrored videos locally,
      spread across the date range, including one from each site and one
      from either end of the 2026-05-14 → 2026-07-29 accumulation window.
- [ ] Confirm the timeseries JSON matches the analytics baseline in
      `liveorc_server/reprocess/`'s `api_timeseries.csv` where they
      overlap.
- [ ] Write `data/liveorc-mirror/README.md` (untracked, alongside the
      data) stating what the mirror contains, what it does **not**, and
      the restore path.

*Phase 4 — release the gate*
- [ ] Update TODO-112's status to note the verified independent copy
      exists, and proceed with Phase 1 there.

**Ordering constraint — do not let this provision IPB.** TODO-104 records
Dan's explicit position from the 2026-08-11 call: who gets LiveORC access,
and when, is **PMI's decision**, and nothing is to be provisioned ahead of
that approval. The mirror account created in Phase 0 is an *operational
account of ours*, for pulling our own backup — it is not IPB access and
does not touch that gate. Keep the two separate: this TODO builds and
proves the access path, TODO-104 decides who else walks down it. The
useful handoff to TODO-104 is the Phase 0 findings — the token flow, the
DELETE answer, and what a non-admin account can actually reach.

**Still to run this while Sukabumi is offline.** TODO-112 notes the media
tree is static because uploads stopped 2026-08-14. That helps here too: a
manifest captured against a static tree stays valid, so Phase 1's
inventory can be trusted as a baseline through Phase 3. If the station
comes back before this finishes, re-run Phase 1 and diff.

---

### TODO-112: Move LiveORC media onto a dedicated EBS volume

| Field | Value |
|-------|-------|
| **Status** | READY TO RUN — gate released 2026-08-25, but **re-scope first** (see below) |
| **Site** | LiveORC server (AWS) |

**Gate released (2026-08-25).** TODO-114 delivered a complete, independently
verified copy of all 30 GB of media to `data/liveorc-mirror/`, checked file by
file against a host-generated list. Phase 5's `rsync --itemize-changes` now has
something external to be checked against.

**Two premises of this TODO are no longer true. Re-read before running.**

**1. The media tree is NOT static.** This TODO says uploads stopped 2026-08-14
and sequences itself *before* the station fix on that basis — "with no uploads
arriving, `rsync --itemize-changes` in Phase 5 means exactly what it says."
Sukabumi came back on **2026-08-20**: 1 file that day, then 45, 43, 9 and 6,
newest `created_at` **2026-08-24T21:32Z**, 104 new mp4s after the stated
cutoff. Normal cadence is 45–48/day, so 08-23 and 08-24 were degraded and it
has been quiet since — but the race this TODO was sequenced to avoid is open
again. Re-run the TODO-114 inventory and diff immediately before any Phase 5
rsync; do not trust a manifest across a gap of days.

**2. `/mnt/s3-storage` is residue, not a repair target.** I suggested on
2026-08-25 that fixing that mount might be shorter than this migration. That
was wrong, and the runbook already answers it — see "Why EBS and not S3" in
`MEDIA_VOLUME_RUNBOOK.md`. S3 was tried first and abandoned for two reasons
that still hold: LiveORC's storage backend is all-or-nothing (prod runs
`FileSystemStorage`, and `prod_reprocess.sh` execs inside the webapp precisely
to read the *local* media volume), and `rename(2)`/`link(2)` fail with `EXDEV`
across a mount boundary, with s3fs having no hardlink support at all.

The dead `mnt-s3\x2dstorage.mount` is the **leftover of that abandoned
migration**, deliberately left pointing somewhere harmless. Its failure is not
why media went to the writable layer. The actual cause is in the runbook's root
cause section: `MEDIA_ROOT` is `/liveorc/media`, and the compose bind pointed at
`/liveorc/data/media` — a path Django never writes to. Nothing was mounted where
it mattered, so writes succeeded into the container layer, silently.

Two things do follow from the mount being dead, and both are worth keeping:

- `liveorc.service` requires it, so the unit cannot start while it fails. That
  is a second interlock behind the `systemctl disable` this runbook mandates —
  and it disappears in Phase 9 when the unit is re-enabled.
- The `RequiresMountsFor` guard that Phase 6 adds must point at
  `/var/lib/liveorc-media`, **not** the old S3 path. The unit currently
  guards the wrong mount, which is landmine #2 in the runbook.

**Unpaused 2026-08-17.** The 2026-08-11 demo it was waiting on has passed
and Phase 0 is fully resolved, including the three files that were still
unread. Until Phase 6 lands the 26 GB of media lives only in the container
writable layer, so **`liveorc.service` must stay disabled** and a
root-volume snapshot is the standing safety net — see the warning block at
the top of the runbook.

**Run this before the station fix.** Decided 2026-08-26: LiveORC storage
first, station issues after. The reason originally given here — uploads
stopped 2026-08-14, so the media tree is static and Phase 5's
`rsync --itemize-changes` means exactly what it says — is **no longer
true**; Sukabumi resumed on 2026-08-20 (premise 1 above). The ordering
stands on its own reasoning: the 26 GB in the writable layer is what is at
risk, and every further day of uploads adds to what an accidental recreate
would destroy.

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
- [x] **Snapshot the root EBS volume** — the 26 GB exists in exactly one
      place. Initiated 2026-08-10, confirmed complete 2026-08-17. This was
      the gate on everything destructive downstream.
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
- [x] Phase 1: DB backup → `s3://openrivercam-video/backups/` (2026-08-27,
      `20260827-125253`, 3488 ts rows / 3189 video rows). The bucket prefix
      was **empty** beforehand — three earlier backups had never left the
      host disk. All four are now off-host.
- [x] Phases 2–5 (2026-08-27): 150 GiB gp3 volume created, attached, ext4,
      mounted at `/var/lib/liveorc-media` by LABEL. Seeded `admin-interface`,
      copied **31 GB / 9775 files** out of the writable layer. Gate passed —
      counts identical both sides, dry-run `--itemize-changes` empty. Media had
      grown 26→31 GB, and mp4s 2630→2643, so uploads are still arriving.
- [x] Snapshot the media volume — `liveorc-media pre-cutover 2026-08-27`,
      completed. First time the 31 GB has existed in two places; this is
      what makes Phase 7 reversible.
- [x] Read the three Phase 6 inputs (2026-08-17). `start-liveorc.sh` passes
      `--storage-dir /mnt/s3-storage` and is a **local wrapper, not
      upstream**, so it is safe to edit. `verify-s3mount.sh` does a write
      test as well as a mountpoint check — rewrite and rename it rather
      than dropping it. `grep -rn "s3-storage"` **undercounts**: `After=`
      and `Requires=` use the escaped form `mnt-s3\x2dstorage.mount`, so
      use `grep -n 's3' /etc/systemd/system/liveorc.service` (5 hits).
- [x] Settled how the compose bind changes (2026-08-17). An override file
      is **not** an option: `liveorc.sh` builds an explicit `-f` list
      (`docker-compose.yml` plus rabbitmq/postgis/spatialite/ssl), and
      Compose auto-loads `docker-compose.override.yml` only when no `-f` is
      given. So the destination fix goes in
      `/opt/LiveORC/docker-compose.yml:8` directly — upstream-owned, and a
      LiveORC upgrade will revert it. The durable defense goes in
      `start-liveorc.sh`, which is a local wrapper: a pre-flight grep that
      refuses to start if the bind was reverted, and a post-start
      `docker inspect` that verifies the mount table rather than the config.
- [ ] Phase 6: repoint **both halves of the path** — `start-liveorc.sh`'s
      `--storage-dir` (the source, and the real control point since it
      overrides `.env`) **and** the compose bind's destination
      (`/liveorc/data/media` → `/liveorc/media`). Changing only the first
      completes cleanly, verifies green, and leaves media in the writable
      layer exactly as now. Then fix all five s3fs couplings in
      `liveorc.service`, retire the vestigial s3fs mount unit, and
      re-enable the service.
- [ ] Confirm the result in the **running container**, not the config:
      `docker inspect liveorc_webapp --format '{{range .Mounts}}…'` must
      show `/var/lib/liveorc-media -> /liveorc/media`.
- [ ] Phase 7: recreate with **`systemctl start liveorc.service`**, never a
      bare `docker compose up -d` — that bypasses `start-liveorc.sh`, so no
      `--storage-dir` is passed and neither guard runs, and
      `LORC_STORAGE_DIR` silently falls back to `.env`'s `lorc_media` named
      volume. Confirm the writable layer drops to MB and `/` falls to
      ~20 G; open an existing video and upload a new one.
- [ ] Phase 9: `systemctl enable liveorc.service` — disabled since
      2026-08-10 so a reboot could not destroy the media. Safe once media
      is on the volume, and leaving it disabled means LiveORC silently does
      not come back after a reboot.
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

   ### TODO-116: Witty Pi restart resiliency — a missed boot leaves the station down

    | Field | Value |
    |-------|-------|
    | **Status** | OPEN — captured 2026-08-25, not started |
    | **Site** | Both stations (Witty Pi scheduling) |

    The station periodically misses a boot cycle — battery is the leading
    suspect — and does not recover on its own. The failure mode is the
    scheduler, not the power event: once a boot is missed, the Witty Pi's
    "next start time" is left in the **past**, and nothing re-arms it. The
    station stays down until someone physically pushes the button.