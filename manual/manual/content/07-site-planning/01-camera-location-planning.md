# 7.1 Camera Location and Installation Planning

Having selected a suitable site using the criteria from Chapter 6, the next critical step is determining the precise camera location and planning the physical installation. This section provides practical guidance on camera placement, viewing angles, mounting structures, and infrastructure requirements.

## Understanding Viewing Angles and Perspective

The camera's viewing angle is one of the most critical factors determining measurement accuracy. As discussed in Section 4.3, perspective distortion increases significantly when the camera angle deviates from optimal ranges.

### Optimal Viewing Angle Range

For accurate discharge measurements, OpenRiverCam requires a viewing angle between 15 and 45 degrees from horizontal (Ran et al., 2016). Below the minimum angle of 15 degrees, the camera views the water surface too obliquely, making it difficult to track surface features and ground control points effectively. The optimal range of 20-30 degrees provides the best balance between surface visibility and measurement accuracy, minimizing perspective distortion while maintaining adequate feature resolution (Tauro et al., 2016). Above the maximum angle of 45 degrees, perspective distortion increases rapidly, substantially reducing measurement precision. As a key principle, lower viewing angles (closer to horizontal) generally provide superior results, provided the water surface and banks remain clearly visible in the field of view.

### Height Requirements

The camera height above the water surface directly affects the achievable viewing angle and field of view:

**Standard height range: 5-10 meters above water surface** (per SURVEY_PROCESS.md specifications)

**Typical applications by river width:**
- **Small streams (5-15m width)**: 5-7 meters (lower end of range adequate)
- **Medium rivers (15-40m width)**: 7-10 meters (standard range optimal)
- **Large rivers (40m+ width)**: 9-10 meters (upper end of range, may require wider lens)

**Important considerations**:
- These heights assume bank-mounted installations
- Bridge-mounted installations may require different heights depending on bridge elevation
- Heights above 10m may be necessary for very wide rivers but require careful attention to perspective distortion (see Section 4.3)
- Lower heights (5-7m) are preferable when achievable, minimizing perspective effects

### Calculating Required Height

To determine the minimum height needed for your site:

1. **Measure the distance** from the intended camera location to the far bank (cross-stream distance)
2. **Select your target viewing angle** (recommend 20-30 degrees)
3. **Calculate minimum height** using: Height = Distance × tan(angle)

**Example calculation:**
- River width: 30 meters
- Target angle: 25 degrees
- Minimum height: 30 × tan(25°) = 30 × 0.466 = 14 meters

This calculation provides the minimum height to achieve your target angle to the far bank. Additional height may be needed to ensure the near bank is also visible.

## Field of View Planning

The camera's field of view (FOV) must capture the entire measurement cross-section while including sufficient visible reference features.

### Essential FOV Requirements

Your camera placement must ensure the field of view includes:

1. **Complete river width**: From bank to bank across the measurement section
2. **Both riverbanks**: Including visible ground control point locations
3. **Representative flow area**: Capturing the main flow channels and avoiding dead zones
4. **Reference features**: Fixed objects for stabilization (rocks, vegetation, structures)
5. **Stage reference**: Water level indicators if available (staff gauges, marked boulders)

### Horizontal Coverage

The horizontal field of view depends on:
- Camera lens focal length (typically 4mm for standard systems)
- Camera distance from the water surface
- Camera viewing angle

**Practical tip**: Most standard OpenRiverCam setups using 4mm lenses achieve horizontal coverage of 1.5 to 2 times the camera height. A camera at 10 meters height typically covers 15-20 meters horizontally.

### Vertical Coverage

Ensure vertical coverage includes:
- **High water conditions**: Sufficient view upstream/downstream to capture flood flows
- **Low water conditions**: Near-bank areas remain visible during low flow periods
- **Transition zones**: Areas where flow velocity changes significantly

## Using the Camera Placement Calculator

OpenRiverCam provides a camera placement calculator spreadsheet to help plan installations. This tool is available in the project repository and should be used during site planning.

### Calculator Inputs

The calculator requires the following site information:

1. **River characteristics**:
   - River width at measurement section (meters)
   - Typical water surface elevation
   - Bank heights on each side

2. **Available mounting locations**:
   - Distance from water's edge
   - Available mounting heights
   - Orientation possibilities

3. **Camera specifications**:
   - Lens focal length (typically 4mm)
   - Sensor size (default values provided)
   - Image resolution

### Calculator Outputs

The calculator provides:

1. **Viewing angle**: Calculated angle to the water surface
2. **Field of view dimensions**: Horizontal and vertical coverage in meters
3. **Ground sampling distance**: Effective pixel resolution on the water surface
4. **Suitability assessment**: Whether the configuration meets minimum requirements

### Using Calculator Results

**Green status (suitable)**: Viewing angle and coverage meet requirements - proceed with planning

**Yellow status (marginal)**: Configuration barely meets requirements - consider alternatives if possible

**Red status (unsuitable)**: Viewing angle or coverage inadequate - must modify camera location or height

## Mounting Structure Options

