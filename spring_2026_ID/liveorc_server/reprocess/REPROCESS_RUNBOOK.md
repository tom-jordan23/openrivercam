# Sukabumi historical reprocess — Fit 6, on LiveORC

Re-derive the ~1,297 historical Sukabumi `time_series` (salvage calibration) using
the certified **IPB Fit 6** config, **on the LiveORC AWS box**, and **overwrite** the
old records in place. Validate on a **staging** LiveORC first. Prepared 2026-06-26.

---

## Why not LiveORC's built-in reprocess

LiveORC's server-side task (`api/tasks.py:run_nodeorc`) feeds the **stored** water
level into pyorc as a fixed input (`h_a = video.time_series.h`) and writes back **only
discharge**. Sukabumi is **gauge-less** — the historical `h` values were detected on
the OLD salvage datum. Pairing them with the new `z_0 = 615.0` camera config gives
inconsistent geometry → wrong discharge. We must **re-detect the optical water level**.

`reprocess_fit6.py` calls the same engine the station uses
(`pyorc.service.velocity_flow_subprocess`) but with **`h_a=None` + the WL
cross-section**, which triggers fresh optical WL detection, then writes **both** the
new `h` and the new discharge. Because `Video.time_series` is **OneToOne**, updating
that row **replaces** the salvage result — no duplicates, no orphans (this resolves the
"replace-not-append" requirement cleanly; no re-sync needed — LiveORC dashboards read
the row directly).

Where it runs: **on the AWS box, inside the `webapp` container** — pyorc and the raw
videos are already there, so there is **no 13 GB download and the solar Pi is never
touched**.

## Files in this dir

| file | what |
|---|---|
| `backup_liveorc_db.sh`   | full pg_dump + targeted `api_timeseries` SQL/CSV (the analytics **baseline**) |
| `restore_liveorc_db.sh`  | rollback: `timeseries` (surgical) or `full` |
| `build_staging_local.sh` | stand up a **local** throwaway LiveORC + restore a prod dump (free; default) |
| `stage_load.sh`          | same but into a remote/second stack (alt to local) |
| `reprocess_fit6.py`      | the reprocessor — **dry-run by default**, parallel, JSONL log, replace-in-place |
| `run_reprocess.sh`       | STAGING wrapper: `docker exec` into the local webapp, pin xarray, run |
| `prod_reprocess.sh`      | PROD wrapper: ephemeral **sidecar** (never touches the serving webapp) |
| `analytics_reprocess.py` | before/after impact report (runs on the **dry-run** log too) |
| `prod_analytics.sh`      | convenience: run analytics on the newest log in `./reprocess-logs/` |

---

## Known good (validated on local staging 2026-06-29, LiveORC 0.3.0)

- **Sukabumi = site id 4** ("Sukabumi City", 1165 videos). **Fit 6 = VideoConfig id 3**
  ("Sukabumi IPB", `cross_section=4`, `cross_section_wl=5`). Site 2 "Test site" (1255
  videos, config `sukabumi_h`) is likely early Sukabumi captures — **decide separately**
  whether to include them.
- **Engine env gotcha (important):** the stock LiveORC image ships pyorc 0.9.4 with an
  xarray years too new (2026.x on py3.14), which crashes pyorc's transect step. Pin
  **`xarray==2024.9.0`** (what `run_reprocess.sh` and `build_staging_local.sh` do).
  Do NOT permanently mutate the serving webapp on prod — use an ephemeral sidecar
  (see `run_reprocess.sh` header).
- **Validated impact** on a 25-video staging sample (2026-05-16): salvage water level
  617.65 m (sd 0.92, wrong datum, q_50≈0) → Fit 6 **614.75 m (sd 0.04)**, q_50 median
  **0.31 m³/s**, velocimetry coverage **~96%**. 23/25 OK, 2 pyorc errors (left intact),
  3 had no time_series (skipped). Storage is **S3/MinIO** on prod — the reprocessor
  streams via Django storage, so no download branch is needed.

---

## Phase 0 — Build a LOCAL staging LiveORC (do this first; it's free)

We do **not** trust the toolkit against prod until it's proven on staging — and we
do staging **locally** to avoid paying for a second EC2.

1. **Pull a prod snapshot down once** (small): run `backup_liveorc_db.sh` on the AWS
   box, then `scp`/SSM the `liveorc-backups/<ts>/` dir to this machine.
2. **Pull a handful of real Sukabumi videos** down too (so they resolve on disk).
   `build_staging_local.sh` prints the exact ids + relative `file` paths to grab;
   on prod they live in MinIO — fetch ~25 with `mc cp` (or the LiveORC video-download
   API) into a local dir that mirrors those relative paths.
3. **Stand up local LiveORC + restore the dump:**
   ```bash
   LIVEORC_REPO=/tmp/LiveORC ./build_staging_local.sh liveorc-backups/<ts> <SITE_ID> ./media-src
   ```
   This brings up a local postgis LiveORC (web `:8010`, db `:5433`, container
   `liveorc_webapp`) with **FileSystemStorage**, restores the dump, copies your sample
   media in, and prints the sample ids + the Fit 6 `VideoConfig` id.

