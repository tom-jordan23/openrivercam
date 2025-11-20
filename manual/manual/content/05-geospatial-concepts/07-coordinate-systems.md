# 5.7 Coordinate Systems (UTM, Local, Global)

You have surveyed your river site with RTK GPS and achieved centimeter-level accuracy. Your receiver reports positions as numbers: Easting 501234.567m, Northing 9876543.210m, Elevation 123.456m. But what do these numbers actually mean? How do they relate to the curved surface of the Earth? Why does SURVEY_PROCESS.md specify "EPSG:32748" for your survey project?

This section explains coordinate reference systems (CRS) - the mathematical frameworks that turn GPS measurements into usable positions. Understanding coordinate systems helps you:
- Choose the correct CRS for your survey project
- Avoid positioning errors when combining data from different sources
- Understand why coordinates look different in different software
- Correctly configure GPS equipment and GIS software
- Integrate OpenRiverCam data with satellite imagery and maps

**Complexity warning:** Coordinate systems involve abstract mathematical concepts (projections, datums, ellipsoids). However, the practical application is straightforward: Use UTM for the zone containing your survey site, maintain consistent CRS throughout your workflow, and understand when coordinate transformations are needed.

This section provides essential knowledge without requiring mathematical expertise. You will understand what coordinate systems are, why they matter, and how to use them correctly for OpenRiverCam surveys.

---

## What is a Coordinate Reference System?

A Coordinate Reference System (CRS) is a standardized method for describing positions on Earth using numbers.

### The Fundamental Problem: Representing a Sphere with Numbers

**The challenge:**
- Earth is (approximately) a sphere
- GPS satellites orbit Earth in 3D space
- We need to record positions as numbers that can be stored, analyzed, mapped
- Maps and computer screens are flat (2D)
- We need coordinates that are convenient for measuring distances, areas, angles

**The solution:** Different coordinate reference systems solve different parts of this problem.

**Three types of coordinate systems:**

**1. Geographic coordinates (latitude/longitude):**
- Describe positions directly on the curved Earth surface
- Natural for GPS (satellites measure angles to receiver)
- Example: 6.1234° South, 106.7890° East
- Problem: Distances and areas are difficult to calculate (requires spherical trigonometry)

**2. Geocentric coordinates (X, Y, Z):**
- Earth-centered 3D Cartesian system
- Used internally by GPS satellites and receivers
- Example: X = -1,234,567m, Y = 5,678,901m, Z = -2,345,678m
- Problem: Not intuitive for mapping or fieldwork

**3. Projected coordinates (Easting/Northing):**
- Mathematical projection of curved Earth surface onto flat plane
- Enables simple distance calculations (Pythagorean theorem works)
- Example: Easting = 501234.567m, Northing = 9876543.210m
- **This is what OpenRiverCam surveys use** (UTM projection)
- Tradeoff: Projections introduce distortions (small for local surveys)

**For OpenRiverCam field surveys, you use projected coordinates (UTM)** because:
- Easy distance and area calculations needed for GCP layout, cross-section analysis
- Compatible with engineering/GIS software
- Minimizes distortion for areas smaller than a UTM zone (~1 million km²)
- Standard for professional surveying and mapping

---

## Geographic vs Projected Coordinates

Understanding the difference between geographic and projected coordinates is essential for working with geospatial data.

### Geographic Coordinates: Latitude and Longitude

**What they are:**
- Angles measured from Earth's center
- **Latitude:** Angle north/south of equator (0° at equator, ±90° at poles)
- **Longitude:** Angle east/west of Prime Meridian (0° through Greenwich, UK, ±180° at International Date Line)
- Units: Degrees (often subdivided: decimal degrees, or degrees/minutes/seconds)

**Example location (Jakarta, Indonesia):**
- Latitude: 6.2088° South (negative in decimal: -6.2088°)
- Longitude: 106.8456° East (positive in decimal: 106.8456°)

**Advantages:**
- Universally understood global system
- Natural output from GPS satellites (which measure angles)
- No arbitrary boundaries (works anywhere on Earth)
- Simple to specify location uniquely

**Disadvantages:**
- **Cannot directly measure distances:** Distance between 6.0°S, 106.0°E and 6.1°S, 106.1°E is NOT the same as distance between 80.0°S, 106.0°E and 80.1°S, 106.1°E (degree spacing varies with latitude)
- **Cannot use simple geometry:** Pythagorean theorem does not work (Earth is curved)
- **Difficult area calculations:** Requires spherical trigonometry
- **Distorted mapping:** If you plot lat/lon directly on flat map, shapes are severely distorted (especially near poles)

**When to use geographic coordinates:**
- Global-scale mapping or analysis
- Data exchange between regions (no projection-specific limits)
- GPS raw output (before transformation)
- Web mapping (Google Maps, OpenStreetMap use lat/lon internally, displayed in Web Mercator projection)

### Projected Coordinates: Easting and Northing

**What they are:**
- Results from mathematically projecting curved Earth surface onto flat plane
- **Easting:** Distance east from an arbitrary origin (false easting), typically in meters
- **Northing:** Distance north from an arbitrary origin (false northing), typically in meters
- Units: Meters (or sometimes feet in older US systems)

