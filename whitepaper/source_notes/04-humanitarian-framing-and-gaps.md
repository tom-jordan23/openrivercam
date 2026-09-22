# Source Notes 4 — Humanitarian Framing, Data-to-Action, Ethics, and Gaps

## 1. Humanitarian proposition supported by the project

The strongest defensible proposition is not that OpenRiverCam has delivered anticipatory action. It is that the deployment explored a potentially useful local observation capability and revealed the technical and institutional requirements for turning observations into humanitarian capability.

**Supported potential uses:**

- Studying river response and establishing a local evidence base.
- Flood and drought preparedness.
- Operational awareness and response planning.
- Complementing government/university hydrology work.
- Longer-term climate adaptation collaboration.

**Not demonstrated in Sukabumi:** a warning issued, action threshold used, operational decision changed, population reached, lead time gained, loss avoided, or life saved.

Tom explicitly states that no humanitarian decisions have yet been made using Sukabumi data; the effort has primarily explored deployment/support and what may be done with generated data.

## 2. Data-to-action chain

The paper can use the following model, while labeling most downstream elements as future work:

1. **Question:** define the hydrologic and humanitarian decision before selecting a site.
2. **Observation:** collect video, water level, geometry, velocity, rainfall or other complementary variables.
3. **Quality control:** validate calibration, flag uncertainty/failure, monitor station/data health, compare against an independent reference.
4. **Stewardship:** establish who owns, hosts, retains, shares, and documents data.
5. **Analysis:** university/government hydrologists characterize basin response, thresholds, trends, and model inputs.
6. **Interpretation:** responsible agencies translate observations into an assessment or forecast.
7. **Decision protocol:** define who may trigger which preparedness or response action and with what corroboration.
8. **Communication:** disseminate accessible, trusted information through established channels.
9. **Action:** National Society, government, and communities implement agreed measures.
10. **Learning:** compare predictions/actions with outcomes and revise thresholds, models, and procedures.

OpenRiverCam currently contributes chiefly to steps 2–3. The partnership model is intended to build steps 4–10.

## 3. Partnership thesis supported by repository evidence

**Evidence base:**

- The project's survey failed twice and became usable only through IPB's different expertise and equipment.
- BHLK contributes standards knowledge, a reference discharge measurement, technical critique, and a possible hosting route.
- PMI provides local presence, relationships, installation/maintenance capacity, community connection, and the humanitarian action role.
- IPB's planned rain-gauge integration and dashboard illustrate scientific analysis and community-facing interpretation beyond station construction.
- Hosting, SIM funding, API stewardship, survey validation, and maintenance expose responsibilities no single device or open-source license resolves.

**Appropriate conclusion:** partnership is not outreach surrounding the technology; it is part of the operational system.

## 4. Humanitarian background sources: use with caution

[`manual/humanitarian_river_monitoring_research_report.md`](../../manual/humanitarian_river_monitoring_research_report.md) and [`manual/REFERENCES.md`](../../manual/REFERENCES.md) contain leads on WMO, UNHCR, ICIMOD, Practical Action, community warning, and technical literature.

However, [`manual/FACT_CHECK_REPORT.md`](../../manual/FACT_CHECK_REPORT.md) says the manual was not publication-ready and flags:

- Uncited or weakly traced statistics such as 43% fatality reduction and 35–50% economic-loss reduction.
- Cost-range inconsistencies.
- Hypothetical use cases that appear real.
- Unverified partnership and country examples.
- Incomplete humanitarian case-study evidence.
- Unsupported/generalized ±10–20% accuracy language.

**Policy for the outline:** use these documents to build a research list, not as final citations. Re-open original WMO, peer-reviewed, government, or humanitarian sources before including any contextual statistic.

## 5. Contactless monitoring and safety

**Technically supported characteristic:** the camera is mounted outside the water and observes the surface remotely.

**Permissible inference:** this can reduce the need to place or service certain instruments in dangerous flows.

**Avoid:** “eliminates risk” or “personnel never enter the water.” Survey, installation, staff-gauge work, independent validation, bridge/road access, work at height, electricity, and maintenance retain safety risks.

