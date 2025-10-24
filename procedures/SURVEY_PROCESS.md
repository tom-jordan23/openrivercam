# SURVEY_PROCESS.md
One-Day River Survey SOP (Points-Only) — **ArduSimple + Android + GNSS Master → SW Maps**  
**CRS:** UTM Zone 48 South (EPSG:32748) • **Heights in field:** Ellipsoidal (meters)  
**Goal:** Collect high-quality points for cross-sections and bank/control features with **centimeter-level relative accuracy** and **0.25–0.5 m global alignment** to OSM/satellite **after a simple PPP translation**.

---

## 1) Plain-English Glossary
- **GNSS** — Satellite positioning (GPS, GLONASS, Galileo, BeiDou).  
- **RTK** — Real-time corrections from a nearby **base** to the mobile **rover** → cm-level relative accuracy.  
- **FIX / FLOAT** — RTK status; **FIX** = precise (use it), **FLOAT** = not fully locked (avoid).  
- **PDOP** — Satellite geometry quality; **lower is better** (≤2.5 good).  
- **RTCM** — Correction messages the base broadcasts to the rover.  
- **RINEX** — Raw GNSS log format used for **PPP** later.  
- **PPP (Precise Point Positioning)** — Post-processing that refines the **base coordinate** using precise orbits/clocks; yields a precise global tie.  
- **ARP (Antenna Reference Point)** — The physical feature on the antenna you measure to (usually the **bottom face** where it seats on the pole/tripod).  
- **Ellipsoidal height** — Height above the Earth ellipsoid (record in field).  
- **Orthometric height** — “Sea-level height” (convert later if required).  
- **Mock location (Android)** — Lets GNSS Master provide the rover’s position to apps as the phone’s GPS.

---

## 2) Crew Defaults (Memorize These)
**Quality gate before recording a point (all true):**  
- RTK **FIX** for ≥ 10 s  
- **PDOP ≤ 2.5** (≤ 2.0 ideal)  
- **Satellites ≥ 12**  
- **Correction age ≤ 2 s**  
- SW Maps estimated precision **σ ≤ 2 cm horizontal**, **≤ 3–4 cm vertical**  
- **Pole bubble centered** (use a bipod)

**Averaging window per point:**  
- **20 s** — open sky  
- **60 s** — near water/trees/structures  
- **120–180 s** — under bridges/heavy canopy

**Bed elevation (computed later in QGIS):**  
```
bed_Z = GNSS_Z_ellipsoidal − pole_height_tip_to_ARP
```

---

## 3) Night-Before Prep (5–10 min)
**What:** Prepare hardware, phone, and app settings; set up your project fields so capture is consistent.
**Why:** Small setup time saves hours in the field and ensures attribute names match the QGIS workflow.

1) Charge base, rover, radios, phone; pack bipod, steel tape/laser, notebook.  
2) Android → Enable **Developer Options** → **Select mock location app = GNSS Master**.  
3) SW Maps → set project CRS to **UTM Zone 48S (EPSG:32748)**; verify project units show **meters** (UTM).  
4) Create SW Maps **point attributes** for QGIS use later:  
   - `sect_id` (e.g., `XS_01`)  
   - `pt_role` (`LB`, `RB`, `BED`, `WSE`, `CTRL`, `CP`)  
   - `station` (integer along section: LB=0 → … → RB=last)  
   - `avg_s`, `PDOP`, `sats`, `sigmaH_cm`, `sigmaV_cm`  
   - `pole_h_m` (tip→ARP)  
   - `offset_m`, `offset_bearing_deg`, `offset_to` (e.g., `water_edge`)  
   - `notes`

---

## 4) **Base Setup for Clean Basemap Alignment (0.25–0.5 m target)**
**What:** Fix a stable local frame for the day and start long raw logging at the base.
**Why:** A short survey-in locks your relative geometry; long RINEX logging enables PPP so your survey aligns to imagery within ~0.25–0.5 m.

**Why:** RTK gives cm-level **relative** accuracy; **absolute** alignment to OSM/satellite depends on the **base coordinate**. Without NTRIP, the reliable path to **0.25–0.5 m** is to do a short survey-in **and** log raw data for PPP.

