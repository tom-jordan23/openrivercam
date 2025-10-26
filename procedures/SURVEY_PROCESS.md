# SURVEY_PROCESS.md
One-Day River Survey SOP (Points-Only) — **ArduSimple + Android + GNSS Master → SW Maps**  
**CRS:** UTM Zone 48 South (**EPSG:32748**) • **Heights in field:** Ellipsoidal (meters)  
**Goal:** Collect high-quality points for cross-sections and bank/control features with **centimeter-level relative accuracy** and **~0.25–0.5 m global alignment** to imagery via PPP translation.

---

## 1) Plain-English Glossary
- **GNSS** — Satellite positioning (GPS, GLONASS, Galileo, BeiDou).  
- **RTK** — Real-time corrections from a nearby **base** to the mobile **rover** → cm-level **relative** accuracy.  
- **FIX / FLOAT** — RTK status; **FIX** = precise (use it), **FLOAT** = not fully locked (avoid).  
- **PDOP** — Satellite geometry quality; **lower is better** (≤2.5 good).  
- **RTCM** — Correction messages the base broadcasts to the rover.  
- **RINEX** — Raw GNSS log format used for **PPP** later.  
- **PPP (Precise Point Positioning)** — Post-processing that refines the **base coordinate** using precise orbits/clocks → precise global tie.  
- **ARP (Antenna Reference Point)** — The physical reference on the antenna you measure to (usually the **bottom face** where it seats).  
- **Ellipsoidal height** — Height above the Earth ellipsoid (record this in the field).  
- **Orthometric height** — “Sea-level height” (convert later with a geoid if needed).  
- **Mock location (Android)** — Lets GNSS Master feed the rover’s position to apps as if it were the phone’s GPS.

---

## 2) Crew Defaults (memorize these)
**What:** Minimum quality conditions before saving any point.  
**Why:** Enforces consistency and keeps the dataset at cm-level relative precision.

- RTK **FIX** for ≥ **10 s**  
- **PDOP ≤ 2.5** (≤2.0 ideal)  
- **Satellites ≥ 12**  
- **Correction age ≤ 2 s**  
- SW Maps precision **σ ≤ 2 cm H**, **≤ 3–4 cm V**  
- **Pole bubble centered** (use a bipod)

**Averaging window per point**  
- **20 s** — open sky  
- **60 s** — near water/trees/structures  
- **120–180 s** — under bridges/heavy canopy

**Bed elevation (computed later in QGIS):**  
```
bed_Z = Z_ellipsoid_shifted − pole_h_m
```
(Where `Z_ellipsoid_shifted` is your ellipsoidal Z after PPP ΔZ; `pole_h_m` is tip→ARP per shot.)

---

## 3) Night-Before Prep (5–10 min)
**What:** Prepare hardware, phone, and app settings; predefine attributes.  
**Why:** Saves time in the field and ensures attributes match the QGIS workflow.

1) Charge base, rover, radios, phone; pack bipod, steel tape/laser, notebook.  
2) Android → Enable **Developer Options** → **Select mock location app = GNSS Master**.  
3) SW Maps → set project CRS to **UTM 48S (EPSG:32748)**; verify units are **meters**.  
4) Prepare SW Maps **point attributes** (you’ll create them in §6.1).  
   - `station`, `avg_s`,   
     `pole_h_m`, `offset_m`, `offset_bearing_deg`, `offset_to`, `notes`.

---

## 4) Base Setup for Clean Basemap Alignment (0.25–0.5 m target)
**What:** Lock a stable local frame and log raw data to refine global position via PPP.  
**Why:** RTK provides cm-level **relative** accuracy; PPP later fixes **absolute** placement.

### 4.1 Site & mark
Open sky, away from water/metal/wires. Level tripod and **mark the ground** (paint/tack).

### 4.2 Measure antenna height to **ARP**
Vertical ground→ARP to the **mm**. Measure twice; record the mean.

