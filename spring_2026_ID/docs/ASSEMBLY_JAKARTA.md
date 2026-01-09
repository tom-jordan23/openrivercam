# Assembly Guide - Jakarta Site

**Site:** Jakarta, Indonesia (coastal/urban)
**Type:** AC-powered with 24hr UPS, 2× PoE cameras
**Purpose:** New training/demo installation

---

## Pre-Assembly Checklist

Complete these steps BEFORE traveling to Indonesia:

### 1. Conformal Coating (Low Humidity Environment Required)

Apply MG 422C silicone conformal coating to all PCBs:

**Boards to Coat:**
- [ ] Raspberry Pi 5
- [ ] Witty Pi 5 HAT+
- [ ] Pi-EzConnect terminal block HAT

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
6. Inspect for complete coverage
7. Label each board "COATED" with date

### 2. Camera Pre-Configuration

Configure ANNKE C1200 cameras BEFORE deployment:

- [ ] Power camera via PoE
- [ ] Find camera IP (use ONVIF discovery tool or router)
- [ ] Access web interface (default: admin/admin)
- [ ] Change admin password (record in secure location)
- [ ] Set static IP addresses:
  - Camera 1: 192.168.1.101
  - Camera 2: 192.168.1.102
- [ ] Enable RTSP streaming
- [ ] Note RTSP URLs:
  - `rtsp://admin:password@192.168.1.101:554/stream1`
  - `rtsp://admin:password@192.168.1.102:554/stream2`
- [ ] Test RTSP with VLC on laptop
- [ ] Adjust image settings (exposure, focus) if needed

### 3. Software Configuration

- [ ] Flash OS image to MicroSD card
- [ ] Boot Pi 5 and verify ORC software runs
- [ ] Configure Witty Pi 5 schedule (15-minute wake cycle)
- [ ] Configure for 2-camera RTSP capture
- [ ] Configure WiFi hotspot for maintenance mode
- [ ] Set up LED GPIO control script
- [ ] Pre-configure Telkomsel APN (if known)

### 4. Hardware Testing

- [ ] Test Pi 5 + Witty Pi 5 + Pi-EzConnect stack boots correctly
- [ ] Verify SSD is recognized via USB
- [ ] Test LTE modem connects (with test SIM)
- [ ] Test PoE injector powers both cameras
- [ ] Verify LEDs light up on GPIO control

---

## Component Inventory

### Compute Stack
- [ ] Raspberry Pi 5 8GB (coated)
- [ ] Witty Pi 5 HAT+ (coated)
- [ ] Pi-EzConnect HAT (coated)
- [ ] M.2 SSD 512GB in USB enclosure
- [ ] MicroSD card 32GB (with OS)
- [ ] Active cooler for Pi 5

### Connectivity
- [ ] Quectel EG25-G modem + PU201 USB adapter
- [ ] LTE antennas (×2)
- [ ] SMA bulkhead connectors (×2)
- [ ] USB-RS485 adapter

### Power System
- [ ] Mean Well SDR-120-12 DIN rail PSU
- [ ] Phoenix Contact surge protector
- [ ] LiFePO4 100Ah battery (source locally)
- [ ] 20A LiFePO4 charger (source locally or carry)
- [ ] Victron BatteryProtect 65A
- [ ] Terminal blocks (12-position ×2)
- [ ] Blade fuse holders + fuses (10A, 15A)

### Camera System
- [ ] ANNKE C1200 PoE cameras (×2)
- [ ] Planet IPOE-260-12V PoE injector
- [ ] Cat6 outdoor shielded cable (100m spool)
- [ ] IP68 RJ45 couplers (×2)
- [ ] RJ45 connectors + boots (20+)
- [ ] Camera pole mount brackets (×2)

### Humidity Control
- [ ] PTC heater 10W (×2 for cameras)
- [ ] PTC heater 15W (for enclosure)
- [ ] Gore M12 vents (×3)

### User Interface
- [ ] IP67 LEDs: Red, Yellow, Green
- [ ] IP67 momentary pushbutton
- [ ] Current-limiting resistors (330Ω)

### Enclosure & Mounting
- [ ] IP66 aluminum enclosure (~400×300×200mm)
- [ ] DIN rail 35mm (×2)
- [ ] DIN rail clips
- [ ] Cable glands (M12, M16, M20, M25)

