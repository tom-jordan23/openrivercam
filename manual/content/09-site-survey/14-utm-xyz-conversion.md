# 9.14 Survey Data Processing - UTM and XYZ Conversion

This section covers the export and format conversion of survey data for use in PtBox configuration. PtBox requires ground control points in XYZ format - a simple text file with three columns representing Easting, Northing, and Elevation. Converting your surveyed GCPs from SW Maps native format to XYZ point cloud format is a critical step before PtBox camera configuration.

Additionally, this section addresses coordinate reference system (CRS) verification to ensure your data uses the correct UTM zone and that coordinates export properly for spatial analysis.

By the end of this section, you will understand:
- How to export survey data from SW Maps
- How to verify coordinate reference system (CRS) in exported data
- When and how to convert to UTM if needed
- How to generate XYZ point cloud format for PtBox
- File format specifications and quality control
- Troubleshooting common export issues

**Reference:** SURVEY_PROCESS.md Section 10 - PPP & Data Processing, Step 4

---

## Exporting Data from SW Maps

### Export Formats Available

**SW Maps supports multiple export formats:**

**Geopackage (.gpkg) - RECOMMENDED:**
- Industry-standard geospatial format (OGC standard)
- Preserves coordinate reference system (CRS) metadata
- Stores all attribute data with full fidelity
- Single file contains all layers (GCPs, cross-sections, water level, etc.)
- Directly compatible with QGIS and most GIS software

**CSV (.csv) - SIMPLE:**
- Plain text comma-separated values
- Columns: point_id, x_coord, y_coord, z_coord, attributes...
- CRS metadata NOT preserved (coordinates are just numbers)
- Easy to open in spreadsheet software (Excel, LibreOffice)
- Requires manual tracking of CRS information

**Shapefile (.shp) - LEGACY:**
- Older GIS format (still widely supported)
- Preserves CRS metadata (.prj file)
- Multiple files per layer (.shp, .shx, .dbf, .prj)
- Attribute names limited to 10 characters
- Use only if required by specific software compatibility

**KML/KMZ (.kml, .kmz) - GOOGLE EARTH:**
- Google Earth format
- Automatically converts coordinates to WGS84 geographic (latitude/longitude)
- NOT suitable for PtBox (requires UTM, not lat/lon)
- Useful for visualization, not for processing

**For OpenRiverCam workflow, use Geopackage for processing, CSV for PtBox XYZ export.**

### Export Procedure from SW Maps

**Export all survey data to Geopackage:**

**Step 1: Open SW Maps project**
- Launch SW Maps app
- Open survey project (e.g., "Canal_Survey_2024_11_14_Location")

**Step 2: Access export function**
- Menu → Export or Share
- Select layers to export (select all survey layers):
  - Ground Control Points
  - Camera Location
  - Camera FOV
  - Cross Section (Discharge and Level)
  - Water Level
  - Check Points

**Step 3: Choose Geopackage format**
- Export format: GeoPackage (.gpkg)
- Verify CRS: Should show EPSG:32748 (or your configured UTM zone)
- Output filename: `site_name_YYYYMMDD_survey.gpkg`

**Step 4: Save to device storage**
- Choose storage location (internal storage or SD card)
- Export (SW Maps creates Geopackage file)

**Step 5: Transfer to computer**
- Connect Android device via USB
- Copy .gpkg file to computer
- Or upload to cloud storage (Google Drive, Dropbox) and download on computer

**Verify export successful:**
- Check file size (should be 50 KB - 5 MB depending on number of points)
- Open in QGIS to verify data exported correctly

---

## Verifying CRS in Exported Data

### Why CRS Verification is Critical

**Coordinate Reference System (CRS) defines what the coordinate numbers mean:**

**Same physical location can have different coordinates in different CRS:**
```
Location: Survey site in Indonesia

WGS84 Geographic (EPSG:4326):
Latitude:   -5.234567°
Longitude:  104.567890°

UTM Zone 48 South (EPSG:32748):
Easting:    685432.15m
Northing:   9456782.33m

UTM Zone 47 South (EPSG:32747):
Easting:    185432.15m  (500 km different!)
Northing:   9456782.33m
```

**If CRS not defined or incorrect:**
- Coordinates interpreted wrongly (site appears in wrong location)
- PtBox transformation fails (GCPs plotted in wrong positions)
- Integration with other data fails (survey misaligned with satellite imagery)

**The essential rule: Verify CRS immediately after export.**

### CRS Verification in QGIS

**Step 1: Open QGIS**
- Launch QGIS (version 3.x or later)
- File → New Project

