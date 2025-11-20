# Appendix A: Glossary of Terms

This glossary provides simple definitions for technical terms used throughout the OpenRiverCam manual. Terms are organized alphabetically with cross-references to manual sections where concepts are explained in detail.

---

## A

**Absolute Accuracy**
The accuracy of a measurement relative to true geographic coordinates (e.g., WGS84). Contrasts with relative accuracy. For RTK surveys, absolute accuracy is initially 20-50 cm from base station survey-in, improving to 2-10 cm with PPP post-processing.
*See: Section 5.3 (RTK Fundamentals), Section 5.6 (PPP Corrections)*

**ADCP (Acoustic Doppler Current Profiler)**
Traditional instrument for measuring river flow using sound waves. Expensive and requires specialized training. OpenRiverCam provides a non-contact alternative.
*See: Section 3.3 (Conventional Methods Comparison)*

**Ambiguity (Carrier Phase)**
The uncertainty in determining which wave cycle a GPS receiver is measuring. RTK fix status indicates ambiguities are resolved. Float status indicates ambiguities are not resolved.
*See: Section 5.3 (RTK Fundamentals)*

**Antenna Reference Point (ARP)**
The specific point on a GNSS antenna where position is measured. Usually at the bottom of the antenna. Critical for accurate pole height measurements.
*See: Section 5.4 (Base and Rover Stations)*

**Area (Cross-Sectional)**
The amount of space water occupies when you slice through the river from bank to bank. Measured in square meters. Combined with velocity to calculate discharge using Q = v × A.
*See: Section 3.1 (Fundamental Relationships)*

**Atmospheric Distortion**
Changes to camera images caused by heat shimmer, humidity, or air density variations. Can affect measurement accuracy.
*See: Section 4.4 (Atmospheric Distortion)*

**AUSPOS**
Free PPP processing service provided by Geoscience Australia. Recommended for processing RINEX data from base station to improve position accuracy.
*See: Section 5.6 (PPP Corrections), SURVEY_PROCESS.md Section 10*

---

## B

**Base Station**
The stationary GPS receiver in an RTK system that establishes a reference position, measures GPS errors, and broadcasts corrections to the rover. Must remain stable throughout the survey.
*See: Section 5.3 (RTK Fundamentals), Section 5.4 (Base and Rover Stations)*

**Baseline (RTK)**
The distance between base station and rover. Shorter baselines provide better RTK accuracy. Optimal performance below 1 km, good performance 1-5 km, marginal above 5 km.
*See: Section 5.4 (Base and Rover Stations)*

**Bathymetry**
The measurement of water depth and the shape of the riverbed. Cross-section surveys provide bathymetric data needed to calculate discharge.
*See: Section 3.1 (Fundamental Relationships), Chapter 9 (Site Survey)*

**BeiDou**
Chinese GNSS satellite constellation. Modern RTK receivers track BeiDou in addition to GPS, GLONASS, and Galileo for improved satellite count and accuracy.
*See: Section 5.3 (RTK Fundamentals)*

---

## C

**Calibration (Camera)**
The process of establishing the relationship between image coordinates (pixels) and real-world coordinates (meters). Requires ground control points.
*See: Section 4.1 (Pixel to Physical Transformation), Chapter 10 (Software Configuration)*

**Carrier Phase**
Precise measurement of GPS signal wave cycles. Provides centimeter-level precision when ambiguities are resolved. The foundation of RTK accuracy.
*See: Section 5.3 (RTK Fundamentals)*

**CBFEWS (Community-Based Flood Early Warning System)**
Early warning systems managed by and for local communities using simple, low-cost technology. OpenRiverCam is well-suited for integration with CBFEWS.
*See: Section 2.1 (Humanitarian Potential), Section 2.2 (Specific Use Examples)*

**Control Points (Ground Control Points / GCPs)**
Visible targets in the camera field of view with known geographic coordinates. Minimum 6 points required. Surveyed with centimeter accuracy using RTK GPS.
*See: Section 4.1 (Pixel to Physical Transformation), Section 9.3 (Ground Control Placement)*

**Coordinate Reference System (CRS)**
The mathematical framework for assigning coordinates to locations. OpenRiverCam surveys use UTM (e.g., EPSG:32748 for UTM Zone 48 South in Indonesia).
*See: Section 5.7 (Coordinate Systems)*

