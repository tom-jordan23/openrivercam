# 4.2 Lens Distortion

Section 4.1 explained how OpenRiverCam transforms pixel measurements into physical measurements. That transformation assumes the camera captures a geometrically accurate image - that straight lines in the real world appear as straight lines in the image.

But camera lenses do not capture perfect images. They introduce distortions that bend and warp what the camera sees. These distortions are predictable and correctable, but we must understand them to ensure accurate measurements.

By the end of this section, you will understand:
- What causes lens distortion
- How distortion affects measurements
- Types of distortion (barrel and pincushion)
- How distortion is corrected
- What to consider when selecting cameras for OpenRiverCam

---

## The Curved Mirror Analogy: Understanding Lens Distortion

### What You Already Know About Distorted Images

You have seen your reflection in curved surfaces:
- **Spoon reflection**: Your face looks stretched and distorted in the curved surface of a spoon
- **Car side mirror**: Objects appear distorted, often with the warning "Objects in mirror are closer than they appear"
- **Funhouse mirror**: Intentionally curved mirrors stretch and compress your image

These distortions happen because the reflecting surface is curved rather than flat. Light bounces off different angles, creating a warped image.

**Camera lenses work similarly.**

All camera lenses have curved glass elements. These curves are necessary to focus light onto the camera sensor, but they also introduce predictable distortions. The image the camera captures is slightly warped compared to reality.

[VISUAL PLACEHOLDER: Split image showing person standing in front of funhouse mirror (left) and same person in front of flat mirror (right), demonstrating how curved surfaces distort images. Caption: "Curved surfaces distort reflections. Camera lenses introduce similar distortions."]

### Why This Matters for River Monitoring

Imagine measuring the width of a river using a camera image. If lens distortion makes straight things appear curved:
- The river's edge (actually straight) might appear curved in the image
- Two markers that are equally spaced in reality might appear unevenly spaced in the image
- Distance measurements near the edges of the image will be wrong

For OpenRiverCam, which measures velocities to centimeter-level accuracy, even small lens distortions matter. If the image is warped by 2-3 pixels due to lens distortion, and we do not correct it, velocity measurements could have errors of 5-10%.

**The good news: lens distortion is predictable and correctable.**

Unlike random errors, lens distortion follows consistent patterns. Once we understand how a specific lens distorts images, we can mathematically "unwarp" the image to remove the distortion.

---

## Types of Lens Distortion

### Barrel Distortion: The Bulging Effect

**What it is:**
Barrel distortion makes images appear to bulge outward, as if wrapped around a barrel. Straight lines near the edges of the image curve outward.

**Where it occurs:**
Barrel distortion is common in:
- Wide-angle lenses (capturing a broad field of view)
- Action cameras (GoPro, similar devices)
- Smartphone cameras (especially when zoomed out)
- Inexpensive cameras with simpler lens designs

**Visual characteristics:**
- Straight lines near the center of the image appear straight
- Straight lines near the edges of the image curve outward (bulge away from center)
- The effect increases toward the corners
- The image appears to "bulge" like inflating a balloon

**The magnifying glass analogy:**
If you look through a magnifying glass held at an angle, objects near the edge appear stretched and distorted compared to objects in the center. Barrel distortion works similarly - the lens acts like it is slightly "over-magnifying" toward the edges.

**Effect on measurements:**
If you measure a distance that crosses near the edge of the image (for example, tracking foam moving from center to edge), barrel distortion will make that distance appear longer than it actually is. Without correction, velocity measurements would be overestimated.

[VISUAL PLACEHOLDER: Photo of river with straight reference lines overlaid showing barrel distortion - lines that should be straight curve outward near edges. Second image shows same photo after correction with straight lines. Labels showing "Before correction: lines curve outward" and "After correction: lines are straight"]

### Pincushion Distortion: The Pinching Effect

**What it is:**
Pincushion distortion makes images appear to be pinched inward, as if the corners are being pulled toward the center. Straight lines near the edges curve inward.

**Where it occurs:**
Pincushion distortion is common in:
- Telephoto lenses (zoomed in to distant subjects)
- Some zoom lenses at maximum zoom
- Older camera designs

