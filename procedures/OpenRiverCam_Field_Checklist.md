# OpenRiverCam Field Installation Checklist

## Pre-Departure Checklist
- [ ] Contact Salvador for hardware consultation
- [ ] Schedule call with Hessel if needed
- [ ] Create WhatsApp group with support team
- [ ] Test all equipment in lab
- [ ] Prepare SD card with software
- [ ] Charge all batteries and devices
- [ ] Check weather forecast
- [ ] Confirm site access permissions

## Equipment Checklist

### Core Hardware
- [ ] Raspberry Pi 5 (8GB)
- [ ] Camera Module v3
- [ ] MicroSD card (32GB+)
- [ ] 4G/LTE modem + SIM card
- [ ] Environmental sensor (SHT30/31)
- [ ] Weatherproof enclosure
- [ ] All mounting hardware

### Power System
- [ ] Solar panel (100W+)
- [ ] Charge controller (MPPT)
- [ ] Battery (12V 100Ah LiFePO4)
- [ ] DC-DC converter
- [ ] Fuses and breakers
- [ ] All power cables

### Survey Equipment
- [ ] GPS device (RTK preferred)
- [ ] 50m measuring tape
- [ ] GCP markers (temporary OK)
- [ ] Camera for documentation
- [ ] Field notebook
- [ ] Depth finder (if available)

### Tools
- [ ] Power drill + bits
- [ ] Wrenches/sockets
- [ ] Wire strippers
- [ ] Multimeter
- [ ] Cable ties (UV resistant)
- [ ] Sealant/caulk
- [ ] Level
- [ ] Safety equipment

## Site Survey Steps

### 1. Initial Assessment (30 min)
- [ ] Record GPS coordinates
- [ ] Take site photos (all angles)
- [ ] Sketch site layout
- [ ] Check 4G signal strength
- [ ] Identify mounting location
- [ ] Plan cable routes

### 2. Camera Positioning (45 min)
- [ ] Find view of entire river width
- [ ] Set ~15° downward angle
- [ ] Avoid glare directions
- [ ] **CRITICAL: Fix camera position**
- [ ] **Do not move camera after fixing**
- [ ] Take reference photo

### 3. Ground Control Points (1 hour)
- [ ] Select 4-6 visible points
- [ ] GPS each point precisely
- [ ] Measure distances from camera
- [ ] Photo document each GCP
- [ ] Record in field notebook
- [ ] Note: GCPs can be removed after survey

### 4. River Measurements (30 min)
- [ ] Measure width at multiple points
- [ ] Note flow direction
- [ ] Document any obstructions
- [ ] Record water level markers
- [ ] Take depth measurements if possible

## Installation Steps

### 1. Mount Hardware (1 hour)
- [ ] Install mounting bracket securely
- [ ] Mount enclosure with proper orientation
- [ ] Install solar panel (south-facing)
- [ ] Connect grounding if required
- [ ] Apply weatherproofing to all penetrations

### 2. Connect Power System (45 min)
- [ ] Wire solar panel to controller
- [ ] Connect battery with correct polarity
- [ ] Install DC-DC converter
- [ ] Add circuit protection
- [ ] Test all voltages
- [ ] Secure all connections

### 3. Install Camera (30 min)
- [ ] Mount camera at surveyed position
- [ ] **DO NOT ADJUST after positioning**
- [ ] Route cable with drip loop
- [ ] Connect to Raspberry Pi
- [ ] Take test photo
- [ ] Verify field of view matches survey

### 4. Configure System (1 hour)
- [ ] Boot Raspberry Pi
- [ ] Connect via SSH
- [ ] Run camera test
- [ ] Configure 4G connection
- [ ] Set camera parameters
- [ ] Define ROI
- [ ] Input GCP coordinates
- [ ] Run calibration

## Testing Checklist

### Functional Tests (30 min)
- [ ] Camera captures clear images
- [ ] Environmental sensors working
- [ ] Solar charging active
- [ ] 4G connection stable
- [ ] Data uploads successfully
- [ ] Remote SSH access works

### Analysis Tests (30 min)
- [ ] Run test analysis
- [ ] Check motion detection
- [ ] Verify flow vectors
- [ ] Confirm data format
- [ ] Test alert system

## Final Steps

### Documentation (30 min)
- [ ] Complete installation report
- [ ] Upload site photos
- [ ] Record all configurations
- [ ] Update LiveORC dashboard
- [ ] Send WhatsApp confirmation

### Training (30 min)
- [ ] Show local contact basic operation
- [ ] Explain cleaning procedure
- [ ] Provide troubleshooting guide
- [ ] Share emergency contacts
- [ ] Schedule first maintenance

## Before Leaving Site
- [ ] All systems operational
- [ ] LiveORC shows data
- [ ] Local contact trained
- [ ] Site is secure
- [ ] Documentation complete
- [ ] Tools accounted for

## Key Reminders from Hessel
1. **Choose camera position carefully - you cannot change it later**
2. **Fix camera completely before any calibration**
3. **Test LiveORC access before leaving**
4. **GCPs are temporary - OK to remove after survey**
5. **Include support team in setup decisions**

## Emergency Contacts
- Salvador: [Hardware support via WhatsApp]
- Hessel: [Software support via WhatsApp]
- LiveORC: [support email]
- Local: [filled on-site]

## Common Issues
- **No upload**: Check SIM data, restart modem
- **Bad images**: Clean lens, check focus
- **No power**: Check connections, clean solar panel
- **High temp**: Check fan, clear vents

---
*Time estimate: 6-8 hours total for complete installation*