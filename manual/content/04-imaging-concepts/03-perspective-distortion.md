# 4.3 Perspective Distortion and Georectification

This section addresses the most complex and most important distortion affecting OpenRiverCam measurements: perspective distortion. Understanding this concept is critical because it explains why camera placement matters, why we need ground control points, and how the transformation process actually works.

Perspective distortion is challenging because it seems counter-intuitive. Our brains automatically compensate for it in daily life, so we rarely notice it. But for precise measurements, we must understand and correct it explicitly.

Take your time with this section. We will build understanding through multiple analogies, starting with familiar experiences and gradually developing the technical concepts needed for OpenRiverCam deployment.

By the end of this section, you will understand:
- What perspective distortion is and why it occurs
- How viewing angle affects measurements
- Why objects far from the camera appear smaller
- The role of ground control points in perspective correction
- What georectification means and why we need it
- How to optimize camera placement to minimize perspective problems
- The connection between perspective distortion and surveying requirements

---

## Understanding Perspective Through Familiar Experiences

### The Railroad Tracks Experience

**The phenomenon:**
Stand between railroad tracks and look down the line toward the horizon. What do you see?

- Near you: The tracks are wide apart (maybe 1.5 meters between rails)
- Further away: The tracks appear to get closer together
- At the horizon: The tracks appear to meet at a single point

**What is really happening:**
The tracks do not actually get closer together. They maintain the same spacing (1.5 meters) along their entire length. But from your viewpoint, they appear to converge.

**Why this happens:**
This is perspective distortion. Objects that are farther from you appear smaller, even though their actual size has not changed. Since the rails maintain constant spacing but appear to shrink with distance, they seem to converge.

**The critical insight:**
If you tried to measure the distance between the rails using only a photograph taken from your viewpoint:
- Measurement near the bottom of the photo: Accurate (tracks actually are 1.5 m apart, appear 1.5 m apart)
- Measurement far away in the photo: Wrong (tracks are still 1.5 m apart, but appear only 0.5 m apart)

Unless you account for the perspective effect, your measurements become increasingly wrong as distance from the camera increases.

**This is exactly the challenge OpenRiverCam faces when measuring river velocity.**

[VISUAL PLACEHOLDER: Classic photograph of railroad tracks extending to horizon, with three measurements marked: near (accurate 1.5m), middle (appears 1.0m but actually 1.5m), far (appears 0.5m but actually 1.5m). Caption: "Perspective distortion makes parallel lines appear to converge."]

### The Hallway Experience

Walk down a long hallway and look at the ceiling tiles. Each tile is the same size (perhaps 60 cm × 60 cm), but:
- Tiles directly above you appear large
- Tiles 5 meters ahead appear medium-sized
- Tiles 20 meters ahead appear tiny

Same-sized objects appear different sizes depending on their distance from you.

**If you took a photo of the hallway:**
The tiles are all identical in reality, but the image shows them in many different sizes. If you tried to measure something using the tiles as a reference, you would get different scale factors depending on which part of the hallway you measured in.

**The camera has no depth perception:**
Your brain knows all the tiles are the same size because you understand 3D space. But a camera image is flat (2D). The camera records tiles of different apparent sizes with no understanding that they are actually identical.

This is why OpenRiverCam needs ground control points - to establish how scale changes with distance from the camera.

[VISUAL PLACEHOLDER: Photo looking down long hallway with floor tiles. Same-size tiles marked near (appear large), middle (appear medium), far (appear small). Overlay showing "All tiles actually 60 cm × 60 cm".]

### The Table Looking Down Experience

**Try this visualization:**
Stand next to a rectangular table and look straight down at it. From this viewpoint:
- You see the table top directly
- All corners are visible
- The table appears rectangular (as it actually is)
- The sides appear parallel
- Measurements across the table in any direction would be accurate to the same scale

**Now move to the end of the table and look at it from an angle:**
- The end near you appears wide
- The end far from you appears narrow
- The sides appear to converge (like railroad tracks)
- The table appears trapezoidal, not rectangular
- A measurement across the near end captures more real distance than a measurement across the far end

**The table has not changed shape. Your viewing angle changed.**

This demonstrates that perspective distortion depends on the angle at which you view objects. The more directly you look down at something (perpendicular view), the less perspective distortion occurs. The more obliquely you view something (shallow angle), the more perspective distortion occurs.

