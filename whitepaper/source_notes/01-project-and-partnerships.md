# Source Notes 1 — Project, Chronology, and Partnerships

## 1. Project identity and scope

**Reported by Tom, September 23, 2026.** The paper covers two installations: October 2025 using a PTBox, and April 2026 using devices Tom built. This clarification expands the earlier draft’s April-only scope. It supersedes the voice guide’s earlier claim that the October 2025 date was incorrect.

**Documented.** The root [`README.md`](../../README.md), opening section, describes this repository as the engineering record for camera-based river-monitoring stations built for PMI and the American Red Cross and deployed in Indonesia in April 2026. It explicitly distinguishes this work from the upstream ORC and ORC-OS software maintained by LocalDevices.

**Useful paper distinction:**

- Upstream technology: ORC measurement software, ORC-OS, pyorc/OpenRiverCam ecosystem, LocalDevices.
- This project's contribution: station hardware and integration, procurement, power/connectivity, surveying workflow, assembly and operator documentation, field deployment, operational analysis, and lessons.

**Primary sources:**

- [`README.md`](../../README.md), introduction, repository layout, partners, and related projects.
- [`spring_2026_ID/README.md`](../../spring_2026_ID/README.md), “Key Architecture,” documentation inventory, and design principles.
- [`spring_2026_ID/docs/REPLICATION_RECOMMENDATIONS.md`](../../spring_2026_ID/docs/REPLICATION_RECOMMENDATIONS.md), “What we did.”

## 2. Station chronology and status

### October 2025 — PTBox installation

**Reported by Tom.** The first installation covered by the paper took place in October 2025 using a PTBox. The [Sukabumi site record](../../spring_2026_ID/SITES.md) identifies the April work as a redeployment after trapped humidity affected the earlier combined compute/video unit. The [PTBox and design-evolution note](05-ptbox-and-design-evolution.md) assembles the preparation, survey workflow, environmental observations, and design responses. Individual on-site credits and an equivalent PTBox performance dataset remain to be established.

**Available research leads:** archived [PTBox configuration files](../../prior_work/legacy_hardware/) and [survey procedures with PTBox instructions](../../survey/SURVEY_PROCESS_v2.md). These establish available technical material, not a verified as-installed configuration or an installation date by themselves.

### April 2026 — devices built by Tom Jordan

**Reported by Tom/documented.** The later phase used devices built by Tom. The repository describes the Sukabumi installation and a separate Jakarta unit that was built but remained undeployed. Do not confuse these two units with the two installation phases.

### Sukabumi — April 2026 build

**Documented.** Built and installed in April 2026; solar powered; scheduled on a 30-minute duty cycle; uploads video and sensor data to LiveORC. The current configuration uses IPB total-station data.

**Measured/documented.** Deployed camera configuration `Fit 6` was applied June 11, 2026 and fits at 0.037 m RMSE against a 5 cm target. The value is calibration fit, not discharge accuracy.

**Primary sources:**

- [`README.md`](../../README.md), “Status.”
- [`spring_2026_ID/README.md`](../../spring_2026_ID/README.md), “Station Status.”
- [`spring_2026_ID/docs/REPLICATION_RECOMMENDATIONS_APPENDIX.md`](../../spring_2026_ID/docs/REPLICATION_RECOMMENDATIONS_APPENDIX.md), §A3.1.

### Jakarta — April 2026 build

**Documented.** Built and software-ready, but never deployed because permission for the intended site did not materialize. It remained at Wisma PMI and had been unpowered since April at the dates of the current records.

**Original purpose, from Tom's questionnaire:** an always-on, commercial-power demonstration station near PMI headquarters; a visitor demonstration, configuration test platform, and source of shareable example data.

**Proposed current use.** Study/test unit for IPB or BHLK, not an operational unit with availability expectations, because it embodies a design now recommended for revision.

**Primary sources:**

- [`spring_2026_ID/ISSUE_LOG.md`](../../spring_2026_ID/ISSUE_LOG.md), ISS-FIELD-001.
- [`spring_2026_ID/LESSONS_LEARNED.md`](../../spring_2026_ID/LESSONS_LEARNED.md), §6.
- [`spring_2026_ID/docs/REPLICATION_RECOMMENDATIONS.md`](../../spring_2026_ID/docs/REPLICATION_RECOMMENDATIONS.md), “What we did” and “The path forward.”
- [`PROGRAM_TODO.md`](../../PROGRAM_TODO.md), TODO-211.

## 3. Partnership evidence

### PMI and community volunteers

**Documented.** The replication report credits PMI staff and volunteers in Sukabumi and Jakarta with building, supporting, and looking after an unfamiliar system. The repository does not yet name the individuals or formally document the SIBAT consultation described by Tom.

