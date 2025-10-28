# Reprojecting a QGIS Project from WGS84 (EPSG:4326) to UTM Zone 48S (EPSG:32748)

Use this when your data are in latitude/longitude (WGS84) and you need meters in **UTM Zone 48S** (Sukabumi/West Java). Follow each step in order.

---

## 0) What you’ll achieve
- A **new copy** of your layers stored in **UTM 48S (EPSG:32748)**
- A project (`.qgz`) configured to **display and measure in meters**
- Optional: permanent **Easting/Northing** columns in your attribute table

---

## 1) Open your project and confirm the source CRS
1. Start **QGIS** and open your project.
2. In the **Layers** panel, right-click a layer you know is in lat/long → **Properties…**.
3. Go to **Source → Geometry → Coordinate reference system** and confirm it says **WGS 84 (EPSG:4326)**.
   - If it’s **wrong or empty** (e.g., “unknown”), fix the declaration:
     - **Layer** menu → **Set Layer CRS…** → choose **WGS 84 (EPSG:4326)** → **OK**.
     *This only tells QGIS what the coordinates mean; it does not convert numbers yet.*
> Repeat this check for each layer that’s supposed to be WGS84.

---

## 2) Set the **Project** CRS to UTM 48S (so maps display correctly)
1. Bottom-right of the QGIS window, click the **CRS/Coordinate** button.
2. Search for **32748** and select **WGS 84 / UTM zone 48S (EPSG:32748)**.
3. Click **OK**.
   - QGIS now **reprojects on the fly** for viewing/measurement, but your layer files are still stored in their original CRS.

---

## 3) Create **actual UTM copies** of your layers (the real reprojection)
For each WGS84 layer that you want in UTM 48S:

1. Right-click the layer → **Export → Save Features As…**
2. **Format:** *GeoPackage* (recommended).
   - Click **…** to choose/create a `.gpkg` file and name the **Layer name** descriptively (e.g., `rivers_utm48s`).
3. **CRS:** click the **CRS** selector → search **32748** → **WGS 84 / UTM zone 48S (EPSG:32748)**.
4. Leave other defaults unless you need to tweak fields/encoding.
5. Click **OK** to export.

You’ll get a **new layer** in the Layers panel with coordinates stored as **meters (Easting/Northing)**.
Repeat for all layers that must live in UTM (points, lines, polygons).

> Tip: If you have many layers, use **Processing → Toolbox → Vector general → Reproject layer** and run it in **Batch**.

---

## 4) Verify the results
1. Toggle the original (WGS84) and the new (UTM) layers on/off—they should **overlay** perfectly.
2. Right-click the **new** layer → **Properties → Source** and confirm **CRS = EPSG:32748**.
3. Hover the map: status bar coordinates should be **Easting/Northing** (meters).

---

## 5) (Optional) Add permanent Easting/Northing fields
If you want explicit columns in the attribute table:

1. Ensure you’re working on the **UTM layer** (not the WGS84 original).
2. Open the **Attribute Table** → click **Toggle editing** (pencil icon).
3. Click **Field Calculator** (Σ icon):
   - **Create a new field**:
     - **Output field name:** `Easting`
     - **Output field type:** *Decimal number (real)*
     - **Precision:** e.g., 3
     - **Expression:** `$x`
   - Click **OK**.
4. Repeat to create **Northing** with expression `$y`.
5. Click **Save edits** → **Toggle editing** to finish.

---

## 6) Point the project to the UTM layers & save
1. Remove or hide the WGS84 layers if you’re done with them.
2. Keep the **Project CRS** set to **EPSG:32748**.
3. **Project → Save** (or **Save As…**) to store your `.qgz` with the UTM setup.

---

## 7) CLI alternative (GDAL)
If you prefer command line or need automation:

```bash
# If your input layer already declares EPSG:4326:
ogr2ogr -t_srs EPSG:32748 out.gpkg in.gpkg

# If your input is missing/incorrect CRS, force input (-s_srs) and convert:
ogr2ogr -s_srs EPSG:4326 -t_srs EPSG:32748 out.gpkg in.gpkg
```

- `out.gpkg` will contain layers stored in **UTM 48S** with CRS embedded in the GeoPackage.

---

## Common pitfalls & fixes
- **“Set Layer CRS” didn’t convert my numbers**
  Correct: it **doesn’t** convert. Use **Export → Save Features As… → CRS: EPSG:32748** to reproject.
- **Wrong hemisphere**
  Java is **south** of the equator → use **EPSG:32748** (not 32648).
- **Mixed CRSs in one map**
  That’s fine for viewing (on-the-fly), but for analysis/buffering/lengths, use layers **stored** in the **same projected CRS**.
- **Losing CRS on export**
  Use **GeoPackage**; it **stores** CRS internally. Always check layer **Properties → Source** after export.

---

### You’re done
Your project and data are now in **UTM Zone 48S**.