### 4.1 Site & mark
- Choose **open sky**, away from water/metal/wires; level tripod and **mark the ground** (paint/tack).

### 4.2 Measure antenna height to **ARP**
- Measure **vertical** ground→ARP to the **millimeter**; measure twice, write both, and use the mean.

### 4.3 Survey-in (freezes your local frame)
- Run **“Here + Average” for 5 minutes**.  
- **Record** the base Lat/Lon/Z it reports.  
- **Do not** re-average or move the base afterward.

### 4.4 Log raw data for PPP (RINEX)
- **Start base RINEX logging (1 Hz)** and **leave it running 6–12 hours** while you work (how-to in **Section 4.5**).  
- This enables a precise base coordinate later, giving a **single translation** you’ll apply to all rover points in QGIS.

> **Fallback if PPP isn’t possible later:** survey-in **30–60 min** (typ. ~0.8–1.5 m absolute bias). Usable, but visual alignment may still look off against imagery.

**Rule-of-thumb improvements (horizontal; vertical often ~2× worse):**

| Base method | Typical absolute bias (H) | Notes |
|---|---|---|
| 5 min survey-in | ~2–4 m | Good for local frame only |
| 30–60 min survey-in | ~0.8–1.5 m | Better if no PPP later |
| **6–12 h RINEX → PPP** | **~0.1–0.4 m (H)**, **~0.2–0.4 m (V)** | **Recommended** for OSM/satellite alignment |

### 4.5 **RINEX logging — how to start and capture (choose ONE route)**
> Your goal is a continuous **6–12 hour** log from the base receiver. Pick whichever tool you brought.

**Route A — ArduSimple microSD Datalogger (if you have it)**  
1. Insert a **FAT32** microSD card (≥8 GB recommended) into the ArduSimple **RTK datalogger** board attached to the base F9P.  
2. Power the base; confirm the datalogger **LOG** LED starts blinking (exact patterns vary by board).  
3. Leave it running all day; avoid power loss.  
4. After the survey, **power down**, remove the card, and copy the **RINEX** (or raw) files to your laptop/storage. Keep the **start/stop times** and **antenna height** with the files.

**Route B — Windows Laptop with u-blox u-center (UBX → RINEX)**  
1. Connect base F9P to the laptop via **USB** (note the COM port).  
2. Open **u-center** → **Receiver** → **Connection** → select the COM port.  
3. **Enable raw messages** (if not already): **View → Messages (F9)** → UBX → RXM → **RAWX** & **SFRBX** → set **Rate = 1** (on the used port, e.g., USB).  
4. Start logging: **File → Log → Start** (choose **UBX** binary). Let it run **6–12 h**.  **do not forget to disable any power saving features that would cause the logging station to stop logging**
5. Afterward, **File → Log → Stop**. Convert to RINEX: **Tools → Convert to RINEX** (or use **RTKLIB convbin**). Save RINEX, and note antenna height + times.

**Route C — RTKLIB (Windows/Linux/Raspberry Pi)**  
1. Connect to the base’s serial port (USB or UART).  
2. Use **STRSVR/str2str** to log **UBX** at **1 Hz** to a file for **6–12 h**. Example (Linux/Pi):  
   ```bash
   str2str -in serial://ttyACM0:115200#ubx -out file://base_ubx_%Y%m%d_%H%M.ubx -b 1
   ```  
3. After the session, convert UBX → RINEX with **RTKLIB convbin**:  
   ```bash
   convbin base_ubx_*.ubx -r ubx -od -os -oi -ot -o base_rinex.obs
   ```  
4. Keep antenna height and exact times alongside the files.

**Data hygiene**  
- Use **UTC** timestamps where possible.  
- Record: **Base Lat/Lon/Z (survey-in)**, **antenna ARP height**, **start/stop (local & UTC)**, **receiver/antenna models**.  
- Back up the RINEX to two places.

---

## 5) Rover → Android (Mock Location)
**What:** Connect the rover to the phone via Bluetooth and let GNSS Master feed precise positions to SW Maps.
**Why:** SW Maps sees the rover as the phone GPS, avoiding app-specific drivers and keeping setup simple.

