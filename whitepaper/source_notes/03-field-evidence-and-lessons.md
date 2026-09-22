# Source Notes 3 — Field Evidence, Failures, Costs, and Recommendations

## 1. Evidence summary suitable for the paper

| Topic | Evidence | Status | Important boundary |
|---|---|---|---|
| Current calibration | `Fit 6`, 0.037 m RMSE against 5 cm target | Measured/documented | Camera fit, not discharge accuracy |
| RTK failure | ~99 cm H / 139 cm V repeat spread; drift to 89 cm | Measured | Same method/crew/site repeated similar noise |
| Optical water level | 100 pass + 100 fail sample; all failures daylight, none at night | Measured | Glint is a strong hypothesis, not visually confirmed cause |
| Processing | 2,324 of 5,406 rows ERROR (43%) on Aug. 27 dataset | Measured | Pilot/design diagnosis, not a production benchmark |
| Sync | 2,744 of 5,406 rows FAILED (51%) | Measured | Historical window; status may later change |
| Availability | 13 interruptions in 133.5 observed days; ~24.8 days estimated true downtime | Reconstructed | Method and caveats must travel with statistic |
| SIM outage | 4.8-day loss of reachability while scheduled boots continued | Measured + reported cause | Unfunded SIM cause reported, not independently verified |
| Materials | Sukabumi BOM $1,340.19 | Documented BOM | Excludes existing solar array and many lifecycle costs |

## 2. Survey failure and recovery

Two RTK surveys repeated large errors; processing could construct an internally coherent interim fit, but the underlying survey was unsuitable for certified discharge. IPB's total-station work changed the method and produced the current fit.

**Lesson supported by sources:** repeated precision is not accuracy; after a method fails, change the method and use an independent field check before leaving.

**Sources:** appendix §A3.1; recommendations R2, R19, R20; Lessons Learned §7; Issue Log ISS-FIELD-002.

## 3. Optical water-level finding

**Measured dataset:** July 8–14, 2026; two sets of 100 recent videos by status.

- Failed S/N median 1.630; passing median 4.009.
- Zero failures at night; every failure between 06:00 and 19:00 WIB.
- Failures show morning and afternoon peaks with a solar-noon dip.
- Detected height remains essentially the same, suggesting the search band is not the problem.
- Lowering the acceptance threshold would recover few failures while admitting low-confidence values.

**Inferred:** specular glint best explains the time pattern. Direct frame-based confirmation was pending.

**Operational consequence:** water level is calculated first; when it fails, the entire run is discarded, including usable velocity work. Water-level error also changes cross-sectional area and therefore discharge.

**Sources:** [`spring_2026_ID/findings/optical_wl_daytime_glint.md`](../../spring_2026_ID/findings/optical_wl_daytime_glint.md), validation plan, appendix §A5, recommendations R1 and R14.

## 4. Failure chain: storage → processing → power → outage

The most useful worked example is a chain rather than isolated defects:

1. USB storage produced boot/USB faults and was removed.
2. OS and video then shared the smaller SD card.
3. Disk remained pinned near its purge threshold.
4. Processing failed on 43% of video rows in the measured dataset.
5. Shutdown waited for processing completion.
6. Failed cycles ran to a 25-minute scheduling backstop rather than about two minutes, roughly 12× normal cycle energy.
7. Repeated long cycles could drain the battery.
8. A missed wake left the next alarm in the past, turning one failure into a multi-day interruption.

**Supported recommendations:** integrated storage/power/timekeeping, one owner for the wake/shutdown cycle, timer-driven shutdown independent of processing, disk telemetry, and a test station.

**Sources:** replication report “What we learned”; appendix §§A4, A6, A7; recommendations R10, R12, R13, R25, R36, R37.

## 5. Availability and observability

**Measured/reconstructed.** April 16–August 28, 2026: 133.5 days, 13 interruptions, raw 27.5 days without server rows; about 2.7 days attributed to sensor-upload rather than station downtime, leaving approximately 24.8 days genuine downtime.

**Caveats from the source:**