**Visual characteristics:**
- Straight lines near the center appear straight
- Straight lines near the edges curve inward (toward the center)
- The image appears "pinched" like a cushion being pressed from the corners
- Less common in modern cameras than barrel distortion

**Effect on measurements:**
If you measure a distance near the edge of the image, pincushion distortion makes that distance appear shorter than it actually is. Velocity measurements would be underestimated.

[VISUAL PLACEHOLDER: Diagram showing grid pattern with three versions - ideal (no distortion), barrel distortion (bulges outward), pincushion distortion (pinches inward). Grid lines are straight, curved outward, and curved inward respectively.]

### Mustache Distortion and Complex Distortion

Some lenses exhibit more complex distortion patterns - combinations of barrel and pincushion that vary across the image. These are less common and usually occur in:
- Very wide-angle lenses
- Fisheye lenses
- Poorly designed or damaged lenses

For most OpenRiverCam deployments with standard cameras, you will encounter either barrel distortion or minimal distortion. Understanding barrel distortion is the most important practical concern.

---

## How Lens Distortion Affects OpenRiverCam Measurements

### The Velocity Measurement Chain

Recall from Section 4.1 how OpenRiverCam measures velocity:
1. Track a feature (foam) in the image from frame to frame
2. Measure how far the feature moved in pixels
3. Transform pixel movement to real-world movement in meters
4. Divide distance by time to calculate velocity

**Where distortion interferes:**

Lens distortion affects step 1 - the pixel measurements:
- Feature moves 1.0 meters in reality (straight line)
- Due to barrel distortion, the feature's path in the image appears to be 1.05 meters (curved path looks longer)
- Pixel measurement: appears to move further than it actually did
- Result: velocity overestimated by 5%

### The Geographic Variation Problem

Lens distortion is not uniform across the image. It is minimal at the center and increases toward the edges.

**Practical implication:**
- Foam tracked in the center of the image: minimal distortion, accurate measurement
- Foam tracked near the left edge: moderate distortion, measurement could have 3-5% error
- Foam tracked in the corner: maximum distortion, measurement could have 5-10% error

If distortion is not corrected, you would get different measurement accuracy depending on where in the river the foam happens to be tracked. This is unacceptable for a reliable monitoring system.

**The calibration solution:**
By measuring how much distortion occurs at every location in the image, we can correct it everywhere. This ensures consistent accuracy whether tracking features in the center or near the edges.

[VISUAL PLACEHOLDER: River image with three tracking examples marked - center (accurate), mid-edge (3% error), corner (8% error). Arrows showing foam movement paths with error percentages labeled. After correction: all show 0-1% error.]

---

## Camera Calibration: Measuring and Correcting Distortion

### What is Camera Calibration?

Camera calibration is the process of precisely measuring a camera's lens distortion pattern so it can be corrected.

**The measuring tape analogy:**
Imagine you have a measuring tape, but you discover it is slightly wrong - it stretches and compresses in different places. Before you can use it for accurate measurements, you need to figure out exactly where and how much it is wrong, then adjust your readings accordingly.

Camera calibration does this for the lens. We determine exactly how the lens distorts the image, then mathematically correct those distortions.

### How Calibration Works (Simplified)

**Step 1: Capture calibration images**
Take multiple photos of a known pattern - typically a checkerboard with precisely measured squares. The checkerboard provides straight lines and regular spacing that should appear perfectly uniform in an ideal image.

**Step 2: Detect distortion**
Software analyzes the calibration images and detects where the checkerboard lines appear curved or spacing appears uneven. These deviations reveal the lens distortion pattern.

**Step 3: Calculate correction parameters**
Mathematical algorithms calculate the distortion parameters - numbers that describe exactly how the lens distorts the image.

**Step 4: Apply correction**
When processing river monitoring videos, the software applies the correction parameters to "unwarp" each frame before performing any measurements. The corrected image now shows straight lines as straight, enabling accurate transformation and velocity measurement.

**Important note for OpenRiverCam users:**
Most modern cameras used for OpenRiverCam have already been calibrated by the manufacturer or can be calibrated using standard computer vision tools. You typically do not need to perform calibration yourself unless using uncommon camera hardware. However, understanding that calibration exists and why it matters helps you appreciate the measurement process.