1) Pair Android **Bluetooth** with the **rover**.  
2) Open **GNSS Master** → Receiver: **Bluetooth** → select rover; verify live sats/PDOP/status.  
3) Toggle **Mock Location ON**.  
4) Wait for **RTK FIX** and stable PDOP/sats.  
> From now on, SW Maps reads the rover’s precise position as the phone’s GPS.

---

## 6) SW Maps Project (Points-Only)
**What:** Create a **UTM 48S** project and a point layer with averaging-by-time.
**Why:** Working natively in meters avoids mistakes when applying translations and computing elevations.

1) **New Project** → **Coordinate System:** search **UTM** and pick **WGS 84 / UTM zone 48S (EPSG:32748)**.
2) **GPS Source:** **Device internal GPS** (this uses the GNSS Master mock). SW Maps will transform incoming lat/lon to UTM on the fly.
3) **Heights:** Ellipsoidal (meters). Ensure **Use orthometric/geoid height** is **OFF**.
4) **Point collection:** Averaging **by time**; enter 20/60/120–180 s per point.

### Why meters (UTM) for calculations
- **What:** Keep the whole project in a **projected CRS (UTM)** so all offsets and translations are in **meters**.
- **Why:** Degrees aren’t constant distances; UTM prevents scale/sign errors when you apply ΔE/ΔN.

### 6.1 **Create the point attributes (step-by-step)**
> Menu names vary slightly by version; the flow is the same.

1. Open **SW Maps** → **New Project** → confirm **WGS84**.  
2. Tap the **menu (☰)** → **Layers**.  
3. Tap your **Point layer** (often named “Points” or your project name).  
4. Tap **Fields / Attributes** → **Add Field**.  
5. Add fields one by one with **Type** and **Defaults**:  
   - `sect_id` — **Text** (e.g., `XS_01`)  
   - `pt_role` — **Text with Pick List** → values: `LB, RB, BED, WSE, CTRL, CP` (so crews can’t mistype)  
   - `station` — **Integer** (LB=0 → 1,2,… → RB=last)  
   - `avg_s` — **Integer** (default 60)  
   - `PDOP` — **Decimal (1)**  
   - `sats` — **Integer**  
   - `sigmaH_cm` — **Decimal (1)**  
   - `sigmaV_cm` — **Decimal (1)**  
   - `pole_h_m` — **Decimal (3)** (e.g., 2.150)  
   - `offset_m` — **Decimal (2)** (default 0.00)  
   - `offset_bearing_deg` — **Decimal (1)** (0–360; default 0.0)  
   - `offset_to` — **Text with Pick List** → values: `water_edge, bank_top, centerline`  
   - `notes` — **Text (multiline)**  
6. Save the layer schema.  
7. **Averaging setting:** **Settings → Data Capture → GPS Averaging → By Time** (you’ll enter per-point 20/60/120–180 s).  
8. **Heights:** **Settings → Location** → ensure **Use orthometric/geoid height** is **OFF** so elevation is **ellipsoidal** (meters).  
9. **Live stats:** enable showing **PDOP / Sats / Accuracy** on the capture screen to help crews pass the quality gate.
### Why meters (UTM) for calculations
- **What:** When you compute deltas/offsets after the field, switch to a **projected CRS** like **UTM Zone 48S (EPSG:32748)**.
- **Why:** WGS84 uses **degrees**, which are not constant distances. Working in UTM guarantees **meters**, preventing scale/sign mistakes during the PPP translation.
  - You’ll do this in Section 11 when computing **ΔE/ΔN/ΔZ**.


---

## 7) Create a **Check Point (CP)**
**What:** Measure the same nearby mark at start/mid/end of day.
**Why:** Confirms your day’s stability (receiver, base, radio, crew technique) without needing external control.

1) Pick open-sky spot 20–50 m from base; **mark it**.  
2) Pole plumb (bipod); confirm **quality gate**.  
3) Record **CP_START** with **60 s** averaging; fill attributes.  
4) Re-occupy at **midday** and **end-of-day** (targets: **≤ 2 cm H**, **≤ 3–4 cm V** vs CP_START).

