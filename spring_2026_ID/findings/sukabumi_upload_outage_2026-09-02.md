# Finding: an upload outage began 2026-09-02 13:32 UTC and is ongoing

**Status:** Active at time of writing (2026-09-02 ~21:35 UTC, ~8 h elapsed).
Measured over four station wakes and one server-side pass.
**Site:** Sukabumi → `openrivercam.endlessprojects.info`.
**Context:** TODO-119 Track 1, items B and C. Neither was answered as posed;
the measurement instead found a live outage.
**Scripts:** `station-health/todo119_nat64_throughput.sh`,
`todo119_size_ladder.sh`, `todo119_outage_diag.sh`,
`liveorc-host/measure-upload-durations.sh`.
**Grabs:** `nat64tput119o`, `nat64tput119p`, `sizeladder119q`, `outagediag119r`.

---

## 1. The headline

Both upload pipelines stopped within two minutes of each other and have not
resumed:

| Signal | Last success | Source |
|---|---|---|
| video `POST /api/video/` → 201 | **2026-09-02 13:32 UTC** | nginx access log |
| row in `sensor_readings` | **2026-09-02 13:30 UTC** (20:30 WIB) | Grafana |

The station is not down. SSH succeeded at 20:00, 20:30 and 21:00 UTC, with
`uptime at grab` of 27–35 s each time, so it is booting on its normal 30-minute
cadence. `mmcli` reports LTE attached, Telkomsel, signal 100%. Only the upload
path is affected.

## 2. Timeline

```
13:01 UTC  deletesafety119g     delete-safety inventory
13:30 UTC  redrivediscovery119h
13:32 UTC  <- LAST SUCCESSFUL VIDEO UPLOAD
14:00 UTC  p02dryrun119i        dry run
14:02 UTC  p02commit119j        <- 12.61 GB reclaim COMMITS, 1,403 clips deleted
           ... no upload of any kind has succeeded since ...
17:30 UTC  pathprobes119n       1 MB POST -> 000
20:00 UTC  nat64tput119o        6 transfers, 6 failures
20:30 UTC  nat64tput119p        6 transfers, 6 failures
21:00 UTC  sizeladder119q       5 transfers, 5 failures
```

**The first wake that failed to upload is the one immediately after the reclaim
committed.** That correlation was tested at the 21:30 wake and **the reclaim is
exonerated** — see §3.

## 3. The station's own account (outagediag119r, 21:32 UTC)

**The reclaim did not cause this.** The sync task runs normally every boot and
reports no error of any kind:

```
21:00:46  schedulers - INFO - Starting sync of videos with a 60-second delay.
21:01:46  schedulers - INFO - There are 0 videos left to synchronize.
```

No `FileNotFoundError`, no missing-path exception, nothing naming a deleted
clip. The predicted mechanism does not appear. What remains is the **known**
starvation behaviour, unchanged and unrelated to the reclaim: `schedulers.py:35`
asks only for `SyncStatus.QUEUE`, so a backlog of `FAILED` rows is never
retried. Root is at 24 G free, exactly as the reclaim left it.

**Capture is still running and still producing rows.** Video rows 5686–5697
were created at 30-minute intervals from 15:31 through 21:01 UTC — i.e. through
the whole outage. So clips are being captured and are failing to *sync*, which
is why they accumulate as `FAILED`:

```
FAILED  2995     <- was 2978 on 09-01; the evening's captures are landing here
SYNCED  2576
LOCAL    126
```

**Sensor uploads are attempted every wake and time out**, which is the same
fault my probes hit:

```
21:30:39  orc-sensors-upload: uploading 5 file(s) to https://...:8443/sensors/upload/sukabumi/
21:31:08  [orc-capture] WARN: orc-sensors-upload failed or timed out
```

Sensors themselves are fine — `rg15`, `sht40` and `wittypi` all wrote to
`/var/log/orc/sensors/*_2026-09-02.csv` during the same wake. **The data is
being collected and is sitting on the station.** Only its delivery is broken.

**The WAN path is degraded, and DNS is part of it:**

