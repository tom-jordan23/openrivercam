# Assembly Guide - Sukabumi Site

**Site:** Sukabumi, Indonesia (foothills)
**Type:** Solar-powered, USB camera with IR night vision
**Purpose:** Replacement of failed river monitoring unit

---

## Pre-Assembly Checklist

Complete these steps BEFORE traveling to Indonesia:

### 1. Conformal Coating (Low Humidity Environment Required)

Apply MG 422C silicone conformal coating to all PCBs:

**Boards to Coat:**
- [ ] Raspberry Pi 5
- [ ] Witty Pi 5 HAT+
- [ ] Pi-EzConnect terminal block HAT
- [ ] Numato USB relay module

**Masking (Use Kapton tape):**
- GPIO header pins (all 40 pins)
- USB-A and USB-C ports
- HDMI ports
- Ethernet port
- MicroSD card slot
- Heat sink mounting holes/thermal pad area
- Any connector that will be plugged in

**Procedure:**
1. Clean boards with IPA wipe, let dry completely
2. Apply Kapton tape to all masked areas
3. Brush thin, even coat of MG 422C on exposed PCB areas
4. Allow 24 hours cure time at room temperature
5. Remove Kapton tape after cure
6. Inspect for complete coverage, recoat bare spots if needed
7. Label each board "COATED" with date

### 2. Software Configuration

- [ ] Flash OS image to MicroSD card
- [ ] Boot Pi 5 and verify ORC software runs
- [ ] Configure Witty Pi 5 schedule (15-minute wake cycle)
- [ ] Test USB camera capture
- [ ] Configure WiFi hotspot for maintenance mode
- [ ] Set up LED GPIO control script
- [ ] Set up relay control service (systemd)
- [ ] Pre-configure Telkomsel APN (if known)

### 3. Hardware Testing

- [ ] Test Pi 5 + Witty Pi 5 + Pi-EzConnect stack boots correctly
- [ ] Verify SSD is recognized via USB
- [ ] Test LTE modem connects (with test SIM)
- [ ] Test USB camera captures video
- [ ] Test Numato relay clicks when controlled
- [ ] Verify LEDs light up on GPIO control

---

## Component Inventory

Verify all components before starting assembly:

### Compute Stack
- [ ] Raspberry Pi 5 8GB (coated)
- [ ] Witty Pi 5 HAT+ (coated)
- [ ] Pi-EzConnect HAT (coated)
- [ ] M.2 SSD 512GB in USB enclosure
- [ ] MicroSD card 32GB (with OS)
- [ ] Heatsink/cooler for Pi 5

### Connectivity
- [ ] Quectel EG25-G modem + PU201 USB adapter
- [ ] LTE antennas (×2)
- [ ] SMA bulkhead connectors (×2)
- [ ] USB-RS485 adapter

### Camera System
- [ ] 8MP IMX179 NoIR USB camera
- [ ] VA Imaging MVEC167 aluminum housing
- [ ] Gore M12 vent
- [ ] Bulgin PX0840 USB cable (or outdoor USB cable)

### IR Illumination
- [ ] Tendelux AI4 850nm IR light
- [ ] Numato USB relay module (coated)
- [ ] 12V power cable with terminals
- [ ] Inline fuse holder + 5A fuse

### User Interface
- [ ] IP67 LEDs: Red, Yellow, Green
- [ ] IP67 momentary pushbutton
- [ ] Current-limiting resistors (330Ω)

### Enclosure & Mounting
- [ ] Outdoor enclosure (~300×200×150mm)
- [ ] DIN rail 35mm (×1-2)
- [ ] DIN rail clips for Pi
- [ ] Terminal blocks
- [ ] Cable glands (M12, M16, M20)
- [ ] Gore M12 vents (×2 for enclosure)

### Rain Gauge
- [ ] DFRobot SEN0575 tipping bucket
- [ ] Mounting bracket
- [ ] 2-conductor cable (5m)

