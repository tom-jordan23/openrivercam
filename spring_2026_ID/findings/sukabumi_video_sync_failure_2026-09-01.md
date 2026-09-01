# Sukabumi video sync: what three station grabs found

**Date:** 2026-09-01
**Session:** 21:30–22:02 UTC, across two station wake cycles
**Status of the station:** healthy, on its 30-minute cadence throughout
**Everything below was read-only.** Nothing on the station was changed and no
upload was started.

---

## The bottom line in one paragraph

3,104 videos have never reached the LiveORC server. For three sessions the
working theory was that a five-second timeout was cutting the uploads off too
early, and that finding which line of code carried that five would point at a
one-line fix. We found the five. It is real. **It is not what is breaking the
uploads.** Roughly half the failures are not timeouts at all — they are the
connection being actively killed — and a fifth of them had already waited a
full 150 seconds before giving up. Making the client more patient will not fix
this, because the client is not being impatient.

---

## What was actually run

Three small scripts, each waiting for the station to wake up and then running a
handful of read commands over SSH before it went back to sleep. The station is
only awake about two minutes in every thirty, so each script had to catch its
window.

| Script | Wake | Got back | What it asked |
|---|---|---|---|
| `todo119_sync_source_grab.py` | 21:30 UTC | 20.5 KB | A full error traceback, and whether a re-upload endpoint exists |
| `todo119_redrive_viability.py` | 22:00 UTC | 4.1 KB | The timeout setting in the database, and a tally of all failures |
| `todo119_timeout_split.py` | 22:01 UTC | 1.3 KB | The actual timeout *values*, and the station's clock setting |

The first of these had been written in the previous session and killed before it
could run. It ran this time.

Raw output is in `data/station-forensics/`, files named `*119c*`, `*119d*`,
`*119e*`.

---

## Finding 1: We found the five-second timeout

It lives in the upstream ORC-OS library, in a function that refreshes the login
token before making a request:

```
orc_api/schemas/callback_url.py, line 115
    response = requests.post(url, data=data, timeout=5)
```

Every upload request first checks whether its login token has expired, and if so
calls this function to get a new one. That call is hardcoded to five seconds and
ignores whatever timeout the caller asked for.

**But the traceback shows something more specific.** The failure happens inside
the *TLS handshake* — the encrypted-connection setup that happens before any
actual request is sent. So on those attempts, no video data moved at all. The
station never got as far as trying to send a file.

---

## Finding 2: The timeout is not the fault

This is the finding that changes the picture. Counting every failed sync between
23 and 28 August:

| What went wrong | How many | What it means |
|---|---|---|
| `read timeout=5` | 85 | Gave up after 5 seconds |
| `ConnectionReset` | 75 | **Something killed the connection** |
| `read timeout=150` | 19 | **Gave up after 150 seconds** |
| `RemoteDisconnected` | 18 | **The other end hung up** |
| `SSLError` | 4 | Encryption setup failed |
| `ConnectTimeout` | **0** | Never once failed to make contact |

**201 failures. 97 of them — 48% — are the connection being torn down, not timing
out.** No timeout value fixes those. And 19 of the remaining ones had already
waited 150 seconds, which is two and a half minutes for something that normally
takes a fraction of a second.

So the one-line fix that this investigation was hoping for would, at best,
address 85 of 201 failures — and we have direct evidence that some of those
would fail anyway, because 19 already did at 30 times the patience.

---

## Finding 3: The upload already had 150 seconds

The code picks its timeout like this:

```python
timeout = min(retry_timeout, 150) if retry_timeout else 150
```

The database has `retry_timeout = 0.0`. In Python, zero counts as "empty" in an
`if`, so this falls through to the `else` branch and the answer is **150**.

This matters because we had been worried the setting might be silently clamping
uploads down to 5 seconds. It is not. The upload path has had 150 seconds all
along. The only thing running on 5 seconds is the token refresh from Finding 1.

---

## Finding 4: There is a re-upload button, and it is reachable

The station runs its own small web API. It exposes:

```
POST /api/video/sync/     (start, stop, site)
```

which re-attempts every failed video in a date range, at the full 150-second
timeout. It is served on port 80 and requires a login (an unauthenticated test
request returned `401`, which confirms it is live).

**This means the backlog can be retried without hand-editing the database.**

Why it has never happened on its own: the boot-time scheduler only asks for
videos marked `QUEUE`, which is the crash-recovery category. It never asks for
`FAILED`. That is why every boot logs "0 videos left to synchronize" while 2,978
failed videos sit there. The log line was answering the question it was asked.

---

## Finding 5: The station's clock is set to UTC, not local time

`timedatectl` confirms UTC, with time sync active.

This has consequences well beyond this investigation. **Every timestamp read off
the station — system logs, application logs, the power-scheduler log — is in UTC
and needs 7 hours added to become Jakarta time.** Server-side queries are the
opposite: they already convert to Jakarta time explicitly.

I got this wrong myself earlier in the session. I read a failure logged at
04:02:58 as being 4am Jakarta time, which would have placed it right at the edge
of the nightly window where uploads were known to succeed, and I flagged it as
possibly a special transition case. It is 11:02 Jakarta time — an ordinary
mid-morning failure, entirely typical. The sample was more representative than I
said, not less.

**Any earlier conclusion that quotes a Jakarta time taken straight from a station
log is displaced by seven hours.** I have flagged this but not audited which
past claims are affected.

---

## What this looks like in plain network terms

Making a secure connection has three stages:

1. **Make contact.** A short exchange of three small packets to establish the
   connection. Tiny, fast.
