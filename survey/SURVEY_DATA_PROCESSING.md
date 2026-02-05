# SURVEY_DATA_PROCESSING.md

This document captures the workflow used to take field survey data in **WGS84 lat/lon** and produce analysis‑ready layers in **UTM Zone 48S (EPSG:32748)**, including **pole‑height adjustment**, adding **water‑depth values recorded by hand in the field**, and explicit **`x_m` / `y_m`** meter columns.

---

## 0) Assumptions & prerequisites
- **Source CRS:** WGS 84 (EPSG:4326), coordinates in degrees (`lat`, `lon`), elevations typically **in meters**.
- **Target CRS:** WGS 84 / UTM Zone 48S (EPSG:32748), coordinates in meters.
- **Software:** QGIS 3.x.
- **Format:** GeoPackage (`.gpkg`) so CRS is stored per layer.
- **Fields present or to be created:**
  - `Elevation` (raw elevation; usually meters from GNSS/SW Maps).
  - `PoleHeight` (meters).
  - `Elev_Adj` (adjusted elevation = `Elevation` − `PoleHeight`).
  - `Depth_m` (water depth from handwritten notes, normalized to meters).
  - `x_m`, `y_m` (Easting/Northing in meters from geometry).

> If elevations are actually **centimeters**, convert them once to meters before doing math (Step 6).

---

## 1) Declare the source CRS (don’t convert yet)
1. Layers panel → right‑click the source layer → **Properties… → Source → Geometry**.
2. Confirm **WGS 84 (EPSG:4326)**. If *unknown/incorrect*: **Layer → Set Layer CRS… → WGS 84 (EPSG:4326)** → OK.  
   *This just declares the CRS; it doesn’t change numbers.*

---

## 2) Set the Project CRS (for viewing in meters)
1. Bottom‑right CRS button → search **32748** → select **WGS 84 / UTM zone 48S (EPSG:32748)** → OK.  
   *On‑the‑fly reprojection for display; data still stored in original CRS.*

---

## 3) Reproject to UTM 48S (create actual meter layers)
For each layer:
1. Right‑click layer → **Export → Save Features As…**
2. **Format:** GeoPackage → choose/create a `.gpkg` → set **Layer name** (e.g., `survey_points_utm48s`).
3. **CRS:** **EPSG:32748**.
4. **Fields / Layer Options:** If you have a non‑integer `FID/fid/ogc_fid`, uncheck/rename it or set **Layer option FID** to a safe name (e.g., `gid`).
5. **OK** → a new **UTM** layer appears whose **geometry** is stored in meters.

(Batch: **Processing → Toolbox → Vector general → Reproject layer** with **Batch**.)

---

## 4) Add explicit meter columns from geometry: `x_m`, `y_m`
Use the **UTM layer** from Step 3.
1. **Open Attribute Table** → **Toggle editing**.
2. **New field** → Name `x_m` → Type *Decimal (Real)* → Length 12 / Precision 3 → **OK**.
3. **Field Calculator** → **Update existing field** = `x_m` → Expression:
   ```
   $x
   ```
4. Repeat for `y_m` with:
   ```
   $y
   ```
5. **Save edits** → **Toggle editing** off.

Now every feature has `x_m` (Easting) and `y_m` (Northing) in **meters**.

---

## 5) Add and populate `PoleHeight` (meters)
1. Attribute Table → **Toggle editing**.
2. **New field:** `PoleHeight` (Decimal, e.g., 10/3) → **OK**.
3. If constant (e.g., 2.000 m): **Field Calculator** → **Update existing field**=`PoleHeight` → Expression: `2.000` → **OK**.  
   If it varies, type per row.
4. **Save edits** (you may keep edit mode on for next steps).

> Keep units in **meters** to avoid confusion.

---

## 6) Ensure elevation is in meters (convert once if needed)
- If `Elevation` is meters, skip to Step 7.
- If it’s centimeters, create `Elevation_m` (Decimal) and set:
  ```
  "Elevation" / 100
  ```
Use `Elevation_m` in formulas below.

---

