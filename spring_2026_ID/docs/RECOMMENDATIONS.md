# Recommended improvements — working list

**This is the source.** Adjust it here and the report
(`REPLICATION_RECOMMENDATIONS.md`) and deck (`build_deck.py`) are regenerated to
match. Do not edit those two for content.

**Numbers are identities, not an order.** R1–R15 keep the meanings they had;
R16–R28 are new, from your comments and from a scan of `LESSONS_LEARNED.md`,
`ISSUE_LOG.md`, `build_notes/` and the BOMs. Say the word and I will renumber
sequentially and carry it through the appendix cross-references.

**Still to decide:** this is now 28 items, which is more than a leadership
document can carry. My suggestion is that the report presents the groups and the
strongest two or three in each, with the full list as an appendix table. Tell me
where to cut.

---

## Acknowledgement — for the report, not a recommendation

Draft, to open the report:

> None of this exists without the people who built and looked after it. PMI
> volunteers and staff at Sukabumi and Jakarta gave their time to a system that
> was new to them and did not always work. IPB re-surveyed the site with a total
> station after our own survey failed twice, and that survey is what the station
> runs on today. BHLK brought the standards knowledge and the offer of server
> capacity that make a pilot possible at all. What follows is a list of things we
> would do differently. Every one of them was learned because someone did the
> work that made it visible.

---

## Choose the site before anything else

- **R16 — Treat site selection as a measurement decision, not a logistics one.**
  The site sets limits that no later work can undo: satellite positioning quality
  for the survey, the sun–water–camera angle that governs optical water level,
  and how much of the flow the camera can resolve across the section. Sukabumi is
  an urban canal with buildings close on both banks, and all three of those went
  against us there.

- **R17 — Confirm site permission in writing before any hardware is built for
  that site.** The Jakarta station was built and tested around an intended site
  whose permission was expected and did not arrive. It has never been installed.
  Permission is a prerequisite for the build, not a parallel activity.

- **R18 — Engage local academic and basin partners in site selection.** IPB and
  BHLK know the rivers, the basin offices and the access constraints. This is
  work they are better placed to do than we are.

## Improve measurement accuracy

- **R1 — Fit an independent water-level reference.** A level sensor, or a staff
  gauge in the camera's view tied to the *papan duga air* zero.

  Optical water level is the weakest part of the chain and it is worth being
  precise about why. The station reads the level from the video, and it fails
  through the whole of daylight — in a 200-capture sample every rejection fell
  between 06:00 and 19:00 and none at night. It matters more than a missing level
  because water level is computed first: when it fails, the whole measurement is
  discarded, including the surface velocity work that succeeded (see R14). And
  the level feeds the cross-sectional area, so an error in it scales the
  discharge figure directly. The station currently produces dependable flow
  numbers only at night. *Cost: sensor, or gauge plus the survey tie.*

- **R2 — Plan the survey as skilled work from the start, and budget for it.**
  "Professional" is probably the wrong word — IPB and BHLK both have people
  capable of high-quality survey. The point is that the survey is unforgiving and
  cannot be recovered later: the surveyed bed geometry is an input the processing
  cannot reconstruct.

  What we learned the hard way: two RTK surveys on consecutive days, same
  equipment and crew, reproduced the same ~99 cm horizontal / ~139 cm vertical
  check-point spread, with same-marker drift up to 89 cm. IPB's total-station
  survey replaced the method and is what the station runs on today, at 3.7 cm
  RMSE. *Cost: Rp 5–15 million per site if contracted.*

- **R19 — If a survey method fails once at a site, change the method.** Repeating
  RTK with the same rover, base and crew reproduces the same noise: the likely
  causes — base-station coordinate quality, multipath, sky obstruction, RF
  interference — all recur at the same site with the same equipment. Doing it
  twice is collecting the same evidence twice, not verifying it.

- **R20 — Carry an independent check of a different kind, and use it before
  leaving site.** A tape-measured distance between two control points, a
  levelling check, a known benchmark inside the camera view. It has to fail while
  the team is still there, not weeks later in processing.