- Server rows are a proxy for operation.
- Local backfill can distinguish some upload gaps from downtime.
- Rotating local CSVs can destroy evidence before later reconstruction.
- This was a volunteer pilot, not designed to production availability standards.

**Finding:** the station did not proactively report many conditions needed for diagnosis. Fleet monitoring should include wake/shutdown, time awake, power, disk, capture-to-delivery reconciliation, processing stage, suppressive modes, camera reachability, queue depth, and last contact.

## 6. Connectivity, sync, and server

**Measured.** On August 27, the station database contained 5,406 video rows: 2,957 done, 2,324 error, 125 new; 2,536 synced, 2,744 failed, 126 local. Disk had 5.1 GB free against a 5.0 GB purge threshold.

**Documented.** A separate 12-day video gap occurred while sensor rows continued at 48/day, strongly suggesting a server-side issue.

**Other documented findings:**

- Duty-cycled stations can starve backlog synchronization because each wake prioritizes the newest work.
- A LiveORC one-to-one database collision caused HTTP 500 responses for some video uploads even though clips were present server-side.
- Nine post-outage failures resolved into multiple fault classes rather than one generic connectivity problem.
- Bulk media mirroring through the REST API took the server down; bulk transfer needs a separate route.

**Sources:** appendix §A6; all files in [`spring_2026_ID/findings/`](../../spring_2026_ID/findings/); Issue Log; Lessons Learned §11.

## 7. 4.8-day communications outage

**Measured.** The station continued scheduled boots during a 4.8-day period when it was unreachable, reconstructed from a 5,714-boot record.

**Reported cause.** The prepaid SIM had no funds. The source treats this as consistent with the evidence but not independently verified.

**Lesson:** an operational technology program needs ownership for recurring costs and must distinguish station health from connectivity and remote reachability.

**Source:** [`spring_2026_ID/findings/sukabumi_duty_cycle_2026-08-28_outage.md`](../../spring_2026_ID/findings/sukabumi_duty_cycle_2026-08-28_outage.md).

## 8. Cost notes

### Supported figures

- Sukabumi electronics/enclosure materials: **$1,340.19**.
- Existing 200 W solar panel and 50 Ah battery were not included.
- Jakarta project BOM total: approximately **$1,333**, with $1,076.88 actually ordered for a one-camera configuration.
- Contract survey planning estimate: **Rp 5–15 million per site**, indicative rather than an actual project invoice.
- Indonesian automatic stage-station comparator: about **Rp 58 million / $3,600 ex-VAT**, which needs fresh authoritative verification before external publication.

### Exclusions from the headline BOM

Shipping, customs, contingency, locally supplied solar equipment, survey, site works, travel, labor/staff time, training, connectivity/SIM, hosting, maintenance, spares, replacement, translation, and decommissioning.

**Editorial recommendation:** say “approximately $1,340 in recorded electronics and enclosure materials for Sukabumi, excluding…” Do not say “a $1,000 station” unless using loose spoken shorthand that is corrected immediately.

**Sources:** [`spring_2026_ID/BOM_Sukabumi.md`](../../spring_2026_ID/BOM_Sukabumi.md); appendix §§A3 and A7; Lessons Learned §9.

## 9. Recommendations with strongest evidentiary support

1. Start with the hydrology question and site, not the hardware.
2. Secure written site permission before site-specific construction.
3. Treat survey as skilled, budgeted work and use an independent check.
4. Add an independent water-level reference.
5. Build a mains-powered, always-online test station first.
6. Instrument station health for fleet operation.
7. Give one process ownership of the complete sleep/wake cycle.
8. Use integrated, durable storage/power/timekeeping.
9. Preserve local repairability, bilingual documentation, and recovery media.
10. Write partner responsibilities and operating costs into the agreement.

## 10. Evidence still needed

- Dated data cutoff and refreshed station metrics for the final paper.
- BHLK August 21 discharge measurement method, number, timing, and uncertainty.
- A valid ORC/reference discharge comparison across useful flow regimes.
- Confirmed current status of optical-level method testing.
- Lifecycle cost and maintenance/staff-time estimate.
- Operator usability or training evaluation.
- Decision on which availability statistics are appropriate for a short public paper.