**CORS (Continuously Operating Reference Station)**
Permanent GNSS base stations operated by government agencies. Can be used as virtual base stations via NTRIP instead of setting up your own base.
*See: Section 5.4 (Base and Rover Stations)*

**Cross-Section**
A profile of the riverbed from one bank to the other. Surveyed by measuring elevation points across the river width. Used to calculate cross-sectional area at different water levels.
*See: Section 3.1 (Fundamental Relationships), Section 9.11 (Cross-Section Survey)*

---

## D

**DGPS (Differential GPS)**
GPS positioning using pseudorange corrections only (not carrier phase). Achieves 0.5-2 meter accuracy. Not adequate for OpenRiverCam surveys - RTK fix required.
*See: Section 5.3 (RTK Fundamentals)*

**Discharge (Q)**
The volume of water flowing through a river cross-section per unit time. Measured in cubic meters per second (m³/s). Calculated as Q = v × A (velocity × area).
*See: Section 3.1 (Fundamental Relationships)*

**Distortion (Lens)**
Image distortion caused by camera lens optics. Barrel distortion (outward curving) common in wide-angle lenses. Corrected through camera calibration.
*See: Section 4.2 (Lens Distortion)*

**Distortion (Perspective)**
Image distortion caused by viewing angle. Objects closer to camera appear larger than distant objects. Corrected using ground control points.
*See: Section 4.3 (Perspective Distortion)*

---

## E

**ECEF (Earth-Centered, Earth-Fixed)**
A 3D Cartesian coordinate system with origin at Earth's center. GPS satellites provide coordinates in ECEF (X, Y, Z), later converted to more practical systems like UTM.
*See: Section 5.7 (Coordinate Systems)*

**Ephemeris (Satellite)**
Orbital position data for GNSS satellites. Broadcast by satellites and used by receivers to calculate positions. Logged in RINEX files for PPP processing.
*See: Section 5.4 (Base and Rover Stations), Section 5.6 (PPP Corrections)*

**EPSG Code**
Standardized numeric code identifying coordinate reference systems. Example: EPSG:32748 = WGS84 / UTM Zone 48 South.
*See: Section 5.7 (Coordinate Systems)*

---

## F

**Field of View (FOV)**
The area visible to the camera. Must include visible tracers on water surface, staff gauge, and ground control points. Assessed during installation.
*See: Section 8.4 (FOV Assessment)*

**Fix (RTK)**
RTK solution status indicating carrier phase ambiguities are resolved. Provides 1-3 cm accuracy. Required for surveying - Float or Single status not adequate.
*See: Section 5.3 (RTK Fundamentals), Section 5.5 (RTK Fix Status)*

**Float (RTK)**
RTK solution status indicating corrections are received but ambiguities are not resolved. Provides 10-100 cm accuracy. Not adequate for surveying.
*See: Section 5.3 (RTK Fundamentals), Section 5.5 (RTK Fix Status)*

**Flow (River)**
See Discharge. The volume of water passing through a river. "Flow" and "discharge" are used interchangeably in this manual.
*See: Section 3.1 (Fundamental Relationships)*

---

## G

**Galileo**
European GNSS satellite constellation. Modern RTK receivers track Galileo in addition to GPS, GLONASS, and BeiDou for improved satellite count and accuracy.
*See: Section 5.3 (RTK Fundamentals)*

**GCP**
See Ground Control Points.

**Geoid**
A model of Earth's gravity field representing mean sea level. Separates ellipsoid heights (GPS measurements) from orthometric heights (elevations above sea level).
*See: Section 5.7 (Coordinate Systems)*

**GLONASS**
Russian GNSS satellite constellation. Tracked by modern RTK receivers alongside GPS, Galileo, and BeiDou for improved satellite count and reliability.
*See: Section 5.3 (RTK Fundamentals)*

**GNSS (Global Navigation Satellite System)**
Generic term for satellite positioning systems including GPS (USA), GLONASS (Russia), Galileo (Europe), and BeiDou (China).
*See: Section 5.3 (RTK Fundamentals)*