[VISUAL PLACEHOLDER: Four-panel flowchart showing calibration process. Panel 1: Checkerboard pattern being photographed. Panel 2: Software detecting curved lines in image. Panel 3: Distortion parameters being calculated. Panel 4: Before/after showing warped image corrected to straight lines.]

### When Calibration is Important

**Critical scenarios:**
- Using action cameras (GoPro, similar) - these often have significant barrel distortion
- Using very wide-angle lenses to capture large river sections
- Using unknown or uncommon camera models
- When measurement accuracy is particularly critical

**Less critical scenarios:**
- Using standard commercial cameras with moderate lenses
- When manufacturer calibration data is available
- When lenses have minimal distortion (good quality telephoto or standard lenses)

If you are deploying OpenRiverCam with guidance from technical partners, they will advise whether calibration is needed for your specific camera setup.

---

## Practical Implications: Camera Selection for OpenRiverCam

Understanding lens distortion helps you make better decisions when selecting cameras for OpenRiverCam installations.

### Lens Types and Distortion Characteristics

**Wide-angle lenses (most distortion):**
- Field of view: Very broad (captures large area)
- Distortion: Significant barrel distortion
- Advantages: Covers wide river sections with single camera
- Disadvantages: Requires careful calibration, more difficult to correct
- Typical use: Narrow camera mounting positions that must cover wide rivers

**Standard lenses (moderate distortion):**
- Field of view: Moderate (natural perspective similar to human vision)
- Distortion: Minimal to moderate (varies by lens quality)
- Advantages: Good balance of coverage and accuracy
- Disadvantages: May not capture entire river width from close mounting positions
- Typical use: Most OpenRiverCam deployments

**Telephoto lenses (least distortion):**
- Field of view: Narrow (zoomed in to distant subjects)
- Distortion: Minimal (often pincushion if any)
- Advantages: Excellent geometric accuracy, minimal correction needed
- Disadvantages: Narrow field of view may require multiple cameras
- Typical use: Distant camera mounting positions or narrow river sections

### Camera Selection Recommendations

**For typical OpenRiverCam deployment:**
- Choose cameras with standard or moderate wide-angle lenses
- Avoid extreme wide-angle or fisheye lenses (excessive distortion)
- Verify that camera can be calibrated or has manufacturer calibration data
- Higher quality lenses generally have less distortion

**Quality indicators:**
- Well-known manufacturers typically design lenses with minimal distortion
- More expensive cameras often have better lens quality (but not always necessary)
- Industrial or surveying-grade cameras have excellent geometric accuracy (but may be cost-prohibitive)

**Practical compromise:**
For humanitarian deployments, standard commercial cameras (even action cameras like GoPro) can work well if properly calibrated. The key is knowing the camera's distortion characteristics and correcting for them, not necessarily using the most expensive equipment.

[VISUAL PLACEHOLDER: Table comparing three camera types (wide-angle, standard, telephoto) with columns for field of view diagram, typical distortion level, calibration difficulty, recommended use cases, and example cameras.]

---

## Distortion Correction in the OpenRiverCam Workflow

### Where Correction Happens

Distortion correction is typically performed early in the image processing workflow:

1. **Camera captures raw video** → image has lens distortion
2. **Distortion correction applied** → image is "unwarped" to remove distortion
3. **Ground control points identified** → on corrected image
4. **Transformation calculated** → using corrected image coordinates
5. **Feature tracking** → on corrected images
6. **Velocity calculated** → using accurate, undistorted pixel measurements

By correcting distortion before any measurements occur, all subsequent steps work with geometrically accurate images.

### Verification: How to Know if Distortion is Corrected

When configuring an OpenRiverCam system, you can verify that distortion correction is working:

**Visual check:**
Look at the corrected image. Straight lines in the real world (river banks, bridge edges, building lines) should appear straight in the image. If they curve, distortion correction may be incomplete or incorrect.

**Reprojection error check:**
When setting up ground control points (Section 4.1), small reprojection errors (<5 cm) indicate that the transformation is working well. If distortion is not properly corrected, reprojection errors will be large (>10 cm) and may show a pattern (for example, errors larger near image edges than center).

**Cross-check measurements:**
If possible, measure a known distance in the field (for example, distance between two permanent markers). Compare with the same distance measured in the corrected image after transformation. They should match within a few centimeters.