**Step 2: Import Geopackage**
- Layer → Add Layer → Add Vector Layer
- Source → select exported .gpkg file
- QGIS lists all layers in Geopackage (select all or desired layers)
- Add layers to map

**Step 3: Check layer CRS**
- Right-click layer (e.g., Ground Control Points) → Properties
- Information tab → Coordinate Reference System
- Verify: EPSG:32748 (or expected UTM zone)

**Example correct CRS display:**
```
Coordinate Reference System:
Name: WGS 84 / UTM zone 48S
Authority: EPSG:32748
Geographic CRS: WGS 84
Datum: WGS 84
Projection: Transverse Mercator
```

**If CRS is correct:**
- Proceed with processing
- CRS preserved through Geopackage export (as designed)

**If CRS is wrong or undefined:**
- See troubleshooting section below
- May need to manually assign CRS or re-configure SW Maps

**Step 4: Visual verification with base map**
- QGIS: Layer → Add Layer → Add XYZ Tiles
- Select base map (Google Satellite, OpenStreetMap, etc.)
- Verify survey points appear in correct geographic location
- Example: Points should overlay river visible in satellite imagery

**If points appear in wrong location:**
- CRS likely incorrect (coordinates misinterpreted)
- Check CRS definition again
- Verify SW Maps project configuration (Section 9.5)

### CRS Verification in CSV Export

**CSV files do NOT contain CRS metadata** - coordinates are just numbers with no context.

**When using CSV export:**

**Step 1: Document CRS externally**
- Create README file: `site_name_YYYYMMDD_CRS.txt`
- Content:
  ```
  Survey Data CRS Information
  Survey Date: 2024-11-14
  Coordinate Reference System: EPSG:32748 (WGS 84 / UTM Zone 48 South)
  Horizontal Units: meters
  Vertical Datum: WGS84 ellipsoid (ellipsoid height)
  ```

**Step 2: Verify coordinates are in expected range**
- UTM Zone 48S Easting: Typically 200,000m to 800,000m
- UTM Zone 48S Northing (Southern Hemisphere): Typically 9,000,000m to 10,000,000m (large values because southern hemisphere uses false northing)
- Elevation: Typically -10m to +300m above WGS84 ellipsoid for Indonesia lowland sites

**Example verification:**
```
point_id    x_coord      y_coord       z_coord
--------    ---------    ----------    -------
GCP_01      685432.15    9456782.33    139.25
GCP_02      685435.20    9456785.10    139.45
GCP_03      685440.50    9456780.55    140.15
```

- x_coord (Easting) in 685xxx range ✓ (valid for UTM 48S)
- y_coord (Northing) in 9456xxx range ✓ (valid for Southern Hemisphere UTM)
- z_coord in 139-140m range ✓ (reasonable elevation)

**If coordinates out of expected range:**
- Check CRS configuration in SW Maps
- Verify export settings
- Coordinates may be in wrong CRS (e.g., lat/lon instead of UTM)

---

## Converting to UTM (If Needed)

### When Conversion is Needed

**Most common scenarios requiring CRS conversion:**

**Scenario 1: Data exported in WGS84 Geographic (lat/lon)**
- SW Maps misconfigured (used EPSG:4326 instead of UTM)
- Coordinates appear as small decimal numbers (-5.234567, 104.567890)
- Need to convert to UTM (meters)

**Scenario 2: Wrong UTM zone**
- Configured as Zone 47 instead of Zone 48 (or vice versa)
- Easting values offset by ~500km (wrong zone)
- Need to reproject to correct zone

**Scenario 3: Local coordinate system**
- Survey used local CRS specific to country or region
- PtBox or analysis requires WGS84 UTM
- Need transformation to WGS84 UTM

**If data already in correct UTM zone (verified in previous section):**
- No conversion needed (skip this section)
- Proceed directly to XYZ export

### Conversion in QGIS

**Method: Reproject layer to correct CRS**

**Step 1: Import layer with incorrect CRS**
- Add Vector Layer → select Geopackage or Shapefile
- QGIS imports with original CRS (e.g., EPSG:4326 or wrong UTM zone)

**Step 2: Reproject layer**
- Right-click layer → Export → Save Features As
- Format: Geopackage (or CSV, depending on next step)
- File name: `site_name_YYYYMMDD_survey_UTM48S.gpkg`
- CRS: Click Select CRS button

**Step 3: Select target CRS**
- Search: 32748 (for UTM Zone 48 South)
- Or search: "UTM 48S"
- Select: WGS 84 / UTM zone 48S (EPSG:32748)
- OK

