# Beyond the Technology: Partnerships for Humanitarian River Monitoring and Anticipatory Action

**Working draft 0.2 — 23 September 2026**  
**Primary audience:** Humanitarian IT — technical leads, field ICT, infrastructure engineers, and data/platform teams  
**Authors:** Tom Jordan, Dan [surname and title to confirm], Teguh [surname and title to confirm]  
**Target:** 8–10 pages of main text, excluding cover and references

> **Author note:** This is draft prose for discussion, not a cleared publication. Bracketed **TASK** notes assign missing evidence or decisions. Numbered **Source notes** at the end point to repository records and indicate what they support. Partner descriptions, figures, images, and quotations need review before circulation outside the project team.

## Executive summary

For humanitarian IT teams, camera-based river monitoring introduces a field data service with coupled measurement, infrastructure, and support requirements. A camera and edge computer must acquire usable observations, process them against surveyed geometry, retain data through connectivity interruptions, and deliver results whose age and quality are visible to users. The Indonesia deployment shows how failures in storage, scheduling, synchronization, and scientific inputs can interrupt that service even when individual components appear to work. Its humanitarian value depends on partners who can validate the measurements and connect them to an agreed decision process. [1–5]

The OpenRiverCam project in Indonesia explored what it takes to assemble, deploy, and support this kind of monitoring with the Indonesian Red Cross (PMI), the American Red Cross, academic and government specialists, community volunteers, and technology developers. A solar-powered station was installed at Sukabumi in April 2026. A second, mains-powered station was built for Jakarta but was never deployed because permission for the intended site did not materialize. At Sukabumi, the team established a usable camera calibration after IPB University carried out a total-station survey. Field operation also revealed failures in water-level detection, storage, processing, power scheduling, synchronization, connectivity, and data stewardship. [1–3]

These findings support a practical conclusion. Camera-based monitoring is promising, and the current deployment has produced useful technical and institutional learning. It has not yet demonstrated that its discharge estimates are accurate across flow conditions or that its data have changed a humanitarian decision. The next phase should start with hydrologic questions and a defined humanitarian use, then test the complete chain from observation to validated data, interpretation, decision, communication, and action. That work calls for a durable partnership with clear responsibility for each step. [2–4]

**TASK — Dan:** Replace the opening with a specific humanitarian decision that motivated the grant, if it can be documented. Confirm the original objectives and success criteria.  
**TASK — Tom:** Freeze a dataset date and replace the general status language with current, reviewed figures.  
**TASK — all:** Confirm title, author names, venue, and target date. The primary audience is humanitarian IT, as established in the first review.

## 1. The problem is larger than a measurement

Flood preparedness and drought planning require more than regional forecasts. Local river stage and flow observations can help characterize how a particular channel responds to rain, how quickly conditions change, and how unusual a current event may be. Frequent observations might be especially useful where conditions develop faster than a sparse manual measurement schedule can describe. They can also contribute to longer-term work on basin behavior and climate adaptation. These are potential uses of the data; the Sukabumi project has not yet evaluated their effect on warnings or decisions. [4]

The path from a river image to humanitarian action has several distinct steps. A monitoring station observes a site. Operators and scientists must determine whether each observation is valid, maintain a record of gaps and uncertainty, combine it with other evidence, and interpret what it means for a particular basin. Responsible agencies then need agreed thresholds, decision authority, communication channels, and preparedness actions. Communities need information they can understand and use. A camera can contribute to this system, but installing one does not create an early-warning system. [4]

The Indonesia work began by testing the practical foundation for such a system: can the station be built and sustained, can its measurements be trusted, and can the right partners work together around the resulting data? Tom reports that no humanitarian decisions have yet been made using Sukabumi station data. This is an important boundary for the present paper. The case is about implementation and learning, with future humanitarian applications to be tested. [4]

**TASK — Dan:** Supply the real operational decisions and Red Cross anticipatory-action context. Identify what level of evidence or authority would be required before data influenced those decisions.  
**TASK — Teguh:** Explain how local government, PMI, and community channels would receive and use information in the Indonesian context.  
**SOURCE CHECK:** Add current primary humanitarian and hydrology references. Do not carry forward unsupported statistics from the older manual. [4]

## 2. Measurement chain and deployment architecture

OpenRiverCam uses a fixed camera to observe the water surface. The system processes images to estimate surface movement and water level. A careful survey relates locations in the image to physical coordinates and records the river cross-section. Software then uses these inputs and a velocity model to estimate discharge. Each calculation depends on conditions at the site and on the quality of the preceding inputs. A discharge figure is therefore a derived estimate, not a quantity directly visible in the video. [5]

