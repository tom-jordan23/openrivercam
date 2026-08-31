# Outline — Recommendations for Replication of the OpenRiverCam Station Design

**Status:** Outline agreed; D1-D6 resolved 2026-08-31. Full draft at `REPLICATION_RECOMMENDATIONS.md`.
**Scope rule (D5):** technology only. No hydrology conclusions.
**Audience rule (D6):** humanitarian and academic leadership. This outline
describes the superseded structure — the report was rebuilt in September against
the style guides, and §§1-12 below no longer match it. Kept for the decision
record; do not write to this structure.
**Not for circulation** in outline form.
**Prepared for:** IPB and BHLK (Balai Hidrologi dan Lingkungan Keairan), following
the PMI / IPB / BHLK meeting at Sukabumi, 21 August 2026.
**Secondary audience:** none. PMI NHQ is not an audience for this document (D3).
**Target length:** 10 pages.
**Audience level:** Scientific, non-specialist in embedded hardware. No part
numbers, wiring detail or code in the body; those are referenced in the appendix.
**Outline date:** 2026-08-31.

---

## Decisions — RESOLVED 2026-08-31

| # | Decision | Resolution |
|---|---|---|
| **D1** | Does §6 stay in the document? | **Keep, reframed as acceptance conditions.** §6 leads with the conditions for the output to be additive to the BBWS record, and presents the correctable / not-correctable distinction as a precondition for meeting those conditions rather than as a rebuttal of the meeting position. Same technical content, no direct contradiction. *Narrowed by D5:* the conditions are now reproduced as design constraints only, and the section no longer positions ORC output against the BBWS rating curve. |
| **D2** | How far to go on permission and licensing in §1. | **Reduce to one sentence** stating that permission and licensing are being handled separately. No detail in the body. |
| **D3** | Is PMI NHQ an audience for this document? | **No — IPB and BHLK only.** The conditional paragraphs flagged in §2 and §9 are dropped. §9 still describes PMI's role, as context rather than as an ask. What PMI is being asked to commit to is a separate conversation. |
| **D4** | Confidence level on unresolved findings. | **Keep §10 as drafted.** All five open items stated as open. |
| **D6** | What register, and how long? | **Humanitarian and academic leadership**, per `STYLE_Humanitarian_Executive.md` and `STYLE_Academic_University_Business.md` (github.com/tom-jordan23/writing). Two criticisms drove it: fixated on the outages, and simultaneously too technical and too vague. The body was rebuilt to ~2,750 words of prose across 12 pages; the outage record moved to appendix A4, mechanism detail moved to the appendix, and the recommendations became a table of what each change buys and costs. A *Questions for consideration* section replaces the bare open-questions list. Protection analysis remains a known gap — existing material was reframed to acknowledge the residents, but no new analysis was written. |
| **D5** | Does the report draw hydrology conclusions? | **No — technology only.** How the output is applied, and what accuracy any application demands, is for IPB, BHLK and their federal partners. Removed: the low-flow / drought area-error argument (§2, exec finding 1, Figure F2), the model-validation argument (§2, §6), the rating-curve positioning (§6), and our comparison of the 30-minute cycle against the 15-minute minimum (§6, R11, A7.3). §2 and §6 are kept, restated as requirements the technology has to meet. Externally-set requirements are still cited, as recorded from BHLK rather than proposed by us. |

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
- Permission and licensing: one sentence stating both are being handled separately (D2).

*Figure candidate: none.*

## 2. What the pilot requires of the design — 0.5 p

Per D5, this section no longer states what the output is for. It states three
properties of the technology that constrain any duplicated unit.

- **Surface velocimetry depends on trackable features on the water surface.**
  Performance is a function of surface state, not a fixed property of the camera,
  and has not been characterised at Sukabumi. Measure it at the pilot sites across
  the conditions those sites present.
- **The surveyed geometry is an input the processing chain cannot recover.**
  Nothing in the video constrains the bed, so survey error propagates through to
  the result. This is what R2 rests on now that the drought argument is out.
- **Reporting cadence is a design parameter, separate from measurement quality.**
  Set by the power architecture: every wake pays a fixed 30–60 s camera boot, so
  shortening the cycle raises energy faster than sample rate. Leads to R11.

*Figure candidate: none. The low-flow area-error schematic (F2) is withdrawn under D5.*

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

**4.1 A missed wake cycle does not self-correct.** 13 discrete interruptions over
133.5 days observed (2026-04-16 to 2026-08-28), reconstructed from the sensor-row
record held on the server. The reportable property is the **duration
distribution**, not the total: 9 under 24 h, 1 at 24-48 h, **none between 2 and 5
days**, 3 at 5 days and over (5.4, 7.3, 9.3 d). The absent middle is the
signature of the latch — a missed cycle leaves the next-startup alarm in the past
and nothing re-arms it. Trigger and latch are separable faults; fixing the latch
converts an open-ended interruption into a 30-minute one. Qualification: at least
one interruption ended unattended in 6.5 h, so recovery may also be
charging-driven (§10).