## Improve monitoring

- **R4 — Build a monitoring regime for a fleet, not a station.** ORC-OS reports
  enough for one station being watched by the people who built it. An agency
  running ten or fifty needs more, and will need to add it. What should be
  monitored, based on what we could not see when we needed it:

  - **Did it wake, and did it shut down?** Wake time, shutdown time, and time
    awake per cycle. A cycle running long is the earliest visible sign of the
    failure in R10.
  - **Power.** Battery voltage and current together (R6), and state of charge if
    the controller reports it.
  - **Free disk space**, against the threshold at which files start being deleted
    (R13).
  - **Captured against delivered**, per station and per day (R7).
  - **Processing outcome per video** — succeeded, failed, and at which stage.
  - **Any mode that suppresses data**, with an alert if it stays set and an
    automatic expiry.
  - **Camera reachability and time to first frame**, which is the boot cost paid
    every cycle.
  - **Last contact per station**, so a station that goes quiet is visible without
    anyone asking.

  The station should send this on every wake. *Cost: modest software; this is the
  single highest-value area of work in the list.*

- **R5 — Have the station send diagnostics; do not require a login.** The station
  is awake for tens of seconds — not long enough to open an interactive session.
  At Sukabumi a station that was awake and uploading was recorded as unavailable,
  because the only route to it needed a connection that never opened inside the
  wake window. No polling rate fixes a window that short.

  The diagnostics that would have saved us the most time, and why:

  - **Why it powered on** — scheduled alarm, power restored, or manual. Separates
    a normal cycle from a recovery after a power loss.
  - **The shutdown reason for the previous cycle**, or its absence. An absent
    shutdown is the R10 failure and was invisible for months.
  - **Disk free, and what was deleted since last cycle.** This was the root cause
    and nothing reported it.
  - **Processing errors with the stage that failed**, not just a count.
  - **Upload queue depth** — how many recordings are waiting, and the oldest.
  - **Voltage and current at wake, mid-cycle and at shutdown**, which is what
    separates a failing battery from a heavy load.

  *Cost: small.*

- **R6 — Record voltage and current together.** The station logs temperature,
  rainfall and humidity, and nothing electrical, so "the battery is the suspect"
  stayed unfalsifiable for months. Voltage on its own cannot separate a failing
  battery from a heavy load. The Witty Pi already reports voltage and current
  over the I2C link the sensor software uses. *Cost: a current-sensing module and
  its logging.*

- **R21 — Remove the rain gauge from the camera station.** Rainfall at the
  measurement point mostly affects flow *downstream* of it. What matters for the
  flow being measured is rainfall *upstream* in the catchment, so a gauge on the
  camera pole does not answer the question it was added for. It also costs a
  bulkhead, a gland, UART wiring and a service.

  If rainfall is wanted, put a standalone, networked gauge where the catchment
  makes it useful, and let it report on its own. For the camera station, an SHT40
  for internal temperature and humidity is worth keeping and is enough — do not
  add more.

- **R7 — Compare what was recorded against what arrived, automatically.** The
  station knows what it captured and the server knows what it received. Nothing
  compares them, so data goes missing with no symptom at either end. This belongs
  in the fleet monitoring of R4. *Cost: negligible.*

## Give one process control of the sleep and wake cycle