The documented Sukabumi configuration uses an ANNKE C1200 Power over Ethernet (PoE) camera and Raspberry Pi 5 running ORC-OS. Every 30 minutes, the station wakes and captures a five-second video through the Real Time Streaming Protocol (RTSP). ORC-OS processes the video locally into velocity fields and discharge estimates, then synchronizes results and video to LiveORC over LTE. Witty Pi 5 controls scheduled power-on; ORC-OS controls shutdown. This division makes the interaction between task completion and power scheduling a service dependency. These are documented deployment settings, not a newly verified live inventory. [1, 5]

The data path is **camera → RTSP acquisition → local processing and storage → LTE synchronization → LiveORC → review and use**. Surveyed control points, channel geometry, and camera configuration enter at processing. The station therefore has several distinct success states: a clip can exist locally without a valid discharge result, a valid result can await upload, and media can reach the server without becoming a complete user-visible record. Operators need to reconcile those states rather than infer data availability from network reachability. [3, 5, 7]

Solar operation couples compute time and communications recovery to the energy budget. Normal wakes were described as roughly two minutes, including 30–60 seconds of camera startup; failed cycles could reach a 25-minute backstop. A retry policy that is reasonable on an always-on server can consume scarce awake time or never run on this station. Proposed alternatives include mains-powered operation where feasible and separation of field acquisition from processing at a partner facility. The split architecture remains a design proposal, not a result demonstrated by this deployment. [2, 3, 5]

Good site selection is part of the measurement method. The camera needs a stable view of moving surface features, suitable geometry, and lighting that does not defeat the image processing. The survey and water-level reference must be accurate enough for the question being asked. Changing channel shape, glare, obscured views, or a failed water-level estimate can undermine the resulting discharge estimate. An independent reference method is needed before claims of discharge accuracy can be made for operational use. [5, 6]

LocalDevices and the upstream OpenRiverCam ecosystem provide the core measurement software and platform. The Indonesia team's contribution includes station engineering and integration, procurement, power and connectivity choices, survey and field procedures, operator documentation, deployment, and analysis of failures. The software stack provides opportunities for inspection and adaptation, but maintenance, support, licensing, and institutional ownership still require explicit arrangements. [1, 5]

**FIGURE 1 — Tom:** System and data-flow diagram. Separate observed inputs, surveyed inputs, derived results, server delivery, quality review, and human decisions.  
**TASK — Tom/LocalDevices:** Check the precise product names and contribution boundary; confirm how to describe licenses and code reuse.  
**TASK — Tom/IPB:** Add a reviewed account of the deployed surface-to-depth velocity conversion and cross-section assumptions, including their uncertainty. These are required to explain the discharge product to IT readers without implying that software completion establishes measurement validity.

## 3. The Indonesia project was built through collaboration

The American Red Cross and PMI partnered to explore a practical river-monitoring installation in Indonesia. The intended Jakarta installation would have been an always-on, mains-powered demonstration and testing station near PMI headquarters. It was built and prepared in software, but the planned site did not receive the needed permission. The Sukabumi station was installed in April 2026 and became the project's field learning site. [1]

PMI staff and volunteers supported the work in Sukabumi and Jakarta. Tom reports particularly strong participation and community support through the Sukabumi PMI team and its SIBAT volunteer network. The current repository records credit this contribution but do not yet provide a detailed, publishable account of who was consulted, what residents understood about the camera, or what concerns were raised. Those details matter both to fair credit and to responsible camera deployment. [1, 4]

IPB University supplied a decisive technical contribution. After two RTK surveys produced unsuitable control data, IPB conducted a total-station re-survey that supports the deployed camera configuration. The project log also records plans for IPB to analyze OpenRiverCam data, integrate rain gauges, and develop a community-facing dashboard. Those plans should be described as ongoing work until IPB confirms their status. BHLK has provided technical engagement, including a reference discharge measurement and questions about capture duration and hosting. Its formal name, the measurement details, and any future role need direct confirmation. [1, 3]

This case suggests a division of work, but not yet a completed governance agreement. PMI brings local presence, relationships, installation and maintenance capacity, and a connection to preparedness and response. University and government partners can strengthen survey, validation, hydrologic interpretation, and standards. Technology developers support the underlying software. The exact roles, data rights, operating costs, and decision authority need to be negotiated and funded for any operational phase. [1, 4]