**For OpenRiverCam:**
This is why camera mounting height and angle matter. A camera mounted high and looking steeply down at the river experiences less perspective distortion than a camera mounted low and looking across the river at a shallow angle.

[VISUAL PLACEHOLDER: Two views of rectangular table - left shows top-down view (table appears rectangular, minimal perspective), right shows angled view (table appears trapezoidal, strong perspective). Measurements marked showing scale variation.]

---

## The Mathematical Reality: How Perspective Works

### The Geometry of Viewing

**The pinhole camera model:**
To understand perspective mathematically, imagine how a simple pinhole camera works:
1. Light travels in straight lines from objects in the scene
2. Light passes through a single point (the pinhole)
3. Light projects onto a flat surface behind the pinhole (the film or sensor)

**Why distance matters:**
Consider two identical objects - one 5 meters from the camera, one 10 meters from the camera:
- Object at 5 m: Light rays from its edges pass through the pinhole at a wider angle
- Object at 10 m: Light rays from its edges pass through the pinhole at a narrower angle
- Result: Farther object appears half the size of nearer object in the image

**The mathematical relationship:**
Apparent size is inversely proportional to distance:
- If object doubles its distance from camera, it appears half the size
- If object is 3 times farther away, it appears 1/3 the size
- If object is 10 times farther away, it appears 1/10 the size

**For OpenRiverCam velocity measurements:**
Imagine foam moving 1.0 meter across the river:
- If foam is 10 meters from camera, the movement might span 50 pixels in the image
- If foam is 20 meters from camera, the same 1.0 meter movement spans only 25 pixels
- The foam moved the same real distance, but appears to move different pixel distances

Without accounting for perspective, pixel-based measurements are meaningless. We must establish how pixel distances relate to real distances at every location in the scene.

[VISUAL PLACEHOLDER: Diagram showing pinhole camera geometry with two identical objects at different distances. Light rays shown converging through pinhole. Near object projects large image, far object projects small image. Mathematical relationship labeled: "Size ∝ 1/distance".]

### The Scale Factor Concept

**What is a scale factor?**
A scale factor describes how many real-world meters each pixel represents at a specific location in the image.

**Example with varying scale:**
In an OpenRiverCam image:
- Near edge of river (5 m from camera): Scale factor = 0.015 m/pixel (1 pixel = 1.5 cm)
- Middle of river (15 m from camera): Scale factor = 0.045 m/pixel (1 pixel = 4.5 cm)
- Far edge of river (25 m from camera): Scale factor = 0.075 m/pixel (1 pixel = 7.5 cm)

**Practical implication:**
If foam moves 30 pixels in the image:
- Near edge: 30 pixels × 0.015 m/pixel = 0.45 meters actual movement
- Middle: 30 pixels × 0.045 m/pixel = 1.35 meters actual movement
- Far edge: 30 pixels × 0.075 m/pixel = 2.25 meters actual movement

The same pixel movement corresponds to five times more real-world movement at the far edge than at the near edge!

**This is why perspective distortion is so critical to correct.**

Without establishing the scale factor at every location, OpenRiverCam cannot accurately calculate how far things actually moved. The pixel tracking would be perfect, but the conversion to real-world distance would be completely wrong.

**How we establish scale factors:**
Ground control points. By surveying the precise real-world locations of multiple points throughout the field of view, and identifying those points in the image, we establish the relationship between pixel distances and real distances throughout the entire scene.

The transformation process (Section 4.1) essentially creates a map of scale factors - telling the system "at this location in the image, each pixel represents this many meters."

[VISUAL PLACEHOLDER: River image divided into three zones (near, middle, far) with scale factors labeled for each. Example foam tracks shown with pixel movement (30 pixels) and resulting real distance (0.45 m, 1.35 m, 2.25 m). Caption: "Scale factor varies dramatically with distance from camera."]

---

## Ground Control Points: Establishing the Perspective Relationship

### Why We Need Multiple Reference Points

Section 4.1 introduced ground control points (GCPs) as reference markers that link pixel coordinates to real-world coordinates. Now we can understand why we need so many (6-10 GCPs) and why their placement matters.

**The perspective challenge:**
- Scale factor varies continuously throughout the scene (different at every distance from camera)
- We cannot possibly survey every single location
- We need to mathematically infer the scale factor everywhere based on known points

