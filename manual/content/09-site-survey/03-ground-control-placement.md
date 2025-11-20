# 9.3 Ground Control Selection and Placement

Ground Control Points (GCPs) are the foundation of accurate OpenRiverCam measurements. This section connects the conceptual understanding from Section 4.3 (Perspective Distortion) with the practical field decisions you will make when selecting and placing GCPs at your survey site.

Strategic GCP placement makes the difference between excellent transformation accuracy and unreliable measurements. You cannot fix poor GCP distribution with better equipment or sophisticated software. Getting this right matters fundamentally.

By the end of this section, you will understand:
- The purpose of GCPs and why they matter for transformation
- How many GCPs you need and why
- Strategic placement for optimal transformation accuracy
- Types of GCP markers and selection criteria
- Visibility requirements for camera identification
- Permanence considerations for long-term monitoring
- How to document GCP locations and conditions

---

## GCP Purpose: Connecting Image to Reality

### Recall from Section 4.3

Section 4.3 explained that perspective distortion causes scale to vary throughout the camera image. Objects farther from the camera appear smaller, even though their actual size has not changed. This means you cannot use a single constant scale factor ("1 pixel = 5 cm everywhere") - scale varies with position in the image.

**Ground Control Points solve this problem** by establishing known correspondences between image positions (pixels) and real-world positions (meters).

**The transformation process:**
1. Identify each GCP precisely in the camera image (pixel coordinates)
2. Survey each GCP precisely with RTK GPS (real-world coordinates)
3. Calculate homography transformation linking the two coordinate systems
4. Apply transformation to all tracked features (foam, debris) to get real-world positions

**GCPs are reference markers that enable the transformation.** Poor GCP placement or accuracy = poor transformation = wrong velocity measurements.

### What GCPs Actually Are

**Physical markers:**
- Visible objects you can identify clearly in camera images
- Located at surveyed positions with known coordinates
- Distributed throughout the camera's field of view
- Stable over time (do not move between survey and monitoring)

**Examples of GCP markers:**
- Painted marks on stable rocks (common, effective)
- Survey stakes driven into ground (soil/sand sites)
- Distinctive natural features (rock corners, tree bases) - use with caution
- Artificial targets mounted on posts (highest visibility, requires installation)
- Floating markers for mid-river positions (temporary, used during survey only)

**The marker itself is not sophisticated.** A rock with painted "X" works perfectly. What matters is:
1. You can identify it precisely in the image
2. You survey its position accurately with RTK
3. It remains in the same position over time

### Connection to Section 4.3 Concepts

**From Section 4.3, strategic GCP placement addresses perspective distortion:**

**Near-to-far distribution:**
GCPs at varying distances from camera (near edge, middle, far edge) enable accurate scale factor calculation throughout the depth of the scene.

**Left-to-right distribution:**
GCPs spanning the width of the field of view ensure transformation accuracy across the entire scene width.

**Coverage of measurement area:**
GCPs should surround or encompass the area where velocity will be measured. Interpolation within the GCP network is accurate; extrapolation beyond GCPs is unreliable.

**The strategic principle:**
GCPs distributed throughout the field of view enable the transformation to accurately account for perspective distortion everywhere in the scene.

---

## Number of GCPs Needed

### Mathematical Minimum vs Practical Requirement

**Mathematical minimum: 4 GCPs**
The homography transformation has 8 parameters. With 4 GCPs providing 8 coordinates (4 × 2 = 8: four X coordinates and four Y coordinates), you can mathematically solve for the 8 parameters.

**Why 4 is inadequate in practice:**
- Zero redundancy (any measurement error directly corrupts transformation)
- No error checking (cannot detect if one GCP is wrong)
- No flexibility (if one GCP becomes obscured or moves, entire transformation fails)
- Poor interpolation (large gaps between GCPs)

**Never use only 4 GCPs for OpenRiverCam.** This is asking for problems.

**Practical minimum: 6 GCPs**
With 6 GCPs providing 12 coordinates, you have 4 extra measurements (redundancy). This enables:
- Error checking through reprojection error analysis
- Detection of outliers (if one GCP surveyed incorrectly)
- Better interpolation (smaller gaps between GCPs)

