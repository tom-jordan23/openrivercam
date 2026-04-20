# Professional Surveyor Procurement and Fallback Options for ORC Stations in Sukabumi Regency

*Research compiled 2026-04-20 (Day 4, Jakarta deployment).*

## Part 1 — Hiring a Professional Surveyor in Sukabumi

### Context and Current Conditions

Idul Fitri 1447H fell on 21–22 March 2026, with official joint leave (cuti bersama) running from 18 March through 1 April 2026, and government offices resuming full operations from 30 March onwards. You are working on Day 4 of your deployment trip on 20 April, meaning the post-Lebaran recovery period is essentially over. Most private survey firms in Bandung and Jakarta will have fully resumed operations by mid-April. This is a generally favorable window: work queues are clearing after the holiday backlog, and school/university terms have restarted, meaning student field teams are available.

### 1. Named Providers

| # | Name | Type | City | Sukabumi coverage | Services relevant to your job | Website / Contact |
|---|------|------|------|--------------------|-------------------------------|-------------------|
| 1 | **Geopasi Survey** | Private firm | Bandung | Explicitly listed as a service area | RTK GPS survey, topographic survey, cross-section, hydrographic survey, drone mapping | [geopasi.com](https://geopasi.com/jasa-survey-gps/) — contact via site form; also on LinkedIn |
| 2 | **TechnoGIS Indonesia** | Private firm | Jakarta / branches | Serves West Java broadly; branch address listed in Kebon Jeruk Jakarta Barat | GPS geodetic survey, topographic, UAV mapping, GIS processing | [technogis.co.id](https://www.technogis.co.id/contact/) — Phone: +62-813-2552-3979; Email: marketing@technogis.co.id |
| 3 | **PT LAPI Ganeshatama Consulting (LAPI GTC)** | ITB commercial unit | Bandung (ITB Ganesha campus) | Serves all of West Java and national projects | Topographic survey, geodetic control, hydrology, GPS data processing; supported by ITB faculty and professional engineers | [lapiganeshatama.co.id](https://www.lapiganeshatama.co.id/) — Phone: +62-22-250-7463; Address: Jl. Ganesha No. 15-B, Bandung 40132 |
| 4 | **CV Tata Bumi Geosurvey** | Smaller private firm | Sukabumi / West Java | Documented as operating in Sukabumi-Bandung corridor; 8+ years experience | RTK geodetic GPS, drone UAV, digital total station; construction and plantation project backgrounds | [tatabumigeosurvey.com](https://tatabumigeosurvey.com/) |
| 5 | **Geoindo Survey Services** | Established private firm | Bandung | National coverage from Bandung base since 1994 | Terrestrial surveys, hydrographic, topographic, GPS control surveys | [geoindo.com](http://www.geoindo.com/) — Phone: +62-22-751-3168; Address: Jl. Batununggal Indah IV No. 83, Bandung |
| 6 | **Geo Survey Persada Indonesia (GSPI)** | Private firm | Jakarta / national | National coverage; active in West Java infrastructure projects | Terrestrial survey, LiDAR, drone photogrammetry, hydrographic, data management | [geosurveypersada.com](https://geosurveypersada.com/contact-us) |
| 7 | **Freelance juru ukur via BNSP network** | Individual certified surveyor | Anywhere in Java | Regional freelancers reachable via Tokopedia Mitra / Facebook groups / word of mouth | GCP measurement only; bring or rent their own RTK kit | No central platform; search "juru ukur SKK geodesi Sukabumi" in Facebook groups or via local contractor contacts |

**Notes on Tier (c) — University teams:** ITB Teknik Geodesi dan Geomatika does not run a public commercial survey service directly, but PT LAPI GTC (entry 3 above) is the formally designated commercial/consulting unit of ITB and employs faculty and post-graduate students. UNPAD (Jatinangor campus near Bandung) does not maintain a specialist geodesy department. UGM Teknik Geodesi (Yogyakarta) is higher quality but adds 2–3 days of travel time and mobilization cost, making it less practical for a same-week job in Sukabumi.

### 2. Turnaround and Lead Time

For a small job (1–2 field days: 4–6 GCPs plus a cross-section survey at one river site):

- **Quote to mobilization:** 2–5 working days for a firm already familiar with the region. Firms with West Java operations can typically mobilize faster than Jakarta firms who need to send a team.
- **Field work:** 1 day for GCPs plus cross-section at a single site; 2 days if two sites are involved.
- **Data processing and report delivery:** 3–7 working days after field work.
- **Total elapsed time from first contact to final report:** approximately 1–2 weeks in a normal period. Contacting multiple providers simultaneously and specifying a 48-hour response window is recommended.

### 3. Accuracy Expectations in Writing

- **RTK GCP accuracy:** Indonesian RTK practice using InaCORS BIG network corrections typically achieves horizontal RMSE of 1–3 cm and vertical RMSE of 3–7 cm with adequate observation time (1–5 minutes RTK fixed).
- **Datum and coordinate system:** Indonesian standard is **SRGI2013** (ITRF2008 at epoch 2012.0, closely aligned with WGS84). Sukabumi is in **UTM Zone 48S**. Always request UTM metres rather than lat/lon — pyorc requires a locally valid projected system in metres.
- **CORS access:** InaCORS BIG (397 stations nationally) covers West Java well. RTK corrections via NTRIP and post-processing of RINEX are both free public services via [srgi.big.go.id](https://srgi.big.go.id/page/online-post-processing).
- **Language for the SOW:** *"Pengukuran GCP dengan metode RTK menggunakan koreksi jaringan InaCORS BIG, akurasi horizontal ≤ 3 cm RMSE, akurasi vertikal ≤ 7 cm RMSE, dalam sistem referensi SRGI2013, koordinat output UTM Zone 48S."*

### 4. Deliverable Formats

- **Coordinate list** in CSV/Excel: point ID, Easting (m), Northing (m), Elevation (m), RMSE horizontal, RMSE vertical, observation duration, fix status (RTK Fixed / Float).
- **Raw RINEX data** (static) or NMEA log (RTK rover) — request explicitly.
- **Cross-section data** as CSV of distance–elevation pairs with chainage from a defined datum stake.
- **Staff gauge tie**: elevation of gauge zero in the survey coordinate system with at least two independent checks.
- **Survey report** (laporan survei): field conditions, equipment model/serial, CORS stations used, processing software, RMSE, sketches of GCP monument positions.
- **DWG/SHP file** of cross-section geometry (specify in SOW if wanted).

### 5. Procurement Mechanics

- **Penawaran harga:** Brief SOW by WhatsApp or email → formal surat penawaran in 1–3 days. Total price range for a 1–2 day job: **Rp 5,000,000–Rp 15,000,000** all-in.
- **DP (down payment):** 30–50% upon SPK (Surat Perintah Kerja); remainder on report delivery.
- **PPN:** 11% as of 2024. Confirm whether quoted price is inclusive or *belum termasuk PPN*.
- **Payment:** Bank transfer standard; cash accepted for small jobs.
- **SOW minimum contents:** Site location, deliverables list, accuracy specification, coordinate system, delivery deadline, payment schedule.

### 6. Specific Risks and How to Manage Them

- **"RTK" delivered at handheld accuracy (3–5 m).** Prevention: require equipment model and serial in the SOW, and RMSE values (not just "centimeter accuracy"). Acceptable kit: Emlid Reach RS2/RS2+, Trimble R series, Leica GS, Hi-Target V, Topcon HiPer. Quotes under Rp 3,000,000/day all-in are likely not multi-band geodetic grade.
- **Float accepted as Fixed.** Float is 20–50 cm. Require "RTK Fixed status only" in the SOW; Float points must be re-measured.
- **Vertical datum inconsistency.** Require a single consistent datum across all deliverables — either InaCORS ellipsoidal height or EGM2008 orthometric height.
- **Late delivery.** Request a denda keterlambatan clause (1% per working day past deadline).

---

## Part 2 — Escape Hatch: What to Do If Existing Survey Data Cannot Be Made to Work

### Overview: Where Errors Actually Matter in ORC

- **Cross-section error dominates at low flow.** Discharge = velocity × area. At low flow the wet section may be 20–40% of bankfull. A 10 cm vertical error in a 0.3 m deep section can produce a 30%+ area error and proportional discharge error.
- **GCP error dominates velocity field projection.** GCPs define pixel-to-world transformation; a 10–20 cm systematic error distorts the orthorectified velocity grid, biasing all discharge estimates.
- **Staff gauge datum error** shifts the wetted area up/down the bank profile; interacts with cross-section shape.

### Options Comparison Table

| Option | What it is | Achievable accuracy | Cost (IDR) | Time | Expected ORC outcome |
|--------|-----------|---------------------|-----------|------|----------------------|
| **A** | Post-process existing GNSS against InaCORS RINEX | 3–7 cm RMSE if raw RINEX logged; no improvement if only positions | Free | 1–3 days desktop | Good if RINEX available; no improvement otherwise |
| **B** | Rent multi-band RTK (Emlid RS2 etc.) + re-measure | 2–5 cm H, 5–10 cm V (RTK Fixed) | Rp 3–5M | 2–4 days | Good; suitable for ORC |
| **C** | Hire surveyor for GCPs only (half-day per site) | 2–3 cm RTK | Rp 3–7M per site | 1–2 weeks | Good for GCPs; cross-section quality = yours |
| **D** | Drone photogrammetry (SfM) | 5–15 cm H / 10–20 cm V without GCPs; 3–5 cm with GCPs | Rp 5–15M | 1–2 weeks | Moderate; no bathymetry |
| **E** | Public datasets (DEMNAS, SRTM, satellite imagery) | DEMNAS ~8 m RMSE vertical; imagery planimetric only | Free | Days | Not suitable for cross-section; planimetric sanity check only |
| **F** | University team (ITB/LAPI GTC) | Same as pro firm, often better reports | Rp 5–15M | 2–3 weeks | High quality; timeline risk |
| **G** | Pro benchmark tie + DIY detail survey | 2–5 cm benchmark; ±3–10 mm DIY level | Rp 2–5M + your time | 1 week | Moderate-good if you're careful |

### Detailed Evaluation

#### Option A — Post-Process Existing GNSS Data Against InaCORS

Upload raw RINEX to the BIG InaCORS online post-processing service at [srgi.big.go.id/page/online-post-processing](https://srgi.big.go.id/page/online-post-processing). For baselines under 3,500 m, achieves 1–3 cm horizontal and under 7 cm vertical with 1 hour of static observation.

**Limitation:** Requires raw RINEX. If you only have recorded positions (e.g. from a smartphone GNSS app or a consumer receiver outputting NMEA), post-processing is not possible. A Garmin or similar consumer unit cannot be improved this way.

**Imagery-based GCP sanity check:** If GCPs have poor accuracy but identifiable features in an orthoimage exist (roads, field boundaries), you can adjust GCP planimetric positions by matching against BIG satellite mosaic or Bing/Maxar in QGIS. Use this only as a sanity check, not a primary method — imagery pixel size is 0.5–1 m.

#### Option B — Rent Multi-Band RTK and Re-Measure

Rent an Emlid Reach RS2/RS2+ or equivalent and rover against InaCORS NTRIP (free, no separate base needed).

**Where to rent:**
- **CV BNT (totalstation.co.id):** Jakarta; Rp 750,000/day, weekly Rp 5,000,000. [Rental link](https://totalstation.co.id/product/sewa-gps-rtk-geodetik-murah/)
- **MSDI (msdi.co.id):** Jakarta; Emlid Reach RS2/RS2+ and Trimble. [Rental link](https://www.msdi.co.id/services/rental-gnss-survey-instrument/emlid-reach-rs2-rsplus/)
- **CV ADHIJASA:** Jakarta/Bandung; covers Sukabumi. [Rental link](https://adhijasa.com/rental-gps-rtk-gnss-geodetik/)
- **DND Survey:** Bandung; multi-brand RTK.
- **Gita Survey:** Jakarta/Bandung; rents Emlid.

**Accuracy for a solo operator:** Emlid RS2+ on InaCORS NTRIP → 2–3 cm H, 5–8 cm V in RTK Fixed in open conditions. Canopy over the river degrades performance; plan GCP positions in open sky.

**Smartphone-based RTK (SW Maps + external antenna):** Android SW Maps supports Bluetooth to Emlid Reach RS2 / ArduSimple boards. With a proper external multi-band antenna and NTRIP, accuracy is comparable to a dedicated data collector. The phone's built-in GNSS is not sufficient — the external receiver does the work.

**Cost all-in:** Rp 750k–1.5M/day × 2 days + travel = Rp 3–5M (USD 185–310). Lowest-cost path to centimetre GCPs if you're comfortable with the equipment.

#### Option C — Hire a Surveyor for GCPs Only

Half-day engagement per site: GCPs and staff gauge tie only, keep your own cross-section. Saves roughly 40–60% vs a full job. **Use when:** cross-section geometry looks consistent but GCPs came from a non-geodetic device. Common real-world combination: cross-section with optical level from a fixed reference (good), GCPs from a phone (poor) — Option C fixes the suspect half.

#### Option D — Drone Photogrammetry (SfM)

Fly 60–120 m altitude, 80%+ image overlap, process with Agisoft Metashape or OpenDroneMap.

**Providers:**
- **Nayaka Aerial (nayakaaerial.com):** West Java; Sukabumi experience; Rp 2–15M for 5–50 ha. [Sukabumi drone](https://nayakaaerial.com/seputar-sewa-drone-murah-di-kabupaten-sukabumi/)
- **Geopasi Survey drone unit:** Combined drone + RTK GCP packages.
- **TechnoGIS Indonesia:** National aerial photography and LiDAR.

**Accuracy:** Without GCPs, 5–15 cm H / 10–30 cm V. With 4–6 RTK GCPs, 3–5 cm H / 5–10 cm V. Replaces above-water bank geometry but does **not** measure below water surface.

**Indonesian drone regulations (important):** Under Permenhub 37/2020, drones >250 g require registration and pilot competency certification for commercial operations. Operations in populated areas require DJPU safety assessment. Commercial operators already hold these permits — hiring a firm handles the regulatory burden. Do not attempt to fly your own unregistered drone commercially over a populated river bank.

#### Option E — Public Open Datasets

- **DEMNAS (BIG 8 m DEM):** vertical RMSE ~8 m. Cannot resolve channel geometry at river scale. Not useful for cross-section.
- **SRTM and ALOS PALSAR:** 30 m, worse. Not suitable.
- **Bing/Google/Maxar imagery:** planimetric accuracy 0.5–3 m. Useful only to sanity-check GCP planimetric positions (not off by metres).

**Conclusion:** Not a substitute for field survey at ORC operating scales.

#### Option F — University Partnership (ITB via LAPI GTC)

Contact PT LAPI GTC (+62-22-250-7463, [lapiganeshatama.co.id](https://www.lapiganeshatama.co.id/)).

**Timeline risk:** Internal project approval, formal proposal, MOU — even a small job can take 2–4 weeks. Fast-track only possible with an existing ITB contact.

**Cost:** Rp 5–15M for 1–2 day survey, roughly comparable to a private firm; value-add is technical quality (faculty-supervised deliverables).

#### Option G — Professional Benchmark Tie + DIY Detail Survey

Pay a surveyor to establish one or two permanent benchmarks (titik dasar) at each site, tied to SRGI2013 with elevation. You then extend measurements — cross-section, GCPs, staff gauge — using an optical/digital level by back-sighting from the benchmark.

**Accuracy:** Benchmark 2–5 cm RMSE. Level extension ±3–10 mm per setup. Tape/offset horizontal: ±2–5 cm per point over 20–30 m. Adequate for ORC.

**Cost:** Benchmark only: Rp 2–5M per half-day visit. Auto-level rental Rp 200–400k/day from the same firms as Option B.

**Limiting factor:** Your own measurement precision from the benchmark. If GCPs are internally consistent in a single reference frame and correctly scaled in metres, 3–5 cm H / 5–10 cm V from an auto-level is within ORC's tolerance.

---

### Decision Tree

```
What problem do you have with your existing data?
│
├─ GCPs collected with smartphone/consumer GNSS (>1 m)
│   AND raw RINEX available
│   └─ Option A first (InaCORS post-processing, free, 1–2 days)
│      If RINEX not available → Option B or C
│
├─ GCPs poor, no RINEX
│   ├─ Comfortable with RTK kit → Option B (Rp 3–5M, 2–4 days)
│   └─ Prefer to delegate → Option C (Rp 3–7M, 1–2 weeks)
│
├─ Cross-section geometrically wrong (shape inconsistent, depths implausible)
│   AND GCPs roughly right
│   ├─ Channel dry/shallow/accessible → Option B or G (re-measure)
│   └─ Channel deep/inaccessible by wading → Option D (drone + wading thalweg)
│
├─ Staff gauge datum uncertain only
│   └─ Option G: half-day benchmark tie (Rp 2–5M); re-level gauge zero yourself
│
├─ Everything suspect
│   ├─ Budget > Rp 10M, 2–3 weeks available → Option C + G
│   ├─ Budget Rp 5–10M, 1 week → Option B (re-measure everything yourself)
│   └─ Budget < Rp 5M, very short time → Option A first, then G; accept higher
│      ORC uncertainty; plan proper resurvey after trip
│
└─ GCPs fine, cross-section fine, but ORC outputs look wrong
    └─ Problem likely camera calibration or video quality, not survey.
       Check pyorc reprojection residuals first before re-surveying.
```

---

## Top 3 Recommended Actions Given You Are In-Country Now

**Action 1 — Send quote requests to three providers today.**
Contact Geopasi Survey, CV Tata Bumi Geosurvey, and Geoindo Survey (or TechnoGIS) in parallel via WhatsApp with a one-paragraph SOW: site location in Sukabumi, 4–6 GCPs per site, cross-section survey, staff gauge tie, RTK Fixed with InaCORS, output in UTM Zone 48S SRGI2013, delivery within 7 working days. Ask for fastest mobilization date and a price including PPN. Three quotes gives you price and availability within 24–48 hours without committing.

**Action 2 — Evaluate your existing data quality before committing to any resurvey.**
Spend one evening in QGIS or pyorc: (a) plot your GCPs against Bing satellite imagery — are they within ~2 m of where they should visually be? (b) load your cross-section — does thalweg depth match field observation? (c) compute pyorc's reprojection residuals from your existing camera configuration. If GCPs plot within 1–2 m and cross-section depths are plausible, the question shifts from "are my data usable at all" to "are they precise enough" — potentially addressed in post-processing (Option A) rather than a full re-survey.

**Action 3 — If equipment rental is your chosen path, contact MSDI or ADHIJASA today.**
Rental logistics from Jakarta/Bandung to Sukabumi typically require 1 business day for shipping or pickup. Specify "Emlid Reach RS2+ or equivalent multi-band L1/L2 RTK receiver with NTRIP capability" and confirm InaCORS NTRIP mount point availability in Sukabumi before field work.

---

## Sources

- [Geopasi Survey — Jasa Survey GPS Geodetik RTK](https://geopasi.com/jasa-survey-gps/)
- [TechnoGIS Indonesia — Contact and Services](https://www.technogis.co.id/contact/)
- [PT LAPI Ganeshatama Consulting (ITB commercial unit)](https://www.lapiganeshatama.co.id/)
- [CV Tata Bumi Geosurvey](https://tatabumigeosurvey.com/)
- [Geoindo Survey Services — Bandung](http://www.geoindo.com/)
- [Geo Survey Persada Indonesia](https://geosurveypersada.com/contact-us)
- [BIG InaCORS / SRGI service portal](https://srgi.big.go.id/page/service-check)
- [BIG InaCORS online post-processing service](https://srgi.big.go.id/page/online-post-processing)
- [Springer Applied Geomatics: Analysis of accuracy of InaCORS BIG post-processing service (2020)](https://link.springer.com/article/10.1007/s12518-020-00343-2)
- [ResearchGate: Reference System and Accuracy Evaluation of InaCORS RTK and Online Post-Processing Services](https://www.researchgate.net/publication/376872090_Reference_System_and_Accuracy_Evaluation_of_InaCORS_RTK_and_Online_Data_Processing_Services)
- [pyorc documentation — camera configuration and GCPs](https://localdevices.github.io/pyorc/user-guide/camera_config/index.html)
- [MSDI Indonesia — Emlid RS2 rental](https://www.msdi.co.id/services/rental-gnss-survey-instrument/emlid-reach-rs2-rsplus/)
- [CV BNT — sewa GPS RTK murah](https://totalstation.co.id/product/sewa-gps-rtk-geodetik-murah/)
- [CV ADHIJASA — rental GPS RTK GNSS geodetik](https://adhijasa.com/rental-gps-rtk-gnss-geodetik/)
- [DND Survey — rental sewa GPS RTK 2025](https://dndsurvey.id/rental-sewa-gps-rtk/)
- [Gita Survey — rental GPS geodetik](https://gitasurvey.com/rental-gps-geodetik/)
- [Nayaka Aerial — sewa drone Sukabumi](https://nayakaaerial.com/seputar-sewa-drone-murah-di-kabupaten-sukabumi/)
- [Terra Drone Indonesia — Regulasi PM 37/2020](https://terra-drone.co.id/regulasi-drone-pm-37-2020/)
- [DEMNAS national DEM portal — BIG Indonesia](https://tanahair.indonesia.go.id/demnas/)
- [ResearchGate: Vertical accuracy assessment DEMNAS vs SRTM-1 vs ASTER GDEM](https://www.researchgate.net/publication/377700715_VERTICAL_ACCURACY_ASSESSMENT_OF_VARIOUS_OPEN-SOURCE_DEM_DATA_DEMNAS_SRTM-1_AND_ASTER_GDEM)
- [ScienceDirect: Uncertainty in open-channel discharges measured with the velocity-area method](https://www.sciencedirect.com/science/article/abs/pii/S0955598612000489)
- [MDPI Water: Evaluation of Discharge Measurement Uncertainty of a Surface Image Velocimeter](https://www.mdpi.com/2073-4441/17/12/1722)
- [SW Maps documentation](https://aviyaantech.com/swmaps/)
- [pix-pro: GCP accuracy in photogrammetry](https://www.pix-pro.com/blog/ground-control-points-accuracy)
- [BNSP Juru Ukur (Surveyor) certification](https://lspkonstruksi.com/sertifikat-kompetensi-bnsp/juru-ukur-surveyor)
