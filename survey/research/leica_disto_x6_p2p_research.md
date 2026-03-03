# Leica Disto X6 P2P Research for Cross-Section Surveys

**Purpose:** Document the Leica Disto X6 with P2P (Point-to-Point) capability for river cross-section measurement as a complement to RTK wading.
**Last Updated:** 2026-03-03

---

## What is the Disto X6 P2P?

The Leica Disto X6 is a handheld laser distance meter. When mounted on the DST 360-X adapter (a precision tilt/pan mount), it gains Point-to-Point (P2P) measurement capability — the ability to measure distances and height differences between any two remote points, not just from the instrument to a target. This is similar in concept to a total station but at a fraction of the cost and complexity.

### P2P Package (SKU 950878)

The complete P2P package includes:

| Component | Description |
|-----------|-------------|
| **Leica Disto X6** | Laser distance meter, 200m range outdoors (400m with target) |
| **DST 360-X** | Precision tilt sensor adapter with 360° pan |
| **TRI 120** | Lightweight tripod (1.2m max height) |
| **GZM 3** | Reflective target plate for long-range measurements |

All four components are required for P2P functionality. The Disto X6 alone measures only direct distance from instrument to target.

---

## Key Specifications (from Leica Datasheet)

### Disto X6

| Specification | Value |
|---------------|-------|
| **Distance range (outdoor)** | 0.05 – 200 m (400 m with target plate) |
| **Distance accuracy** | ±1.0 mm typical |
| **Tilt sensor accuracy** | ±0.1° |
| **Laser type** | Class 2, 635 nm red visible |
| **IP rating** | IP65 (dust-tight, water jets) |
| **Operating temperature** | -10°C to +50°C |
| **Battery** | Li-ion, USB-C rechargeable |
| **Battery life** | ~8 hours typical (up to 4,000 measurements) |
| **Weight** | 214 g (Disto X6 alone) |
| **Bluetooth** | 4.2 LE for data transfer to phone |
| **Display** | Color touchscreen, 2.4" |

### DST 360-X Adapter

| Specification | Value |
|---------------|-------|
| **Tilt accuracy** | ±0.1° (both axes) |
| **Pan range** | 360° |
| **Tilt range** | ±65° |
| **Self-leveling** | Yes (compensator range ±5°) |
| **Mounting** | 5/8" thread (standard survey tripod) |

### P2P Measurement Accuracy

The P2P accuracy is a function of both distance accuracy (±1mm) and angle accuracy (±0.1°). At short ranges, angle error is negligible. At longer ranges, it dominates:

| Target Distance | Lateral Error (from ±0.1° angle) | Distance Error | Combined (approx.) |
|-----------------|-----------------------------------|----------------|---------------------|
| 10 m | ±17 mm | ±1 mm | ±17 mm |
| 20 m | ±35 mm | ±1 mm | ±35 mm |
| 50 m | ±87 mm | ±1 mm | ±87 mm |
| 100 m | ±175 mm | ±1 mm | ±175 mm |
| 150 m | ±262 mm | ±1 mm | ±262 mm |

**Calculation:** Lateral error = distance × tan(0.1°) ≈ distance × 0.001745

### Accuracy Assessment for River Cross-Sections

- **<30 m river width:** ±35-50 mm — adequate for monitoring-grade cross-sections
- **30-60 m river width:** ±50-100 mm — marginal for detailed work, fine for change detection
- **>60 m river width:** >100 mm — only suitable for coarse geometry, not detailed cross-sections
- **Height differences:** Same angular error applies to vertical component

**Bottom line:** The Disto X6 P2P is adequate for monitoring-grade cross-sections on rivers up to ~50m wide. For detailed hydraulic model calibration requiring <2cm accuracy, RTK wading or a total station is needed.

---

## P2P Measurement Principle

### How P2P Works