**6 GCPs is the minimum for acceptable transformation quality.**

**Recommended: 8-10 GCPs**
This provides:
- Good redundancy for error detection
- Excellent interpolation throughout field of view
- Flexibility if 1-2 GCPs become obscured or unusable
- Higher confidence in transformation accuracy

**Diminishing returns beyond 10 GCPs:**
- More GCPs do not significantly improve transformation accuracy (interpolation already excellent with 8-10)
- More survey time required
- More potential for errors (more points to survey and identify)

**For typical OpenRiverCam installations: Aim for 8-10 GCPs with strategic distribution.**

### Quality vs Quantity

**Better to have 6 well-placed, accurately surveyed GCPs than 12 poorly placed or poorly surveyed GCPs.**

**Well-placed GCPs:**
- Distributed throughout field of view (near/far, left/right)
- Surrounding the velocity measurement area
- Clearly visible in camera images
- Surveyed with RTK fix and all quality gates met

**Poorly placed GCPs:**
- Clustered in one area (leaving large areas poorly covered)
- Outside the velocity measurement area
- Barely visible or ambiguous in images
- Surveyed hastily without verifying quality standards

**Strategic placement matters more than sheer numbers.**

---

## GCP Placement Strategy

### Distribution Principles

**Principle 1: Cover depth (near to far)**

Place GCPs at varying distances from camera:
- Near zone: 20-30% of GCPs close to camera (near edge of field of view)
- Middle zone: 40-50% of GCPs at medium distance (middle of velocity measurement area)
- Far zone: 20-30% of GCPs far from camera (far edge of field of view)

**Why this matters:**
Perspective distortion is most severe with distance from camera. Scale factor may vary 3-5× from near to far. GCPs at all distances enable accurate interpolation of scale factor throughout depth.

**Practical example:**
River site with camera 10m above water, viewing area extending from 5m to 30m from camera:
- Near GCPs: 5-10m from camera (2-3 points)
- Middle GCPs: 12-20m from camera (3-4 points)
- Far GCPs: 22-30m from camera (2-3 points)

Total: 8-10 GCPs covering full depth range.

**Principle 2: Cover width (left to right)**

Place GCPs across the full width of the velocity measurement area:
- Left side: 25-30% of GCPs (left bank or left edge of measurement area)
- Center: 40-50% of GCPs (mid-river or center of measurement area)
- Right side: 25-30% of GCPs (right bank or right edge of measurement area)

**Why this matters:**
Transformation must work across entire scene width. GCPs on both banks and at mid-river enable accurate interpolation across the width.

**Practical example:**
River 15m wide:
- Left bank GCPs: 2-3 points distributed along left bank
- Mid-river GCPs: 3-4 points (floating markers during survey, or rocks if present)
- Right bank GCPs: 2-3 points distributed along right bank

Total: 8-10 GCPs covering full width.

**Principle 3: Surround measurement area**

GCPs should encompass the area where velocity will be measured:
- Avoid measuring velocity outside the GCP network (extrapolation is unreliable)
- Place GCPs at or slightly beyond the edges of the measurement area
- If measurement area is the full river width, place GCPs on both banks (not just one)

**Why this matters:**
Homography interpolation between GCPs is accurate. Extrapolation beyond GCPs is much less reliable. Keep measurements within the GCP network.

**Practical example:**
Velocity measurement area is cross-section from left bank (X=0m) to right bank (X=15m):
- Place GCPs from X=-0.5m (just beyond left edge) to X=15.5m (just beyond right edge)
- Do not place all GCPs on left bank (X=0 to X=5m) and try to measure velocity at right bank (X=12-15m)
- Measurements at X=12-15m would be extrapolation (unreliable)

**Principle 4: Avoid clustering**

Do not place all GCPs in one cluster, even if that is the most convenient location:
- Bad: All GCPs on near left bank (convenient access, poor coverage)
- Good: GCPs distributed throughout scene (may require more effort, excellent coverage)

**Clustering leaves large areas with poor transformation accuracy.**

**Practical example - avoid this:**
River site with easy access to left bank upstream. Place 10 GCPs in 5m × 5m area on left bank near camera. Far right bank and downstream areas have no GCPs.