**GNSS Master**
Android app that receives NMEA data from RTK rover via USB and provides position as mock location to other apps like SW Maps.
*See: SURVEY_PROCESS.md Appendix A*

**GPS (Global Positioning System)**
United States GNSS constellation. Often used generically to refer to all satellite positioning, though technically GPS is one of several GNSS systems.
*See: Section 5.3 (RTK Fundamentals)*

**Ground Control Points (GCPs)**
See Control Points.

---

## H

**Horizontal Accuracy**
Position accuracy in the east-north (horizontal) plane. Typically better than vertical accuracy for GNSS. RTK achieves 1-2 cm horizontal accuracy under good conditions.
*See: Section 5.3 (RTK Fundamentals)*

**Hydrograph**
A graph showing river discharge or water level over time. OpenRiverCam produces continuous hydrographs for monitoring flow conditions.
*See: Section 3.1 (Fundamental Relationships)*

---

## I

**Ionosphere**
Layer of Earth's atmosphere (60-1000 km altitude) containing charged particles that delay GPS signals. Major source of GPS error. RTK cancels ionospheric delays through differential corrections.
*See: Section 5.3 (RTK Fundamentals), Section 5.8 (Environmental Factors)*

**IP Camera**
Network camera that transmits video over internet protocol. Standard IP cameras can be used for OpenRiverCam deployments.
*See: Section 1.1 (ORC Overview), Chapter 8 (Equipment Installation)*

---

## L

**Lens Distortion**
See Distortion (Lens).

**LSPIV (Large-Scale Particle Image Velocimetry)**
Computer vision technique for measuring water velocity by tracking features on the river surface. The core technology behind OpenRiverCam.
*See: Section 4.5 (PIV Overview), Section 1.1 (ORC Overview)*

---

## M

**Mock Location**
Android feature allowing apps to override device GPS with external position data. GNSS Master provides RTK positions as mock location to SW Maps.
*See: SURVEY_PROCESS.md Appendix A*

**MSM7 (Multiple Signal Message Type 7)**
High-precision RTCM3 message format containing full carrier phase and pseudorange corrections. Required for RTK fix.
*See: Section 5.4 (Base and Rover Stations)*

**Multipath**
GPS signal error caused by signals bouncing off reflective surfaces (metal, water, buildings) before reaching antenna. Mitigated by keeping antennas away from reflective surfaces.
*See: Section 5.3 (RTK Fundamentals), Section 5.8 (Environmental Factors)*

---

## N

**NMEA**
Standard text format for GPS position data. RTK rover outputs NMEA sentences to data collector.
*See: Section 5.4 (Base and Rover Stations)*

**NTRIP (Networked Transport of RTCM via Internet Protocol)**
Method for transmitting RTK corrections over internet instead of radio. Enables unlimited range but requires cellular coverage.
*See: Section 5.4 (Base and Rover Stations)*

---

## O

**OpenPIV**
Open-source library for Particle Image Velocimetry. Used by OpenRiverCam software to analyze river surface movement.
*See: Section 4.5 (PIV Overview)*

**Orthometric Height**
Elevation above mean sea level (geoid). The familiar elevation shown on topographic maps. Contrasts with ellipsoid height measured by GPS.
*See: Section 5.7 (Coordinate Systems)*

---

## P

**Particle Image Velocimetry (PIV)**
See LSPIV.

**PDOP (Position Dilution of Precision)**
Measure of satellite geometry quality. Lower values are better. Target PDOP ≤2.5 for standard RTK surveys. PDOP >3.0 indicates satellites bunched in one area of sky.
*See: Section 5.3 (RTK Fundamentals), Section 5.5 (RTK Fix Status)*

**Perspective Distortion**
See Distortion (Perspective).

**PIV (Particle Image Velocimetry)**
See LSPIV.

**Pole Height**
Distance from survey pole tip to antenna reference point. Must be measured and recorded for each survey point to calculate ground elevation from antenna elevation.
*See: Section 5.4 (Base and Rover Stations), Section 9.7 (Camera Location Survey)*

**PPP (Precise Point Positioning)**
Post-processing technique that improves GPS position accuracy to 2-10 cm using precise satellite orbit and clock data. Applied to base station position after field survey.
*See: Section 5.6 (PPP Corrections), SURVEY_PROCESS.md Section 10*

