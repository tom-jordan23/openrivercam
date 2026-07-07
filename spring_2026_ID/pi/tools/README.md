# pi/tools — operator scripts (not deployed to stations)

Ad-hoc diagnostic and recovery scripts for the station sensor pipeline. These
are **operator tools**, run by hand over SSH/Tailscale — they are *not* part of
the deployed station image (`pi/shared/`) and nothing installs them.

All three are read-only except where noted, and none touch the capture
schedule, systemd services, or config.

| Script | What it does |
|--------|--------------|
| `orc_collect.sh` | Read-only diagnostic bundle: sensor CSVs, logger/upload journals, connectivity, power, deployed code, wake cadence. Writes one `/tmp/orc_collect_<host>_<ts>.txt` to scp back. Run with `sudo`. |
| `orc_flush_sensors.sh` | Recover the whole upload backlog: waits for the LTE link, then runs the real `orc-sensors-upload` with retries until the watermark advances. Run as `pi`, in maintenance mode. |
| `orc_flush_one.sh` | Flush **one** sensor directly (`./orc_flush_one.sh sht40 [since-date]`). No fail-fast — continues past failed files, so it finishes a laggard sensor inside a short wake window. Run as `pi`. |

## Background — the July 2026 Sukabumi sensor-upload incident

Sensor data (sht40/rg15/ds18b20) stopped appearing on the LiveORC server at
staggered dates while video uploads kept working. Root cause: the sensor upload
(`orc-sensors-upload`, invoked early in `orc-capture`) fires ~5 s after boot,
before the LTE modem registers, so its PUTs failed with `curl 6/7`. The old
all-or-nothing watermark never advanced, and alphabetical upload order starved
`sht40` (uploaded last). The 30-day CSV rotation then permanently deleted the
un-uploaded `sht40` data from 2026-05-16 → 06-07.

The fix (retry + oldest-mtime-first + per-file resumable watermark) is in
`pi/shared/usr/local/bin/orc-sensors-upload`. These tools were used to diagnose
and to recover the ~30 days of data still on the Pi.