1. The Disto X6 sits on the DST 360-X adapter, which has a precision tilt sensor
2. You aim at Point A and fire the laser — the adapter records distance and tilt angle
3. You swivel to Point B and fire again — distance and tilt angle recorded
4. The instrument calculates the horizontal distance, vertical difference, and slope distance between Points A and B using trigonometry
5. You never need to walk to the measurement points

### Why This Matters for Rivers

Traditional cross-section measurement requires wading across the river with an RTK pole. This works well for shallow, safe rivers. But some rivers are:
- Too deep to wade safely
- Too fast-flowing (dangerous current)
- Contaminated or obstructed
- Inaccessible (steep banks, no wading access)

The Disto P2P allows measuring from one bank across to features on the opposite bank without entering the water. You measure from a single instrument station.

### Important Limitation: Cannot Target Water Surface

The laser cannot reliably target the water surface — it reflects, scatters, or passes through. You must aim at:
- Bank edges and features
- Stakes or markers placed at accessible points
- The GZM 3 reflective target plate (held by an assistant)
- Natural features like rocks, tree bases, structures

This means P2P does **not** directly measure submerged bed topography. It measures bank geometry and any exposed features above water. For the wetted portion, you still need RTK wading, acoustic sounding, or estimation from bank geometry.

---

## Setup Procedure for River Cross-Sections

### Equipment Setup

1. **Choose instrument station:** Select a bank position with:
   - Clear line of sight across the full cross-section
   - Stable ground (not soft mud or sand that will settle)
   - Open enough for the tripod legs to spread fully
   - Ideally 2-5m back from the bank edge for stability

2. **Set up tripod (TRI 120):**
   - Extend legs to comfortable working height
   - Press legs firmly into ground
   - Rough-level using the tripod leg adjustments

3. **Mount DST 360-X adapter:**
   - Thread onto tripod 5/8" mount
   - Attach Disto X6 to adapter
   - Power on and allow the compensator to self-level
   - Verify level indicator shows green/centered

4. **RTK-survey the instrument station:**
   - Place the RTK rover pole next to the tripod
   - Survey the exact tripod position with standard quality gates
   - Record the instrument height (tripod top to ground)
   - This gives the instrument station an absolute position in UTM

5. **Establish azimuth reference:**
   - RTK-survey a second visible point (reference direction)
   - Calculate the bearing from instrument station to reference point
   - This allows converting Disto relative measurements to absolute coordinates later

### Measurement Procedure

1. **Select P2P mode** on the Disto X6 (Menu → P2P)

2. **Measure reference direction first:**
   - Aim at your RTK-surveyed reference point
   - Fire laser to establish the azimuth baseline
   - This "orients" the Disto in absolute coordinates

3. **Measure cross-section points systematically (LB → RB):**
   - Start at the far left bank edge
   - Aim at each visible cross-section point
   - For each point, the Disto records:
     - Horizontal distance from instrument
     - Height difference from instrument
     - Bearing angle (relative to starting direction)
   - Work systematically across to the right bank

4. **Use GZM 3 reflector plate for distant targets:**
   - Targets >60m in bright sunlight may not return enough signal
   - Have an assistant hold the GZM 3 reflective plate at the target point
   - The reflector extends effective range to ~400m

5. **Take repeat measurements:**
   - 3-5 repeat measurements per critical point
   - Average the results to reduce random error
   - Discard obvious outliers (>3× typical spread)
   - Repeat measurements also catch operator errors (wrong target, tripod bumped)

### Data Recording

For each measurement point, record:
- Point ID / station number
- Horizontal distance from instrument
- Height difference from instrument
- Bearing angle (or relative angle from reference direction)
- Number of repeat measurements and spread
- Target description (bank edge, stake, rock, reflector plate)
- Notes on measurement conditions

---

## Combining Disto Data with RTK Data

### The Conversion Process

The Disto produces **relative** measurements from the instrument station (polar coordinates: distance + angle + height difference). RTK produces **absolute** coordinates (UTM easting/northing/elevation). Combining them:

1. **Instrument station position:** Known from RTK survey (E₀, N₀, Z₀)

