# LiveORC server-side additions

Services that run alongside LiveORC on the same EC2 host **without modifying
LiveORC's container or config**:

- **`sensor-upload/`** — FastAPI endpoint receiving sensor CSV uploads from
  Pi stations. Terminates TLS directly on port 8443 with a self-signed
  certificate. Authenticated via per-station bearer token. Writes files
  atomically under `/var/orc/sensors/<station>/`.
- **`sensor-ingest/`** — Python watcher that polls `/var/orc/sensors/*.csv`
  every 30 s and upserts parsed rows into the TimescaleDB hypertable.
  Idempotent (composite unique key per `(ts, station, sensor, metric)`).
- **`timescale`** — TimescaleDB instance backing the sensor time-series.
- **`grafana`** — UI at port 9443 with anonymous viewer access (admin
  login required for editing). Reuses the same self-signed cert.
- **`sheets-export/`** — hourly job that appends un-exported rows from the
  TimescaleDB `sensor_readings` table to a Google Sheet, so stakeholders can
  read the data without a login or a self-signed-cert warning. Pure consumer:
  it never writes to `sensor_readings`. See
  [§ Google Sheets export](#google-sheets-export).
- **`reprocess/`** — one-off toolkit to re-derive historical Sukabumi
  `time_series` with a corrected camera config (re-detects optical water
  level, overwrites in place). Backup/restore + a free **local** staging
  build + before/after analytics. Start at
  [`reprocess/REPROCESS_RUNBOOK.md`](reprocess/REPROCESS_RUNBOOK.md).

## Architecture

```
Pi station --HTTPS PUT :8443--> orc-sensor-upload container
    (curl --cacert pinned)        - uvicorn terminates TLS
                                  - 10-year self-signed cert (NOT a public CA)
                                  - writes to /var/orc/sensors/<station>/
                                            |
                        orc-sensor-ingest (30s poll, upsert)
                                            |
                                            v
                                  timescale: sensor_readings
                                       |            |
                          orc-grafana :9443    orc-sheets-export (hourly)
                                                    |  anti-join vs sensor_exports
                                                    v
                                            Google Sheet (append-only)
```

**Why self-signed?** LiveORC's letsencrypt volume turns out to be empty
(LiveORC writes certs to a container-internal path that isn't on the
persistent volume), so we can't share their cert. Getting our own LE cert
would require either coordinating port 80 with LiveORC for HTTP-01 or
adding a DNS-01 plugin with API credentials — neither is worth the
complexity for an internal Pi→server channel. Self-signed + Pi-side
pinning gives us TLS without the renewal or coupling cost.

The Pi pins against our cert via `curl --cacert`, so MITM with a
public-CA-issued cert for our hostname won't work either.

**LiveORC is untouched.** Its container, nginx, port mappings, network,
volumes — all unchanged. We share only the host EC2 instance.

## First-time deployment

### 1. Get this directory onto the server

```bash
# If you have the repo cloned (on this host it is ~/code/git/openrivercam):
sudo mkdir -p /opt/orc-additions
sudo rsync -a --exclude='.env' --exclude='certs/' --exclude='secrets/' \
    ~/code/git/openrivercam/spring_2026_ID/liveorc_server/ /opt/orc-additions/
sudo find /opt/orc-additions -path /opt/orc-additions/secrets -prune -o \
    -exec chown $USER:$USER {} +
cd /opt/orc-additions
```

**Do NOT use `rsync --delete`** — it would wipe `.env`, `certs/`, and
`secrets/` on the server (all three are server-local, not in the repo). The
`--exclude` flags are belt-and-braces in case someone forgets.

**Do not `chown -R` over `secrets/`.** The Sheets service-account key must
stay `1001:1001` — `chown`ing it to your login user makes `sheets-export`
fail at startup with `PermissionError`. This bites on *re*-deploys, not the
first one. `chown` has no `--exclude` flag, which is why the command above
uses `find ... -prune`. If you ever run a plain `chown -R` by habit,
re-assert the key's ownership afterwards:

```bash
sudo chown 1001:1001 /opt/orc-additions/secrets/sheets-sa.json
sudo chmod 0400      /opt/orc-additions/secrets/sheets-sa.json
```

### 2. Generate the self-signed cert

```bash
sudo ./bootstrap-cert.sh
```

This creates `/opt/orc-additions/certs/{fullchain,privkey}.pem` with a
10-year validity. The script refuses to overwrite an existing cert.

### 3. Commit the public cert to the repo

The Pi side needs to pin against this cert. Copy the public half (NOT the
private key) into the repo:

```bash
cp /opt/orc-additions/certs/fullchain.pem \
   ~/code/git/openrivercam/spring_2026_ID/pi/shared/etc/orc/sensor-upload-ca.pem
cd ~/code/git/openrivercam && git add spring_2026_ID/pi/shared/etc/orc/sensor-upload-ca.pem
git commit -m "Add self-signed CA cert for sensor-upload (Pi-side pinning)"
git push
```

The cert is a public artifact — committing it is fine. The private key
stays on the server and is gitignored.

### 4. Generate per-station tokens

```bash
python3 -c 'import secrets; print("sukabumi:" + secrets.token_urlsafe(32))'
python3 -c 'import secrets; print("jakarta:"  + secrets.token_urlsafe(32))'
```

Store **each token in the password manager**.

### 5. Create `.env`

```bash
cp .env.example .env && chmod 600 .env
$EDITOR .env   # paste the comma-separated station:token pairs
```

`.env` is gitignored. Never commit it.

### 6. Create the upload directory on the host

```bash
sudo mkdir -p /var/orc/sensors
sudo chmod 0755 /var/orc/sensors
# Container runs as root and writes here directly — no chown needed.
```

### 7. Open AWS Security Group for ports 8443 + 9443

In the EC2 console → Security Groups → SG attached to the LiveORC instance,
add two inbound rules:

| Port | Description |
|------|-------------|
| `8443` | `orc-sensor-upload (station CSV ingest)` |
| `9443` | `orc-grafana (public read-only dashboards)` |

Both: Type `Custom TCP`, Source `0.0.0.0/0` (public dashboards are an
explicit design choice — see disclaimer banner on every dashboard).

### 8. Bring up the service

```bash
sudo docker compose --env-file .env up -d --build
sudo docker ps --filter name=orc-sensor-upload
sudo docker logs orc-sensor-upload --tail 20
```

Expect to see `loaded tokens for stations: ['jakarta', 'sukabumi']` and
`Uvicorn running on https://0.0.0.0:8443`.

### 9. Smoke test Grafana

Browser → `https://openrivercam.endlessprojects.info:9443/`. You'll see a
browser cert warning (self-signed). Accept the risk; you'll land on the
Grafana home page in anonymous viewer mode. The "Station overview"
dashboard should be available under "Browse → ORC station dashboards".

The disclaimer banner at the top of every dashboard is **mandatory and
non-removable** — see `memory/project_grafana_disclaimer.md`. If you add
new dashboards, copy the banner panel as the first row.

Admin login (to edit dashboards) is at `/login` with `orc-admin` and the
password from `.env`.

### 10. Smoke test sensor-upload from the open internet

```bash
TOKEN=<paste sukabumi token>
SERVER_CERT=~/code/git/openrivercam/spring_2026_ID/pi/shared/etc/orc/sensor-upload-ca.pem

curl --cacert "$SERVER_CERT" -sS \
    https://openrivercam.endlessprojects.info:8443/sensors/health
# Expect: {"ok":true,"stations":["jakarta","sukabumi"]}

echo "ts,value
$(date -u +%FT%TZ),42" | curl --cacert "$SERVER_CERT" -sS -X PUT \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: text/csv" \
    --data-binary @- \
    https://openrivercam.endlessprojects.info:8443/sensors/upload/sukabumi/smoke-$(date -u +%FT%TZ).csv
# Expect: {"ok":true,...}

sudo ls -la /var/orc/sensors/sukabumi/
```

`--cacert` is required because the cert is self-signed. Without it, curl
refuses to connect with `unable to get local issuer certificate`.

## Google Sheets export

`sheets-export` appends rows from `sensor_readings` to a Google Sheet once an
hour, in long format: `ts, station, sensor, metric, value`. Grafana is the
better tool for looking at this data; the sheet exists so people who will
never log into Grafana (and shouldn't have to click through a self-signed
cert warning) can filter and chart it themselves.

**Why a service account?** The alternatives are worse. OAuth user credentials
tie the export to one person's Google account and a refresh token that can be
revoked out from under the job. An Apps Script pulling from our side would
mean exposing another authenticated endpoint to the internet, and Google's
fetcher won't accept our self-signed cert. A service account is a
non-human identity with access to exactly one document, granted by sharing
that document — no IAM roles, no Drive scope, nothing to revoke by accident.

**Why no `ts` watermark?** Because sensor CSVs backfill. In July 2026 weeks of
stalled uploads were replayed (TODO-103), inserting rows with old `ts` values
long after newer rows existed. A `max(ts)` cursor would have silently skipped
every one. Instead a ledger table, `sensor_exports`, records what has been
exported and the query is an anti-join. Regression check — run these two
against the live database; the first is what the naive design would have
found, the second is what actually gets exported:

```sql
SELECT count(*) AS naive_ts_cursor_would_export
FROM sensor_readings
WHERE ts > (SELECT max(ts) FROM sensor_exports);

SELECT count(*) AS antijoin_will_export
FROM sensor_readings r
WHERE NOT EXISTS (
    SELECT 1 FROM sensor_exports e
    WHERE e.ts=r.ts AND e.station=r.station
      AND e.sensor=r.sensor AND e.metric=r.metric);
```

After a backfill the first returns `0` while the second returns the real
count. **Never prune `sensor_exports` — it *is* the cursor.** Deleting rows
from it re-exports them.

### 1. Create the spreadsheet (a human, not the service account)

A service account has no Drive storage quota, so it cannot usefully own
files. Create the sheet yourself. A Shared Drive is the better long-term home
— it survives the creating account being deleted — but a personal Drive is
fine to start, since the target is one `.env` variable and repointing costs a
restart.

1. Rename the first tab to `readings`.
2. Header row `A1:E1`: `ts`, `station`, `sensor`, `metric`, `value`.
3. **Disclaimer in `G1`.** Paste the text below into that single cell
   (Alt+Enter for line breaks), widen column G, enable text wrapping, and
   freeze row 1 (`View > Freeze > 1 row`). One wrapped cell rather than three
   so that freezing row 1 alone keeps the whole notice on screen without also
   freezing data rows. Appends are pinned to `A:E` and land at the bottom, so
   column G is never touched or shifted.

   > ⚠️ RESEARCH PROJECT — NOT an official Indonesian government weather
   > station. This data is not authoritative and must not be used for
   > emergency response, planning, or official reporting. For official
   > information see bmkg.go.id (weather) and bnpb.go.id (disaster
   > management).
   >
   > Proyek penelitian — bukan stasiun cuaca resmi pemerintah Indonesia.

   This mirrors the mandatory Grafana dashboard banner. The sheet is another
   public-facing surface for the same data, so it carries the same notice.
4. `File > Settings > Time zone` → **UTC**. Not optional: timestamps are
   written as UTC wall-clock strings, and a non-UTC sheet renders every one of
   them shifted. The service logs a warning at startup if it detects this.

### 2. Create the service account

1. Google Cloud console → select or create a project.
2. Enable the **Google Sheets API** (`sheets.googleapis.com`).
3. IAM & Admin → Service Accounts → Create. **Grant it no project IAM roles**
   — Sheets access is per-document, not IAM.
4. Keys → Add key → Create new key → **JSON** → download.
5. Copy the `client_email` value out of the JSON
   (`<name>@<project>.iam.gserviceaccount.com`).

If the organisation enforces `iam.disableServiceAccountKeyCreation`, that
policy has to be waived for the project — find out before you need it.

### 3. Share the sheet with the service account

Share → paste the `client_email` → role **Editor** → **uncheck "Notify
people"**. The service account has no mailbox, and the notification email can
fail the whole share.

### 4. Install the key on the server

The key file is server-local and gitignored, exactly like `certs/`. There is
no public half — none of it is ever committed.

```bash
# On your workstation — single line survives a browser-terminal paste intact:
base64 -w0 ~/Downloads/<project>-<hash>.json
```

Then in the Session Manager shell on the server:

```bash
sudo mkdir -p /opt/orc-additions/secrets
sudo tee /opt/orc-additions/secrets/sheets-sa.json.b64 >/dev/null <<'EOF'
<paste the single base64 line here>
EOF
sudo base64 -d /opt/orc-additions/secrets/sheets-sa.json.b64 \
    | sudo tee /opt/orc-additions/secrets/sheets-sa.json >/dev/null
sudo rm /opt/orc-additions/secrets/sheets-sa.json.b64

# The container runs as uid 1001 (non-root, unlike sensor-upload and grafana).
# Skip this and every startup fails with PermissionError.
sudo chown 1001:1001 /opt/orc-additions/secrets/sheets-sa.json
sudo chmod 0400      /opt/orc-additions/secrets/sheets-sa.json
```

### 5. Configure and bring up

Add the spreadsheet ID (the `/d/<ID>/` segment of the sheet URL) to `.env`:

```bash
echo 'SHEETS_SPREADSHEET_ID=<id>' | sudo tee -a /opt/orc-additions/.env
```

Dry-run the access check first — `preview` neither appends nor marks, so it
is safe to run against production:

```bash
cd /opt/orc-additions
sudo EXPORT_MODE=preview docker compose --env-file .env up -d --build sheets-export
sudo docker logs orc-sheets-export --tail 20
```

Expect `sheet ok title=... tz=Etc/UTC` and a `PREVIEW would export rows=N`
line. If instead you see `cannot access spreadsheet`, the sheet is not shared
with the service account. Then switch to live:

```bash
sudo docker compose --env-file .env up -d sheets-export
sudo docker logs -f orc-sheets-export
```

The first run backfills all history (~130k rows as of August 2026) in batches
of 2000, taking a few minutes. Steady state is ~60 rows/hour.

## API access

Established and verified 2026-08-25 (TODO-115). Base URL
`https://openrivercam.endlessprojects.info`, LiveORC **v0.3.0**.

### How permissions actually work

`api/permissions.py` defines one class, applied to every viewset in
`api/views/base.py`:

```python
permission_classes = [IsOwnerOrReadOnlyAsInstitute, IsAuthenticated]
```

- **Safe methods** (`GET`/`HEAD`/`OPTIONS`) — allowed if the user is an
  institute member of the object's institute, **or** is its creator.
- **Everything else** (`PATCH`, `DELETE`) — allowed **only** if
  `obj.creator == request.user`.

So an account that is an institute **Member** but created nothing gets read on
the whole institute's data and 403 on every write. That is the read-only model,
enforced upstream, needing no change to LiveORC.

`BaseModelViewSet.list()` adds a second gate: nested `site_pk` routes return
**403** to non-members, so non-membership is a wall rather than an empty list.

**The gap: CREATE is not covered.** DRF calls `has_object_permission` only from
`get_object()`, i.e. on detail routes. The class defines no `has_permission`, so
`POST` to a *collection* is gated by `IsAuthenticated` alone. Any authenticated
account can create — including `POST /api/video/`, which writes a file and can
enqueue a celery task. Existing data is safe (no modify, no delete), but the
exposure is additive.

### Two traps

- **The `viewers` group does nothing.** `manage.py creategroups` builds groups
  carrying Django *model* permissions. These viewsets use
  `IsOwnerOrReadOnlyAsInstitute`, **not** `DjangoModelPermissions`, so group
  membership has zero effect on the REST API. It affects `/admin/` only.
- **Never hand over a station credential.** The `creator` of existing videos is
  whichever account ORC-OS authenticated as — user **1** at site 4, user **3**
  at site 2. Those accounts *can* delete those records. Partners get fresh
  users, always.

### Verification matrix — measured, not assumed

Run against the mirror account (`user_id 18`, institute 1), 14 PASS / 0 FAIL:

| Request | Expected | Actual |
|---|---|---|
| `POST /api/token/` | 200 + access/refresh | 200 |
| `GET /api/site/` (no `?institute`) | `[]` | `[]` |
| `GET /api/site/?institute=1` | the sites | 2, 3, 4 |
| `GET /api/site/4/video/` | 200 | 200 |
| `GET /api/site/4/video/{id}/` | 200 | 200 |
| `GET .../video/{id}/playback/` | 200 | 200 |
| `GET .../video/{id}/thumbnail/` | 200 | 200 |
| `GET /api/site/4/timeseries/` | 200 | 200 |
| `GET /api/site/4/cameraconfig/` | 200 | 200 |
| `GET /api/site/4/videoconfig/` | 200 | 200 |
| `GET /api/site/4/crosssection/` | 200 | 200 |
| `GET /api/recipe/` | `[]` | `[]` |
| `PATCH .../video/{id}/` (empty body) | **403** | **403** |
| `POST /api/video/` (invalid payload) | **400** | **400** |

That 400 is the important one: the permission layer let the request through to
validation without creating anything, confirming the CREATE gap by observation.

`DELETE` is **not** in the run above, deliberately — see `verify-api-access.sh`.

Re-run it any time, and against every new partner account before announcing
access:

```bash
export LIVEORC_EMAIL='...'
read -rs LIVEORC_PASSWORD && export LIVEORC_PASSWORD
./verify-api-access.sh --institute 1 --site 4
```

### Onboarding gotchas for a partner doc

- `GET /api/site/` returns **`[]`** for a non-superuser without
  `?institute=<id>`. A partner's first call looks like an empty server. Give
  them the institute id (**1**) up front.
- `/api/recipe/` and `/api/device/` return empty for any non-superuser — both
  `get_queryset()` methods fall through to `queryset.none()`. Recipe and device
  metadata are simply unavailable over REST. Camera configs and video configs
  *are* reachable per-site and carry the calibration that matters.
- Auth is JWT: `POST /api/token/` with **email** + password (not username).
  Access tokens last **360 minutes**; `/api/token/refresh/` renews.
- `/api/schema/` serves the full OpenAPI spec unauthenticated, so a partner can
  explore before they have credentials.

### Where media actually lives

**Not at the URLs the serializer returns.** The `file`, `keyframe`, `image` and
`thumbnail` fields carry URLs under `/media/` that return **404 with and without
a JWT** — media is in MinIO behind Django's storage API and was never on the
nginx filesystem. Those URLs are still useful as *identifiers*: their paths give
the storage-relative layout.

Bytes come from the DRF actions on the video detail route:

| Asset | Route | Verified |
|---|---|---|
| video | `/api/site/{s}/video/{id}/playback/` | `video/mp4` |
| analysis image | `/api/site/{s}/video/{id}/image/` | `image/jpeg` |
| thumbnail | `/api/site/{s}/video/{id}/thumbnail/` | `image/jpeg` |
| keyframe | **no route exists** | unreachable over REST |

All three support `HEAD` and return a correct `Content-Length`.

> **Do not bulk-pull media through these routes.** Doing so took the host down
> on 2026-08-25 after 773 files — see ISS-FIELD-004. Use `mirror/` instead:
> `export-media-to-s3.sh` on the host, `fetch-media-from-s3.sh` locally.

### Tooling in `mirror/`

| Script | Runs on | Purpose |
|---|---|---|
| `orc_inventory.py` | workstation | record inventory + per-site manifests, no downloads |
| `probe_media_access.py` | workstation | which routes actually serve bytes |
| `orc_mirror.py` | workstation | per-file REST pull — **superseded**, see the warning above |
| `export-media-to-s3.sh` | **host** | stream the media tree to S3, throttled |
| `fetch-media-from-s3.sh` | workstation | download, verify, extract |

---

## Day-2 operations

### Adding a new station

1. Generate a new token: `python3 -c 'import secrets; print(secrets.token_urlsafe(32))'`
2. Append to `ORC_UPLOAD_TOKENS` in `.env` (e.g., `,ipb:<token>`)
3. `sudo docker compose --env-file .env up -d` to apply (recreates the container)
4. Install the token on that station's Pi (Pi-side docs in `pi/README.md`)

### Rotating a station's token

1. Generate new token
2. Update `.env` (replace the old value)
3. `sudo docker compose --env-file .env up -d`
4. Update the Pi's `~pi/.orc_deploy_<site>` and trigger the upload to verify
5. The old token is invalidated immediately on container restart

### Rotating the server cert

10-year cert; we should never need this in practice. But if compromised:

1. Remove the old cert: `sudo rm /opt/orc-additions/certs/{fullchain,privkey}.pem`
2. Re-run `sudo ./bootstrap-cert.sh`
3. Copy the new `fullchain.pem` into the repo at
   `spring_2026_ID/pi/shared/etc/orc/sensor-upload-ca.pem`, commit, push
4. Restart the container: `sudo docker compose --env-file .env up -d`
5. Each Pi must pull + re-deploy to pick up the new pinned cert before
   their next upload will succeed. Stale Pis will start logging cert
   verification failures — that's the rotation in flight.

### Inspecting recent uploads

```bash
sudo docker logs --tail 100 orc-sensor-upload
sudo ls -la /var/orc/sensors/sukabumi/
```

### Checking the Sheets export is alive

```bash
sudo docker logs --tail 20 orc-sheets-export
```

One `exported: batches=N rows=N elapsed_s=N` line per hour, **including
zero-row runs** — at one run an hour, a silent log is indistinguishable from a
dead container, so idle runs log too. `query_ms` on the fetch lines is the
anti-join cost; it grows slowly with ledger size and is worth a glance if it
ever reaches seconds.

To ask "what would go out right now?" without any side effect:

```bash
sudo docker compose --env-file .env run --rm -e EXPORT_MODE=preview sheets-export
```

### Removing duplicate rows from the sheet

The export is deliberately **at-least-once**: rows are appended to Sheets
first and marked exported second, because Sheets appends are not idempotent
and have no idempotency key. A crash — or an ambiguous HTTP response where the
append landed but the reply was lost — re-appends that batch next cycle.
Duplicates, never loss; a duplicate is a menu click away, a missing row is
undetectable.

To find the affected batch, look for a `sheets append ok` line with **no**
following `marked exported`:

```bash
sudo docker logs orc-sheets-export 2>&1 | grep -E 'sheets append ok|marked exported' | tail -20
```

The dangling line carries both the `ts` span and the exact
`updated_range=readings!A101:E2100`, so you can delete precisely those rows.
Or, more simply: select columns `A:D` and use
**Data > Data cleanup > Remove duplicates**. The four-tuple
`(ts, station, sensor, metric)` is a natural key, which is why no extra
dedupe column is needed.

### Rolling over to a new spreadsheet

Sheets caps a spreadsheet at 10,000,000 cells — 2,000,000 rows at 5 columns,
roughly 19 months at two stations. The service warns above 750,000 rows. The
UI gets sluggish well before the hard cap.

1. A human creates a fresh spreadsheet, set up per § 1 above.
2. Change `SHEETS_SPREADSHEET_ID` in `.env`.
3. `sudo docker compose --env-file .env up -d sheets-export`.

`sensor_exports` is untouched, so nothing re-exports — the new sheet simply
continues forward from where the old one stopped. Keep the old sheet; it is
the only copy of that history in Sheets form (the database remains
authoritative either way).

### What `liveorc.sh rebuild` does to us

Nothing. LiveORC's container rebuild does not touch our service, our
certs, our `.env`, our network, or our volumes. The isolation is by
design.

## Local development (dev workstation, no AWS)

Only `timescale` + `sensor-ingest` + `sheets-export` are needed to work on the
exporter. Starting that subset means `./certs` is never mounted, so
`bootstrap-cert.sh` is not needed locally.

```bash
cp .env.example .env      # junk values are fine; compose interpolates EVERY
                          # ${VAR:?...} in the file even for services you
                          # aren't starting
printf 'ORC_SENSORS_HOST_DIR=./devdata/sensors\n' >> .env
mkdir -p devdata/sensors/sukabumi secrets

cat > docker-compose.override.yml <<'EOF'
services:
  sheets-export:
    environment:
      EXPORT_MODE: dry-run
      EXPORT_INTERVAL_SECS: "20"
      EXPORT_BATCH_ROWS: "2000"
      EXPORT_BATCH_PAUSE_SECS: "0"
EOF

docker compose --env-file .env up -d --build timescale sensor-ingest sheets-export
```

`ORC_SENSORS_HOST_DIR` redirects the sensor-CSV bind mount away from the
host-absolute `/var/orc/sensors` (no sudo needed). It is **unset on the
server**, where it defaults back to the production path. Verify with
`docker compose config` before trusting a change.

`EXPORT_MODE=dry-run` marks rows exported *without* writing them anywhere —
useful for exercising batching and the cursor with no Google credentials, and
**dangerous on the server**, where it would advance the cursor past data that
was never exported. The override file is gitignored and must not exist on the
host.

Seed data through the real ingest path rather than inserting rows by hand:

```bash
python3 sheets-export/devtools/seed_synthetic.py --sensor all \
    --date 2026-08-05:2026-08-06 --out devdata/sensors/sukabumi
```

To reproduce the backfill bug this design exists to prevent, let the exporter
catch up, then seed a date *older* than everything already exported and run
the two regression queries from
[§ Google Sheets export](#google-sheets-export). The naive query returns `0`;
the anti-join returns the full backfilled count.

Note when probing for NaN readings: Postgres treats `NaN = NaN` as **true**,
so the usual `value != value` idiom finds nothing. Use `value = 'NaN'::float8`.

## Files in this directory

| File | Role | Tracked? |
|------|------|----------|
| `docker-compose.yml` | Service definitions | Yes |
| `.env.example` | Template for the secrets file | Yes |
| `.env` | Real tokens; server-local | No (gitignored) |
| `bootstrap-cert.sh` | One-shot cert generator | Yes |
| `certs/fullchain.pem` | Public cert; copy of repo's CA pin | No (gitignored) |
| `certs/privkey.pem` | Private key; stays on server | No (gitignored) |
| `sensor-upload/app.py` | FastAPI endpoint (~85 lines) | Yes |
| `sensor-upload/Dockerfile` | python:3.12-slim + fastapi + uvicorn | Yes |
| `sheets-export/app.py` | Hourly TimescaleDB → Google Sheets exporter | Yes |
| `sheets-export/Dockerfile` | python:3.12-slim + psycopg2 + google-api-python-client | Yes |
| `sheets-export/devtools/seed_synthetic.py` | Dev tool: synthetic sensor CSVs for local testing | Yes |
| `secrets/sheets-sa.json` | Google service-account key; stays on server | No (gitignored) |
| `docker-compose.override.yml` | Local dev tuning; must NOT exist on the server | No (gitignored) |
| `devdata/` | Local dev synthetic CSVs | No (gitignored) |
| `README.md` | This file | Yes |