---

## 8) Collecting Points (Banks/Controls/Features)
**What:** Capture points using time-averaging and offsets where needed near water.
**Why:** Offsets avoid multipath while preserving correct feature locations; averaging reduces random noise.

**Avoid multipath:** When marking bank edges, stand **2–3 m back** from water and store an **offset** to the true feature (distance + bearing).

**Per point workflow**
1) Pole plumb; verify **FIX** and **quality gate**.  
2) Averaging: **20 s** open • **60 s** near water/trees • **120–180 s** bridges/heavy canopy.  
3) If offsetting: set `offset_m`, `offset_bearing_deg`, `offset_to="water_edge"`.  
4) Save with clear `sect_id`, `pt_role`, `station`, and notes.  
5) **Tricky spots:** take a **second occupation** ≥ 20–30 min later (60 s). Accept if within **≤ 2 cm H / ≤ 3 cm V**.

---

## 9) River Cross-Section by Pole (Points-Only)
**What:** Walk a transect from LB to RB, logging bed stations and pole heights at each stop.
**Why:** Provides bed profile geometry for hydraulics; per-station pole height lets you convert antenna heights to bed elevations.

**Plan:** Choose a straight reach. Define `sect_id` (e.g., `XS_01`). Mark **LB** and **RB** on firm ground. Choose safe station spacing (e.g., 1–2 m).

**Pole height logic:** record `pole_h_m` (tip→ARP) **per station**. Later in QGIS:  
```
bed_Z = GNSS_Z_ellipsoidal − pole_h_m
```

**Steps**
1) **LB:** stand 2–3 m back; collect LB (**60 s**). Offset to water edge if needed. `pt_role=LB`, `station=0`.  
2) **Across channel:** for each planned station: plant **pole tip on bed**, keep bubble centered; verify **FIX**; average **60–120 s** (or **120–180 s** under bridges); record **`pole_h_m`**; save as `pt_role=BED` with `station` 1,2,3…  
3) **RB:** same as LB; `pt_role=RB`, `station=last`.  
4) **Optional WSE:** capture `pt_role=WSE` at water surface (note method/time).

---

## 10) Midday & End-of-Day QA
**What:** Re-occupy the CP and review outliers before packing up.
**Why:** Catches drift or mistakes early so you can re-shoot while still on site.

- **Midday:** re-occupy **CP** (60 s). Target **≤ 2 cm H / ≤ 3–4 cm V** vs CP_START. If worse: re-level, back away from metal/vehicles, check base/radio, extend averages.  
- **End-of-day:** re-occupy **CP_END** (60 s).  
- Export SW Maps **points** (CSV/GeoJSON/SHZ) with all attributes.  
- Turn **Mock Location OFF**; power down rover/base.  
- Stop base **RINEX** last (if used). Photograph base, CP, and context.

---

## 11) After the Field — QGIS Steps (PPP Translation + Bed Z)

**What & Why:** Use the base’s PPP solution to get a precise global position, compute a **meter-based** translation (ΔE, ΔN, ΔZ) between the **field base** and the **PPP base**, and apply that translation to **all survey points**. Then subtract **pole height** to get **bed elevations**. Keeping the project in **UTM** means all steps are in **meters** end-to-end.

### 11.1 PPP the base — get a precise base coordinate
- **What:** Run **PPP** on the base’s **RINEX (6–12 h)** to obtain a precise **Lat/Lon/Z (ellipsoidal)** for the base.
- **Why:** Short survey-in can carry meter-level bias; PPP removes clock/orbit/ionosphere biases, giving a solid global tie.
- **Keep:** `Lat_ppp, Lon_ppp, Z_ppp`, antenna ARP height, PPP frame/epoch, uncertainties.

### 11.2 Bring base points into UTM and compute ΔE/ΔN/ΔZ
- **What:** Create two base points: **Field base** (from the 5‑min survey‑in) and **PPP base** (from PPP). If they arrive as lat/lon, import as **WGS84** and then **Save As → EPSG:32748**. Read their **Easting (E)**, **Northing (N)**, and Z to compute:
  - **ΔE = E_ppp − E_field**
  - **ΔN = N_ppp − N_field**
  - **ΔZ = Z_ppp − Z_field**