The mounting structure must provide a stable platform at the required height and location. Several options are available depending on site conditions and budget.

### Existing Structures

Utilizing existing structures reduces cost and installation complexity:

**Bridges**:
- Advantages: Stable platform, established access, often optimal viewing position
- Considerations: Vibration from traffic, permission requirements, power access
- Installation: Side-mounting brackets, weatherproof housing

**Buildings**:
- Advantages: Security, power access, maintenance access
- Considerations: Viewing angle limitations, ownership/permission
- Installation: Wall-mounting brackets, cable routing

**Trees**:
- Advantages: Low cost, minimal infrastructure, natural camouflage
- Considerations: Growth and movement, seasonal changes, stability
- Installation: Tree-mounting straps (avoid nails/screws), flexible mounting

**Utility poles**:
- Advantages: Appropriate height, established infrastructure
- Considerations: Permission requirements, power access, stability
- Installation: Pole-mounting hardware, weatherproof enclosure

### New Structures

When existing structures are unavailable, purpose-built structures are required:

**Scaffolding towers**:
- Advantages: Adjustable height, relatively quick installation, relocatable
- Considerations: Stability requirements, visual impact, cost
- Typical cost: 500-1,500 USD depending on height and specifications
- Installation time: 1-2 days with appropriate tools

**Metal poles**:
- Advantages: Permanent installation, minimal visual impact, good stability
- Considerations: Requires concrete foundation, specialized installation
- Typical cost: 800-2,000 USD for 10-15m pole with foundation
- Installation time: 2-3 days including foundation curing

**Wooden structures**:
- Advantages: Lower cost, locally available materials, customizable
- Considerations: Durability concerns, maintenance requirements, treatment needed
- Typical cost: 300-800 USD depending on design and materials
- Installation time: 2-4 days depending on complexity

### Structure Stability Requirements

All mounting structures must provide:

1. **Vertical stability**: Minimal swaying or movement in typical wind conditions
2. **Foundation integrity**: Adequate anchoring to resist environmental forces
3. **Vibration resistance**: Structure does not oscillate from wind or other sources
4. **Load capacity**: Supports camera system weight plus environmental loads (wind, ice)

**Stability testing**: After installation, manually shake or push the structure. Any movement should dampen within 1-2 seconds. Visible swaying or continued oscillation indicates inadequate stability.

## Infrastructure Assessment

Before finalizing camera location, assess the infrastructure requirements and accessibility:

### Access Requirements

**During installation**:
- Vehicle access for equipment and materials
- Working space for assembly
- Tool and equipment requirements
- Personnel safety considerations

**For maintenance**:
- Regular access path (at least quarterly)
- Ladder or climbing equipment needs
- Safety equipment requirements
- Seasonal access limitations

### Site Preparation Needs

**Ground preparation**:
- Foundation excavation for new structures
- Ground leveling for equipment placement
- Drainage considerations
- Vegetation management

**Safety infrastructure**:
- Ladder or climbing system
- Fall protection anchor points
- Working platform if needed
- Safety barrier for public areas

### Utility Access

**Power source location**:
- Distance to grid connection if available
- Solar panel mounting location
- Cable routing path
- Protection requirements

**Communication infrastructure**:
- Cellular signal strength at mounting height
- WiFi access point location if applicable
- Satellite view availability
- Antenna mounting requirements

## Camera Orientation and Alignment

Precise camera orientation ensures optimal viewing angle and field of view coverage.

### Horizontal Alignment

The camera should be oriented to view the measurement cross-section perpendicular to the primary flow direction:

**Optimal orientation**:
- Camera viewing axis perpendicular to flow direction
- Equal coverage on both banks
- Centered on the main flow channel

**Acceptable deviations**:
- Up to 15 degrees off perpendicular
- Asymmetric coverage if justified by channel geometry
- Slight upstream/downstream angle if needed for reference features

### Vertical Alignment

Set the vertical angle to achieve the target viewing angle calculated earlier:

**Adjustment process**:
1. Mount camera at planned height
2. Set initial angle using inclinometer or angle gauge
3. Check field of view using live preview
4. Fine-tune angle to capture required features
5. Secure mounting hardware

**Verification**: The water surface should occupy approximately the middle third of the image frame, with visible bank areas above and below.

### Rotation (Roll) Alignment

The camera must be level horizontally to prevent image distortion:

**Alignment method**:
1. Use bubble level on camera mounting bracket
2. Check that horizon line is horizontal in image
3. Verify riverbanks appear at consistent angles
4. Secure mounting after achieving level alignment

**Acceptable tolerance**: Less than 2 degrees rotation from level. Greater rotation causes geometric distortions that reduce measurement accuracy.

## Site-Specific Considerations

### Steep Terrain

When deploying on steep riverbanks or gorges:

**Challenges**:
- Achieving low viewing angles requires greater height
- Access for installation and maintenance more difficult
- Foundation stability critical on sloped ground
- Cable routing more complex

**Solutions**:
- Consider mounting on opposite (higher) bank if available
- Use extended mounting brackets to project camera outward
- Install safety anchors and fall protection systems
- Plan cable routing carefully to prevent damage

