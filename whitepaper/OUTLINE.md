# Beyond the Technology: Partnerships for Humanitarian River Monitoring and Anticipatory Action

**Working outline — 22 September 2026**  
**Form:** Technical implementation and lessons-learned paper, 8–10 pages excluding cover and references  
**Primary audience:** Humanitarian IT — technical leads, field ICT, infrastructure engineers, and data/platform teams  
**Audience revision:** 23 September 2026; assume IT literacy and explain hydrology and measurement uncertainty  
**Target release:** 1 November 2026, pending confirmation  
**Authors:** Tom, Dan, and Teguh; Tom is final editor

This outline follows the [working brief](WORKING_BRIEF.md), [source notes](source_notes/README.md), and [voice guide](VOICE_GUIDE.md). Section claims below are proposed arguments, not publication-ready prose. Evidence marked **measured**, **documented**, **reported**, **inferred**, or **proposed** should retain that status through drafting and review.

## Central argument

Camera-based river monitoring can produce useful local observations, but observations become humanitarian capability only when partners can validate, interpret, steward, and act on them. The Indonesia deployment demonstrates both the promise of the technology and the practical work needed to make it reliable. Its most durable result may be the collaboration among PMI, community volunteers, universities, government specialists, the American Red Cross, and technology developers.

**Claim boundary:** The project has not demonstrated a warning, anticipatory action, changed humanitarian decision, or independently validated discharge accuracy across flow conditions. It is a field implementation and learning case, not an impact evaluation.

## 1. Executive summary — the capability and the partnership (about ½–1 page)

**Lead:** Tom; joint final review.

1. Open with the practical problem: local stage and flow observations can inform flood and drought preparedness, but data alone do not specify an action.
2. State what the project attempted in Indonesia: adapt and deploy OpenRiverCam stations with PMI and partners, learn whether they could operate under local field conditions, and explore how their data might support hydrologic and humanitarian work.
3. Summarize what is established: Sukabumi was deployed; a usable camera fit followed IPB's total-station survey; operation exposed measurement, power, storage, synchronization, connectivity, and institutional ownership problems. Jakarta was built but never deployed because site permission did not materialize.
4. State the central lesson: technical expertise, local presence, scientific validation, data stewardship, and decision authority need named owners.
5. End with the next step: a hydrology-led, jointly governed pilot that defines the decision question, independent reference measurements, operating responsibilities, and data-to-action pathway before scaling.

**Evidence/qualification:** Use current station status and metrics with a dated cutoff. State explicitly that no Sukabumi data have yet triggered humanitarian decisions. Do not equate camera-fit RMSE with discharge accuracy.

## 2. The humanitarian question — from river observation to action (about ¾ page)

**Lead:** Dan; Tom on data chain; Teguh on Indonesian institutions.

1. Describe the decisions that better local evidence could inform: preparedness for rapid flood development, drought monitoring, operational awareness, response planning, recovery, and longer-term climate adaptation. Keep each use prospective unless a documented decision exists.
2. Explain why local observations may complement forecasts, rain gauges, and established hydrometric networks, while remaining dependent on site suitability and validation.
3. Introduce the complete chain: **question → observation → quality control → stewardship → analysis → interpretation → decision protocol → communication → action → learning**. Identify the station's current contribution mainly at observation and initial quality control.
4. Distinguish a monitoring station from an operational early-warning or anticipatory-action system. Thresholds, authority, communications, accessible messages, and community response arrangements require separate design and testing.

**Evidence/qualification:** Dan should anchor the anticipatory-action account in actual Red Cross practice. Any contextual statistics or external examples need original, verified sources; the older manual is a research lead only.

## 3. Measurement chain and deployment architecture (about 1½–2 pages)

**Lead:** Tom.

1. Explain the system in plain language: a fixed camera records the river; survey data relate pixels to physical space; software estimates surface movement and water level, then uses river geometry and assumptions to estimate discharge. State precisely which inputs are observed, supplied by survey or other instruments, and calculated.
2. Show the concrete station and data path: PoE camera → RTSP capture → Raspberry Pi / ORC-OS processing → local records and media → LTE synchronization → LiveORC → quality review and downstream use. Explain wake/shutdown ownership, limited energy and storage, backlog recovery, and capture-to-delivery reconciliation. Separate deployed components from proposed architectures.
3. Explain the conditions for useful measurements: visible surface tracers, suitable camera angle and field of view, reliable water level, accurate survey and cross-section, stable mounting, adequate light, and independent checks.
4. Explain the limits: glare and low-contrast water, obscured views, changing channel geometry, errors in water level or survey, intermittent power and communications, and the difference between a calculated value and a validated one.
5. Credit upstream ORC/ORC-OS/pyorc and LocalDevices separately from this project's station engineering, integration, field methods, documentation, and analysis. Describe the stack's openness precisely; do not imply that every repository artifact has a formal reuse license.