**The interpolation solution:**
If we survey enough reference points spread throughout the scene, we can mathematically interpolate (calculate) the scale factor at any location between the reference points.

**The puzzle analogy:**
Think of perspective correction like completing a jigsaw puzzle:
- Each ground control point is a completed piece showing the correct relationship
- The transformation process fills in the gaps between the pieces
- More pieces (GCPs) distributed throughout the puzzle make it easier to complete the picture accurately
- All pieces clustered in one corner leave most of the puzzle ambiguous

**Minimum vs. recommended GCPs:**
- **4 GCPs**: Mathematical minimum to solve the transformation equations, but no error checking, no redundancy
- **6 GCPs**: Allows error checking through redundancy, better coverage
- **8-10 GCPs**: Recommended for accurate interpolation throughout entire field of view
- **More than 10**: Diminishing returns, but helpful for very large or complex scenes

[VISUAL PLACEHOLDER: Two river images with GCP distribution overlaid. Left image labeled "Poor Distribution" shows 6 GCPs all clustered near camera. Right image labeled "Good Distribution" shows 8 GCPs spread throughout scene - near, far, left, right. Checkmark on right image.]

### Strategic GCP Placement for Perspective Correction

**Near-to-far distribution:**
GCPs should span the range of distances from camera:
- Some GCPs close to camera (near edge of field of view)
- Some GCPs at medium distance (middle of river area of interest)
- Some GCPs far from camera (far edge of field of view)

This distribution ensures accurate scale factor calculation from near to far.

**Left-to-right distribution:**
GCPs should span the width of the field of view:
- Some GCPs on the left side
- Some GCPs in the center
- Some GCPs on the right side

This ensures perspective correction works across the entire width.

**Coverage of velocity measurement area:**
GCPs should surround or encompass the area where velocity will be measured:
- If measuring velocity across the full river width, GCPs should extend to both banks
- If camera captures beyond the river (e.g., includes part of the bank), place GCPs at the actual edges of the measurement area, not at the edges of the camera view
- Avoid trying to measure velocity in areas beyond the GCP coverage (extrapolation is less reliable than interpolation)

**Practical example:**
For a river 15 meters wide, with camera mounted 8 meters above water, 12 meters from near bank:
- Place 2-3 GCPs on near bank (visible in foreground)
- Place 2-3 GCPs at mid-river (perhaps on rocks or floating markers)
- Place 2-3 GCPs on far bank (visible in background)
- Distribute along the river length (not all at one cross-section)

This 6-9 GCP distribution provides excellent coverage for perspective correction.

[VISUAL PLACEHOLDER: Overhead diagram of river showing strategic GCP placement - near bank (3 GCPs), mid-river (3 GCPs), far bank (3 GCPs), distributed along river length. Velocity measurement area shaded, showing GCPs encompass measurement zone.]

---

## Georectification: Removing Perspective Distortion

### What Georectification Means

**The term:**
Georectification is the process of transforming an image taken from a perspective view (at an angle) into an orthogonal view (looking straight down) with correct geometric scaling.

**Breaking down the term:**
- **Geo-**: relating to geographic position (earth, real-world coordinates)
- **Rectification**: making right or correcting (removing distortion)
- Combined: Making the image geometrically correct with respect to real-world geography

**The goal:**
Transform the camera's angled view into an image that shows the scene as if looking directly down from above (like a map), where:
- Parallel lines in reality appear parallel in the image
- Equal distances in reality correspond to equal distances in the image
- Scale is consistent throughout the image (like a map with a scale bar)

**Why "georectified" images are useful:**
A georectified image can be used like a map:
- Measure distances directly in the image (with consistent scale)
- Overlay the image on actual maps or satellite imagery
- Compare images from different times or different cameras (all georectified to the same coordinate system)

[VISUAL PLACEHOLDER: Before/after comparison showing camera perspective view of river (angled, perspective distortion visible) and georectified view (orthogonal, looks like map). Grid overlay on georectified version showing uniform square cells.]

### The Homography Transformation

**What is a homography?**
A homography is the mathematical transformation that converts between perspective views. It is the specific type of transformation OpenRiverCam uses to correct perspective distortion.

**What a homography does:**
- Takes pixel coordinates in the perspective image (what the camera sees)
- Transforms them to coordinates in a georectified view (overhead map perspective)
- Accounts for the specific viewing angle, camera position, and camera characteristics