**TASK — Dan:** Write the grant origin, original objectives, project evolution, and American Red Cross contribution.  
**TASK — Teguh/PMI:** Replace the general community account with named, approved examples of PMI and SIBAT work; document consultation and permission.  
**TASK — IPB/BHLK:** Review attributed contributions, plans, titles, and institutional names.  
**TASK — Tom:** Add a short chronology with dates and distinguish completed work from planned work.  
**FIGURE 2:** Approved site map/status panel or field photograph with names, date, credit, and image permission.

## 4. What Sukabumi showed, and what it did not

The station established that this team could assemble a field unit, install it at Sukabumi, operate it off grid on a scheduled cycle, and generate images and data products. The deployment also produced documentation for assembly, survey, operation, and troubleshooting. These are real outcomes. They do not by themselves demonstrate sustained data availability, validated discharge accuracy, or an operational decision pathway. [1–3]

The survey history shows why a technically plausible output can still be wrong. Two RTK attempts produced large spread and drift. A processing workflow could build an internally coherent interim fit from those observations, but the underlying control was not suitable for a trusted discharge estimate. IPB's total-station survey changed the method. The deployed `Fit 6` camera configuration achieved a 0.037 m fit root-mean-square error against a 5 cm target. That statistic describes the camera calibration fit. It does not measure final water-level, surface-velocity, or discharge accuracy. [2, 3, 5]

The operational data show why the team needs several measures of reliability. In an August 27 snapshot, 2,324 of 5,406 local video rows had a processing error and 2,744 showed failed synchronization. A reconstructed April–August record identified 13 interruptions in 133.5 observed days and roughly 24.8 days of estimated true downtime after separating some upload gaps from station downtime. These figures describe a historical pilot window and the method used to reconstruct it; they should not be presented as a current availability rate or a production benchmark. [3]

The team also needs a valid independent comparison for discharge. BHLK measured discharge at Sukabumi in August, and a comparison with OpenRiverCam output was requested. The method, result, timing, and uncertainty are not yet assembled into a defensible validation statement. A future comparison should span useful flow conditions and should preserve the uncertainty of both methods. [1, 3]

**TASK — Tom:** Replace historical figures with a dated table of scheduled captures, successful captures, valid water levels, processed results, successful uploads, user-visible results, and gaps. Keep denominators and definitions in the source note.  
**TASK — Tom/BHLK:** Document the August reference measurement and any comparable ORC results; omit an accuracy conclusion until supported.  
**FIGURE 3:** One verified calibration view, time series, or AR view, with date, units, provenance, and a caption that states what it demonstrates.

## 5. Failure exposed the full operating chain

The project encountered failures at several points in the chain from image to usable information. Their value lies in the changes they suggest, provided that the paper distinguishes observation from suspected cause.

Water-level detection is one example. In a July sample of 100 passing and 100 failing videos, every failure occurred during daylight; none occurred at night. The time pattern is consistent with reflected sunlight, but direct image-based confirmation was still pending in the reviewed record. Lowering the acceptance threshold would admit weak readings and recover few of the failed cases. When water-level detection fails, the full processing run is discarded, including velocity information that may otherwise be usable. The next design should test lighting at the actual site and add an independent water-level reference. [3, 6]

Storage and scheduling failures compounded each other. A USB storage problem led the team to put the operating system and video on a smaller SD card. Low free space coincided with processing errors. Shutdown waited for processing to finish, so failed cycles could remain awake until a 25-minute backstop instead of ending after roughly two minutes. The extra load could drain the battery, and a missed wake could turn a short fault into a longer interruption. This chain argues for durable storage, power and disk telemetry, and one controller responsible for the entire wake and shutdown sequence. [3]

Data delivery created a different kind of ambiguity. Sensor rows continued during a 12-day gap in server video, suggesting that the station and the delivery path had different health states. In another event, scheduled boots continued during a 4.8-day period without remote reachability. The operating record attributes that outage to an unfunded prepaid SIM; the account balance has not been independently verified. These cases show why an operator needs to know whether the station woke, captured, processed, queued, uploaded, and made data available to users. They also show why a recurring connectivity payment needs an owner. [3]

Two software incidents make the delivery boundary more specific. A September 2 analysis of ORC-OS 0.6.0 found that backlog synchronization starts after a 60-second delay, while the capture path can shut down the station about 15 seconds after completing the current job. Across 823 observed boots, the backlog task was cut off before checking on 45% of wakes. On the remaining wakes it searched a queue that failed records did not enter. Extending awake time alone would therefore leave a second fault unresolved. [7]