### Grounding (source locally)
- [ ] Copper grounding rod (1.5m)
- [ ] Ground cable 6 AWG (10m)
- [ ] Ground lugs and clamps

### Mounting (source locally)
- [ ] Galvanized pole (4m × 50mm)
- [ ] Pole base flange + anchors
- [ ] U-bolts for enclosure mounting

### Rain Gauge
- [ ] DFRobot SEN0575 tipping bucket
- [ ] Mounting arm
- [ ] Cable (5m)

---

## Assembly Steps

### Step 1: Install Grounding System (1 hour)

**CRITICAL: Complete grounding BEFORE connecting any electronics.**

**Tools needed:** Post driver or hammer, shovel, wrench

1. **Drive ground rod:**
   - Select location near pole base
   - Drive 1.5m copper rod until 15cm remains above ground
   - If rocky soil, may need to angle or use multiple rods

2. **Connect ground cable:**
   - Attach ground lug to rod with clamp
   - Run 6 AWG cable to enclosure location
   - Leave 2m extra for enclosure connection

3. **Test ground:**
   - Measure resistance to earth (<25Ω acceptable)
   - If >25Ω, add second rod 2m away, bond together

### Step 2: Install Mounting Pole (2-3 hours)

**Tools needed:** Shovel, level, concrete mix, wrenches

1. **Dig foundation:**
   - 50cm × 50cm × 60cm deep hole
   - Position for optimal camera view of river

2. **Set pole base:**
   - Install base flange on pole bottom
   - Set pole in hole, verify vertical with level
   - Pour concrete, allow 24 hours cure

3. **Alternative (existing structure):**
   - Use U-bolts to mount to existing pole/structure
   - Ensure mounting is stable and rated for wind

### Step 3: Prepare Enclosure (45 min)

**Tools needed:** Drill, step bit, marker

1. **Mark hole positions:**
   - 3× M12 holes for Gore vents
   - 2× M12 holes for SMA antenna bulkheads
   - 1× M25 hole for AC power entry
   - 2× M20 holes for Cat6 camera cables
   - 1× M16 hole for ground cable
   - 3× 10mm holes for status LEDs
   - 1× 16mm hole for pushbutton
   - 1× PG9 hole for rain gauge cable

2. **Drill holes:**
   - Use step bit for clean cuts
   - Deburr all holes
   - Test-fit all glands

3. **Install Gore vents:**
   - Position for cross-ventilation
   - Hand-tight plus 1/4 turn

4. **Install DIN rails:**
   - Mount 2 rails horizontally
   - Upper rail: PSU, surge protector, terminal blocks
   - Lower rail: Pi stack, PoE injector, BatteryProtect

### Step 4: Install Power System (45 min)

**Tools needed:** Screwdriver, wire strippers, ferrule crimper

**IMPORTANT: Do NOT connect AC power until all wiring is complete.**

1. **Mount power components on upper DIN rail:**
   ```
   ┌──────────────────────────────────────────────────┐
   │ [Surge] ─► [Mean Well PSU] ─► [Terminal Block]  │
   └──────────────────────────────────────────────────┘
   ```

2. **Wire surge protector:**
   - AC input through M25 gland
   - L (line) → Surge protector input
   - N (neutral) → Surge protector input
   - PE (earth) → Ground terminal → Ground cable

3. **Wire Mean Well SDR-120-12:**
   - AC input from surge protector output
   - 12V output to terminal block
   - Verify input voltage selector (if any) set for 220V

4. **Wire battery system:**
   ```
   Mean Well 12V+ ──┬──► Charger input (+)
                    │
                    └──► Terminal block (system 12V+)

   Charger output ──► Battery (+)
   Battery (-) ──► BatteryProtect IN (-)
   BatteryProtect OUT (-) ──► Terminal block (system GND)
   Battery (+) ──► BatteryProtect IN (+)
   BatteryProtect OUT (+) ──► Terminal block (battery 12V+)
   ```