```
lookup pangolin.openrivercam.com on [::1]:53: server misbehaving
tailscaled: failed to resolve "controlplane.tailscale.com": no DNS fallback candidates remain
tailscaled: dial tcp 205.147.105.78:443: connect: network is unreachable
tailscaled: dial tcp [2600:3c18::2000:acff:fe8e:3ed5]:443: connect: network is unreachable
```

`network is unreachable` on both IPv4 and IPv6 to external addresses, a local
resolver on `[::1]:53` reporting `server misbehaving`, and `tailscaled` logged
out — while `mmcli` reports LTE attached at 100% signal. The modem's "connected"
does not mean the station has working connectivity.

**A separate, intermittent camera fault**, quantified below as 2 failed cycles
in 63. At the 21:30 wake, capture failed outright:

```
Error opening input file rtsp://admin:***@192.168.50.139:554/Streaming/Channels/101.
Error opening input files: Connection refused
[orc-capture] ERROR: All 3 attempts failed — no video delivered
```

This is intermittent, not constant: the 21:01 wake logged
`capture_result=delivered` and produced row 5697. Recorded as a distinct issue
from the upload outage; it is on the station's own LAN and cannot be a WAN
symptom.

**Battery: excluded** (`powercapture119s`, 22:00 UTC). The station's local CSVs
carry the whole curve, so this is measured rather than inferred. Today against
yesterday, hour by hour UTC:

| | 13:00 | 16:00 | 18:00 | 20:00 | 22:00 | overnight min | daily max |
|---|---|---|---|---|---|---|---|
| 09-02 (outage) | 12.688 | 12.702 | 12.668 | 12.657 | 12.656 | **12.559** | 13.160 |
| 09-01 (normal) | 12.726 | 12.769 | 12.702 | 12.781 | 12.713 | **12.592** | 13.098 |

The two nights are within ~0.1 V, and **yesterday reached the same overnight
minimum with no outage**. Today charged slightly higher at peak, so solar was
also fine. Voltage does not discriminate an outage night from a normal one, and
the power hypothesis — including the idea that a sagging rail explained the
camera's `Connection refused` — is dead.

**Capture: healthy.** 122 `delivered` against 2 failed cycles today (19:31 and
21:31 UTC, each logged twice); 36/36 delivered yesterday with no failures. The
camera fault is real but minor and **is not the outage**: 122 clips were
captured and delivered today, and none since 13:32 has synced.

**This is therefore an upload outage specifically** — not power, not capture.

### Correction to my own diagnostic

Section C of `todo119_outage_diag.sh` reported all 12 recent rows as `MISSING`.
**That check is unreliable and its result should be disregarded.** The `file`
column holds paths relative to an ORC-OS data root
(`videos/20260902/5697/20260902T210132.mp4`), and the script tested them with
`[ -e ]` against the SSH working directory, `/home/pi`. Independent evidence
says the files are there: the 21:01 wake logged `capture_result=delivered`, and
root usage is unchanged at 33 G. The check needs an absolute root before it
means anything.

## 4. What the server side settled

**`sensor-upload` is healthy.** Container up 8 days; `/sensors/health` returns
`{"ok":true,...}` in 12 ms from the host; an unauthenticated 64 KB PUT returns
`401` in 12 ms. This was checked because `time_starttransfer` was `0.000000` on
all 17 station attempts, which is also the signature of a wedged application
behind a working TLS listener. It is not wedged, so the station measurements are
evidence about the link.

**Only 0.54% of one payload ever arrived.** The server holds
`linkprobe-default-20260902T200045Z.bin.tmp` at **16,128 bytes** of a 3,000,000
byte payload. No probe transfer completed; there is no `upload ok` line for any
of them.

**nginx logs in `combined` format** — neither `$request_time` nor
`$request_length`. Upload durations and request sizes were never recorded, so
item C cannot be answered from these logs. Absence here means "not measured",
not "fast".

**43 × 201 and 2 × 500** on `/api/video/` in the whole retained log, arriving
one per wake at 30-minute spacing. Response bodies are 477 or 560 bytes.

## 5. Corrections to this session's own work

