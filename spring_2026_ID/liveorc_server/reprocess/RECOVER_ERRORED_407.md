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
cd ~/code/git/openrivercam && git pull
cd spring_2026_ID/liveorc_server/reprocess
```

That is the checkout path on this host — the same as on the workstation. The
`check` stage prints the directory it resolved, so a wrong path shows up
immediately rather than three commands later.

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
| `probe` | dry-run over ids you name; `VC=<id>` targets another VideoConfig | no |
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

## ON HOLD — this work now belongs to TODO-113 (2026-09-02)

**The `smoke` run failed 5 of 5, and that is the predicted result, not a fault.**
Recovering these videos is decided by the transect, so it was folded into
**TODO-113**, the cross-section swap and reprocess, rather than run on its own.
Reasoning below; run `probe` after the switch, not before. Do not run `commit`.

### Night is the reliable case. Daylight is where this fails.

An earlier draft of this file said to expect night and low-light clips to fail.
**That is backwards**, and `findings/optical_wl_daytime_glint.md` opens by
flagging exactly that inversion.

| | Day 06–18 WIB | Night 18–06 |
|---|---|---|
| **Errored (407)** | **388 — 95.3%** | 19 — 4.7% |
| Finished (2,242) | 961 — 42.9% | 1,281 — 57.1% |

### Why reprocessing under VideoConfig 3 cannot help

All 100 error videos measured in July fail identically — pyorc finds a plausible
waterline, then the signal-to-noise gate rejects it:

```
Found water level at h: 614.795 m with too low signal-to-noise: 1.306 < 2.000
```

That gate is `s2n_thres: 2.0` in `recipe_3`, which is what **VideoConfig 3
uses**. So `--video-config-id 3` re-runs the identical computation that already
failed. Lowering the gate is not a way out either: the distribution is bimodal —
passes at S/N 3–5, failures at 1.3–1.8, almost nothing between 1.98 and 2.00 —
and the finding concluded that lowering it *"would admit unreliable estimates,
not recover good ones."* The failures already locate the correct waterline
(614.794 m, same as the passes); they cannot confirm it.

### Why the transect switch changes the question

The recipe detects water level against the WL cross-section
(`water_level_options: bank near, length 3.0, padding 0.5, min_z 614.3,
max_z 618.5`). **A different transect changes the geometry that detection runs
on**, so the S/N these clips achieve under a new cross-section is genuinely
unknown — it is not predictable from the measurements above, which were all
taken under the current one.

That is the reason to wait rather than to close this out. Re-testing the 407
under VideoConfig 3 answers a question about a configuration we are about to
replace.

### When the transect lands

```bash
VC=<new-video-config-id> ./ssm_recover_407.sh probe 2421,2423,2424,2425,2427,2432,2433,2468
```

Those eight are July daytime clips — the bulk case, 377 of the 407 fall in
July–August. If they pass under the new transect, the full run is worth doing
and the id list is still valid. If they fail the same way, the finding is that
these clips need a different water-level approach, not a reprocess.

## Also worth knowing

**The 407 is a floor, not a total.** It comes from the TODO-114 mirror manifest
of 2026-08-25. Sync failed from 08-23 and resumed 09-02, so production holds
more errored videos than this list names. `check` reports the count so you can
see if it has drifted; refresh the list before any real run.

## Rollback

`--repoint` and `--recover` both change `api_video`, not just `api_timeseries`,
so the **full** restore is the correct rollback:

```bash
./restore_liveorc_db.sh full liveorc-backups/<ts>
```

The `timeseries` mode restores only `api_timeseries` and cannot undo the video
row changes. Do not reach for it here.
