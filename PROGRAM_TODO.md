# PROGRAM TODO — transition, collaboration, and next-generation hardware

**Last updated:** 2026-09-03

This file tracks moving this system onto a footing that does not depend on
American Red Cross or on Tom, the collaboration now underway with IPB and BHLK,
and the next-generation hardware specification.

Day-to-day station and server operations stay in
[`spring_2026_ID/TODO.md`](spring_2026_ID/TODO.md) (TODO-101…199). The two files
do not overlap. If an item is about keeping the deployed station producing data,
it belongs there; if it is about what other institutions do with this work, or
about the system outliving this grant, it belongs here.

| Track | Numbers |
|-------|---------|
| **Transition** — funding, hosting and ownership move off American Red Cross | TODO-201…299 |
| **Next-generation hardware** — the v2 design specification | TODO-301…399 |
| **Collaboration** — joint work with IPB and BHLK, now live | TODO-401…499 |

## Where this came from

The organising commitments are in the PMI / IPB / BHLK thread of 19 August –
3 September 2026 (Teguh Wibowo's meeting minutes, Dewi Ariyani's update of
2 September, and Tom's reply of 3 September). What was agreed or stated there:

- **PMI and IPB have agreed three areas of collaboration** — IPB analyses the
  ORC data, integrates its own rain gauges, and builds a community-facing
  dashboard.
- **IPB installed three sets of rain gauges on 22–23 August 2026.**
- **IPB has requested ORC API access. Tom has committed to providing it.** The
  PMI gate recorded in TODO-104 is therefore open for IPB.
- **BHLK wants to see the device, inside the box included, and has asked for the
  GitHub installation guidance.** They are interested in replication.
- **BHLK measured river discharge at Sukabumi on 21 August 2026** and wants to
  compare it against ORC output from the same period.
- **BHLK suggests captures of around 45 seconds** rather than the present 5.
- **BHLK has offered server capacity for ORC.**
- **Tom has stated in writing that all project materials are freely shareable** —
  code, documentation, build notes, installation instructions — and that access
  to the devices and their data is PMI's decision.
- **Tom has told PMI the current server cannot be sustained past the end of the
  grant**, and recommended following up on BHLK's server capacity soon. *Softer
  in practice (Tom, 2026-09-03): American Red Cross can extend the server a
  little. The real objective is not a deadline — it is **a funding model that
  does not depend on American Red Cross**, and **freeing Tom's time**.*
- **Relocating the Sukabumi station is under discussion.** Tom has asked whether
  it is likely; unanswered as of 2026-09-03.
- **Real-time monitoring argues for AC mains**, agreed 20–21 August: the Jakarta
  station will not be converted to solar.

## The objective

Two things, and most items below are worth ranking against them:

1. **A funding and operating model that does not depend on American Red Cross.**
   Not a shutdown deadline — the grant ends 31 December 2026 and American Red
   Cross can carry the server about three months past that, six at the outside.
   The work is finding who pays for and runs this next, and moving it there
   deliberately rather than at the end. **Who pays is currently unowned, and it
   is PMI's to own** — TODO-213.
2. **Reducing what only Tom can do.** American Red Cross wants his time freed.
   Every dependency on one person — a credential, an undocumented procedure, a
   judgement nobody else can make — is a thing to transfer or write down.

These reframe the deadline. Little here is a cliff; most of it is a handover
that gets harder the longer it waits, and a set of single points of failure that
are currently a person rather than a component.

## Priority

The constraint is the transition, not a data outage, so this file uses its own
ladder. Do not read these as the P0–P2 in `spring_2026_ID/TODO.md`, which mean
something different.

| Priority | Meaning |
|----------|---------|
| **G0 · November** | Needs PMI to spend. Must be committed before ~30 Nov 2026. |
| **G0 · December** | Needs Tom. Must land before the grant ends, 31 Dec 2026. |
| G1 | Should land before the grant closes |
| G2 | Hand to the successor as a documented open item |

The two G0 tiers are split by *what* the deadline is made of, not by importance.
November is a money deadline; December is a people deadline. An item can be
blocked by either.

| Status | Meaning |
|--------|---------|
| OPEN | Not started |
| IN PROGRESS | Work underway |
| PARKED | Waiting on an external dependency |
| DONE | Complete |

**Planning horizon (Tom, 2026-09-03).** There are four dates, and they are not
the same deadline:

| Date | What ends | |
|---|---|---|
| **~30 Nov 2026** | **PMI wraps up grant expenditures** | **The binding one.** Anything needing PMI to spend — travel, procurement, contracted survey, a site visit — has to be done or committed by here. |
| **31 Dec 2026** | Grant ends | End of calendar 2026. |
| **31 Mar 2027** | AmCross server carry, planned | 3 months past the grant. **Do not depend on more than this.** |
| **30 Jun 2027** | AmCross server carry, outer bound | Do not build a plan that needs it. |

**End of November is the deadline that actually constrains this file**, and it
is under three months away. It gates every item with a physical or travel
component: the in-country training and design walkthrough (TODO-210), the
Sukabumi relocation if it happens (TODO-212), getting the Jakarta station in
front of IPB and BHLK (TODO-211), field photographs (TODO-206), and any
contracted survey work. Documentation and software items are not gated by it.

Anything depending on the current server has to be resolved by **March 2027**,
June 2027 at the outside. Working back: a migration decided in January is
comfortable; one decided in March is not a migration, it is an evacuation.

**The two 2027 dates are fungible if new funding appears** — see TODO-213, which
is the item that decides whether they move. **End of November is not**, unless
PMI's expenditure window itself moves.

Read G0 as "the lead time is long enough that starting late means not
finishing", not as "the money stops that day".

## How this file relates to the recommendations

[`spring_2026_ID/docs/RECOMMENDATIONS.md`](spring_2026_ID/docs/RECOMMENDATIONS.md)
is the source of record for **R1–R37**. This file schedules those
recommendations; it does not restate them. Items cite the R-numbers and `ISS-*`
identifiers they discharge.

---

## G0 · November — anything that needs PMI to spend

**Deadline: ~30 November 2026, when PMI closes grant expenditures.** Under three
months away. If it needs money — travel, procurement, a contracted survey, a
site visit — it has to be committed by here or it does not happen on this grant.

Two G1 items and one G2 item share this gate rather than the December one:
**TODO-211** (Jakarta station in front of IPB and BHLK), **TODO-206** (field
photographs), and **TODO-212** (Sukabumi relocation). They sit lower because
they are less certain, not because they have longer.

### TODO-210: Hands-on training and the design walkthrough

| Field | Value |
|-------|-------|
| **Status** | OPEN |
| **Priority** | G0 · November |
| **Opened** | 2026-09-03 |

Tom has offered two things in the thread: a **meeting walking IPB and BHLK
through the design**, and **training someone in-country on hands-on operation**,
the latter tied to a possible Sukabumi relocation visit.

Both are the parts of a handover that documentation cannot carry, and they are
the clearest single transfer of what only Tom can do.

**This is the most time-critical item in the file.** In-country training needs
travel, travel needs PMI grant money, and **PMI closes grant expenditure around
30 November 2026** — under three months out, before visas, scheduling and
permissions are accounted for. If it is going to happen on this grant, it has to
be committed now, not planned now.

**Steps:**
- [ ] Schedule the design walkthrough. BHLK asked to see inside the box; the
      Jakarta station is the unit to do it with (TODO-211).
- [ ] Identify who is being trained and what they must be able to do
      unsupervised — the operator guide and troubleshooting doc define the
      floor.
- [ ] Tie the visit to the relocation if it happens (TODO-212).
- [ ] Capture field photographs while in country (TODO-206).

---

---

### TODO-213: Get funding continuity owned by PMI

| Field | Value |
|-------|-------|
| **Status** | OPEN — unowned |
| **Priority** | G0 · November |
| **Opened** | 2026-09-03 |

**Nobody currently owns the question of who pays for this after the grant.**
That is the single largest open risk in this file, and it is not a technical
one.

Tom's position (2026-09-03): he does not know whether a second round of this
grant is possible, or whether other funding lines could sustain the work.
**He is not the right person to know.** Sustaining funding is a PMI
responsibility, and it has not yet emerged as anyone's assigned task.

Everything else in this file is planned against the 3-month assumption above.
If PMI finds a funding line, the 2027 dates move and several items relax. If
nobody looks, they hold by default and the archive option in TODO-208 becomes
the outcome — not because it was chosen, but because nothing else was.

**The November expenditure close makes this urgent rather than merely
important.** If a second round or another line exists, knowing before PMI closes
its books is worth far more than knowing after: it is the difference between a
funded site visit this year and a conversation about one next year.

**Steps:**
- [ ] Raise it explicitly with PMI, naming it as a decision they own rather
      than a status question. American Red Cross freeing Tom's time is part of
      the same conversation and makes the ask concrete.
- [ ] Get a named owner at PMI. An organisation is not an owner.
- [ ] Establish whether a second round of this grant is a real possibility, and
      who would write it.
- [ ] Ask what other lines exist — BHLK and IPB both have institutional
      funding routes, and BHLK's server-capacity offer is itself a partial
      answer to the hosting half.
- [ ] Set a date by which "no funding identified" becomes the working answer,
      so TODO-208 can be decided on something firmer than hope.
- [ ] Record the answer here. This question will otherwise be re-asked every
      few months and answered afresh each time.

**Related:** TODO-208 (the hosting decision this gates), TODO-205.

---

---

## G0 · December — anything that needs Tom

**Deadline: 31 December 2026, when the grant ends and Tom's time with it.**

Note the mismatch this creates: **the server is carried to roughly 31 March 2027,
but the person who can migrate it is funded only to 31 December.** Infrastructure
outliving the engineer is not a reprieve. Anything below that needs Tom's hands
has a December deadline regardless of how long the hardware survives, and
TODO-208 is the sharpest case — deciding the server's home in February is
useless if nobody is left to move it.

### TODO-208: Move the server to a home that does not depend on American Red Cross

| Field | Value |
|-------|-------|
| **Status** | OPEN |
| **Priority** | G0 · December |
| **Opened** | 2026-09-03 |
| **Trigger** | Tom to PMI, 2026-09-03, and the funding-model objective above |

**Not a cliff, but bounded.** American Red Cross can carry the AWS host past the
grant — **plan on 3 months (to 31 March 2027), 6 at the outside** (Tom,
2026-09-03). So this is not an emergency migration, but the runway ends in
roughly seven months, not someday.
It is G0 because the *decision* has a long lead time and because an extension
spent deferring the question rather than answering it is the failure mode here.

The AWS host carries every measurement the project has produced, and the
repository currently records nothing about who pays for it or what happens next.
BHLK has offered server capacity; that is an offer, not yet a plan.

**Three shapes, different lead times:**
1. **BHLK infrastructure** — where the collaboration points. Needs their
   capacity assessed, LiveORC stood up, data moved, station repointed. Longest
   lead time, and the best fit with the funding objective.
2. **PMI or IPB infrastructure** — if BHLK's capacity does not suit.
3. **Archive and hand over the data** — the live service ends, the record
   survives. Not a failure outcome if chosen deliberately; a poor one if it
   happens by default.

Whoever hosts it inherits the operational load, so pick against the second
objective too: the option that needs least of Tom is worth something.

**Steps:**
- [ ] Assess BHLK's server capacity against what LiveORC needs —
      `liveorc_server/README.md` and the compose stack document it.
- [ ] Decide among the three shapes, and set the date the decision has to be
      made by rather than the date the money runs out.
- [ ] Produce the durable data export regardless of the outcome. TODO-114
      already built an independent REST copy, so the mechanism exists.
- [ ] Plan the station repoint. Sukabumi uploads to a fixed endpoint; moving the
      server without moving the station strands it.
- [ ] Settle retention before the move, not during it — media is ~10 GB/month
      and growing (R22).

**Related:** R15, R22, R24 · TODO-112 (media on a dedicated EBS volume, done),
TODO-114 (independent mirror, done).

---

---

### TODO-209: Provision API access for IPB

| Field | Value |
|-------|-------|
| **Status** | OPEN — account shape settled, docs written 2026-09-08; the account itself is not yet created |
| **Priority** | G0 · December |
| **Opened** | 2026-09-03 |

IPB requested API access to support its data analysis, rain-gauge integration
and dashboard work. **Tom committed to providing it on 2026-09-03**, which
opens the PMI gate that TODO-104 recorded as closed.

The technical work is already done. **TODO-115 proved the read-only account
model against production on 2026-08-25, 14 PASS / 0 FAIL**, and it needs no
change to LiveORC. What remains is provisioning and documentation.

**Nothing is blocking this.** TODO-115 held provisioning behind two gates:
PMI approval (cleared 2026-09-03) and TODO-112 (DONE 2026-08-27, media on the
EBS volume). Both are clear, so the account creation below can be done now.

**Account shape — a single IPB service account (decided 2026-09-08).**
TODO-115's default was one login per person, never shared. That rule is for
*people*; this consumer is a machine. IPB is building a community dashboard,
so the credential lives in a server's configuration and is read by software,
not typed by a human. A named person's login in that position is worse, not
better: it ties a shared service to one individual's employment and gives the
dashboard a credential that can also sign in to the web UI as them. This is
the same shape as the TODO-114 mirror account (`user_id 18`), which is already
proven against production.

- One account, login **`ipb-dashboard@liveorc.local`** (decided 2026-09-08).
  Named for its function, not a person. The domain is deliberately
  non-routable: LiveORC has no mail configured and there is no password-reset
  flow, so an address that looks deliverable would be a false promise. Set
  `name` to "IPB dashboard (service account)" — `list_display` is the only
  place a future admin learns what the account is for.
- `is_staff=False`, `is_superuser=False`.
- `Member` of institute **1**, which owns sites 2, 3 and 4. Membership is the
  whole of the grant; it is set by hand and nothing else stands between
  read-only and nothing.
- Do **not** put it in the `viewers` group — that group carries Django model
  permissions the REST viewsets never consult, so it grants nothing while
  reading as though it grants read-only.
- Never hand over the ORC-OS station credential: it is `creator` on the
  existing videos and can delete them.

**Two consequences of a shared credential, to record rather than to solve.**
Attribution collapses — every API call from IPB is one principal, so if
something anomalous appears in the logs it cannot be traced past "the
dashboard". And the CREATE gap TODO-115 documents (any authenticated account
can `POST /api/video/`; the decision on 2026-08-24 was to accept it) now sits
behind a credential stored on a dashboard host rather than in one person's
password manager. Neither changes the decision. Both mean rotation is a
deliberate act by IPB and us, not something that happens when a person leaves.
If a second, differently-scoped IPB consumer ever appears, give it its own
account rather than sharing this one.