**Exhibit 1:** One system and data-flow diagram that also marks where quality checks and human decisions occur.

## 4. The Indonesia case and the people behind it (about ¾–1 page)

**Leads:** Dan on origin and grant; Teguh on local roles; Tom on configurations.

1. Give the project origin, initial objectives, funding arrangement, intended success criteria, and how the work evolved. **Dan to supply.**
2. Describe each partner's documented contribution and proposed future role without treating the proposed division as an executed agreement: PMI and Sukabumi staff/SIBAT volunteers; American Red Cross; IPB; BHLK; LocalDevices; BMKG only if its participation and position are confirmed.
3. Describe Sukabumi: installed in April 2026, solar powered, scheduled duty cycle, with video and sensor uploads. Describe Jakarta: a planned mains-powered, always-on demonstration and test station, built but never deployed after site permission failed.
4. Make local collaboration concrete. Explain who identified and maintained the site, supported installation, engaged the community, conducted the survey, evaluated measurements, and managed data access. Record the limits of the current documentation rather than generalizing about community consent.

**Exhibit 2:** Small map/status panel or one permitted field photograph with a factual caption. Obtain permission for people, site identification, and credits.

## 5. What the deployment demonstrated (about 1 page)

**Lead:** Tom; IPB/BHLK review of attributed work.

1. Report the dated Sukabumi operating status, the measurements and products available, and the flow conditions represented. Distinguish captures, valid processing, successful uploads, and data available to an end user.
2. Explain why IPB's total-station survey mattered after two unsuccessful RTK surveys. The deployed `Fit 6` calibration achieved **0.037 m camera-fit RMSE against a 5 cm target**; this establishes camera-fit quality for that configuration, not water-level, velocity, or discharge accuracy.
3. Describe what field operation established about off-grid scheduling, connectivity, local repair, documentation, and remote support. Include failures as part of that result.
4. State the status of any BHLK reference discharge measurement and ORC comparison. Include a quantitative comparison only when its method, timing, flow conditions, and uncertainty are documented.
5. Describe IPB's recorded rain-gauge and dashboard work as work in progress, subject to partner confirmation. Do not imply that a community dashboard or operational analysis pathway is already live.

**Exhibit 3:** A verified ORC output or calibration diagnostic with date, units, sample window, and interpretation. Select the exhibit after refreshing the evidence ledger.

## 6. Failures as evidence — how the design and method changed (about 1 page)

**Lead:** Tom; Dan and Teguh review framing and institutional accuracy.

Organize this section around **observation → consequence → response**, rather than a chronological defect list.

1. **Survey:** Two RTK attempts produced large errors despite superficially repeatable results. IPB changed the measurement method with a total station. Lesson: repeatability is not accuracy; budget skilled survey work and independent field checks.
2. **Optical water level:** In a July sample of 100 passing and 100 failing videos, all failures occurred in daylight. Specular glint is a strong hypothesis, pending direct frame confirmation. Water-level failure discards the full processing run and affects discharge calculations. Lesson: test under the site's light conditions and add an independent water-level reference.
3. **Duty cycle and storage:** USB/storage faults, tight SD capacity, processing failures, long awake cycles, and missed wake scheduling formed a linked failure chain. Lesson: separate shutdown timing from processing success, use durable storage, instrument power and disk health, and assign one owner to the sleep/wake sequence.
4. **Data delivery:** Sync failures, a server-side video gap, and a 4.8-day communications outage show why station operation, capture, processing, upload, and user availability need separate measures and owners. The prepaid-SIM explanation for the outage is reported, not independently verified.
5. **Permission:** Jakarta's undeployed status shows why written site permission must precede site-specific construction.

**Exhibit 4:** Compact failure/response table with 3–5 cases and evidence labels. If using historical percentages or downtime estimates, include the dataset cutoff and method caveat in the caption.

## 7. The operational system is institutional (about 1 page)

**Lead:** Dan; Teguh on Indonesia and local ownership; Tom on technical boundaries.