- **Why:** We need the pure meter translation between the two base positions in the same projected CRS.

**Steps:**
1) Add `Field_Base` and `PPP_Base` layers.
2) Ensure both are in **EPSG:32748** (Save As if needed).
3) Use **Identify** or add `$x`, `$y` fields to read E/N; note Z values; compute ΔE/ΔN/ΔZ.

### 11.3 Shift all survey points in UTM
- **What:** Apply **ΔE/ΔN** to the entire survey to create `Survey_UTM_shifted`. Add **ΔZ** to the altitude field.
- **Why:** This fixes absolute placement without changing any relative distances/slopes.

**Steps:**
1) Ensure your survey layer is **EPSG:32748** (if not, **Save As → EPSG:32748**).
2) **Vector ► Geoprocessing ► Translate (Move, shift)** → Input = survey layer → **Offset X = ΔE**, **Offset Y = ΔN** → Output = `Survey_UTM_shifted`.
3) If Z is an attribute (e.g., `Z_ellipsoid`), add a new field `Z_ellipsoid_shifted`:
   - Field Calculator: `"Z_ellipsoid" + <DeltaZ>`
   If Z is in geometry only, calculate a field as `$z + <DeltaZ>`.

### 11.4 Compute bed elevation (subtract pole height)
- **What:** Convert antenna heights to **bed elevations** using your recorded pole height per station.
- **Why:** The antenna is above the bed by `pole_h_m`; removing it yields the true bed.

**Steps:**
1) Confirm `pole_h_m` exists per point.
2) Field Calculator → new/updated field `bed_Z`:
```
bed_Z = "Z_ellipsoid_shifted" - "pole_h_m"
```
If you skipped PPP: use `"Z_ellipsoid" - "pole_h_m"` (vertical may have a constant bias).

### 11.5 (Optional) Deliverables in WGS84
- **What:** If a client needs WGS84, you can **Save As → EPSG:4326** after all UTM work is done.
- **Why:** Web maps often prefer WGS84, but doing the math in UTM avoids degree/meter confusion.

### 11.6 Sanity checks
- Overlay the result on high‑quality imagery; expect **~0.25–0.5 m** visual agreement.
- Confirm CP start/mid/end repeatability **≤ 2 cm H / ≤ 3–4 cm V**.
- Archive ΔE/ΔN/ΔZ, PPP report, antenna ARP height, and CRS details.

---

## 12) Troubleshooting Quick Guide
- **SW Maps shows big errors:** Ensure GNSS Master has **FIX**, **Mock ON**, Bluetooth is connected to the **rover**.  
- **Can’t get FIX:** Step 2–3 m away from water/metal; wait for PDOP to drop; extend averaging; confirm base radio & antenna cables.  
- **Heights look wrong everywhere:** Re-check that you will subtract **tip→ARP**; confirm SW Maps is recording **ellipsoidal meters**; verify antenna **ARP** location and pole height entry.

---