Result: Transformation excellent in left bank upstream area, poor everywhere else. Velocity measurements at mid-river or right bank unreliable.

**Better:** Place 3 GCPs on left bank, 3-4 at mid-river, 3 on right bank, distributed along river length. Requires more effort (wading, boating, or walking around) but produces reliable transformation everywhere.

### Practical Distribution Example

**Scenario:**
River 15m wide, camera 8m above water, 6m from left bank, viewing area 25m long (downstream direction).

**GCP distribution (9 points total):**

**Left bank (3 GCPs):**
- GCP1: Near, upstream (5m from camera, left edge)
- GCP2: Mid-distance, center-left (12m from camera, left bank)
- GCP3: Far, downstream (20m from camera, left bank)

**Mid-river (3 GCPs):**
- GCP4: Near, center (7m from camera, mid-river position)
- GCP5: Mid-distance, center (14m from camera, mid-river position)
- GCP6: Far, center (22m from camera, mid-river position)

**Right bank (3 GCPs):**
- GCP7: Near, upstream (8m from camera, right bank)
- GCP8: Mid-distance, center-right (15m from camera, right bank)
- GCP9: Far, downstream (23m from camera, right bank)

**Coverage achieved:**
- Depth: 5m to 23m from camera (near, middle, far zones covered)
- Width: Left bank to right bank (full width covered)
- Area: 15m × 25m velocity measurement area fully encompassed

This distribution enables accurate transformation throughout the entire measurement area.

---

## GCP Marker Types

### Painted Marks on Rocks

**Most common and effective method for natural river sites.**

**Advantages:**
- Rocks are stable (do not move with floods unless extreme)
- High visibility (bright paint contrasts with rock)
- Permanent (paint lasts months to years with proper paint)
- No installation required (use existing rocks)
- Works on banks and mid-river (if rocks present)

**Procedure:**
1. Identify stable, visible rock at desired GCP location
2. Clean rock surface (brush off dirt, dry if wet)
3. Apply bright paint (orange, yellow, pink - high visibility colors)
4. Paint simple target: "X" or "+" or solid circle 5-10cm diameter
5. Photograph target with measuring tape for scale documentation
6. Survey target center with RTK rover

**Paint selection:**
- Exterior spray paint (weather-resistant)
- Bright colors (orange, yellow, pink, lime green)
- Matte finish (reduces glare in camera images)

**Target size:**
- 5-10 cm diameter typical (visible in images but small enough to identify center precisely)
- Larger targets (15-20 cm) for high-mounting cameras (lower resolution at GCP distance)
- Smaller targets (3-5 cm) for low cameras or close GCPs

### Survey Stakes

**Effective for soil or sand sites where rocks are not available.**

**Advantages:**
- Can be placed at any desired location (not limited by rock positions)
- High visibility (paint stake brightly or attach flag)
- Inexpensive and portable

**Disadvantages:**
- May be removed by people or animals
- May shift slightly if ground is soft
- May be washed away by floods
- Temporary (months-scale permanence at best)

**Procedure:**
1. Drive wooden or fiberglass stake firmly into ground (30+ cm depth)
2. Paint stake brightly or attach high-visibility flag
3. Mark survey point clearly (top of stake, or nail in top of stake)
4. Survey stake position with RTK rover (pole tip touching nail or stake top)
5. Photograph stake with surroundings for relocation

**Use for temporary installations or sites where rocks are not available.**

### Artificial Targets on Posts

**Highest visibility option, requires installation effort.**

**Design:**
- Printed target pattern (checkerboard, circular bullseye, etc.)
- Mounted on rigid backing (plastic, metal, wood)
- Attached to post or structure
- Size: 15-30 cm typical

**Advantages:**
- Extremely high visibility and contrast
- Unambiguous center point (designed for precision)
- Can be placed at exact desired locations
- Professional appearance

**Disadvantages:**
- Requires installation (posts must be secured)
- May be vandalized or stolen
- More expensive (materials and labor)
- More visible to public (may attract attention/interference)

**Use for permanent installations with resources for proper GCP infrastructure.**

### Floating Markers for Mid-River GCPs

**Temporary solution for mid-river positions during survey.**

