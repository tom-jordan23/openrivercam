# Sukabumi upload failures: what the nine post-outage failures actually were

**Date:** 2026-09-03
**Evidence:** `failreasons119z1/z2/z3`, three station wakes at 16:30, 17:00 and
17:30 UTC, plus the 16:00 dry run. Read-only throughout; nothing was written to
the station and nothing was synced.

## Summary

The 09-02 outage cleared on its own at about 01:30 UTC on 09-03. In the fifteen
hours after it, nine video syncs failed. They are not one fault. They are three,
and only one of them is the fault the remedy chosen on 2026-09-03 addresses.

The failure rate is also no longer what the record says. It is currently zero.

## The counters

| read | time UTC | SYNCED | FAILED |
|---|---|---|---|
| dry run | 16:00 | 2596 | 3012 |
| z1 | 16:30 | 2597 | 3012 |
| z2 | 17:00 | 2598 | 3012 |
| z3 | 17:30 | 2599 | 3012 |

`FAILED` did not move across four reads spanning ninety minutes. Every capture
from 12:31 to 17:30 synced — eleven consecutive, six hours.

The "20 synced, 17 failed, ~46%" in the resume block was measured across a
window that still contained the outage. Post-outage the rate is 8 failures in
29 captures to 12:01, and nothing since. One window was not a rate, and neither
is this one; what can be said is that the 46% figure describes the outage, not
the present.

## The nine failures, by mechanism

| time UTC | innermost frame | mechanism |
|---|---|---|
| 01:31:51 | `callback_url.py:115` | token refresh |
| 02:01:57 | `callback_url.py:115` | token refresh |
| 02:32:02 | `callback_url.py:115` | token refresh |
| 03:01:53 | `callback_url.py:115` | token refresh |
| 03:32:00 | `callback_url.py:115` | token refresh |
| 06:04:17 | `callback_url.py:172` | time-series sub-sync |
| 07:31:58 | none | server refusal, status discarded |
| 10:31:56 | none | server refusal, status discarded |
| 12:02:03 | `callback_url.py:172` | time-series sub-sync |

### 1. The token refresh — five failures, and they are a post-outage tail

`get_set_refresh_tokens` POSTs with a hardcoded `timeout=5`
(`schemas/callback_url.py:115`) and advances `token_expiration` **only on
success**. A refresh that times out leaves the timestamp untouched, so the next
request refreshes too.

All five sit in the 01:31–03:32 window, immediately after the outage cleared.
The reading that fits: the token went stale during the outage, each wake paid
the five seconds and failed, and one finally got through before 04:31, which
synced. The healthy cadence then resumed — the row read at 16:30 showed
`created_at = 14:31:55` with expiry 19:31:55, and the refresh before it lands on
the 09:31 wake. Five hours apart, exactly as `get_token_expiration` intends.

**This is a recovery cost, not a steady-state fault.** It costs roughly four or
five clips after each outage and nothing in between.

The record's "64% of historical failures at `callback_url.py:115`" was measured
over 08-23→08-28, which was itself an outage window. The same tail would
dominate that tally. Whether the 64% is steady-state or another recovery
artefact has not been tested and should not be assumed either way.

### 2. The time-series sub-sync runs at five seconds — two failures

The station's own traceback, verbatim:

```
File ".../orc_api/schemas/video.py", line 388, in sync_remote
    self.time_series = self.time_series.sync_remote(session=session, site=site)
File ".../orc_api/schemas/time_series.py", line 83, in sync_remote
    response_data = super().sync_remote(session=session, endpoint=endpoint, json=data)
File ".../orc_api/schemas/base.py", line 35, in sync_remote
    r = callback_url.post(endpoint=endpoint, data=data, json=json, files=files, timeout=timeout)
File ".../orc_api/schemas/callback_url.py", line 172, in post
    return requests.post(url, headers=self.headers, json=json, data=data, files=files, timeout=timeout)
requests.exceptions.ReadTimeout: ... Read timed out. (read timeout=5)
```

`time_series.sync_remote` calls `super().sync_remote` **without a timeout**, so
`base.py`'s default of 5 applies. The 150 seconds the video path computes at
`video.py:387` never reaches it.

The sub-sync runs **before** the video file is uploaded. When it times out the
clip is marked FAILED without the video ever being attempted — so these two
failures cost a clip each while transferring almost nothing.

This is a third, independent five-second timeout, and it is not the one at
`:115`. Raising or passing a timeout here is a separate change from anything to
do with tokens.