A separate LiveORC investigation found that an upload could commit its video row and file, then fail while attaching a time series already assigned to another video. The one-to-one database constraint produced HTTP 500, while the station marked the upload failed even though the clip existed on the server. The technical lesson is to distinguish transport failure, partial server completion, and processing failure; recovery must reconcile records on both sides before assuming that retransmission restores a usable result. These findings describe the investigated versions and dates, not a claim that the defects remain present today. [7]

Finally, Jakarta's site-permission failure was operational rather than computational. The team completed a station that could not serve its intended location. Written permission and a viable maintenance arrangement should precede site-specific construction. [1]

**TABLE 1 — Tom:** Four-row “observation / consequence / response / remaining test” table covering survey, optical level, duty-cycle/storage, and data delivery.  
**TASK — Tom:** Check whether later testing confirmed the glare hypothesis or changed the recommended water-level method.  
**TASK — Dan/Teguh:** Review how the paper presents responsibility for SIM funding and site permission; preserve the lesson without assigning unverified blame.

## 6. The durable system is a partnership

A National Society should be able to use scientific information without being expected to employ every specialist needed to produce it. A river-monitoring service may require surveyors, hydrologists, software and power engineers, data stewards, field operators, and people who understand local risk and response practice. A partnership becomes useful when these tasks have named owners, shared standards, and a way to resolve problems after the initial installation. [1, 4]

The Sukabumi record makes this concrete. IPB's change in survey method improved the basis for calibration. BHLK's interest in a reference comparison and capture duration points toward scientific validation beyond station operation. PMI's staff and volunteers supplied local support and a possible route from information to community preparedness. LocalDevices supported the upstream technology. None of these contributions substitutes for the others. The proposed division of responsibility is a starting point for a negotiated arrangement, not a formal agreement already in force. [1, 4]

The operating model also needs money and governance. The recorded Sukabumi electronics and enclosure bill was approximately US$1,340, excluding the existing solar panel and battery. It also excludes shipping, customs, site work, survey, labor, travel, training, connectivity, hosting, spare parts, replacement, and long-term support. Tom reports that current costs are grant-funded through the end of 2026. Hosting transition, SIM funding, data export, and post-grant maintenance remain open. A low materials bill is useful, but it cannot stand in for installed or lifecycle cost. [1, 3]

Camera imagery raises responsibilities beyond ordinary sensor data. The repository contains technical access-control notes and an open retention decision, but it does not yet establish an approved framework for identifying people or property in the field of view, retaining or sharing raw video, masking published images, responding to complaints, or preventing secondary use. These issues belong in the partnership agreement and site review before wider deployment. [4]

For an operational handover, we propose a defined data contract between the monitoring service and downstream dashboards or decision tools. Each observation should carry a station identifier, capture time and time zone, units, processing and quality status, configuration provenance, and delivery time. Reprocessed observations should remain distinguishable from earlier results, and missing or rejected measurements should remain explicit. A dashboard must be able to distinguish an old valid observation from a new failed one. This is a proposed integration requirement; the project has not yet established it as a complete implemented interface.

The IT support agreement should likewise identify who owns device access, server administration, software and configuration changes, backup and restore, connectivity payments, and escalation to field staff or measurement specialists. Raw imagery and derived measurements need separately agreed access and retention rules. Recovery procedures should cover loss of connectivity, exhausted local storage, station replacement, and restoration of the survey and calibration configuration. These responsibilities make the partnership operationally testable rather than leaving “maintenance” as an undivided obligation.

**FIGURE 4 — Dan/Teguh/Tom:** Responsibility map covering site and community, measurement, validation, hosting, privacy, maintenance, funding, decision, and communication. Label partner roles as proposed until confirmed.  
**TASK — Teguh/PMI:** Identify an accountable post-grant owner for each recurring obligation and describe local repair and support realistically.  
**TASK — joint:** Establish an approved description of image access, server location, retention, sharing, masking, deletion, and community feedback. Do not claim an existing comprehensive protection framework.

## 7. A next phase designed around learning and use

The next phase should begin with questions from hydrologists and intended humanitarian users. IPB and relevant government partners could help identify which basins and river behaviors are worth studying for flood and drought applications. PMI and other local actors should identify the decisions that better information could support and the community arrangements needed to use it. Only then should the team select sites and decide what equipment, reference measurements, and operating model each site requires. [4]

A candidate site should pass several gates before installation: written permission; suitable camera view, lighting, tracers, and channel geometry; a defensible survey plan; independent water-level and discharge references; power and connectivity budgets; community consultation and image safeguards; and named owners for maintenance, data, and recurring costs. The project should test changes on an always-on station before moving them to a remote duty-cycled unit. [2–4]