## 7) Create adjusted elevation: `Elev_Adj = Elevation − PoleHeight`
1. **New field:** `Elev_Adj` (Decimal, 12/3) → **OK**.
2. **Field Calculator** → **Update existing field** = `Elev_Adj`:
   - If base elevation is meters:
     ```
     "Elevation" - "PoleHeight"
     ```
   - If you made `Elevation_m` in Step 6:
     ```
     "Elevation_m" - "PoleHeight"
     ```
3. **Save edits**.

> Interpretation: If `Elevation` is ellipsoidal from GNSS and you later apply a geoid model, recompute `Elev_Adj` from the corrected elevation. The pole subtraction logic stays the same.

---

## 8) Bring in water depth from handwritten notes
You recorded **water depth** at each wetted station by hand. Add those values to the layer as `Depth_m` in **meters**.

### Option A — Enter manually (fastest for small datasets)
1. Attribute Table → **Toggle editing**.
2. **New field:** `Depth_m` (Decimal, 10/3) → **OK**.
3. Type the depth values row‑by‑row from your notes:
   - If notes are **cm**, type as cm for now, then convert with **Field Calculator**:
     ```
     "Depth_m" / 100
     ```
     into a temporary `Depth_tmp`, then overwrite `Depth_m` = `Depth_tmp`, delete `Depth_tmp`.
   - If notes are **inches**, convert by multiplying by **0.0254**.
4. **Save edits**.

### Option B — Import a CSV from notes and JOIN
1. Make a small CSV from the notebook with keys that exist in your layer (e.g., `StationID`, `DateTime`, `Depth_value`).
2. **Layer → Add Layer → Add Delimited Text Layer…** to load the CSV (no geometry needed).
3. Right‑click your UTM layer → **Joins → +**  
   - **Join layer:** your CSV  
   - **Join field:** `StationID` (and optionally time if multiple visits)  
   - **Target field:** same key in your UTM layer  
   - OK.
4. Open Attribute Table → verify `Depth_value` appears.
5. Create permanent `Depth_m` and copy values:
   ```
   "Depth_value"      -- (if already meters)
   "Depth_value" / 100 -- (if cm)
   "Depth_value" * 0.0254 -- (if inches)
   ```
6. Remove the join if you like (values are now permanent).

**QA tips**
- Sort by `Depth_m` and scan outliers.
- Map styling: graduated symbology on `Depth_m` to spot entry errors.

---

## 9) (Optional) Derive water‑surface elevation from depth
If `Depth_m` is measured **from the water surface to the ground/sensor point**, then:
- **Water surface elevation** per station:
  ```
  WSE_m = "Elev_Adj" + "Depth_m"
  ```
Create a new field `WSE_m` (Decimal) and update with that expression.

If instead you measured **from a fixed staff/sensor elevation**, adjust the formula accordingly (add/subtract to reference).

> Convention: Depth positive **downward**. Ensure your field notes match this convention.

---

## 10) Final checks & housekeeping
- Hover map: the status bar shows UTM meters.  
- **Project → Properties → General → Measurements:** Distance = meters; Area = m².
- **Layer → Properties → Source:** CRS = EPSG:32748.
- Keep the original WGS84 layers archived; do analysis on the UTM layers.

---

## Appendix — Reprojection via GDAL (CLI)
```bash
# If input declares EPSG:4326
ogr2ogr -t_srs EPSG:32748 out.gpkg in.gpkg

# If input missing/incorrect CRS, declare and convert:
ogr2ogr -s_srs EPSG:4326 -t_srs EPSG:32748 out.gpkg in.gpkg
```
GeoPackage preserves CRS inside the file.

---

### Field name summary created/used
- `x_m`, `y_m` — geometry‑derived Easting/Northing (meters).
- `PoleHeight` — pole height (meters).
- `Elevation` (or `Elevation_m`) — elevation in meters.
- `Elev_Adj` — adjusted elevation = `Elevation(_m)` − `PoleHeight`.
- `Depth_m` — water depth (meters) from handwritten notes.
- `WSE_m` (optional) — computed water surface elevation (meters).
