# Finding: why a duty-cycled ORC-OS station never drains its sync backlog

**Status:** Source-verified on ORC-OS **0.6.0**; the timing consequence is
**inferred, not yet observed** — see §6.
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
finishes processing**. If capture and processing complete in under ~45 seconds,
the machine is gone before the backlog task starts.

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

## 6. What is verified, and what is not

| | |
|---|---|
| **Verified** — source read on the station and against upstream `v0.6.0`, matching | the 60 s delay; the 15 s + `shutdown -h now`; that only `process_video` carries `shutdown_after_task`; the single-worker executor; the `TypeError`, reproduced directly |
| **Not verified** | that `settings.shutdown_after_task` is actually `True` on Sukabumi — the settings row has not been read. Tom states ORC-OS performs the shutdown, and `orc-capture.conf` describes itself as *"belt-and-braces backup to wp5's hardware timer and ORC-OS's `shutdown_after_task`"*, which is consistent but not the same as reading it |
| **Not verified** | that `delayed_sync_videos` never completes in practice. The 15:00 UTC grab on 2026-09-02 ran ~30 s into the boot, before the 60 s could elapse, so the absence of its log line proves nothing |
| **Not verified** | how long capture and processing actually take, which is what decides whether ~45 s of headroom exists |

The way to settle the last three is a local ORC-OS 0.6.0 harness — built and
ready at the time of writing — or a grab taken late in a wake rather than early.

## 7. Why it matters beyond Sukabumi

Any ORC-OS station on a wake/sleep duty cycle with `shutdown_after_task` enabled
has the same structure. The symptom is quiet: the retry path exists, the logs
say nothing alarming, and the failed videos simply accumulate. At Sukabumi that
went unnoticed until the backlog reached 2,982 rows.
