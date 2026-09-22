# Source Notes 2 — Technology and Measurement Chain

## 1. Plain-language system description

**Documented.** A camera observes the river; a Raspberry Pi-based station records a short video; ORC/ORC-OS derives water level and surface velocity, combines these with surveyed river geometry to estimate discharge, and uploads data and video through LTE to LiveORC.

At Sukabumi, the station wakes every 30 minutes, starts the camera, records, processes, uploads, and shuts down. The normal wake is described as roughly two minutes, with 30–60 seconds spent waiting for camera startup.

**Primary sources:**

- [`spring_2026_ID/docs/REPLICATION_RECOMMENDATIONS.md`](../../spring_2026_ID/docs/REPLICATION_RECOMMENDATIONS.md), “What we did.”
- [`spring_2026_ID/README.md`](../../spring_2026_ID/README.md), “Key Architecture.”
- [`spring_2026_ID/docs/REPLICATION_RECOMMENDATIONS_APPENDIX.md`](../../spring_2026_ID/docs/REPLICATION_RECOMMENDATIONS_APPENDIX.md), §§A1 and A7.

## 2. What is observed versus inferred

### Directly observed or supplied

- Image frames/video of the river surface.
- Surveyed ground-control coordinates and cross-section geometry.
- A water-level reference/search range and camera configuration.
- Environmental sensor readings included by the station, such as rain, temperature, and humidity, where configured.

### Calculated or inferred

- Optical water level from imagery.
- Surface velocity from movement of visible water-surface features.
- Transformation from image pixels to real-world coordinates using camera calibration.
- Discharge from velocity, water level, and surveyed channel geometry.

**Editorial caution:** Tom's phrase “based solely on camera observations” is too broad because final discharge also depends on an accurate survey, calibration, cross-section, and water-level/geometry assumptions.

**Sources:** technical explanation across the manual; current implementation summarized in the replication report and appendix. The older manual is explanatory background, not the source for deployment-performance claims.

## 3. Required site and measurement conditions

**Documented/proposed.** Site suitability is a measurement decision. Important constraints include:

- Visible, trackable surface features.
- Camera view covering a useful portion of the cross-section.
- Stable mounting and stable channel geometry.
- Suitable camera angle, resolution, and distance.
- Lighting and sun angle compatible with optical water-level detection.
- Survey access and a method that can meet accuracy gates.
- Adequate power, connectivity, physical access, permission, and maintenance safety.

Sukabumi's urban canal presented buildings, sky obstruction/RF conditions, and unfavorable sun/geometry constraints. Recommendations R16–R18 say to select the site before hardware, confirm written permission, and involve academic/basin partners.

**Sources:**

- [`spring_2026_ID/SITES.md`](../../spring_2026_ID/SITES.md).
- [`spring_2026_ID/docs/RECOMMENDATIONS.md`](../../spring_2026_ID/docs/RECOMMENDATIONS.md), R16–R20.
- [`spring_2026_ID/LESSONS_LEARNED.md`](../../spring_2026_ID/LESSONS_LEARNED.md), §§5–7.

## 4. Calibration and survey

**Measured.** Two RTK surveys on consecutive days showed approximately 99 cm horizontal and 139 cm vertical check-point spread, with same-marker drift up to 89 cm. This exceeded the applicable RTK gate by roughly 30 times.

**Measured/documented.** IPB replaced the RTK method with a total-station survey. Deployed `Fit 6`, applied June 11, 2026, uses IPB data alone and fits at 0.037 m RMSE against the 5 cm target, with `z_0 = h_ref = 615.0 m`.

**Conflict/stale.** The interim calibration derived from failed RTK data (4.61 cm RMSE on a six-GCP subset, `z_0 = 617.065`) is obsolete and must not be combined with IPB data; the low-water surfaces differ by about 2 m.

**Interpretation boundary.** The 0.037 m RMSE establishes that the camera model fits the selected IPB ground-control geometry within the stated target. It does not establish:

- Water-level accuracy across lighting/flow conditions.
- Surface-velocity accuracy.
- Cross-sectional area accuracy at all stages.
- Absolute discharge accuracy.
- Suitability for a warning threshold.

**Source:** [`spring_2026_ID/docs/REPLICATION_RECOMMENDATIONS_APPENDIX.md`](../../spring_2026_ID/docs/REPLICATION_RECOMMENDATIONS_APPENDIX.md), §A3.1.

## 5. Architecture and design principles

**Documented.** Five constraints governed component selection:

1. Commodity parts with multiple suppliers.
2. No soldering; screw terminals, plugs, or headers.
3. No specialist assembly skills.
4. Common hand tools.
5. Any component replaceable in five minutes.

Additional retained principles in R30–R35:

- Factory-sealed commercial camera.
- Recovery media and procedures kept with the station.
- English and Bahasa Indonesia documentation.
- Local spares and part-swap maintenance.
- Alignment with existing Indonesian hydrometric practice.
- Open processing stack.
- Three unused relay channels retained for future siren, beacon, PA, or messaging interfaces.

**Caution:** available relay outputs are extensibility, not proof that alerts were implemented or used.

## 6. Power and connectivity configurations

### Sukabumi

- Solar/battery station, 30-minute duty cycle.
- Corrected estimated consumption: approximately 118 Wh/day rather than 94 Wh/day.
- Estimated no-sun autonomy: approximately 2.5 days rather than 3.2.
- Witty Pi provides wide-input conversion, low-voltage/temperature cutoffs, and full power removal, but separates wake control from ORC-OS shutdown.

### Jakarta

- Designed as commercial-power, always-on configuration with UPS.
- Always-on operation avoids repeated camera boot, repeated white-light flash, short diagnostic windows, and the missed-wake latch.
- Not field deployed.

**Source:** replication appendix §A7.

## 7. Camera constraints

**Measured/documented.** ANNKE C1200/Hikvision G6-platform findings include:

- Recorded video download through the desired HTTP interface is unavailable in ANNKE firmware; production capture uses live RTSP.
- Configured 16 Mbps baseline delivered about 15.5 Mbps; appendix estimates 10–20% RTSP overhead.
- Camera emits a full-brightness white-light flash for 2–3 seconds at every power-on; tested configuration approaches did not suppress it.
- Boot milestones are about 30 seconds for basic activity and about 60 seconds for network readiness.

These are specific to the tested platform/firmware and should not be generalized to camera monitoring as a whole.

## 8. Architecture options for the next phase

**Proposed.** Repository recommendations include:

- Mains/always-on as default where site measurement requirements permit.
- Industrial Pi carrier with integrated NVMe, protected RTC, power/UPS telemetry, and possibly modem.
- Independent water-level reference.
- Bench/test station built before remote operational stations.
- Split architecture: camera/sensors at the river, compute at IPB/BHLK or another facility.
- Camera-only field node installed using common security-camera skills.

The split and camera-only arrangements were designed/researched but not field tested by this deployment.

**Sources:** recommendations R1, R8, R11, R27, R36, R37 and [`spring_2026_ID/docs/SPLIT_ARCHITECTURE_DESIGN.md`](../../spring_2026_ID/docs/SPLIT_ARCHITECTURE_DESIGN.md).
