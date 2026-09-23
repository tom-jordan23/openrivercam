# OpenRiverCam Humanitarian Whitepaper — Working Brief

**Status:** Working brief based on Tom's completed questionnaire; audience revised after first review, 23 September 2026
**Target length:** 8–10 pages, excluding cover and references
**Target publication date:** November 1, 2026 (assumed from `11/1`; confirm)
**Primary form:** Technical implementation and lessons-learned paper for humanitarian IT
**Final editor:** Tom
**Final approval:** Tom, Dan, and Teguh

**Writing voice:** Follow [`VOICE_GUIDE.md`](VOICE_GUIDE.md), adapted from Tom's public writing-style repository. Use a blend of humanitarian executive, humanitarian technical, and academic/shared-governance voice. The voice guide governs expression; the source notes govern facts.

## 1. Working title

**Beyond the Technology: Partnerships for Humanitarian River Monitoring and Anticipatory Action**

Alternative titles:

- **OpenRiverCam in Indonesia: Lessons in Technology, Partnership, and Humanitarian Preparedness**
- **From River Data to Humanitarian Action: Partnership Lessons from OpenRiverCam in Indonesia**
- **Building the Partnerships Behind Humanitarian Hydrology: Lessons from an OpenRiverCam Deployment**

## 2. Paper purpose

The paper will use the Indonesia OpenRiverCam project as a candid lessons-learned case to show:

1. The potential of emerging, open technologies to generate high-frequency local river data for flood and drought preparedness, operational awareness, anticipatory action, recovery, and climate adaptation.
2. The technical and organizational complexity that still prevents these systems from being consumer-level tools a National Society can simply purchase and operate alone.
3. The importance of durable collaboration among National Societies, universities, government scientists, local communities, and technology developers.
4. The need to design the complete data-to-action pathway: generation, quality control, sharing, interpretation, analysis, decision-making, and humanitarian action.

The paper is not principally a product pitch or an impact evaluation. No humanitarian decisions have yet been made using the Sukabumi data. Its contribution is the implementation experience, the evidence generated so far, the failures and adaptations, and the partnership model emerging from the work.

## 3. Primary audience

**Humanitarian IT:** technical leads, field ICT staff, infrastructure and systems engineers, and data/platform teams in National Societies and humanitarian organizations who would assess, integrate, deploy, or support this service.

Assume familiarity with networks, Linux systems, remote support, data pipelines, and constrained field operations. Explain hydrology, surveying, camera calibration, and measurement uncertainty; do not assume specialist knowledge of those disciplines. Humanitarian program leaders, university partners, and government scientists are secondary readers.

The paper should enable a technical reader to assess the architecture, understand failure mechanisms, identify integration and support obligations, and define evidence required before operational adoption. Include concrete components, interfaces, power and connectivity constraints, data-quality boundaries, and recovery responsibilities. Keep configuration commands and assembly instructions in linked technical documentation.

## 4. Intended reader takeaway

Advanced technology has substantial humanitarian potential, but realizing that potential requires partnerships with university, government, technical, and local-community actors. Those relationships must be intentionally developed before technology can reliably support anticipatory action or climate adaptation.

## 5. Central thesis

> The OpenRiverCam technology is promising, but the durable value of the Indonesia project lies in the partnerships required to deploy it, understand its data, and connect scientific observation to humanitarian preparedness and action.

Short form:

> The technology is interesting; the partnerships are transformative.

## 6. Editorial position and claim boundaries

### The paper can establish

- An open, camera-based river-monitoring station can be built from relatively low-cost, adaptable components and operated in a difficult field environment.
- Camera-based, non-contact monitoring offers potential advantages at locations where in-water work is dangerous or impractical.
- The system can support off-grid power and multiple connectivity strategies.
- High-frequency observations may be useful for studying rapid-onset events, including flood waves.
- The project produced an operating station, a documented measurement chain, a field-tested hardware design, survey and calibration experience, operational documentation, and a substantial record of failures and adaptations.
- Effective deployment required complementary expertise from humanitarian, university, government, community, and technology partners.
- The next phase should be driven by explicit hydrologic questions and a defined data-to-action pathway.

### The paper must qualify carefully

