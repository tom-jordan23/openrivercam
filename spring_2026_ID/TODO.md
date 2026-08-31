# TODO — Indonesia Spring 2026 Deployment (post-trip)

**Last updated:** 2026-08-31

The pre-trip task list (departure schedule day-by-day, in-country
deferred items, etc.) was archived to `archive/` after the April 2026
trip. This file tracks what's actually open *now*, post-trip.

| Priority | Meaning |
|----------|---------|
| P0 | Active workstream — blocks station producing useful data |
| P1 | Important — should resolve before scaling or before the next trip |
| P2 | Nice to have — schedule when slack is available |

| Status | Meaning |
|--------|---------|
| OPEN | Not started |
| IN PROGRESS | Work underway |
| PARKED | Waiting on external dependency (IPB engagement, vendor, etc.) |
| DONE | Complete |

---

## P0 — Active workstreams

### TODO-101: Configure deployed Sukabumi station with the salvage CameraConfig

| Field | Value |
|-------|-------|
| **Status** | IN PROGRESS |
| **Site** | Sukabumi |

The auto-fit salvage pipeline produced a passing CameraConfig
(`spring_2026_ID/survey_data/sukabumi_handoff/sukabumi_autofit_camera_calibration.json`,
4.61 cm RMSE on the 6-GCP subset GCP7/8/10/13/14/3.2) and an end-to-end
ORC-OS run on the calibration video already produced
`q_50 = 0.51 m³/s`, `v_av = 0.49 m/s`, `fraction_velocimetry = 65.7 %`.
Remaining work is loading the same configuration onto the deployed
station (not just the local Docker harness) and verifying it processes
real captured video.

**Prerequisite — `h_ref` durability:**
Set `h_ref = 617.065` through the dashboard form for camera_config
"Sukabumi_A" (not via SQL — see ISS-FIELD-003). Verify by
`sqlite3 ~/.ORC-OS/orc-os.db "select json_extract(data,'$.gcps.h_ref') from camera_config where name='Sukabumi_A'"`.
Then exercise a dashboard save and re-check — the value must survive.

**Steps:**
- [ ] Import `sukabumi_autofit_camera_calibration.json` onto the
      deployed Sukabumi station (one-shot API import per
      `survey_data/sukabumi_handoff/README.md` § "One-shot API import",
      OR paste the 6-GCP subset and click GCPs in the dashboard).
- [ ] Set `h_ref = 617.065` through the dashboard form. Verify
      durability by saving once and re-querying the DB.
- [ ] Upload `cross_section.geojson` from the handoff folder via
      `POST /cross_section/from_geojson/` (CSV upload has no CRS
      parameter, ends up CRS-less).
- [ ] Wire `video_config.id=1` to the new camera_config and
      cross_section. Set `cross_section_wl_id` for optical fallback.
- [ ] Trigger Process on a real recent capture (not just the
      calibration video). Expected: end-to-end completes, produces
      `transect_*.nc`, `plot_quiver.jpg`, populates `time_series`.
- [ ] Inspect `plot_quiver.jpg` for flow direction. The 2026-04-22
      run on the calibration video showed vectors that *appeared* to
      oppose the true downstream direction — diagnosis was parked
      after a cross-section reversal turned out to be the wrong fix
      (see `survey_data/corrections.md` 2026-04-22 entries). This
      needs an unbiased look on a real capture, not the calibration
      video.

### TODO-102: Stand up Grafana on the AWS LiveORC server for sensor data

| Field | Value |
|-------|-------|
| **Status** | OPEN |
| **Site** | LiveORC server (AWS) |

The Sukabumi station uploads sensor CSVs (RG-15 rainfall, SHT40
temperature/humidity, DS18B20 temp probe) to the LiveORC server via
`orc-sensors-upload` on every boot / hourly. There's no visualization
of that data yet — it accumulates in CSV form on the server.

**Goal:** A Grafana instance on the LiveORC AWS host with dashboards
for each station's sensor stream, viewable via a public-but-auth'd URL
that PMI, IPB, and other stakeholders can reach.

**Steps:**
- [ ] Decide on data source backend: read CSVs directly, or import to
      InfluxDB / Postgres with a TimescaleDB extension first. CSV-direct
      via the Grafana CSV plugin is simplest for the current scale; a
      TSDB pays off once we have multi-station + multi-month data.
- [ ] Provision Grafana on the LiveORC host (Docker Compose alongside
      the existing LiveORC stack, or systemd direct install).
- [ ] Configure auth — at minimum a non-default admin password; ideally
      reverse-proxied behind the same auth as LiveORC's web UI.
- [ ] Build dashboards: rainfall (RG-15 cumulative + interval),
      enclosure temperature/humidity (SHT40), water/air temp (DS18B20),
      uptime / capture cadence (derived from upload timestamps).
- [ ] Document the URL, credentials handoff, and refresh cadence in
      `reference_liveorc_server.md` (in user memory) and a public-facing
      doc.

### TODO-103: Verify LiveORC video and sensor uploads from Sukabumi

| Field | Value |
|-------|-------|
| **Status** | RESOLVED 2026-07-07 (alerting follow-up remains — see below) |
| **Site** | Sukabumi → LiveORC server |

End-to-end verification done. Videos/hydrology were uploading fine.
**Sensor CSV uploads were silently failing** — and had been for weeks:
`orc-sensors-upload` fires ~5 s after boot, before the LTE modem
registers, so its PUTs failed (`curl 6/7`); the old fail-fast +
all-or-nothing watermark then never advanced, and alphabetical upload
order starved sht40. The server had stalled at sht40≤05-15, rg15≤06-15,
ds18b20≤07-03 while the sensors kept logging locally.

**Resolution:** fixed in commit 966d327 (curl `--retry` +
oldest-mtime-first + per-file resumable watermark), deployed to the
station 2026-07-07. Backlog recovered with `pi/tools/orc_flush_one.sh`;
all three sensors now current on the server. Permanently lost: sht40
2026-05-16 → 06-07 (the 30-day CSV rotation deleted it before recovery —
see `pi/tools/README.md`).

**Steps:**
- [x] Confirm recent Sukabumi video uploads on LiveORC (videos were flowing).
- [x] Inspect sensor CSV ingest — root-caused the stall, fixed, rows now
      landing for the current date.
- [x] Verify Pi side: `orc-sensors-upload` now rides the boot-race and
      advances its watermark (it's invoked from orc-capture each wake
      cycle, not a boot+hourly timer).
- [ ] **Alerting (still open):** add a low-rate detector so the next
      upload gap is caught in hours, not weeks — e.g. a Grafana "no
      sensor rows in N hours" alert on the TimescaleDB, or a daily
      server-side scrape. This gap went undetected precisely because
      nothing watched for staleness.

### TODO-104: Coordinate IPB engagement (site + survey)

| Field | Value |
|-------|-------|
| **Status** | OPEN |
| **Sites** | Both |

Three parallel asks for IPB:

**Sukabumi — total station re-survey.** Use
`survey/outsourced_survey_brief.md` as the SOW template, scoped to
total station (not RTK). Section 2 deliverables stand; section 5
checklist needs the RTK-specific items replaced with total-station
equivalents (instrument model + serial, control point coordinates and
how they were established, traverse closure error, vertical
adjustment method).

**Jakarta — site selection.** Need IPB's hydrological judgment on
candidate sites that are (a) in PMI's flood-warning catchments of
interest, (b) have a clear permission/installation path, and
(c) are not subject to the same urban RF / sky-view problems that
appear to have hurt RTK at the Sukabumi canal site.

**Data access — LiveORC logins for IPB.** Ready to provision on
request: additional login links, account setup, and a walkthrough of
where the data lives. **Gated on PMI, not on us.** Dan was explicit on
the 2026-08-11 call that who gets access, and when, is PMI's decision —
do not provision ahead of that approval. Dan separately confirmed this
does *not* need to wait on the water-level adjustment, so the gate is
purely PMI's, not a technical readiness one.

**Steps:**
- [ ] Identify the right IPB contact(s) and make introductions
      through PMI.
- [ ] Send the survey SOW for Sukabumi.
- [ ] Send a separate brief for Jakarta site selection.
- [ ] Track responses; do not block other workstreams on them.
- [ ] **Data access — wait on PMI's approval.** Do not provision
      ahead of it. The *technical* side is TODO-115: read-only API
      access is achievable natively (institute membership, no LiveORC
      changes), and that account model can be built and proven while
      this gate is still closed.
- [ ] Once approved: create the LiveORC accounts, send login links,
      and confirm IPB can reach the data surfaces they actually need —
      the LiveORC web UI, Grafana (TODO-102), and the Sheet (TODO-111).

---

## P1 — Important, but not blocking the active workstreams

### TODO-105: Document `h_ref` durability problem upstream

| Field | Value |
|-------|-------|
| **Status** | OPEN |
| **Site** | Both (ORC-OS general issue) |

ISS-FIELD-003: ORC-OS dashboard "save" overwrites SQL-edited
camera_config fields. File a clear repro upstream so the
ORC-OS team can scope a fix (partial PATCH vs full-blob clobber on
save). Until then, the workaround is "always go through the dashboard
form."

### TODO-106: Re-evaluate camera-only / split-architecture deployment

| Field | Value |
|-------|-------|
| **Status** | OPEN |
| **Site** | Future deployments |

Per LESSONS_LEARNED #4, a camera-only field node with remote compute
would have made the Jakarta permission situation much easier (the
permission ask is "mount an IP camera" not "build a full enclosure").
The `docs/SPLIT_ARCHITECTURE_DESIGN.md` doc was written pre-trip but
not field-tested. Pick this up before the next site selection round.

### TODO-107: Sukabumi station — outstanding small issues

| Field | Value |
|-------|-------|
| **Status** | OPEN |
| **Site** | Sukabumi |

Carried over from pre-trip TODO. Now that the station is on-site and
remote-accessible:

- [ ] **TODO-019** (was P2): `getty@tty1` cycling auto-login for
      non-existent `hcwinsemius` user. Fix the autologin override.