The pilot should measure more than whether a station turns on. It should track valid observations across flow regimes; uncertainty against independent references; time from capture to usable result; station, processing, and delivery availability; maintenance hours and cost; operator usability; community acceptance; and whether a defined decision was actually informed. A staged review can then decide whether to improve the method, change site or architecture, or test an operational protocol. Scaling should follow evidence of reliable measurements and responsible use, not the number of installed cameras. [3, 4]

Technical acceptance should use a defined observation window and separate denominators. Capture coverage is successful captures divided by scheduled captures; processing yield is accepted results divided by captured clips; timely delivery is accepted results available within an agreed latency divided by scheduled observations. Track capture-to-availability latency, oldest pending upload, remaining storage, awake duration, and field interventions alongside these ratios. The team should set thresholds from the intended use and test outage recovery before adopting them as service commitments. These are proposed measures, not achieved service levels.

**TASK — Tom/IPB/BHLK:** Specify the hydrologic questions, validation methods, reference instruments, flow conditions, and acceptance thresholds.  
**TASK — Dan/Teguh/PMI:** Specify one plausible decision pathway and how it would be evaluated without claiming a current operational outcome.  
**TASK — joint:** Agree on data stewardship, lifecycle funding, and go/no-go gates before naming candidate sites.  
**FIGURE 5:** Staged pathway from technical validation through sustained operation, hydrologic interpretation, agreed decisions, and evaluated humanitarian use.

## Conclusion

The Indonesia project shows both the attraction and the difficulty of emerging monitoring technology. A relatively modest materials budget and adaptable components can put a capable instrument in the field. Reliable measurements require suitable sites, skilled survey, independent validation, dependable operation, and care for the data and people the camera may capture. Useful humanitarian information requires further work: analysis, authority, communication, and practiced action. [1–4]

The strongest result so far is therefore a way of working. PMI's local presence, IPB's survey and scientific work, BHLK's technical engagement, the American Red Cross's support, community volunteers, and the upstream developers each contribute a piece of the capability. Future pilots should make those relationships durable, assign responsibilities openly, and evaluate whether the resulting information actually improves decisions. Technology will mature through testing and repair; the partnerships built around it can support a wider shared response to flood, drought, and climate risk.

**TASK — all:** Review the closing for accurate credit, institutional voice, and a concrete invitation to the next collaboration. Obtain partner approval for attributed positions before publication.

## Source notes for drafting

These are working citations to repository material, not a final reference list. Add external primary sources and page or section references during revision.

1. **Project and partners:** [source note 1](source_notes/01-project-and-partnerships.md); primary records include the [repository overview](../README.md), [deployment overview](../spring_2026_ID/README.md), [issue log](../spring_2026_ID/ISSUE_LOG.md), and [program TODO](../PROGRAM_TODO.md). Partner descriptions and plans require confirmation.
2. **Survey and design lessons:** [replication recommendations](../spring_2026_ID/docs/REPLICATION_RECOMMENDATIONS.md), [appendix](../spring_2026_ID/docs/REPLICATION_RECOMMENDATIONS_APPENDIX.md), and [recommendations](../spring_2026_ID/docs/RECOMMENDATIONS.md). These are internal working syntheses; check underlying measurements for numerical claims.
3. **Field metrics, failures, and costs:** [source note 3](source_notes/03-field-evidence-and-lessons.md), [findings](../spring_2026_ID/findings/), [lessons learned](../spring_2026_ID/LESSONS_LEARNED.md), and [Sukabumi BOM](../spring_2026_ID/BOM_Sukabumi.md). Historical windows must be dated and updated before release.
4. **Humanitarian framing and gaps:** [source note 4](source_notes/04-humanitarian-framing-and-gaps.md) and [Tom's questionnaire](QUESTIONS_FOR_TOM.md). Prospective uses, partner reports, and missing protection details are identified there.
5. **Measurement chain:** [source note 2](source_notes/02-technology-and-measurement.md), with links to survey and configuration records. Calibration fit must not be described as discharge accuracy.
6. **Optical water-level analysis:** [daylight failure finding](../spring_2026_ID/findings/optical_wl_daytime_glint.md). The daylight pattern is observed; glare remains a hypothesis until direct image review confirms it.

7. **Synchronization failure mechanisms:** [ORC-OS 0.6.0 backlog analysis, September 2](../spring_2026_ID/findings/orc_os_backlog_sync_starvation.md) and [LiveORC partial upload/database collision, September 3](../spring_2026_ID/findings/liveorc_video_500_timeseries_collision_2026-09-03.md). Version-specific incident evidence; distinguish historical findings from current software status.