**Retracted: the ~167 KB/s throughput figure, and everything derived from it.**
It came from wake 1's single sample. Two further samples falsified it:

| | payload | handshake | post-handshake window | implied rate |
|---|---|---|---|---|
| wake 1 | 3 MB | 9.19 s | 17.51 s | 167 KB/s |
| wake 2 | 2 MB | 7.04 s | 17.04 s | 115 KB/s |

A 50% larger payload took 2.7% more time. The window was a fixed cutoff, so
dividing payload by it produced an artifact rather than a rate. The 17.3-hour
backlog estimate built on it falls with it.

The server-side evidence then falsified the underlying quantity as well: curl's
`size_upload` counts bytes handed to a socket, not bytes acknowledged on the
wire. Against 16,128 bytes actually received, `size_upload` was wrong by a
factor of 186.

**Retracted: the "37 successes vs 12 failures" contradiction.** Those were never
simultaneous. Every success predates 13:32 UTC; every probe ran at 20:00–21:00,
inside the outage. There was no contradiction to explain, and the framing was an
error of mine.

**The record's 5.2–5.5 s per 9.2 MB clip (1.74 MB/s) remains unverified.** It
enters the record in `580512a` as an assertion. No derivation exists in that
commit or in any of the 40 grabs under `data/station-forensics/`. This session
could not replace it with a measurement either.

## 6. What items B and C did settle

**B — NAT64 is not the cause, and the 464XLAT concern does not apply.**

```
wwan0 v4: 10.127.175.136/28          native, CGNAT
wwan0 v6: 2404:c0:2429:6bbf:.../64
CLAT interfaces: none
route to 34.203.227.187: via 10.127.175.129 dev wwan0
```

The station is genuinely dual-stack with a native IPv4 path. DNS64 is real
(`getent hosts` returns `64:ff9b::22cb:e3bb`), but every connection that
reported a peer used `34.203.227.187`. The two arms also inverted between
wakes: forced IPv4 failed 3/3 in wake 1 and was the only full-body push in
wake 2, while the default arm did the reverse. Failures hit both address
families and swap arms, so **a stateful translator dropping state mid-flow is
retired as the leading candidate.**

**The fault is not size-bound.** A 64 KB PUT failed the same way a 2 MB one
did, and 64 KB is smaller than a sensor CSV.

**Handshakes are consistently slow**, 4.4–9.2 s across the three wakes,
consistent with the 7.17–15.35 s measured on 09-02. The finding that a 7 s
handshake exceeds the hardcoded `timeout=5` at `callback_url.py:115` stands
unaffected by anything here.

## 7. Open

- **Cause of the WAN degradation.** The reclaim is exonerated; DNS failures and
  `network is unreachable` are now the visible symptoms, and nothing yet
  explains them. Whether this is the same fault as the 07-29 and 08-23
  blackouts is untested.
- **The camera's intermittent `Connection refused`** on RTSP. Separate from the
  upload outage, on the station's own LAN. Not investigated.
- **Whether the station recovers at sunrise.** The outage began at 20:32 WIB
  and has run through the overnight battery low. If it clears with daylight
  that points somewhere quite different from a link fault.
- **`sensor-upload`'s last `upload ok` is 2026-07-29**, yet `sensor_readings`
  carried rows through 2026-09-02 13:30. Both cannot be right. Unresolved.
- **Item C, throughput.** Not measured, and not measurable from nginx's current
  log format. Requires either a log format change or a completed timed transfer.
- **`station_gaps.py` infers station downtime from absent sensor rows.** Today
  shows absent rows can equally mean a working station whose upload path is
  dead. Prior "outages" in that report may merit re-reading with this in mind.

## 8. Litter to clean up

On the server, `/var/orc/sensors/sukabumi/linkprobe-default-20260902T200045Z.bin.tmp`
(16 KB). Inert — `sensor-ingest` globs `*.csv` against a strict filename regex
(`sensor-ingest/app.py:137`) — but it is mine and should be removed. Its
persistence also suggests the request handler never reached its cleanup path,
which is worth a glance if `.tmp` files accumulate.
