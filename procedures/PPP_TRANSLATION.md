# PPP_TRANSLATION.md
QGIS Cheat‑Sheet — Apply PPP Translation to Your Survey
**Goal:** Align your RTK survey (collected with a short base survey‑in) to **precise global coordinates** by shifting everything to the **PPP‑refined base**. This preserves all **relative** geometry (cm‑level) while improving **absolute** alignment (≈0.25–0.5 m typical).

---

## 0) What you need
- **Field base coordinate** (from the base’s 5‑min survey‑in): `Lat_field, Lon_field, Z_field` (ellipsoidal).  
- **PPP base coordinate** (from PPP on 6–12 h RINEX): `Lat_ppp, Lon_ppp, Z_ppp` (ellipsoidal).  
- Your **survey points** dataset (WGS84, ellipsoidal Z), exported from SW Maps (CSV/GeoJSON/SHZ).

> Keep antenna **ARP height** and the **exact survey‑in height entry** handy. Z values must be internally consistent (ellipsoidal). You can convert to orthometric (geoid) later, after translation.

---

## 1) Create two base points in QGIS
1. **Start a new QGIS project.**
2. **Add your survey points** (WGS84 / EPSG:4326). Confirm attribute fields are present.
3. Create a new **temporary scratch layer** (Point, WGS84) and **add a single feature** at `Lat_field, Lon_field` named **Field_Base**. Set its Z to `Z_field` if using 3D/measure Z in attributes.
4. Duplicate that feature for **PPP_Base** and edit its geometry to `Lat_ppp, Lon_ppp`, Z `Z_ppp`.

> Optional: Instead of manual points, you can **Import from CSV** twice (one row each) to create **Field_Base** and **PPP_Base** layers.

---

## 2) Work in a metric CRS for offsets
Although your layers are WGS84, do **calculations in meters**:
1. **Reproject** all three layers (Survey, Field_Base, PPP_Base) to **UTM Zone 48S (EPSG:32748)**:  
   - Right‑click layer ► **Export ► Save Features As…** ► CRS: **EPSG:32748** ► save as new layers: `Survey_UTM`, `FieldBase_UTM`, `PPPBase_UTM`.
2. Style `FieldBase_UTM` and `PPPBase_UTM` so you can see both.

---

## 3) Compute the translation vector (ΔE, ΔN, ΔZ)
We want **PPP_Base − Field_Base** in meters.
1. Open **Field Calculator** on `FieldBase_UTM` and **add geometry attributes** if needed:
   - `x_field = $x`
   - `y_field = $y`
   - `z_field = "Z_field"` (if Z is in an attribute) or leave Z for later.
2. On `PPPBase_UTM`, compute:
   - `x_ppp = $x`
   - `y_ppp = $y`
   - `z_ppp = "Z_ppp"` (if available)
3. Read the numeric values (identify tool), then calculate:  
   - **ΔE = x_ppp − x_field**  
   - **ΔN = y_ppp − y_field**  
   - **ΔZ = Z_ppp − Z_field** (ellipsoidal; skip if doing 2D only)

> Tip: Put these three numbers in your project notes. Example: ΔE = +0.42 m, ΔN = −0.18 m, ΔZ = +0.27 m.

---

## 4) Shift (translate) all survey points
1. Use **Vector ► Geoprocessing Tools ► Translate (Move, shift)**.  
2. **Input layer:** `Survey_UTM`.  
3. **Offset X:** ΔE (meters). **Offset Y:** ΔN (meters).  
4. **Run** ► Output: `Survey_UTM_shifted`.

> If you need **3D Z shift**, add a new numeric field `Z_shifted` and compute:  
> `Z_shifted = "Z_ellipsoid" + ΔZ`.  
> Later bed elevation formula uses this shifted Z.

---

## 5) Optional: return to WGS84 for delivery
- Right‑click `Survey_UTM_shifted` ► **Export ► Save Features As…** ► CRS: **EPSG:4326**.  
- Name it `Survey_WGS84_aligned`. This is the layer to overlay with OSM/satellite in web maps.

---

## 6) Validate the alignment
- Overlay `Survey_WGS84_aligned` with a high‑quality basemap (OSM, satellite).  
- Check nearby **hard features** (bridge corners, pavement edges, quay walls). Expect **~0.25–0.5 m** coincidence.  
- Re‑check your **CP** point(s) from start/mid/end—differences between occupations should remain **≤ 2 cm H / ≤ 3–4 cm V** (relative precision preserved).

---

## 7) Bed elevation reminder (after translation)
If your survey points carry **ellipsoidal Z**, compute **bed_Z** in a new field:
```text
bed_Z = Z_ellipsoid_shifted − pole_h_m
```
Where `Z_ellipsoid_shifted` is your **Z after ΔZ** was applied.  
If you add a geoid later for orthometric heights, apply it **after** the PPP translation.

---

## 8) Common pitfalls & quick fixes
- **Did offsets move in degrees?** Make sure the translation ran in a **projected CRS (EPSG:32748)**, not in WGS84 degrees.  
- **Wrong sign on ΔE/ΔN:** Vector must be **PPP − Field**. If you used the opposite, reverse signs.  
- **Heights look off by a constant:** You likely skipped **ΔZ**. Apply it and recompute `bed_Z`.  
- **PPP coordinate epoch mismatch:** For short intervals this is negligible; if using high‑precision geodetic frames, note the PPP epoch in project notes.  
- **Mixed height types:** Keep everything **ellipsoidal** through the translation. Apply **geoid** only after.

---

## 9) Minimal record to archive
- PPP report (PDF/CSV) and **RINEX** used.  
- Field base Lat/Lon/Z, ARP height, and **survey‑in duration**.  
- ΔE, ΔN, ΔZ values and CRS used (EPSG:32748).  
- QGIS project or processing log (so anyone can repeat the shift).

---

### One‑liner summary
**Compute ΔE/ΔN/ΔZ from PPP vs field base in UTM (EPSG:32748) → Translate the entire survey by those deltas → (optional) back to WGS84.** Alignment to OSM/satellite should now be within **~0.25–0.5 m** while keeping your cm‑level relative accuracy.
