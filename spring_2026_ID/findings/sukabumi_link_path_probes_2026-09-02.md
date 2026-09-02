# Finding: the link is slow, not port-discriminated — and the station is on NAT64

**Status:** Measured on the station 2026-09-02 17:30 UTC, one wake, ~1 MB on the
wire. Two results contradict entries currently in TODO-119; see §6.
**Site:** Sukabumi → `openrivercam.endlessprojects.info`.
**Context:** TODO-119 Track 1, final step. The server side was cleared for zero
bytes (`sukabumi_sync_server_side_cleared.md`), leaving carrier action and a
path-MTU blackhole. These probes were meant to separate the two.
**Script:** `liveorc_server/station-health/todo119_path_probes.sh`.

---

## 1. The sharpest test came back negative

Three timed TLS handshakes to each port, same host, same address, same SIM,
within seconds of each other:

| attempt | :443 — the port that fails | :8443 — the port that never has |
|---|---|---|
| 1 | 7.50 s | 15.36 s |
| 2 | 7.17 s | 7.19 s |
| 3 | 15.35 s | 7.13 s |

**Indistinguishable**, down to each having one ~15 s outlier. Whatever is slow
is slow for both ports.

That eliminates per-flow carrier treatment of the video traffic, which was the
leading remaining hypothesis, and it independently confirms what TODO-119
already concluded from client configuration: *"443 vs 8443 is not an APN
question... the asymmetry is client config."* Two different methods, same
answer. `sensor-upload` survives the same link because it is configured to —
10 s timeouts and `--retry 5` — not because its traffic is treated differently.

## 2. The headline: a 7-second handshake against a 5-second timeout

Seven seconds to complete a TLS handshake is pathological, and it lands exactly
on the one timeout that cannot be configured:

```python
# orc_api/schemas/callback_url.py:115, get_set_refresh_tokens
response = requests.post(url, data=data, timeout=5)
```

**7 > 5.** The handshake alone exceeds it, which is precisely what the traceback
captured on 2026-09-01: the innermost orc_api frame at `get_set_refresh_tokens`,
with the urllib3 frames above it ending in `do_handshake` — dead before any HTTP
request was sent, no video bytes moved.

The innermost-frame tally for 08-23→08-28 was **139 at `get_set_refresh_tokens`
against 78 at the data POST**. So this measurement quantitatively accounts for
roughly **64% of the failures**.

**This corrects TODO-119.** That entry says raising the hardcoded 5 "is not
sufficient and may not help." On this evidence it would address the majority of
failures. It would still do nothing for the 75 `ConnectionReset`s, which is why
the entry's underlying caution stands even though its conclusion does not.

## 3. The station is on NAT64 — the record says otherwise

```
route to server: 64:ff9b::22cb:e3bb  dev wwan0
source:          2404:c0:2444:c95d:5a2c:80ff:fe13:9208
```

`64:ff9b::/96` is the well-known NAT64 prefix (RFC 6052), and the low 32 bits
`22cb:e3bb` decode to **34.203.227.187** — the server's IPv4 address. The
station therefore resolves this host through DNS64 and reaches it over IPv6
through a stateful translator.

TODO-119 records the opposite, as a tested and closed question: *"NAT64/IPv6 was
proposed, tested and killed... The station resolves this host to IPv4 only."*

One of the two is wrong, and this one is a direct reading of the routing table
rather than an inference. What may reconcile them: `getent hosts` returns the
first match and will prefer a synthesized AAAA where one exists, so an earlier
test that forced `--ipv4` would have measured a genuinely different path and
found it no better — without that establishing which path is used by default.

**Why it matters.** A stateful NAT64 translator sits in the path of every video
upload. Translation state that is dropped or reaped mid-flow produces exactly
`ConnectionReset` and `RemoteDisconnected` — the 93 failures that no timeout
value fixes and that nothing so far has explained. This is now the leading
candidate for that half of the problem.

## 4. A 1 MB upload did not survive

```
1 MB POST to :443 -> 000, 0 bytes uploaded, in 7.2 s
```

curl `000` is no response at all. A ninth of a clip failed to transfer while the
station was otherwise syncing at ~87% that day. Consistent with the failure
being intermittent per-connection rather than a steady bandwidth limit.

## 5. Ruled out or unmeasurable

| | |
|---|---|
| **Radio quality** | Not the problem. LTE, connected, packet service attached, signal 100%, Telkomsel (51010) |
| **Path MTU** | **Unmeasured.** No DF-set ping of any size returned, so ICMP is filtered. Common on mobile networks and not itself a finding |
| **Interface MTU** | wwan0 1500, eth0 1500, wlan0 1500, tailscale0 1280 — nothing anomalous |

A path-MTU blackhole remains possible and untested. It would fit the handshake
stalls; it would **not** explain the resets.

## 6. An unresolved tension, stated rather than smoothed

TODO-119 records successful syncs taking **5.2–5.5 s for a 9.2 MB clip**
(~1.74 MB/s). If a handshake alone now costs 7 s, both cannot describe the same
link. Possibilities, none verified:

- the 5.2 s figure excluded connection setup
- connections were being reused across clips, amortising the handshake
- the link's latency is materially worse now than in August, despite a higher
  success rate today (87%) than then (~14%)

This matters because the 1.74 MB/s figure underpins every throughput estimate
made so far, including the five-day upload projection. It should be re-measured
before being relied on again.

## 7. Where Track 1 now stands

| Candidate | Status |
|---|---|
| Server-side refusal, size cap, fail2ban, firewall | **Eliminated** — see the server-side finding |
| Per-flow carrier treatment of :443 | **Eliminated** — :8443 is identically slow |
| Client timeouts too short for a 7 s handshake | **Confirmed**, accounts for ~64% of failures |
| Stateful NAT64 dropping translation mid-flow | **Leading candidate** for the remaining ~36% |
| Path-MTU blackhole | Possible, unmeasured, cannot explain the resets |
