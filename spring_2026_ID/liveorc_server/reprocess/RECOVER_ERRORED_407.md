# Phase 01 — recover the 407 errored site-4 videos

Approved 2026-09-02. This is TODO-119 phase 01: the video is already on the
server with its bytes intact, so this costs **no metered bytes and does not
touch the station**.

## Why this is a scoped run, not the full reprocess

`REPROCESS_RUNBOOK.md` describes re-deriving *all* site-4 history under Fit 6.
That is a larger, separate operation (TODO-113) which also rewrites the ~2,242
records that already finished. **This run touches only the 407 that failed**,
using `--ids` to override the site scan.

| | |
|---|---|
| Target | 407 site-4 videos in `error` state, all with file bytes present |
| Of those, needing `--recover` (no `time_series` at all) | **405** |
| Already having a `time_series` (would be overwritten) | 2 |
| Months | 2026-05: 10, 2026-06: 20, **2026-07: 280**, 2026-08: 97 |
| Id list | `sukabumi_error_video_ids.txt` (comma-separated, ready for `--ids`) |

The runbook already settled the policy this run depends on: *"Errored /
no-time_series videos: RECOVER them (decided)"*, validated on staging
2026-06-29 with 3/3 recovered and no OneToOne violations. The only thing new
here is the scale — 405 against those 3 — which is why the dry run matters.

## The id list is a snapshot, and it is stale by design

The 407 comes from the TODO-114 mirror manifest of **2026-08-25**. Sync has
been failing since 08-23 and resumed on 09-02, so production will hold more
errored videos than this list names. Refresh it before the commit run, or
accept that a second pass will be needed. It is a floor, not a total.

## Run it from the EC2 checkout

```bash
cd ~/openrivercam/spring_2026_ID/liveorc_server/reprocess
git pull                                   # this file and the id list
IDS=$(cat sukabumi_error_video_ids.txt)

# 1  smoke dry-run, 5 videos - proves the env and the id path
./prod_reprocess.sh --ids "$IDS" --limit 5 --recover

# 2  full dry-run over all 407, then read the impact BEFORE writing
./prod_reprocess.sh --ids "$IDS" --recover
./prod_analytics.sh

# 3  backup - every time, before any commit
./backup_liveorc_db.sh

# 4  the write, backgrounded
DETACH=1 ./prod_reprocess.sh --ids "$IDS" --commit --repoint --recover
```

`prod_reprocess.sh` passes arguments straight through to `reprocess_fit6.py`,
runs inside the webapp via `docker exec` so it inherits the real media volume,
and pins `xarray==2024.9.0` in an isolated venv. Dry-run is the default; it
prompts before any `--commit`.

## Rollback

`--repoint` and `--recover` both change `api_video`, not just `api_timeseries`,
so the **full** restore is the correct rollback:

```bash
./restore_liveorc_db.sh full liveorc-backups/<ts>
```

## What success looks like

Videos are written only when pyorc returns 0 and both `h` and `q_50` are
finite. Night and low-light clips that fail optical WL or PIV are logged
`incomplete` or `pyorc_error` and left untouched — never overwritten with a
failed detection. Expect a meaningful share of the 407 to stay errored for that
reason; they were captured in the dark, and reprocessing does not add light.
