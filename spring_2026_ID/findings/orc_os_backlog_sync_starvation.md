# Finding: why a duty-cycled ORC-OS station never drains its sync backlog

**Status:** Source-verified on ORC-OS **0.6.0**, and the timing consequence is
now **measured** — see §6. Supersedes the 2026-09-02 first draft, which leaned
toward "the backlog task never runs"; it runs 55% of the time.
**Software:** ORC-OS 0.6.0 (`orc_api == 0.6.0`, read from the installed package
on Sukabumi 2026-09-02). Confirmed identical to upstream tag `v0.6.0`.
**Site:** Sukabumi — 2,982 `FAILED` video rows, 1,193 of which still hold their
file, none ever retried.
**Author:** analysis by Claude, for Tom Jordan.
**Date:** 2026-09-02.

> Why this is written down: the retry path exists, is more patient than the one
> that failed, and has never once run. Two separate things in the code explain
> that, and one of them is a plain bug. Both matter to anyone running ORC-OS on
> a duty cycle, not just to Sukabumi.

---

## 1. Headline

On a station that sleeps between wakes, the task that would re-sync failed
videos is scheduled to begin **60 seconds after boot**, while the capture path
issues `sudo shutdown -h now` roughly **15 seconds after the current video
finishes processing**. Measured over 823 boots at Sukabumi, **the task is killed
before it can look 45% of the time**; the other 55% it looks at a queue nothing
ever fills.

Two stacked causes, then, not one. Neither alone accounts for a backlog that has
never been retried.

Separately, the environment variable that would let an operator lengthen that
15-second window **cannot be set to any value without raising `TypeError`**.

## 2. The two clocks

**The backlog side** — `schedulers.py:24`, started fire-and-forget at
`main.py:86`:

```python
async def delayed_sync_videos(app, logger):
    logger.info("Starting sync of videos with a 60-second delay.")
    await asyncio.sleep(60)
    ...
    videos_for_syncing = crud.video.get_list(db=session, sync_status=SyncStatus.QUEUE)
```

The delay is deliberate; `main.py:85` explains it as *"delay syncing of
non-synced videos to ensure any video jobs for daemon are always prioritized."*
On a continuously powered station that is sound. On a duty-cycled one it assumes
a machine that will still be there in a minute.

**The shutdown side** — `schemas/video.py:335`, at the end of `video.run()`,
after the current clip has been processed and synced inline:

```python
if shutdown_after_task:
    logger.info(f"Shutdown triggered by daemon. Shutting down in {timeout_before_shutdown} seconds.")
    time.sleep(timeout_before_shutdown)          # default 15
    subprocess.call("sudo shutdown -h now", shell=True)
```

Nothing coordinates the two. The shutdown is not aware that a sync task is
pending, and the sync task is not aware that a shutdown is coming.

## 3. It is the capture path that shuts down, not the sync path

Worth stating precisely, because the reverse is easy to assume.
`shutdown_after_task` is a parameter of **`process_video` only**
(`utils/queue.py:142`), which passes it through at `queue.py:192`:

```python
executor.submit(video.run, upload_directory, "", shutdown_after_task, priority=priority)
```

`sync_video`, `sync_videos_start_stop` and `sync_videos_list` do **not** take or
pass it. So a backlog sync can never trigger a shutdown — it can only be
*interrupted* by the one the capture path already scheduled.

The interruption is total: `app.state.executor` is a
`PriorityThreadPoolExecutor(max_workers=1)` (`main.py:75`), so processing and
syncing share a single thread, and `sudo shutdown -h now` takes the whole
process with it.

## 4. Correction — one thing this is NOT

An earlier reading of `schedulers.py:107` treated this as the system deliberately
refusing backlog work:

```python
if settings.shutdown_after_task:
    process_queue_videos = False    # "prevent that older videos are being processed"
```