**Example location (same Jakarta point in UTM Zone 48S):**
- Easting: 723,896 m (distance east of zone's central meridian)
- Northing: 9,313,021 m (distance north of equator, in southern hemisphere uses false northing)

**Advantages:**
- **Simple distance calculations:** Distance = √[(E₂-E₁)² + (N₂-N₁)²] (Pythagorean theorem)
- **Easy area calculations:** Area of polygon using simple coordinate geometry
- **Intuitive for fieldwork:** "Walk 50 meters east" is straightforward
- **Compatible with engineering tools:** CAD, surveying software expect projected coordinates
- **Accurate for local areas:** Within projection zone, distortions are minimal (<0.1% for UTM)

**Disadvantages:**
- **Limited geographic extent:** Each projection has valid area (e.g., one UTM zone)
- **Distortions at edges:** Accuracy degrades far from projection's central region
- **Zone boundaries:** Must change CRS when crossing zone boundaries
- **Not intuitive globally:** Easting 501234m is meaningless without knowing which projection and zone

**When to use projected coordinates:**
- Local to regional surveying and mapping
- Engineering projects (infrastructure design, construction)
- Accurate distance and area measurements
- GIS analysis requiring metric measurements
- **OpenRiverCam surveys** (field surveys typically <10 km extent, well within one UTM zone)

### Real-World Example: Why Projection Matters

**Scenario:** You survey river cross-section with 10 survey points spanning 200 meters.

**Using geographic coordinates (lat/lon):**
- Point 1: 6.123450°S, 106.789000°E
- Point 10: 6.123480°S, 106.789180°E
- **Calculate distance:** Complex spherical trigonometry required. Small errors if you naively compute √[(lat₂-lat₁)² + (lon₂-lon₁)²] because degrees are not constant distances.

**Using projected coordinates (UTM 48S):**
- Point 1: E=501234.567m, N=9876543.210m
- Point 10: E=501434.123m, N=9876509.876m
- **Calculate distance:** √[(501434.123-501234.567)² + (9876509.876-9876543.210)²] = √[199.556² + (-33.334)²] = 202.3 meters
- Simple, accurate, no special functions needed

**For OpenRiverCam analysis** (camera calibration, discharge calculations, bathymetry), you need many distance and area calculations. Projected coordinates (UTM) make this practical and accurate.

---

## The UTM Projection System

UTM (Universal Transverse Mercator) is the most widely used projected coordinate system for regional surveying and mapping. OpenRiverCam surveys use UTM.

### What is UTM?

**Universal Transverse Mercator (UTM):**
- A worldwide coordinate system dividing Earth into 60 longitude zones (each 6° wide)
- Each zone uses Transverse Mercator projection (optimized for north-south oriented regions)
- Provides accurate metric coordinates for areas within each zone
- Coordinates expressed as Easting (meters east from zone's central meridian) and Northing (meters north from equator)

**Key characteristics:**
- **60 zones:** Numbered 1 to 60, starting at 180°W (International Date Line), proceeding eastward
- **Each zone:** 6° longitude wide
- **Two hemispheres:** Northern hemisphere (N) and Southern hemisphere (S) separate
- **Coordinates always positive:** Uses "false easting" (500,000m) and "false northing" (southern hemisphere: 10,000,000m) to avoid negative numbers

**Example zone coverage:**
- UTM Zone 1: 180°W to 174°W (Alaska, Pacific)
- UTM Zone 30: 6°W to 0° (UK, Western Africa)
- **UTM Zone 48: 102°E to 108°E (Indonesia, Malaysia, Thailand)**
- UTM Zone 60: 174°E to 180°E (Russia, Pacific)

**Northern vs Southern hemisphere:**
- **Northern zones:** Northing measured from equator (Northing=0 at equator, increases northward)
- **Southern zones:** Northing uses false northing of 10,000,000m at equator (decreases southward from 10,000,000m to avoid negatives)

### UTM Zone Selection for Your Survey

**From SURVEY_PROCESS.md, OpenRiverCam surveys use UTM Zone 48 South (EPSG:32748).**

**Why UTM Zone 48S?**
- Covers 102°E to 108°E longitude (includes Jakarta, most of western Indonesia)
- Southern hemisphere (most Indonesian rivers south of equator)
- Optimal accuracy for this region (minimal distortion within zone)

**How to determine correct UTM zone for your location:**

**Method 1: Online UTM zone map**
- Search "UTM zone map" or "UTM zone finder"
- Locate your survey site on map
- Read zone number and hemisphere

**Method 2: Calculate from longitude**
- Zone number = ⌊(Longitude + 180) / 6⌋ + 1
- Example: Longitude = 106.7890°E
  - (106.7890 + 180) / 6 = 47.798
  - Floor(47.798) + 1 = 48
  - **Zone = 48**
- Hemisphere: Latitude > 0 = North, Latitude < 0 = South
  - Example: Jakarta at 6.2088°S → **Southern hemisphere**
  - **Result: UTM Zone 48 South**

**Method 3: Use GIS software**
- Open location in QGIS, Google Earth, or similar
- Read coordinates in UTM (software often auto-detects zone)
- Verify zone number and hemisphere

**Important: Use the zone containing your base station position.** If your survey area is small (<10 km extent), it will be entirely within one zone.

### UTM Coordinate Format

**Standard UTM coordinates consist of:**

**Zone + Hemisphere + Easting + Northing**

**Example (survey point in Jakarta):**
- Zone: 48
- Hemisphere: South (S)
- Easting: 501,234.567 m
- Northing: 9,876,543.210 m
- Full coordinate: **48S 501234.567mE 9876543.210mN**

**Easting explained:**
- Measures distance east from zone's central meridian
- False easting = 500,000m (central meridian assigned 500,000m, not 0m)
- This makes all Easting values positive (west of central meridian: <500,000m, east of central meridian: >500,000m)
- Range within zone: ~160,000m to ~840,000m (depending on latitude)

**Northing explained (Southern hemisphere):**
- Measures distance from equator (southern hemisphere uses false northing)
- False northing = 10,000,000m at equator (to keep values positive)
- Northing decreases as you go south from equator
- Example: Northing 9,876,543m means ~123 km south of equator (10,000,000 - 9,876,543 = 123,457m)

**EPSG code:**
- EPSG (European Petroleum Survey Group) codes uniquely identify CRS
- **EPSG:32748 = WGS84 / UTM Zone 48 South**
- EPSG codes remove ambiguity (software knows exact projection, datum, zone, hemisphere from single number)
- Other examples: EPSG:32648 = UTM Zone 48 North, EPSG:4326 = WGS84 geographic (lat/lon)

**Always specify EPSG code in GIS software and data files** to ensure correct coordinate interpretation.

### UTM Accuracy and Limitations

**Accuracy within zone:**
- **Scale distortion:** <0.04% at central meridian, <0.1% at zone edges (3° from central meridian)
- **Distance error:** <1m per 1000m measured (for area spanning full zone width)
- **For typical survey (<10km extent):** Distortion negligible (<1cm over 1km)

**Practical rule:** UTM provides survey-grade accuracy (millimeter to centimeter level) for projects within a single zone.

**Limitations:**

**1. Zone boundaries:**
- UTM zones overlap slightly, but coordinates are discontinuous at boundaries
- If survey crosses zone boundary, must choose one zone (typically where base station located)
- Do not mix coordinates from different zones without transformation

**2. Polar regions:**
- UTM not defined above 84°N or below 80°S
- Polar regions use UPS (Universal Polar Stereographic) instead
- Not relevant for OpenRiverCam (humanitarian water programs typically in temperate/tropical regions)

**3. Large-scale projects:**
- Continental or global mapping requires different projections (or multiple zones)
- For projects spanning >1,000 km east-west, consider alternative projections (Lambert Conformal Conic, Albers Equal Area, etc.)

**4. Distortion type:**
- Transverse Mercator preserves shape (conformal projection) but distorts area slightly
- For area-intensive work spanning large regions, equal-area projections may be preferred
- For OpenRiverCam surveys: Shape preservation is valuable (cross-sections, GCP layouts), area distortion is negligible

---

## Datums: WGS84 and Local Reference Frames

In addition to choosing a projection (like UTM), you must specify a **datum** - the mathematical model of Earth's shape and size used as the reference surface.

### What is a Geodetic Datum?

**A geodetic datum defines:**

**1. Reference ellipsoid:**
- Mathematical model of Earth's shape (ellipsoid = slightly flattened sphere)
- Defined by two parameters: semi-major axis (equatorial radius) and flattening
- Example: WGS84 ellipsoid has equatorial radius 6,378,137m, polar radius 6,356,752m
- Different ellipsoids fit different regions of Earth better (Earth is not a perfect ellipsoid)

**2. Origin and orientation:**
- Where is the center of the ellipsoid? (usually Earth's center of mass)
- How is the ellipsoid oriented? (rotation axes aligned with Earth's rotation axis)

**3. Relationship to physical features:**
- How does ellipsoid relate to mean sea level (geoid)?
- Reference points (fundamental stations) with precisely known coordinates

**Why datums matter:**
- Same lat/lon coordinates on different datums can differ by meters to hundreds of meters
- GPS uses WGS84 datum; local maps may use regional datums (NAD83, GDA2020, etc.)
- **Using wrong datum = systematic position errors**

**Analogy:** Think of datum as choosing which globe model you use. If you use a globe manufactured in 1950 (old datum, before satellite measurements) vs. a modern GPS-measured globe (WGS84), the same city might be marked 50 meters apart on the two globes because the models have slightly different sizes and orientations.

### WGS84: The GPS Standard Datum

**WGS84 (World Geodetic System 1984):**
- Global datum used by GPS satellites
- Defined by US Department of Defense, maintained by National Geospatial-Intelligence Agency
- Origin: Earth's center of mass
- Orientation: Aligned with Earth's rotation axis and Greenwich meridian
- Reference ellipsoid: Semi-major axis = 6,378,137m, flattening = 1/298.257223563

**Why WGS84 is standard:**
- GPS satellites broadcast positions in WGS84 coordinates
- All GPS receivers output WGS84 coordinates (unless manually transformed)
- **For RTK surveys with modern GPS equipment, you use WGS84 datum**
- Global consistency (coordinates mean the same thing worldwide)
- Continuously updated (WGS84 has minor revisions: WGS84(G730), WGS84(G1762), etc., differences <1cm)

**EPSG:32748 = WGS84 / UTM Zone 48 South** means:
- Projection: UTM Zone 48 South
- Datum: WGS84
- Both specified together define complete CRS

### Local and Regional Datums

Before GPS, countries established local datums optimized for their region:

**Examples of local datums:**
- **NAD83 (North American Datum 1983):** Used in USA, Canada, Mexico
- **ETRS89 (European Terrestrial Reference System 1989):** Used in Europe
- **GDA2020 (Geocentric Datum of Australia 2020):** Used in Australia
- **JGD2011 (Japanese Geodetic Datum 2011):** Used in Japan
- **ITRF (International Terrestrial Reference Frame):** Global geodetic reference, updated periodically (ITRF2014, ITRF2020)

**Differences from WGS84:**
- Most modern regional datums are very similar to WGS84 (differences <2 meters globally, often <50cm regionally)
- Older local datums (pre-GPS) can differ by tens to hundreds of meters
- **NAD83 vs. WGS84:** ~1-2 meters difference in North America (varies by location and time)
- **GDA2020 vs. WGS84:** <5cm difference (essentially identical for most applications)

**Why local datums exist:**
- Better fit to Earth in specific region (reduces ellipsoid-to-geoid separation)
- Consistency with existing infrastructure (maps, cadastral records from pre-GPS era)
- Government standards and legal requirements
- Integration with national reference networks (control points)

**For OpenRiverCam surveys in Indonesia:**
- GPS equipment outputs WGS84 coordinates
- Indonesian national datum is DGN95 (Datum Geodesi Nasional 1995) - differs from WGS84 by ~1-2 meters
- **Use WGS84/UTM 48S (EPSG:32748) for field surveys** (GPS native datum)
- Transform to local datum only if required for integration with government mapping or engineering projects

### Datum Transformations

**When you need datum transformation:**
- Combining GPS survey data (WGS84) with older maps (local datum)
- Meeting government requirements (cadastral surveying often requires national datum)
- Integrating with engineering plans (may be in local datum)

**How datum transformation works:**
- Mathematical conversion between ellipsoids
- Accounts for position shifts (translation), rotation, and scale differences
- Can be simple (3-parameter Helmert transformation) or complex (7-parameter, grid-based)

**Tools for datum transformation:**
- GIS software (QGIS, ArcGIS): Built-in reprojection tools
- Online calculators: National geodetic agencies provide transformation services
- GPS post-processing software: RTKLIB, commercial packages
- Coordinate conversion utilities: PROJ library, CS2CS command-line tool

**Critical: Always verify transformation accuracy:**
- Check results against known control points
- Transformation accuracy varies (modern datums: <10cm, old datums: 1-5 meters)
- Document transformations applied (for data provenance and QA)

**Practical guidance for OpenRiverCam:**
- Configure GPS equipment and SW Maps to **WGS84/UTM Zone 48S (EPSG:32748)**
- Maintain this CRS throughout survey workflow (equipment → data collection → QGIS analysis → PtBox)
- Only transform to local datum if external integration explicitly requires it
- **Consistency prevents coordinate errors** - use one CRS for entire project

---

## Choosing the Right CRS for Your Project

Different projects have different coordinate system requirements. This section helps you make informed choices.

### CRS Selection Criteria

**Consider these factors when selecting CRS:**

**1. Project extent:**
- **Local (<100 km):** UTM zone containing area (best accuracy)
- **Regional (100-1000 km):** UTM or region-specific projection (Lambert Conformal Conic, Albers)
- **National (>1000 km):** National standard projection or multiple UTM zones
- **Global:** Geographic coordinates (lat/lon) or specialized global projections (Web Mercator for display, equal-area projections for analysis)

**2. Integration requirements:**
- What CRS do existing datasets use? (satellite imagery, government maps, LiDAR, etc.)
- What CRS do collaborating organizations use?
- Are there legal/regulatory requirements? (cadastral surveys, official mapping)

**3. Measurement needs:**
- **Distance/area calculations:** Projected coordinates (UTM, Lambert, etc.)
- **Global coverage:** Geographic coordinates (lat/lon)
- **Shape preservation:** Conformal projections (UTM, Lambert)
- **Area preservation:** Equal-area projections (Albers, Lambert Azimuthal Equal-Area)

**4. Software compatibility:**
- What CRS does your GIS software default to?
- What CRS does data exchange format require? (some formats assume specific CRS)
- What CRS do stakeholders expect? (government agencies, engineering firms)

**5. Precision requirements:**
- **Survey-grade (<5cm):** Use UTM for zone containing site
- **Mapping-grade (0.5-5m):** Most projections adequate
- **Visualization only:** Any reasonable projection works

### Recommended CRS for OpenRiverCam Surveys

**For field surveys in western Indonesia:**

**Primary CRS: EPSG:32748 (WGS84 / UTM Zone 48 South)**

**Rationale:**
- UTM provides accurate metric coordinates (distance/area calculations for GCP layout, cross-sections)
- Zone 48 covers 102°E-108°E (Jakarta, Sumatra, western Java)
- Southern hemisphere (most Indonesian rivers south of equator)
- WGS84 datum (GPS native, no transformation needed)
- Standard for professional surveying
- Minimal distortion for survey areas <10km extent

**Alternative CRS for other regions:**

**Eastern Indonesia (109°E-114°E):**
- **EPSG:32749 (WGS84 / UTM Zone 49 South)** - covers Kalimantan, Java east of 108°E

**Far eastern Indonesia (115°E-120°E):**
- **EPSG:32750 (WGS84 / UTM Zone 50 South)** - covers Sulawesi, Bali, Nusa Tenggara

**Northern hemisphere surveys (rare for Indonesia):**
- **EPSG:32648 (WGS84 / UTM Zone 48 North)** - for areas north of equator

**To determine UTM zone:**
1. Note base station longitude from GPS
2. Calculate zone: ⌊(Longitude + 180) / 6⌋ + 1
3. Determine hemisphere from latitude (North if >0, South if <0)
4. Look up EPSG code: 326NN for North, 327NN for South (NN = zone number)

**Verify your selection:**
- Check that entire survey area is within selected zone (survey extent <10km almost always within one zone)
- Verify software supports EPSG code (virtually all modern GIS supports UTM)
- Confirm consistency: All survey equipment, software, and analysis use same CRS

### Common CRS Mistakes and How to Avoid Them

**Mistake 1: Mixing CRS within project**

**Problem:**
- Base station configured to UTM Zone 48S
- SW Maps accidentally set to WGS84 geographic (lat/lon)
- Survey points exported with mixed coordinate types
- GIS analysis fails or produces nonsense results (treats lat/lon as meters)

**Solution:**
- **Configure all systems to same CRS before starting survey**
- Verify: GPS base station configuration → GNSS Master → SW Maps → QGIS project
- Check EPSG code matches everywhere: EPSG:32748

**Mistake 2: Wrong UTM zone**

**Problem:**
- Survey site at 110°E (UTM Zone 49), but project configured for Zone 48
- Coordinates appear shifted by hundreds of kilometers
- Position errors of 100-500 km east-west

**Solution:**
- Verify base station longitude during survey-in
- Calculate correct zone before configuring equipment
- Check coordinates are reasonable (Easting 200,000-800,000m, Northing makes sense for latitude)

**Mistake 3: Wrong hemisphere (North vs South)**

**Problem:**
- Survey site at 6°S, but configured for UTM Zone 48 North instead of 48 South
- Northing appears inverted or shows huge offset (~11,000 km error)

**Solution:**
- Always specify hemisphere along with zone number
- Use EPSG code (includes hemisphere): 32748 = Zone 48 South, 32648 = Zone 48 North
- Verify Northing values are reasonable (Southern hemisphere: <10,000,000m)

**Mistake 4: Ignoring datum**

**Problem:**
- Combine GPS survey (WGS84 datum) with old government map (local datum)
- Positions mismatch by 1-5 meters (looks like survey error, but actually datum difference)

**Solution:**
- Check datum for all data sources
- Apply datum transformation when combining data from different datums
- Document datum in metadata

**Mistake 5: Undefined CRS in exported data**

**Problem:**
- Export survey points as CSV with Easting/Northing columns
- No CRS metadata included in file
- Recipient does not know which CRS to use, guesses wrong

**Solution:**
- **Always include CRS information with exported data:**
  - For Geopackage/Shapefile: CRS embedded in file metadata
  - For CSV: Include CRS in filename (`site_YYYYMMDD_UTM48S.csv`) or README file
  - For reports: Document CRS in methods section
- **Best practice:** Use formats that embed CRS (Geopackage, GeoJSON, Shapefile)

---

## Coordinate Transformations and Conversions

Sometimes you need to convert coordinates between different CRS. Understanding when and how to do this prevents errors.

### When Coordinate Transformation is Needed

**Common scenarios requiring transformation:**

**1. Integrating data from different sources:**
- GPS survey in WGS84/UTM 48S
- Satellite imagery in WGS84 geographic (lat/lon)
- Old topographic map in local datum/different projection
- **Solution:** Transform all to common CRS for analysis

**2. Crossing UTM zone boundaries:**
- Project spans 108°E (boundary between Zone 48 and Zone 49)
- Must choose one zone, transform data from other zone
- **Solution:** Use zone containing base station; transform other data to match

**3. Meeting external requirements:**
- Government requires data in national datum (e.g., DGN95 for Indonesia)
- Engineering firm expects data in specific CRS
- **Solution:** Transform final outputs to required CRS

**4. PPP post-processing workflow:**
- PPP service outputs WGS84 geographic coordinates (lat/lon)
- Survey data in UTM Zone 48S
- **Solution:** Transform PPP coordinates to UTM to calculate correction (see Section 5.6)

**5. Web mapping and visualization:**
- Web maps often use Web Mercator (EPSG:3857)
- Your survey data in UTM
- **Solution:** GIS software automatically reprojects for display (no manual transformation needed)

### Transformation vs. Conversion

**Important distinction:**

**Coordinate conversion:**
- Changing between coordinate types within same datum
- Example: WGS84 geographic (lat/lon) → WGS84 UTM Zone 48S
- Mathematically exact (no approximation error)
- Straightforward calculation

**Coordinate transformation:**
- Changing between different datums
- Example: WGS84 → NAD83, or WGS84 → local datum
- Requires transformation parameters (may have uncertainty)
- More complex, potential for errors

**For OpenRiverCam surveys:**
- **Conversion** (WGS84 geographic ↔ WGS84 UTM) is common and straightforward
- **Transformation** (WGS84 ↔ local datum) only needed for specific integration requirements

### Tools for Coordinate Transformation

**Method 1: GIS software (recommended for most users)**

**QGIS coordinate transformation:**

**Option A: Reproject layer**
- Right-click layer → Export → Save Features As...
- Select target CRS from dropdown (search by EPSG code or name)
- QGIS handles transformation automatically
- Preserves attributes, geometry types

**Option B: On-the-fly reprojection**
- QGIS can display layers in different CRS together
- Set project CRS (lower right corner of QGIS window)
- QGIS reprojects all layers for display
- Useful for visualization, but should explicitly reproject for analysis

**ArcGIS Pro:**
- Use "Project" tool (Data Management toolbox)
- Select input layer, target CRS, output location
- Specify transformation if changing datums

**Method 2: Online coordinate conversion tools**

**Examples:**
- Geoscience Australia Coordinate Transformation Tool
- NOAA CORS coordinate conversion
- Many national geodetic agencies provide online calculators

**Use for:**
- Single-point conversions (e.g., converting PPP result to UTM)
- Verifying transformations
- Quick checks

**Limitations:**
- Manual entry (not practical for large datasets)
- May not support all CRS combinations

**Method 3: Command-line tools (for advanced users)**

**CS2CS (part of PROJ library):**
```
echo "106.789 -6.123 0" | cs2cs +init=epsg:4326 +to +init=epsg:32748
```

**Converts:**
- Input: WGS84 geographic (lon, lat, height)
- Output: WGS84 UTM Zone 48S (Easting, Northing, elevation)

**Advantages:**
- Scriptable (batch processing)
- Precise control over transformation parameters
- Free, open-source

**Disadvantages:**
- Command-line interface (steeper learning curve)
- Requires PROJ installation

**Method 4: Spreadsheet formulas (for simple conversions)**

**Geographic to UTM conversion:**
- Mathematical formulas exist (complex: 10+ terms)
- Spreadsheet implementations available online
- **Not recommended:** Easy to make errors, better to use tested software

### Transformation Accuracy Considerations

**Factors affecting transformation accuracy:**

**1. Transformation type:**
- Geographic ↔ projected (same datum): Exact (no error)
- Modern datums (WGS84 ↔ GDA2020): <5cm
- WGS84 ↔ older local datums: 0.5-5 meters
- Poorly documented local datums: 5-50 meters (uncertain)

**2. Transformation parameters:**
- Well-defined transformations (official parameters): High accuracy
- Approximate transformations (default parameters): Lower accuracy
- Unknown/undocumented transformations: Unpredictable accuracy

**3. Software implementation:**
- Professional GIS (QGIS, ArcGIS): Uses EPSG database, tested transformations
- Online calculators: Vary in quality and parameter sources
- Custom code: Only as good as implementation and parameters used

**Best practices:**

**1. Verify transformations with known control points:**
- If transforming survey data to local datum, check results against published control point coordinates
- Differences should be within expected transformation accuracy

**2. Document all transformations:**
- Record source CRS, target CRS, transformation method/parameters
- Include in project metadata and reports
- Enables verification and reproducibility

**3. Minimize transformations:**
- Choose initial CRS to avoid unnecessary transformations
- Each transformation introduces potential for error
- **Ideal workflow:** Collect data in final CRS, no transformation needed

**4. Use embedded CRS metadata:**
- Geopackage, Shapefile, GeoJSON embed CRS in file
- Software reads CRS automatically, applies correct transformations
- Reduces manual errors

**5. Test transformation accuracy:**
- Transform test point, verify result is reasonable
- Compare transformation results from different tools (should agree within mm-cm)
- For critical applications, compare to independent control

---

## Practical Workflow: CRS Configuration for OpenRiverCam

This section provides step-by-step guidance for configuring CRS throughout the OpenRiverCam survey workflow.

### Step 1: Determine UTM Zone Before Survey

**Before equipment setup, identify correct UTM zone:**

**1. Check approximate site location:**
- Google Maps, OpenStreetMap, or similar
- Note latitude, longitude (decimal degrees)
- Example: 6.1234°S, 106.7890°E

**2. Calculate UTM zone:**
- Zone = ⌊(Longitude + 180) / 6⌋ + 1
- Example: ⌊(106.7890 + 180) / 6⌋ + 1 = ⌊47.798⌋ + 1 = 48
- Hemisphere: Latitude < 0 → South
- **Result: UTM Zone 48 South**

**3. Look up EPSG code:**
- Southern hemisphere: EPSG:327XX (XX = zone number)
- Northern hemisphere: EPSG:326XX
- Example: Zone 48 South = **EPSG:32748**

**4. Record for use in all systems:**
- Write in field notebook
- Include in SW Maps project configuration
- Document in QGIS project settings

### Step 2: Configure Base Station CRS

**From SURVEY_PROCESS.md, base station configuration in u-center:**

**Set output coordinate format:**
- Connect base station to computer running u-center
- Navigate to: View → Messages View → UBX → CFG → NAV5
- Set "Position Mode": 3D only (or Auto)
- Set "Position Coordinate System": **ECEF** (Earth-Centered Earth-Fixed) or **LLH** (Lat/Lon/Height)
- Note: Base station typically outputs geographic coordinates; UTM conversion happens in rover/smartphone

**Configure survey-in for base position:**
- Set survey-in duration: 30-60 minutes
- Survey-in establishes base position in WGS84 (GPS native datum)
- Position accuracy target: 0.25m

**Configure RTCM output for RTK corrections:**
- Base broadcasts corrections in RTCM format (industry standard)
- RTCM corrections are datum-independent (rover applies to its WGS84 solution)

**Record base station position when survey-in completes:**
- Note coordinates in geographic (lat/lon) or ECEF (X/Y/Z)
- Transform to UTM Zone 48S for documentation:
  - Use online converter or QGIS point layer method
  - Record: Base Easting, Northing, Elevation in EPSG:32748
- Example: Base position = 48S 501234.567mE 9876543.210mN 123.456m elevation

### Step 3: Configure GNSS Master and SW Maps CRS

**GNSS Master configuration:**
- GNSS Master passes GPS position from rover to Android as "mock location"
- Typically passes geographic coordinates (lat/lon)
- No explicit CRS configuration needed (operates transparently)

**SW Maps project CRS configuration (critical):**

**1. Create new SW Maps project:**
- Open SW Maps application
- Projects → Create New Project
- Project name: Site name and date

**2. Set project CRS:**
- Project Settings → Coordinate Reference System
- Search for: "32748" or "UTM Zone 48 South"
- Select: **EPSG:32748 - WGS84 / UTM Zone 48S**
- Verify: Units = meters, Datum = WGS84

**3. Verify CRS active:**
- Collect test point with rover
- Check coordinate values:
  - Easting should be 200,000-800,000 range (typical UTM Easting)
  - Northing should be <10,000,000 (Southern hemisphere)
  - If values are in degrees (0-180 lat/lon), CRS not set correctly - reconfigure

**4. Configure survey layers:**
- Create layers for Ground Control Points, Cross Sections, Water Level, Check Points
- Layer CRS inherits from project CRS (EPSG:32748)
- Add attribute fields for point names, descriptions, pole height, etc.

**Critical: Verify CRS before collecting any survey points.** Test point coordinates should be sensible UTM values.

### Step 4: Verify CRS in QGIS Post-Processing

**After survey, when importing data to QGIS:**

**1. Create new QGIS project:**
- Project → New
- Save project with descriptive name

**2. Set project CRS:**
- Project → Properties → CRS
- Search: "32748"
- Select: **EPSG:32748 - WGS84 / UTM Zone 48S**
- Enable "on-the-fly reprojection" (allows viewing layers in different CRS, but analysis should use project CRS)

**3. Import SW Maps Geopackage export:**
- Layer → Add Layer → Add Vector Layer
- Navigate to SW Maps export (.gpkg file)
- QGIS reads embedded CRS metadata (should be EPSG:32748)
- Verify: Right-click layer → Properties → Information → CRS = EPSG:32748

**4. Add satellite imagery basemap:**
- Plugins → QuickMapServices → Google Satellite (or OSM, Bing, etc.)
- Basemap will be automatically reprojected to match project CRS (EPSG:32748)
- Survey points should overlay correctly on imagery

**5. Verify coordinates:**
- Open attribute table for survey layer
- Check Easting/Northing values are sensible:
  - Easting: 200,000 - 800,000 m
  - Northing: For locations near Jakarta (6°S): ~9,300,000 - 9,400,000 m
  - If values wrong, CRS may be incorrect - check layer CRS

**6. Apply PPP corrections (if using):**
- Transform PPP coordinates from WGS84 geographic to EPSG:32748 (see Section 5.6)
- Calculate correction: ΔE, ΔN, ΔZ
- Apply translation to all survey points
- Export corrected data, maintaining EPSG:32748 CRS

### Step 5: Export Data with CRS Metadata

**When exporting data for PtBox or other applications:**

**Geopackage export (recommended):**
- Right-click layer → Export → Save Features As...
- Format: **Geopackage** (.gpkg)
- CRS: EPSG:32748 (verify this matches layer CRS)
- Filename: Descriptive name with date
- **Geopackage embeds CRS metadata** - recipient software can read it automatically

**CSV/XYZ export for PtBox:**
- Right-click layer → Export → Save Features As...
- Format: CSV (Comma Separated Value)
- Layer Options: GEOMETRY=AS_XYZ
- CRS: EPSG:32748
- **Important:** CSV does not embed CRS metadata
  - Include CRS in filename: `site_YYYYMMDD_UTM48S.xyz`
  - Or create README.txt documenting CRS
- PtBox should be configured to same CRS (EPSG:32748) for import

**Shapefile export (for compatibility):**
- Format: ESRI Shapefile
- CRS: EPSG:32748
- Shapefile embeds CRS in .prj file
- Widely compatible with GIS software

**GeoJSON export (for web mapping):**
- Format: GeoJSON
- CRS: EPSG:32748 or EPSG:4326 (WGS84 geographic - standard for web)
- GeoJSON CRS support varies - verify recipient software handles correctly

**Documentation:**
- Include CRS information in data delivery package
- README or metadata file: "All coordinates in EPSG:32748 (WGS84 / UTM Zone 48 South), units = meters"

---

## Connection to Survey Procedures

Now you understand coordinate systems and their practical application to OpenRiverCam surveys:

**SURVEY_PROCESS.md specifies EPSG:32748:**
- This is WGS84 / UTM Zone 48 South
- Covers 102°E-108°E, southern hemisphere
- Appropriate for western Indonesia (Jakarta, Sumatra, western Java)
- Provides accurate metric coordinates for field surveys

**CRS consistency throughout workflow:**
- Base station: Outputs WGS84 (GPS native)
- Rover: Receives WGS84 from satellites + RTK corrections from base
- GNSS Master: Passes geographic coordinates (WGS84 lat/lon) to Android
- **SW Maps: Configured to EPSG:32748** - converts lat/lon to UTM on-the-fly
- **QGIS: Project CRS = EPSG:32748** - all analysis in consistent system
- **PtBox: Configured to EPSG:32748** - imports XYZ coordinates correctly

**PPP workflow uses coordinate conversion:**
- AUSPOS outputs: WGS84 geographic (lat, lon, ellipsoid height)
- Convert to: EPSG:32748 (UTM Easting, Northing, elevation)
- Use converted coordinates to calculate correction translation
- Apply correction to all survey points (already in EPSG:32748)

**Why this matters:**
- Consistent CRS prevents position errors (mixing CRS = errors of kilometers)
- UTM enables simple distance/area calculations for GCP layout, cross-sections
- WGS84 datum compatible with GPS equipment (no transformation needed)
- EPSG:32748 standard for regional surveying in this area

**Troubleshooting CRS problems:**
- If coordinates look wrong (degrees instead of meters, or vice versa): Check CRS configuration
- If survey points do not overlay correctly on imagery: Verify both use same CRS
- If distances calculate incorrectly: Ensure using projected coordinates (UTM), not geographic (lat/lon)

You now understand what EPSG:32748 means, why it is used, and how to configure it throughout the OpenRiverCam workflow. Chapter 9 field procedures apply this knowledge in operational checklists.

---

## Summary: Key Concepts

**What is a Coordinate Reference System (CRS):**
- Mathematical framework for representing positions on Earth with numbers
- Consists of: coordinate type (geographic/projected), projection (if applicable), datum (ellipsoid model)
- Uniquely identified by EPSG code (e.g., EPSG:32748)

**Geographic vs. Projected coordinates:**
- **Geographic (lat/lon):** Angles on curved Earth, difficult for distance calculations, universal
- **Projected (Easting/Northing):** Flat-plane coordinates in meters, simple distance/area math, limited extent
- **OpenRiverCam uses projected (UTM)** for field surveys

**UTM (Universal Transverse Mercator):**
- Global system dividing Earth into 60 zones (6° longitude each)
- Each zone uses Transverse Mercator projection
- Coordinates: Zone + Hemisphere + Easting + Northing (in meters)
- Accurate for areas within single zone (distortion <0.1%)
- **EPSG:32748 = WGS84 / UTM Zone 48 South** (western Indonesia)

**Datums:**
- Mathematical model of Earth's shape (ellipsoid)
- WGS84: Global datum used by GPS
- Local datums: Regional systems (may differ from WGS84 by meters)
- **OpenRiverCam uses WGS84** (GPS native, no transformation needed)

**Choosing CRS for your survey:**
- Determine UTM zone: Calculate from base station longitude
- Specify hemisphere: North or South based on latitude
- Look up EPSG code: 327XX (South) or 326XX (North), XX = zone number
- Verify zone contains entire survey area

**CRS consistency:**
- Configure all systems to same CRS before survey (equipment, software, analysis)
- Verify coordinates are sensible (UTM Easting 200,000-800,000m, Northing appropriate for latitude)
- Include CRS metadata in exported data (Geopackage, Shapefile embed CRS)
- Document CRS in project records

**Coordinate transformations:**
- Needed when integrating data from different CRS
- Conversion (same datum): Exact, no error
- Transformation (different datums): May have cm-m uncertainty
- **Minimize transformations** - choose correct CRS initially

**Common mistakes:**
- Mixing CRS within project (degrees vs. meters)
- Wrong UTM zone or hemisphere (hundreds of km error)
- Ignoring datum differences (meter-level errors)
- Missing CRS metadata in exported files
- **Prevention: Verify CRS at every workflow step**

**Practical workflow:**
1. Determine UTM zone before survey (calculate from longitude)
2. Configure SW Maps project to EPSG:32748 (or appropriate zone)
3. Verify test point coordinates are sensible UTM values
4. Set QGIS project CRS to match (EPSG:32748)
5. Export data with CRS metadata (Geopackage preferred)
6. Document CRS in all deliverables

**Why coordinate systems matter for OpenRiverCam:**
- Enable accurate distance/area calculations (GCP layout, cross-sections)
- Ensure data integrates correctly with imagery and maps
- Prevent systematic position errors
- Support PPP post-processing workflow
- Meet professional surveying standards

You now understand coordinate reference systems and how to use them correctly for OpenRiverCam surveys. This knowledge prevents costly errors and ensures your survey data is accurate, consistent, and compatible with other geospatial datasets. Section 5.8 addresses the final piece: environmental factors that affect survey quality in the field.

---

**[VISUAL PLACEHOLDER: CRS hierarchy diagram showing:
- Top level: Geographic vs Projected
- Geographic branch: WGS84 lat/lon (EPSG:4326), examples of use cases
- Projected branch: UTM, Lambert, Albers, etc.
- UTM detail: Zone selection map, Easting/Northing explanation, example coordinates
- Datum comparison: WGS84 vs local datums, transformation arrows
- Bottom: OpenRiverCam workflow showing CRS at each step (Base→Rover→SW Maps→QGIS→PtBox, all EPSG:32748)]**

**[VISUAL PLACEHOLDER: UTM zone map of Indonesia showing:
- Zones 46-54 covering Indonesia
- Zone 48 highlighted (102°E-108°E)
- Example survey sites marked with coordinates
- Boundary lines between zones
- Equator marked (Northern vs Southern zones)
- Color-coded by zone for clarity]**

**[VISUAL PLACEHOLDER: Side-by-side comparison showing:
- Geographic coordinates (lat/lon degrees) on globe
- Same point in UTM (Easting/Northing meters) on flat map
- Distance calculation examples for both
- Why projected coordinates are better for field surveys]**