1. Explain why no single National Society needs to hold every engineering, surveying, hydrologic, server, and protection specialty internally, while it must have accountable partners for each function.
2. Propose a responsibility map for site selection and permission, community engagement, installation and maintenance, survey and validation, hosting and security, analysis, communication, decision authority, and funding. Present this as a model to negotiate with partners, not an agreement already made.
3. Use concrete examples: IPB's survey recovered the calibration; BHLK's technical critique and reference-measurement interest could strengthen validation; PMI contributes long-term local presence and links to preparedness and response.
4. Discuss the post-grant transition. Current support is funded through 2026; ongoing SIM, hosting, repair, staff time, training, and data export need named owners and funding before operational use.
5. Treat image privacy and data responsibility as part of the operating model. The record has technical access-control notes but does not yet establish an approved retention, sharing, masking, consent, or misuse framework.

**Exhibit 5:** Responsibility and data-to-action diagram. Use partner-specific labels only after those partners confirm their roles.

## 8. A hydrology-led next phase and evidence for scaling (about 1 page)

**Leads:** Tom on technical evidence; Dan on humanitarian learning; Teguh on feasible Indonesian arrangements.

1. Ask IPB and relevant government partners to identify the basin, flood, rain, and drought questions that matter, alongside a defined humanitarian decision. Select sites only after those questions, access, permission, community consultation, and measurement conditions are established.
2. Set predeployment gates: written permission; field-of-view/privacy review; suitable geometry and tracers; reliable survey plan; independent water-level and discharge references; power and connectivity budget; clear owner for each recurring task; data-sharing agreement; and testable acceptance criteria.
3. Use a mains-powered, always-online test station to evaluate camera and software changes before sending them to remote sites. Design the next field units for local repair and observable failures.
4. Measure separate outcomes: observation coverage, calibration and discharge validity across flow regimes, capture/processing/upload latency, station availability, maintenance effort, operator usability, community acceptance, total cost, and actual decision use.
5. Advance in stages: technical validation → sustained operations and stewardship → hydrologic interpretation → agreed decision protocols → evaluated humanitarian use. Specify a stop or redesign response when a gate fails.

**Exhibit 6, if space permits:** Staged learning pathway with evidence required at each gate. Keep the final paper to five or six primary exhibits total.

## 9. Recommendations and conclusion (about ¾ page)

**Lead:** Tom; joint final review.

1. Begin with a hydrologic question and a humanitarian decision, then select the site and tools.
2. Build the partnership and assign authority for survey, validation, data, maintenance, funding, and action before treating the station as operational.
3. Budget the complete lifecycle. The **$1,340.19 Sukabumi electronics/enclosure BOM** excludes the existing solar panel and battery and substantial installation and operating costs; it is not an installed or lifecycle price.
4. Make failure visible through independent reference measurements, health telemetry, clear data-quality labels, and documented incident review.
5. Preserve local repairability, Indonesian-language support, community participation, and responsible data practice.
6. Close with Tom's intended message: adopting emerging technology takes time and expertise; collaboration among National Societies, universities, government, communities, and developers is the lasting capability for climate adaptation and preparedness.

## Exhibits and page discipline

Give architecture, measurement dependencies, failure mechanisms, integration requirements, and service acceptance most of the main text. Compress general humanitarian framing and repeated partnership arguments to retain the 8–10 page target. Explain partnerships through ownership of the technical and decision interfaces.

The main text should fit approximately nine pages. Use **five primary exhibits** by default: system/data flow; site/status or permitted field image; one verified data product; failure/response table; responsibility/data-to-action diagram. The staged pilot pathway can replace another exhibit if it tells the conclusion more clearly. Captions must state date, provenance, uncertainty, and claim limits where relevant.

## Drafting inputs and decisions still needed

These gaps should be assigned during drafting; they do not prevent a first draft.

| Owner | Required input |
|---|---|
| Dan | Grant origin, original objectives and success criteria, Red Cross anticipatory-action framing, administrative costs, and a practical partnership proposition. |
| Teguh | Verified Indonesian partner roles and terminology; publishable PMI/SIBAT and community account; site-permission and post-grant ownership reality; translation and local-context review. |
| Tom | Dated dataset cutoff; refreshed capture, processing, sync, and availability metrics; independent discharge-comparison status; exhibit files; exact cost scope; upstream/project contribution boundary. |
| Partners | Confirm attributed roles and positions, BHLK's formal name and measurement details, IPB's planned work, any BMKG interest, names and acknowledgements, and permissions for logos, photos, quotations, and identifiable imagery. |
| Joint | Publication venue and citation style; November 1 date; communications template; approved image access, retention, sharing, masking, and deletion account; final responsibility model and partner circulation. |

Maintain an evidence ledger alongside the draft. Every quantitative statement and specific partner claim should link to a primary source or be visibly marked as reported, inferred, or proposed. The [source notes](source_notes/README.md) identify the current evidence and unresolved conflicts.