- **R10 — One process should control both shutdown and startup.** At Sukabumi
  these are split between two systems, and that split caused a large share of the
  outages.

  How it works now: the station software (ORC-OS) decides when to shut down,
  using a setting that shuts down after the processing task finishes. The
  scheduling board (Witty Pi) decides when to start up, using an alarm set for
  the next wake. Neither controls the whole cycle.

  Two failures result, and they compound:

  - **The station does not shut down.** When processing does not finish, shutdown
    never fires. Processing failed on 43% of videos because the disk stayed full
    at its deletion threshold. The station then ran to the scheduling board's
    25-minute backstop instead of stopping after about two minutes — roughly
    twelve times the energy for that cycle. Repeated across a night, that
    flattened the battery. This was the root cause found in August.
  - **The station does not start again.** A missed wake leaves the next-startup
    alarm in the past and nothing sets a new one, so one missed cycle becomes
    days.

  Either device can own the cycle, but one of them must, and the next wake should
  be set as part of shutting down. The Raspberry Pi's own clock does this: the
  operating system writes the alarm at shutdown, so the two halves cannot
  disagree.

  Two cautions. The Pi's own clock was the original design and was replaced late
  in the build because a small battery connector failed on both boards — treat it
  as fragile and keep a scheduling board in spares. And on a solar site the
  scheduling board does real work the Pi's clock does not: cutting power
  completely rather than leaving the Pi in standby, accepting 6–30 V straight
  from the battery, and providing low-voltage and temperature cut-offs. *Cost:
  saves about USD 50 per station where the board is removed; otherwise software.*

- **R12 — A processing failure must not prevent shutdown.** Shutdown should be
  driven by a timer that runs regardless of what the processing task does, so a
  bad video costs one measurement rather than a night of battery.

## Improve the server and the processing chain

- **R13 — Manage disk space before it stops the station working.** The station
  disk stayed pinned at the level where it deletes old files, which caused the
  processing failures behind R10 and deleted recordings before they could be sent
  again. Free space should be reported with station health, should alarm before
  the deletion threshold, and recordings not yet delivered should be the last
  deleted. *Cost: small.*

- **R14 — A failed water level should not discard the whole measurement.** Level
  is computed first, and when it fails the entire run is abandoned including the
  surface velocity that already succeeded. Storing the partial result keeps the
  velocity data and makes the failure visible as a missing level rather than a
  missing measurement. *Cost: software only.*

- **R15 — Monitor the server as well as the station.** Video stopped arriving for
  twelve days while the station was healthy and logging throughout, and nobody
  noticed. Two server constraints found in practice also belong in the design:
  the video store and the database must share one filesystem, and server and
  station software versions are tied together, so a server upgrade obliges the
  stations to follow — which a duty-cycled remote station cannot do on demand.

- **R22 — Plan video storage before the fleet grows.** Storage scales with the
  number of stations multiplied by the capture rate, and it is the cost that
  grows fastest as a network expands. Decide up front how long raw video is kept,
  whether it is kept at all once a measurement is derived, and where the boundary
  sits between the station, the server and any archive. A policy chosen early is
  much cheaper than one forced by a full disk.

- **R23 — Configuration edits must go through one interface.** Editing the
  ORC-OS database directly is not durable: the dashboard later writes its
  in-memory copy over the row, and any form interaction can trigger it. This
  reverted a calibration value during bring-up at Sukabumi and sent processing
  back to optical water level without any warning. Use the dashboard or the API,
  and treat this as worth raising with the ORC-OS maintainers — the save should
  be a partial update rather than replacing the whole record.

- **R24 — Do not move bulk media through the API.** Mirroring media through the
  REST interface took the server down. Bulk transfers need a path that does not
  go through the application.

## Choose parts for operating cost, not just purchase price

- **R9 — These stations were built with low unit cost as the primary goal, and
  some of those choices raise operating cost at volume.** That trade was
  reasonable for two prototypes and should be re-examined for a network. Apply
  the budget to the whole station rather than to each part separately, and screen
  any part under software control before buying it.

- **R25 — Three specific parts cost more than they saved.**

  - **The camera.** Bought for about USD 60 against a professional alternative
    near USD 1,268. It meets its specification, but its firmware is a reseller's
    version with capability removed. Recorded video cannot be fetched over HTTP,
    so capture falls back to a live stream and delivers about 15.5 Mbps against
    the 20 Mbps the processing chain wants. Its light fires at full brightness on
    every power-on and cannot be disabled. Its cold-boot time is paid on every
    wake.
  - **USB storage.** The chosen flash drive caused a driver fault at boot — 228
    USB disconnects and 158 errors in twelve minutes, which knocked the modem off
    the bus. It was removed rather than fixed.
  - **The SD card as the only volume.** With the USB drive gone, the operating
    system and all captured video ran from the SD card. That is what made the
    disk small enough to hit its deletion threshold, which caused the processing
    failures, which prevented shutdown, which flattened the battery. A cheap part
    removed early became the root cause of the outages months later.

  For the next build: **use NVMe storage**, and **record to the camera's own card
  and fetch the file**, rather than streaming over RTSP.

