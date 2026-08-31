# Outline — Recommendations for Replication of the OpenRiverCam Station Design

**Status:** Draft outline for internal review. Not for circulation.
**Prepared for:** IPB and BHLK (Balai Hidrologi dan Lingkungan Keairan), following
the PMI / IPB / BHLK meeting at Sukabumi, 21 August 2026.
**Secondary audience:** PMI NHQ (to be confirmed — see D3).
**Target length:** 10 pages.
**Audience level:** Scientific, non-specialist in embedded hardware. No part
numbers, wiring detail or code in the body; those are referenced in the appendix.
**Outline date:** 2026-08-31.

---

## Decisions to resolve before drafting

| # | Decision | Notes |
|---|---|---|
| **D1** | Does §6 stay in the document? | §6 sets out where hydrological correction can and cannot repair a measurement difference, and disagrees with a position recorded in the 21 August meeting ("differences in data resulting from ORC measurements are not a major issue; these can be corrected through hydrological calculations"). It is technically material to the drought use case. Options: keep as drafted, soften, move to appendix, or remove and raise verbally. |
| **D2** | How far to go on permission and licensing in §1. | Currently one paragraph: ORC and ORC-OS are open source under LocalDevices; the hardware design documentation and field record are ours; the permission question recorded at the meeting is being handled separately. Expand, shorten, or remove. |
| **D3** | Is PMI NHQ an audience for this document? | If yes, §2 and §9 each need a short paragraph on what PMI is being asked to commit to. |
| **D4** | Confidence level on unresolved findings. | The two unexplained outages and the 13 V recovery-voltage behaviour are open. Outline currently reports them as open in §10 rather than omitting them. Confirm that is the right posture for this audience. |

## Assumptions