**And rotation is not where you would look for it — found 2026-09-08 while
writing the procedure.** Three things in LiveORC v0.3.0 make the obvious
offboarding moves useless. `is_active` is a hardcoded `True` class attribute on
Django's `AbstractBaseUser` and LiveORC never overrides it with a field, so the
`active` checkbox in the admin is a different field entirely and **cannot lock
anyone out**. JWTs are stateless, so **changing the password invalidates
nothing** already issued — and `REFRESH_TOKEN_LIFETIME` is **3650 days**, which
makes any refresh token IPB holds a ten-year credential. What does work is
deleting the `Member` row: `SiteViewSet.list()` falls through to
`queryset.none()` for a non-member and the nested routes 403, so data access
stops on the next request even with a live token. **Offboarding is: delete the
membership, then delete the user.** Written up in `liveorc_server/README.md`
under "Revoking access is not where you would look for it".

**Steps:**
- [ ] **Tom, in a browser at `/admin/`** — create the user, then the membership.
      The exact two forms, every field value, and what each wrong value would
      grant are written up in `liveorc_server/README.md` under "Creating a
      partner or service account". No host access needed; `/admin/` is publicly
      reachable and redirects to a login page. Creating a user has no side
      effects — the one signal in `users/signals.py` fires on `Institute`
      creation, not `User` creation.
