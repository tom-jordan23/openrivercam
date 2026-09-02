# Phase 01 — recover the 407 errored videos, from the console

TODO-119 phase 01, approved 2026-09-02. The video is already on the server with
its bytes intact, so this costs **no metered bytes and never touches the
station**.

Everything here is typed by hand into Session Manager. There is no SSH on this
host and the local AWS credentials are S3-only, so no agent and no workstation
can run these steps.

---

## 1. Get a shell

**AWS Console → Systems Manager → Session Manager → Start session**, then pick:

| | |
|---|---|
| Instance | `LiveORC-Server` |
| Instance id | `i-01d5ccd8c3d4a3858` |
| Region / AZ | us-east-1, us-east-1c |
| You land as | `ssm-user` |

`prod_reprocess.sh` decides for itself whether it needs `sudo docker`, so you do
not have to.

> **If the session dies with `Plugin with name Standard_Stream not found`, the
> disk is full.** It is the SSM agent failing to write its own session working
> files, not a configuration fault. The same root cause produced instant,
> zero-byte Run Command failures during the media-volume incident. Check `df -h`
> before touching anything SSM-related — stage `check` below does it for you.

## 2. Update the checkout

```bash
cd ~/openrivercam && git pull
cd spring_2026_ID/liveorc_server/reprocess
```

If the checkout is not at `~/openrivercam`, the next stage fails on a missing id
file and tells you so.

## 3. Run the stages

One short word each. Session Manager is a browser terminal — long paste
sequences get mangled, and a mangled command carrying `--commit` writes to
production. That is the whole reason this is a script.

```bash
./ssm_recover_407.sh check
```

| Stage | What it does | Writes? |
|---|---|---|
| `check` | id count, toolkit files, container, disk, existing backups | no |
| `smoke` | dry-run over 5 videos — proves the env and the `--ids` path | no |
| `dryrun` | dry-run over all 407, then the impact report | no |
| `backup` | `pg_dump` + `api_timeseries` baseline | to disk only |
| `commit` | the real write — refuses without a backup from today, and asks | **yes** |

`commit` requires you to type `RECOVER` in full. Nothing else prompts.

---

## What this run is, and is not

**Scoped.** `--ids` overrides the site scan, so only the 407 that failed are
touched. The ~2,242 site-4 records that already finished are left alone. The
full-site Fit 6 reprocess is a separate, larger operation (TODO-113).

| | |
|---|---|
| Target | 407 site-4 videos in `error` state, all with file bytes present |
| Needing `--recover` (no `time_series` at all) | **405** |
| Already having one (would be overwritten) | 2 |
| Months | 2026-05: 10, 2026-06: 20, **2026-07: 280**, 2026-08: 97 |

`REPROCESS_RUNBOOK.md` already settled the policy: *"Errored / no-time_series
videos: RECOVER them (decided)"*, validated on staging 2026-06-29, 3/3 recovered
with no OneToOne violations. What is new here is scale — 405 against those 3 —
which is why `dryrun` comes before `commit`.

## Two things to expect

**A real share will stay errored, by design.** A video is written only when
pyorc returns 0 and both `h` and `q_50` are finite. Night and low-light clips
that fail optical WL or PIV are logged `incomplete` or `pyorc_error` and the old
row is left intact — never overwritten with a failed detection. Read the
Outcomes table in the `dryrun` report before committing. Reprocessing does not
add light.

**The 407 is a floor, not a total.** It comes from the TODO-114 mirror manifest
of 2026-08-25. Sync failed from 08-23 and resumed 09-02, so production holds
more errored videos than this list names. `check` reports the count so you can
see if it has drifted; a second pass with a refreshed list will be worth it.

## Rollback

`--repoint` and `--recover` both change `api_video`, not just `api_timeseries`,
so the **full** restore is the correct rollback:

```bash
./restore_liveorc_db.sh full liveorc-backups/<ts>
```

The `timeseries` mode restores only `api_timeseries` and cannot undo the video
row changes. Do not reach for it here.