**Step 4: Export reprojected layer**
- Click OK (QGIS reprojects coordinates and saves to new file)
- Original layer unchanged (new file contains reprojected coordinates)

**Step 5: Verify reprojection**
- Add new layer to QGIS
- Check CRS: Should now be EPSG:32748
- Check coordinates: Should be UTM meters (e.g., 685432.15, 9456782.33)
- Verify with base map: Points should align correctly with satellite imagery

**Example coordinate transformation:**
```
Original (EPSG:4326, WGS84 Geographic):
Longitude: 104.567890°
Latitude:  -5.234567°

Reprojected (EPSG:32748, UTM 48S):
Easting:   685432.15m
Northing:  9456782.33m
```

### Alternative: Coordinate Conversion Tools

**If not using QGIS:**

**Online coordinate conversion:**
- https://epsg.io/transform (EPSG.io Coordinate Converter)
- Input CRS: EPSG:4326 (or source CRS)
- Output CRS: EPSG:32748 (or target CRS)
- Paste coordinates (lat, lon), convert to (E, N)

**Command-line tools (for batch conversion):**
- GDAL ogr2ogr: `ogr2ogr -f "GPKG" output.gpkg input.gpkg -t_srs EPSG:32748`
- PROJ cs2cs: `cs2cs EPSG:4326 EPSG:32748` (pipe coordinates for conversion)

**Spreadsheet with formulas (approximate, for small areas):**
- UTM projection formulas can be implemented in Excel
- Complex formulas, error-prone
- Not recommended (use QGIS or GDAL instead)

---

## Generating XYZ Point Cloud for PtBox

### XYZ File Format Specification

**XYZ format is simple text file with three columns:**

```
X           Y           Z
685432.15   9456782.33  139.25
685435.20   9456785.10  139.45
685440.50   9456780.55  140.15
685438.30   9456778.20  139.65
685442.80   9456783.45  140.05
685445.10   9456781.90  140.25
```

**Format specifications:**
- **Column 1 (X):** Easting (UTM meters)
- **Column 2 (Y):** Northing (UTM meters)
- **Column 3 (Z):** Elevation (meters above datum)
- **Delimiter:** Space, tab, or comma (space or tab recommended)
- **Header:** Optional (first row can be "X Y Z" or omitted)
- **Decimal precision:** 2-3 decimal places (centimeter resolution)
- **Units:** Meters (no unit labels in file, meters assumed)

**PtBox expects:**
- Ground control points only (not entire cross-section)
- Coordinates in UTM (not lat/lon)
- Elevations as ellipsoid heights or geoid heights (consistent with how PtBox is configured)

### Export XYZ from QGIS

**From SURVEY_PROCESS.md Section 10, Step 4:**
```
Create XYZ Point Cloud:
- Select cross-section and control point layers from corrected Geopackage
- Right-click layer → Export → Save Features As
- Format: "Comma Separated Value [CSV]"
- Geometry: AS_XYZ (exports X,Y,Z coordinates)
- Layer options: GEOMETRY=AS_XYZ, CREATE_CSVT=NO
```

**Detailed procedure:**

**Step 1: Select Ground Control Points layer**
- In QGIS Layers panel, right-click "Ground Control Points" layer
- Export → Save Features As

**Step 2: Configure CSV export with XYZ geometry**
- Format: Comma Separated Value [CSV]
- File name: `site_name_YYYYMMDD_GCP.xyz` (use .xyz extension)
- CRS: EPSG:32748 (or correct UTM zone, should already be set)
- Layer Options → click "Add layer options" button
- Add option: `GEOMETRY=AS_XYZ`
- Add option: `CREATE_CSVT=NO` (suppresses type definition file)
- Click OK

**Step 3: QGIS exports XYZ file**
- File created: `site_name_YYYYMMDD_GCP.xyz`
- Open in text editor to verify format

**Step 4: Verify XYZ file format**

**Open file in text editor (Notepad++, Sublime, VS Code):**
```
X,Y,Z
685432.15,9456782.33,139.25
685435.20,9456785.10,139.45
685440.50,9456780.55,140.15
685438.30,9456778.20,139.65
685442.80,9456783.45,140.05
685445.10,9456781.90,140.25
```

**Format check:**
- First row: Header (X,Y,Z) - if present, PtBox may require you to skip first row during import, or delete header row
- Data rows: Three columns (X, Y, Z) separated by commas
- Coordinates in UTM meters (not lat/lon degrees)
- Decimal precision: 2-3 decimal places