- [ ] Record in the password manager what the account is for and who at IPB
      holds it.
- [x] **Partner-facing API guide written 2026-09-08** —
      `liveorc_server/partner-api/`, a self-contained bundle with no
      credentials in it. `README.md` covers auth and the 6-hour token, the
      `?institute=1` trap, the full time series schema with units, the UTC/WIB
      note, the media warning with ISS-FIELD-004, what the account cannot do,
      the service horizon from TODO-208, and a symptom/cause table.
      `fetch_timeseries.py` is a stdlib-only worked client — token, refresh
      semantics, date-bounded incremental pulls, CSV out. Its error paths are
      tested against production; the authenticated paths are not, and cannot be
      until the account exists.
- [ ] Send credentials through a channel that is not this repository, and name
      the IPB owner responsible for where the credential is stored — a
      dashboard host, not a laptop.
- [ ] Re-run TODO-115's verification matrix against **the IPB account itself**
      before announcing access — not against the mirror. Membership is set by
      hand and is the only thing standing between read-only and nothing.
      `./verify-api-access.sh --institute 1 --site 4 --probe-writes`
- [ ] While that credential is to hand, **check the four undocumented time
      series parameters** the guide tells IPB to use — `startDateTime`,
      `endDateTime`, `fields`, `format=csv`. They are read from v0.3.0 source
      and have never been exercised against the running server. The guide flags
      them as unverified; remove that flag once they are, or correct the guide.