### Hardware & Consumables
- [ ] Stainless steel hardware kit
- [ ] Cable ties (UV-resistant)
- [ ] Dielectric grease
- [ ] Silicone sealant

---

## Assembly Steps

### Step 1: Prepare Enclosure (30 min)

**Tools needed:** Drill, step bit or hole saw, marker

1. **Mark hole positions:**
   - 2× M12 holes for Gore vents (opposite sides for airflow)
   - 2× M12 holes for SMA antenna bulkheads
   - 1× M16 hole for USB camera cable
   - 1× M12 hole for 12V power input
   - 3× 10mm holes for status LEDs
   - 1× 16mm hole for pushbutton
   - 1× PG9 hole for rain gauge cable

2. **Drill holes:**
   - Use step bit for clean cuts in plastic/metal
   - Deburr all holes
   - Test-fit cable glands and LEDs

3. **Install Gore vents:**
   - Thread M12 vents into holes
   - Hand-tight plus 1/4 turn (do not overtighten)
   - Vents should be on opposite sides for air circulation

4. **Install DIN rail:**
   - Cut to fit enclosure width
   - Mount horizontally using provided screws
   - Leave clearance for cable routing below

### Step 2: Assemble Compute Stack (15 min)

**Tools needed:** Phillips screwdriver

1. **Stack order (bottom to top):**
   ```
   [Raspberry Pi 5]
        ↑
   [Witty Pi 5 HAT+]
        ↑
   [Pi-EzConnect HAT]
   ```

2. **Assembly:**
   - Install heatsink on Pi 5 CPU (thermal pad contact)
   - Align Witty Pi 5 HAT+ GPIO header with Pi 5 header
   - Press down firmly until fully seated
   - Secure with standoffs if provided
   - Align Pi-EzConnect on top of Witty Pi 5
   - Press down firmly
   - Secure entire stack with long standoffs

3. **Verify:**
   - All headers fully seated
   - No bent pins
   - Heatsink secure

### Step 3: Mount Components on DIN Rail (20 min)

**Tools needed:** Screwdriver, DIN rail clips

1. **Mount Pi stack:**
   - Attach DIN rail clip to Pi mounting holes
   - Snap onto DIN rail
   - Verify secure fit

2. **Mount other components:**
   - Numato relay module (use clip or Velcro)
   - Terminal blocks (snap onto rail)
   - Fuse holder (snap onto rail or screw mount)

3. **Mount items without DIN holes:**
   - SSD enclosure: Use Velcro/Dual-Lock on enclosure floor
   - Quectel modem: Use Velcro/Dual-Lock

4. **Layout:**
   ```
   ┌─────────────────────────────────────────┐
   │  [Gore Vent]              [Gore Vent]   │
   │                                         │
   │  ┌──────────────────────────────────┐   │
   │  │         DIN RAIL                 │   │
   │  │ [Pi Stack] [Relay] [Fuse] [Term] │   │
   │  └──────────────────────────────────┘   │
   │                                         │
   │  [SSD]     [Modem]                      │
   │  (velcro)  (velcro)                     │
   │                                         │
   │  ○ ○ ○  [●]                             │
   │  LEDs   Button                          │
   └─────────────────────────────────────────┘
   ```

### Step 4: Install User Interface (15 min)

**Tools needed:** Screwdriver, wire strippers

1. **Install LEDs:**
   - Insert LEDs into 10mm panel holes
   - Secure with provided nuts (inside)
   - Order: Red (error) | Yellow (working) | Green (OK)

2. **Install pushbutton:**
   - Insert into 16mm hole
   - Secure with nut from inside
   - Should be slightly recessed to prevent accidental press

3. **Wire LEDs to Pi-EzConnect:**
   ```
   LED Wiring (common cathode):

   GPIO Pin → 330Ω resistor → LED anode (+)
   LED cathode (-) → GND terminal

   Suggested GPIO assignments:
   - Green LED: GPIO 17
   - Yellow LED: GPIO 27
   - Red LED: GPIO 22
   ```