**The mathematics (simplified):**
A homography uses eight parameters (numbers) to describe the perspective transformation. These eight parameters are calculated using the ground control points:
- GCPs provide known correspondences (this pixel location corresponds to this real-world location)
- Mathematical algorithms solve for the eight parameters that best fit all the GCP data
- Once calculated, the homography can transform any point in the image to real-world coordinates

**Why this matters for velocity measurement:**
When OpenRiverCam tracks foam moving from pixel (720, 450) to pixel (755, 465):
1. Apply homography to start position (720, 450) → real-world position (6.3, 8.7) meters
2. Apply homography to end position (755, 465) → real-world position (7.15, 8.8) meters
3. Calculate real-world distance: sqrt((7.15-6.3)² + (8.8-8.7)²) = 0.86 meters
4. Divide by time interval: 0.86 m / 0.2 s = 4.3 m/s velocity

The homography has automatically accounted for perspective distortion, applying the correct scale factor at each location.

**The technical note:**
You do not need to understand the detailed mathematics of homography transformations to use OpenRiverCam. The software calculates and applies homographies automatically once you provide ground control points. But understanding what a homography does helps you appreciate why GCP quality and placement matter so much.

[VISUAL PLACEHOLDER: Flowchart showing homography transformation process: "Pixel coordinates (720, 450)" → "Homography transformation (uses 8 parameters calculated from GCPs)" → "Real-world coordinates (6.3 m, 8.7 m)". Second parallel path for end position. Final box shows velocity calculation.]

### The Limitations of Homography

**What homography assumes:**
The homography transformation used by OpenRiverCam assumes all features being measured are on a flat plane (the water surface).

**Why this assumption is reasonable:**
Rivers are relatively flat (water surface is essentially planar), making homography appropriate for OpenRiverCam applications. The transformation accurately converts image positions to real-world positions for anything on the water surface.

**What happens if the assumption is violated:**
If you tried to measure the position of something not on the water surface (e.g., a bird flying 3 meters above the water, or a rock protruding 1 meter above the surface), the transformation would give an incorrect real-world position.

**Practical implication:**
OpenRiverCam tracks surface features (foam, floating debris) that are by definition on the water surface. The homography transformation works correctly for this purpose. Just remember that the system is measuring surface velocity, not velocity at depth or velocity of objects above the water.

**Advanced note (for complex installations):**
If the river has very large elevation changes within the field of view (e.g., camera sees both a lower pool and higher rapid with 2+ meters elevation difference), a single homography may not be sufficient. Multiple homographies or more complex transformations may be needed. This is rare and would be addressed during system design by technical partners.

---

## Viewing Angle Effects: Why Camera Placement Matters

### The Direct Overhead Ideal

**The ideal scenario (rarely achievable):**
Camera mounted directly above the river, looking straight down:
- Minimal perspective distortion (all parts of river similar distance from camera)
- Scale factor nearly constant throughout image
- Parallel lines remain parallel
- Measurements equally accurate everywhere

**Why this is usually impractical:**
- Requires mounting structure directly over the river (expensive, difficult to install)
- River may be too wide to capture entirely from overhead
- Mounting structure could interfere with river flow or create safety hazards
- Maintenance access is difficult

While ideal geometrically, direct overhead mounting is rarely used in practice.

[VISUAL PLACEHOLDER: Diagram showing overhead camera mount (expensive tower structure) with river below. Labels showing "Ideal geometry but impractical mounting" and challenges listed.]

### Typical Oblique Mounting

**The practical scenario:**
Camera mounted on river bank, looking across and downstream at an angle:
- Camera 5-15 meters above water level
- Camera positioned on bank or nearby structure
- Looking at river at oblique angle (30-60 degrees from vertical)
- Captures cross-section and substantial length of river

**Perspective implications:**
- Near edge of river (close to camera): Large scale, detailed view
- Far edge of river (far from camera): Small scale, compressed view
- Scale factor may vary 3-5X from near to far
- Perspective distortion is significant and must be corrected

**Why this works despite perspective distortion:**
Ground control points and homography transformation can accurately correct for perspective, even with substantial distortion. The key is having good GCP coverage throughout the perspective-distorted view.