- [ ] Confirm IPB can reach what they actually need for the three collaboration
      areas, not merely that the token works.
- [ ] **Tell IPB about TODO-208 before they build on this API.** A dashboard
      built against a server that stops being paid for is a poor gift. §9 of the
      guide states the dates; that is the written record, not the conversation.

**Related:** TODO-104, TODO-115 (`spring_2026_ID/TODO.md`), TODO-401.

---

---

### TODO-204: Close out the replication report so it can be circulated

| Field | Value |
|-------|-------|
| **Status** | OPEN |
| **Priority** | G0 · December |
| **Opened** | 2026-09-03 |
| **Parent** | TODO-118 (`spring_2026_ID/TODO.md`) |

`spring_2026_ID/docs/REPLICATION_RECOMMENDATIONS.md` is committed to a public
repository while its own header reads *"draft for internal review — not yet
circulated"*. **BHLK is actively asking for exactly this material**, which makes
the draft label the thing standing between them and it.

**Steps:**
- [ ] Settle the page budget — 18 pages built against a 10-page brief.
- [ ] **Confirm BHLK's full name.** The repo cites PUSAIR's *Balai Hidrologi dan
      Tata Air*; the thread consistently gives *Balai Hidrologi Lingkungan dan
      Keairan*. It appears on the title page of a document addressed to them.
- [ ] Build the Bahasa Indonesia PDFs for report and appendix — registered in
      `build_pdf.sh`'s `ALL_DOCS`, absent from `docs/pdf/id/`.
- [ ] Clear the draft label, circulate, then unblock the link in TODO-201.

---

---

### TODO-202: Make the stated sharing position operative — licence and citation

| Field | Value |
|-------|-------|
| **Status** | OPEN |
| **Priority** | G0 · December |
| **Opened** | 2026-09-03 |

**Tom has already told PMI in writing that all project materials are freely
shareable** — code, documentation, build notes, installation instructions — and
that PMI may share them as they wish. BHLK has asked for the GitHub installation
guidance on the strength of that.