**Design:**
- Buoyant platform (foam, plastic float)
- Weighted to remain in position (anchor line or weight)
- High-visibility marker on top (bright flag or target)

**Procedure:**
1. Position floating marker at desired mid-river GCP location
2. Allow marker to stabilize (wind, current settle)
3. Take camera sample video (marker visible)
4. Survey marker position immediately with rover (wade or boat to marker, touch with rover pole)
5. Remove marker after survey (cannot remain for long-term monitoring)

**Advantages:**
- Enables mid-river GCP placement where no rocks exist
- Can be positioned at exact desired locations

**Disadvantages:**
- Temporary only (cannot be left in river)
- Position may shift slightly (wind, current)
- Requires wade or boat access to survey
- Not useful for long-term monitoring (must resurvey each time)

**Use when mid-river GCPs needed but no rocks or structures available.**

### Natural Features

**Use with extreme caution.**

**Examples:**
- Distinctive rock corners or edges
- Tree bases or roots
- Structure corners (bridge abutments, walls)

**Advantages:**
- No marker installation required
- Permanent (natural or structural features do not move)

**Disadvantages:**
- Often ambiguous (which exact pixel is the "corner"? hard to identify precisely)
- May change appearance (vegetation grows, erosion, weathering)
- Lower visibility (no bright paint or targets)
- Difficult to relocate precisely for future surveys

**Only use natural features if:**
- Feature is unambiguously identifiable in image (clear corner, distinct point)
- Feature is stable (rock edge, not vegetation)
- Feature is documented thoroughly (photos from multiple angles, measurements)

**Painted marks on natural features are better than unpainted natural features** - adds visibility and unambiguous point identification.

---

## Visibility Requirements

### Camera Field of View

**Every GCP must be visible in the camera's field of view.**

This seems obvious, but requires verification:
- Stand at camera position (or view camera live feed)
- Verify each planned GCP location is visible in frame
- Check that GCPs are not obscured by vegetation, structures, or terrain

**If GCP is not visible in camera:**
It cannot be used for transformation, even if surveyed perfectly.

**Common visibility problems:**
- GCP hidden behind vegetation (plants grow between survey and operation)
- GCP outside camera frame (field of view narrower than expected)
- GCP visible from camera position but not when camera mounted (different viewing angle)
- GCP obscured by water level rise (mark placed too low)

**Verification procedure:**
1. Mount camera at intended position (or mock-up camera position)
2. Take sample photo showing full field of view
3. Review photo to verify all planned GCP locations are visible
4. Adjust GCP locations if needed before surveying

**From SURVEY_PROCESS.md, Section 5:**
> Take sample video → Detailed procedure in Appendix D
> Survey each control point after video

This sequence ensures GCPs are visible before you invest time surveying them.

### Identification Precision

**You must be able to identify the GCP center precisely in the image.**

Precision requirement: ±1-2 pixels

**Why this matters:**
If you survey GCP position to 2 cm accuracy, but identify it in the image to ±10 pixels (maybe 20 cm), the transformation error is dominated by identification error, not survey error.

**Design for precise identification:**
- Use small, distinct targets (5-10 cm diameter circle or X)
- High contrast (bright paint on dark rock)
- Clear center point (cross-hair, bullseye, small dot)
- Unambiguous (no similar features nearby that could be confused)

**When identifying GCP in image (during PtBox configuration):**
- Zoom in closely on GCP marker
- Click precisely on target center
- If target is "X", click at intersection
- If target is circle, click at center
- If target is painted rock, click at center of painted area

**Precision technique:**
Some software allows sub-pixel clicking (you can click between pixels). Use this capability for maximum precision.

**Avoid ambiguous markers:**
- Large painted area with no clear center (where to click?)
- Natural features with gradual edges (which pixel is the "edge"?)
- Markers that blend into background (poor contrast)

### Lighting Conditions

**GCPs must be visible under the lighting conditions when monitoring operates.**

**Consider:**
- Will GCPs be in shadow at certain times? (sun angle changes through day)
- Will glare from water obscure GCPs? (low sun reflecting off water)
- Will GCPs be visible at night? (if night monitoring planned)

**Test visibility:**
Take sample photos at different times of day (morning, noon, afternoon) to verify GCP visibility under varying lighting.