### Bridge Installations

Bridge-mounted systems offer advantages but require specific considerations:

**Advantages**:
- Established access for maintenance
- Typically optimal height and viewing position
- Power may be available from bridge lighting
- Protection from vandalism

**Challenges**:
- Vibration from traffic affects image stability
- Permission requirements from authorities
- Mounting hardware must not damage structure
- Cable routing through/along bridge structure

**Vibration mitigation**:
- Use vibration-damping mounting hardware
- Mount on bridge piers rather than deck if possible
- Enable image stabilization in software
- Accept reduced accuracy during heavy traffic periods

### Vegetation Management

Vegetation can obstruct the field of view or damage equipment:

**Initial clearing**:
- Remove overhanging branches that may enter FOV
- Clear mounting area to prevent interference
- Maintain clear line of sight to river surface
- Remove vegetation that may contact cables

**Ongoing management**:
- Plan quarterly vegetation inspection/trimming
- Monitor for seasonal growth patterns
- Consider faster-growing species near camera
- Budget for regular maintenance access

### Seasonal Variations

River conditions change seasonally, affecting camera placement decisions:

**Flow stage variations**:
- Ensure FOV captures both low and high water levels
- Plan GCP locations visible across flow range
- Consider seasonal vegetation changes
- Account for ice formation in cold climates

**Access variations**:
- Wet season access limitations
- Flood risk to equipment and infrastructure
- Dry season maintenance windows
- Seasonal security considerations

## Pre-Installation Site Documentation

Before finalizing plans and proceeding to installation, thoroughly document the site:

### Photographic Documentation

Capture images showing:
1. Overall site context from multiple angles
2. Proposed camera location and mounting area
3. River cross-section from camera perspective
4. Access routes and approaches
5. Reference features and GCP locations
6. Existing infrastructure relevant to installation

### Measurements and Sketches

Record critical dimensions:
1. River width at measurement section
2. Distance from camera location to water's edge
3. Available mounting heights
4. Distance to power source or solar panel location
5. Cable routing distances
6. Access path dimensions and constraints

### Site Plan Drawing

Create a simple sketch showing:
- River alignment and flow direction
- Proposed camera location and viewing direction
- GCP locations on both banks
- Power system location
- Access paths
- Notable features and constraints

This documentation supports detailed installation planning, equipment procurement, and provides reference for future maintenance or troubleshooting.

## Integration with Ground Control Points

Camera location planning must be coordinated with GCP placement (discussed in Section 8.3):

**Visibility requirements**:
- All GCPs must be clearly visible in camera FOV
- GCPs should be distributed across the image frame
- Minimum 4 GCPs required, 6-8 recommended
- GCPs should remain visible across flow stage variations

**Geometric distribution**:
- GCPs near each bank (both sides)
- GCPs at different distances from camera
- GCPs at different elevations if possible
- Avoid clustering all GCPs in one area

**Verification**: Once camera position is determined, mark proposed GCP locations and verify visibility from that position before finalizing plans.

## Common Planning Mistakes to Avoid

Learn from common errors in camera placement planning:

1. **Insufficient height**: Underestimating required height leads to excessive viewing angles and poor accuracy. Always calculate minimum height before committing to a structure.

2. **Ignoring seasonal variation**: Planning based only on current conditions without considering high/low water stages results in inadequate coverage during extreme flows.

3. **Poor GCP integration**: Finalizing camera location without verifying GCP visibility leads to installation challenges and may require relocation.

4. **Inadequate access planning**: Underestimating installation and maintenance access requirements causes delays and increased costs.

5. **Structure instability**: Choosing inadequate mounting structures to save costs results in unreliable data and potential equipment damage.

6. **Vegetation underestimation**: Failing to account for vegetation growth leads to obstructed views and frequent maintenance needs.

## Planning Checklist

Before proceeding to equipment procurement and installation, verify:

- [ ] Camera location identified with specific coordinates
- [ ] Required mounting height calculated and achievable
- [ ] Viewing angle verified within 15-45 degree range
- [ ] Field of view covers entire river width plus banks
- [ ] Camera placement calculator confirms suitability
- [ ] Mounting structure type selected and feasible
- [ ] Structure stability requirements understood
- [ ] Installation access verified and documented
- [ ] Maintenance access planned and acceptable
- [ ] GCP locations identified and visible from camera position
- [ ] Seasonal variations considered in planning
- [ ] Site documentation completed (photos, measurements, sketches)
- [ ] Power system location coordinated with camera position
- [ ] Communication infrastructure requirements identified
- [ ] Security considerations addressed in location selection

## Next Steps

With camera location and mounting requirements determined, proceed to:

- **Section 7.2**: Calculate power requirements and design power system
- **Section 7.3**: Plan network connectivity and data transmission
- **Section 7.4**: Assess security requirements and protective measures
- **Chapter 8**: Execute physical installation and system configuration

Thorough camera location planning at this stage prevents costly mistakes and ensures the deployed system can deliver accurate measurements throughout its operational life.