**PtBox**
Hardware device used in some OpenRiverCam deployments for automated camera control and video collection.
*See: SURVEY_PROCESS.md Appendix D*

**Pseudorange**
GPS measurement based on signal travel time. Less precise than carrier phase. Used alongside carrier phase in RTK calculations.
*See: Section 5.3 (RTK Fundamentals)*

**pyOpenRiverCam (pyorc)**
Open-source Python library for image-based river flow analysis. The software component of OpenRiverCam.
*See: Section 1.1 (ORC Overview)*

---

## Q

**Q**
Symbol for discharge. Q = v × A (discharge equals velocity times area).
*See: Section 3.1 (Fundamental Relationships)*

---

## R

**Rating Curve**
Graph showing the relationship between water level (stage) and discharge. Once established, enables estimating discharge from water level alone. Must be updated after major floods that reshape the riverbed.
*See: Section 3.1 (Fundamental Relationships), Section 3.4 (Rating Curves)*

**Relative Accuracy**
Position accuracy between surveyed points (how accurately points relate to each other). RTK provides 1-3 cm relative accuracy. More important than absolute accuracy for OpenRiverCam transformation.
*See: Section 5.3 (RTK Fundamentals)*

**RINEX (Receiver Independent Exchange)**
Standard file format for GNSS observation data. Base station UBX logs are converted to RINEX for PPP processing.
*See: Section 5.6 (PPP Corrections), SURVEY_PROCESS.md Section 10*

**RTCM3 (Radio Technical Commission for Maritime Services)**
Standard message format for RTK corrections. Base station transmits RTCM3 messages to rover.
*See: Section 5.4 (Base and Rover Stations)*

**RTK (Real-Time Kinematic)**
GPS positioning technique using two receivers (base and rover) to achieve centimeter-level accuracy in real time. Foundation of OpenRiverCam survey work.
*See: Section 5.3 (RTK Fundamentals), Section 5.4 (Base and Rover Stations), Section 5.5 (RTK Fix Status)*

**RTKLIB**
Open-source software for GNSS data processing. CONVBIN tool converts UBX files to RINEX format.
*See: SURVEY_PROCESS.md Section 10*

**Rover (RTK)**
The mobile GPS receiver carried to survey points. Receives corrections from base station and calculates precise positions.
*See: Section 5.3 (RTK Fundamentals), Section 5.4 (Base and Rover Stations)*

---

## S

**Single (GPS Solution)**
GPS position calculated without corrections. Provides 2-10 meter accuracy. Not adequate for surveying - RTK fix required.
*See: Section 5.3 (RTK Fundamentals)*

**Staff Gauge**
A pole or board marked with measurement gradations (like a ruler) positioned in the river. Visible in camera view to measure water level.
*See: Section 3.1 (Fundamental Relationships), Chapter 8 (Equipment Installation)*

**Stage (Water Level)**
The height or depth of water in a river, measured in meters above a reference point. Used with rating curve to estimate discharge.
*See: Section 3.1 (Fundamental Relationships), Section 3.4 (Rating Curves)*

**Survey-In**
Process by which RTK base station determines its reference position by averaging GPS measurements over 30-60 minutes. Achieves approximately 25 cm absolute accuracy.
*See: Section 5.3 (RTK Fundamentals), Section 5.4 (Base and Rover Stations)*

**SW Maps**
Android/iOS data collection app used for recording RTK survey points. Displays fix status, quality indicators, and enables point collection with attributes.
*See: SURVEY_PROCESS.md Appendix B*

---

## T

**Tracer (Surface)**
Visible feature on water surface that can be tracked by camera - foam, debris, ripples, or texture. Adequate tracers are essential for OpenRiverCam to measure velocity.
*See: Section 6.1 (Visible Tracers), Section 4.5 (PIV Overview)*

**Transformation (Coordinate)**
Mathematical process of converting between coordinate systems (e.g., WGS84 to UTM). Also refers to converting image pixels to real-world coordinates using ground control points.
*See: Section 4.1 (Pixel to Physical Transformation), Section 5.7 (Coordinate Systems)*