> The reprocessor reads videos through Django's storage API, so it behaves the same
> on local FS as on prod MinIO/S3 — local staging genuinely exercises the prod code path.

**Confirm the Fit 6 VideoConfig is present** in the restored DB (camera_config
"Sukabumi IPB", recipe, both cross-sections incl. `cross_section_wl`). If
`cross_section_wl` is missing, fix that first — the optical WL path needs it.

_(Alternative, if you ever want a remote staging stack instead: `stage_load.sh` does
the restore+media step against a second containerized stack — see its header.)_

## Phase 1 — Backup prod (every time, before any commit)

```bash
./backup_liveorc_db.sh        # → liveorc-backups/<ts>/  (KEEP api_timeseries.csv = baseline)
```

**Do I need a media (video) backup? No.** The backup is DB-only and small on
purpose — the video bytes live in MinIO/S3, not Postgres. Reprocessing is
**read-only on videos** (it streams them, never writes/deletes), so the only thing
that can change — and the only thing rollback needs — is the `api_timeseries` rows,
which the DB dump captures in full. A media backup would only matter for full
disaster recovery (a separate `mc mirror`/`rsync` of the bucket; many GB) and is not
part of this operation.

## Phase 2 — Dry-run + impact preview (staging, then prod)

`run_reprocess.sh` pins the compatible xarray, copies the script in, and runs it
(dry-run is the default). On staging it targets `liveorc_webapp`:
```bash
./run_reprocess.sh --site-id 4 --video-config-id 3 --workers 2     # dry-run, all site-4 videos
# (or scope: --ids <list>  /  --start 2026-05-16T00:00:00 --stop 2026-05-16T23:59:59)

# preview how the corrections move the data — BEFORE writing anything
docker cp liveorc_webapp:/tmp/<log>.jsonl ./staging_dry.jsonl   # log path is printed by the run
python analytics_reprocess.py ./staging_dry.jsonl --out staging-report
```
Expect (matches the validated sample): consistent **negative Δh** to ~614.7 m, q_50
shifting off zero to ~0.2–0.7 m³/s, ~96% velocimetry coverage, a couple of
`pyorc_error`/`no_timeseries` that are left intact.

## Phase 3 — Commit on staging, verify, then prod

```bash
# staging commit (proves the write path + analytics end-to-end)
./run_reprocess.sh --site-id 4 --video-config-id 3 --commit --repoint --recover --workers 2
```
`--recover` creates time_series for previously-errored videos; `--repoint` sets each
video's config to Fit 6 so config↔result stay consistent.
For **prod**, use `prod_reprocess.sh` — it launches an **ephemeral sidecar** from the
webapp's image on the same docker network (reaches `db` + the S3/MinIO `storage`),
pins the xarray, and never touches the serving webapp. It auto-uses `sudo docker` if
needed and prompts before any `--commit`. Run on the EC2 from the repo checkout:
```bash
cd ~/openrivercam/spring_2026_ID/liveorc_server/reprocess
./prod_reprocess.sh --limit 5                        # smoke dry-run (5 videos)
./prod_reprocess.sh --recover                        # full dry-run (all site 4)
./prod_analytics.sh                                  # report on the newest log
./backup_liveorc_db.sh                               # Phase 1 backup BEFORE writing
DETACH=1 ./prod_reprocess.sh --commit --repoint --recover   # the real write, backgrounded
```
Defaults are `--site-id 4 --video-config-id 3`; tunables (`ENV_FILE`, `WEBAPP`, `NET`,
`IMG`, `XARRAY_PIN`) are in the script header. `--commit` run: ~1165 site-4 videos ×
~30–90 s ÷ workers ≈ a few hours (≈747 overwritten, ~3+ recovered, the rest left as-is).

## Phase 4 — Final report + rollback path

```bash
python analytics_reprocess.py reprocess-logs/reprocess_commit_<stamp>.jsonl --out final-report
```
Rollback if needed (uses the Phase-1 backup):
```bash
./restore_liveorc_db.sh timeseries liveorc-backups/<ts>      # surgical undo of api_timeseries
# ./restore_liveorc_db.sh full liveorc-backups/<ts>          # only if the targeted undo is insufficient
```

## Failure handling (decided)

A video is written **only** when pyorc returns 0 and both `h` and `q_50` are finite.
Night/low-light clips where optical WL or PIV fails are logged `incomplete`/`pyorc_error`
and the **old row is left intact** — never silently overwritten with a failed detection.
They surface in the analytics `Outcomes` table for review (tie-in to the parked
night-profile work).

## Resolved inputs + decisions (from staging)

- `SITE_ID = 4`, `FIT6_VC_ID = 3`. Storage is **S3/MinIO** — handled by the
  storage-agnostic streaming read (no download branch needed).
- **Site 2 "Test site": EXCLUDED** (decided) — different camera + scene, not the
  Sukabumi gauge. Only site 4 is reprocessed.
- **Errored / no-time_series videos: RECOVER them** (decided). `--recover` creates a
  new time_series (via `bulk_create`, bypassing the model's thumbnail-regen /
  auto-associate side effects) when Fit 6 succeeds; videos where pyorc still fails are
  left untouched. Validated on staging: 3/3 errored 2026-05-16 clips recovered, with
  no OneToOne violations.