**If GCPs not visible under all conditions:**
- Adjust GCP positions (move to avoid shadow or glare areas)
- Add redundant GCPs (if some obscured at certain times, others remain visible)
- Limit monitoring to times when GCPs are visible

**For 24-hour monitoring:**
Consider illuminated GCPs or reflective markers (adds complexity but enables night operation).

---

## Permanence Considerations

### Short-Term vs Long-Term Monitoring

**Short-term deployment (weeks to months):**
- Survey stakes acceptable (may last months)
- Painted rocks ideal (will last months to years)
- Floating markers acceptable for initial survey (resurvey as needed)

**Long-term monitoring (months to years):**
- Painted rocks required (stable over long term)
- Artificial targets on posts (if resources for installation)
- Survey stakes will likely fail (moved, removed, degraded)

**Plan GCP permanence based on monitoring duration.**

### Flood Resilience

**GCPs must survive typical floods.**

**Risk assessment:**
- Will GCP locations be underwater during high flows? (Place GCPs above expected flood level)
- Will GCPs be scoured by flood currents? (Avoid loose rocks or exposed stakes)
- Will debris accumulation cover GCPs? (Place on protected banks or elevated positions)

**Flood-resistant GCP placement:**
- Banks above high water mark (visible during floods when monitoring is most critical)
- Large, stable rocks (not moved by typical floods)
- Securely installed posts (concreted or deeply driven)

**Mid-river GCPs and floods:**
Mid-river rocks may be underwater during floods. This is acceptable if:
- Bank GCPs remain visible (transformation still possible with partial GCP coverage)
- System recalibrates when water recedes (resurvey mid-river GCPs if moved)

**The practical approach:**
Place 6-8 GCPs on stable banks (flood-resistant) plus 2-4 mid-river GCPs (best-case coverage, may be lost during floods). Bank GCPs alone provide adequate transformation; mid-river GCPs improve accuracy when available.

### Vegetation Growth

**GCPs can become obscured by vegetation over time.**

**Prevention strategies:**
- Clear vegetation around GCPs during installation
- Select GCP locations in areas with slow vegetation growth (rock outcrops, bare soil)
- Avoid placing GCPs near fast-growing plants

**Maintenance plan:**
- Inspect GCPs seasonally
- Trim vegetation as needed
- Repaint markers if fading

**For long-term monitoring:**
Budget time for GCP maintenance (1-2 times per year typically adequate).

### Vandalism and Interference

**Human interference:**
GCPs may be removed, covered, or relocated by:
- Curious people (what are these painted rocks?)
- Children playing (painted rocks become toys)
- Maintenance activities (bank cleaning, mowing)
- Deliberate vandalism

**Mitigation strategies:**
- Coordinate with local community (explain purpose, request they leave markers alone)
- Place GCPs in less accessible locations (reduces casual interference)
- Use natural-looking markers (painted rocks less obvious than artificial targets)
- Check GCPs periodically (detect problems early)

**If GCPs are moved:**
Reprojection errors will increase (surveyed position no longer matches marker position). You will notice this during system validation. Re-survey moved GCPs if discovered.

---

## GCP Documentation

Thorough documentation enables future surveys and troubleshooting.

### Field Documentation

**For each GCP, record:**
- **GCP ID:** Unique identifier (GCP1, GCP2, etc.)
- **Description:** Location description ("Left bank, 5m upstream from bridge, large granite rock")
- **Marker type:** What marks the point ("Painted orange X on rock", "Survey stake with flag")
- **Coordinates:** Surveyed position (Easting, Northing, Elevation in UTM)
- **Survey quality:** RTK fix time, precision estimates, satellites, PDOP at time of survey
- **Survey timestamp:** When surveyed (date and time)
- **Visibility:** Visible in camera? Lighting conditions?
- **Photos:** Multiple angles showing GCP and surroundings

**Field notebook entry example:**
```
GCP3 - Left bank, mid-distance
- Position: E=685428.34, N=9456788.12, Z=142.68 (EPSG:32748)
- Marker: Painted yellow X on large granite boulder
- Survey: 2024-11-15 10:45, FIX 45s, H=1.4cm V=2.1cm, Sats=16, PDOP=1.9
- Visibility: Clear in camera image, no shadows
- Photos: IMG_3421, IMG_3422, IMG_3423
- Notes: Stable rock, above high water mark, excellent long-term GCP
```

