# SURVEY_PROCESS.md
One-Day River Survey SOP (Points-Only) — **ArduSimple + Android + GNSS Master → SW Maps**  
**CRS:** WGS84 (EPSG:4326, default in SW Maps) • **Heights in field:** Ellipsoidal (meters)  
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
1) Charge base, rover, radios, phone; pack bipod, steel tape/laser, notebook.  
2) Android → Enable **Developer Options** → **Select mock location app = GNSS Master**.  
3) SW Maps → keep **WGS84 default**; display **Decimal degrees** with 7–8 decimals.  
4) Create SW Maps **point attributes** for QGIS use later (see **Section 6.1** for step‑by‑step).  
   - `sect_id` (e.g., `XS_01`)  
   - `pt_role` (`LB`, `RB`, `BED`, `WSE`, `CTRL`, `CP`)  
   - `station` (integer along section: LB=0 → … → RB=last)  
   - `avg_s`, `PDOP`, `sats`, `sigmaH_cm`, `sigmaV_cm`  
   - `pole_h_m` (tip→ARP)  
   - `offset_m`, `offset_bearing_deg`, `offset_to` (e.g., `water_edge`)  
   - `notes`

---

## 4) **Base Setup for Clean Basemap Alignment (0.25–0.5 m target)**
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
- **Start base RINEX logging (1 Hz)** and **leave it running 6–12 hours** while you work (how‑to in **Section 4.5**).  
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

**Route B — Windows Laptop with u‑blox u‑center (UBX → RINEX)**  
1. Connect base F9P to the laptop via **USB** (note the COM port).  
2. Open **u‑center** → **Receiver** → **Connection** → select the COM port.  
3. **Enable raw messages** (if not already): **View → Messages (F9)** → UBX → RXM → **RAWX** & **SFRBX** → set **Rate = 1** (on the used port, e.g., USB).  
4. Start logging: **File → Log → Start** (choose **UBX** binary). Let it run **6–12 h**.  
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
- Record: **Base Lat/Lon/Z (survey‑in)**, **antenna ARP height**, **start/stop (local & UTC)**, **receiver/antenna models**.  
- Back up the RINEX to two places.

---

## 5) Rover → Android (Mock Location)
1) Pair Android **Bluetooth** with the **rover**.  
2) Open **GNSS Master** → Receiver: **Bluetooth** → select rover; verify live sats/PDOP/status.  
3) Toggle **Mock Location ON**.  
4) Wait for **RTK FIX** and stable PDOP/sats.  
> From now on, SW Maps reads the rover’s precise position as the phone’s GPS.

---

## 6) SW Maps Project (Points-Only)
1) **New Project** (WGS84 default).  
2) **GPS Source:** **Device internal GPS** (this uses the GNSS Master mock).  
3) **Heights:** Ellipsoidal (meters).  
4) **Point collection:** Averaging **by time**; enter 20/60/120–180 s per point.  

### 6.1 **Create the point attributes (step‑by‑step)**
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
7. **Averaging setting:** **Settings → Data Capture → GPS Averaging → By Time** (you’ll enter per‑point 20/60/120–180 s).  
8. **Heights:** **Settings → Location** → ensure **Use orthometric/geoid height** is **OFF** so elevation is **ellipsoidal** (meters).  
9. **Live stats:** enable showing **PDOP / Sats / Accuracy** on the capture screen to help crews pass the quality gate.

---

## 7) Create a **Check Point (CP)**
1) Pick open-sky spot 20–50 m from base; **mark it**.  
2) Pole plumb (bipod); confirm **quality gate**.  
3) Record **CP_START** with **60 s** averaging; fill attributes.  
4) Re-occupy at **midday** and **end-of-day** (targets: **≤ 2 cm H**, **≤ 3–4 cm V** vs CP_START).

---

## 8) Collecting Points (Banks/Controls/Features)
**Avoid multipath:** When marking bank edges, stand **2–3 m back** from water and store an **offset** to the true feature (distance + bearing).

**Per point workflow**
1) Pole plumb; verify **FIX** and **quality gate**.  
2) Averaging: **20 s** open • **60 s** near water/trees • **120–180 s** bridges/heavy canopy.  
3) If offsetting: set `offset_m`, `offset_bearing_deg`, `offset_to="water_edge"`.  
4) Save with clear `sect_id`, `pt_role`, `station`, and notes.  
5) **Tricky spots:** take a **second occupation** ≥ 20–30 min later (60 s). Accept if within **≤ 2 cm H / ≤ 3 cm V**.

---

## 9) River Cross-Section by Pole (Points-Only)
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
- **Midday:** re-occupy **CP** (60 s). Target **≤ 2 cm H / ≤ 3–4 cm V** vs CP_START. If worse: re-level, back away from metal/vehicles, check base/radio, extend averages.  
- **End-of-day:** re-occupy **CP_END** (60 s).  
- Export SW Maps **points** (CSV/GeoJSON/SHZ) with all attributes.  
- Turn **Mock Location OFF**; power down rover/base.  
- Stop base **RINEX** last (if used). Photograph base, CP, and context.

---

## 11) After the Field — QGIS Steps (PPP Translation + Bed Z)
### 11.1 PPP the base
- Run **PPP** on the base **RINEX** (6–12 h). You get a **precise base coordinate** (Lat/Lon/Z_ellipsoid).

### 11.2 Compute translation (ΔE, ΔN, ΔZ)
1) In QGIS, create points for **Field base** (from survey-in) and **PPP base**.  
2) Reproject both to **UTM Zone 48S (EPSG:32748)**.  
3) Compute **ΔE, ΔN, ΔZ = PPP_base − Field_base** (meters).

### 11.3 Shift all survey points
1) Reproject your **survey points** to **EPSG:32748**.  
2) Use **Vector ► Translate (Move, shift)** to apply **ΔE** (East), **ΔN** (North).  
3) For elevations, add **ΔZ** to Z (either now or when computing bed_Z).  
4) (Optional) Reproject back to **WGS84** for delivery.

### 11.4 Compute bed elevation
- Add a field `bed_Z` and calculate:  
```
bed_Z = Z_ellipsoid + ΔZ  − pole_h_m
```
(or compute `Z_ellipsoid + ΔZ` first, then subtract `pole_h_m` per point).

**Result:** Visual alignment to OSM/satellite typically **0.25–0.5 m**, while internal geometry remains at cm-level.

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
CRS: WGS84 (EPSG 4326) | Heights: Ellipsoidal (m)

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