5. **Battery protection wiring:**
   ```
   ┌─────────────────────────────────────────────────────────┐
   │                                                         │
   │  [Mean Well PSU]                                        │
   │       │ 12V                                             │
   │       ▼                                                 │
   │  [Charger] ──► [LiFePO4 100Ah] ──► [BatteryProtect]    │
   │                                          │              │
   │                                          ▼              │
   │                              [Terminal Block 12V]       │
   │                                          │              │
   │              ┌───────────────────────────┤              │
   │              ▼                           ▼              │
   │       [PoE Injector]              [Pi 5 Power]          │
   │                                                         │
   └─────────────────────────────────────────────────────────┘
   ```

6. **Install fuses:**
   - Main 12V feed: 15A fuse
   - PoE injector feed: 10A fuse
   - Pi/accessories feed: 5A fuse

### Step 5: Assemble Compute Stack (15 min)

Same as Sukabumi:

1. **Stack order (bottom to top):**
   ```
   [Raspberry Pi 5]
        ↑
   [Witty Pi 5 HAT+]
        ↑
   [Pi-EzConnect HAT]
   ```

2. Install active cooler on Pi 5
3. Mount stack on lower DIN rail

### Step 6: Install PoE System (30 min)

1. **Mount Planet IPOE-260-12V** on DIN rail

2. **Wire 12V input:**
   - 12V+ from terminal block → PoE injector DC input (+)
   - GND from terminal block → PoE injector DC input (-)

3. **Prepare camera cables:**
   - Measure cable runs to each camera location
   - Add 2m extra for service loops
   - Crimp RJ45 connectors on both ends
   - Test with cable tester

4. **Connect PoE outputs:**
   - PoE Port 1 → Camera 1 cable (through M20 gland)
   - PoE Port 2 → Camera 2 cable (through M20 gland)

5. **Data port:**
   - PoE injector LAN port → Pi 5 Ethernet port
   - Use short patch cable

### Step 7: Install User Interface (15 min)

Same as Sukabumi:

1. Install LEDs in panel holes (Red/Yellow/Green)
2. Install pushbutton
3. Wire to Pi-EzConnect terminals:
   - Green LED: GPIO 17 → 330Ω → LED → GND
   - Yellow LED: GPIO 27 → 330Ω → LED → GND
   - Red LED: GPIO 22 → 330Ω → LED → GND
   - Button: GPIO 23 → Button → GND

### Step 8: Install Humidity Control (20 min)

1. **Enclosure PTC heater:**
   - Mount 15W PTC heater on enclosure interior wall
   - Wire to 12V through thermostat/hygrostat
   - Set to activate when humidity >70% or temp <25°C

2. **Camera PTC heaters:**
   - Install 10W heaters in camera housings (if applicable)
   - Or rely on camera's internal heating
   - ANNKE C1200 is rated for outdoor use

3. **Verify Gore vents clear:**
   - No obstruction
   - Cross-ventilation path available

### Step 9: Connect Peripherals (15 min)

1. **SSD:** USB 3.0 to Pi 5
2. **LTE Modem:** USB to Pi 5, antennas to bulkheads
3. **PoE data:** Ethernet from injector to Pi 5
4. **Rain gauge:** I2C to Pi-EzConnect terminals
5. **USB-RS485:** USB to Pi 5 (for future sensors)

### Step 10: Mount Enclosure on Pole (30 min)

1. **Position enclosure:**
   - Use U-bolts around pole
   - Position for easy access to door
   - Ensure cable glands face downward (drip prevention)

2. **Secure mounting:**
   - Tighten U-bolts evenly
   - Check level
   - Verify stable, no wobble

3. **Route cables:**
   - Camera cables along pole, secured with ties
   - AC power cable (from building) through conduit
   - Ground cable to ground rod

### Step 11: Mount Cameras (45 min)

1. **Install camera brackets** on pole:
   - Camera 1: Upstream view
   - Camera 2: Downstream or different angle
   - Use stainless U-bolts

2. **Mount cameras:**
   - Attach cameras to brackets
   - Connect Cat6 cables (use IP68 couplers at cameras)
   - Aim and focus cameras

3. **Protect connections:**
   - Apply dielectric grease to RJ45 connections
   - Ensure IP68 couplers fully sealed
   - Secure cables with UV-resistant ties

### Step 12: Mount Rain Gauge (20 min)