The repository does not yet say so. There is no `LICENSE`, `CITATION.cff`, or
`CONTRIBUTING.md`. A public repository with no licence grants no rights by
default, so the stated position and the legal position currently disagree. The
intent is settled; what is missing is the instrument.

**Steps:**
- [ ] Choose licences consistent with the position already stated. The
      repository is mixed — research prose and documentation alongside working
      code in `survey/auto_fit/`, `pi/`, `camera/` and `liveorc_server/` — so a
      content licence plus a code licence is likely right.
- [ ] Confirm nothing in the grant or American Red Cross policy constrains this.
      The commitment has been made to a partner; a conflict would need finding
      now rather than later.
- [ ] Add `CITATION.cff` — IPB is an academic partner and will cite this.
- [ ] **Two things a licence of ours cannot cover:** the third-party
      flow-measurement guide redistributed under `manual/` carries no licence
      note, and the partner logos under `spring_2026_ID/docs/logos/` have no
      recorded usage permission — that directory's `README.md` already flags
      BHLK as open.

---

---

### TODO-203: Public-repository readiness

| Field | Value |
|-------|-------|
| **Status** | OPEN |
| **Priority** | G0 · December |
| **Opened** | 2026-09-03 |

**BHLK has asked to be pointed at the GitHub repository.** This is no longer
hypothetical traffic.

**(a) Location metadata in tracked images — the serious one.** 65 of 138 tracked
images carry a GPS EXIF IFD resolving to a private US residence, at roughly 10 m
precision. Verified 2026-09-03 by reading the GPS IFD directly. Affected:
`spring_2026_ID/docs/images/sukabumi/`,
`spring_2026_ID/build_notes/sukabumi/photos/originals/`, and
`prior_work/utilities/images/`. **The data is also in git history, so scrubbing
working-tree files does not remove it.** Rewriting history on a published
repository breaks existing clones and forks and needs an explicit decision.

**(b) Production identifiers.** EC2 instance ID and public IPv4 in
`spring_2026_ID/liveorc_server/MEDIA_VOLUME_RUNBOOK.md`,
`spring_2026_ID/ISSUE_LOG.md`, `spring_2026_ID/TODO.md`, and two
`liveorc_server/station-health/*.sh` scripts; Tailscale addresses in
`spring_2026_ID/RECOVERY_JAKARTA.md`. Note this partly resolves itself through
TODO-208 — an instance that no longer exists is not a disclosure.

**(c) Hygiene.** `.claude/.claude/agents/` duplicates `.claude/agents/` verbatim
— 43 tracked files of generic agent definitions unrelated to the project;
tracked `.pyc` artifacts under `spring_2026_ID/camera/`; absolute
`/home/tjordan` and `/Users/tjordan` paths in roughly 20 files; and a Claude
memory file from the Pi committed under `spring_2026_ID/.claude/`.

**No credentials were found.** History was checked; the only `.env`-family files
ever added are `.env.example` placeholders and a deliberately public CA
certificate. Site coordinates are handled correctly — `survey_data/` is
gitignored and the only tracked coordinates are town-level worked examples.

---

---

### TODO-201: Recreate the repository landing page

| Field | Value |
|-------|-------|
| **Status** | IN PROGRESS — first rewrite landed 2026-09-03 |
| **Priority** | G0 · December |
| **Opened** | 2026-09-03 |

The root `README.md` had gone 193 commits without an edit and was publishing a
calibration the project had retired — it presented the April auto-fit salvage
config (4.61 cm RMSE, `h_ref = 617.065 m`) as current and the IPB total-station
survey as pending, when the station has run on IPB `Fit 6` (0.037 m RMSE,
`h_ref = 615.0 m`) since 2026-06-11.

**Done 2026-09-03:** correctness pass against `spring_2026_ID/README.md` and
`TODO.md`; restructured to route four audiences; the same contradiction fixed in
`spring_2026_ID/README.md`, along with its stale capture interval and research
count; the single-source-of-truth rule written into both files.

**Remaining:**
- [ ] Licence section, once TODO-202 lands. It currently states the position
      Tom gave PMI and notes the instrument is missing.
- [ ] Link the replication report once TODO-204 clears it.
- [ ] Reflect the transition once TODO-208 is decided — a landing page that
      points at a server about to be switched off is worse than one that says so.
- [ ] Set the GitHub repository description and topics. Both are empty.

---

---

### TODO-205: Successor handover pack

| Field | Value |
|-------|-------|
| **Status** | OPEN |
| **Priority** | G0 · December |
| **Opened** | 2026-09-03 |

**This is the direct instrument of the second objective.** American Red Cross
wants Tom's time freed; that cannot happen while the access model, the runbooks
and a good deal of operational judgement exist only in one person's head and
credentials. G0 because it is the longest-running item here — it is not a task
so much as a discipline of writing things down as they come up.