### 4.3 Survey-in (freezes your local frame)
Run **“Here + Average” for 5 minutes**. Record the base **Easting/Northing/Height** in **EPSG:32748**. **Do not move** afterward.

### 4.4 Start raw logging for PPP (RINEX target 6–12 h)
Start base logging at **1 Hz** and keep it running all day (see §4.5/4.6).

**Rule-of-thumb absolute tie (horizontal; vertical often ~2× worse):**

| Base method | Typical absolute bias (H) | Use when… |
|---|---|---|
| 5 min survey-in | ~2–4 m | Local frame only (PPP later will fix) |
| 30–60 min survey-in | ~0.8–1.5 m | No PPP later (fallback) |
| **6–12 h RINEX → PPP** | **~0.1–0.4 m (H)**, ~0.2–0.4 m (V) | **Recommended** for OSM/satellite alignment |

### 4.5 RINEX logging — how to start and capture (choose ONE route)
Your goal is a continuous **6–12 hour** base log. Pick your tool.

**Route A — ArduSimple microSD Datalogger**  
1. Insert **FAT32** microSD (≥8 GB) into the ArduSimple datalogger.  
2. Power base; verify LOG LED. Leave running all day.  
3. Power down; copy **RINEX/raw** files. Record antenna height + UTC times.

**Route B — Windows laptop with u‑center (UBX → RINEX)**  
1. USB-connect base F9P; open **u‑center** (COM/baud).  
2. Enable raw: **UBX‑RXM‑RAWX/SFRBX** at **1 Hz** on **USB**.  
3. **File → Log → Start (UBX)** for **6–12 h**; **Stop**; **Tools → Convert to RINEX**.

**Route C — RTKLIB (Windows/Linux/Raspberry Pi)**  
1. Log **UBX** at **1 Hz** with **str2str/STRSVR** to a file all day.  
2. Convert with **convbin** to RINEX. Save antenna height + UTC times.

**Data hygiene**: keep **UTC**, record base E/N/Z, **ARP height**, start/stop, receiver/antenna models. Back up twice.

### 4.6 Configure the base in **u‑center** (ArduSimple F9P) — step‑by‑step
> **Goal:** Make the F9P act as a **base** that (a) runs **Survey‑In**, (b) **broadcasts RTCM3** on the radio port, and (c) **exposes raw** at 1 Hz for logging.

**Prereqs**  
- Connect F9P via **USB**; note the COM port. Launch **u‑center**.

**A) Connect & sanity**  
1. **Receiver ► Connection ► COMxx** (115200 or your configured rate).  
2. Open **Packet Console (F8)** and **Messages (F9)**. You should see **NAV‑PVT** updating at 1 Hz.

**B) Set Survey‑In (TMODE3)**  
1. **UBX‑CFG‑TMODE3** → **Mode = Survey‑in**.  
2. **Minimum Observation Time (s)** = **300** (5 min) or **1800–3600** for longer.  
3. **Required Position Accuracy (m)** = **2.0** (typical; lower makes it run longer).  
4. **Send**.

**C) RTCM3 out on radio port (UART2)**  

**Note:** If you purchase the base and rover as a kit from Ardusimple, this step will be done at the factory. You will only need to do this step if you purchased the base and rover separately.

1. **UBX‑CFG‑PRT** → **Target: UART2**, **Baud = 115200**, **Protocol out = RTCM3** → **Send**.  
2. **UBX‑CFG‑MSG** (on **UART2**) enable at ~1 Hz: **RTCM 1005** (ARP), **1077** (GPS MSM7), **1087** (GLONASS MSM7), **1097** (Galileo MSM7), **1127** (BeiDou MSM7). Also **1230** at 0.2–1 Hz. (Trim constellations if bandwidth is tight.)