**The trade-off:**
Oblique mounting is practical (easy installation, maintenance) but requires careful surveying (good GCP coverage) and produces more complex perspective relationships than overhead mounting.

[VISUAL PLACEHOLDER: Diagram showing oblique camera mounting on bank, looking across river at angle. Rays from camera showing perspective view of near vs. far objects. Scale factor variation illustrated with measurements.]

### Optimizing Camera Angle

While fully overhead mounting is impractical, you can optimize camera placement to minimize perspective problems:

**Height above water:**
- Higher mounting = less severe perspective distortion (viewing from farther away, more overhead-like)
- Lower mounting = more severe perspective distortion (shallower viewing angle)
- Typical: 5-10 meters above water provides good compromise

**Downstream looking angle:**
- Camera should look downstream (in the direction of flow) to capture velocity vectors along the natural flow path
- Viewing angle typically 15-45 degrees from horizontal optimizes velocity vector measurement (per SURVEY_PROCESS.md specifications)

**Distance from near edge:**
- Too close to near edge: Very high scale factor variation from near to far
- Too far from near edge: May not capture enough river detail
- Typical: Position camera so near edge is 5-15 meters away

**Field of view coverage:**
- Capture full river width plus margins (ensure GCPs can be placed near both banks)
- Capture sufficient river length (20-50 meters of river centerline) for multiple velocity measurements
- Avoid capturing excessive area beyond the river (wastes resolution)

**The site survey process (Chapter 9) includes specific guidance on camera placement optimization based on these geometric considerations.**

[VISUAL PLACEHOLDER: Four camera placement scenarios illustrated with side-view diagrams: "Too low" (severe perspective), "Good height" (moderate perspective, checkmark), "Too close" (scale variation), "Good distance" (balanced, checkmark). Each showing resulting scale factor variation graphically.]

---

## Real-World Example: Perspective Correction in Action

Let's work through a complete example showing how perspective distortion is corrected.

**Scenario:**
OpenRiverCam system monitoring a river 12 meters wide. Camera mounted on left bank, 8 meters above water surface, positioned 6 meters from near edge of water.

**Ground control points surveyed:**
- GCP1 (near left bank): Real-world position (2.0, 10.0, 142.5) meters
- GCP2 (near left, downstream): Real-world position (2.5, 18.0, 142.3) meters
- GCP3 (mid-river): Real-world position (7.0, 12.0, 140.8) meters
- GCP4 (mid-river, downstream): Real-world position (7.5, 20.0, 140.6) meters
- GCP5 (far right bank): Real-world position (13.5, 11.0, 142.0) meters
- GCP6 (far right, downstream): Real-world position (14.0, 19.0, 141.8) meters

**Image coordinates identified:**
- GCP1 appears at pixel (320, 720)
- GCP2 appears at pixel (380, 520)
- GCP3 appears at pixel (680, 650)
- GCP4 appears at pixel (720, 480)
- GCP5 appears at pixel (1520, 680)
- GCP6 appears at pixel (1550, 530)

**Calculate homography:**
Software uses these six point correspondences to calculate the eight parameters of the homography transformation. The mathematics finds the best-fit transformation that converts between pixel coordinates and real-world coordinates.

**Verify with reprojection error:**
After calculating the transformation, software checks how well it fits:
- GCP1: Reprojection error 2.3 cm (excellent)
- GCP2: Reprojection error 1.8 cm (excellent)
- GCP3: Reprojection error 3.1 cm (excellent)
- GCP4: Reprojection error 2.7 cm (excellent)
- GCP5: Reprojection error 4.2 cm (good)
- GCP6: Reprojection error 3.8 cm (good)
- RMS (overall): 3.1 cm (excellent - within survey accuracy)

Small reprojection errors confirm the homography accurately represents the perspective relationship.

**Measure velocity using the transformation:**

Frame 1 (time = 0.0 seconds):
- Foam visible at pixel (820, 580)
- Apply homography → real-world position (9.2, 15.3, 140.9) meters

Frame 2 (time = 0.2 seconds):
- Same foam now at pixel (850, 495)
- Apply homography → real-world position (10.1, 16.2, 140.9) meters

**Calculate real-world movement:**
- Distance in X: 10.1 - 9.2 = 0.9 meters
- Distance in Y: 16.2 - 15.3 = 0.9 meters
- Total distance: sqrt(0.9² + 0.9²) = 1.27 meters
- Time elapsed: 0.2 seconds
- Surface velocity: 1.27 / 0.2 = 6.35 m/s
- Average velocity (apply 0.85 factor): 6.35 × 0.85 = 5.4 m/s