- **R26 — Check the control interface before buying anything under software
  control.** For a camera: can recorded files be fetched, not only streamed; can
  the illuminator be disabled in every mode including at power-on; what is the
  cold-boot time to first frame; and is it the manufacturer's own firmware or a
  reseller's version.

## Choose the architecture to suit the site

- **R11 — Mains power should be the default. Use solar only where mains is not an
  option.** An always-on mains station removes the wake cycle, and with it the
  latch, the boot cost paid every cycle, the light firing 48 times a day, and the
  diagnostic window that is too short to use.

- **R8 — Consider putting the computer indoors, and decide deliberately where the
  processing happens.** Camera and sensors at the river, computer at a BHLK or
  IPB facility over a network link. Two questions worth separating: where the
  hardware lives, and where the computation happens.

  Processing at the station and sending only the derived values suits a thin or
  expensive link, and keeps working when the connection does not. Sending video
  and computing centrally suits a good link, and puts the processing where it can
  be re-run, corrected and improved without visiting anything. It also allows a
  calibration to be revised and the whole archive reprocessed — which we could
  not do here. *Designed, not yet field tested.*

- **R27 — A camera-only field node is the most deployable version of this
  system.** A PoE camera, an injector, power and a network path can be installed
  by any security-camera installer, using suppliers and skills that already exist
  in every country. Everything ORC-specific then lives in the compute layer.
  This lowers what has to be asked of a landowner, and it removes the enclosure,
  battery and modem from the riverbank.

## Support local construction and maintenance

- **R3 — Specify interfaces, not part numbers.** Publish which properties must be
  matched — voltage, current, ingress protection, operating temperature — and
  which are free to vary, such as brand and mounting style. Parts will be bought
  in Indonesia under Indonesian procurement rules, so substitution is normal and
  should not require asking us.

  Two things that would have helped us: a **site adaptation checklist** to walk
  the design against local conditions before ordering, and a **bilingual
  specification sheet** with photographs, so a local team can source parts without
  a translation problem in the middle of it. "Shielded Cat6 outdoor cable, F/UTP,
  UV-resistant jacket" can be sourced; "Cat6 cable" cannot.

- **R28 — Order locally-sourced parts weeks in advance, not on arrival.**
  Procurement consumed most of the first two days in Jakarta and forced a
  substitution that changed the power architecture. Identify which trade would
  normally buy each item, and ask the local team where that trade shops — this
  reaches the right supplier faster than searching general hardware stores.

## Divide responsibilities

- **R29 — Write the division of responsibility into the agreement.** Technology
  development and field operations are different disciplines. Where the boundary
  is informal, field problems arrive in research inboxes and wait. BHLK on data
  processing and standards; IPB on design, calibration methodology and training;
  PMI on installation, maintenance and response. Written down, it survives staff
  changes on any side.

---

## Notes for you

- **28 items is too many for the report body.** Suggest: groups plus the two or
  three strongest in each, full list as an appendix table.
- **R10, R12 and R25 tell one story** — the SD card filled, processing failed,
  shutdown never fired, the battery flattened. It may be stronger as a single
  worked example than as three separate items.
- **R8, R11 and R27 overlap.** All three move the station away from a solar,
  duty-cycled box at the riverbank.
- **Not included, tell me if they should be:** a cheaper stage sensor to replace
  USD 1,000 pressure transducers; a standalone solar rain gauge; the enclosure
  and humidity work. All are in `LESSONS_LEARNED.md` but read as our own future
  work rather than advice to IPB and BHLK.
- **R2's cost is the only real price in the list.** Everything else is effort and
  is unestimated.