## 13) Field Card (Copy/Paste)
```
Date/Time:
Crew:
CRS: UTM 48S (EPSG 32748) | Heights: Ellipsoidal (m)

BASE
- Ant model: ________   ARP ht: _______ m
- Survey-In/Here+Avg: 5 min (target) | Lat/Lon/Z: __________ / __________ / __________
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

**Version:** 2025-10-25 • **Target alignment:** 0.25–0.5 m to OSM/satellite via PPP translation • **Project:** OpenRiverCam

---

## 14) Attribute Dictionary (what each field means & how we use it in QGIS)

These match the fields you create in **SW Maps** (see Section 6.1). Keeping names consistent makes the QGIS steps straightforward.

| Field | Type | Meaning | How it’s used in QGIS |
|---|---|---|---|
| `sect_id` | Text | Cross‑section identifier (e.g., `XS_01`) | Group and label stations to build profiles per section. |
| `pt_role` | Pick list | Point role: `LB` (left bank), `BED` (bed station), `RB` (right bank), `WSE` (water surface), `CTRL` (control), `CP` (check point) | Filter/symbolize; bed profiles use `BED`; `LB/RB` mark ends; `CP` used for repeatability checks. |
| `station` | Integer | Order along the cross‑section (LB=0 → 1,2,… → RB=last) | Sort for plotting; derive chainage later if needed. |
| `avg_s` | Integer (s) | Averaging time used at capture | QA context: longer averages expected near bridges/canopy. |
| `PDOP` | Decimal | Sky geometry (lower = better) | QA filtering (e.g., drop PDOP > 2.5). |
| `sats` | Integer | Satellites used | QA: low counts explain noise; flag outliers. |
| `sigmaH_cm` | Decimal | Reported horizontal precision (cm) | QA threshold and symbology. |
| `sigmaV_cm` | Decimal | Reported vertical precision (cm) | QA threshold affecting confidence in bed Z. |
| `pole_h_m` | Decimal (m) | **Tip→ARP** pole height used for the shot | **Subtract from ellipsoidal Z** (after PPP ΔZ) to compute **bed_Z**. |
| `offset_m` | Decimal (m) | Distance from where you stood to the true feature | Optional geometric correction using bearing, or just metadata. |
| `offset_bearing_deg` | Decimal (°) | Bearing of the offset (0–360, clockwise from north) | With `offset_m`, can place adjusted points if desired. |
| `offset_to` | Pick list | What the offset references (`water_edge`, `bank_top`, `centerline`) | Metadata/documentation. |
| `notes` | Text | Free text | Context for obstacles, special methods. |
| `Z_ellipsoid`* | Decimal (m) | Height stored by SW Maps (ellipsoidal) | Add **ΔZ** (PPP shift) to get `Z_ellipsoid_shifted`. |
| `Z_ellipsoid_shifted` | Decimal (m) | Post‑PPP corrected ellipsoidal height | Subtract `pole_h_m` to get `bed_Z`. |
| `bed_Z` | Decimal (m) | Computed bed elevation (ellipsoidal) | Use for profiles/analysis; convert to orthometric later if needed. |

\* Some exports store Z only in the geometry (not as a column). In QGIS you can reference it with `$z` or copy it into a field using the Field Calculator.

---

## 15) Pole Height Correction (clear steps for crew & desk)

**Why:** The GNSS height you record is at the antenna (**ARP**). For **bed elevations**, subtract the **pole height** (tip→ARP) you recorded at each bed station.

### In the field (notes only)
- Always record `pole_h_m` (tip→ARP) **for each bed shot**. If pole length changes, update the value before you press “Collect.”

### In QGIS — with PPP translation (recommended)
1. Apply the **PPP translation** (ΔE, ΔN, ΔZ) as described in *PPP_TRANSLATION.md* or Section 11.  
2. Ensure you have a field `Z_ellipsoid_shifted` that equals your ellipsoidal Z **after ΔZ was added**.  
   - If Z is an attribute field (e.g., `Z_ellipsoid`):  
     ```
     Z_ellipsoid_shifted = "Z_ellipsoid" + <DeltaZ>
     ```
   - If Z is only in geometry:  
     ```
     Z_ellipsoid_shifted = $z + <DeltaZ>
     ```
3. Compute **bed_Z** (ellipsoidal) by subtracting the pole height:  
   ```
   bed_Z = "Z_ellipsoid_shifted" - "pole_h_m"
   ```

### In QGIS — without PPP (fallback if you didn’t log RINEX)
- Skip ΔZ and compute:  
  ```
  bed_Z = "Z_ellipsoid" - "pole_h_m"    # or $z - "pole_h_m" if Z is in geometry
  ```
- **Note:** Absolute vertical may be biased, but **relative** bed shapes remain valid.

### (Optional) Sea‑level heights later
- After PPP/pole correction, if you need orthometric (sea‑level) heights, subtract geoid undulation `N`:  
  ```
  bed_Z_orthometric = bed_Z - geoid_undulation
  ```
  (Use a geoid model plugin or raster; document which geoid you used.)