1. **Install mounting arm** on pole (separate from cameras)
2. **Level the gauge** (critical for accuracy)
3. **Route cable** to enclosure
4. **Connect to Pi-EzConnect:**
   - VCC → 3.3V
   - GND → GND
   - SDA → GPIO 2
   - SCL → GPIO 3

### Step 13: Final Assembly & Testing (30 min)

1. **Cable management:**
   - Bundle and tie all internal cables
   - Ensure no cables block vents or heaters

2. **Seal all glands:**
   - Tighten firmly
   - Apply silicone around exterior

3. **Pre-power checks:**
   - [ ] All connections secure
   - [ ] Ground connected
   - [ ] No loose wires
   - [ ] Gore vents clear
   - [ ] Surge protector installed

4. **Close enclosure** (leave AC disconnected)

---

## Power-On Procedure

### Ground and Surge Protection First

1. Verify ground cable connected to rod and enclosure ground bar
2. Verify surge protector in line with AC input
3. Verify all fuses installed

### Connect AC Power

1. **Connect AC cable** to building power (220V)
2. **Observe Mean Well PSU:**
   - Green LED should light
   - 12V output active

3. **Check battery charger:**
   - Charging indicator should light
   - Battery voltage rising (if depleted)

4. **Check BatteryProtect:**
   - Status LED should indicate connected

### Verify Pi Boot

1. Wait 2-3 minutes for full boot
2. Status LEDs should indicate:
   - Green = OK
   - Yellow blink = working
   - Red = error

### Verify Cameras

1. Enter maintenance mode (long press button)
2. Connect laptop to WiFi hotspot
3. SSH into Pi
4. Ping cameras:
   ```
   ping 192.168.1.101
   ping 192.168.1.102
   ```
5. Test RTSP capture:
   ```
   ffmpeg -i rtsp://admin:pass@192.168.1.101:554/stream1 -frames:v 1 cam1.jpg
   ffmpeg -i rtsp://admin:pass@192.168.1.102:554/stream2 -frames:v 1 cam2.jpg
   ```

### Verify LTE Connection

1. Check modem: `mmcli -L`
2. Check signal: `mmcli -m 0 --signal-get`
3. Test data: `ping -c 3 8.8.8.8`

### Verify Rain Gauge

1. I2C scan: `i2cdetect -y 1`
2. Manually tip bucket, verify count

### Verify UPS Function

1. With system running stable, disconnect AC power
2. System should continue running on battery
3. Monitor battery voltage (should be >12.0V)
4. Reconnect AC after 5-10 minutes test
5. Verify charger resumes

---

## Power Budget Verification

After installation, verify actual power consumption:

| Component | Expected | Measured |
|-----------|----------|----------|
| Pi 5 (idle) | ~5W | |
| Pi 5 (active) | ~8W | |
| PoE cameras (×2) | ~15W | |
| PoE injector | ~5W | |
| Modem (idle) | ~1W | |
| PTC heaters (avg) | ~12W | |
| **Total average** | ~40W | |

**Battery runtime:** 1280Wh ÷ 40W = 32 hours (theoretical)

---

## Troubleshooting

See `TROUBLESHOOTING.md` for detailed diagnostics.

**Quick Checks:**

| Symptom | Check |
|---------|-------|
| No power | AC voltage? Surge protector? PSU LED? |
| No Pi boot | Fuse? 12V at terminals? USB-C power? |
| Cameras offline | PoE injector powered? Cable continuity? Ping test? |
| No LTE | Antennas? SIM? IMEI registered? |
| Battery not charging | Charger LED? Battery terminals? |

---

## Site-Specific Configuration

**Record after installation:**

| Parameter | Value |
|-----------|-------|
| Pi hostname | |
| Pi IP (static) | 192.168.1.100 |
| Camera 1 IP | 192.168.1.101 |
| Camera 2 IP | 192.168.1.102 |
| Camera password | |
| WiFi hotspot SSID | |
| WiFi hotspot password | |
| LTE SIM number | |
| Modem IMEI | |
| Ground resistance | Ω |
| GPS coordinates | |
| AC circuit breaker # | |
| Installation date | |
| Installer name | |

---

**Document Version:** 1.0
**Last Updated:** January 9, 2026