This documentation enables:
- Relocation of GCP for future surveys
- Troubleshooting if reprojection errors are large
- Understanding GCP quality and suitability
- Verification of survey conditions

### Photographic Documentation

**For each GCP, capture:**

1. **Close-up photo:** Shows marker clearly with measuring tape or scale reference
2. **Medium photo:** Shows GCP and immediate surroundings (context)
3. **Wide photo:** Shows GCP location in broader site context (aids relocation)

**Additional useful photos:**
- View from camera position showing all GCPs
- Overview photo with GCP locations annotated
- Base station location and setup

**Organize photos systematically:**
- Name files clearly (GCP1_closeup.jpg, GCP1_context.jpg, etc.)
- Store with survey data
- Include in documentation package

### GIS Documentation

**After survey, create GIS layer with GCP locations:**
- Import surveyed GCP coordinates
- Add attributes (ID, description, marker type, survey quality, date)
- Display on satellite imagery or base map (verify positions look correct)
- Export as standard format (GeoJSON, Shapefile, KML)

**This GIS layer serves as:**
- Permanent record of GCP locations
- Reference for future surveys
- Quality control visualization (do positions look reasonable?)

---

## Connection to Transformation Quality

**GCP placement directly determines transformation quality.**

**Good GCP placement:**
- 8-10 GCPs strategically distributed throughout field of view
- Covering measurement area (near/far, left/right)
- Surveyed accurately (RTK fix, all quality gates met)
- Clearly visible and precisely identifiable in images

**Result:**
- Excellent transformation accuracy (reprojection errors <5cm)
- Reliable velocity measurements throughout measurement area
- Confident discharge calculations

**Poor GCP placement:**
- 4-6 GCPs clustered in one area
- Leaving large areas without coverage
- Ambiguous markers or poor visibility
- Surveyed hastily without quality verification

**Result:**
- Poor transformation accuracy (reprojection errors >10cm)
- Unreliable velocity measurements in areas far from GCPs
- Uncertain discharge calculations

**The investment in strategic GCP placement pays off in every measurement the system makes** over its operational lifetime. Do this step correctly.

---

## Summary: Ground Control Placement Guidelines

**Number of GCPs:**
- Minimum: 6 GCPs with strategic distribution
- Recommended: 8-10 GCPs for excellent coverage
- Quality more important than quantity

**Distribution strategy:**
- Cover depth: Near zone, middle zone, far zone (GCPs at varying distances from camera)
- Cover width: Left side, center, right side (GCPs across full measurement area width)
- Surround measurement area: Place GCPs at or beyond edges of area where velocity will be measured
- Avoid clustering: Distribute throughout scene, not concentrated in one convenient location

**Marker types:**
- Painted marks on rocks: Most common and effective (stable, visible, permanent)
- Survey stakes: Acceptable for temporary deployments or where rocks unavailable
- Artificial targets: Highest visibility, requires installation effort
- Floating markers: Temporary mid-river solutions during survey
- Natural features: Use with caution (often ambiguous)

**Visibility requirements:**
- Every GCP visible in camera field of view
- Identifiable precisely in images (±1-2 pixels)
- Visible under operating lighting conditions
- High contrast and distinct markers

**Permanence considerations:**
- Select markers appropriate for monitoring duration
- Place above expected flood levels when possible
- Account for vegetation growth
- Mitigate vandalism risk through community coordination
- Budget for maintenance (repaint, trim vegetation)

**Documentation:**
- Record GCP ID, description, marker type, coordinates, survey quality
- Photograph each GCP (close-up, context, wide views)
- Create GIS layer with GCP locations and attributes
- Maintain permanent record for future surveys

**The critical principle:**
Strategic GCP placement enables accurate transformation. Invest time in thoughtful GCP selection and placement. This foundation determines the reliability of every measurement your OpenRiverCam system produces.

---

**Next Section:** [9.4 Survey Setup - Hardware](04-survey-setup-hardware.md)