- OpenRiverCam's effectiveness for anticipatory action is a prospective use, not yet a demonstrated humanitarian outcome in Sukabumi.
- The approximately USD 1,340 Sukabumi bill is a scoped materials cost, not a complete installed cost or lifecycle cost.
- The 0.037 m figure is camera-calibration fit RMSE against a 5 cm target; it is not proof of final discharge accuracy.
- Reports of extremely low maintenance at other sites should be attributed to Hessel or supported with an independent source; they are not findings from this deployment.
- Relays can support sirens or messaging integrations, but the project has not demonstrated an operational end-to-end warning system.
- Temporal resolution provides the potential to observe rapid events; the project has not yet demonstrated warning lead time or operational response benefits.
- BMKG's interest in drought modeling and risk-based forecasting must be verified and described with approved wording before publication.

### The paper should not claim

- Demonstrated lives saved, losses avoided, warning-time improvements, or humanitarian decisions changed
- That monitoring alone constitutes an early-warning system
- Consumer-level maturity or operation without technical expertise
- Independently validated discharge accuracy across flow regimes unless new evidence becomes available
- That all sites are suitable or that OpenRiverCam should replace established monitoring methods

## 7. Narrative arc and page plan

### Page 1 — Executive summary: technology opens the door; partnership makes it useful

- Humanitarian need for usable local hydrologic information
- What the Indonesia project attempted
- What it demonstrated
- What it did not yet demonstrate
- Principal lesson: partnership is the enabling infrastructure
- Recommended next step: hydrology-led collaborative pilot

**Target:** 450–550 words
**Lead:** Tom, finalized jointly

### Page 2 — From river observation to anticipatory action

- Flood and drought preparedness, operational awareness, response planning, recovery, and climate adaptation
- Why local stage and flow observations may complement forecasts and regional products
- The full chain: observation → validated data → interpretation → decision protocol → communication → action
- Clear distinction between a monitoring station and a complete early-warning or anticipatory-action system

**Target:** 450–550 words
**Lead:** Dan
**Contributors:** Tom on the data chain; Teguh on Indonesian institutions

### Page 3 — What OpenRiverCam is

- Technical explanation of image acquisition, edge processing, local persistence, synchronization, and server delivery; define hydrologic concepts
- Direct observations versus calculated quantities
- Camera, survey, water level, river geometry, compute, power, connectivity, server, and data products
- Suitability conditions and limitations
- Boundary between upstream ORC/ORC-OS/pyorc/LocalDevices work and this project's station engineering and field implementation

**Target:** 750–900 words; allocate additional space from general framing and partnership repetition
**Lead:** Tom

**Exhibit:** System and data-flow diagram with interfaces, failure boundaries, and quality checks

### Page 4 — The Indonesia project and its partnership model

- Project origin, grant, objectives, and evolution
- Roles of American Red Cross, PMI, IPB, BHLK, BMKG if applicable, LocalDevices, the Sukabumi PMI team, and SIBAT volunteers
- Sukabumi and Jakarta configurations and intended purposes
- Community support and field collaboration

**Target:** 450–550 words
**Lead:** Dan on origin and humanitarian direction; Teguh on partner roles and local context

**Exhibits:** Site map/status panel and one field photograph

### Page 5 — What the deployment demonstrated

- Current Sukabumi status
- Build and operating accomplishments
- IPB total-station survey and current calibration
- Off-grid operation and connectivity
- Data and analysis products generated
- Documentation, repairability, and support model
- Jakarta as the intended always-on demonstration and test station, while stating clearly that it was never deployed

**Target:** 500–600 words
**Lead:** Tom

**Exhibits:** AR view, time series, or verified-results panel

### Page 6 — Failure as evidence: what the field taught us

- Failed RTK surveys and successful recovery through IPB
- Daylight optical water-level failures and need for an independent reference
- Power, duty-cycle, connectivity, synchronization, server, and observability issues
- Jakarta site-permission failure
- Distinguish technical defects, design choices, field constraints, and ownership gaps

**Target:** 550–650 words
**Lead:** Tom
**Review:** Dan for accessible framing; Teguh for institutional accuracy

**Exhibit:** Observation → consequence → response table