### 3. Two uploads reached the server and LiveORC returned 500

**Answered from the host, 2026-09-03.** The station's requests arrived. LiveORC
threw an unhandled server error on both:

```
[03/Sep/2026:07:31:58 +0000] "POST /api/video/ HTTP/1.0" 500 145 "-" "python-requests/2.32.3"
[03/Sep/2026:10:31:56 +0000] "POST /api/video/ HTTP/1.0" 500 145 "-" "python-requests/2.32.3"
```

Excluded by the same run: `client_max_body_size` is **512M**, not nginx's 1 MB
default; `proxy_read_timeout` is 300000s; there is no fail2ban and no rate
limiting. This is not a refusal, a size cap or a proxy timeout. It is our own
application erroring, and it has nothing to do with the link, the SIM or any
timeout.

**The rate, over 14 days of `POST /api/video/`: 68 × 201 and 4 × 500 — 5.6%.**

```
02/Sep/2026:07:31:52    03/Sep/2026:07:31:58
02/Sep/2026:09:31:52    03/Sep/2026:10:31:56
```

Two per day on both days. Flat, so it is a property of the upload rather than
an incident with a start and an end. **At that rate the 1,190-clip re-drive
meets it about 66 times**, having spent the metered bytes each time to do so.

All four land at `:31` past the hour. The station wakes at `:01` and `:31`, so
roughly half of uploads occur at `:31` anyway and four out of four is about a
1-in-16 coincidence. Suggestive, not significant at n=4. Worth re-checking once
there are more.

Not yet known: **what the exception is.** `docker logs liveorc_webapp` carries
only the access line — no traceback, no exception class. With `DEBUG=False` and
no `LOGGING` config Django routes `django.request` errors to `mail_admins`
rather than the console, and gunicorn's stderr is not arriving either.
`liveorc-host/find-500-traceback.sh` looks for where it went.

### 3b. How the reason was destroyed on the station side

`schemas/base.py:47`:

```python
raise ValueError(f"Remote update failed with status code {r.status_code}, detail: {r.json()['detail']}")
```

On a non-2xx response whose body is not JSON — an nginx error page, for
instance — `r.json()` raises `JSONDecodeError`, which replaces the `ValueError`
and takes the status code with it. The log records only
`Expecting value: line 2 column 1 (char 1)`.

From the station there was no way to tell a 500 from a 502 from a 413 — the
status code never reached the log. It took a server-side read to recover it,
which cost no metered station bytes.

**This is the more consequential half of the finding.** A 5.6% server-side
error rate was invisible from the station for as long as anyone has been
looking at these failures, because ORC-OS reports it as a JSON parse error.
Every previous tally counted these as transport failures or did not count them
at all.

This class appears in no historical tally, because nothing has previously
looked for it under that error text.

## What this means for the chosen remedy

Token freshness was chosen on 2026-09-03 over patching the station's
site-packages, on the grounds that a version upgrade silently reverts an
upstream edit. That reasoning is unchanged and the route is still the right one
for what it covers.

What has changed is what it covers: **five of nine failures, all of them the
tail after an outage.** It does not reach the time-series timeout and it does
not reach the refusals. It is worth doing, and it is not sufficient on its own.

Note also that the two remaining mechanisms both live in upstream
site-packages, so the argument that killed the `:115` patch applies to them
equally. Neither can be fixed on the station without the same silent-revert
exposure.

## What is not established

- Whether the 64% historical figure is steady-state or a recovery artefact.
- What the server returned at 07:31:58 and 10:31:56.
- Whether the time-series five-second timeout fires often enough to matter
  outside a degraded link. Two instances in fifteen hours is not a rate.
- `newt`, the Pangolin tunnel client, fails DNS resolution three times at
  boot+21/24/27s on **every** wake observed (15:00 through 17:30 without
  exception). Different host from the upload path, so not the same fault. It
  poses a question worth testing: video sync starts at boot+60s, and if the
  resolver is not ready twenty seconds into a wake, some read timeouts may be a
  station still coming up rather than a policed link.

## Correction

The first pass at this pairing reported `frame=none` for eight of the nine
failures, which would have retired the token route outright. That was a bug in
the analysis script, not a finding: it searched only 80 lines past each error
line, and a `requests` `ReadTimeout` logs a chained traceback whose
`callback_url` frames sit further down. Raising the cap to 400 produced the
table above. The aggregate tally it appeared to contradict was right all along.
