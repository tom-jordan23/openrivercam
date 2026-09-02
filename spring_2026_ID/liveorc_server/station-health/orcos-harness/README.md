# ORC-OS 0.6.0 harness — testing station behaviour without the station

Built 2026-09-02 to answer whether moving `sync_status` from `FAILED` to
`QUEUE` actually drains Sukabumi's backlog, without spending metered bytes or
risking a field station. Results are in
`findings/orc_os_backlog_sync_starvation.md` §7.

## Version fidelity is the whole point

The station runs **ORC-OS 0.6.0** (`orc_api == 0.6.0`, read from the installed
package). That is **older** than the checkout in `rainbow-sensing/orc-os`, which
is v0.7.0 — and 0.7.0 is the release that **deleted `schedulers.py`** in the move
to celery-beat. Since `schedulers.py` is exactly what this tests, a harness on
the default checkout would exercise different code and prove nothing.

Fingerprints that identify 0.6.0, all confirmed against the station:

| | v0.6.0 | station |
|---|---|---|
| `utils/queue.py` `sync_videos_start_stop` | 250 | 250 |
| `schedulers.py` | present | present |
| `schemas/callback_url.py` `timeout=5` | 115 | 115 |
| `routers/video.py` POST `/sync/` | 530 | 530 |
| `routers/video.py` `timeout=` | 548 | 548 |

## Build it

```bash
cd rainbow-sensing/orc-os
git fetch --all --tags
git worktree add --detach /tmp/orc-os-v060 v0.6.0
cd /tmp/orc-os-v060
mkdir -p testdata/uploads/incoming
printf 'ORC_SECRET_KEY=test-only\nORC_DEV_MODE=1\nORC_DATA_PATH=./testdata\n' > .env
docker compose up -d orcapi          # v0.6.0 stack is just orcapi + dashboard
```

## Run it

```bash
UPLOAD_DELAY=5.3 python3 mock_liveorc.py &     # 5.3 s = a 9.2 MB clip at 1.74 MB/s
docker exec orc-api ffmpeg -y -f lavfi -i testsrc=size=64x48:rate=5:duration=1 \
    -pix_fmt yuv420p /tmp/tiny.mp4
docker cp seed.py orc-api:/tmp/seed.py
docker exec orc-api python3 /tmp/seed.py /app/data/orc-os.db /app/data/uploads <gateway-ip> 30
bash kill_test.sh <scratchpad>                 # the interruption test
```

`<gateway-ip>` is `docker network inspect <net> --format '{{range .IPAM.Config}}{{.Gateway}}{{end}}'`.

## Three traps, each of which looked like an ORC-OS bug

1. **`status` must be the enum NAME, not its value.** Seeding `4` yields
   `LookupError: '4' is not among the defined enum values` when SQLAlchemy
   hydrates the row.
2. **The video files must be decodable.** The sync path opens them; zero-filled
   stand-ins die in `cvtColor` with `!_src.empty()`. Hence the ffmpeg step.
3. **Every video needs a `video_config` with a `remote_id`.** `sync_remote`
   builds its payload from `self.video_config.remote_id` and dies on
   `AttributeError` before sending anything.

`seed.py` handles all three; they are listed here because each cost a run.

## What it cannot tell you

Throughput. Uploads on localhost are instant, so the mock *imposes* the
field-measured 5.3 s rather than discovering it. Clips-per-wake remains a field
number. This rig answers mechanism: pickup, ordering, batching, and what
survives an interruption.
