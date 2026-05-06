# Indonesian Government Hydrometric Station Standards

**Purpose:** Feed into PMI/OpenRiverCam lessons-learned documentation.
**Date:** 2026-04-22
**Author:** Research compiled for ORC field deployment, Sukabumi / West Java.

---

## Executive Summary

- River stage and discharge monitoring in Indonesia is the responsibility of **Kementerian PUPR / Ditjen SDA** through its 34 BBWS/BWS river-basin offices. BMKG's mandate is atmosphere and rainfall, not river discharge; BMKG stations do not produce rated discharge records.
- Automatic water level stations (called **AWLR** or **pos duga air telemetri**) form a national network reported through the SIHLSDA and SIHKA portals. Sensors cover three main principles: vented pressure transducer, float/shaft encoder, and non-contact (radar or ultrasonic).
- The dominant international brands procured by BBWS offices are **OTT HydroMet** (pressure probes, bubbler, radar, netDL data logger) and to a lesser extent **Seba Hydrometrie**. Domestic assemblers — **Mertani**, **IDDATA (PT. Indonesia Data)**, and **PT. Tatonas** — supply a growing share of government tenders, especially for radar-based units.
- Discharge is derived almost entirely from **stage-discharge rating curves** (lengkung debit / kurva debit). Periodic current-meter gaugings (3–5 per year per station) maintain those curves; both propeller current meters and **SonTek FlowTracker / RiverSurveyor M9 ADCP** are in active use.
- The binding Indonesian standard is **SNI 8066:2015** (discharge measurement, current meter). The foundational method standard is **SNI 03-2414-1991** (river discharge / open channel). **WMO-No. 168** (Guide to Hydrological Practices) is the acknowledged international baseline.

---

## 1. Institutional Responsibility — Who Does What

| Agency | Role | River Hydrology? |
|---|---|---|
| **Kementerian PUPR / Ditjen SDA** | National water resources policy and investment | Yes — primary authority |
| **BBWS / BWS** (34 offices, e.g. BBWS Citarum, BBWS Bengawan Solo, BWS Sumatera I) | Operational station network, data collection, rating curves | Yes — executes field program |
| **PUSAIR** (Bandung) | R&D, equipment calibration laboratory (KAN-accredited, LK-127-IDN), standards development | Yes — technical backstop |
| **BMKG** | Meteorology, climatology, geophysics; operates rainfall and climate stations | **No** — BMKG does not produce river discharge records. Some BBWS information portals ingest BMKG rainfall data alongside BBWS water-level data (e.g., SIH3 portals), but the water-level and discharge measurements at *pos duga air* are owned by BBWS/BWS, not BMKG. |
| **Dinas PUPR** (provincial/kabupaten) | Smaller irrigation canals and local rivers | Partial — variable by region |

**BMKG finding confirmed:** BMKG's station network (Stasiun Klimatologi, Geofisika, and Meteorologi) measures rainfall, temperature, humidity, and similar atmospheric variables. River stage and discharge gaugings are outside its statutory mandate. No public evidence was found that BMKG operates rated river discharge stations.