**D) Raw on USB (for logging)**  
1. **UBX‑CFG‑PRT** → **Target: USB**, **Protocol out = UBX+NMEA** → **Send**.  
2. **UBX‑CFG‑MSG** (on **USB**): enable **UBX‑RXM‑RAWX** and **UBX‑RXM‑SFRBX** at **1 Hz**. (Optional: **NAV‑PVT**, **NAV‑HPPOSLLH** at 1 Hz.)

**E) Save to flash**  
- **UBX‑CFG‑CFG** (or **VALSET/Configuration** on newer): **Save current configuration** to **Flash/BBR** → **Send** (watch for ACK).

**F) Monitor Survey‑In**  
- **UBX‑NAV‑SVIN**: confirm **active = true**, watch **obsTime** and **position accuracy**. When it completes, the base holds a fixed averaged position.

**G) Start logging in u‑center (if using laptop)**  
- **File ► Log ► Start (UBX)** at 1 Hz; **Stop** when done; **Tools ► Convert to RINEX**. Archive with ARP height + UTC times.

**Quick checks**  
- Rover not getting **FIX**? Check **UART2 baud**, **RTCM3 on UART2**, radio link, and that **Survey‑In** finished.  
- No raw data? Ensure **RAWX/SFRBX** are enabled on **USB** and you’re logging **UBX** (not NMEA).

---

## 5) Rover → Android (mock location)
**What:** Connect rover to phone; GNSS Master feeds precise positions to apps.  
**Why:** SW Maps reads the rover as the phone GPS—simple and robust.

1) Pair Android **Bluetooth** with the **rover**.  
2) Open **GNSS Master** → Receiver: **Bluetooth** → select rover; verify live sats/PDOP/status.  
3) Toggle **Mock Location ON**.  
4) Wait for **RTK FIX** and stable PDOP/sats.

---

## 6) SW Maps Project (Points-Only)
**What:** Create a **UTM 48S** project and a point layer with averaging-by-time.  
**Why:** Working natively in **meters** avoids mistakes when applying translations and computing elevations.

1) **New Project** → **Coordinate System:** **WGS 84 / UTM zone 48S (EPSG:32748)**.  
2) **GPS Source:** **Device internal GPS** (uses the GNSS Master mock). SW Maps converts incoming lat/lon to UTM on the fly.  
3) **Heights:** Ellipsoidal (meters). Ensure **Use orthometric/geoid height** is **OFF**.  
4) **Point collection:** Averaging **by time**; enter **20/60/120–180 s** per point.
5) **Set Pole Height:** In GNSS dialog, set instrument height to the length of the survey pole.

### Why meters (UTM) for calculations
- **What:** Keep the whole project in a **projected CRS (UTM)** so all offsets and translations are in **meters**.  
- **Why:** Degrees aren’t constant distances; UTM prevents scale/sign errors when you apply ΔE/ΔN.

### 6.1 Create the point attributes (step-by-step)
1. **Menu (☰) ► Layers** → tap your **Point** layer.  
2. **Fields / Attributes** → **Add Field**:  
   - `station` — **Integer** (LB=0 → 1,2,… → RB=last)  
   - `avg_s` — **Integer** (default 60)  
   - `offset_m` — **Decimal (2)** (default 0.00)  
   - `offset_bearing_deg` — **Decimal (1)** (0–360; default 0.0)  
   - `offset_to` — **Text**
   - `notes` — **Text (multiline)**  
3. **Averaging:** **Settings ► Data Capture ► GPS Averaging ► By Time**.  
4. **Live stats:** enable **PDOP / Sats / Accuracy** on capture screen.

---

## 7) Create a Check Point (CP)
**What:** Measure the same nearby mark at start/mid/end.  
**Why:** Proves day stability without external control.

1) Pick open-sky spot 20–50 m from base; **mark it**.  
2) Pole plumb (bipod); confirm **quality gate**.  
3) Record **CP_START** with **60 s** averaging; fill attributes.  
4) Re-occupy at **midday** and **end-of-day** (targets: **≤2 cm H**, **≤3–4 cm V** vs CP_START).