4. **Wire pushbutton:**
   ```
   Pushbutton Wiring:

   GPIO Pin (with internal pull-up) ← Button terminal 1
   GND terminal ← Button terminal 2

   Suggested: GPIO 23 (active low)
   ```

5. **Use Pi-EzConnect screw terminals:**
   - Strip wire ends 5-6mm
   - Insert into terminal
   - Tighten screw firmly
   - Tug to verify secure

### Step 5: Wire Power Distribution (20 min)

**Tools needed:** Wire strippers, screwdriver

1. **12V Input from solar controller:**
   - Run 18AWG wire from solar controller 12V output
   - Through M12 cable gland into enclosure
   - To input terminal block

2. **Power distribution:**
   ```
   Solar 12V ──┬── Inline Fuse (5A) ── Relay ── IR Light
               │
               └── USB-C converter ── Pi 5 (via Witty Pi)

   Note: Witty Pi 5 can accept 5-26V input.
   Use 12V→5V USB-C adapter OR power Witty Pi directly at 12V.
   ```

3. **Terminal block connections:**
   - Use ferrules on all stranded wire ends
   - Label all terminals (12V+, 12V-, GND, etc.)

### Step 6: Wire IR Control Circuit (15 min)

**Tools needed:** Screwdriver

1. **Circuit overview:**
   ```
   Pi USB Port ──► Numato Relay ──┐
                                  │ (relay contacts)
   Solar 12V ── Fuse ─────────────┴──► Tendelux AI4
   ```

2. **Connections:**
   - Numato relay USB cable → Pi 5 USB-A port
   - 12V+ from terminal block → fuse holder input
   - Fuse holder output → relay NO (normally open) terminal
   - Relay COM (common) terminal → Tendelux 12V+
   - Tendelux 12V- → terminal block GND

3. **Operation:**
   - When Pi boots, systemd service activates relay
   - Relay closes, providing 12V to Tendelux
   - Tendelux photocell controls actual illumination (only at night)
   - When Pi shuts down, relay opens, IR light unpowered

### Step 7: Connect Peripherals (15 min)

1. **SSD:**
   - USB-A cable from SSD enclosure → Pi 5 USB 3.0 port (blue)

2. **LTE Modem:**
   - USB cable from PU201 → Pi 5 USB 2.0 port
   - SMA cables from modem → bulkhead connectors
   - External antennas on bulkheads

3. **USB Camera:**
   - Bulgin USB cable through M16 gland
   - Connect to Pi 5 USB port

4. **Rain Gauge:**
   - I2C cable through PG9 gland
   - Connect to Pi-EzConnect I2C terminals:
     - VCC → 3.3V
     - GND → GND
     - SDA → GPIO 2 (SDA)
     - SCL → GPIO 3 (SCL)

5. **Verify all connections before powering on.**

### Step 8: Assemble Camera Housing (20 min)

**Tools needed:** Screwdriver, silicone sealant

1. **Prepare housing:**
   - Install Gore M12 vent in housing vent port
   - Clean all sealing surfaces

2. **Install camera:**
   - Mount USB camera board inside housing
   - Align lens with window
   - Secure with provided hardware

3. **Connect USB cable:**
   - Route Bulgin cable through housing cable entry
   - Connect to camera board
   - Seal cable entry with provided gland/seal

4. **Close housing:**
   - Verify O-ring/gasket is clean and seated
   - Close housing, secure all screws
   - Apply thin bead of silicone around seam (optional extra protection)

5. **Test:**
   - Connect to Pi, verify camera captures image
   - Check focus through housing window

### Step 9: Mount External Components (30 min)

**Tools needed:** Adjustable wrench, stainless U-bolts