[[BBWS Bengawan Solo SIHKA portal]](https://hidrologi.bbws-bsolo.net/)
[[SIHLSDA — Ditjen SDA national telemetry portal]](http://sihlsda.sda.pu.go.id/)
[[PUSAIR Balai Hidrologi dan Tata Air]](https://pusair-pu.go.id/page/balai-hidrologi-dan-tata-air)
[[BBWS Ciliwung Cisadane — 37 pos duga air, 16 rivers]](https://pu.go.id/berita/37-pos-duga-air-milik-bbwscc-pantau-tinggi-muka-air-di-16-sungai)

---

## 2. Water Level Measurement — Automatic (AWLR)

### 2.1 Terminology

The Indonesian field term for an automatic recording water-level station is **AWLR** (Alat/Automatic Water Level Recorder), sometimes **AWLL** (Alat Pengukur Level/Liquid). The station site is called a **pos duga air** (water-gauge post). The national telemetry data system is **SIHLSDA** / **SIH3** / **SIHKA** depending on the BBWS region.

### 2.2 Measurement Principles and Brands

Three sensor principles are found in BBWS deployments. Evidence is strongest for the first two.

**A. Vented pressure transducer (submersible)**
The most common automatic sensor type. A ceramic pressure cell is installed below minimum water level; the vented cable compensates for barometric fluctuation.

- **OTT PLS / OTT PLS 500** — German, Kempten. Ceramic pressure cell, SDI-12 / RS-485 output. One of the most widely named instruments in Indonesian distributor catalogs and PUSAIR evaluation literature. PUSAIR's KAN-accredited calibration lab (range 0–300 cm) explicitly supports pressure-type AWLR, consistent with OTT PLS usage.
- **OTT PS 1** — Older OTT pressure/tidal sensor; cited in Indonesian research on tidal-station performance (Binuangeun estuary, Banten province).
- **Seba Hydrometrie** (Germany, now Xylem brand family) — Named alongside OTT in procurement-related literature and distributor sites; specific model families used by BBWS are unconfirmed from public sources.
- **Schlumberger/van Essen Mini-Diver / Diver** — Referenced in the broader regional market context but not confirmed in Indonesian government tenders from public search results.
- **Keller** pressure sensors — available through Indonesian distributors; not yet confirmed in BBWS procurement records.

[[OTT PLS product page]](https://www.ott.com/products/water-level-1/ott-pls-pressure-level-sensor-959/)
[[PUSAIR AWLR calibration service — SITU portal]](https://situ.pusair-pu.go.id/shop/product/kalibrasi-awlr-alat-ukur-tinggi-muka-air-sungai-89?category=2)
[[PUSAIR evaluation paper — Jurnal Teknik Hidraulik]](https://jurnalth.pusair-pu.go.id/index.php/JTH/article/view/585)

**B. Non-contact radar / ultrasonic**
Increasingly procured for new or replacement stations because they avoid sediment fouling and require no desiccant maintenance.

- **OTT RLS** (Radar Level Sensor) — German, 24 GHz FMCW radar; available through Indonesian distributors and referenced in PUSAIR comparison tests (labeled "Kalesto" in some older OTT product families, now OTT RLS).
- **IDDATA RL03 / IDAS RLO3** — Domestic radar-based AWLR unit listed on INAPROC government catalog. Listed price: **Rp 58,000,000 (approx. USD 3,600)** ex-VAT; total with 12% PPN Rp 64,960,000. Includes GSM telemetry. Represents a cost-competitive domestic alternative.
- **Mertani AWLR** — Indonesian IoT-oriented manufacturer; supplies radar and ultrasonic variants. Reported in use by DLH offices and BBWS units, with real-time cloud dashboard. No public unit price found in this search.
- **PT. Tatonas** — Indonesian systems integrator; documented projects at BBWS Pemali Juana including ultrasonic AWLR (±3 mm accuracy claimed) and float/encoder (ARL) telemetry units.

[[IDDATA RL03 on INAPROC catalog]](https://katalog.inaproc.id/iddata-indonesia-data/awlr-automatic-water-level-recorder-pemantau-ketinggian-air-telemetri-radar-rl03-iddata)
[[Mertani AWLR product page]](https://www.mertani.co.id/automatic-water-level-recorder)
[[PT. Tatonas — AWLR ultrasonic project BBWS Pemali Juana]](https://web.tatonas.co.id/proyek/pemasangan-awll-ultrasonik-telemetri-di-bbws-pemali-juana)
[[PT. Tatonas — ARL telemetri project BBWS Pemali Juana]](https://web.tatonas.co.id/proyek/pemasangan-arl-telemetri-dan-ombrometer-di-bbws-pemali-juana)

**C. Float and shaft encoder**
Historically the primary AWLR type (mechanical float in stilling well, connected to a rotating drum recorder or digital shaft encoder). Still in service at older stations; being replaced by electronic sensors in new procurement.

- **OTT Thalimedes** (shaft encoder, SDI-12) — available via Indonesian distributors; used in mixed-sensor networks alongside pressure probes.
- Generic float / rotary encoder units by Tatonas and others — cited at BBWS Pemali Juana.

**D. Bubbler (gas purge)**
- **OTT CBS** (Compact Bubbler Sensor) — available through the regional market; preferred where sediment-laden rivers make submersible sensors impractical. No confirmed large-scale Indonesian BBWS deployment found in public records.

### 2.3 Data Logger and Telemetry Platform

- **OTT netDL 500 / netDL 1000** — the dominant professional logger found in BBWS networks, with built-in GSM/GPRS modem, SDI-12, RS-485 (Modbus), and analogue inputs. Configures to transmit at user-set intervals to SIHLSDA/SIH3 servers.
- **Campbell Scientific CR300 / CR1000** — present in the regional market and cited in technical literature; usage in Indonesian BBWS appears secondary to OTT netDL based on available sources.
- Domestic GSM telemetry units (Higertech, Tatonas) — often paired with domestic sensors for lower-cost deployments.

[[OTT netDL data logger]](https://www.ott.com/products/data-logging-and-telemetry-4/ott-netdl-data-logger-972/)

---

## 3. Water Level Measurement — Manual (Staff Gauge / Papan Duga Air)

### 3.1 Equipment Standard

The manual staff gauge is called **papan duga air** or **peilschaal** in Indonesian government documents. Standard characteristics from PUPR/BBWS technical training materials:

- Material: enameled steel or fiberglass board with embossed centimeter graduations.
- Scale unit: **centimeters**, resolution 1 cm; readings to nearest whole centimeter.
- Mounting: bolted to a concrete wing-wall or steel pipe at the river bank, with the zero referenced to a local benchmark (patok tetap).
- Range: sufficient boards to cover the full range from minimum to maximum recorded stage.

### 3.2 Observation Protocol

Standard observation cadence at manual pos duga air: **three readings per day at 07:00, 12:00, and 17:00 WIB/WITA/WIT** local time. An additional 06:00 reading is required at some priority stations. Data are recorded on printed forms (formulir) and submitted to the relevant BBWS unit.

Observers (called **juru pengamat** or **pengamat hidrologi**) are typically local community members contracted by BBWS. Selection criteria include literacy, honesty, and proximity to the station. Observer-based manual reading remains common for stations outside reliable GSM coverage or where AWLR installation budget is unavailable.

[[Standard TMA observation protocol — BBWS Sumatera I article]](https://sda.pu.go.id/balai/bwssumatera1/article/proses-pengambilan-data-lengkung-debit)
[[PUPR training module — Pengenalan Analisis Hidrologi (sibangkoman.pu.go.id)]](https://sibangkoman.pu.go.id/center/pelatihan/uploads/edok/2023/11/1e5ee_Bahan_Tayang_8_Pengenalan_Analisis_Hidrologi.pdf)

---

## 4. Water Discharge / Flow Measurement

### 4.1 Primary Method: Stage-Discharge Rating Curve

Indonesian BBWS offices do not operate continuous-discharge instruments at most stations. The standard practice is:

1. Maintain a water-level record (AWLR or manual papan duga air) at the pos duga air.
2. Conduct periodic **current-meter gaugings** to measure instantaneous discharge at a cross-section.
3. Fit a **lengkung debit** (rating curve / liku kalibrasi debit) relating stage (H) to discharge (Q), using a minimum of **30 data points** spanning low to flood stage.
4. Apply the rating curve to the continuous stage record to produce the discharge time series.

Gaugings are conducted **3–5 times per year per station** under typical conditions (BWS Sumatera I practice, confirmed in published article). At high stages (depth > ~1 m from low-flow cross-section) boat-based measurement is standard; above approximately 3 m depth or in extreme flood conditions, current-meter measurement may not be feasible.

### 4.2 Instruments for Discharge Gaugings

**Propeller current meter (alat ukur arus baling-baling):**
The traditional reference instrument. Used for mid-section / mean-section method per SNI 03-2414-1991. Specific models confirmed in Indonesian literature and distributor catalogs:
- **OTT C31** — propeller type, widely cited in Indonesian university teaching materials and distributor listings. Training for BBWS Pemali Juana staff included current-meter use.
- **OTT MF Pro** — electromagnetic current meter (no moving parts); available from PT. Majuma Mandiri (OTT distributor) and other Indonesian agents.
- Generic propeller current meters at lower cost levels also in use.

[[OTT MF Pro at PT. Majuma Mandiri Indonesia]](http://www.majumapanmandiri.co.id/index.php?product_id=4140&route=product%2Fproduct)

**Acoustic Doppler instruments:**
Increasingly adopted for speed and flood-stage capability.
- **SonTek FlowTracker 2** (handheld ADV) — wading / bridge-mounted; cited in Indonesian training materials and Xylem Indonesia's local product page. Suitable for shallow, accessible cross-sections.
- **SonTek RiverSurveyor M9 ADCP** — boat-mounted, multi-frequency; available through Xylem Indonesia. ADCP surveys reduce field time and allow measurement at stages previously inaccessible to current meters.
- **SonTek Argonaut-XR** — fixed side-looking acoustic (H-ADCP) for continuous index-velocity deployment; documented use in Indonesian coastal/estuarine contexts.

[[SonTek RiverSurveyor M9 — Xylem Indonesia]](https://www.xylem.com/en-id/products--services/analytical-instruments-and-equipment/data-collection-mapping-profiling-survey-systems/acoustic-doppler-profilers-adpadcp/riversurveyor/)
[[Geochem Survey — ADCP survey services Indonesia]](https://geochemsurvey.com/jasa-survey-adcp-sungai/)
[[SonTek — Xylem Indonesia brand page]](https://www.xylem.com/en-id/brands/sontek/)

**Continuous-discharge instruments:**
There is no public evidence of widespread H-ADCP or hydroacoustic index-velocity systems at BBWS stations beyond research or pilot contexts. The rating-curve method dominates operational practice.

### 4.3 Rating Curve Development Standard

Per BBWS Sumatera I published guidance and university hydrology teaching modules:
- Minimum 30 Q-H pairs required.
- Curve fitted as power-law (Q = a(H – H₀)^b) or segmented polynomial.
- Annual or biennial review when stage-discharge relationship may have shifted (channel morphology change, vegetation).
- PUSAIR's Jurnal Teknik Hidraulik publishes peer-reviewed rating-curve studies for Indonesian rivers (e.g., Sungai Martapura, Sungai Temef).

[[BWS Sumatera I — lengkung debit process article]](https://sda.pu.go.id/balai/bwssumatera1/article/proses-pengambilan-data-lengkung-debit)
[[Rating curve study — ResearchGate / Sungai Martapura]](https://www.researchgate.net/publication/369537236_Analisis_Kurva_Lengkung_Debit_Sungai_Martapura_pada_Pos_Duga_Air_Gudang_Tengah_Kecamatan_Sungai_Tabuk_Kabupaten_Banjar_Provinsi_Kalimantan_Selatan)

---

## 5. Standards and Specifications Documents

| Code / Document | Full Title | Scope |
|---|---|---|
| **SNI 03-2414-1991** (partially superseded by SNI 8066:2015) | Tata Cara Pengukuran Debit Aliran Sungai dan Saluran Terbuka Menggunakan Alat Ukur Arus dan Pelampung | River discharge measurement using current meter and float; site selection; non-tidal rivers |
| **SNI 8066:2015** | Tata cara pengukuran debit aliran sungai dan saluran terbuka menggunakan alat ukur arus | Updated current-meter discharge method; developed by BSN Technical Committee 91-01-S1 (Water Resources / Hydrology Working Group) |
| **WMO-No. 168** | Guide to Hydrological Practices (6th ed.) | International baseline; explicitly referenced in Indonesian university hydrology teaching and PUSAIR publications |
| **PUSAIR Pedoman Teknis** | Internal PUPR technical manuals for AWLR station construction, survey procedures for pos duga air site selection | Not fully public; referenced in BBWS training materials |
| **PP No. 38 Tahun 2011** | Government Regulation on Rivers | Legal basis for hydrometric monitoring obligations |

[[SNI 8066:2015 — BSN catalog page]](https://pesta.bsn.go.id/produk/detail/9873-sni80662015)
[[SNI 03-2414-1991 — Scribd scan]](https://www.scribd.com/document/580135182/SNI-03-2414-1991-Rev-2004-Tata-cara-pengukuran-debit-aliran-sungai)
[[WMO-No. 168 Vol. I — WMO Library]](https://library.wmo.int/viewer/35804?medianame=168_Vol_I_en_1_)

---

## 6. Procurement Landscape

### 6.1 International Brands with Confirmed Indonesian Market Presence

| Brand | Products | Indonesian Presence |
|---|---|---|
| **OTT HydroMet** (Germany / Hach-Xylem group) | PLS / PLS 500 pressure probe, RLS radar, CBS bubbler, Thalimedes shaft encoder, netDL data logger, C31 / MF Pro current meters | Confirmed via distributor catalog (PT. Majuma Mandiri), PUSAIR evaluation literature, dataloggerindonesia.com, testindo.co.id |
| **SonTek** (USA / Xylem) | FlowTracker 2, RiverSurveyor M9 ADCP, Argonaut-XR | Confirmed via Xylem Indonesia country site |
| **Seba Hydrometrie** (Germany / Xylem) | Water-level sensors | Named alongside OTT in distributor literature; specific BBWS deployment unconfirmed from public sources |
| **Campbell Scientific** (USA) | CR300/CR1000 data loggers | Present in market; secondary to OTT netDL for BBWS work based on available sources |

### 6.2 Domestic / Assembled Brands

| Brand / Vendor | Product | INAPROC/LKPP listed? | Notes |
|---|---|---|---|
| **IDDATA (PT. Indonesia Data)** | AWLR RL03 radar unit | Yes — INAPROC | Rp 58 M (~USD 3,600) ex-VAT; GSM telemetry included |
| **Mertani** | AWLR radar and ultrasonic | Unconfirmed from this search | Used by DLH and BBWS units; real-time cloud dashboard |
| **PT. Tatonas** | AWLL ultrasonic, ARL float encoder telemetry | Partial — project references | Documented BBWS Pemali Juana installations |
| **Higertech (PT. Higertech Karya Sinergi)** | Telemetry platform for BBWS Citarum | Indirect — system integrator | Operates the BBWS Citarum real-time monitoring web platform |
| **PT. Rismasen** | AWLR telemetry systems (Banten) | Via Indonetwork | Reseller/integrator, not manufacturer |

Procurement for government use goes through **INAPROC / e-katalog LKPP** for catalogued items, or through tender (LPSE) for larger installations. Domestic-content (TKDN) policy under Indonesian procurement rules increasingly favors domestically assembled units.

[[INAPROC — IDDATA AWLR RL03]](https://katalog.inaproc.id/iddata-indonesia-data/awlr-automatic-water-level-recorder-pemantau-ketinggian-air-telemetri-radar-rl03-iddata)
[[INAPROC — Tatonas pressure AWLR with pos structure]](https://katalog.inaproc.id/tatonas/automatic-water-level-recorder-sensor-pressure-with-router-gsm-telemetry-50-meter-awlr-dengan-kelengkapan-pos)

---

## 7. Gaps and Unconfirmed Items

The following items were researched but not verified from public sources:

- **Exact OTT / Seba model procurement records** for specific BBWS offices — likely documented in internal BBWS annual reports (LAKIP) not publicly accessible online.
- **Van Essen Mini-Diver / Schlumberger Diver** in Indonesian government use — referenced as typical in the regional market context but not confirmed in Indonesian government tender records found in this search.
- **H-ADCP or SonTek Argonaut-XR deployments in rivers** (as opposed to estuaries or coastal channels) by BBWS — not confirmed in public records; research context only.
- **PUSAIR Pedoman Teknis full text** for AWLR station construction — referenced but not publicly available online.
- **Specific price data for OTT PLS / netDL in Indonesian government tenders** — not found in public records.

---

## 8. Recommended Target Standard for Our Device

To be interchangeable with the existing Indonesian hydrometric record, a low-cost ORC station must satisfy the following:

**Stage (water level) output:**
- Units: **meters above local datum**, referenced to the same peilschaal (papan duga air) zero that BBWS uses at the site. Resolution must be ≤ 1 cm (0.01 m) to match manual observer precision; target ≤ 5 mm.
- Timestep: report at **minimum 15-minute intervals**; 5-minute preferred for flood early-warning compatibility with SIH3 / SIHLSDA ingest.
- Sensor principle: any (pressure, radar, or ultrasonic are all used by BBWS), but the value must be referenced to the same local datum as the papan duga air at the co-located pos duga air.
- Calibration: must be verifiable against PUSAIR KAN-accredited calibration (range 0–300 cm for pressure type). The PUSAIR lab accepts pressure-transducer-type AWLR for calibration.

**Discharge output:**
- ORC stations do not replace periodic current-meter gaugings; they provide continuous video-derived surface velocity, which is converted to Q via the standard ORC rating approach or by index-velocity rating.
- To be accepted alongside BBWS data, the Q time series should be expressed in **m³/s**, and uncertainty should be documented following SNI 8066:2015 principles (or WMO-No. 168 Chapter 5 for velocity-area method).

**Data format and telemetry:**
- SIHLSDA/SIH3 ingest uses standard hydromet formats (typically CSV or simple HTTP POST with TMA value, timestamp, station ID).
- GSM/GPRS transmission at regular intervals is the operational expectation; satellite not required for Java/Sumatra coverage.

**Documentation for acceptance:**
- Site report must include: station coordinates, local benchmark reference, peilschaal zero elevation, sensor installation height, and calibration record.
- Calibration against co-located BBWS papan duga air is the minimum field validation check before data are submitted to BBWS.

---

*Sources consulted include: sda.pu.go.id, pusair-pu.go.id, jurnalth.pusair-pu.go.id, katalog.inaproc.go.id, bsn.go.id, ott.com, xylem.com/en-id, mertani.co.id, tatonas.co.id, testindo.co.id, library.wmo.int, researchgate.net (Indonesian hydrology papers), and sih3.dpuair.jatimprov.go.id.*