**Steps:**
- [ ] Inventory access and who holds it — AWS, the LiveORC host, the station,
      Tailscale, Pangolin, the carrier account, DNS and TLS. Several of these
      end with TODO-208.
- [ ] Point at existing runbooks rather than rewriting them:
      `liveorc_server/README.md`, `MEDIA_VOLUME_RUNBOOK.md`,
      `reprocess/REPROCESS_RUNBOOK.md`,
      `survey_data/ipb_survey_1/handoff_station/`.
- [ ] Write down what is in no file. The prepaid SIM whose lapse caused a
      4.8-day outage is the worked example: nothing monitors it and nothing in
      the repo said so.
- [ ] Name the open defects the successor inherits, from `ISSUE_LOG.md`.

---

---

### TODO-302: Evaluate the integrated carrier class named by R37

| Field | Value |
|-------|-------|
| **Status** | OPEN |
| **Priority** | G0 · December |
| **Opened** | 2026-09-03 |

R37 is described in `RECOMMENDATIONS.md` as the strongest recommendation on the
list: an industrial Raspberry Pi carrier with storage, power and timekeeping
integrated — NVMe on board, a protected RTC, wide-input power with UPS
telemetry reporting voltage and current, often a modem slot. It recommends a
**class**, because **no specific product was ever evaluated.** There is no
research file for industrial Pi or CM4/CM5 carriers anywhere in the repository.

TODO-301 is blocked behind it, and BHLK's 45-second capture request (TODO-403)
lands directly on the storage half of it.

**Steps:**
- [ ] Survey carriers against what the failure chain requires: NVMe; a protected
      RTC that does not depend on the ML-2020 connector that failed on both
      boards; wide-input power; V/I telemetry (also R6, TODO-117).
- [ ] Score against R30 explicitly — an integrated carrier is more likely to be
      single-source, which trades directly against the commodity/multi-source
      constraint. Record the trade rather than letting it pass.
- [ ] Recommend a class and two or three candidates with prices, so a partner
      procuring locally has a starting point.

---

---

## G1 — should land before the grant closes

### TODO-401: Support IPB's rain gauge integration and dashboard

| Field | Value |
|-------|-------|
| **Status** | OPEN |
| **Priority** | G1 |
| **Opened** | 2026-09-03 |

IPB installed **three sets of rain gauges on 22–23 August 2026** and will
integrate that data with ORC output, then build a community-facing dashboard.
This is IPB's work, not ours. Our job is to make it possible and to avoid
duplicating it.

**It bears directly on two of our own items.** TODO-102 in the operations
tracker is a Grafana instance for sensor visualisation, substantially built. If
IPB is building the partner-facing dashboard, TODO-102's audience shrinks to
internal diagnostics and should be rescoped rather than finished as specified.
And `LESSONS_LEARNED.md` §8 proposes a networked rain-gauge node — IPB has now
installed gauges, so that concept needs re-examining against what they chose
(see TODO-305).

**Steps:**
- [ ] Ask IPB what they installed and how it reports, before assuming anything.
- [ ] Establish whether our RG-15 at Sukabumi is now redundant (R21 already
      recommends removing the rain gauge from the camera station).
- [ ] Decide TODO-102's scope in light of IPB's dashboard, and say so there.
- [ ] Give IPB what the dashboard needs from the ORC side — data shapes, units,
      cadence, and the known gaps, including the days with no captures.

---

### TODO-402: BHLK discharge comparison, 21 August 2026

| Field | Value |
|-------|-------|
| **Status** | OPEN — time sensitive |
| **Priority** | G1 |
| **Opened** | 2026-09-03 |
| **Discharges** | R20 |

BHLK measured river discharge at Sukabumi on **21 August 2026** and asked to
compare it against ORC output from a similar time. Photo documentation came with
Dewi's 2 September mail.

**This is the independent field check of a different kind that R20 asks for, and
it arrived for free.** It is the first opportunity to compare our output against
a reference measurement made by a hydrological authority.

**Handle the caveats honestly rather than around them.** The station's own
record has holes — TODO-119 established days with no captures at all, and
optical water level fails through daylight (`findings/optical_wl_daytime_glint.md`),
so a daytime measurement is exactly when our water level is least reliable.
Establish what the station actually recorded on 21 August before promising a
comparison.

**Steps:**
- [ ] Pull what exists for 21 August 2026 — captures, processing outcomes,
      water level source, and whether optical WL succeeded or fell back.
- [ ] Get BHLK's method, time, and uncertainty, not only their number.
- [ ] Compare, and state the uncertainty on our side plainly. The calibration
      carries the IPB survey's noise floor; the comparison is worth doing and
      is not a validation of absolute discharge on its own.
- [ ] Write it up in `findings/`. Whichever way it comes out, it is the most
      externally meaningful measurement the project has.

---

### TODO-403: Answer the 45-second capture question

| Field | Value |
|-------|-------|
| **Status** | OPEN |
| **Priority** | G1 |
| **Opened** | 2026-09-03 |