If verification reveals problems, distortion correction parameters may need adjustment or recalibration may be necessary.

---

## Common Problems and Solutions

### Problem 1: "My reprojection errors are large near the image edges but small in the center"

**Likely cause:**
Lens distortion is not properly corrected. The distortion is minimal at the center (so measurements there are accurate) but significant toward the edges (causing errors).

**Solution:**
- Verify that camera calibration has been performed
- Check that distortion correction is being applied in the processing workflow
- Consider recalibrating the camera if using non-standard hardware
- Redistribute ground control points to better cover the edges of the field of view

### Problem 2: "Straight objects in the image appear curved"

**Likely cause:**
Distortion correction is not being applied, or correction parameters are incorrect.

**Solution:**
- Enable distortion correction in the software settings
- Verify that correct camera calibration parameters are being used
- If using a new camera model, perform calibration
- Check that the camera lens has not been changed (if using interchangeable lens camera)

### Problem 3: "Velocity measurements vary depending on where in the river I track features"

**Likely cause:**
Uncorrected lens distortion causes measurements to be accurate in some regions (low distortion) and inaccurate in others (high distortion).

**Solution:**
- Apply proper distortion correction so accuracy is uniform across the entire image
- Verify calibration quality
- Consider using a lens with less inherent distortion if the problem persists

[VISUAL PLACEHOLDER: Three scenarios illustrated with before/after images showing the problems and visual indicators that help diagnose each issue.]

---

## Connection to Perspective Distortion (Section 4.3)

It is important to distinguish between lens distortion and perspective distortion:

**Lens distortion (this section):**
- Caused by: Curved glass in the camera lens
- Effect: Straight lines appear curved
- Solution: Camera calibration and correction
- Happens: In all camera images, regardless of what is being photographed

**Perspective distortion (next section):**
- Caused by: Viewing angle and distance from camera to objects
- Effect: Objects far from camera appear smaller than nearby objects
- Solution: Transformation using ground control points
- Happens: Whenever camera views 3D scene from a single viewpoint

**Both must be corrected:**
Lens distortion is corrected first (unwarp the image). Then perspective distortion is addressed through the transformation process (Section 4.1). Both corrections work together to enable accurate measurements.

**Think of it like this:**
- Lens distortion = fixing problems with the camera itself (bad lens)
- Perspective distortion = accounting for how 3D reality is projected onto a 2D image (geometry of viewing)

The next section (4.3) will explain perspective distortion in detail. For now, remember that lens distortion is a property of the camera hardware that must be measured and corrected, while perspective distortion is a property of geometry that must be accounted for through transformation.

---

## Summary: Key Concepts to Remember

**What lens distortion is:**
Curved glass elements in camera lenses cause images to be slightly warped - straight lines appear curved, especially near the edges of the image.

**Types of distortion:**
- **Barrel distortion** (most common): Image bulges outward, common in wide-angle lenses
- **Pincushion distortion**: Image pinches inward, common in telephoto lenses
- **Complex distortion**: Combination patterns, less common

**Why it matters:**
Lens distortion causes pixel measurements to be inaccurate, leading to velocity measurement errors if not corrected. Error is larger near image edges than center.

**How it is corrected:**
Camera calibration measures the distortion pattern, then software applies mathematical correction to "unwarp" the image before any measurements are performed.

**Camera selection implications:**
- Standard lenses typically have minimal to moderate distortion
- Wide-angle lenses have more distortion but cover larger areas
- Telephoto lenses have minimal distortion but narrow field of view
- Higher quality lenses generally have less distortion
- Any camera can work if properly calibrated

**Practical considerations:**
- Most OpenRiverCam deployments use standard commercial cameras
- Calibration is usually handled during system setup by technical partners
- Verification through reprojection errors confirms correction is working
- Distortion correction must be applied before transformation and measurement

**The key takeaway:**
Lens distortion is a predictable, correctable camera artifact. Understanding it helps you select appropriate cameras, recognize when correction may be needed, and verify that your system is measuring accurately.

---

**Next Section:** [4.3 Perspective Distortion](03-perspective-distortion.md)

[VISUAL PLACEHOLDER: Single-page summary showing a camera with light rays passing through curved lens (illustrating distortion source), before/after images showing correction, and key decision points for camera selection with distortion characteristics for each lens type.]