**Optional: Convert delimiter from comma to space**

Some software prefers space-delimited XYZ. Convert in text editor (find and replace):
- Find: `,` (comma)
- Replace: ` ` (space)
- Result:
  ```
  X Y Z
  685432.15 9456782.33 139.25
  685435.20 9456785.10 139.45
  ...
  ```

**Or delete header row if PtBox does not expect it:**
```
685432.15 9456782.33 139.25
685435.20 9456785.10 139.45
685440.50 9456780.55 140.15
...
```

**Save modified file** (same filename or new filename).

### Alternative: Export XYZ from Spreadsheet

**If using CSV export from SW Maps (not Geopackage):**

**Step 1: Open CSV in spreadsheet software**
- Import: `site_name_YYYYMMDD_GCP.csv`
- Columns include: point_id, x_coord, y_coord, z_coord, attributes...

**Step 2: Create XYZ columns**
- Select three columns: x_coord, y_coord, z_coord
- Copy to new sheet or new file

**Step 3: Export as text**
- File → Save As → Text (Tab delimited) or CSV
- Filename: `site_name_YYYYMMDD_GCP.xyz`
- Format: Include only X, Y, Z columns (no attributes)

**Step 4: Verify format in text editor**
- Open .xyz file
- Check columns, delimiter, precision

---

## Quality Control for XYZ Export

### Verification Checks

**Check 1: Correct number of points**

**Verify point count:**
- Count rows in XYZ file (excluding header row)
- Compare to number of GCPs surveyed (should match)
- Example: Surveyed 6 GCPs → XYZ file should have 6 data rows

**If point count wrong:**
- Check layer selection in export (all GCPs selected?)
- Check for duplicates (same GCP exported twice)
- Check for missing points (GCP not saved during survey)

**Check 2: Coordinate values in expected range**

**UTM coordinate ranges (Zone 48S example):**
- Easting: 200,000m to 800,000m (typical)
- Northing: 9,000,000m to 10,000,000m (Southern Hemisphere)
- Elevation: -10m to +500m (depends on site)

**If coordinates out of range:**
- Wrong CRS (data in lat/lon instead of UTM)
- Wrong UTM zone (coordinates shifted by zone width)
- Data corruption (decimal point misplaced, digits missing)

**Check 3: No duplicate points**

**Verify unique coordinates:**
- Sort XYZ file by X, then Y
- Check for rows with identical X, Y, Z values (duplicates)
- Duplicates may cause errors in PtBox transformation

**If duplicates found:**
- Delete duplicate rows (keep one copy)
- Or verify in source data (are two GCPs at same location?)

**Check 4: Consistent decimal precision**

**Verify precision:**
- All coordinates to same decimal places (e.g., all 2 decimals: 685432.15)
- Elevation precision: 2-3 decimals typical (centimeter resolution)

**Example inconsistent precision (poor quality):**
```
685432.15   9456782.33   139.25    ✓ Good (2 decimals)
685435.2    9456785.1    139.4     ✗ Bad (inconsistent, 1 decimal)
685440.501  9456780.553  140.152   ✗ Overkill (3 decimals for mm, exceeds measurement accuracy)
```

**Standardize precision:**
- Round to 2-3 decimals (centimeter resolution matches survey accuracy)

---

## File Format for PtBox Import

### PtBox Ground Control Point Requirements

**PtBox configuration requires:**

**Ground control points in image:**
- Visible markers in camera field of view (surveyed during Section 9.8)
- Click GCP locations in image (pixel coordinates)
- Provide real-world coordinates (from survey XYZ file)

**PtBox matches image pixel coordinates to real-world coordinates:**
- Image: (pixel_x, pixel_y) for each GCP
- Real-world: (UTM_E, UTM_N, Z) from XYZ file
- Calculates transformation: Image coordinates ↔ Real-world coordinates

**XYZ file provides real-world coordinates for transformation:**

**Import process in PtBox:**
1. Load XYZ file (or manually enter coordinates)
2. For each GCP: Click location in image
3. Associate image point with real-world coordinates from XYZ
4. PtBox calculates camera parameters (position, orientation, lens distortion)
5. Transformation validates: Reprojection errors reported

**File format compatibility:**

**PtBox typically accepts:**
- Plain text XYZ (space-delimited or comma-delimited)
- Optional header row (may need to skip)
- Units: Meters (assumed)

