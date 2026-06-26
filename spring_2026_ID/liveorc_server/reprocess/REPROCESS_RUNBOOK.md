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
| `analytics_reprocess.py` | before/after impact report (runs on the **dry-run** log too) |

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

```bash
docker cp reprocess_fit6.py liveorc_webapp:/tmp/
docker exec -it liveorc_webapp python /tmp/reprocess_fit6.py \
    --site-id <SITE_ID> --video-config-id <FIT6_VC_ID> \
    --ids <staged_sample_ids> --workers 4        # dry-run is default

# preview how the corrections move the data — BEFORE writing anything
python analytics_reprocess.py reprocess-logs/reprocess_dry_<stamp>.jsonl --out staging-report
```
Expect: a consistent **negative Δh** (615.0 datum vs higher salvage), plausible
discharge, few/no `pyorc_error`/`incomplete`. Spot-check that a video the **station**
already processed under Fit 6 gives a **matching h/q** here (engine-equivalence check —
the AWS pyorc is newer than the station's 0.9.4).

## Phase 3 — Commit on staging, verify, then prod

```bash
# staging commit (full set) to prove the write path + analytics end-to-end
docker exec -it liveorc_webapp python /tmp/reprocess_fit6.py \
    --site-id <SITE_ID> --video-config-id <FIT6_VC_ID> --commit --repoint --workers 6
```
When satisfied, repeat **Phase 1 → dry-run → commit** on **prod** (`webapp`):
```bash
docker cp reprocess_fit6.py webapp:/tmp/
docker exec -it webapp python /tmp/reprocess_fit6.py \
    --site-id <SITE_ID> --video-config-id <FIT6_VC_ID> --workers 6           # dry-run
python analytics_reprocess.py reprocess-logs/reprocess_dry_<stamp>.jsonl --out prod-preview
docker exec -it webapp python /tmp/reprocess_fit6.py \
    --site-id <SITE_ID> --video-config-id <FIT6_VC_ID> --commit --repoint --workers 6
```
Run `--commit` `nice`/overnight; it competes with the live app (low-traffic site, fine).
~1,297 × ~30–90 s ÷ 6 workers ≈ a few hours.

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

## Open inputs to fill before running

- `<SITE_ID>` — Sukabumi site id on LiveORC (server ref says "TBD"; read from admin).
- `<FIT6_VC_ID>` — the Fit 6 VideoConfig id on LiveORC (or use `--video-config-name`).
- Confirm prod storage is local `FileSystemStorage` (default). If S3 is configured
  (`LORC_STORAGE_HOST` set), `reprocess_fit6.py` needs a download branch — flag it.
