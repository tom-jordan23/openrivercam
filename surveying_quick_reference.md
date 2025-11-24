# Surveying Quick Reference for River Monitoring

A condensed reference guide for field use. For detailed explanations, see `surveying_concepts_explained.md`.

## Quick Decision Guide

### Which Positioning Method Should I Use?

```
Need base station position for permanent installation?
    → Use PPP (24 hours + post-processing)

Setting up temporary base for field day?
    → Use survey-in (5-10 minutes)

Measuring ground control points?
    → Use RTK with established base station

Remote location, no base station available?
    → Use PPP (collect data, post-process later)
```

## Field Checklist: Measuring GCPs

```
BEFORE measuring each point:
[ ] RTK solution status: FIXED (required)
[ ] PDOP: ≤ 3 (or ≤ 4 maximum)
[ ] Satellite count: ≥ 8
[ ] Base station: Connected and broadcasting
[ ] Sky view: Clear, no obstructions

DURING measurement:
[ ] Position antenna precisely over mark
[ ] Occupy point for 30-60 seconds
[ ] Verify RTK Fixed maintained throughout
[ ] Record position
[ ] Photograph point

AFTER measurement:
[ ] Note any warnings in field log
[ ] Verify coordinates look reasonable
[ ] Confirm point recorded in correct coordinate system
```

## Accuracy Targets

| Measurement | Target | Method |
|-------------|--------|--------|
| Base station position | 2-5 cm | PPP (24 hours) |
| GCP measurements | 1-3 cm | RTK Fixed, PDOP < 3 |
| Check point RMSE | < 5 cm | Independent validation |
| Velocity measurements | < 5-10 cm/s | Depends on GCP accuracy |
| Discharge uncertainty | < 10-15% | Cumulative effects |

## PDOP Interpretation

| PDOP | Use It? | Quality |
|------|---------|---------|
| < 2 | ✓ Yes | Excellent |
| 2-3 | ✓ Yes | Good |
| 3-4 | ✓ Yes | Acceptable |
| 4-6 | ⚠ Caution | Fair - consider waiting |
| > 6 | ✗ No | Poor - do not use |

## RTK Solution Types

| Type | Accuracy | Use for GCPs? |
|------|----------|---------------|
| RTK Fixed | 1-2 cm | ✓ YES - only this one |
| RTK Float | 10-50 cm | ✗ NO |
| DGPS | 0.5-2 m | ✗ NO |
| Autonomous | 2-10 m | ✗ NO |

## Satellite Count

| Satellites | Quality | Action |
|------------|---------|--------|
| < 4 | None | No position possible |
| 4-5 | Poor | Avoid if possible |
| 6-7 | Fair | Acceptable but not ideal |
| 8-12 | Good | Recommended minimum |
| 13+ | Excellent | Ideal conditions |

## GCP Layout Guidelines

**Minimum Setup**: 4 GCPs + 1 check point

**Recommended Setup**: 6-8 GCPs + 2 check points

**Optimal Setup**: 10-15 GCPs + 3-4 check points

**Distribution**:
- Spread GCPs around perimeter of camera view
- Include points at varying distances from camera
- Place some along riverbanks at different elevations
- Keep check points separate (not used in processing)
- Distribute check points in middle/interior of site

## Common Error Prevention

| Mistake | Impact | Prevention |
|---------|--------|------------|
| Using survey-in for permanent base | 1-5 m error | Use 24-hr PPP instead |
| Measuring with RTK Float | 10-50 cm error | Wait for RTK Fixed |
| High PDOP (> 6) | 2-10x error magnification | Wait for better geometry |
| Few satellites (< 6) | Unreliable positioning | Enable all constellations |
| No check points | Unknown accuracy | Always include 1-3 check points |
| Poor GCP distribution | Transformation errors | Distribute around site perimeter |

## File Formats & Conversion

### When to Convert to RINEX

- Post-processing with PPP services (OPUS, CSRS-PPP)
- Using RTKLIB or other open-source tools
- Data archival for long-term storage
- Sharing data between different software

### How to Convert

1. Use manufacturer's official conversion tool
2. Export as RINEX 3.x format (supports multi-GNSS)
3. Preserve original binary files as backup
4. Disable any data filtering or modification options

## PPP Processing Services

**CSRS-PPP (Canada)**
- URL: https://webapp.geod.nrcan.gc.ca/geod/tools-outils/ppp.php
- Free, no registration required
- Supports static and kinematic modes
- Typical turnaround: minutes to hours

**OPUS (USA)**
- URL: https://www.ngs.noaa.gov/OPUS/
- Free for US users
- Static mode only
- Requires 2+ hours of data
- Typical turnaround: minutes to hours

**Both require**:
- RINEX format input
- Minimum 1-2 hours data (24 hours recommended)
- Clear sky view during data collection
- Valid email for results

## Survey-In Duration Guide

| Duration | Expected Accuracy | Best Use |
|----------|------------------|----------|
| 60 seconds | 2-5 meters | Quick temporary setup |
| 5 minutes | 1-3 meters | Field surveys, relative positioning |
| 1 hour | 0.5-1 meter | Semi-permanent installations |
| 24 hours + PPP | 2-5 cm | Permanent base stations |

