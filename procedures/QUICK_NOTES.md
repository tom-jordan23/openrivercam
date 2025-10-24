# QUICK_NOTES.md
PPP Translation — UTM‑Everywhere Cheat Sheet (EPSG:32748)

**Goal**  
Align your RTK survey to precise global coordinates by applying a **UTM‑meter translation** from the PPP‑refined base. Keep cm‑level relative geometry; expect ~0.25–0.5 m absolute alignment to imagery.

**Project CRS:** UTM Zone 48 South (**EPSG:32748**) • **Heights:** Ellipsoidal (m)

---

## Inputs
- **Survey points**: already in **EPSG:32748** (exported from SW Maps project set to UTM).  
- **Field base** (from 5‑min survey‑in): Lat/Lon/Z or E/N/Z.  
- **PPP base** (from 6–12 h RINEX): Lat/Lon/Z (ellipsoidal).  
- Your field attribute columns, esp. `Z_ellipsoid` (or geometry Z), `pole_h_m`, `sect_id`, `pt_role`, `station`.

---

## 1) Bring base points into UTM
**What:** Get both **Field base** and **PPP base** into **EPSG:32748** so you can work in **meters**.  
**Why:** UTM avoids degree/meter mistakes and makes ΔE/ΔN straightforward.

Steps
1. If bases are in Lat/Lon: **Add Delimited Text** (WGS84), then **Save As → EPSG:32748**.  
2. Name layers: `FieldBase_UTM` and `PPPBase_UTM`.  
3. Use **Identify** (or add `$x`, `$y`) to read **Easting (E)** and **Northing (N)**; note **Z** (ellipsoidal).

---

## 2) Compute translation (ΔE, ΔN, ΔZ)
**What:** Compute PPP minus Field in the **same CRS**.  
**Why:** This is the constant meter shift you will apply to all points.

Formulas
- **ΔE = E_ppp − E_field**  
- **ΔN = N_ppp − N_field**  
- **ΔZ = Z_ppp − Z_field**

Write these three numbers into your project notes.

---

## 3) Translate the survey (planar)
**What:** Shift all points by **ΔE/ΔN** in **EPSG:32748**.  
**Why:** Fixes absolute placement without touching relative geometry.

Steps
1. Ensure your survey layer is **EPSG:32748** (Save As if needed).  
2. **Vector ► Geoprocessing ► Translate (Move, shift)**  
   - Input: your survey layer  
   - **Offset X = ΔE**  
   - **Offset Y = ΔN**  
   - Output: `Survey_UTM_shifted`

---

## 4) Apply vertical shift and compute bed_Z
**What:** Update Z for PPP (**ΔZ**) and subtract **pole height** to get bed elevation.  
**Why:** Antenna is at ARP; you want river **bed** heights.

If you have a Z attribute (e.g., `Z_ellipsoid`):
- Add field `Z_ellipsoid_shifted` (Decimal):  
  ```
  "Z_ellipsoid" + <DeltaZ>
  ```

If Z is only in geometry:
- Add field `Z_ellipsoid_shifted`:  
  ```
  $z + <DeltaZ>
  ```

Compute **bed_Z** (Decimal):  
```
"Z_ellipsoid_shifted" - "pole_h_m"
```

*(If no PPP, skip ΔZ and use `"Z_ellipsoid" - "pole_h_m"` or `$z - "pole_h_m"`; absolute vertical may have a constant bias.)*

---

## 5) QA & sanity checks
- **Imagery alignment:** Overlay on high‑quality satellite; expect **~0.25–0.5 m** coincidence near hard edges.  
- **Repeatability:** CP START/NOON/END differences should remain **≤ 2 cm H / ≤ 3–4 cm V** (confirms relative precision survived).  
- **Recordkeeping:** Save ΔE/ΔN/ΔZ, PPP report (epoch/frame), antenna ARP height, CRS (EPSG:32748).

---

## Common pitfalls
- Doing translations in **degrees** (WGS84) → always translate in **EPSG:32748**.  
- Using **Field − PPP** by mistake → must be **PPP − Field**.  
- Forgetting **ΔZ** → verticals off by a constant.  
- Mixing orthometric and ellipsoidal heights → keep ellipsoidal through translation; apply geoid later if needed.

---

## One‑liner
**Compute ΔE/ΔN/ΔZ = (PPP − Field) in EPSG:32748 → Translate survey by ΔE/ΔN → Set `Z_ellipsoid_shifted` = old Z + ΔZ → `bed_Z` = `Z_ellipsoid_shifted` − `pole_h_m`.**