2. **Azimuth reference:** Bearing from instrument to RTK-surveyed reference point gives the orientation of the Disto's angle system in UTM coordinates

3. **For each Disto measurement point:**
   ```
   E = E₀ + horizontal_distance × sin(bearing)
   N = N₀ + horizontal_distance × cos(bearing)
   Z = Z₀ + height_difference
   ```
   Where bearing = reference_azimuth + relative_angle_from_Disto

4. **Result:** Each Disto point now has absolute UTM coordinates that integrate with the rest of the RTK survey

### Accuracy of Combined Data

- **Horizontal position:** RTK instrument station accuracy (2-3cm) + Disto lateral error (distance-dependent)
- **Vertical position:** RTK elevation accuracy (3-5cm) + Disto height error (distance-dependent)
- At 30m range: ~5cm combined horizontal, ~6cm combined vertical
- At 50m range: ~9cm combined horizontal, ~10cm combined vertical

---

## Field Tips for Indonesia

### Timing

- **Best:** Early morning (06:00-09:00) or late afternoon (15:00-18:00)
- **Avoid:** Noon (11:00-14:00) — intense tropical sun causes:
  - Heat shimmer (refraction distorts laser path)
  - Bright ambient light reduces laser dot visibility
  - Glare on water surface
- **Overcast days:** Actually ideal for laser measurement — consistent lighting, less shimmer

### Environmental Considerations

- **Rain:** IP65 rated — survives light rain and splashes. Avoid heavy tropical downpours (impairs laser visibility). Wipe lens if water droplets form.
- **Humidity:** Tropical humidity can cause lens fogging. Keep the instrument in its case when not measuring. Allow it to acclimate to ambient temperature before use.
- **Dust/sand:** IP65 protects against dust ingress. Keep the lens cap on when not measuring.
- **Temperature:** Indonesia's tropical temperatures (25-35°C) are well within the operating range.

### Battery and Power

- Li-ion battery lasts ~8 hours of continuous use
- USB-C rechargeable — bring a power bank as backup
- In practice, P2P measurements take 1-2 hours per cross-section, well within battery capacity
- Cold weather reduces battery life, but this is not a concern in Indonesia

### Practical Tips

- Mark the instrument station with a stake/paint so you can return to the exact spot
- Photograph the setup showing tripod position relative to the river
- If measuring across a wide river, have an assistant on the far bank with the GZM 3 reflector
- Use Bluetooth to transfer measurements to your phone for backup
- The Disto can export data via Bluetooth to the Leica Disto Plan app

---

## Rental in Jakarta

### Options

1. **Leica Store Jakarta**
   - Location: Plaza Senayan, 3rd Floor
   - Contact for P2P package rental availability
   - Most likely to have genuine Leica P2P package

2. **Indosurta Group**
   - Major Indonesian survey equipment distributor
   - Multiple locations in Jakarta
   - Rents survey instruments including laser distance meters
   - Website: https://www.indosurta.co.id/

3. **Alternative: Total Station Rental**
   - If Disto X6 P2P unavailable, a basic total station provides similar functionality with better angle accuracy (±1-5" vs ±0.1°)
   - More complex to operate but well-established for cross-section surveys
   - Available from most survey equipment rental companies

### What to Verify When Renting

- [ ] Complete P2P package: Disto X6 + DST 360-X + TRI 120 + GZM 3
- [ ] Battery charged, USB-C charger included
- [ ] Calibration is current (check calibration sticker)
- [ ] Test P2P function before leaving the shop
- [ ] Confirm rental period covers your full field campaign + buffer day

---

## References

- Leica Disto X6 Datasheet: https://leica-geosystems.com/products/disto-and-leica-blk/leica-disto/leica-disto-x6
- DST 360-X Adapter: https://leica-geosystems.com/products/disto-and-leica-blk/accessories/leica-dst-360-x
- P2P Measurement Technology: Leica Disto X6 Technical Reference Manual
- GZM 3 Target Plate: Leica Accessories Catalog