**That is about a different queue.** `process_queue_videos` gates only the block
at `main.py:89-95`, which reads `status=VideoStatus.TASK` and
`status=VideoStatus.QUEUE` — the **processing** status enum, not `SyncStatus`.
It suppresses re-*processing* of older videos and has no bearing on syncing.
`SyncStatus.QUEUE` and `VideoStatus.QUEUE` are different enums that share a
member name, which is what makes the misreading easy.

## 5. The escape hatch does not work

`timeout_before_shutdown` looks configurable — `orc_api/__init__.py:26`:

```python
timeout_before_shutdown = os.getenv("ORC_TIMEOUT_BEFORE_SHUTDOWN", 15)
```

`os.getenv` returns a **string** when the variable is set; the fallback `15` is
an **int**; and there is no `int()` cast anywhere in the package — those three
lines are its only appearances. So any value an operator sets reaches
`time.sleep()` as a string:

```
>>> time.sleep("300")
TypeError: 'str' object cannot be interpreted as an integer or float
```

The exception fires *before* the next line, so the effect of setting the
variable is not a longer delay but **no shutdown at all**, plus an exception
that also skips the `VideoStatus.ERROR` check below it. The comment immediately
after is *"only do a raise after the shutdown has been done, to avoid not
shutting down at all"* — the author was guarding against this exact class of
failure, but the guard sits below the line that raises.

**Fix upstream:** `int(os.getenv("ORC_TIMEOUT_BEFORE_SHUTDOWN", 15))`.

## 6. Measured on the station, 2026-09-02

The two log lines in `delayed_sync_videos` bracket the race precisely. The first
is written before the sleep, the second only after it returns, so counting them
across every boot the journal holds settles it without needing to catch a wake
at the right instant:

| Log line | Count | |
|---|---|---|
| `Starting sync of videos with a 60-second delay.` | **823** | the task started |
| `There are N videos left to synchronize.` | **454** | it survived the sleep — **55%** |
| *(difference)* | **369** | killed before it could look — **45%** |
| `Shutdown triggered by daemon` | **818** | ORC-OS ends 99% of cycles |

**The settings row, read for the first time:**

```
active  enable_daemon  shutdown_after_task  reboot_after  sync_file  sync_image  video_config_id
1       1              1                    3600.0        1          1           3
```

`shutdown_after_task` is on, and at 818 of 823 boots ORC-OS — not `orc-capture`
and not the Witty Pi hardware timer — is what ends the cycle. That matches the
design intent recorded in `pi/sukabumi/etc/orc-capture.conf`, which describes
its own `CYCLE_MODE` as a belt-and-braces backup rather than the normal path.

**Wake duration**, from `journalctl --list-boots`:

```
boot -4:  13:30:21 -> 13:32:23  = 2m02s
boot -3:  14:00:15 -> 14:02:30  = 2m15s
```

So a wake runs ~122-135 s and the sync task fires at t+60 — inside the window,
which is why it survives more often than not rather than never. The 45% that
die are the wakes where capture and processing finished early enough that the
15-second shutdown timer expired first.

**What this changes.** The backlog is not structurally unreachable. Roughly one
wake in two, the task lives long enough to act on whatever is in
`SyncStatus.QUEUE` — it simply always finds it empty. Any remedy that fills that
queue should expect to lose about half its attempts to the shutdown, and to
have only the remainder of the wake after t+60 to work in.

**Still not measured:** how long the sync itself gets before the shutdown lands
on a wake where the task does survive, and therefore how many clips can realistically
complete per wake. That needs either the local ORC-OS 0.6.0 harness or a grab taken
after t+60 in a wake.

## 7. Why it matters beyond Sukabumi

Any ORC-OS station on a wake/sleep duty cycle with `shutdown_after_task` enabled
has the same structure. The symptom is quiet: the retry path exists, the logs
say nothing alarming, and the failed videos simply accumulate. At Sukabumi that
went unnoticed until the backlog reached 2,983 rows.

The quietest part is that the one log line an operator would look for —
`There are N videos left to synchronize.` — prints **0** on every wake where it
prints at all, while thousands of failed rows sit in the database. It is
truthfully reporting the queue, which is empty, and saying nothing about the
backlog, which is not.