2. **Set up encryption** (the "TLS handshake"). The server sends its security
   certificate, which is several kilobytes — the first time any real volume of
   data moves.
3. **Send the actual request.** For us, the video file.

Our failures cluster at stage 2, and stage 1 succeeded **every single time in
five days**. That is informative:

- **Stage 1 always working** rules out the boring explanations. The station is
  reachable, the address resolves, the server is up and accepting connections,
  nothing is blocking traffic outright.
- **Dying at stage 2** is notable because it is both the first point where a
  meaningful amount of data flows *and* the first point where the traffic
  becomes identifiable — the hostname being contacted is sent unencrypted at the
  start of this stage. Equipment in the middle of the network that wants to make
  a decision about your traffic makes it here.
- **"Connection reset" means something sent a deliberate kill signal.** A weak
  or congested mobile signal produces slow transfers and timeouts. It does not
  produce resets. Resets are an action, not a degradation.
- **150 seconds of waiting, then nothing.** Whatever this is, the station was
  not being hasty.

Put together: the connection is established, then either starved of data or
deliberately terminated. That is the shape of something in the network path
acting on this traffic — not the shape of a client that gives up too early.

---

## Where I am less certain

I described this as a "policed link" in conversation. That names a culprit, and
the evidence only establishes a *pattern*. Something actively terminates or
starves these connections after contact is made. **Who or what does it is not
established.** At least three explanations fit:

1. **The mobile carrier acting on the traffic** — blocking or throttling based
   on the destination, or throttling because a data allowance is exhausted. This
   would fit the recorded pattern of uploads only working in a narrow window
   each night.

2. **A network path problem with packet sizes** (a "PMTUD blackhole"). This one
   I initially under-weighted, and it deserves attention. Stage 1 uses tiny
   packets and always works. Stage 2 is the first time full-size packets are
   sent. If the network path cannot carry packets as large as the station
   thinks, and the error messages that would normally report this are being
   filtered, those large packets vanish silently. The result looks exactly like
   what we see: contact succeeds, encryption setup hangs, timeout. This is
   common on mobile links, and this station also runs Tailscale, which adds
   overhead that makes it more likely. **This is a plumbing fault, not anyone's
   policy.**

3. **Something at the server end** — rate limiting, an intrusion-blocking tool,
   or a firewall rule on the AWS host.

Explanation 2 has one clear weakness: it produces hangs, not resets, so it does
not account for the 75 connection resets. It may well be that two things are
going on at once.

---

## The test that would separate these

The station talks to the **same server** on two ports: port 443 for video
(failing) and port 8443 for our own sensor-data uploader. Same route, same
mobile signal, same packet sizes during encryption setup.

If sensor uploads on 8443 were succeeding during 23–27 August while video on 443
was failing, then explanations 2 and any general "bad signal" theory are largely
ruled out — neither can tell one port from another. That would point firmly at
something acting on the specific destination, or a difference between the two
listeners on the server.

**One caveat before relying on this.** The existing record says sensors were
*logging* 48 readings a day through the window. Logging is local; it is not proof
that uploads were getting through. Sensor readings keep their original
measurement timestamp, so a reading uploaded three days late still files itself
under its original time — a per-day count cannot distinguish "uploaded then"
from "backfilled later." Settling this needs a column recording when each row
*arrived*, which I have not yet checked for.

---

## Corrections to the existing record

- **Commit `580512a`** recorded that "bytes were moving; the failures land
  mid-transfer" and withdrew the earlier token-refresh explanation. That
  withdrawal was wrong for half the picture: 139 failures do die at token
  refresh, before any request is sent. Its mid-transfer reading was right for
  the other half. Both halves are real.
- **My own reading of the 04:02:58 sample** as sitting at a nightly boundary was
  wrong, for the timezone reason in Finding 5.
- **The traceback in grab 119c is fragmented.** The search that captured it
  matched twice and skipped the lines between, so some frames are missing. The
  innermost captured frame is still the encryption handshake, so the conclusion
  holds, but it is not a clean single traceback.

---

## Where things stand

**Current backlog:** 2,978 failed, 126 local, 2,546 successfully synced.
Unchanged during the session — nothing is draining on its own.

**Still open:**

- Whether the re-upload endpoint survives the *network*, as opposed to merely
  existing in the code. It is reachable and runs at 150 seconds, but 19 failures
  already had 150 seconds and 97 were resets. Only a real attempt measures this.
- Which past Jakarta-time claims were derived from station logs without the
  7-hour correction.
- Whether the sensor table records an arrival time, which would settle the
  443-versus-8443 test above.

**Decision needed from you:** whether to fire the re-upload endpoint against a
small date range as a test. It would change station state and spend metered
mobile data on the same prepaid SIM whose exhaustion caused the 4.8-day outage
in ISS-FIELD-011. I have not done this and will not without a decision.

**A note on the likely remedy.** Raising the hardcoded 5 to something larger is
a one-line change, but it sits in the upstream ORC-OS library, which we do not
modify because a version upgrade would overwrite it and the station and server
have to move versions together. Given that it would address at most 85 of 201
failures, and that some of those would fail anyway, it is not worth breaking
that rule for.

---

## Files

| What | Where |
|---|---|
| Raw grab output | `data/station-forensics/orc-sukabumi-{backlog119c,redrive119d,timeoutsplit119e}-*.txt` |
| The scripts | `liveorc_server/station-health/todo119_*.py` |
| Issue entry | `ISSUE_LOG.md` → ISS-FIELD-012 |
| Task entry | `TODO.md` → TODO-119 |
| Commit | `6f1c0dc` |