**Troposphere**
Lower layer of Earth's atmosphere (0-10 km) that delays GPS signals. RTK cancels tropospheric delays through differential corrections.
*See: Section 5.8 (Environmental Factors)*

---

## U

**UBX**
Proprietary binary file format used by u-blox GPS receivers for logging raw satellite data. Converted to RINEX for PPP processing.
*See: Section 5.6 (PPP Corrections), SURVEY_PROCESS.md Section 10*

**u-center**
Software from u-blox for configuring GPS receivers and logging data. Used to set up RTK base station.
*See: SURVEY_PROCESS.md Appendix C*

**UTM (Universal Transverse Mercator)**
Coordinate system dividing Earth into 60 north-south zones. Provides east-north-elevation coordinates in meters. Preferred CRS for OpenRiverCam surveys.
*See: Section 5.7 (Coordinate Systems), Section 9.14 (UTM XYZ Conversion)*

---

## V

**Velocity (Water)**
Speed at which water moves downstream, measured in meters per second (m/s). OpenRiverCam measures surface velocity and adjusts by 0.85 to estimate average velocity through water column.
*See: Section 3.1 (Fundamental Relationships), Section 3.2 (Tracers and Measurement)*

**Vertical Accuracy**
Elevation accuracy. Typically worse than horizontal accuracy for GNSS by factor of 1.5-2×. RTK achieves 2-3 cm vertical accuracy under good conditions.
*See: Section 5.3 (RTK Fundamentals)*

---

## W

**WASH**
Water, Sanitation, and Hygiene - humanitarian sector responsible for water supply and sanitation services in emergency and development contexts.
*See: Section 2.1 (Humanitarian Potential), Section 2.2 (Specific Use Examples)*

**WGS84 (World Geodetic System 1984)**
Global reference ellipsoid and datum. GPS satellites broadcast positions in WGS84. Often converted to UTM for practical use.
*See: Section 5.7 (Coordinate Systems)*

---

## Acronyms and Abbreviations

**ADCP**: Acoustic Doppler Current Profiler
**ARP**: Antenna Reference Point
**CBFEWS**: Community-Based Flood Early Warning System
**CORS**: Continuously Operating Reference Station
**CRS**: Coordinate Reference System
**DGPS**: Differential GPS
**ECEF**: Earth-Centered, Earth-Fixed
**EPSG**: European Petroleum Survey Group (coordinate system registry)
**FOV**: Field of View
**GCP**: Ground Control Point
**GNSS**: Global Navigation Satellite System
**GPS**: Global Positioning System
**IP**: Internet Protocol
**LSPIV**: Large-Scale Particle Image Velocimetry
**MSM7**: Multiple Signal Message Type 7
**NMEA**: National Marine Electronics Association (data format)
**NTRIP**: Networked Transport of RTCM via Internet Protocol
**PDOP**: Position Dilution of Precision
**PIV**: Particle Image Velocimetry
**PPP**: Precise Point Positioning
**RINEX**: Receiver Independent Exchange
**RTCM3**: Radio Technical Commission for Maritime Services Version 3
**RTK**: Real-Time Kinematic
**UBX**: u-blox binary format
**UTM**: Universal Transverse Mercator
**WASH**: Water, Sanitation, and Hygiene
**WGS84**: World Geodetic System 1984

---

## Alternative Terms

**Base Station** = Reference Station, Static Receiver
**Discharge** = Flow, River Flow, Streamflow
**Fix (RTK)** = Fixed Solution, RTK Fixed
**Float (RTK)** = Float Solution, RTK Float
**GCP** = Ground Control Point, Control Point, Reference Point
**GNSS** = GPS (when used generically)
**Rating Curve** = Stage-Discharge Relationship, Stage-Discharge Curve
**Rover** = Mobile Receiver, Roving Receiver
**Stage** = Water Level, River Stage, Gauge Height
**Survey-In** = Base Station Initialization, Reference Position Establishment
**Velocity** = Water Speed, Flow Speed, Current Speed

---

**Note to Users:**
When you encounter an unfamiliar term in the manual, consult this glossary for a simple definition and reference to the section where the concept is explained in detail. Technical terms are unavoidable in a system combining hydrology, surveying, and computer vision, but every effort has been made to explain concepts in plain language.