### Page 7 — The real system is institutional

- Why a National Society should not be expected to supply every discipline internally
- Proposed division of responsibility among National Society, university, government, community, and technology partners
- Scientific data generation, stewardship, quality assurance, sharing, interpretation, and analysis
- Local ownership, maintenance, funding, and the post-grant transition
- The value of sustained collaboration beyond OpenRiverCam

**Target:** 500–600 words
**Lead:** Dan
**Contributors:** Teguh on local operations; Tom on technical support boundaries

**Exhibit:** Partnership and responsibility diagram

### Page 8 — From pilot technology to humanitarian capability

- Next phase led by explicit hydrology questions developed with IPB and government partners
- Basin and river selection for rain, flood, and drought behavior
- Site selection and deployment gates
- Technical validation and independent reference measurements
- Measures of availability, validity, latency, maintainability, operator usability, community acceptance, cost, decision use, and humanitarian relevance
- Data-to-action protocols and partner ownership

**Target:** 500–600 words
**Lead:** Tom on technical/evidence design; Dan on humanitarian learning; Teguh on feasible Indonesian arrangements

**Exhibit:** Staged learning and scale pathway

### Page 9 — Recommendations and conclusion

- Do not fear emerging technology, but plan for its maturity curve
- Begin with the hydrology and humanitarian decision, not the device
- Build the partnership before the station
- Secure site permission and community support early
- Fund survey, validation, data stewardship, maintenance, and interpretation
- Design for local repair and institutional continuity
- Treat failure documentation as part of responsible innovation
- Invite National Societies, universities, and government agencies to develop shared climate-adaptation capability

**Target:** 400–500 words
**Lead:** Tom, finalized jointly

## 8. Author responsibilities

### Tom — technical lead and final editor

- Technical system and measurement explanation
- Field evidence and quantitative claims
- Failure analysis and design recommendations
- Exhibits using survey and ORC data products
- Evidence ledger and numerical verification
- Editorial integration and final decisions

### Dan — senior humanitarian lead

- Project origin, grant purpose, and original success criteria
- Humanitarian problem and anticipatory-action framing
- Partnership proposition and institutional model
- Administrative and programmatic cost considerations
- Humanitarian review and external positioning

### Teguh — Indonesia program and partnership lead

- Indonesian institutional and operational context
- PMI, local-government, university, and community roles
- In-country activity and site experience
- Sukabumi PMI and SIBAT contribution
- Indonesian-context review
- Facilitation and review of Bahasa Indonesia translation

### Shared responsibilities

- Executive summary
- Central recommendations
- Acknowledgements
- Partner descriptions and implied endorsements
- Final approval

## 9. Evidence and source policy

Every substantive claim will be entered in an evidence ledger and classified as:

- **Measured:** directly supported by project data
- **Documented:** supported by a dated project record
- **Reported:** supplied by a named person or partner but not independently verified
- **Inferred:** the project team's interpretation of evidence
- **Proposed:** a recommendation or future possibility

The current repository record should be the factual spine:

- `README.md`
- `spring_2026_ID/README.md`
- `spring_2026_ID/findings/`
- `spring_2026_ID/ISSUE_LOG.md`
- `spring_2026_ID/LESSONS_LEARNED.md`
- `spring_2026_ID/docs/RECOMMENDATIONS.md`
- `spring_2026_ID/docs/REPLICATION_RECOMMENDATIONS.md`
- `spring_2026_ID/docs/REPLICATION_RECOMMENDATIONS_APPENDIX.md`
- `spring_2026_ID/BOM_Sukabumi.md`
- Current survey provenance and the deployed camera configuration

The older humanitarian research report and manual may be used to discover sources, but their factual claims must be re-verified before publication.

## 10. Proposed exhibits

1. System and data-flow diagram
2. Map or status panel for Sukabumi and Jakarta
3. Sukabumi field photograph featuring PMI/SIBAT participation where permission permits
4. Survey diagnostic or calibration visualization
5. ORC output such as an AR view, hydrograph, or time series
6. Failure-to-design-response table
7. Partnership/responsibility diagram
8. Pilot learning and scale pathway

The final layout should use no more than five or six primary exhibits. Each must advance an argument rather than merely decorate the paper.