1. **Camera mounting:**
   - Select pole/mounting location with clear river view
   - Use stainless U-bolts to secure housing bracket
   - Aim camera at target water area
   - Secure USB cable along pole with UV-resistant cable ties

2. **IR light mounting:**
   - Mount Tendelux AI4 adjacent to camera
   - Aim to illuminate same area as camera view
   - Secure 12V cable alongside USB cable

3. **Rain gauge mounting:**
   - Mount on separate arm, away from obstructions
   - Level the gauge (critical for accuracy)
   - Route cable to enclosure

4. **Antenna mounting:**
   - Mount LTE antennas on enclosure exterior
   - Position vertically for best reception
   - Apply dielectric grease to SMA connections

### Step 10: Final Assembly & Sealing (15 min)

1. **Cable management:**
   - Route all internal cables neatly
   - Use cable ties to bundle
   - Ensure no cables block Gore vents

2. **Seal cable glands:**
   - Tighten all glands firmly
   - Apply thin silicone bead around each gland exterior

3. **Final checks:**
   - [ ] All connections secure
   - [ ] Gore vents unobstructed
   - [ ] LEDs visible from outside
   - [ ] Button accessible
   - [ ] No loose items inside

4. **Close enclosure:**
   - Verify gasket is clean and seated
   - Close lid, secure all latches/screws

---

## Power-On Procedure

### First Boot

1. **Verify solar battery voltage:** Should be >12V
2. **Connect 12V input** to enclosure
3. **Observe:**
   - Witty Pi LED should light
   - Pi 5 should boot (activity LED flashing)
   - Status LEDs should indicate boot sequence

4. **Wait 2-3 minutes** for full boot

5. **Check status LEDs:**
   - Green steady = OK
   - Yellow blinking = working (capture/upload)
   - Red = error (check logs)

### Verify Camera

1. Enter maintenance mode (long press button)
2. Connect to WiFi hotspot
3. SSH into Pi
4. Run: `ls /dev/video*` - should show camera device
5. Run test capture: `ffmpeg -f v4l2 -i /dev/video0 -frames:v 1 test.jpg`
6. Verify image captured

### Verify IR Light

1. Cover Tendelux photocell with hand (simulate darkness)
2. IR light should illuminate
3. Verify camera captures IR-lit scene
4. Uncover photocell, IR should turn off

### Verify LTE Connection

1. Check modem detected: `mmcli -L`
2. Check signal: `mmcli -m 0 --signal-get`
3. Test data: `ping -c 3 8.8.8.8`

### Verify Rain Gauge

1. Run I2C scan: `i2cdetect -y 1`
2. Should show device at expected address
3. Manually tip bucket, verify count increments

---

## Troubleshooting

See `TROUBLESHOOTING.md` for detailed diagnostics.

**Quick Checks:**

| Symptom | Check |
|---------|-------|
| No boot | Battery voltage, fuses, USB-C power |
| No camera | USB cable, `lsusb` output |
| No IR | Relay clicking? Cover photocell. Check fuse. |
| No LTE | Antennas tight? SIM inserted? IMEI registered? |
| No rain data | I2C address? Cable connections? |

---

## Maintenance Notes

### Monthly
- Visual inspection of enclosure seals
- Check antenna connections
- Verify status LEDs functioning

### Quarterly
- Clean camera lens (through housing if sealed)
- Check cable gland tightness
- Verify rain gauge not clogged

### Annually
- Inspect conformal coating on PCBs
- Check battery health (solar system)
- Replace any degraded cable ties

---

## Site-Specific Configuration

**Record after installation:**

| Parameter | Value |
|-----------|-------|
| Pi hostname | |
| Pi IP (if static) | |
| WiFi hotspot SSID | |
| WiFi hotspot password | |
| LTE SIM number | |
| Modem IMEI | |
| Camera device path | |
| GPS coordinates | |
| Installation date | |
| Installer name | |

---

**Document Version:** 1.0
**Last Updated:** January 9, 2026
