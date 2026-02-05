# PPP_TRANSLATION.md
PPP Translation — UTM‑Everywhere Guide (EPSG:32748)

**What & Why**  
Your day’s RTK survey has **cm‑level relative** accuracy but the **absolute** base position from a short survey‑in can be off by meters. By running **PPP** on the base RINEX (see *SURVEY_PROCESS.md* §4.5–4.6), you obtain a precise base coordinate. Compute a constant **meter translation** (ΔE, ΔN, ΔZ) between the **Field Base** and the **PPP Base** in **UTM Zone 48S (EPSG:32748)** and apply it to **all points**. Then subtract **pole height** per shot to get **bed elevations**. Expect **~0.25–0.5 m** alignment to imagery while preserving internal geometry.

**Project CRS:** UTM Zone 48 South (**EPSG:32748**) • **Heights:** Ellipsoidal (m)

Cross‑refs: *SURVEY_PROCESS.md* §4 (Base), §6 (SW Maps/UTM), §11 (QGIS workflow), §15 (Pole height).

---

## Inputs
- **Survey points**: layer in **EPSG:32748** (from SW Maps project set to UTM; see §6).  
- **Field Base** (from 5‑min survey‑in in §4.3): Lat/Lon/Z or E/N/Z.  
- **PPP Base** (from RINEX 6–12 h in §4.5–4.6): Lat/Lon/Z (ellipsoidal).  
- Attributes: `Z_ellipsoid` (if exported), `pole_h_m`, `sect_id`, `pt_role`, `station`.

> Keep **ARP height**, **UTC start/stop**, receiver/antenna models; PPP frame/epoch from the PPP report.

---

## 1) Build base points in UTM (meters)
**What:** Create **FieldBase_UTM** and **PPPBase_UTM** layers in **EPSG:32748**.  
**Why:** ΔE/ΔN/ΔZ must be computed in **meters** in the same projected CRS.

Steps
1. If your bases are Lat/Lon: **Layer ► Add Delimited Text** (WGS84) → **Save As ► EPSG:32748**.  
2. Name the layers **FieldBase_UTM** and **PPPBase_UTM**.  
3. Use **Identify** (or add fields `$x`, `$y`) to read **Easting (E)**, **Northing (N)**; record **Z** (ellipsoidal).

---

## 2) Compute the translation (ΔE, ΔN, ΔZ)
**What:** Calculate **PPP − Field** in meters.  
**Why:** This constant 3‑D vector translates your entire survey into the PPP frame.

Formulas
- **ΔE = E_ppp − E_field**  
- **ΔN = N_ppp − N_field**  
- **ΔZ = Z_ppp − Z_field**

Record these three numbers in your project notes (include sign).

---

## 3) Translate the survey (planar shift)
**What:** Shift all survey points by **ΔE/ΔN** in **EPSG:32748**.  
**Why:** Fixes absolute placement without changing relative distances/slopes.

Steps
1. Ensure your survey layer is **EPSG:32748** (Save As if needed) → call it `Survey_UTM`.  
2. **Vector ► Geoprocessing ► Translate (Move, shift)**  
   - Input: `Survey_UTM`  
   - **Offset X = ΔE**, **Offset Y = ΔN**  
   - Output: `Survey_UTM_shifted`

---

## 4) Apply vertical shift and compute bed_Z
**What:** Add **ΔZ** to the ellipsoidal altitude and subtract the **pole height** (`pole_h_m`) per station.  
**Why:** GNSS Z is at the antenna (**ARP**); you need river **bed** elevations.

If Z is an attribute (e.g., `Z_ellipsoid`):  
```
Z_ellipsoid_shifted = "Z_ellipsoid" + <DeltaZ>
```

If Z is only in geometry:  
```
Z_ellipsoid_shifted = $z + <DeltaZ>
```

Compute bed elevation:  
```
bed_Z = "Z_ellipsoid_shifted" - "pole_h_m"
```

*(If you didn’t run PPP, skip ΔZ and use `"Z_ellipsoid" - "pole_h_m"` or `$z - "pole_h_m"`; vertical may have a constant bias.)*

---

## 5) Validate & archive
- **Imagery overlay:** Expect **~0.25–0.5 m** visual agreement near hard edges (bridges, pavement, walls).  
- **Relative precision:** CP START/NOON/END differences remain **≤ 2 cm H / ≤ 3–4 cm V**.  
- **Archive:** ΔE/ΔN/ΔZ, PPP report (frame/epoch/uncertainties), ARP height, CRS (EPSG:32748), processing notes.

---

## Common pitfalls
- Doing translations in **degrees** (WGS84) → always use **EPSG:32748**.  
- Using **Field − PPP** by mistake → must be **PPP − Field**.  
- Forgetting **ΔZ** → verticals off by a constant.  
- Mixing orthometric and ellipsoidal heights → keep ellipsoidal through translation; apply geoid later if needed.

---

## One‑liner
**Compute ΔE/ΔN/ΔZ = (PPP − Field) in EPSG:32748 → Translate survey by ΔE/ΔN → Set `Z_ellipsoid_shifted` = old Z + ΔZ → `bed_Z` = `Z_ellipsoid_shifted` − `pole_h_m`.**