## 11. Review and approval

1. Tom: technical and numerical review
2. Dan: senior humanitarian review
3. Teguh: Indonesian institutional and contextual review
4. Partner circulation: all descriptions of partner roles, attributed positions, logos, photographs, site names, and quotations
5. Tom, Dan, and Teguh: final publication approval

American Red Cross communications standards and templates will govern branding, accessibility, and presentation.

## 12. Working schedule

This schedule assumes publication by November 1, 2026.

| Date | Milestone |
|---|---|
| By July 31 | Confirm brief, title direction, author assignments, venue, and partner list |
| By August 14 | Complete evidence ledger, source packet, exhibit inventory, and outstanding interviews |
| By August 28 | Dan and Teguh section briefs complete |
| By September 11 | All first-draft sections and rough exhibits complete |
| By September 25 | Integrated first draft complete |
| By October 2 | Technical, humanitarian, and Indonesian-context reviews complete |
| By October 9 | Partner circulation draft complete; potential alignment with Hessel's October WMO presentation confirmed |
| By October 16 | Partner comments and permissions due |
| By October 23 | Revised text, Indonesian translation plan, and layout complete |
| By October 28 | Final proof, citation audit, accessibility check, and approvals complete |
| November 1 | Publish or release |

## 13. Open questions and verification needs

These items remain open; they do not prevent drafting the first version.

### Direction and logistics

- Confirm that the deadline is November 1, 2026.
- Confirm Hessel's October WMO event, exact title, date, location, audience, and relationship to this paper.
- Obtain the relevant American Red Cross communications template and standards.
- Decide the publication venue and citation style.

### Humanitarian and partner evidence

- Obtain Dan's account of project origin, grant purpose, original objectives, success criteria, and evolution.
- Obtain PMI, SIBAT, IPB, BHLK, and any BMKG feedback suitable for publication.
- Verify BMKG's expressed interest in drought modeling and risk-based forecasting, including approved wording.
- Confirm correct names, titles, and contributions for acknowledgements.
- Document the SIBAT consultation and community-support process in publishable terms.
- Confirm permission and credits for logos, photographs, site names, quotations, and identifiable imagery.

### Technical evidence

- Freeze a dated dataset cutoff for all station-status and performance claims.
- Produce a defensible summary of captures, valid results, failure modes, flow conditions, and data gaps.
- Distinguish station uptime, capture success, processing validity, upload success, and end-user availability.
- Describe the status and results of independent discharge comparison work.
- Define what the 0.037 m calibration RMSE does and does not establish.
- Confirm the exact scope and exclusions of all cost figures.
- Decide which claimed maintenance experience from other deployments can be sourced and attributed.

### Data responsibility

- Locate and assess the repository documentation Tom referenced for privacy, data governance, safeguards, and misuse risks; fill any gaps rather than assuming they are covered.
- Document current image access, retention, server location, security, and deletion practices.
- Decide whether identifiable people or private property must be masked in published imagery.

## 14. Drafting guardrails

- Lead with the humanitarian service requirement, then explain the architecture and its operational dependencies. Make partnership concrete through technical ownership, scientific validation, support, and decision authority.
- Be candid about failures and unresolved limitations.
- Separate current evidence from future potential in every section.
- Never convert a calibration statistic into a discharge-accuracy claim.
- Never imply that Sukabumi data has already triggered humanitarian decisions.
- Treat monitoring as one component of anticipatory action, not the whole system.
- Describe Jakarta as built but never deployed.
- Attribute partner interest or opinions and obtain approval before publication.
- Use “could,” “may,” and “is intended to” where outcomes are prospective.
- Preserve Tom's intended closing message: technological maturity takes time and expertise, while partnerships create the lasting capability.
- Follow Tom's characteristic argument sequence: problem → framework → specific approach → evidence → tradeoff → practical guidance.
- Write as an experienced practitioner addressing capable peers: calm, exact, candid about complexity, and optimistic about what partners can learn together.
- Use active, translation-friendly sentences and avoid idioms, marketing language, and generic enthusiasm.
- Name local contributions and authority specifically; do not present Indonesian partners or communities as passive recipients of outside expertise.