**If PtBox import fails:**
- Check delimiter (try space instead of comma, or vice versa)
- Remove header row (some software expects data only, no labels)
- Verify column order (X, Y, Z vs. Y, X, Z - some software uses northing-easting order)
- Check for special characters (units labels, extra columns)

**Consult PtBox documentation for specific format requirements** (format preferences vary between software versions).

---

## Common Issues and Solutions

### Issue: Coordinates in Lat/Lon Instead of UTM

**Symptom:** XYZ file contains small decimal numbers (e.g., 104.567890, -5.234567)

**Cause:** Data exported in EPSG:4326 (WGS84 Geographic) instead of UTM

**Solution:**
- Reproject data to correct UTM zone in QGIS (see "Converting to UTM" section)
- Re-export XYZ with corrected CRS

### Issue: Wrong UTM Zone

**Symptom:** Coordinates in UTM format but easting values offset by 500 km

**Cause:** Data in adjacent UTM zone (e.g., Zone 47 instead of 48)

**Solution:**
- Verify correct UTM zone for site (calculate from longitude)
- Reproject to correct zone in QGIS
- Re-export XYZ

### Issue: Missing Elevation Values

**Symptom:** XYZ file has X and Y columns but Z column empty or zero

**Cause:**
- 2D survey (only horizontal positions collected, no elevation)
- Z coordinate not saved during survey
- Export setting excludes Z dimension

**Solution:**
- Verify survey included elevation (RTK should provide 3D positions)
- Check SW Maps export: Ensure 3D geometry exported (not 2D)
- If elevations truly missing: Cannot create valid XYZ (must resurvey)

### Issue: File Import Fails in PtBox

**Symptom:** PtBox cannot read XYZ file (error during import)

**Causes and solutions:**

**Delimiter mismatch:**
- Try different delimiter (space vs. comma vs. tab)
- Edit file in text editor, change delimiter

**Header row unexpected:**
- PtBox expects data only, no header
- Delete first row (X,Y,Z header)

**Column order wrong:**
- Some software expects Y,X,Z (northing, easting, elevation)
- Swap columns in spreadsheet and re-export

**Units not in meters:**
- Data in feet instead of meters
- Convert all coordinates: meters = feet / 3.28084

**File encoding issues:**
- File saved with wrong text encoding (UTF-16 instead of UTF-8, or with BOM)
- Re-save as UTF-8 without BOM in text editor

---

## Summary: UTM and XYZ Conversion

**Purpose:**
- Export survey data from SW Maps in usable format
- Verify coordinate reference system (CRS) correctness
- Convert to XYZ point cloud format for PtBox GCP import
- Enable camera transformation configuration

**Key steps:**

1. **Export from SW Maps:**
   - Geopackage format preferred (preserves CRS)
   - CSV format acceptable (track CRS separately)

2. **Verify CRS:**
   - Check in QGIS: Layer properties → CRS
   - Expected: EPSG:32748 or appropriate UTM zone
   - Visual check: Overlay with satellite base map

3. **Convert to UTM if needed:**
   - Reproject in QGIS: Export → Save Features As → Select target CRS
   - Verify coordinate ranges (UTM meters, not lat/lon degrees)

4. **Generate XYZ file:**
   - Export GCP layer as CSV with GEOMETRY=AS_XYZ
   - Format: Three columns (X, Y, Z) in UTM meters
   - Save as .xyz file (space or comma delimited)

5. **Quality control:**
   - Correct point count (matches surveyed GCPs)
   - Coordinates in expected range (UTM zone values)
   - No duplicates
   - Consistent decimal precision (2-3 decimals)

**File format for PtBox:**
- Plain text XYZ (X, Y, Z columns)
- UTM coordinates in meters
- Elevations in meters
- Optional header row (may need to remove)

**Workflow position:**
- **COMPLETED:** Pole height adjustment, water level calculation
- **CURRENT:** UTM and XYZ conversion (prepare data for PtBox)
- **NEXT:** PPP corrections (Section 9.15, improve absolute accuracy before PtBox import)

**Note:** Section 9.15 (PPP Corrections) is typically performed BEFORE final XYZ export for PtBox. The workflow sequence is:
1. Export raw survey data (this section, preliminary)
2. Apply PPP corrections (Section 9.15, improve coordinates)
3. Re-export corrected XYZ (this section, final)
4. Import to PtBox (camera configuration)

The procedures in this section apply both to preliminary exports (for quality checking) and final exports (after PPP corrections applied).

---

**Next Section:** [9.15 Survey Data Processing - PPP Corrections](15-ppp-corrections.md) - THE CRITICAL POST-PROCESSING WORKFLOW
