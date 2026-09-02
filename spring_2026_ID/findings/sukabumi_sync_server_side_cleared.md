# Finding: the sync failures are not server-side

**Status:** Measured on the LiveORC host 2026-09-02. Conclusive for the period
the logs cover; see §5 for what they do not cover.
**Site:** Sukabumi → LiveORC (`openrivercam.endlessprojects.info`).
**Context:** TODO-119 Track 1 — what interrupts the station's uploads. Three
explanations fitted the evidence and none was excluded: carrier action on the
traffic, a path-MTU blackhole, or something server-side. **This eliminates the
third**, for no metered bytes.
**Author:** analysis by Claude, run on the host by Tom Jordan.

> Why this mattered enough to check first: a self-inflicted block — fail2ban, a
> request size cap, a rate limit — is completely invisible from the station. It
> would look exactly like a bad link, and we would have spent the SIM chasing it.

---

## 1. Four candidates eliminated

| Candidate | Finding |
|---|---|
| **Request size cap** | `client_max_body_size 512M`, set explicitly in all four nginx configs (`nginx.conf`, `nginx-ssl.conf` and both templates). The 1 MB default never applied. **This was the leading hypothesis and it is wrong.** |
| **fail2ban ban** | `fail2ban-client` is not installed |
| **Host firewall** | `iptables -S` carries nothing but Docker's own chains |
| **Server refusing or failing** | Every video POST in the covered window returned **201** |

nginx *is* in the request path — master process on `:8000` (SSL) and `:8080`,
proxying to gunicorn over `unix:/tmp/liveorc.sock`. Host 443 → nginx → gunicorn.
Worth stating because `liveorc_webapp` maps 443 to container port 8000, which
conventionally suggests gunicorn direct and would have made nginx's config
irrelevant.

## 2. The number that settles it

Cross-referencing nginx's log against the station's own `sync_status` tally for
the same period:

| | Server logged | Station recorded |
|---|---|---|
| Last 2 days | **37 × `/api/video/` 201** | **37 SYNCED** (11 on 09-01, 26 on 09-02) |
| Same period | 2 × `/api/video/` 500 | ~25 FAILED |

**The successes match exactly. The failures almost entirely do not appear at
all** — roughly 23 of ~25 produced no log line, no status code, nothing. The
connection died before the request completed.

That is transport failure, not server refusal, and it matches the error profile
already measured on the station for 08-23→08-28: 75 `ConnectionReset` and 18
`RemoteDisconnected` against **zero** `ConnectTimeout`. Connections are being
established and then torn down mid-flight.

The same shape holds in the 08-27 slice the log reaches: 6 arrivals, 6
successes — and the station recorded exactly 6 SYNCED that day, in the
18:00–22:00 UTC band the log covers.

## 3. Nothing was refused

No `413`, no `499`, no `502/503/504`, no "reset by peer" or "client closed" in
the window. The server neither rejected a request nor gave up on one.

## 4. One genuine server-side item

**2 × `/api/video/` → 500** in the last two days. Small against 37 successes,
but those are real server errors on video upload rather than transport, and they
are the only server-side defect this found. Worth identifying separately; they
are not the cause of the backlog.

## 5. What this does NOT cover

**The log begins 2026-08-27 16:25:19 UTC**, when the container was started —
almost certainly the EBS media migration (`MEDIA_VOLUME_RUNBOOK.md`). The
failure window opened on **08-23**, so only its final ~7.5 hours are visible.

So the honest claim is: the server behaved correctly throughout the slice we can
see, and the failure signature in that slice is identical to the current one.
It is **not** proof that the server behaved correctly on 08-23 itself. Nothing
survives from that date to check, and nothing will — `json-file` with no rotation
options keeps only what has accumulated since the last container start.

If a future window matters, the log driver is the thing to change first.

## 6. What remains

Carrier action on the traffic, and a path-MTU blackhole. Both are station-side
questions now, and both are answerable for roughly 20 KB:

- interface MTU against real path MTU, by `ping -M do` binary search
- a timed `openssl s_client` handshake to :443
- the same to :8443, where `sensor-upload` has never had this problem

The last comparison is the sharpest available: same host, same address, same
SIM, different port and different client settings — and one works while the
other does not.