- [ ] **TODO-020**: Document unprovisioned-SIM diagnostic state in
      `docs/TROUBLESHOOTING.md` (full symptom signature is in this
      file's prior version, archived in git history).
- [ ] **TODO-021**: Tailscale persistent-login `deploy.sh` integration
      — auth key is staged at `/home/pi/.tailscale_nodekey` on
      Sukabumi but `deploy.sh` doesn't yet wire it up.
- [ ] **TODO-022**: Verify RG-15 rain gauge response and polling-mode
      configuration (gauge went silent on UART 2026-04-17). Field
      check on next site visit.
- [ ] **TODO-012** (rev): Verify DDR-60G quiescent power draw against
      the 0.5 W estimate. Update power budget if the measured value
      diverges.
- [ ] **TODO-012b**: Re-export `circuit_diagram.pdf` from the updated
      drawio source.

### TODO-108: Jakarta station — bench soak rather than warehouse

| Field | Value |
|-------|-------|
| **Status** | OPEN |
| **Site** | Jakarta (currently in US) |

The built Jakarta station is back in the US. While IPB site selection
is in flight, run it on a bench as an extended soak rig:

- [ ] Power on, run on continuous capture against any RTSP source
      (a webcam pointed at a window is fine for soak).
- [ ] Verify all sensors (RG-15, DS18B20, SHT40), capture daemon,
      sensor logger, upload, LED status all run reliably for weeks.
- [ ] Track any failures that emerge on long soak — these are the
      thermal/humidity issues that would otherwise show up first in
      the field.

### TODO-113: Reprocess retained video under changed settings — and announce it

| Field | Value |
|-------|-------|
| **Status** | OPEN |
| **Site** | Sukabumi → LiveORC server |

Committed on the 2026-08-11 call: old video is retained, so a settings
change can be applied retroactively rather than only affecting future
captures. Two obligations follow.

**The experiment.** Swapping the cross sections was named specifically
— reprocess existing video with them swapped and see what it does to
the data. **Reconcile with TODO-101 first:** a cross-section reversal
was already tried on 2026-04-22 and turned out to be the wrong fix for
the apparent flow-direction problem (`survey_data/corrections.md`,
2026-04-22 entries). Either what was described on the call is a
different change than the one already tried, or that earlier finding
needs revisiting. Establish which before spending a reprocess run.

**The communication protocol.** Reprocessing changes numbers
stakeholders may already have seen, so each run gets announced to
PMI/IPB as it happens: what setting changed, which date range was
reprocessed, and that the prior figures are superseded. Silent
retroactive edits to a shared dataset are the failure mode.

**Blocked on TODO-112 in practice.** `prod_reprocess.sh` execs inside
`liveorc_webapp` to read local media, and that media currently exists
only in the container's ephemeral writable layer. Until the EBS
migration lands, any reprocess work on the server carries the same
risk the runbook already warns about — never `compose up` or
`--force-recreate` on that host.

**Steps:**
- [ ] Settle the cross-section question against the 2026-04-22
      correction before running anything.
- [ ] Confirm what video is retained and over what date range, on the
      station and on the server — this bounds the reprocess window.
- [ ] Sequence against TODO-112, or accept and document the writable-
      layer risk explicitly if a run can't wait.
- [ ] Run the reprocess per
      `liveorc_server/reprocess/REPROCESS_RUNBOOK.md`; compare outputs
      against the currently published figures.
- [ ] Announce the run and its effect on published data to PMI/IPB.

---

### TODO-118: Recommendation report for IPB and BHLK on replicating the station design

| Field | Value |
|-------|-------|
| **Status** | IN PROGRESS — D1-D4 resolved, full draft written, awaiting review |
| **Opened** | 2026-08-31 |
| **Trigger** | PMI / IPB / BHLK meeting at Sukabumi, 2026-08-21 |

**What BHLK asked for.** At the 21 August meeting BHLK offered to duplicate
**one to three ORC devices** as a pilot, subject to permission from Tom, Hessel
and Dan to study the current design. BHLK also offered server capacity for ORC
data storage, and recommended relocating the current site to a flat area free of
obstruction from buildings. BHLK has separately been asked by BNPB's early
warning division to assess drought and link it to preventive measures, and sees
ORC as a validation tool for a modelling framework to be developed later. The
agreed split is BHLK and IPB on data processing, PMI as the user of the derived
information.

**Deliverable.** A recommendation report, **10 pages or fewer**, for a
scientific but non-specialist audience. Visuals and a slide deck follow as
separate deliverables — five candidate figures are already scoped in the outline.

**State.** D1-D4 were resolved 2026-08-31 and the full draft is written to
`spring_2026_ID/docs/REPLICATION_RECOMMENDATIONS.md` (~5,500 words against the
10-page budget, F1-F5 marked as placeholders). The outline at
`REPLICATION_RECOMMENDATIONS_OUTLINE.md` records the resolutions and the
superseded figures. Both are registered in `docs/build_pdf.sh` (ALL_DOCS and
DOC_AUDIENCE = "IPB and BHLK"), so the English and Bahasa Indonesia PDFs build
without extra setup. **Built 2026-08-31: 18 pages for the report, 15 for the
appendix.** Neither pandoc nor xelatex was installed, so `build_pdf.sh` gained a
second engine — pandoc to HTML then WeasyPrint, styled by `docs/pdf_print.css` —
and a `docs/.venv-pdf` toolchain that installs without root. The LaTeX path is
still preferred and still selected automatically wherever xelatex is present.

**Two findings drive the recommendations and are worth knowing independently of
the report.**

1. **The survey method failed reproducibly and nothing caught it on site.** Two
   RTK surveys on consecutive days, same equipment and crew, reproduced
   check-point spreads of ~99 cm H / ~139 cm V — roughly 30× the applicable
   tolerance. The surveyed geometry is an input the processing chain cannot
   recover, so this bounds everything downstream of it. *This finding was
   originally written as the drought/low-flow accuracy argument; under the D5
   scope rule it now rests on the reproducibility failure alone, which is the
   part that is ours to state.*
2. **Optical water-level detection fails through daylight at Sukabumi** and each
   failure loses the whole discharge measurement, not just the level
   (`findings/optical_wl_daytime_glint.md`). Any duplicated unit should carry an
   independent water-level reference — a sensor, or a staff gauge in the camera
   view referenced to the *papan duga air* zero. This is R1 in the outline and
   the highest-value single change to the design.

**D1–D4 resolved 2026-08-31:**

- [x] **D1** — §6 **stays, reframed as acceptance conditions.** It now leads with
      the conditions for the output to be additive to the BBWS record, and
      presents the correctable / not-correctable distinction as a precondition
      for meeting them rather than as a rebuttal of the meeting position.
- [x] **D2** — permission and licensing **reduced to one sentence** in §1.
- [x] **D3** — **PMI NHQ is not an audience.** The conditional §2 and §9
      paragraphs are dropped; §9 states PMI's role as the meeting recorded it and
      says explicitly that it has not been agreed with PMI NHQ.
- [x] **D4** — **§10 kept as drafted**, all five items stated as open.

**Scope added 2026-08-31 (Tom), after the first full draft.** Four additions, all
written:

1. **§3.2 The cost ceiling and how it was applied.** ~USD 3,000 for two stations
   = a USD 1,500/station ceiling. The ceiling was applied *component by
   component* — cheapest part meeting the functional requirement — which prices
   each part against its datasheet and not against what its limits cost the rest
   of the system.
2. **§3.3 What the camera choice cost.** ANNKE C1200 at ~USD 60/camera against a
   professional 12MP Hikvision at ~USD 1,268 (20x, more than four-fifths of the
   station budget on its own). Three firmware-imposed costs: ANNKE strips
   `ContentMgmt/download` so Profile C (SD record, HTTP fetch at full CBR) died
   and capture fell back to RTSP at ~15.5 Mbps against pyorc's recommended 20;
   the white-LED boot flash is pre-OS and unsuppressable (ISS-004), and 24/7
   camera power was rejected at 425 Wh/day vs 118; 30-60 s boot paid every wake.
3. **§3.4 Firmware replacement risks.** **Note the terminology gap:** Tom asked
   about *open source* firmware; what the repo actually researched
   (`research/annke_hikvision_crossflash_research.md`) is cross-flashing
   *genuine Hikvision* firmware — proprietary, different vendor. §3.4 says so
   explicitly and notes no open-source stack was evaluated against this
   hardware. Risks documented: bricking with TFTP/UART recovery inside an IP67
   housing, hardware-revision-specific community recipe, no support path, void
   warranty, spares no longer interchangeable (conflicts with the 5-minute
   replaceability constraint), and it does not fix the boot flash.
4. **R9, R10, R11.** R9 — budget per station and screen the control interface
   before buying. R10 — Pi 5 native RTC instead of the Witty Pi where the site
   allows; this was the *original* design, reinstated only because the ML-2020
   connector failed on both boards, and it changes the §4.1 latch failure mode.
   Keep the Witty Pi on solar (low-voltage cutoff, 6-30 V input, true power cut).
   R11 — where real-time monitoring is required, build always-on and AC-powered.

**R11 is the one that ties the report together.** The 30-minute duty cycle misses
§6's 15-minute *minimum* time step and cannot reach the 5-minute preferred
flood-warning cadence, because every wake costs a 30-60 s camera boot. It is also
the origin of the §4.1 latch and of R5's too-short diagnostic window. And the
grid configuration is *cheaper* (~USD 1,030 vs 1,340). Wired into §2, §5 preamble
and §6.

**Restructured 2026-08-31 (Tom): exec summary -> report proper -> appendix**, to
match Indonesian professional report convention. Now two documents:

- `REPLICATION_RECOMMENDATIONS.md` — ~1 p executive summary, then §1-§12.
- `REPLICATION_RECOMMENDATIONS_APPENDIX.md` — A1 camera firmware detail,
  A2 firmware replacement, A3 survey SOW, A4 availability record, A5 optical WL
  dataset, A6 data delivery, A7 power/scheduling/always-on comparison, A8 source
  index. ~7.6 p.

Both registered in `build_pdf.sh`. Register adjustments for the audience: full
institution names on first use, offers acknowledged before findings,
recommendations framed as offered for consideration, PMI NHQ named in full.

**PAGE BUDGET: 10 p is no longer reachable.** Report body is **~12.7 p text plus
~0.7 p of figures, about 13.5 p**, after moving §3.3/§3.4 detail, the R2 contract
terms, the R10 comparison and figures F2/F5 to the appendix. The added scope —
cost ceiling, camera firmware, firmware replacement, R9/R10/R11, and the
executive summary — is roughly double the original brief; three compression
passes are now returning ~1% each. Further reduction means deleting content, not
relocating it. **Decide: accept ~13 p, or name what to cut.** Candidate cuts if
10 p is firm: §6 conditions list to the appendix (-0.5 p, but D1 kept §6 in the
body), §11 summary table (-0.8 p, duplicates §5), §2 folded into the executive
summary (-0.7 p).

**Next steps:**
- [x] Tom reviews and comments on the outline.
- [x] Write the full draft against the agreed outline and page budget.
- [ ] **Accept ~13 p or name what to cut** (see candidates above). Blocks the
      figure work, since F1-F5 have to fit whatever is decided.
- [ ] Confirm the BHLK expansion — the repo cites PUSAIR's *Balai Hidrologi dan
      Tata Air*, the meeting notes give *Balai Hidrologi dan Lingkungan
      Keairan*. Get the name right before this goes out.
- [x] Build the PDFs and check the real page count against the 10-page budget.
      **18 p report, 15 p appendix** — the report is 8 pages over the budget, so
      the cut decision above is still open and is now measured rather than
      estimated.
- [x] Produce the figures. **Four in the report, one in the appendix**, generated
      by `docs/figures/build_figures.py` (SVG for the PDF, header-cropped PNG for
      the deck). The two data figures are computed from the record, not drawn.
      The old F2 went with the drought argument under D5.
- [x] Add photographs. Five, all from the build — **there are no field
      photographs of the deployed station in the repo**, worth fixing on the next
      visit. `build_photos/PHOTO_METADATA.md` is not reliable: IMG_1345 is
      described as the camera on a pole and is actually a basement water filter.
      Open every image before using it.
- [x] Derive the slide deck; §2, §4, §5 and §9 are the sections that carry over.
      `docs/build_deck.py`, **31 slides on the American Red Cross Classic
      template** (`/home/tjordan/code/templates/AmCross/English PowerPoint
      Templates/`), which is now the script's default. Content is held in the
      script; `--no-template` builds on a neutral base. The Classic template is
      16:9 at 10 × 5.62 in with a 3.35 in body, roughly half the content height
      of the neutral template, so the deck was re-cut to fit rather than only
      re-skinned — the dense slides were split. Six visual slides were added on top
      of that. Verified: no slide overflows the footer band, and every picture
      carries alt text.

**Rewritten for leadership (Tom, 2026-08-31). Two criticisms: still fixated on
the outages, and simultaneously too technical and too vague.** The audience is
humanitarian and academic leadership, so the report and deck were rebuilt against
`STYLE_Humanitarian_Executive.md` and `STYLE_Academic_University_Business.md` from
`github.com/tom-jordan23/writing`.

- **Outages.** §4 collapsed from four subsections to three findings in a page,
  and the availability figure moved to appendix A4 as Figure A2. The interruption
  count survives as one sentence; the duration table, the maintenance-mode
  statistics and the timeline live in the appendix.
- **Too technical.** ISAPI, RTSP, bitrate, tmpfs, signal-to-noise and the RTC
  connector are all appendix material now. The body carries the consequence and
  the number. Chart labels changed with it: "signal-to-noise ratio" became
  "confidence in the detected water line", "quality gate" became "acceptance
  threshold".
- **Too vague.** The report now opens on what a low-cost station makes possible —
  network density against the Rp 58,000,000 e-catalogue alternative — and names
  what each change buys, in a table with costs.
- **Register.** Mission framing first, local capacity and repair over dependency,
  resource realism, consultative rather than directive, and a *Questions for
  consideration* section instead of a bare open-questions list.

Report is **12 pages, ~2,750 words of prose** (was 21 pages, ~5,500). Deck is
**19 slides** (was 31). Figures renumbered: 1 system, 2 water level, 3
arrangements; A1 capture path, A2 availability.

**Jakarta station: it is at Wisma PMI, not back here (Tom, 2026-08-31).** Two
drafts said the Jakarta unit was "flown to Indonesia and flown back without
producing data". That was invented — nothing in the repo says it returned.
`SITES.md` says only that Jakarta was not deployed and that permission for the
intended site fell through during the trip. The unit is complete and held at
**Wisma PMI in Jakarta, waiting for a site.** Corrected in the report and the
deck. The siting lesson is unchanged and slightly stronger: a finished station has
been sitting unused since April because permission was assumed.

**Sukabumi runs the IPB total-station survey. Not a salvage. (Tom, 2026-08-31.)**
Three drafts of the report, and `README.md`, said the station runs on "a
calibration salvaged from a failed survey". Wrong. The deployed camera config is
**`Fit 6`, applied 2026-06-11, built from IPB data alone** — GCPs from the IPB
spreadsheet, cross-sections from the IPB transects, calibration frame from the May
survey video — fitting at **0.037 m RMSE** against a 5 cm target, `z_0 = h_ref =
615.0 m`. Source: `survey_data/ipb_survey_1/handoff_station/README.md`, which
states "IPB data only, zero April salvage". The April RTK auto-fit (4.61 cm on a
6-GCP subset, `z_0 = 617.065`) is obsolete and **must not be mixed in** — the IPB
low-water surface is ~2 m lower. Corrected in the report, appendix A3.1, the deck
and `README.md`. R2 now credits IPB for the fix, which is right on the facts and
right for the audience.

**Cause: I carried an inherited sentence forward across three rewrites without
re-checking it**, and `survey_data/ipb_survey_1/` was sitting in the repo the
whole time. Same failure as the invented "flown home" claim and the
signal-to-noise claim the figure falsified. **Verify every factual claim against
the repo before it ships, including the ones that were already there.**

**Stop benchmarking a volunteer pilot as a production instrument (Tom,
2026-08-31).** The framing note above was already on record and I violated it: the
body led with "51% never arrived" and scored the station on availability. That is
an unfair benchmark for what this was and disingenuous to the volunteers who kept
it running. The body now describes **three design gaps in words** — the station
cannot report its own condition, nothing reconciles sent against received, and
daylight defeats the optical water level — with the measurements moved to appendix
A4, which opens by stating they are failure modes of this design and explicitly
not a performance benchmark. Do not restore availability statistics to the body.

**Also corrected: the "mains is cheaper, USD 1,030 vs 1,340" claim is withdrawn.**
It was unsourced. `BOM_Sukabumi.md` totals **$1,340.19 for electronics and
enclosure only** — Sukabumi already had its 200 W panel and 50 Ah battery, so no
array is in that figure. `BOM_Jakarta.md` shows ~$1,333 project total / $1,076.88
ordered. The defensible statement, now in both documents: a new solar site must
add an array and a mains site need not.

**`docs/RECOMMENDATIONS.md` is the source for the recommendations (Tom,
2026-08-31).** The eleven were written into the report and the deck first and
edited in place, which made them awkward to adjust. They now live as a plain
bulleted list that Tom edits directly; the report and the deck are regenerated
from it. **Do not make content changes to the recommendations in
`REPLICATION_RECOMMENDATIONS.md` or `build_deck.py` — change the list and
propagate.** If the numbering changes, carry it through both documents and the
appendix cross-references (A3 supports R2, A4 supports R4/R5/R7, A5 supports R1,
A7.2 supports R10, A7.3 supports R11).

**The message is handover, not replication (Tom, 2026-08-31).** The report was
framed as "here is our design and what to change before you copy it". It is now:
the pilot was a good experience, it taught us all something and it brought PMI,
IPB and BHLK together — **and the path forward is for IPB and BHLK to start on
their own approach.** Retitled *OpenRiverCam in Indonesia: What the Pilot Taught
Us, and the Path Forward*. The eleven recommendations are now "eleven things we
would do differently", offered as input to their design rather than corrections to
ours, and explicitly not expected to be adopted as a set. New closing section,
*What we can offer from here*: the record, the documentation in both languages,
the software, the Wisma PMI unit to take apart, continued reporting from Sukabumi
— and not building their stations for them. Keep this framing; do not revert to
replication language.

**Jakarta station: a study and test unit, not an operational station (Tom,
2026-08-31).** It should go to whichever of IPB or BHLK will use it as a **lab /
study device** — open it, trace it, power it up, take it apart while they build
their own. **Installing it locally as a test unit is fine**, including against
real water; what we do not want is it put into service as an operational station
with expectations of availability and data consistency. It was built to the design
this report recommends changing, so it carries the known problems: acceptable in
something you are learning from, a poor foundation for a record anyone depends on.
It also answers the request recorded at the meeting, access to the design in order
to study it, with hardware instead of only documents.

Status: complete and software-ready, held at **Wisma PMI in Jakarta**, **not
powered on since the April visit**. Transfer to IPB was the plan; whether IPB or
BHLK holds it is now put to them as a question rather than answered. An earlier
draft of this report pitched it as a fast first pilot unit — that framing is
withdrawn and should not come back.

**Privacy and protection are not ours to write (Tom, 2026-08-31).** An earlier
draft flagged a missing Do No Harm section and recorded it as a gap for us to
close. That was wrong, and the note is withdrawn. The Indonesian government is the
authority on the legal requirements for protecting Indonesian citizens' privacy;
BHLK sits inside that government. Writing them guidance on it would be a lecture,
and it is the same overreach D5 rules out for hydrology — their domain, their
call. Removed from the report and deck: the line telling them site permission
should be "a conversation with the people who live there". What remains is our own
side of it — the camera's light fires 48 times a day at the present site, which
bears on siting and cycle length, and we will not build to a site again before
being told the permission is in place. Do not reintroduce a protection section.

**Correction forced by the figures (2026-08-31).** Plotting the optical
signal-to-noise data falsified a claim that was in both the report and the
appendix: "passing captures cluster at 3–5, failing ones at 1.3–1.8, with almost
nothing between." **36 of the 100 passes fall between 2.0 and 3.0**, so there is
no empty middle, and the absence of overlap at the gate is definitional rather
than a result. Both documents now state what the data supports: failures are not
marginal (median 1.63, only 23 of 100 reach 1.8), and a substantial share of
accepted levels sit close to the threshold — which argues for R1 rather than for
adjusting the gate. The general lesson is to draw the data before writing the
sentence about it.

**Scope note (Tom, 2026-08-31). No hydrology conclusions — technology only.**
How the output is applied is for IPB and their federal partners. Removed from the
report: the low-flow/drought area-error argument, the model-validation argument,
the rating-curve positioning, and our comparison of the 30-minute cycle against
the 15-minute minimum. §2 and §6 were kept and restated as requirements the
technology has to meet. This applies to F1–F5 and the deck as well — F2, the
low-flow area-error schematic, is withdrawn. Recorded as D5 in the outline.

**Register note.** Tom stopped the first outline draft over its writing style —
no aphorisms, no punchy closing clauses, no editorial asides. Plain professional
register throughout; the numbers carry the argument. This applies to the report,
the figures' captions and the deck.

**Framing note (Tom, 2026-08-31). Do not dwell on downtime totals.** Sukabumi is
a volunteer-supported installation and criticising response times is not fair
comment. The §4 field record is therefore framed entirely as properties of the
*design*: a fault the system never reported, a mode with no expiry or alarm, two
data paths nothing reconciles. §4.1 leads on the **duration distribution** — 9
interruptions under 24 h, none between 2 and 5 days, 3 at 5 days and over — as
evidence of the re-arm latch, rather than on an availability percentage. §1
carries the framing: the station is volunteer-supported and rarely visited, so
tolerating long unattended periods is a design requirement, not an operational
expectation. This makes the case for R4/R5/R7 stronger, not weaker.

**Corrected figure.** The outline's "22.7 days of 118 days observed, in 13
outages" was wrong — it paired ISS-FIELD-008's May-onward duration and window
(117.9 d, 8 outages) with ISS-FIELD-010's April-onward outage count. Regenerated
over one window with `station_gaps.py --since 2026-04-01`: **13 interruptions
over 133.5 days, 2026-04-16 to 2026-08-28.**

---

## P2 — Schedule when slack allows

### TODO-109: Indonesia trip retrospective writeup

| Field | Value |
|-------|-------|
| **Status** | OPEN |

`LESSONS_LEARNED.md` has the structured outcomes; a more narrative
trip retrospective (timeline, what worked, what didn't, photos) would
be useful for funder reporting and as input for the next trip plan.

### TODO-110: Spares inventory reconciliation

| Field | Value |
|-------|-------|
| **Status** | OPEN |

`BOM_Spares.md` was the pre-trip plan. After the trip, the actual
spares left at the PMI office (and what came back to the US with the
Jakarta kit) need reconciling. Do this before the next trip plan.

### TODO-111: Google Sheets export of sensor data

| Field | Value |
|-------|-------|
| **Status** | IN PROGRESS |
| **Site** | LiveORC server (AWS) |

Grafana (TODO-102) covers people who will log into Grafana. Stakeholders
who won't — PMI, IPB — need the sensor data somewhere they can filter
and chart it themselves, without a login or a self-signed-cert warning.
A Google Sheet is that surface.

The `sheets-export` service is written, wired into the compose stack, and
verified locally against a seeded TimescaleDB. What remains is the
Google-side setup and the deploy, both of which need a human in a browser.

**Design note — why there is no `ts` watermark:** sensor CSVs backfill
(that is exactly what the TODO-103 recovery did), so a `max(ts)` cursor
would silently skip replayed rows. Instead a `sensor_exports` ledger
table is anti-joined against `sensor_readings`. Verified locally: after
a backfill the naive query finds 0 rows while the anti-join finds all
1,440. `sensor_readings` is never altered. **Never prune
`sensor_exports` — it is the cursor.**

**Steps:**
- [x] Write the exporter, matching `sensor-ingest` conventions.
- [x] Validate the cursor against a local TimescaleDB, including the
      backfill case and a fault-injected crash in the append/mark window
      (0 rows lost; the batch re-appends, by design).
- [x] Document setup, deploy, dedupe, and rollover in
      `liveorc_server/README.md`.
- [x] Create the spreadsheet (must be a human — a service account has no
      Drive storage quota). Done; the ID is server-side only, never
      committed, because this repo is public.
- [x] Create the GCP service account, enable the Sheets API, download the
      JSON key, share the sheet with its `client_email` as Editor.
- [x] Fix the `preview` gate (2026-08-10). `build_sheets_client()` returned
      `None` for every mode but `live`, and `check_sheet_access()` no-ops on a
      `None` client — so `preview`, the mode this deploy starts in precisely to
      prove auth and sharing, never loaded the key and never called the API. A
      bad share, a missed `chown 1001:1001`, or a non-UTC sheet would all have
      stayed silent until `live`, whose first act is the ~130k-row append. Now
      only `dry-run` gets a `None` client. Verified locally: preview reaches the
      access check and still appends nothing (`sensor_exports` flat across
      cycles, no `sheets append ok` lines).
- [ ] **Re-confirm the JSON key exists and locate it** — as of 2026-08-10 its
      whereabouts are unconfirmed, so treat the download as unverified. If it
      cannot be found, generate a new key and delete the old one in the console
      rather than hunting for it.
- [ ] Verify the sheet itself: tab named exactly `readings`, `A1:E1` =
      `ts,station,sensor,metric,value`, File → Settings → Time zone = UTC.
      `check_sheet_access()` warns on a non-UTC timezone at startup but
      does not fix it, and nothing creates the header row.
- [ ] Add the `G1` disclaimer cell mirroring the mandatory Grafana banner.
- [ ] Get the JSON key onto the host — **open question: where does it live
      now?** It must never transit chat. Target
      `/opt/orc-additions/secrets/sheets-sa.json`, `chown 1001:1001`,
      `chmod 0400` (the container drops to uid 1001 per its Dockerfile).
- [ ] Deploy via Session Manager (no SSH on that host): `git pull`,
      rsync into `/opt/orc-additions` (**no `--delete`**, and **exclude
      `.env`, `certs/`, `secrets/`**), run once with
      `EXPORT_MODE=preview`, then switch to `live`.
- [ ] Confirm the ~130k-row first backfill completes without rate-limit
      errors, and that the four pre-existing containers were not
      recreated.

**Unblocked 2026-08-10.** The root volume was repaired (`/` at 62%, 30 G
free), so this proceeds ahead of TODO-112. It is also safely separable:
sheets-export is a service in the `/opt/orc-additions` stack and never
touches `/opt/LiveORC` or the `liveorc_webapp` container.

**Ordering constraint:** put `SHEETS_SPREADSHEET_ID` into
`/opt/orc-additions/.env` **before** the rsync lands the new
`docker-compose.yml`. `${SHEETS_SPREADSHEET_ID:?…}` is evaluated for the
whole file, so without it every `docker compose` command against that
stack fails — including ones targeting the four healthy ORC containers.

**Start in `preview`.** The compose default is `EXPORT_MODE=${EXPORT_MODE:-live}`,
so an unset variable goes straight to live. `preview` neither appends nor
advances the ledger. Never set `dry-run` here: it advances the cursor
without writing, silently skipping real data.

### TODO-115: Read-only LiveORC API access — the account model

| Field | Value |
|-------|-------|
| **Status** | **MODEL PROVEN 2026-08-25** (14 PASS / 0 FAIL) — partner provisioning still gated |
| **Site** | LiveORC server (AWS) |

**Verified against production 2026-08-25** with `verify-api-access.sh` and the
mirror account (`user_id 18`, institute **1**). Everything below that was read
from upstream source has now been observed on the running server:

- Reads resolve for an institute member; bare `GET /api/site/` really does
  return `[]` with a valid token, and `?institute=1` is mandatory.
- `PATCH` → **403**. `POST /api/video/` with an invalid payload → **400**,
  so the permission layer passes the request to validation without creating
  anything — the CREATE gap is confirmed by observation, not just by reading.
- `/api/recipe/` and `/api/device/` return `[]` as predicted.
- Access token lifetime is **360 minutes**; `/api/token/refresh/` works.
- Sites **2, 3 and 4 all belong to institute 1**, so one membership covers
  everything and the partner doc needs one id, not two.
- `creator` is **user 1** at site 4 and **user 3** at site 2 — two accounts,
  not one. Neither is the mirror account, which is what makes it read-only
  *by construction* rather than by policy.

**The DELETE probe is deliberately still unrun.** `PATCH` and `DELETE` share
one branch of `has_object_permission`, so the observed 403 on an empty-body
PATCH exercises the same predicate without being able to destroy a production
video. Now that the mirror exists it is safe to run:
`./verify-api-access.sh --institute 1 --site 4 --probe-delete --video-id <id>`.

IPB needs programmatic access to the data, and we need an account to pull
the backup mirror with (TODO-114). Both want the same thing: an account
that can **read everything and change nothing**. This TODO establishes
that account model, proves it against the running server, and writes down
what a partner needs to actually use it.

**The answer is yes, and it needs no change to LiveORC** — which matters,
because the standing rule is that nothing a version upgrade would
overwrite gets modified.

#### How LiveORC's permissions actually work

Read from the upstream source at tag **v0.3.0** (the deployed version;
`/api/version/` confirms 0.3.0 on Django 6.0.3 / Python 3.14.3). Upstream
has since tagged v0.3.1 — re-check this section on any upgrade.

`api/permissions.py` defines a single custom class, and
`api/views/base.py` applies it to every API viewset:

```python
class BaseModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrReadOnlyAsInstitute, IsAuthenticated]
```

`IsOwnerOrReadOnlyAsInstitute.has_object_permission`:

- **Safe methods** (`GET`/`HEAD`/`OPTIONS`) — allowed if
  `request.user.is_institute_member(obj.institute)` **or**
  `request.user == obj.creator`.
- **Everything else** (`PATCH`, `DELETE`) — allowed **only** if
  `obj.creator == request.user`.

So an account that is an institute member but did not create the records
gets read on the whole institute's data and **403 on every write**. That
is exactly the required behaviour, enforced upstream, for free.

`BaseModelViewSet.list()` adds a second gate: any nested `site_pk` route
returns **403** unless the caller is an institute member of that site (or
a superuser). So membership is what unlocks data, and non-membership is a
hard wall rather than an empty list.

#### The gap: CREATE is not covered

DRF invokes `has_object_permission` only from `get_object()` — i.e. on
**detail** routes. `IsOwnerOrReadOnlyAsInstitute` defines no
`has_permission`, so it defaults to `True`, and `POST` to a **collection**
is gated by `IsAuthenticated` alone. Any authenticated account can create:

| Route | Effect of a POST |
|---|---|
| `/api/video/` | **Uploads a video file and can enqueue a celery task** — `VideoViewSet.create()` calls `instance.create_task()` when the record is ready |
| `/api/site/` | Creates a site |
| `/api/site/{pk}/timeseries/` | Injects rows into the analytics series |
| `/api/site/{pk}/cameraconfig/`, `/crosssection/`, `/videoconfig/` | Creates calibration objects |
| `/api/recipe/`, `/api/device/` | Creates recipes / registers devices |

They still cannot **modify or delete** anything they did not create, so
existing data is safe. The exposure is additive: clutter, junk timeseries
rows, and — the sharp one — **disk writes plus celery load from
`POST /api/video/`**.

**Decision (2026-08-24): accept the gap, control it by timing.** Adding a
gateway to close it would mean another internet-facing service with its
own TLS and token rotation to own, for a partner-integrity risk rather
than a data-loss one. Instead, hand credentials to IPB only **after
TODO-112 lands**, so an accidental upload cannot threaten the root disk.
Revisit if the partner list grows beyond IPB.

#### Two traps

- **The `viewers` group does nothing.** `manage.py creategroups` builds
  `viewers`/`editors` groups carrying Django **model** permissions. These
  viewsets use `IsOwnerOrReadOnlyAsInstitute`, **not**
  `DjangoModelPermissions`, so group membership has **zero effect on the
  REST API**. It only affects `/admin/`, and only for `is_staff` users.
  Putting IPB in `viewers` looks like read-only access and grants nothing.
- **Never hand over the station credential.** The `creator` of every
  existing video is whichever account ORC-OS authenticated as at
  `/callback_url`. That account *can* delete them. IPB gets fresh users,
  always.

#### Onboarding gotchas to put in the partner doc

- `GET /api/site/` returns an **empty list** for a non-superuser unless
  `?institute=<id>` is supplied. A partner's first call looks like "there
  is no data". Give them the institute id up front.
- `/api/recipe/` and `/api/device/` return **empty / 404** for any
  non-superuser: both `get_queryset()` methods filter on `institute` and
  then fall through to `return queryset.none()`, so the filter branch is
  dead code upstream. Fail-safe, but it means recipe and device metadata
  are simply unavailable over the API. Camera configs and video configs
  are reachable per-site and carry the calibration that matters.
- Auth is JWT: `POST /api/token/` with email + password returns access +
  refresh; `POST /api/token/refresh/` renews. Confirm the access lifetime
  — a long pull will outlive one token.
- `/api/schema/` serves the full OpenAPI spec and needs no auth, so a
  partner can explore the surface before they have credentials.

**Steps:**

*Establish and prove the model — do this now*
- [ ] In `/admin/`, identify the institute that owns sites **2**, **3**
      and **4**, and record its id. Confirm sites 2/3/4 all belong to the
      same institute — if they do not, membership has to be granted per
      institute and the partner doc needs both ids.
- [ ] Find out which account is `creator` on the existing videos (the
      ORC-OS callback account) and confirm it is **not** shared with
      anyone. Note it in the password manager as station-only.
- [ ] Create the **mirror service account** for TODO-114: own user, not
      staff, not superuser, added as a `Member` of that institute.
      This is ours, not IPB's — it proves the model before any partner
      touches it.
- [ ] Run the verification matrix below against that account and record
      the actual results.

*Verification matrix — run against the mirror account, not an admin*

| Request | Expect | Proves |
|---|---|---|
| `POST /api/token/` | 200 + access/refresh | credential works |
| `GET /api/site/` | `[]` | the no-`?institute` gotcha is real |
| `GET /api/site/?institute=<id>` | the sites | membership resolves |
| `GET /api/site/4/video/` | 200, full list | `list()` institute gate passes |
| `GET /api/site/4/video/{id}/` | 200 | safe method + member |
| `GET /api/site/4/video/{id}/playback/` | video bytes | media is reachable |
| `PATCH /api/site/4/video/{id}/` | **403** | not creator |
| `DELETE /api/site/4/video/{id}/` | **403** | **the finding that matters** |
| `GET /api/site/4/timeseries/` | 200 | analytics readable |
| `DELETE /api/site/4/timeseries/{id}/` | **403** | not creator |
| `GET /api/recipe/` | `[]` | `queryset.none()` fall-through |
| `GET /api/site/{foreign}/video/` | 403 | non-member wall, if a foreign site exists |

- [ ] **Do not POST a real video to production to test the gap.** It is
      confirmed by source reading, and a test upload writes to the very
      disk this whole workstream is about. If you want it confirmed
      empirically, `POST /api/video/` with a deliberately **invalid**
      payload: a **400** proves the permission layer let you through
      without creating anything, a **403** would mean it did not.
- [ ] Record the matrix results in `liveorc_server/README.md` under a new
      "API access" section, alongside the permission explanation above.
      This is the durable artefact — the next person should not have to
      re-read upstream source to know what a partner account can do.

*Partner provisioning — gated, do not run early*
- [ ] Write the IPB-facing doc: base URL, token flow, the institute id,
      the endpoint list, the `?institute=` gotcha, and a worked `curl`
      example. Keep it in the repo; it contains no secrets.
- [ ] **Wait for both gates.** PMI approval (TODO-104 — Dan was explicit
      on the 2026-08-11 call that who gets access is PMI's decision) and
      TODO-112 complete (so `POST /api/video/` cannot threaten the root
      disk).
- [ ] Once both clear: create one user per IPB person — never a shared
      login — each `is_staff=False`, `is_superuser=False`, added as
      `Member` of the institute. Send credentials out of band.
- [ ] Re-run the verification matrix against **one real IPB account**
      before announcing access. Membership is the only thing standing
      between read-only and nothing, and it is set by hand.

---

### TODO-114: Pull an independent copy of LiveORC's data over the REST API

| Field | Value |
|-------|-------|
| **Status** | **DONE 2026-08-25** — complete media copy verified locally; TODO-112 gate released |
| **Sites** | LiveORC server (AWS) + workstation |

The 26 GB of media exists in exactly one place — `liveorc_webapp`'s
writable layer — and the only thing standing behind it is the root-volume
EBS snapshot from 2026-08-10. That snapshot is a real safety net, but a
*bad* one to have to use: recovering a single video from it means
launching an instance from the snapshot and digging through
`overlay2/<hash>/diff` to find files Django named. It is insurance you
cannot inspect, cannot test, and cannot restore from selectively.

> **Superseded approach.** The REST pull described below was replaced on
> 2026-08-25 after it took production down. Media is now exported host-side
> with `mirror/export-media-to-s3.sh`. See "What actually happened" further
> down before acting on anything in this section.

This TODO builds the copy you *can* inspect: pull site data down over
LiveORC's REST API to the workstation, where the files have names, the
inventory is a manifest you can diff, and nothing about the retrieval can
touch the container. Then TODO-112 runs against a known-good, verified
baseline instead of against nerve.

**It also does double duty.** IPB needs programmatic access to this data
anyway (TODO-104). Standing up API access properly — accounts, token
flow, what a non-admin account can and cannot do — is work that has to
happen regardless, and doing it first means the mirror *is* the test of
the access path IPB will later use.

**Why this is safe to run before TODO-112 — PARTLY WRONG, corrected
2026-08-25.** The claim below was that every step is an authenticated HTTP
GET, so it carries no risk to the writable layer. The *data* reasoning held:
reads never recreated a container, never invoked `docker compose`, never
touched `liveorc.service`, and nothing was lost. What it missed is that
"read-only" says nothing about **availability**. Bulk-reading media through
Django is expensive per byte, and running it against production took the host
down for ~90 minutes (ISS-FIELD-004). Safe for the writable layer is not the
same as safe for the service. Original reasoning follows:

> Every step is an authenticated HTTP GET against the running container.
> Reads do not recreate containers, do not invoke `docker compose`, and do
> not touch `liveorc.service` — the three things the runbook's warning block
> is about. This is the one substantial piece of TODO-112 preparation that
> carries no risk to the writable layer. See the hazard note on `/` below
> for the one thing that does need watching.

**What the API exposes** — verified 2026-08-24 by unauthenticated probe
against `https://openrivercam.endlessprojects.info`. Public HTTPS is up,
LE cert valid (expires 2026-11-08, see TODO-102 notes), version
**0.3.0** on Django 6.0.3 / Python 3.14.3.

| Endpoint | Gives you |
|---|---|
| `/api/schema/` | Full OpenAPI 3.0.3 spec, **readable without auth** |
| `/api/version/` | Version; the only anonymous data endpoint |
| `/api/token/`, `/api/token/refresh/` | JWT access + refresh pair from username/password |
| `/api/site/` | Site list — id, name, coordinates |
| `/api/site/{pk}/video/` | **The manifest.** Each `Video` carries `file`, `keyframe`, `image`, `thumbnail` as URIs, plus `timestamp`, `status`, `video_config`, `time_series` |
| `/api/site/{pk}/video/{id}/playback|image|thumbnail/` | The bytes |
| `/api/site/{pk}/timeseries/` | `h`, `q_05`/`q_25`/`q_50`/`q_75`/`q_95` per timestamp — the analytics output |
| `/api/site/{pk}/cameraconfig/`, `/crosssection/`, `/videoconfig/` | The calibration that makes the numbers reproducible |
| `/api/recipe/`, `/api/device/` | Processing recipes; registered devices |

`/api/site/`, `/api/site/4/video/` and `/api/site/4/timeseries/` all
return **401** unauthenticated — the API is not leaking, and the mirror
needs a real credential.

**Known site ids** (from the reprocess work, LiveORC 0.3.0): Sukabumi =
**4** ("Sukabumi City", 1165 videos), Jakarta = **3**, and site **2**
("Test site", 1255 videos) which is *probably* early Sukabumi captures.
Mirror all of them — the whole point is not having to decide later what
mattered.

**`DELETE` on the same URL as `GET` — resolved, see TODO-115.** The
schema declares `delete` on `/api/site/{site_pk}/video/{id}/` under the
same security block as the read, which looked alarming. Reading the
v0.3.0 source settled it: writes require `obj.creator == request.user`,
so a non-creator account gets 403. The mirror account creates nothing and
is therefore structurally incapable of deleting anything. The mirror
script should still issue no verb but `GET` — belt and braces, and it
keeps the script honest if the permission model ever changes upstream.

**Hazard — watch `/` during the pull.** The failure being guarded against
here is a full root disk, and the mirror pulls 26 GB through Django and
nginx on a host whose `/` sits at 62% with ~30 G free. Streaming
responses should not spool to disk, but "should not" is exactly the
assumption that produced this incident. Keep a `df -h /` running in a
second Session Manager pane for the first site, throttle the client, and
stop if free space moves. The instance is a t3.large — sustained transfer
will also draw down CPU credits, so pace it rather than saturating.

#### What actually happened — read this before the design notes below

The REST pull in this TODO **took production down** on 2026-08-25 after 773 of
2630 files (see ISS-FIELD-004). It was replaced by a host-side export. The
design notes that follow are kept for the reasoning, but several of their
premises were wrong:

| Assumed | Measured 2026-08-25 |
|---|---|
| ~1165 video records | **3176** across sites 2/3/4 — 2630 at site 4, 546 at site 2, 0 at site 3 |
| media fetched from the serializer's `file` URL | those URLs **404 with and without a JWT** — media is in MinIO behind Django's storage API, never on the nginx filesystem |
| all assets reachable over REST | **no `/keyframe/` action exists** — 1.4 GB of keyframes are unreachable by REST at any effort |
| site 2 holds media | site 2 has **no video files at all** (`file` null for all 546); all 29 GB is site 4 |

Bytes are served by the DRF actions `/playback/`, `/image/` and `/thumbnail/`.
The dead `file` URLs remain useful as **identifiers**: their paths give the
storage-relative layout the reprocessor needs on disk locally.

**The route that worked** — `mirror/export-media-to-s3.sh` on the host streams
`docker exec … tar -cf -` straight into `aws s3 cp -`, throttled, touching
neither Django nor host disk; `mirror/fetch-media-from-s3.sh` then pulls from
S3 with no load on LiveORC at all. 30 GB moved in 61 minutes.

It is also **more complete than this TODO's original design could have been**:
it captures the 1.4 GB of keyframes REST cannot serve, and 88 keyframe + 88
thumbnail files that exist on disk with a null database field.

#### Reconciliation — the question this TODO existed to answer

`videos/` holds **4463** files against 2630 records. Fully explained: LiveORC
stores velocimetry analysis images under `videos/` alongside the mp4s, and
exactly **1833** records have a non-null `image`. 2630 + 1833 = 4463, and
2630 × 9.2 MB + 1833 × 2.8 MB ≈ 29 GB against the measured 29 G.

**So the API accounts for everything of substance on disk.** The only real gap
is the 88 orphaned keyframe/thumbnail files noted above.

**Local mirror, verified 2026-08-25** — `data/liveorc-mirror/4/media`:

| Directory | Files | Size |
|---|---|---|
| `videos` | 4463 (2630 mp4 + 1833 jpg) | 29 G |
| `keyframe` | 2630 | 1.4 G |
| `thumb` | 2630 | 11 M |

Every file was checked against a host-generated list by name **and size** —
the check that catches a truncated tar, which a matching sha256 cannot, since
a short stream produces a valid tar whose checksum agrees at both ends. A
sample was then re-checksummed against the API-pulled hashes from the partial
REST pull: two independent transports agreeing on the same bytes.

**Still outstanding:** a fresh DB dump. `backup_liveorc_db.sh` has not been run
since the S3 copies of 2026-06-26/29, and without it these videos cannot be
reprocessed — `build_staging_local.sh` needs the Fit 6 `VideoConfig`,
camera_config and both cross-sections including `cross_section_wl`.

**Design notes:**

- **No pagination, no filters.** `site_video_list` declares no `page`,
  `limit`, or date parameters and returns a bare `array` of `Video`. So
  the list call may return all 1165 records in one response, and
  resumability has to be **client-side**: write the manifest to disk
  first, then work down it, skipping what already exists with a matching
  size. Never re-list to resume.
- **`file` is nullable.** Both stations run "LiveORC sync: time series +
  analysis images", with full-video upload disabled, so some records will
  legitimately have no video. Record them as null in the manifest rather
  than treating them as failures — the count of nulls is itself a result.
- **The manifest is the deliverable, not just the bytes.** A per-site
  JSON of every video id, timestamp, status, asset URLs and byte sizes is
  what makes TODO-112 Phase 5's `rsync --itemize-changes` checkable
  against something external. Right now that verification only compares
  the host to itself.
- **The mirror does not cover everything.** Be explicit about this in the
  README so it is never mistaken for a full backup: it captures media and
  the API-visible records, **not** the Postgres database (TODO-112
  Phase 1 does that, to `s3://openrivercam-video/backups/`), not
  `/liveorc/media/admin-interface`, and not the TimescaleDB sensor data,
  which is a separate stack entirely and reachable via Grafana.
- **Land it in `data/`,** which is already gitignored at the repo root.
  This repo is public — no manifest, token, or media file gets committed.
  610 G free on the workstation, so 26 GB is not a constraint.
- **The mirror account is ours, not IPB's.** See the ordering constraint
  below.

**Steps:**

*Phase 0 — access, before any bytes move*
- [ ] **Done in TODO-115**: create the mirror service account and run the
      verification matrix. The mirror runs as that account — an institute
      member that created nothing, so upstream's
      `IsOwnerOrReadOnlyAsInstitute` makes it read-only by construction.
      Do not start the pull until that matrix has actually been run.
- [ ] Confirm the access token's lifetime and that `/api/token/refresh/`
      works — a 26 GB pull will outlive one token, so the client needs
      refresh built in from the start rather than bolted on after a
      mid-pull 401.
- [ ] Note the institute id; `GET /api/site/` returns `[]` without
      `?institute=<id>`, which would otherwise look like an empty server.

*Phase 1 — inventory, no downloads*
- [ ] `GET /api/site/` and record every site id, not just 2/3/4.
- [ ] For each site, pull the video list and the timeseries list and
      write `data/liveorc-mirror/<site>/manifest.json`.
- [ ] Summarise: video count, how many have a null `file`, total bytes
      by asset type. **Reconcile against the runbook's 26 GB video /
      1.3 GB keyframe / 9.5 MB thumb figures.** A large gap here is
      information, not an error — it would mean the API does not see
      everything on disk, which changes what the mirror is worth.

*Phase 2 — the pull*
- [ ] Write `liveorc_server/mirror/orc_mirror.py` and commit it. Follow
      the repo conventions: `--check`/dry-run default, resumable,
      rate-limited, `--site` scoping, structured log. Read-only by
      construction — it issues **no** verb but `GET` and the one `POST`
      to `/api/token/`.
- [ ] Run it against the smallest site first, verify, then the rest.
      Watch `df -h /` on the host throughout the first site.
- [ ] Record per-file size and a checksum in the manifest as each file
      lands.

*Phase 3 — prove the copy is good*
- [ ] Re-run in `--check` mode: every manifest entry present, sizes
      match, nothing missing.
- [ ] Spot-check playability — open several mirrored videos locally,
      spread across the date range, including one from each site and one
      from either end of the 2026-05-14 → 2026-07-29 accumulation window.
- [ ] Confirm the timeseries JSON matches the analytics baseline in
      `liveorc_server/reprocess/`'s `api_timeseries.csv` where they
      overlap.
- [ ] Write `data/liveorc-mirror/README.md` (untracked, alongside the
      data) stating what the mirror contains, what it does **not**, and
      the restore path.

*Phase 4 — release the gate*
- [ ] Update TODO-112's status to note the verified independent copy
      exists, and proceed with Phase 1 there.

**Ordering constraint — do not let this provision IPB.** TODO-104 records
Dan's explicit position from the 2026-08-11 call: who gets LiveORC access,
and when, is **PMI's decision**, and nothing is to be provisioned ahead of
that approval. The mirror account created in Phase 0 is an *operational
account of ours*, for pulling our own backup — it is not IPB access and
does not touch that gate. Keep the two separate: this TODO builds and
proves the access path, TODO-104 decides who else walks down it. The
useful handoff to TODO-104 is the Phase 0 findings — the token flow, the
DELETE answer, and what a non-admin account can actually reach.

**Still to run this while Sukabumi is offline.** TODO-112 notes the media
tree is static because uploads stopped 2026-08-14. That helps here too: a
manifest captured against a static tree stays valid, so Phase 1's
inventory can be trusted as a baseline through Phase 3. If the station
comes back before this finishes, re-run Phase 1 and diff.

---

### TODO-112: Move LiveORC media onto a dedicated EBS volume

| Field | Value |
|-------|-------|
| **Status** | **DONE 2026-08-27** — media on the EBS volume, `/` 51 G → 21 G |
| **Site** | LiveORC server (AWS) |

**Gate released (2026-08-25).** TODO-114 delivered a complete, independently
verified copy of all 30 GB of media to `data/liveorc-mirror/`, checked file by
file against a host-generated list. Phase 5's `rsync --itemize-changes` now has
something external to be checked against.

**Two premises of this TODO are no longer true. Re-read before running.**

**1. The media tree is NOT static.** This TODO says uploads stopped 2026-08-14
and sequences itself *before* the station fix on that basis — "with no uploads
arriving, `rsync --itemize-changes` in Phase 5 means exactly what it says."
Sukabumi came back on **2026-08-20**: 1 file that day, then 45, 43, 9 and 6,
newest `created_at` **2026-08-24T21:32Z**, 104 new mp4s after the stated
cutoff. Normal cadence is 45–48/day, so 08-23 and 08-24 were degraded and it
has been quiet since — but the race this TODO was sequenced to avoid is open
again. Re-run the TODO-114 inventory and diff immediately before any Phase 5
rsync; do not trust a manifest across a gap of days.

**2. `/mnt/s3-storage` is residue, not a repair target.** I suggested on
2026-08-25 that fixing that mount might be shorter than this migration. That
was wrong, and the runbook already answers it — see "Why EBS and not S3" in
`MEDIA_VOLUME_RUNBOOK.md`. S3 was tried first and abandoned for two reasons
that still hold: LiveORC's storage backend is all-or-nothing (prod runs
`FileSystemStorage`, and `prod_reprocess.sh` execs inside the webapp precisely
to read the *local* media volume), and `rename(2)`/`link(2)` fail with `EXDEV`
across a mount boundary, with s3fs having no hardlink support at all.

The dead `mnt-s3\x2dstorage.mount` is the **leftover of that abandoned
migration**, deliberately left pointing somewhere harmless. Its failure is not
why media went to the writable layer. The actual cause is in the runbook's root
cause section: `MEDIA_ROOT` is `/liveorc/media`, and the compose bind pointed at
`/liveorc/data/media` — a path Django never writes to. Nothing was mounted where
it mattered, so writes succeeded into the container layer, silently.

Two things do follow from the mount being dead, and both are worth keeping:

- `liveorc.service` requires it, so the unit cannot start while it fails. That
  is a second interlock behind the `systemctl disable` this runbook mandates —
  and it disappears in Phase 9 when the unit is re-enabled.
- The `RequiresMountsFor` guard that Phase 6 adds must point at
  `/var/lib/liveorc-media`, **not** the old S3 path. The unit currently
  guards the wrong mount, which is landmine #2 in the runbook.

**Unpaused 2026-08-17.** The 2026-08-11 demo it was waiting on has passed
and Phase 0 is fully resolved, including the three files that were still
unread. Until Phase 6 lands the 26 GB of media lives only in the container
writable layer, so **`liveorc.service` must stay disabled** and a
root-volume snapshot is the standing safety net — see the warning block at
the top of the runbook.

**Run this before the station fix.** Decided 2026-08-26: LiveORC storage
first, station issues after. The reason originally given here — uploads
stopped 2026-08-14, so the media tree is static and Phase 5's
`rsync --itemize-changes` means exactly what it says — is **no longer
true**; Sukabumi resumed on 2026-08-20 (premise 1 above). The ordering
stands on its own reasoning: the 26 GB in the writable layer is what is at
risk, and every further day of uploads adds to what an accidental recreate
would destroy.

On 2026-08-10 the root filesystem hit 100% and took the host down —
LiveORC dead, Session Manager refusing to open a shell, Run Command
returning exit 1 with zero bytes on both streams, CPU pinned at ~98% for
a week.

The cause was a **path mismatch**. `MEDIA_ROOT` is `/liveorc/media`
(`settings.py:126`), but the compose bind targeted `/liveorc/data/media`
— a path Django never writes to. So 26 GB of video, 1.3 GB of keyframes
and 9.5 MB of thumbnails accumulated in the webapp container's
**ephemeral writable layer** between 2026-05-14 and 2026-07-29, with no
persistence, no backup, and no error ever raised. The mismatch is residue
from an abandoned S3 migration whose mount was left pointing somewhere
inert rather than removed.

S3 is not the fix and was correctly abandoned: LiveORC's storage backend
is all-or-nothing (prod runs `FileSystemStorage`, and `prod_reprocess.sh`
execs inside the webapp precisely to read local media), and `rename`/
`link` fail with `EXDEV` across a mount boundary — s3fs has no hardlink
support at all.

Full incident analysis and the phased procedure are in
[`liveorc_server/MEDIA_VOLUME_RUNBOOK.md`](liveorc_server/MEDIA_VOLUME_RUNBOOK.md).

**Two landmines this exposed**, both worth fixing regardless: the
reprocess runbook asserted a media backup was unnecessary "because the
video bytes live in MinIO/S3" — they did not, so any `--force-recreate`
during those runs would have destroyed 26 GB silently; and nothing
guarded the mount, so the one condition that mattered went unchecked.

**Steps:**
- [x] Diagnose: disk full, not compromise or runaway process.
- [x] Repair the root volume — it had been grown 50→80 GiB but
      `growpart` died at boot with `ENOSPC`, so partition and filesystem
      were expanded by hand. `/` now 77 G at 62%.
- [x] Confirm the database is safe (`db` → named volume
      `liveorc_lorc_data`, writable layer 0 B).
- [x] Phase 0 — no `os.link`/`os.rename`/`shutil.move` anywhere in the
      application code, so `/liveorc/data` can stay on `/` and Phase 5b is
      not needed. The image ships `/liveorc/media/admin-interface`, making
      Phase 4's seed step mandatory. `liveorc.service` turned out to couple
      to the s3fs mount in five places, not one.
- [x] **Snapshot the root EBS volume** — the 26 GB exists in exactly one
      place. Initiated 2026-08-10, confirmed complete 2026-08-17. This was
      the gate on everything destructive downstream.
- [x] `systemctl disable liveorc.service` (2026-08-10) — it runs
      `start-liveorc.sh` → `liveorc.sh start` → `docker compose up -d`,
      which recreates the webapp and destroys the writable layer, and the
      unit is `WantedBy=multi-user.target` so a reboot alone triggers it.
      Re-enable in Phase 6.
- [x] `docker update --restart unless-stopped rabbitmq` (2026-08-10). It
      was `restart=no` while `db` and `liveorc_webapp` were already
      `unless-stopped`, so a reboot would have brought the webapp up
      without its broker — video processing failing silently while the
      site looked healthy. `docker update` changes the policy in place
      and does not recreate the container.
- [x] Brought LiveORC up safely for the 2026-08-11 demo with
      `docker start db rabbitmq liveorc_webapp` (never `compose up`).
      Verified: video plays from the web UI.
- [x] Phase 1: DB backup → `s3://openrivercam-video/backups/` (2026-08-27,
      `20260827-125253`, 3488 ts rows / 3189 video rows). The bucket prefix
      was **empty** beforehand — three earlier backups had never left the
      host disk. All four are now off-host.
- [x] Phases 2–5 (2026-08-27): 150 GiB gp3 volume created, attached, ext4,
      mounted at `/var/lib/liveorc-media` by LABEL. Seeded `admin-interface`,
      copied **31 GB / 9775 files** out of the writable layer. Gate passed —
      counts identical both sides, dry-run `--itemize-changes` empty. Media had
      grown 26→31 GB, and mp4s 2630→2643, so uploads are still arriving.
- [x] Snapshot the media volume — `liveorc-media pre-cutover 2026-08-27`,
      completed. First time the 31 GB has existed in two places; this is
      what makes Phase 7 reversible.
- [x] Read the three Phase 6 inputs (2026-08-17). `start-liveorc.sh` passes
      `--storage-dir /mnt/s3-storage` and is a **local wrapper, not
      upstream**, so it is safe to edit. `verify-s3mount.sh` does a write
      test as well as a mountpoint check — rewrite and rename it rather
      than dropping it. `grep -rn "s3-storage"` **undercounts**: `After=`
      and `Requires=` use the escaped form `mnt-s3\x2dstorage.mount`, so
      use `grep -n 's3' /etc/systemd/system/liveorc.service` (5 hits).
- [x] Settled how the compose bind changes (2026-08-17). An override file
      is **not** an option: `liveorc.sh` builds an explicit `-f` list
      (`docker-compose.yml` plus rabbitmq/postgis/spatialite/ssl), and
      Compose auto-loads `docker-compose.override.yml` only when no `-f` is
      given. So the destination fix goes in
      `/opt/LiveORC/docker-compose.yml:8` directly — upstream-owned, and a
      LiveORC upgrade will revert it. The durable defense goes in
      `start-liveorc.sh`, which is a local wrapper: a pre-flight grep that
      refuses to start if the bind was reverted, and a post-start
      `docker inspect` that verifies the mount table rather than the config.
- [x] Phase 6 (2026-08-27): repointed **both halves of the path** — `start-liveorc.sh`'s
      `--storage-dir` (the source, and the real control point since it
      overrides `.env`) **and** the compose bind's destination
      (`/liveorc/data/media` → `/liveorc/media`). Changing only the first
      completes cleanly, verifies green, and leaves media in the writable
      layer exactly as now. Then fix all five s3fs couplings in
      `liveorc.service`, retire the vestigial s3fs mount unit, and
      re-enable the service.
- [x] Confirmed in the **running container**, not the config:
      `docker inspect liveorc_webapp --format '{{range .Mounts}}…'` must
      show `/var/lib/liveorc-media -> /liveorc/media`.
- [x] Phase 7 (2026-08-27): recreated with **`systemctl start liveorc.service`**, never a
      bare `docker compose up -d` — that bypasses `start-liveorc.sh`, so no
      `--storage-dir` is passed and neither guard runs, and
      `LORC_STORAGE_DIR` silently falls back to `.env`'s `lorc_media` named
      volume. Confirm the writable layer drops to MB and `/` falls to
      ~20 G; open an existing video and upload a new one.
- [ ] Phase 9: `systemctl enable liveorc.service` — pending — disabled since
      2026-08-10 so a reboot could not destroy the media. Safe once media
      is on the volume, and leaving it disabled means LiveORC silently does
      not come back after a reboot.
- [x] Disk-space check on `/` and the media volume (2026-08-27) — 15-min
      systemd timer, warn 75% / critical 85%, publishes `ORC/Disk/UsedPercent`.
      **Still needs an SNS notification on the CloudWatch alarm** — journal
      output is not an alarm.
- [x] Corrected the false media-backup claim in
      `liveorc_server/reprocess/REPROCESS_RUNBOOK.md` (2026-08-27).

**Two things this exposed, both logged as issues:**

- **ISS-FIELD-005** — LiveORC 0.3.0's nginx template uses `ssl on;`, removed in
  nginx 1.25.1, while its own image ships 1.26.3. A hand-patched config had been
  living in the writable layer since May with no copy anywhere. The recreate
  deleted it and took the site down. Same failure class as the media itself.
  Repaired durably in `start-liveorc.sh`.
- **ISS-FIELD-006** — `liveorc.sh` appends `--scale liveorc_worker=N` while
  upstream has that service **commented out** (`# TODO: add back workers that
  connect to ORC-OS API`), so any value above 0 makes compose abort before
  starting anything. `LORC_DEFAULT_NODES=0` is correct for this version. Acting
  on the opposite assumption took LiveORC down for ~6 minutes on 2026-08-27.
- **ISS-FIELD-007** — video processing errors ran 2-5% through June, then
  **24% in July and 32% in August**, tracking the root disk filling up. Roughly
  377 videos were stored but never became timeseries. The files are on the media
  volume, so if the cause was the full disk they are likely recoverable — feed
  into TODO-113.

### RESUME HERE — state at 2026-08-28 22:05 WIB

Session of 2026-08-28, **ended deliberately to restart under tmux** — nothing
was interrupted, the tree is clean and both commits are in. **First action on
resume is to re-arm the watcher; see "Restarting" at the end of this block.**

**Station is still DOWN.** Last sensor row 08-28 05:30 WIB; 16 h and 32 missed
wakes later there is nothing. `tcp/22` closed, Tailscale `offline, last seen
14h ago`. Genuinely down, not an upload fault.

**The self-recovery did not come.** The previous resume block expected one —
"it has self-recovered mid-morning before, unattended". 11:00 WIB came and
went. Two corrections to that expectation, both from the sensor record:

- There was **no sensor outage on 2026-08-27 at all** — zero gaps over 31
  minutes anywhere between 08-25 and 05:30 today. Whatever came back at 11:00
  WIB on 08-27 was SSH/Tailscale reachability, not the station. The precedent
  was weaker than it was written up as.
- Sorting the 13 historical outages by onset hour splits them cleanly.
  Daylight onsets (06:23, 06:31, 08:20, 10:39, 10:43, 11:33, 14:09, 14:13,
  15:01) ran 0.9 h – 23.1 h. **Night onsets (23:01, 00:47, 01:30, 04:30) ran
  38 h, 9.3 d, 5.4 d and 7.3 d** — the four longest outages on record. This
  one started at 05:30. n=4, so suggestive rather than proven, but the odds of
  it clearing unattended are poor and a site visit may be the only way back.

**How the night actually ran.** Better than expected, then abrupt:

| Window (WIB) | Behaviour |
|---|---|
| 08-27 18:35 – 20:51 | extended wakes — 17, running to the 25-min backstop |
| 08-27 21:00 – 08-28 05:30 | **18 consecutive clean on-cadence wakes**, one tick each, dead on :00/:30 |
| 08-28 06:00 → | nothing |

Two things in that timeline cut against the working theory:

1. **The extended wakes stopped at 21:00 WIB, 6.5 hours before the purge**
   (purge landed 03:32 WIB). Nothing had been deployed to the station at that
   point and the disk was still at 5.00 GiB free. They ceased on their own, so
   the purge cannot be credited with the clean run that followed.
2. **The station died out of the clean stretch, not out of a long-wake
   window.** The final reading is unremarkable: V-IN 12.717 V, both samples
   identical, iout 0.923 A.

The 18:30–21:00 long-wake test **still has not run on a healthy disk.** It did
not run tonight either — 08-28 18:30 passed with the station down.

**What the Witty Pi telemetry says.** Only 11 rows exist, all 02:30–05:30 WIB
on 08-28; the 03:00 and 03:30 wakes were lost to the root-owned CSV, which the
04:01 WIB deploy fixed (rows resume at 04:00, confirmed working). V-IN sits
**12.56 – 12.85 V** across three hours with **no downward slide**, then the
station vanishes. Against the decision table in `wittypi.conf` that is not the
capacity-exhaustion signature — there is no knee — and flatness across three
sleep intervals disfavours a large parasitic drain, though the LiFePO4 plateau
is flat enough to mask real SoC change. Five wakes of data, none at the moment
of failure. Thin, and it should not be leaned on.

**The source-resistance fit cannot be done with this sensor's output.** It was
attempted: R² = 0.232 over 11 points and a 0.358 A load span. The fit is not
merely weak, it is impossible, and the reason is a direct contradiction —

    04:02:15   iout 0.852 A   V-IN span 0.009 V
    04:30:27   iout 0.852 A   V-IN span 0.479 V

Same current, 53x the sag. No fixed source resistance produces both. Reading
`read_wittypi()` explains it: with `SAMPLES=2` and `SAMPLE_GAP_SEC=1.0`,
`vin_v` is the **mean** of two samples, `vin_min_v`/`vin_max_v` are the min and
max **of those same two** — so the "spread" is just the delta across one second
— while `vout_v` and `iout_a` come from `lasts`, i.e. **the last sample only**.
Voltage and current are therefore read at different instants, and the instant
that sagged has no current measurement at all. The 0.479 V sag is real; the
load that caused it was never measured, so it cannot be divided into ohms.

**Ohms vs milliohms — bad connection vs worn pack — remains undecided, and
will stay undecided until the driver emits paired V and I.** See TODO-117.

**Still unchanged on the station, by instruction.** Low-voltage threshold still
UNSET (menu option 7). Recovery voltage 13.0 V (option 8) — note this is
probably inert while the threshold is unset, which is worth confirming. The
2744 failed syncs are untouched. `/home/pi/code/git` has 3 uncommitted local
changes, left alone.

**Changed on the workstation this session:**

- `station_watch.py` now triggers on **tcp/22**, not Tailscale's `Online` flag.
  `port_open()` had been present and documented as ground truth since it was
  written, and `check()` never called it — the file carried the warning in two
  docstrings while doing the wrong thing anyway. Poll interval 60 s -> 15 s
  (the awake window is under 60 s, so a 60 s poll can miss a whole wake); the
  Grafana query is throttled separately by `--sensor-poll`, default 300 s. A
  fresh sensor row is now reported but never triggers a collect, because a
  collect that cannot connect is a window spent for nothing.
- Added `station-watch.service`, the systemd user unit the module docstring has
  referenced since it was written and which did not exist. **Not installed** —
  it needs `systemctl --user enable --now station-watch` and, to survive
  logout, `sudo loginctl enable-linger $USER`. Until that happens the watcher
  is still session-local, which is the whole reason it keeps needing re-arming.

**Session of 2026-08-28 (under tmux), what changed:**

- **The watcher did not die.** The previous block twice predicted it would.
  It had been reparented to init and was still polling on resume, with an
  unbroken log. The prediction was wrong; the underlying fragility was not.
- **It is now a systemd user unit and no longer session-local.**
  `station-watch.service` is installed, enabled and running. Its logging was
  changed from the journal to `append:` on
  `data/station-forensics/station-watch.log`, so the one continuous record is
  preserved — the hand-run watcher's last line is 14:43:14Z and the unit's
  first is 14:43:34Z, no gap. **Still needs one manual step to survive logout:**
  `sudo loginctl enable-linger tjordan` (root, interactive).
- **The long-wake precursor was tested across all 13 outages** — see
  ISS-FIELD-009. Long wakes precede 9/12 usable onsets vs 10% of baseline
  windows (p = 2.7e-07), which is the first quantitative support the energy
  mechanism has had. But they are **not necessary**: 2026-08-15, the 5.4-day
  outage, came out of 42.6 days of clean cadence with zero long wakes in the
  preceding 72 h. A cold-temperature explanation was tested and killed.
- **2026-08-15 investigated.** Three explanations ruled out: it did not die
  mid-cycle (the 01:30 final wake is complete), there was no drain (48 rows/day
  for 42 consecutive days), and harvest was not declining (flat diurnal swing,
  08-14 above median). What turned up instead is in how outages *end* —
  **10 of 13 recoveries are unscheduled boots**, 3.6–14.9 min off the :00/:30
  grid against a p99 of 1.20 min for on-cadence wakes.
- **Tom confirms those are button presses at the site**, and that the 13 V
  recovery voltage was set *after* the 08-21 recovery. Two consequences: the
  station does not clear these outages by itself, and **the current outage is
  the first test of the recovery-voltage setting.** The three on-grid
  recoveries (07:00, 07:31, 08:30 WIB, all within 90 min of sunrise) are the
  signature of a genuine self-recovery — that is what to look for.

**The station did not come back.** Still down at 22:05 WIB, ~16.6 h and 33
missed wakes. Nothing collected unattended. The night-onset pattern continues
to hold.

**Next session, in order:**

1. Check whether it came back: `station_gaps.py`, and
   `data/station-forensics/` for anything the unit grabbed unattended.
   The watcher now runs unattended for real, so an overnight recovery
   should finally be captured.
2. If it is back — the deferred test. Does the 18:30–21:00 WIB window run clean
   with a healthy disk? Untested since 08-27, and still untested.
3. TODO-117 is written and tested but **not deployed** — the station has been
   unreachable since. Run `pi/tools/orc_deploy_wittypi_sensor.sh` the moment
   tcp/22 opens; the pre-flight now runs `test_wittypi_pairing.py` itself, so
   there is nothing to check by hand first.
4. **Decide on a site visit.** 08-15 is now largely worked out (see
   ISS-FIELD-009) and the conclusion is operational: 10 of 13 outages needed
   someone at the site. An unattended recovery would appear **on-grid between
   07:00 and 08:30 WIB**; the 08-28 dawn passed with nothing. The open
   question is no longer the recovery but the **trigger** — what stops a
   station that has run 42 flawless days — and the artefact that speaks to it
   is the Witty Pi power-on-reason log, which is what step 3 unlocks.
5. Run `sudo loginctl enable-linger tjordan` so the watcher survives logout.

**Restarting.** Branch `iss-field-009-wittypi-paired-vi`, working tree clean.
The watcher is a systemd unit now — `systemctl --user status station-watch` to
check it, and there is nothing to re-arm by hand. If it ever needs stopping,
`systemctl --user stop station-watch`, not a kill.

**Access notes.** SSH is `pi@orc-sukabumi` over Tailscale with the password in
the gitignored `spring_2026_ID/.env`, driven via `SSH_ASKPASS` +
`SSH_ASKPASS_REQUIRE=force`. Trigger on **tcp/22**, never on Tailscale's
`Online` flag — it stays stale for minutes after this station sleeps. The awake
window is **under 60 seconds**, so nothing can be done by hand.

---


### TODO-116: Witty Pi restart resiliency — a missed boot leaves the station down

| Field | Value |
|-------|-------|
| **Status** | OPEN — captured 2026-08-25; measured 2026-08-27, see ISS-FIELD-008 |
| **Site** | Both stations (Witty Pi scheduling) |

The station periodically misses a boot cycle — battery is the leading
suspect — and does not recover on its own. The failure mode is the
scheduler, not the power event: once a boot is missed, the Witty Pi's
"next start time" is left in the **past**, and nothing re-arms it. The
station stays down until someone physically pushes the button.

**Measured 2026-08-27 (ISS-FIELD-008).** Eight outages since May, **25.4 days
down out of 117.9 — 22%**, including one of 9.3 days. Sukabumi is down right
now, since 08-27 04:30 WIB. Every failure since May starts between 23:00 and
04:30 WIB; every recovery lands in local business hours, which is what a button
press looks like, not a voltage threshold. Regenerate any of this with
`liveorc_server/station-health/station_gaps.py`.

**Split the work along the two mechanisms.** The *latch* (alarm left in the
past, nothing re-arms it) is independent of the *trigger* (whatever kills the
cycle) and is the higher-value half: it turns an unbounded outage into a
30-minute one, and it is worth fixing even if the battery diagnosis is wrong.

**The mechanism has a second candidate now.** The station also boots
off-schedule in episodes, at 5-minute spacing — 332 such boots in May, 49 in
August, and a run every five minutes from 22:05 to 02:30 on the night of
08-25→26. That is either a voltage threshold or the Witty Pi re-powering the Pi
inside its own 25-minute `ON` window; the 5-minute spacing equals `OFF M5` in
`prod_30.wpi`. Timestamps cannot separate them. **Do not design a fix until the
`wp5` power-on-reason log has been read** — it names the cause directly, and it
is the first thing to collect when the station is reachable.

**A live, undocumented variable:** a 13 V recovery voltage was set around
2026-08-21 and is recorded in no committed file. It did not cause the
off-schedule boots (they predate it by months), but it may be why 08-27's full
sunny day produced no boot at all. Read the low-voltage cutoff alongside it —
one threshold alone says nothing about hysteresis.

- [ ] Collect the `wp5` power-on-reason log and both voltage thresholds, before
      changing anything else on the station. Run
      `station-health/station_watch.py`; the awake window is under 60 seconds,
      measured 08-27, so a human cannot catch it.
- [ ] Confirm from the `wp5` source what the firmware does with a past-due
      alarm at power-on — the latch mechanism is a plausible reading, not a
      verified one.
- [ ] Add Witty Pi Vin + power-on reason to `orc-sensors`, so the battery
      hypothesis stops being unfalsifiable. Closes TODO-012's DDR-60G question
      as a side effect.
- [ ] Bench-reproduce on Jakarta — merge with TODO-108, which already wants it
      on a soak rig. Sweep Vin and find the hunting band directly.
- [ ] Fix the latch: prefer a config threshold if the firmware has one;
      otherwise a boot-time re-arm unit that sets the next alarm unconditionally,
      early enough that ORC-OS cannot shut the box down first. Then a human
      button press also re-arms the schedule instead of buying one cycle.
- [ ] Commit the active schedule and voltage thresholds. `deploy.sh:347`
      excludes `*.wpi` from the overlay, so schedule changes reach the Witty Pi
      only by USB-C drag-drop or the `wp5` menu — **prefer fixes that live in
      files `deploy.sh` already manages.** The running schedule is 30-minute
      while the assembly docs call `prod_15.wpi` the default.

**No longer blocked on physical access.** The station recovered **on its own**
at 11:00 WIB on 2026-08-27, 6.5 hours after failing, with nobody sent to site.
It is up and cycling now. That also unseats this TODO's premise: "stays down
until someone physically pushes the button" is not established, and the
07:00-13:00 recovery cluster is at least as consistent with solar pushing the
battery back over a voltage threshold. The 6.5-hour outage against a prior
range of 21 hours to 9 days suggests the 13 V recovery voltage set on ~08-21
may be doing exactly what it was meant to.

**Root cause found 2026-08-27 — ISS-FIELD-009.** The station disk is pinned at
its 5 GB purge threshold, 43% of videos fail processing, the ORC-OS task never
completes, so `shutdown_after_task` never fires and the Pi runs to the Witty
Pi's 25-minute backstop instead of ~2 minutes. That is ~12x the energy budget
per affected cycle, and it is what flattens the battery overnight.

Two things I had wrong and that are corrected in ISS-FIELD-008: the "5-minute
restarts" were never restarts — `wp5d.log` records every startup as a scheduled
one, and the extra rows are the sensors' own 300-second interval firing during
an extended wake. And the battery is the last link in this chain, not the
first.

**Fix ISS-FIELD-009 before touching power settings.** A low-voltage threshold is
worth having regardless, but the right value looks different against a station
that is not burning 12x its budget, and the disk is where the damage starts.

**Correction 2026-08-28 — the 08-27 "self-recovery" was not one.** This entry
says the station "was down since 08-27 04:30 WIB" and "recovered **on its own**
at 11:00 WIB", and rests the "No longer blocked on physical access" conclusion
on it. The sensor record does not support it: there is **no gap over 31 minutes
anywhere between 08-25 and 08-28 05:30**, so the station was logging normally
straight through 08-27 04:30–11:00. The natural reading is that the outage was
in *reachability* — SSH/Tailscale — and not in the station, which is exactly
the confusion `station_watch.py` was carrying in `check()` (fixed 08-28). A
station that is up but unreachable produces no sensor gap; a station that is
down cannot log at all.

That withdraws the evidence for "it recovers without a site visit", and with it
the inference that the 13 V recovery voltage is working. Both go back to
unknown. The 07:00–13:00 recovery cluster across the *other* twelve outages is
untouched by this and still stands.

### TODO-117: Witty Pi sensor must emit paired V and I, or the battery question stays unanswerable

| Field | Value |
|-------|-------|
| **Status** | IN PROGRESS — found and driver reworked 2026-08-28; **not yet deployed**, the station has been down since 05:30 WIB that morning |
| **Site** | Sukabumi (and any station running `orc-sensors`) |

The `wittypi` sensor was added to settle whether the overnight failures come
from a **worn pack** or a **bad connection** — ohms versus milliohms in the
battery-to-Witty-Pi path. That is decided by an effective source resistance,
which needs `V_in` and `I_in` measured **at the same instant**. The driver does
not provide that, so the question cannot be answered from what it uploads.

**What `read_wittypi()` actually emits.** With `SAMPLES=2` and
`SAMPLE_GAP_SEC=1.0` in `wittypi.conf`:

| Field | What it is |
|---|---|
| `vin_v` | **mean** of the two samples |
| `vin_min_v` / `vin_max_v` | min and max **of those same two** — so the "spread" is one 1-second delta, not an extremum over the wake |
| `vout_v`, `iout_a` | `lasts[...]` — **the last sample only** |

So the voltage figures and the current figure come from different instants, and
whichever instant sagged has no current reading attached to it at all.

**How it fails in practice.** Fitting `V_in` against load across the 11 rows
from 2026-08-28 gives R² = 0.232 over a 0.358 A span — but the fit is not
merely weak, it is ruled out:

    04:02:15   iout 0.852 A   V-IN span 0.009 V
    04:30:27   iout 0.852 A   V-IN span 0.479 V

Identical current, 53x the sag. No fixed source resistance produces both. The
0.479 V sag is real and it is the most interesting number in the dataset; the
load that caused it was simply never measured.

**The fix is small.** Keep per-sample `(vin, iout)` pairs inside the sampling
loop instead of averaging one and taking the last of the other, and emit enough
of the pairing to fit a line. Minimum viable: `iout_min_a` / `iout_max_a` plus
the `vin` recorded at each, so every row carries at least two paired points.

- [x] Rework `read_wittypi()` to collect `(vin, vout, iout)` per sample and emit
      paired extremes rather than mean-vs-last. `CSV_HEADER` extended with
      `iout_min_a`, `iout_max_a`, `vin_at_imin_v`, `vin_at_imax_v`, `samples_n`,
      `samples_paired_n`; `sensor-ingest` derives metric names from the header
      with no whitelist, so no server-side change was needed. **Semantic change:
      `iout_a` and `vout_v` were the last sample and are now means over the same
      samples as `vin_v`, which makes `(vin_v, iout_a)` a legitimate paired point
      for an across-wake fit. Rows before this carry the old meaning.**
- [x] Raise `SAMPLES` above 2 — now 6 at 2.0 s, ~10 s per tick. The old budget
      note was stale: it claimed each read costs the full `READ_TIMEOUT_SEC`
      because `wp5` never exits, which stopped being true when `_wp5_sample`
      started feeding it Exit. Measured 2026-08-28, sht40 logged at 04:30:26 and
      wittypi at 04:30:27 with two samples and a mandatory 1.0 s gap, so reads
      cost well under a second and the budget was pessimistic by ~10x.
- [x] Add `pi/tools/test_wittypi_pairing.py` and wire it into the deploy
      pre-flight. `py_compile` proves only that the file parses; it passed
      happily on the broken driver. The test drives the sampling logic against
      synthetic `wp5` status headers (through the module's own regexes, since
      those have broken before on the `V-IN` hyphen), asserts the emitted keys
      match `CSV_HEADER` in both directions, and asserts the specific defect —
      a Vin spread reported against a zero load spread — cannot recur.
- [ ] **Deploy.** Blocked only on the station being reachable. Run
      `orc_deploy_wittypi_sensor.sh`; the watcher will say when tcp/22 opens.
- [ ] Widen the lever arm if the first day's rows are still cramped. ~10 s of
      wall time may or may not straddle the camera/PoE switch-on, which is the
      largest load step available. If `iout_max_a - iout_min_a` stays small,
      raise `SAMPLES` further or move the tick — do not raise it blind, the
      wake budget is real even if the old number was wrong.
- [ ] Then fit, and read the answer: **ohms means a bad connection** — fuse
      holder, terminal, crimp — which is cheap to fix and changes the remedy
      completely. **Milliohms points back at the cells.** Convert through the
      buck first (`I_in ~ Vout*Iout/(eta*Vin)`); it shifts magnitude, not the
      ohms-vs-milliohms verdict.

**Do not set a low-voltage threshold before this resolves.** The right value
differs depending on whether the sag is connection resistance or pack
condition, and a threshold chosen against the wrong one over-discharges a
LiFePO4 pack or cuts a healthy station off early.

Deploys via `pi/tools/orc_deploy_wittypi_sensor.sh`, which already backs up,
`py_compile`s before going live, and rolls back on failure. Note the 2026-08-27
lesson recorded in that script's history: **test as the service user** — a
root-created CSV silently broke every timer run, and cost the 03:00 and 03:30
WIB rows on the night the station died.

---

## DONE — post-trip

(Completed work since returning from Indonesia goes here. Use the
`Last updated` date at the top of the file as the reference point.)

*(none yet — file just rebuilt)*

---

## Pre-trip TODO history

The pre-trip task list (TODO-001 through TODO-022, all the day-by-day
hardware/software/integration items, and the build-week checklists)
is preserved in git history. Run
`git log --follow -p spring_2026_ID/TODO.md` to read it. Anything from
that list that's still open post-trip is mentioned by reference under
TODO-107 above.