---

## 8) Collecting Points (banks/controls/features)
**What:** Capture with averaging and use offsets near water.  
**Why:** Offsets reduce multipath; averaging reduces random noise.

Per point
1) Pole plumb; verify **FIX** and **quality gate**.  
2) Averaging: **20 s** (open) • **60 s** (near water/trees) • **120–180 s** (bridges/heavy canopy).  
3) If offsetting: set `offset_m`, `offset_bearing_deg`, `offset_to="water_edge"` (or relevant).  
4) Save with clear `station`, and notes.  
5) Tricky spots: take a **second occupation** ≥20–30 min later (60 s). Accept if within **≤2 cm H / ≤3 cm V**.

---

## 9) River Cross-Section by Pole (points-only)
**What:** Walk LB→RB, logging bed stations and pole heights at each stop. **Do this two times:** once for a discharge cross section and again for a water level cross section.
**Why:** Produces bed profile geometry for hydraulics.

Planning: pick a straight reach. Define `sect_id` (e.g., `XS_01`). Mark **LB**/**RB** on firm ground. Choose safe station spacing (e.g., 1–2 m).

Steps
1) **LB:** stand 2–3 m back; collect **60 s**. Offset to water edge if needed.
2) **Across channel:** at each station: plant **pole tip on bed**, keep bubble centered; verify **FIX**; average **60–120 s** (or **120–180 s** under bridges); record `station` 1,2,3…  
4) **Water Level:** Create a separate SWMaps layer to capture the water level at the time of the survey. The water level must be in the same coordinate system as the rest of the survey. If you are using a survey pole, you must read the water level manually and then add it to the UTM altitude you get from collecting this point.

---

## 10) Midday & End-of-Day QA
**What:** Re-check CP and review outliers before packing up.  
**Why:** Catches drift/mistakes early so you can re-shoot on site.

- **Midday:** re-occupy **CP** (60 s). Target **≤2 cm H / ≤3–4 cm V**. If worse: re-level, move from metal/vehicles, check base/radio, extend averaging.  
- **End-of-day:** re-occupy **CP_END** (60 s).  
- Export SW Maps **points** (CSV/GeoJSON/SHZ).  
- Turn **Mock Location OFF**; power down rover/base.  
- Stop base **RINEX** last. Photograph base, CP, and context.

---

## 11) After the Field — QGIS Steps (PPP Translation + Bed Z)
**What & Why:** Use the base’s PPP solution to get a precise global position, compute a **meter-based** translation (ΔE, ΔN, ΔZ) between the **field base** and the **PPP base**, and apply that translation to **all survey points**. Then subtract **pole height** to get **bed elevations**. Keeping the project in **UTM** means all steps are in **meters** end-to-end.

### 11.1 PPP the base — get a precise base coordinate
- **What:** Run **PPP** on the base’s **RINEX (6–12 h)** to obtain a precise **Lat/Lon/Z (ellipsoidal)** for the base.  
- **Why:** Short survey-in has meter-level bias; PPP removes clock/orbit/ionosphere biases → solid global tie.  
- **Keep:** `Lat_ppp, Lon_ppp, Z_ppp`, antenna ARP height, PPP frame/epoch, uncertainties.

### 11.2 Bring base points into UTM and compute ΔE/ΔN/ΔZ
- **What:** Create two base points: **Field base** (from the 5‑min survey‑in) and **PPP base**. If they arrive as lat/lon, import as **WGS84** and then **Save As → EPSG:32748**. Read **Easting (E)**, **Northing (N)**, and Z to compute:  
  - **ΔE = E_ppp − E_field**  
  - **ΔN = N_ppp − N_field**  
  - **ΔZ = Z_ppp − Z_field**  
- **Why:** Same projected CRS ensures a clean **meter** translation.

**Steps:**  
1) Add `Field_Base` and `PPP_Base` layers.  
2) Ensure both are **EPSG:32748**.  
3) Use **Identify** or add `$x`, `$y` to extract E/N; note Z values; compute ΔE/ΔN/ΔZ.

### 11.3 Shift all survey points in UTM
- **What:** Apply **ΔE/ΔN** to the survey to create `Survey_UTM_shifted`; add **ΔZ** to Z.  
- **Why:** Fixes absolute placement without changing relative geometry.

**Steps:**  
1) Ensure your survey layer is **EPSG:32748**.  
2) **Vector ► Geoprocessing ► Translate (Move, shift)** → Input = survey layer → **Offset X = ΔE**, **Offset Y = ΔN** → Output = `Survey_UTM_shifted`.  
3) If Z is an attribute (e.g., `Z_ellipsoid`): Field Calculator → `Z_ellipsoid_shifted = "Z_ellipsoid" + <DeltaZ>`  
   If Z is geometry-only: `Z_ellipsoid_shifted = $z + <DeltaZ>`.

### 11.4 Compute bed elevation (subtract pole height) - maybe we don't need this if SWMaps handles 'instrument height' correctly.
- **What:** Convert antenna heights to **bed elevations** using your recorded pole height per station.  
- **Why:** The antenna sits above the bed by `pole_h_m`.

**Steps:**  
1) Confirm `pole_h_m` exists per point.  
2) Field Calculator → `bed_Z = "Z_ellipsoid_shifted" - "pole_h_m"`  
   (If no PPP: `bed_Z = "Z_ellipsoid" - "pole_h_m"`.)

### 11.5 (Optional) Deliverables in WGS84
- **What:** If a client needs WGS84, **Save As → EPSG:4326** after all UTM work is done.  
- **Why:** Web maps prefer WGS84, but all calculations should stay in meters.

### 11.6 Sanity checks
- Imagery overlay: expect **~0.25–0.5 m** agreement near hard edges.  
- CP repeatability: **≤2 cm H / ≤3–4 cm V** between START/NOON/END.  
- Archive ΔE/ΔN/ΔZ, PPP report, ARP height, CRS (EPSG:32748).

---

## 12) Troubleshooting Quick Guide
- **SW Maps shows big errors:** Verify GNSS Master has **FIX**, **Mock ON**, Bluetooth is connected to **rover**.  
- **Can’t get FIX:** Move 2–3 m from water/metal, wait for PDOP to drop, extend averaging, confirm base radio & antenna cables.  
- **Heights off everywhere:** Re-check that you will subtract **tip→ARP**; ensure ellipsoidal heights; verify ARP and `pole_h_m` entries.  
- **PPP won’t converge:** Check log duration (≥6 h), sky view, and that you logged **UBX RAWX/SFRBX**.

---

## 13) Field Card (Copy/Paste)
```
Date/Time:
Crew:
CRS: UTM 48S (EPSG 32748) | Heights: Ellipsoidal (m)

BASE
- Ant model: ________   ARP ht: _______ m
- Survey-In/Here+Avg: 5 min (target) | E/N/Z: __________ / __________ / __________
- RINEX logging: start ____:____ / stop ____:____  (goal: 6–12 h total)
- Notes: ____________________________________________

CHECK POINT (CP)
- CP_START: avg ____ s | PDOP ___ | sats ___ | σH ___ cm | σV ___ cm
- CP_NOON : avg ____ s | PDOP ___ | sats ___ | σH ___ cm | σV ___ cm
- CP_END  : avg ____ s | PDOP ___ | sats ___ | σH ___ cm | σV ___ cm

SECTION <sect_id>
LB: avg ____ s | offset ____ m @ ____° to water_edge
BED stations (repeat):
  station  avg_s  PDOP  sats  σH  σV  pole_h_m  notes
  _______  _____  ____  ____  __  __  ________  ______________________
RB: avg ____ s | offset ____ m @ ____° to water_edge
WSE: method __________  time ________  notes __________________
```

---

## 14) Attribute Dictionary (what each field means & how we use it in QGIS)
These match the fields you create in **SW Maps** (§6.1). Consistent names keep the QGIS steps simple.

| Field | Type | Meaning | How it’s used in QGIS |
|---|---|---|---|
| `sect_id` | Text | Cross‑section identifier (e.g., `XS_01`) | Group and label stations to build profiles per section. |
| `pt_role` | Pick list | Point role: `LB`, `BED`, `RB`, `WSE`, `CTRL`, `CP` | Filter/symbolize; bed profiles use `BED`; `LB/RB` mark ends; `CP` for repeatability. |
| `station` | Integer | Order along the cross‑section (LB=0 → … → RB=last) | Sort for plotting; derive chainage if needed. |
| `avg_s` | Integer (s) | Averaging time used at capture | QA context. |
| `PDOP` | Decimal | Sky geometry (lower = better) | QA filtering (e.g., PDOP > 2.5). |
| `sats` | Integer | Satellites used | QA; low counts can explain noise. |
| `sigmaH_cm` | Decimal | Reported horizontal precision (cm) | QA threshold & symbology. |
| `sigmaV_cm` | Decimal | Reported vertical precision (cm) | QA threshold; affects confidence in bed Z. |
| `pole_h_m` | Decimal (m) | **Tip→ARP** pole height for the shot | Subtract from `Z_ellipsoid_shifted` to compute `bed_Z`. |
| `offset_m` | Decimal (m) | Distance from occupied point to true feature | Optional geometric correction using bearing; often metadata. |
| `offset_bearing_deg` | Decimal (°) | Bearing of the offset (0–360) | With `offset_m`, can place adjusted points. |
| `offset_to` | Pick list | What the offset references | Metadata/documentation. |
| `notes` | Text | Free text | Context for obstacles, special methods. |
| `Z_ellipsoid`* | Decimal (m) | Ellipsoidal height (if exported as attribute) | Add **ΔZ** to get `Z_ellipsoid_shifted`. |
| `Z_ellipsoid_shifted` | Decimal (m) | Post‑PPP corrected ellipsoidal height | Subtract `pole_h_m` to get `bed_Z`. |
| `bed_Z` | Decimal (m) | Computed bed elevation (ellipsoidal) | Use for profiles/analysis; geoid later if needed. |

\* Some exports store Z only in the geometry (not a column). In QGIS use `$z` or copy it into a field via Field Calculator.

---

## 15) Pole Height Correction (clear steps for crew & desk)
**Why:** The GNSS height is at the antenna (**ARP**). For **bed elevations**, subtract the **pole height** (tip→ARP) recorded at each bed station.

### In the field  
- Always record `pole_h_m` for each **BED** shot. If pole length changes, update the value before collecting.

### In QGIS — with PPP translation (recommended)  
1) Ensure `Z_ellipsoid_shifted = Z_ellipsoid + ΔZ` (or `$z + ΔZ`).  
2) Compute:  
```
bed_Z = "Z_ellipsoid_shifted" - "pole_h_m"
```

### In QGIS — without PPP (fallback)  
```
bed_Z = "Z_ellipsoid" - "pole_h_m"    # or $z - "pole_h_m" if Z is from geometry
```
(Absolute vertical may be biased, but relative bed shapes remain valid.)

### (Optional) Sea‑level heights later  
After PPP/pole correction, if you need orthometric heights, subtract geoid undulation `N`:  
```
bed_Z_orthometric = bed_Z - geoid_undulation
```
(Document which geoid you used.)

---

**Version:** 2025-10-26 • **Target alignment:** ~0.25–0.5 m to imagery via PPP translation • **Project:** OpenRiverCam