**Key observation:**
The foam moved only 30 pixels horizontally in the image (from pixel 820 to 850), but this corresponded to 0.9 meters in reality because the homography applied the correct scale factor for that location in the scene (middle of river, moderate distance from camera).

If we had tried to use a single constant scale factor (e.g., "1 pixel = 3 cm everywhere"), we would have calculated 30 pixels × 0.03 m/pixel = 0.9 m, which happens to match in this case. But at a different location in the image (near bank or far bank), the constant scale factor would give wrong results.

The homography automatically handles the varying scale factor, giving correct results everywhere in the image.

[VISUAL PLACEHOLDER: Complete example illustrated with four panels: 1) River overhead view showing GCP positions with coordinates, 2) Camera image showing GCP pixel positions, 3) Foam tracking with pixel positions labeled, 4) Transformed real-world positions showing actual movement with velocity calculation.]

---

## Perspective Distortion vs. Other Distortions

It is helpful to understand how perspective distortion relates to the other distortions discussed in this chapter:

### Comparison Summary

| Distortion Type | Cause | Effect | Correction Method | Correction Timing |
|-----------------|-------|--------|------------------|------------------|
| **Lens Distortion** (Section 4.2) | Curved lens elements | Straight lines appear curved | Camera calibration | Applied before transformation |
| **Perspective Distortion** (This section) | Oblique viewing angle | Scale varies with distance | Homography transformation (using GCPs) | Applied during coordinate transformation |
| **Atmospheric Distortion** (Section 4.4) | Heat shimmer, air turbulence | Image wavers and blurs | Time averaging, optimal conditions | Minimized during image capture |

### Correction Order

The distortions are corrected in sequence:

1. **First: Lens distortion correction**
   - Unwarp the image to remove optical artifacts
   - Results in geometrically straight image of the perspective-distorted scene

2. **Second: Perspective distortion correction (transformation)**
   - Apply homography to convert from perspective view to georectified coordinates
   - Account for scale variation with distance from camera
   - Results in real-world measurements

3. **Throughout: Atmospheric distortion minimization**
   - Capture images during optimal conditions (avoid midday heat)
   - Average multiple measurements to reduce random shimmer effects

**Why order matters:**
Perspective correction (homography) assumes straight lines are straight. If lens distortion is not corrected first, the homography will try to fit a transformation to curved lines, resulting in errors.

Think of it like this:
- Lens correction: Fix problems with the camera equipment itself
- Perspective correction: Fix problems with the geometry of viewing the 3D world in 2D
- Atmospheric correction: Minimize random environmental effects

All three must be addressed for accurate measurements.

[VISUAL PLACEHOLDER: Flowchart showing correction sequence: "Raw camera image" → "Lens correction (unwarp)" → "Lens-corrected image" → "Perspective correction (homography)" → "Georectified coordinates" → "Velocity measurement". Atmospheric effects shown as noise throughout process, minimized by averaging.]

---

## Common Problems and Solutions

### Problem 1: "Velocity measurements are accurate in the center of the river but wrong near the banks"

**Likely cause:**
Ground control points are not well-distributed. GCPs may be clustered in the center, leaving the banks poorly covered. Homography cannot accurately interpolate to areas far from GCPs.

**Solution:**
- Add GCPs on or near both banks
- Ensure GCPs span the full width of the velocity measurement area
- Recalculate transformation with better GCP distribution

### Problem 2: "Velocity measurements seem accurate in the foreground but wrong in the background"

**Likely cause:**
GCPs are not well-distributed from near to far. All GCPs may be close to camera, leaving distant areas poorly covered.

**Solution:**
- Add GCPs at medium and far distances from camera
- Ensure GCPs span the full depth (near-to-far) of the field of view
- Consider adding floating GCPs if mid-river placement is difficult

### Problem 3: "Reprojection errors are large (>10 cm), and there is no obvious pattern"

**Likely causes:**
- GCPs were surveyed with insufficient accuracy (meter-level GPS instead of RTK)
- GCPs were identified incorrectly in the image (wrong pixels clicked)
- GCPs moved between survey and image capture
- Water surface elevation changed significantly

