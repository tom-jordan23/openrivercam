# OpenRiverCam Complete Setup Guide

## Overview
This guide provides step-by-step instructions for planning, surveying, installing, and configuring an OpenRiverCam station for river flow monitoring.

## Phase 1: Pre-Installation Planning

### 1.1 Site Selection Criteria
- [ ] River section with clear view of entire width
- [ ] Stable mounting location (bridge, pole, building)
- [ ] Height 5+ meters above maximum water level
- [ ] Access to cellular network (4G/LTE coverage)
- [ ] Security from vandalism/theft
- [ ] Legal permissions for installation

### 1.2 Equipment Preparation

#### Core Hardware Checklist:
- [ ] Raspberry Pi 5 (8GB RAM recommended)
- [ ] Camera Module v3
- [ ] MicroSD card (32GB+ high-endurance)
- [ ] 4G/LTE modem (Waveshare SIM7600G-H or SixFab)
- [ ] SIM card with data plan
- [ ] Environmental sensor (SHT30/SHT31)
- [ ] Weatherproof enclosure (IP65/67)
- [ ] Mounting hardware (brackets, screws, etc.)

#### Power System:
- [ ] Solar panel (100W+)
- [ ] MPPT charge controller
- [ ] 12V 100Ah LiFePO4 battery
- [ ] DC-DC converter (12V to 5V)
- [ ] Power cables and connectors
- [ ] Circuit protection (fuses/breakers)

#### Survey Equipment:
- [ ] RTK GPS system or high-accuracy GPS
- [ ] Measuring tape (50m+)
- [ ] Depth finder/sonar (if available)
- [ ] Markers for ground control points
- [ ] Camera/phone for documentation
- [ ] Field notebook

### 1.3 Pre-Installation Tasks
- [ ] Contact Salvador for hardware consultation
- [ ] Schedule installation with local team
- [ ] Obtain site access permissions
- [ ] Check weather forecast
- [ ] Prepare software on SD card
- [ ] Test all equipment in lab
- [ ] Create WhatsApp group for field support

## Phase 2: Site Survey Procedures

### 2.1 Initial Site Assessment
1. **Document arrival conditions:**
   - GPS coordinates of site
   - Photos from multiple angles
   - Sketch site layout
   - Note access routes and obstacles

2. **Evaluate mounting location:**
   - Measure height above water
   - Check structural stability
   - Assess sun exposure for solar panel
   - Identify cable routing paths

### 2.2 Camera Position Planning
1. **Determine optimal viewing angle:**
   - Position camera to see entire river width
   - Avoid direct sunlight glare
   - Typically 15° downward angle
   - Consider seasonal water level changes

2. **Key positioning notes from Hessel:**
   - Look across the river (left to right view preferred)
   - If mounting is too close to bank, position slightly downstream for better width coverage
   - Fix camera position before proceeding - do not move after initial setup

### 2.3 Ground Control Points (GCP) Survey

#### Essential GCP Measurements:
1. **Select 4-6 ground control points:**
   - Points visible from camera position
   - Distributed across field of view
   - Include both banks if possible
   - Mark with visible markers

2. **For each GCP, record:**
   - Precise GPS coordinates (RTK preferred)
   - Distance from camera
   - Elevation relative to water surface
   - Photo documentation
   - Permanent vs temporary marker type

3. **River measurements:**
   - Width at multiple points
   - Depth profile if possible
   - Flow direction
   - Notable features (rocks, structures)

**Important:** Per Hessel, ground control points can be temporary - they don't need to remain after survey completion.

## Phase 3: Hardware Installation

### 3.1 Mounting System
1. **Install mounting bracket:**
   - Secure to structure with appropriate hardware
   - Ensure no movement/vibration
   - Apply weatherproofing to penetrations
   - Test load capacity

2. **Mount enclosure:**
   - Orient for optimal cooling
   - Ensure door faces away from weather
   - Leave service access space
   - Install grounding if required

### 3.2 Solar Power Setup
1. **Solar panel installation:**
   - Face true south (northern hemisphere)
   - Tilt angle = latitude + 15°
   - Secure against wind loads
   - Install lightning protection

2. **Battery and controller:**
   - Install in shaded/ventilated area
   - Connect following polarity markings
   - Program charge controller settings
   - Test voltage outputs

### 3.3 Camera Installation
1. **Camera positioning (CRITICAL):**
   - Set desired field of view
   - **Fix camera firmly - do not move after this point**
   - Document exact position/angle
   - Take reference photo

2. **Cable management:**
   - Route cables with drip loops
   - Secure with weather-resistant ties
   - Apply sealant to entry points
   - Label all connections

## Phase 4: Software Configuration

### 4.1 Initial System Setup
1. **Boot Raspberry Pi:**
   ```bash
   # Connect via SSH
   ssh pi@[IP_ADDRESS]
   
   # Update system
   sudo apt update && sudo apt upgrade -y
   
   # Enable camera interface
   sudo raspi-config
   # Navigate to Interface Options > Camera > Enable
   ```