## 6. Anticipatory action and alerts

**Proposed capability.** High-frequency observation could contribute to detecting rapid river changes. Spare relays could interface with a siren, beacon, PA relay, or messaging gateway.

**Not demonstrated.** No threshold-to-warning-to-action chain was operated or evaluated. Hardware relay capacity does not demonstrate community alerting, message accessibility, decision authority, or response readiness.

**Recommended phrasing:** “The design preserves interfaces that could support local alerting, but an operational warning system requires validated thresholds, authority, communication protocols, preparedness, and community response arrangements beyond the station.”

## 7. Privacy and data responsibility audit

### What the repository does contain

- Technical account access, credential, and offboarding notes in [`PROGRAM_TODO.md`](../../PROGRAM_TODO.md), especially TODO-209.
- An open item to decide retention before server migration; a working estimate of roughly 10 GB media/month.
- Storage/deletion behavior and risks documented in findings and recommendations.
- General network-security and access-control guidance in the older manual.
- General site-security/community-engagement language in the older manual.
- A root-level warning that tracked photographs may contain location metadata; repository cleanup is open in TODO-203.

### What is not adequately documented

- Whether camera audio is disabled in the deployed configuration.
- A map of what identifiable people, homes, routes, or property appear in the field of view.
- Community notice/consent records and a complaint mechanism.
- Purpose limitation for imagery.
- Current image retention and deletion policy approved by partners.
- Data controller/steward and server jurisdiction.
- Rules for sharing raw video versus derived measurements.
- Masking/cropping standards for publication or partner access.
- Protection-impact assessment, misuse analysis, breach response, or data-subject request process.
- Policy for surveillance, policing, migration, land/water disputes, or other secondary use.

**Conclusion:** Tom's questionnaire says these safeguards are documented, but the repository search supports only technical security fragments and open retention work. The whitepaper should not claim a mature governance framework. It can identify responsible data practice as a lesson and requirement for the next phase.

## 8. Community evidence

**Reported by Tom:** excellent community support through PMI's SIBAT volunteer network.

**Repository gap:** current source files praise PMI volunteers but do not provide a sufficiently detailed, attributable record of consultation, installation participation, perceptions, concerns, or consent.

**Needed source note/interview:** who participated; what was explained; whether residents/property owners were consulted; concerns raised; how the station is perceived; and whether photographs/quotations may be used.

## 9. Technology maturity framing

The repository strongly supports Tom's intended message:

- The system is not consumer-level.
- It requires electronics/integration, hydrology, survey, IT/server, and operational capabilities.
- Low purchase cost can create higher operating cost.
- Open source enables inspection and extension but does not itself supply support, ownership, validation, security updates, hosting, or lifecycle funding.
- Failure documentation is a responsible-innovation asset when used to improve design.

**Suggested source-backed formulation:** “National Societies need not reproduce every technical discipline internally; they need the partnerships and governance to ensure each discipline is owned.”

## 10. Outline-driving gaps and assignments

### Dan

- Project and grant origin.
- Original objectives and definitions of success.
- Anticipatory-action framing grounded in actual Red Cross practice.
- Administrative and institutional costs.
- How National Societies should identify, formalize, and sustain partners.

### Teguh

- Accurate PMI, SIBAT, IPB, BHLK, and government roles.
- Community involvement and publishable local account.
- Correct Indonesian institutional terminology.
- Local ownership, permission, procurement, and post-grant reality.
- Partner review and Bahasa Indonesia translation.

### Tom / technical record

- Refreshed dataset cutoff and metrics.
- Discharge-validation status.
- Technical boundary between upstream products and project work.
- Final diagrams/data products.
- Cost-scope statement.

### Partner confirmation

- BHLK's formal name, measurement, hosting offer, and recommendation.
- IPB's dashboard/rain-gauge work and intended analytical role.
- BMKG interest and wording.
- Hessel's maintenance experience and October WMO presentation details.
- Permissions for names, logos, photographs, quotations, and identifiable imagery.