**Reported by Tom.** The project had strong community support through PMI's SIBAT volunteer network. This is important but needs a publishable account and partner confirmation.

**Supported role model.** Lessons Learned §10 argues that PMI/Red Cross strengths include local language, community trust, long-term site presence, volunteer networks, installation, maintenance, and connecting output to humanitarian action.

### IPB

**Measured/documented contribution.** IPB performed the total-station re-survey that provided suitable control after two RTK surveys showed the need for a different method and underpins the deployed configuration.

**Documented active collaboration.** [`PROGRAM_TODO.md`](../../PROGRAM_TODO.md), opening commitments and TODO-401, records that:

- PMI and IPB agreed that IPB would analyze ORC data, integrate its rain gauges, and build a community-facing dashboard.
- IPB installed three sets of rain gauges on August 22–23, 2026.
- IPB requested API access; an account passed an 18-test verification matrix on September 9, but credentials had not yet been handed over at the recorded status.

These are working-log facts and should be confirmed with IPB before publication.

### BHLK

**Documented active collaboration.** [`PROGRAM_TODO.md`](../../PROGRAM_TODO.md) records that BHLK:

- Asked to inspect the station hardware and receive the repository/install material.
- Measured discharge at Sukabumi on August 21, 2026 and wanted a comparison with ORC output.
- Suggested captures around 45 seconds rather than the current 5 seconds.
- Offered server capacity.

The comparison, rationale for 45 seconds, and server transition were still open. The document also flags that BHLK's formal full name needs confirmation.

### American Red Cross

**Documented.** The root README names American Red Cross as a project partner. The repository contains little narrative on the grant's origin or American Red Cross management role.

**Assigned source.** Dan should supply project origin, grant purpose, initial objectives, success criteria, and evolution. Tom identifies Dan as manager of the American Red Cross International Services Data, Tech and Innovation group and the senior humanitarian advisor who helped identify and secure the grant.

### LocalDevices / Hessel Winsemius

**Documented.** Root README credits LocalDevices and Hessel for the upstream open platform and project support.

**Needs attribution/source.** Tom reports that Hessel visits other sites only a few times per year to clear vegetation. This is not evidence from the Indonesia deployment and should be quoted/attributed or independently sourced.

### BMKG

**Repository support is limited.** Lessons Learned §§8–9 discusses BMKG's institutional role in rainfall rather than river stage/discharge and refers to the ombrometer standard. It does not substantiate Tom's statement that BMKG showed interest in future drought modeling and risk-based forecasting.

**Action:** obtain approved wording, speaker, date/context, and whether the interest was exploratory or a commitment.

## 4. Emerging division of responsibility

**Proposed/inferred, not an executed governance agreement.** Two repository formulations are useful:

- [`spring_2026_ID/LESSONS_LEARNED.md`](../../spring_2026_ID/LESSONS_LEARNED.md), §10: university owns or leads technology; Red Cross owns deployment and operations.
- [`spring_2026_ID/docs/RECOMMENDATIONS.md`](../../spring_2026_ID/docs/RECOMMENDATIONS.md), R29: BHLK on data processing and standards; IPB on design, calibration methodology, and training; PMI on installation, maintenance, and response.

This supports the paper's central argument, but the exact allocation should be described as a recommendation unless partners have formally agreed.

## 5. Sustainability and transition

**Documented.** Tom's questionnaire states that connectivity, hosting, repairs, consumables, and support are grant-funded through the end of calendar 2026, after which PMI must determine the arrangement.

**Documented risk.** [`PROGRAM_TODO.md`](../../PROGRAM_TODO.md), TODO-208 and TODO-213, records:

- The current server cannot be sustained past the grant without a transition.
- BHLK's server offer is not yet a migration plan.
- Funding continuity needs a named PMI owner.
- Durable data export is required regardless of hosting outcome.

This is strong evidence for the claim that open technology does not eliminate institutional ownership or operating-cost requirements.

## 6. Publication caveats and missing information

- Use [source note 5](05-ptbox-and-design-evolution.md) for the PTBox account and design transition; complete its publication checks. Keep later station metrics and costs separate from the PTBox evidence.
- All descriptions of partner roles require circulation and approval.
- Partner logos are not the project's assets to license; permission is required.
- Correct individual names, titles, and acknowledgements are missing.
- SIBAT participation is reported by Tom but not adequately documented in the repo.
- BMKG interest requires verification.
- The replication report is a draft prepared after an August 21 meeting and was not yet circulated at its August 31 version.
- [`PROGRAM_TODO.md`](../../PROGRAM_TODO.md), TODO-202, says a formal repository license has not landed. The intent to share is documented, but legal reuse rights remain incomplete.