## Coordinate System Notes

**Critical**: Ensure all components use same coordinate system

- Base station coordinates
- GCP measurements
- Check point measurements
- Camera calibration parameters
- Photogrammetry software settings

**Common systems for river monitoring**:
- WGS84 (latitude/longitude/ellipsoid height)
- Local UTM zone (meters, easier for calculations)
- Local projected system with orthometric heights

**Verify**:
- Datum (WGS84, NAD83, etc.)
- Projection (UTM, State Plane, etc.)
- Height system (ellipsoid vs. orthometric/MSL)
- Units (meters vs. feet)

## Field Data Recording

**Minimum metadata for each GCP**:

```
Point ID: _________
Date/Time: _________
Coordinates (X/Y/Z): _________
PDOP: _________
Satellite count: _________
Solution type: _________
Occupation time: _________
Notes: _________
Photo filename: _________
```

**Base station log**:

```
Station ID: _________
Setup date/time: _________
Coordinates (X/Y/Z): _________
Position source: [ ] Survey-in [ ] PPP [ ] Known point
Antenna height: _________
Antenna type: _________
Firmware version: _________
Coordinate system: _________
Data collection period: _________
```

## Troubleshooting

### Can't Get RTK Fixed Solution

**Check**:
- Base station broadcasting corrections?
- Data link signal strength adequate?
- Base-rover distance < 20 km?
- Rover has clear sky view?
- PDOP < 6?
- At least 5 satellites visible?
- Initialization time elapsed (1-2 minutes)?

**Try**:
- Move to location with clearer sky view
- Wait for better satellite geometry
- Check base station is receiving corrections
- Verify coordinate system matches between base/rover
- Power cycle rover receiver

### High PDOP Values

**Check**:
- Satellite count (need 8+)
- Sky obstructions (trees, buildings, terrain)
- Time of day (some times have poor geometry)

**Try**:
- Enable all constellations (GPS+GLONASS+Galileo+BeiDou)
- Wait 30-60 minutes for satellite geometry to improve
- Move to location with less obstructions
- Use satellite planning tools to identify better times

### Check Points Show Large Errors

**Investigate**:
- Were all GCPs measured with RTK Fixed?
- Was PDOP < 4 for all measurements?
- Is base station position accurate?
- Are coordinates in correct system?
- Were GCPs well-distributed?
- Any measurement blunders (antenna height, point ID mix-ups)?

**Solutions**:
- Remeasure GCPs with better conditions
- Verify base station position with PPP
- Add more GCPs for better distribution
- Check for systematic coordinate system errors

## Equipment Maintenance

**Before each field session**:
- Charge all batteries (base, rover, radios)
- Verify firmware is up to date
- Test base-rover communication
- Bring backup batteries and cables
- Load current base station coordinates

**After each field session**:
- Download and backup all data files
- Clean equipment (especially antenna connectors)
- Check for firmware or ephemeris updates
- Document any issues or anomalies
- Archive field notes and photos

**Periodic calibration**:
- Verify antenna height measurements (monthly)
- Check base station position stability (quarterly)
- Validate against known benchmarks (annually)
- Update receiver firmware (as released)

## Safety and Best Practices

**Field safety**:
- Always wear appropriate PPE near rivers
- Never work alone in remote locations
- Carry communication device (satellite phone/radio)
- Be aware of weather and water level changes
- Use appropriate sun protection for long occupations

**Data safety**:
- Backup data files immediately after collection
- Maintain multiple backup copies
- Include metadata with all files
- Use consistent file naming conventions
- Archive raw data before any processing

**Quality assurance**:
- Always measure check points
- Document conditions during measurements
- Photograph all GCP locations
- Record equipment serial numbers
- Maintain field logs with observations

## Quick Conversion Factors

**Position accuracy to velocity uncertainty** (approximate):
- 1 cm position error ≈ 1-2 cm/s velocity error
- 5 cm position error ≈ 5-10 cm/s velocity error
- 10 cm position error ≈ 10-20 cm/s velocity error

**Velocity uncertainty to discharge uncertainty** (approximate):
- 5 cm/s velocity error ≈ 5-10% discharge error
- 10 cm/s velocity error ≈ 10-20% discharge error

**PDOP multiplication effect** (approximate):
- Actual error ≈ Receiver precision × PDOP
- Example: 1 cm receiver × PDOP 3 = 3 cm error

## Resources

**Software**:
- RTKLIB (open source): http://www.rtklib.com/
- Emlid Studio (PPK): https://emlid.com/
- Coordinate conversion: https://www.ngs.noaa.gov/TOOLS/

**Online services**:
- CSRS-PPP: https://webapp.geod.nrcan.gc.ca/geod/tools-outils/ppp.php
- OPUS: https://www.ngs.noaa.gov/OPUS/
- Satellite visibility: https://www.gnssplanning.com/

**Education**:
- Penn State GEOG 862: https://www.e-education.psu.edu/geog862/
- IGS resources: https://igs.org/

---

**Last Updated**: 2025-11-24
**For detailed explanations**: See `surveying_concepts_explained.md`