**Register note (Tom, 2026-08-31): do not dwell on downtime totals.** This is a
volunteer-supported installation and criticising response times is not fair
comment. Every §4 result is framed as a property of the *design* — a fault the
system did not report, a mode with no expiry, two paths nothing reconciles — not
as an operational failing. §1 carries the framing paragraph: the station is
volunteer-supported and rarely visited, so tolerating long unattended periods is
a design requirement. This strengthens R4/R5/R7 rather than weakening them.

Superseded figure: an earlier draft gave "22.7 days of 118 days observed, in 13
outages", and an availability percentage. The first paired ISS-FIELD-008's
May-onward duration and window with ISS-FIELD-010's April-onward outage count;
the second is out of scope per the register note. Regenerated 2026-08-31 over a
single April-onward window via `station_gaps.py --since 2026-04-01`.

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

## 6. Output conditions the design must satisfy — 0.75 p

Reframed per D1 and narrowed per D5: the conditions are reproduced because they
constrain the design, the BOM and the installation procedure, not as an assessment
of whether the output should be accepted.

- Conditions recorded for output to be additive to BBWS time series: level
  referenced to the local staff-gauge zero in metres; 15-minute time step minimum,
  5-minute preferred; SIH3 / SIHLSDA format, CSV or HTTP POST; paired daily manual
  readings during commissioning; uncertainty documented per **SNI 8066:2015** and
  WMO-No. 168 Ch. 5; site report with datum and calibration record.
  Source: `spring_2026_ID/research/indonesia_hydrometric_standards.md`.
  The station's 30-minute cycle is stated as a fact against the time-step
  condition; the comparison is left to the reader (D5).
- **Dropped under D5:** the rating-curve positioning bullet, the low-flow
  correction argument, and the model-validation independence argument.
- What survives of the correction material is metrology rather than hydrology: a
  stable bias is correctable by a fitted relationship, random geometric survey
  error is not and enters the uncertainty budget, and correction of either kind
  needs a reference independent of the ORC output. This is what ties §6 back to
  R1 and R2.

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
informal understanding between individuals.
Source: `spring_2026_ID/LESSONS_LEARNED.md` §10.

## 10. Open questions — 0.25 p

Stated as open, not resolved (D4: keep as drafted).

- The cause of the two unexplained outages, which carry the maintenance-mode
  signature without the mode set.
- Whether the 13 V recovery-voltage setting bounds outage duration. One
  observation is consistent with it; one observation is not sufficient.
- Whether a staff gauge can be read directly from the camera image, removing the
  need for a separate level sensor.
- Absolute discharge accuracy at Sukabumi, unresolved pending the survey.
- Velocimetry performance across the surface conditions at the pilot sites.

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

**Produced 2026-08-31.** Renumbered F1–F4 plus one appendix figure, after F2 was
withdrawn under D5. All are generated by `docs/figures/build_figures.py`; the two
data figures are computed from the recorded data rather than drawn, so they cannot
drift from the record.

| # | Section | Figure | Source |
|---|---|---|---|
| 1 | §3.1 | How a measurement is made — system flow, non-technical register | schematic |
| 2 | §4.1 | Availability: timeline of the 13 interruptions, and their duration on a log scale | appendix §A4 |
| 3 | §4.3 | Optical detection: pass/fail by hour of day, and the S/N distribution against the gate | `findings/ipb_optical_wl_s2n_2026-07-08_to_14.csv` |
| 4 | §5 R8 | Two configurations — everything at the river against camera-only with indoor compute | schematic |
| A1 | app. §A1.2 | The capture path, intended against implemented, and the delivered bitrate | appendix §A1.3 |

*Withdrawn:* the old F2 (vertical error into area error at low stage) went with the
drought argument under D5.

**Photographs.** Five are used, all from the build; there are no field photographs
of the deployed station anywhere in the repository. Every image was opened and
checked before use — `build_photos/PHOTO_METADATA.md` has at least one wrong entry
(IMG_1345, listed as the camera on a pole, is a basement water filter).

**Accessibility.** Two-series palette validated with the data-viz validator (worst
CVD ΔE 24.7, all six checks pass on white). Colour is never the only channel: the
second series is hatched as well as coloured, every series is direct-labelled, and
the figures were checked in greyscale. Each SVG carries `<title>` and `<desc>`;
each figure carries a descriptive caption; every picture in the deck carries alt
text.

A slide deck derived from this report is a separate deliverable; §2, §4, §5 and §9
are the sections that carry over.