**Solution:**
- Verify survey accuracy (must be RTK or total station, not standard GPS)
- Carefully recheck GCP identification in image (zoom in, identify exact pixel)
- Confirm GCPs are stable (not moved by erosion, flooding, or vandalism)
- Resurvey water level and verify it matches the image being configured

### Problem 4: "Reprojection errors show a systematic pattern (e.g., all larger on the right side of the image)"

**Likely causes:**
- Lens distortion is not properly corrected (creating systematic errors)
- Water surface is not planar (large waves, rapids, varying elevation across width)
- Camera moved slightly between calibration and current use

**Solution:**
- Verify lens distortion correction is applied correctly
- Consider if water surface assumption is valid (calm water required for standard homography)
- Check camera mounting stability (may have shifted since installation)
- For non-planar water surfaces, consult technical support for advanced transformation options

### Problem 5: "Everything seems correct but velocity measurements are consistently too high or too low"

**Likely causes:**
- Survey coordinate system error (surveyed in wrong datum or units)
- Water level error (GCP elevations referenced to wrong water surface elevation)
- Systematic scale error in survey (equipment miscalibration)

**Solution:**
- Verify survey coordinate system and units (must be in meters, correct datum)
- Check water level measurement methodology
- Perform independent verification measurement (measure known distance in field, compare with transformed measurement)

[VISUAL PLACEHOLDER: Five scenarios illustrated showing the symptoms and visual indicators of each problem type, with checkboxes for diagnostic steps.]

---

## Advanced Topic: Why Camera Height and Angle Matter

Now that you understand perspective distortion, we can explain why Chapter 7 (Camera Installation) emphasizes specific mounting heights and angles.

### The Foreshortening Effect

**What is foreshortening?**
When viewing objects at a shallow angle (looking along them rather than across them), distances in the direction away from you appear compressed. Railroad tracks demonstrate this - the ties (perpendicular to your view) remain visible, but the spacing between ties (along your view direction) appears to shrink with distance.

**For river monitoring:**
If the camera looks along the river (flow direction) at a very shallow angle:
- Velocity in the across-river direction is measured accurately (perpendicular to view)
- Velocity in the downstream direction appears compressed (foreshortened)
- Errors in downstream velocity component affect total velocity calculation

**Optimal angle:**
Camera should look across the river at a viewing angle of 15-45 degrees from horizontal (per SURVEY_PROCESS.md), not directly along the flow direction. This minimizes foreshortening while still capturing the velocity vector.

### The Resolution Trade-Off

**Higher mounting = lower resolution:**
- Camera at 15 meters height captures large area but with lower pixels-per-meter
- Camera at 5 meters height captures smaller area but with higher pixels-per-meter
- Higher resolution enables tracking smaller features (smaller foam, less visible tracers)

**Higher mounting = less perspective distortion:**
- Camera at 15 meters height views river more overhead-like (less scale variation)
- Camera at 5 meters height views river more obliquely (more scale variation)
- Less perspective distortion means less demanding correction requirements

**The compromise:**
OpenRiverCam installations typically use 5-10 meter mounting heights (per SURVEY_PROCESS.md specifications). This provides:
- Sufficient resolution to track typical river surface features
- Manageable perspective distortion that can be corrected with proper GCPs
- Practical mounting structures (not excessively tall)
- Maintainable access for servicing
- Heights toward the lower end (5-7m) are preferable when river width allows

**Site-specific optimization:**
The ideal height depends on:
- River width (wider rivers benefit from higher mounting)
- Camera resolution (higher megapixel cameras can mount higher without losing tracking ability)
- Available mounting structures (use what is practical and stable)
- Expected tracer sizes (visible foam, seeded tracers, etc.)

Chapter 7 provides detailed guidance on evaluating these factors for specific sites.

[VISUAL PLACEHOLDER: Graph showing height above water (vertical axis, 0-20m) vs. both resolution (pixels per meter, declining curve) and perspective distortion (increasing curve). Optimal zone highlighted around 8-12m where curves intersect favorably.]

---

## Connection to Surveying (Chapter 9)

Understanding perspective distortion clarifies why the surveying chapter emphasizes specific practices:

**Why RTK accuracy matters:**
Small survey errors (2-3 cm) remain small after homography transformation. Large survey errors (50 cm+) remain large and corrupt the transformation at every location.