1. BHLK is the Balai Hidrologi dan Lingkungan Keairan under PUSAIR / Kementerian
   PUPR. Confirmed against the meeting notes ("Central Office for Environmental
   Hydrology"). Cross-reference: `spring_2026_ID/research/indonesia_hydrometric_standards.md`.
2. Scope is a pilot of **one to three units** built and owned by BHLK, not a
   network build-out and not a kit shipment from us.
3. Costs given in USD with Rupiah equivalents where an Indonesian benchmark exists.
4. The report is a recommendation document, not a validation study. The evidence
   base is one deployed station, one built-but-undeployed station, and
   approximately four months of station telemetry to 2026-08-29.

---

## 1. Purpose and status — 0.5 p

- What this document responds to: the request recorded on 21 August that BHLK
  duplicate one to three ORC devices as a pilot.
- What it contains: the design as built, the field record to date, and what we
  recommend changing before units are built.
- Standing and limits of the evidence, stated at the outset: one site, one river,
  one season, and a calibration not certified for absolute discharge.
- Permission and licensing paragraph (see **D2**).

*Figure candidate: none.*

## 2. Intended use, and what it requires of the design — 0.75 p

The purposes recorded at the meeting — drought assessment linked to BNPB
preventive measures, and validation of a modelling framework — impose
requirements that flood monitoring does not.

- **Low flow is the harder measurement case.** Discharge is velocity × area. At
  low flow the wetted section may be 20–40% of bankfull, so a 10 cm vertical
  error in a 0.3 m deep section can produce a 30% area error and a proportional
  discharge error. Survey accuracy therefore matters *more* for drought work than
  for flood work, not less.
  Source: `survey/research/professional_surveyor_and_escape_hatch.md` §"Where Errors Actually Matter in ORC".
- **Surface velocimetry depends on trackable surface features.** Low-flow,
  low-turbulence conditions supply fewer of them. Performance in this regime is
  documented in the literature (Pearce et al., 2020) and should be established at
  the pilot sites rather than assumed.
- **Use as a validation reference requires a stated uncertainty.** A measurement
  without an uncertainty band cannot validate a model. This makes the survey and
  cross-section requirements in §5 binding rather than advisory.
- If PMI NHQ is an audience (**D3**), add: what PMI is committing to as the user
  of the derived information.

*Figure candidate: schematic of wetted area at low vs high stage, showing how a
fixed vertical error propagates into a proportionally larger area error at low flow.*

## 3. The design as built, and its cost — 0.75 p

- System description in one paragraph: PoE camera, Raspberry Pi 5 with scheduled
  power management, on-station processing, LTE upload to a central server.
- The four constraints that governed every component choice: commodity parts with
  multiple suppliers; no soldering; no specialist assembly skills; any component
  replaceable in five minutes with common tools.
  Source: `rc-box/DESIGN_SPECS.md`, `spring_2026_ID/README.md` §Design Principles.
- Cost: **USD 1,340 materials** (solar configuration, as built at Sukabumi);
  **~USD 1,030** grid-powered configuration.
  Source: `spring_2026_ID/BOM_Sukabumi.md` §Total BOM Cost Summary; `rc-box/BOM_VERIFIED.md`.
- Comparison: lowest confirmed Indonesian government-catalogue automatic
  water-level station (IDDATA RL03 radar + GSM, INAPROC) at **Rp 58 M /
  ~USD 3,600 ex-VAT**. Relevance is network density — how many stations a basin
  authority can afford determines how much of a catchment is instrumented.
  Source: `spring_2026_ID/research/indonesia_hydrometric_standards.md`.

*Figure candidate: system block diagram (camera → compute → upload → server),
non-technical register. Reuse/simplify from `docs/SPLIT_ARCHITECTURE_DESIGN.md`.*

## 4. Field record, April to August 2026 — 1.25 p

Measurements with their derivation. Attributions that were subsequently withdrawn
are identified as withdrawn.

**4.1 Availability.** 22.7 days unavailable of 118 days observed, in 13 discrete
outages, reconstructed from the sensor-row record held on the server. No alerting
was in place during the period; the outages were identified retrospectively.
Source: `spring_2026_ID/ISSUE_LOG.md` ISS-FIELD-008; `liveorc_server/station-health/station_gaps.py`.

**4.2 Attribution.** Nine of the 13 outages are attributable to maintenance mode
being left active. The mode suppresses video capture and holds the processor awake
for the full scheduled window at approximately 12× normal energy consumption;
long-wake events run at 1.59/h inside maintenance windows against 0.18/h outside.
Two outages remain unexplained. An earlier statistical association between long
wakes and outage onsets is **withdrawn** — maintenance mode was generating both
terms.
Source: `spring_2026_ID/ISSUE_LOG.md` ISS-FIELD-010.

**4.3 Daytime water-level failure.** Sukabumi has no water-level sensor and falls
back to optical water-level detection. Over 2026-07-08→14, sampled daytime
captures failed at the signal-to-noise gate (S/N 1.3–1.8 against a threshold of
2.0) while night captures passed at S/N 3–5. Failures are bounded by the daylight
window with a dip at solar noon, which is the geometric signature of specular sun
glint rather than general daytime brightness. Water-level estimation aborts the
whole run, so each daytime failure loses the entire discharge measurement, not
only the level.
Source: `spring_2026_ID/findings/optical_wl_daytime_glint.md`.

**4.4 Data delivery.** Approximately half of all captured video did not reach the
server. A separate 12-day gap in the video record occurred while the station was
operating normally.
Source: `spring_2026_ID/ISSUE_LOG.md` ISS-FIELD-009, ISS-FIELD-008.

*Figure candidates: (a) availability timeline showing the 13 outages against the
observation window, with maintenance-mode windows shaded; (b) the day/night S/N
distribution, or the hour-of-day pass/fail histogram from the glint finding.*

## 5. Recommendations for the pilot units — 3.5 p

Ordered by effect on the pilot's stated purpose. Each stated with its supporting
observation and the cost of adopting it.

**R1 — Fit an independent water-level reference. Do not depend on optical
detection.** A level sensor, or a staff gauge within the camera view referenced to
the local *papan duga air* zero. Basis: §4.3. Effect: the difference between a
station that measures through the day and one that measures at night.

**R2 — Commission a professional survey before the first installation.** Survey
accuracy sets the lower bound on discharge accuracy and no downstream processing
recovers it. Basis: two RTK surveys on consecutive days at Sukabumi reproduced
check-point spreads of ~99 cm horizontal and ~139 cm vertical against a 3 cm gate;
the salvage calibration in use (4.61 cm RMSE on a six-GCP subset) supports trend
monitoring but not certified discharge. Cost: **Rp 5–15 M per site**. Include the
contract terms that manage the known risks — RTK Fixed status only, equipment
model and RMSE specified in the SOW, one consistent vertical datum.
Source: `spring_2026_ID/ISSUE_LOG.md` ISS-FIELD-002; `survey/outsourced_survey_brief.md`;
`survey/research/professional_surveyor_and_escape_hatch.md`.
 - Sub-point: carry an independent in-field check of a different type, so a failed
   survey is caught on site rather than in post-processing.
 - Sub-point: if a method fails once at a site, change the method. The dominant
   failure modes reproduce day to day with the same equipment and crew.

**R3 — Build to interfaces, not part numbers.** Publish the interface
specification and the substitution rules — which parameters bind (voltage,
current, ingress protection, operating temperature) and which do not (brand, form
factor, mounting style) — so units can be sourced in Indonesia without
re-engineering. Basis: substitution under schedule pressure during the Jakarta
build changed the power architecture, with no written rule available to evaluate
it against.
Source: `spring_2026_ID/LESSONS_LEARNED.md` §3.

**R4 — Specify health telemetry and mode alarms as functional requirements.** Any
mode that suppresses data or raises energy consumption must be remotely visible,
must raise an alert, and should expire automatically rather than persist until
cleared. Basis: §4.1, §4.2. Cost: negligible — the maintenance flag was readable
from a public API throughout the period without contacting the station.

**R5 — Have the station push diagnostics rather than requiring a login.** A
duty-cycled station may be awake for only tens of seconds per cycle, which is not
long enough to establish an interactive session. Diagnostic state should travel
with the routine data upload. Basis: an operating station was recorded as
unavailable because monitoring depended on a connection path that never opened
within the wake window.
Source: `spring_2026_ID/ISSUE_LOG.md` ISS-FIELD-010.

**R6 — Instrument the power system; record voltage and current as paired
samples.** Voltage alone cannot separate a battery fault from a load fault. Size
for the worst case: the sleep-phase budget was initially understated by 25%
(118 Wh/day against 94 Wh/day estimated), reducing calculated autonomy from
3.2 days to 2.5 days.
Source: `spring_2026_ID/ISSUE_LOG.md` ISS-001; `spring_2026_ID/TODO.md` TODO-117.

**R7 — Reconcile captured data against received data automatically.** Video and
sensor data travel independent paths and fail independently; neither confirms the
other. Basis: §4.4.

**R8 — Consider siting compute indoors for the pilot units.** Reduces the field
installation to mounting a camera and providing a network path, and places the
processing equipment where temperature, humidity and access are controlled — well
suited to units hosted at a BHLK or IPB facility. Note honestly that the design
exists but has not been field-tested; recommended as the pilot's first test, not
as a proven configuration.
Source: `spring_2026_ID/docs/SPLIT_ARCHITECTURE_DESIGN.md`.
 - Related: where the field node is a standard IP camera, the existing Indonesian
   security-camera supply chain covers installation, mounting, outdoor power and
   weatherproofing with local support.

*Figure candidate: comparison diagram, co-located station vs camera-only node with
indoor compute.*

## 6. Measurement differences, correction, and data acceptance — 0.75 p

See **D1** — this section addresses a position recorded in the meeting.

- A stable bias is correctable: a systematic offset against a reference can be
  removed by a rating or index-velocity relationship.
- Two cases in the current record are not correctable that way. Random geometric
  error from a poor survey varies between points and has no single correction
  factor. Error at low flow scales disproportionately into area error (§2).
- Correction requires an independent reference. Where ORC is intended to validate
  a modelling framework, correcting ORC output using that framework removes its
  independence as a validation source.
- Conditions for output to be additive to BBWS time series: level referenced to
  the local staff-gauge zero in metres; 15-minute time step minimum, 5-minute
  preferred for flood-warning ingest; SIH3 / SIHLSDA format, CSV or HTTP POST;
  paired daily manual readings during commissioning; uncertainty documented per
  **SNI 8066:2015** and WMO-No. 168 Ch. 5; camera-derived discharge positioned as
  supplementary to the BBWS rating curve rather than as a replacement for it.
  Source: `spring_2026_ID/research/indonesia_hydrometric_standards.md`.

## 7. Data hosting — 0.5 p

Accepts BHLK's offer of server capacity in principle, with the conditions that
apply in operation.

- The server is a containerised deployment. Two constraints found in practice:
  video storage and the database must share a filesystem, and the server and
  station software versions are coupled — a server upgrade requires the stations
  to follow.
- Recommend mirroring to the BHLK server in parallel before any cut-over, and
  agreeing in advance where the authoritative copy sits and who administers it.
- Note the data-sovereignty benefit of in-country hosting for a
  government-partnered pilot.

## 8. Site selection — 0.5 p

Supports BHLK's recommendation to relocate to a flat site free of obstruction from
buildings and other structures, and adds our own evidence for it. An open site
addresses three separate problems at once:

1. GNSS multipath and sky obstruction, among the leading candidate causes of the
   survey noise at the present site (§5 R2).
2. Camera-to-sun geometry, which drives the daytime glint failure (§4.3).
3. View geometry across the section.

Also note: the cost of a move is a re-survey, a re-calibration and fresh site
permission; and written site permission should be in hand before any unit is built
for a specific site.
Source: `spring_2026_ID/LESSONS_LEARNED.md` §6; `spring_2026_ID/ISSUE_LOG.md` ISS-FIELD-001.

## 9. Division of responsibility — 0.5 p

As recorded at the meeting, with the reasoning that technology development and
field operations are distinct disciplines:

- **BHLK** — data processing, standards conformance, and the route to acceptance
  within PUPR data systems. Offers server capacity (§7).
- **IPB** — design, calibration methodology, training material, and the
  development pipeline for future sensor types.
- **PMI** — user of the derived information; field operations, siting within its
  mission scope, maintenance, and spares held locally.

Recommend this is written into the collaboration agreement rather than held as an
informal understanding between individuals. If PMI NHQ is an audience (**D3**),
add what PMI is being asked to commit to.
Source: `spring_2026_ID/LESSONS_LEARNED.md` §10.

## 10. Open questions — 0.25 p

Stated as open, not resolved (see **D4**):

- The cause of the two unexplained outages, which carry the maintenance-mode
  signature without the mode set.
- Whether the 13 V recovery-voltage setting bounds outage duration. One
  observation is consistent with it; one observation is not sufficient.
- Whether a staff gauge can be read directly from the camera image, removing the
  need for a separate level sensor.
- Absolute discharge accuracy at Sukabumi, unresolved pending the survey.
- Low-flow velocimetry performance at the pilot sites.

## 11. Summary of recommendations — 0.25 p

Table: recommendation | supporting observation | cost of adoption.

## Appendix — 0.5 p

Pointers, not content:

- Reference bill of materials — `spring_2026_ID/BOM_Sukabumi.md`, `rc-box/BOM_VERIFIED.md`
- Design specification — `rc-box/DESIGN_SPECS.md`
- Survey scope of work — `survey/outsourced_survey_brief.md`
- Indonesian hydrometric standards research — `spring_2026_ID/research/indonesia_hydrometric_standards.md`
- Operator and assembly documentation, English and Bahasa Indonesia — `spring_2026_ID/docs/`

---

## Page budget

| Section | Pages |
|---|---|
| 1. Purpose and status | 0.5 |
| 2. Intended use and what it requires | 0.75 |
| 3. The design as built, and its cost | 0.75 |
| 4. Field record | 1.25 |
| 5. Recommendations | 3.5 |
| 6. Measurement differences and acceptance | 0.75 |
| 7. Data hosting | 0.5 |
| 8. Site selection | 0.5 |
| 9. Division of responsibility | 0.5 |
| 10. Open questions | 0.25 |
| 11. Summary table | 0.25 |
| Appendix | 0.5 |
| **Total** | **10.0** |

## Candidate visuals (for later — not part of this outline)

Listed here so the figure work is scoped when the draft is written. Five figures
is the right count for ten pages.

| # | Section | Figure |
|---|---|---|
| F1 | §3 | System block diagram, non-technical register |
| F2 | §2 | Vertical error propagating into area error at low vs high stage |
| F3 | §4.1–4.2 | Availability timeline, 13 outages, maintenance windows shaded |
| F4 | §4.3 | Hour-of-day pass/fail, or day/night S/N distribution |
| F5 | §5 R8 | Co-located station vs camera-only node with indoor compute |

A slide deck derived from this report is a separate deliverable; §2, §4, §5 and §9
are the sections that carry over.