BHLK suggested captures of around **45 seconds** rather than the present 5 for
more stable results. Tom's initial answer: the 5-second capture follows Hessel's
recommendation, and the current stations lack the storage for 45 seconds without
a hardware upgrade or a change to video retention.

That answer is right and incomplete. **The storage constraint is not incidental —
it is the same constraint that caused the largest outage.** ISS-FIELD-009 records
the chain: OS and video sharing one SD card, the disk pinned at its purge
threshold, 43% of videos failing processing, shutdown never firing, and a flat
battery. A 9× increase in capture length walks straight into it.

**Steps:**
- [ ] Get the reasoning behind 45 seconds from BHLK — it likely reflects
      standard gauging practice, and that is worth understanding rather than
      just costing.
- [ ] Ask Hessel why 5 seconds, so the two positions can be compared on
      technical grounds instead of by authority.
- [ ] Cost 45 seconds properly: storage per capture, per day, per retention
      window; upload volume over a metered link; and processing time.
- [ ] Feed the answer into TODO-301 and TODO-302 as a design input. If a v2
      station should support long captures, that changes the storage
      specification, not a config value.

---

### TODO-211: Put the Jakarta station in front of IPB and BHLK

| Field | Value |
|-------|-------|
| **Status** | OPEN |
| **Priority** | G1 — on the November gate |
| **Opened** | 2026-09-03 |
| **Parent** | TODO-108 (`spring_2026_ID/TODO.md`) |

BHLK asked to see an ORC device directly, including the equipment inside the
box. The Jakarta station is built, complete, and has sat unpowered at Wisma PMI
since April 2026. Tom has proposed it as the unit IPB and BHLK learn to build
from.

It is also the physical instantiation of **R36** — keep a station you can break,
on a bench, mains-powered and always on. TODO-108 already asks for a bench soak
rather than a warehouse; this gives that a purpose and an audience.

Two things to say plainly when handing it over: it is a **study and test unit,
not operational service**, and it carries the design the replication report
recommends changing.

**Steps:**
- [ ] Power it up and soak it before showing it to anyone. It has not run since
      April.
- [ ] Confirm with PMI where it lives and who is responsible for it.
- [ ] Use it for the walkthrough (TODO-210) and as the reference build for
      TODO-303's substitution guidance.

---


### TODO-206: Field photographs of the deployed station

| Field | Value |
|-------|-------|
| **Status** | PARKED — next site visit |
| **Priority** | G1 — on the November gate |
| **Opened** | 2026-09-03 |

TODO-118 records that **there are no field photographs of the deployed station
anywhere in the repository.** All five photographs in the replication report are
bench and build shots. BHLK, meanwhile, sent photo documentation of their own
field measurement.

`build_photos/PHOTO_METADATA.md` is not a reliable index — TODO-118 records a
frame captioned as a pole-mounted camera that is actually a basement water
filter. Open every image before using it.

Coordinate with TODO-203: phone photographs carry GPS EXIF, and at Sukabumi that
metadata is the site location.

---

### TODO-301: Write the v2 hardware design specification

| Field | Value |
|-------|-------|
| **Status** | OPEN |
| **Priority** | G1 |
| **Opened** | 2026-09-03 |
| **Scope** | A design specification to hand off. No prototype is built by us in this grant. |

**There is no current parent document for the as-built platform.**
`rc-box/DESIGN_SPECS.md` declares itself authoritative but is dated 2024-12-03
and describes a design never built — two cameras, USB-preferred, Witty Pi 4, an
IR spotlight, a stereo stretch goal. What was actually deployed is spread across
`BOM_Sukabumi.md`, `docs/ASSEMBLY_*.md`, `docs/WIRING_*.md` and `diagrams/`. So
v2 must be written from R1–R37 plus as-built reality, not by editing
DESIGN_SPECS.md.

**The chain the design must break.** The Sukabumi outage record is one causal
chain, not a set of independent faults: the Pi 5 ML-2020 RTC connector failed on
both boards → the Witty Pi was reinstated → sleep and wake split across two
systems → the USB drive was removed for a UAS boot storm → OS and video shared
one SD card → the disk pinned at its purge threshold → 43% of videos failed
processing → `shutdown_after_task` never fired → the Pi ran to its 25-minute
backstop at roughly 12× the energy → flat battery → missed wake → the alarm was
left in the past with nothing to re-arm it → multi-day outage.
(ISS-FIELD-008, ISS-FIELD-009; R10, R12, R13, R25, R37.)

**Two inputs now come from the partners rather than from us:** BHLK's
45-second capture request (TODO-403), which is a storage requirement; and the
20–21 August agreement that **real-time monitoring means AC mains**, which is
R11 confirmed by the people who would operate it.

**Steps:**
- [ ] Decide whether v2 supersedes `rc-box/DESIGN_SPECS.md` or sits beside it.
      Either way that file needs a status banner — it is currently misleading.