Perspective correction cannot fix bad survey data - it relies on accurate survey data to work correctly.

**Why GCP distribution matters:**
The homography interpolates between GCPs. Good distribution (near/far, left/right) enables accurate interpolation everywhere. Poor distribution (all GCPs clustered) leaves large areas with uncertain transformation.

**Why water level matters:**
The homography assumes all features are on a plane (the water surface). If water level changes significantly between survey and measurement, the plane elevation changes, making the homography incorrect.

This is why water level must be recorded during GCP survey and updated if water level changes substantially.

**Why survey timing matters:**
GCPs must be surveyed during conditions representative of monitoring operations:
- Similar water level
- Similar lighting (to enable GCP identification in images)
- Stable conditions (GCPs not underwater or recently disturbed)

Surveying during low flow then trying to measure during high flow creates errors because the geometric relationship has changed.

**The integrated process:**
Surveying and perspective correction are not separate steps - they are integrated parts of establishing accurate measurement capability. Good surveying enables accurate perspective correction. Poor surveying makes perspective correction impossible, regardless of sophisticated algorithms.

This is why OpenRiverCam emphasizes survey quality so heavily. The entire system depends on it.

---

## Summary: Key Concepts to Remember

**What perspective distortion is:**
The geometric effect that makes objects farther from the camera appear smaller, even though they have not changed size. Results in scale variation throughout the image - scale factor depends on distance from camera.

**Why it occurs:**
Fundamental geometry of viewing 3D scenes from a single viewpoint. Light from distant objects enters the camera at narrower angles than light from nearby objects, causing different apparent sizes.

**Key demonstrations:**
- Railroad tracks appearing to converge (parallel lines appear to meet)
- Tiles appearing different sizes with distance (same-size objects appear different)
- Table appearing trapezoidal when viewed at angle (shape appears distorted)

**Effects on measurement:**
Without correction, the same pixel distance represents different real-world distances depending on location in the image. Scale factor can vary 3-5X from near to far in typical oblique views.

**The correction method:**
Georectification using homography transformation:
1. Survey ground control points (establish real-world positions)
2. Identify GCPs in image (establish pixel positions)
3. Calculate homography (8-parameter transformation linking the two)
4. Apply homography to all tracked features (correct perspective automatically)

**GCP requirements:**
- **Minimum**: 6 GCPs with good distribution
- **Recommended**: 8-10 GCPs spanning full field of view
- **Distribution**: Near to far, left to right, surrounding measurement area
- **Accuracy**: RTK survey (2-3 cm accuracy) required

**Camera placement implications:**
- Higher mounting reduces perspective distortion (more overhead-like view)
- Moderate viewing angle avoids foreshortening (don't look directly along flow)
- Standard specifications: 5-10 meters height, 15-45 degrees viewing angle (per SURVEY_PROCESS.md)
- Site-specific optimization based on river width, camera resolution, practical constraints
- Lower heights (5-7m) preferable when river width allows

**Relationship to other distortions:**
- Lens distortion corrected first (unwarp image)
- Perspective distortion corrected second (homography transformation)
- Atmospheric distortion minimized throughout (environmental effects)

**Why perspective correction is critical:**
Unlike lens distortion (camera artifact) or atmospheric distortion (random effects), perspective distortion is large, systematic, and affects every measurement. Velocity calculations would be completely wrong without proper perspective correction through georectification.

**The practical takeaway:**
You do not need to calculate homographies yourself - the software does this automatically. But understanding perspective distortion helps you:
- Place GCPs strategically for good coverage
- Understand why survey accuracy matters so much
- Optimize camera mounting for better geometry
- Troubleshoot when measurements seem wrong in specific areas
- Appreciate the integrated nature of surveying and measurement

Perspective distortion is the most complex concept in OpenRiverCam imaging principles, but also the most important. Take time to understand it, because this understanding will guide every aspect of your system deployment from site selection through camera mounting to survey execution.

---

**Next Section:** [4.4 Atmospheric Distortion](04-atmospheric-distortion.md)

[VISUAL PLACEHOLDER: Comprehensive one-page infographic showing: railroad tracks convergence example, scale factor variation graph, GCP distribution diagram, homography transformation flowchart, camera placement optimization diagram, and connection to surveying process. Central message: "Perspective distortion is large but predictable - good GCP coverage enables accurate correction."]