2. **Install OpenRiverCam software:**
   ```bash
   # Clone repository
   git clone https://github.com/openrivercam/openrivercam
   cd openrivercam
   
   # Create virtual environment
   python3 -m venv venv
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

### 4.2 Camera Calibration
1. **Configure camera parameters:**
   ```python
   # Edit configuration file
   nano config/camera_config.json
   
   # Set parameters:
   {
     "resolution": [1920, 1080],
     "fps": 30,
     "rotation": 0,  # Adjust based on mounting
     "exposure_mode": "auto",
     "awb_mode": "auto"
   }
   ```

2. **Define Region of Interest (ROI):**
   - Use test images to identify analysis area
   - Exclude banks and obstructions
   - Document ROI coordinates

3. **Calibrate with GCPs:**
   - Input surveyed GCP coordinates
   - Run calibration routine
   - Verify pixel-to-meter conversion
   - Save calibration matrix

### 4.3 Connectivity Setup
1. **Configure 4G modem:**
   ```bash
   # Install modem manager
   sudo apt install modemmanager network-manager
   
   # Configure APN settings
   sudo nmcli connection add type gsm \
     ifname cdc-wdm0 \
     con-name "4G" \
     apn "your-apn-here"
   ```

2. **Test data upload:**
   ```bash
   # Run upload test
   python test_upload.py
   
   # Verify on LiveORC dashboard
   ```

## Phase 5: System Testing and Validation

### 5.1 Functional Tests
- [ ] Camera captures clear images
- [ ] Environmental sensors report data
- [ ] Solar charging system working
- [ ] 4G connection stable
- [ ] Data uploads successfully
- [ ] Remote access functional

### 5.2 Analysis Validation
1. **Capture test video:**
   ```bash
   python river_analysis.py --test-mode
   ```

2. **Verify outputs:**
   - Motion detection working
   - Flow vectors reasonable
   - No false triggers
   - Data format correct

### 5.3 Environmental Testing
- [ ] System survives rain simulation
- [ ] Temperature control activates
- [ ] Power consumption within limits
- [ ] Enclosure remains sealed

## Phase 6: Documentation and Handover

### 6.1 Required Documentation
1. **Installation report including:**
   - Site photos and GPS coordinates
   - As-built configuration
   - GCP survey data
   - Calibration results
   - Contact information

2. **Maintenance guide:**
   - Cleaning schedule
   - Battery maintenance
   - Troubleshooting steps
   - Local contact details

### 6.2 Training Local Team
- [ ] Basic system operation
- [ ] Cleaning procedures
- [ ] Problem identification
- [ ] Emergency contacts
- [ ] Data access methods

## Phase 7: Post-Installation

### 7.1 Remote Monitoring Setup
1. **Configure LiveORC dashboard:**
   - Add new station
   - Set alert thresholds
   - Configure data retention
   - Enable notifications

2. **Establish monitoring routine:**
   - Daily data quality checks
   - Weekly performance review
   - Monthly maintenance reminder
   - Seasonal recalibration

### 7.2 Maintenance Schedule
- **Weekly:** Visual inspection via uploaded images
- **Monthly:** Data quality analysis
- **Quarterly:** Physical inspection and cleaning
- **Annually:** Full recalibration

## Troubleshooting Quick Reference

### Common Issues:
1. **No data upload:**
   - Check 4G signal strength
   - Verify SIM card data balance
   - Restart modem service
   - Check API credentials

2. **Poor image quality:**
   - Clean camera lens
   - Check for condensation
   - Adjust exposure settings
   - Verify focus distance

3. **Power issues:**
   - Check solar panel connections
   - Test battery voltage
   - Verify charge controller settings
   - Clean solar panel surface

## Emergency Contacts
- Hardware support: Salvador (via WhatsApp group)
- Software support: Hessel (via WhatsApp group)
- LiveORC server: [support email]
- Local technician: [to be determined per site]

## Important Notes from Hessel
1. **Camera positioning is critical** - once set, do not move
2. **Fix the camera completely** before proceeding with calibration
3. **Ground control points** don't need to be permanent
4. **Test access to LiveORC** before leaving site
5. **Include Hessel in Salvador hardware consultation** if possible

---

## Appendices

### A. Required Tools for Installation
- Drill with masonry/metal bits
- Socket wrench set
- Wire strippers/crimpers
- Multimeter
- Cable ties (UV resistant)
- Sealant/caulk gun
- Level
- Ladder/safety equipment

### B. Spare Parts Recommended
- Backup SD card with software
- Spare fuses
- Extra cable ties
- Replacement gaskets
- Cleaning supplies

### C. Data Management
- Local storage: 7-30 days
- Upload frequency: Every 6 hours
- Compression: gzip + base64
- Retention on server: Configurable

This guide should be reviewed and updated based on field experience and site-specific requirements.