- [ ] Capture the as-built platform as the baseline v2 departs from.
- [ ] Work R1–R37 in, recording which are adopted, which declined, and why.
- [ ] State interfaces rather than part numbers (R3).
- [ ] Route it through the same EN/ID PDF pipeline as the other partner
      deliverables.

**Blocked on:** TODO-302.

---

### TODO-303: Interface specification sheet and site adaptation checklist

| Field | Value |
|-------|-------|
| **Status** | OPEN |
| **Priority** | G1 |
| **Opened** | 2026-09-03 |
| **Discharges** | R3 |

R3 asks for interfaces rather than part numbers — what binds (voltage, current,
ingress rating, temperature) and what is free (brand, mounting) — as a bilingual
specification sheet with photographs, plus a site adaptation checklist.

This is what lets BHLK build with locally-sourced parts instead of hunting the
exact components we used, and BHLK's interest in replication is what makes it
worth doing now rather than at the end.

Distinct from TODO-301: the v2 spec says what to build; this says how to
substitute safely into it.

---

### TODO-304: Decide the split architecture in or out of v2

| Field | Value |
|-------|-------|
| **Status** | OPEN |
| **Priority** | G1 |
| **Opened** | 2026-09-03 |
| **Discharges** | R8, R27 · **Related** TODO-106 |

R27 argues a camera-only field node with remote compute is the most deployable
version of the system — any security-camera installer can deploy it, and
everything ORC-specific moves to the compute layer.
`spring_2026_ID/docs/SPLIT_ARCHITECTURE_DESIGN.md` exists but was written before
the trip and has **never been field-tested**. ORC-OS 0.7.0's Celery/Redis worker
split is the software half.

This interacts with TODO-208: if processing moves to a partner-hosted server,
the split architecture stops being speculative and becomes the natural shape.
Decide it before TODO-301 gets far, and say plainly that the design is untested.

---

## G2 — hand to the successor

### TODO-212: Sukabumi relocation, if it happens

| Field | Value |
|-------|-------|
| **Status** | PARKED — awaiting PMI |
| **Priority** | G2 — but the parking has a deadline, see below |
| **Opened** | 2026-09-03 |

BHLK recommended relocating the station to a flat area free of obstruction from
buildings, and relocation was discussed. Tom asked on 2026-09-03 whether it is a
likely outcome; unanswered.

If it happens it is the best opportunity the project will get: a chance to apply
R16 (treat site selection as a measurement decision), to fix what the first site
made hard — the urban RF and sky-view problems that appear to have hurt RTK, and
the sun–water–camera geometry behind the daytime optical water-level failure —
and to do the in-country training on a real installation (TODO-210).

Do not start work on this until PMI answers. But **the waiting itself now has a
deadline**: a relocation funded by this grant needs PMI's spend committed by
around 30 November 2026, and the lead time on a survey and a permission is long.
If PMI has not answered by roughly the end of October, treat the answer as no
for planning purposes and say so, rather than holding the slot open.

---

### TODO-207: Documentation site

| Field | Value |
|-------|-------|
| **Status** | OPEN |
| **Priority** | G2 |
| **Opened** | 2026-09-03 |

Deferred deliberately: the README rewrite (TODO-201) is the front door.

Note that **Hessel has refreshed the upstream documentation site at
<https://openrivercam.org/documentation/>**. That covers the software; a site of
ours would cover the field deployment record. Check what it now says before
building anything that might duplicate it.

Most scaffolding already exists in `spring_2026_ID/docs/` — `build_pdf.sh` with
its `ALL_DOCS` registry and `DOC_AUDIENCE` map, `build_index.py`, and a
WeasyPrint path that installs without root. There is no `.github/` directory, so
CI would start from nothing.

---

### TODO-305: Adjacent sensor products — re-examine against what IPB installed

| Field | Value |
|-------|-------|
| **Status** | OPEN |
| **Priority** | G2 |
| **Opened** | 2026-09-03 |

`spring_2026_ID/LESSONS_LEARNED.md` §8 and §9 propose two standalone products.
Neither is fundable in the remaining window, and §8's premise has changed.

- **§8 — networked solar rain gauge node.** LoRa / LTE-M / NB-IoT, USD 200–400
  BOM target, matched to the BMKG ombrometer standard. **IPB installed three
  sets of rain gauges on 22–23 August 2026 and is integrating them.** Before
  this concept goes any further, find out what they chose and why; the gap it
  was written to fill may be smaller than it was.
- **§9 — river stage sensor with public-alert relays.** Target well under
  USD 1,000 against a USD 3,600 government e-catalogue entry; acceptance is
  interoperability, not sensor principle. Aimed at PUPR / Ditjen SDA / BBWS.
  Unaffected, and still relevant to R1's independent water-level reference.

Keep both scoped and written down so a partner or successor can pick them up.

---

## DONE

*(nothing yet — file created 2026-09-03)*
