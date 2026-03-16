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
- [ ] Geekworm G469 terminal block HAT

**Masking (Use Kapton tape):**
- GPIO header pins (all 40 pins)
- J2 power button header (2-pin, near USB-C port)
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

Configure ANNKE C1200 cameras BEFORE deployment. The Pi acts as DHCP server on the camera network using dnsmasq, assigning predictable IPs to each camera.

**Note:** The SADP utility (Hikvision's camera discovery tool) does not run on ARM Macs — neither natively nor under Parallels. The dnsmasq approach below eliminates the need for SADP entirely.

**Note:** The ANNKE web interface requires a Windows-only browser plugin for live view. Use ISAPI snapshot or FTP test upload to verify the camera image instead.

**Set up Pi camera network (one-time):**

1. Set Pi eth0 to a static IP on the camera network:
   ```bash
   sudo nmcli con mod "Wired connection 1" ipv4.addresses 192.168.50.1/24
   sudo nmcli con mod "Wired connection 1" ipv4.method manual
   sudo nmcli con up "Wired connection 1"
   ```

2. Install and configure dnsmasq as DHCP server on eth0:
   ```bash
   sudo apt install dnsmasq
   ```
   Edit `/etc/dnsmasq.conf`:
   ```
   interface=eth0
   bind-interfaces
   dhcp-range=192.168.50.100,192.168.50.200,24h
   dhcp-host=<CAMERA_1_MAC>,192.168.50.101
   dhcp-host=<CAMERA_2_MAC>,192.168.50.102
   ```
   Replace `<CAMERA_x_MAC>` with each camera's MAC address (printed on the camera label). If you don't have the MACs yet, omit the `dhcp-host` lines, let the cameras get any IP from the range, then check `cat /var/lib/misc/dnsmasq.leases` to find their MACs and update the config.

   Restart dnsmasq:
   ```bash
   sudo systemctl restart dnsmasq
   sudo systemctl enable dnsmasq
   ```

**Configure each camera:**

1. Connect camera to PoE switch, connect switch uplink port to Pi Ethernet
2. Wait 60-90 seconds for camera to boot and receive DHCP lease
3. Verify: `ping 192.168.50.101` (or .102)
4. Access web interface at `http://192.168.50.101` (default credentials: admin / admin)
5. Test ISAPI snapshot (works on macOS/Linux without plugins):
   ```bash
   curl --digest -u admin:password http://192.168.50.101/ISAPI/Streaming/channels/101/picture -o cam1_test.jpg
   ```

- [ ] Change admin password (record in secure location)
- [ ] Set camera to DHCP so it picks up the dnsmasq-assigned address on every boot
- [ ] Configure FTP upload to Pi (192.168.50.1) via web interface or camtool.py:
  ```bash
  python3 camtool.py push jakarta-cam1 ftp
  python3 camtool.py push jakarta-cam2 ftp
  ```
- [ ] Test FTP upload: trigger snapshot, verify files arrive in Pi FTP directory
- [ ] Verify both cameras upload correctly:
  - Camera 1 (192.168.50.101) → check FTP directory
  - Camera 2 (192.168.50.102) → check FTP directory
- [ ] Adjust image settings (exposure, focus) if needed

### 3. Software Configuration

- [ ] Flash ORC-OS image to MicroSD card using Raspberry Pi Imager
  - Follow the [ORC-OS README](https://github.com/localdevices/ORC-OS/blob/main/README.md) — section **"Getting the image on the SD card"**
  - Use the `.img.gz` file provided by Rainbow Sensing (do NOT unpack it)
  - In Pi Imager: choose Pi 5 as device, "Use custom" for OS, select the `.img.gz` file
  - When prompted for OS customisation: set hostname (e.g. `orc-jakarta`), keep username as `pi`, enable SSH, skip WiFi (we use Ethernet/LTE)
  - **WARNING:** Do NOT change the username from `pi` — this will break ORC-OS
- [ ] Boot Pi 5 and verify ORC-OS runs
  - Follow the [ORC-OS README](https://github.com/localdevices/ORC-OS/blob/main/README.md) — section **"Test your installation"**
  - First boot takes 2-3 minutes (services compile, filesystem expands, then auto-reboots)
  - After reboot, navigate to `http://<hostname>.local` to verify the ORC-OS web dashboard loads
  - Set the ORC-OS web dashboard password when prompted
- [ ] Install ML-2020 RTC battery in Pi 5
- [ ] Configure for 2-camera FTP capture (Pi FTP server + camera FTP upload config)
- [ ] Configure WiFi hotspot for maintenance mode
- [ ] Set up LED GPIO control script
- [ ] Pre-configure Telkomsel APN (if known)

### 4. Hardware Testing

- [ ] Test Pi 5 + Geekworm G469 stack boots correctly (2-board stack)
- [ ] Verify USB flash drive is recognized
- [ ] Test LTE modem connects (with test SIM)
- [ ] Test PoE switch powers both cameras
- [ ] Verify LEDs light up on GPIO control

---

## Component Inventory

### Compute Stack
- [ ] Raspberry Pi 5 8GB (coated)
- [ ] Geekworm G469 terminal block HAT (coated)
- [ ] SanDisk 256GB USB flash drive
- [ ] MicroSD card 64GB (with OS)
- [ ] Active cooler for Pi 5
- [ ] ML-2020 RTC battery for Pi 5

### Connectivity
- [ ] Quectel EG25-G modem + EXVIST Mini PCIe-USB adapter
- [ ] Proxicast ANT-122-S02 MIMO LTE puck antenna (IP67, 12mm hole mount)

### Power System
- [ ] Mean Well SDR-120-12 DIN rail PSU
- [ ] Heschen HS-40-N 2P surge protector (40kA, 275V)
- [ ] DDR-60G-5 DC-DC buck converter (12V→5V for Pi power)
- [ ] LiFePO4 100Ah battery (source locally)
- [ ] 20A LiFePO4 charger (source locally or carry)
- [ ] Power distribution blocks (12-position, DIN rail)
- [ ] Blade fuse holders + fuses (5A, 10A, 15A)

### Camera System
- [ ] ANNKE C1200 PoE cameras (×2, factory-sealed IP67)
- [ ] LINOVISION Industrial PoE Switch (Gigabit, 12V DC input)
- [ ] Electronics-Salon 4-channel SPDT DIN Rail relay module (GPIO-triggered via G469)
- [ ] Cat6 outdoor shielded cables, 10ft pre-terminated (×4)
- [ ] CNLINKO weatherproof ethernet bulkheads, IP67 (×2)
- [ ] Camera pole mount brackets (×2)

### Humidity Control & Climate Monitoring
- [ ] PTC heater 15W (for enclosure)
- [ ] SHT40 temperature/humidity sensor (I2C, inside enclosure)
- [ ] DS18B20 waterproof temperature probe (1-Wire, outside enclosure)
- [ ] Amphenol Gore vents, IP68 (×2)
- [ ] 40 CFM fans (×2, for internal air circulation)

### User Interface
- [ ] 12V IP67 panel-mount LEDs: Red, Yellow, Green
- [ ] IP67 momentary pushbutton (maintenance mode, GPIO 23)
- [ ] IP67 momentary pushbutton (external power button, Pi 5 J2 header)

### Enclosure & Mounting
- [ ] VEVOR NEMA 4x enclosure (16"×12"×8")
- [ ] DIN rail 35mm (×2)
- [ ] DIN rail clips
- [ ] CNLINKO weatherproof ethernet bulkheads (×2, for cameras)
- [ ] SP13 weatherproof DC power bulkheads (IP68, for AC input)
- [ ] Neoprene rubber (galvanic isolation for mounting)

### Grounding (source locally)
- [ ] Copper grounding rod (1.5m)
- [ ] Ground cable 6 AWG (10m)
- [ ] Ground lugs and clamps

### Mounting (source locally)
- [ ] Galvanized pole (4m × 50mm)
- [ ] Pole base flange + anchors
- [ ] U-bolts for enclosure mounting

### Rain Gauge
- [ ] Hydreon RG-15 optical rain gauge (UART RS232 TTL 3.3V)
- [ ] Built-in mounting holes (no separate bracket needed)
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
   - 2× M12 holes for Gore vents
   - 1× 12mm hole for Proxicast puck antenna (enclosure top)
   - 2× holes for CNLINKO ethernet bulkheads (camera cables)
   - 1× hole for SP13 DC power bulkhead (AC input)
   - 1× M16 hole for ground cable
   - 2× holes for 40 CFM fans
   - 3× 10mm holes for status LEDs
   - 1× 16mm hole for maintenance pushbutton
   - 1× 16mm hole for external power button
   - 1× PG9 hole for rain gauge cable
   - 1× PG9 hole for DS18B20 temperature probe

2. **Drill holes:**
   - Use step bit for clean cuts
   - Deburr all holes
   - Test-fit all bulkheads, glands, and vents

3. **Install Gore vents:**
   - Position for cross-ventilation
   - Hand-tight plus 1/4 turn

4. **Install DIN rails:**
   - Mount 2 rails horizontally
   - Upper rail: PSU, surge protector, terminal block, fuse holders
   - Lower rail: Pi stack, PoE switch, relay module, DDR-60G-5

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
   - AC input through SP13 DC power bulkhead
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
                     └──► Terminal block TB1 (system 12V+)

   Charger output ──► Battery (+)
   Battery (+) ──► Terminal block TB1 (backup 12V+)
   Battery (-) ──► Terminal block TB1 (system GND)
   ```
   Battery BMS handles low-voltage cutoff automatically.

5. **Install DDR-60G-5 buck converter on lower DIN rail:**
   ```
   TB1 12V+ ──[FUSE 5A]──► DDR-60G-5 input (+)
   TB1 GND ──► DDR-60G-5 input (-)
   DDR-60G-5 output (5V) ──► hardwired 5V/GND ──► Pi 5 GPIO pins
   ```

6. **Install fuses:**
   - Main 12V feed: 15A fuse
   - PoE relay/switch feed: 10A fuse
   - Pi/DDR-60G-5 feed: 5A fuse
   - Heater/fan feed: 5A fuse

### Step 5: Assemble Compute Stack (15 min)

1. **Stack order (bottom to top):**
   ```
   [Raspberry Pi 5]
        ↑
   [Geekworm G469 HAT]
   ```
   2-board stack. Pi 5 built-in RTC with ML-2020 battery provides timekeeping.

2. Install active cooler on Pi 5
3. Install ML-2020 RTC battery
4. Mount stack on lower DIN rail using DIN rail clip

### Step 6: Install PoE System (30 min)

1. **Mount LINOVISION PoE Switch** on lower DIN rail

2. **Mount Electronics-Salon relay module** on lower DIN rail

3. **Wire relay module (via Geekworm G469 terminals):**
   - Relay VCC → 5V from G469
   - Relay GND → GND from G469
   - GPIO 24 → IN1 (PoE switch power)
   - GPIO 17 → IN2 (Green LED)
   - GPIO 27 → IN3 (Yellow LED)
   - GPIO 22 → IN4 (Red LED)
   - 12V+ from TB1 → relay CH1 NO (normally open) input
   - Relay CH1 COM output → LINOVISION PoE switch 12V+ input
   - TB1 GND → PoE switch GND input

4. **Connect Ethernet cables:**
   - Short patch cable: PoE switch uplink port → Pi 5 Ethernet
   - PoE Port 1 → CNLINKO bulkhead 1 → Cat6 10ft cable → Camera 1
   - PoE Port 2 → CNLINKO bulkhead 2 → Cat6 10ft cable → Camera 2

5. **Install CNLINKO ethernet bulkheads:**
   - Mount in pre-drilled enclosure holes
   - Connect internal Cat6 patch cables to PoE switch ports
   - External Cat6 cables connect to cameras

### Step 7: Install User Interface (15 min)

1. Install 12V panel-mount LEDs in panel holes (Red/Yellow/Green)
2. Install maintenance pushbutton
3. Install external power button
4. Wire LEDs through relay channels (12V switched by relay):
   - Green LED: 12V from TB1 → relay CH2 COM → LED → GND (GPIO 17 → IN2)
   - Yellow LED: 12V from TB1 → relay CH3 COM → LED → GND (GPIO 27 → IN3)
   - Red LED: 12V from TB1 → relay CH4 COM → LED → GND (GPIO 22 → IN4)
5. Wire maintenance pushbutton to Geekworm G469 terminals:
   - Button: GPIO 23 → Button → GND
6. Wire external power button to Pi 5 J2 header:
   - J2 is a dedicated 2-pin power button header on the Pi 5, located near the USB-C port
   - This is NOT a GPIO pin — it is hardware-level power control
   - Connect two wires (22 AWG) from J2 pin 1 and J2 pin 2 to the IP67 momentary switch
   - Polarity does not matter (momentary short between the two pins)
   - Behavior: brief press powers on (from halted), brief press initiates clean shutdown (while running), ~10s hold forces power off (if frozen)

### Step 8: Install Humidity Control & Climate Monitoring (20 min)

1. **Enclosure PTC heater:**
   - Mount 15W PTC heater on enclosure interior wall
   - Wire to 12V through thermostat/hygrostat
   - Set to activate when humidity >70% or temp <25°C

2. **Install 40 CFM fans:**
   - Mount fans in pre-drilled enclosure holes
   - Wire to 12V from TB1 (through heater/fan fuse)
   - Fans run whenever system is powered

3. **Install SHT40 temperature/humidity sensor:**
   - Mount inside enclosure
   - Connect STEMMA QT to bare wire cable to Geekworm G469:
     - VCC → 3.3V
     - GND → GND
     - SDA → GPIO 2
     - SCL → GPIO 3

4. **Install DS18B20 waterproof temperature probe:**
   - Route probe cable through PG9 gland to outside enclosure
   - Connect to Geekworm G469:
     - Data → GPIO 4 / Pin 7 (with 4.7kΩ pull-up to 3.3V)
     - VCC → 3.3V
     - GND → GND

5. **Verify Gore vents clear:**
   - No obstruction
   - Cross-ventilation path available

### Step 9: Connect Peripherals (15 min)

1. **USB flash drive:** SanDisk 256GB directly into Pi 5 USB-A 3.0 port
2. **LTE Modem:** USB to Pi 5, SMA pigtails to puck antenna
3. **Puck antenna:** Mount Proxicast ANT-122-S02 in 12mm hole on enclosure top
4. **PoE data:** Ethernet from PoE switch uplink to Pi 5 (already done in Step 6)
5. **Rain gauge:** UART cable through PG9 gland to Geekworm G469 terminals:
   - VCC → 12V (from TB1)
   - GND → GND (TB1)
   - TX → GPIO 15 (Pi RX)
   - RX → GPIO 14 (Pi TX)
6. **Relay GPIO:** Already wired in Step 6 (VCC, GND, IN1-IN4 from G469)

### Step 10: Mount Enclosure on Pole (30 min)

1. **Position enclosure:**
   - Use U-bolts around pole
   - Position for easy access to door
   - Ensure cable glands face downward (drip prevention)
   - Place neoprene rubber between enclosure and pole (galvanic isolation)

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
   - Connect Cat6 cables to CNLINKO bulkhead exterior connectors
   - Aim and focus cameras

3. **Protect connections:**
   - CNLINKO bulkheads provide IP67 weatherproofing
   - Secure cables with UV-resistant ties

### Step 12: Mount Rain Gauge (20 min)

1. **Mount Hydreon RG-15** on pole (separate from cameras)
   - Built-in mounting holes, no separate bracket needed
2. **Level the gauge** (critical for accuracy)
3. **Route cable** to enclosure through PG9 gland
4. **Connect to Geekworm G469:**
   - VCC → 12V (TB1)
   - GND → GND (TB1)
   - TX → GPIO 15 (Pi RX)
   - RX → GPIO 14 (Pi TX)

### Step 13: Final Assembly & Testing (30 min)

1. **Cable management:**
   - Bundle and tie all internal cables
   - Ensure no cables block vents, fans, or heaters

2. **Seal all bulkheads and glands:**
   - Tighten firmly
   - Apply silicone around exterior

3. **Pre-power checks:**
   - [ ] All connections secure
   - [ ] Ground connected
   - [ ] No loose wires
   - [ ] Gore vents clear
   - [ ] Surge protector installed
   - [ ] Fans unobstructed
   - [ ] External power button wired to Pi 5 J2 header

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

### Power On Pi

1. **Press the external power button** (brief press) to power on the Pi 5
   - The Pi does not auto-power-on from 5V alone — the J2 power button (or software config) is required
   - If the Pi was previously shut down cleanly, a brief press on the external power button will boot it
2. Wait 2-3 minutes for full boot
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
   ping 192.168.50.101
   ping 192.168.50.102
   ```
5. Test FTP upload from both cameras:
   - Trigger snapshot from camera web interface or ISAPI
   - Check Pi FTP upload directory for files from each camera
   - Verify image quality is acceptable

### Verify LTE Connection

1. Check modem: `mmcli -L`
2. Check signal: `mmcli -m 0 --signal-get`
3. Test data: `ping -c 3 8.8.8.8`

### Verify Rain Gauge

1. Check UART device: `ls /dev/ttyAMA0` or `ls /dev/serial0`
2. Test serial communication: `cat /dev/ttyAMA0` (tip bucket, check for data)
3. Manually tip bucket, verify data received

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
| PoE switch | ~5W | |
| Modem (idle) | ~1W | |
| PTC heater (avg) | ~8W | |
| Fans (×2) | ~3W | |
| **Total average** | ~40W | |

**Battery runtime:** 1280Wh ÷ 40W = 32 hours (theoretical)

---

## Troubleshooting

See `TROUBLESHOOTING.md` for detailed diagnostics.

**Quick Checks:**

| Symptom | Check |
|---------|-------|
| No power | AC voltage? Surge protector? PSU LED? |
| No Pi boot | Fuse? 12V at terminals? DDR-60G-5 output? 5V at GPIO pins? Power button pressed? J2 wiring? |
| Cameras offline | PoE switch powered? Relay GPIO wiring correct? Cable continuity? Ping test? |
| No LTE | Antenna? SIM? IMEI registered? |
| Battery not charging | Charger LED? Battery terminals? |

---

## Site-Specific Configuration

**Record after installation:**

| Parameter | Value |
|-----------|-------|
| Pi hostname | |
| Pi IP (static) | 192.168.50.1 |
| Camera 1 IP | 192.168.50.101 |
| Camera 2 IP | 192.168.50.102 |
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

**Document Version:** 2.0
**Last Updated:** March 9, 2026
**Changes from v1.0:**
- Removed Witty Pi 5 HAT+ (Pi 5 built-in RTC sufficient)
- Renamed Pi-EzConnect → Geekworm G469
- Replaced M.2 SSD with SanDisk 256GB USB flash drive
- Replaced Planet IPOE-260-12V with LINOVISION PoE Switch + relay
- Replaced Phoenix Contact surge protector with Heschen HS-40-N 2P
- Removed Victron BatteryProtect (BMS built-in cutoff)
- Added DDR-60G-5 buck converter for Pi power
- Replaced DFRobot SEN0575 I2C rain gauge with Hydreon RG-15 UART
- Added SHT40 and DS18B20 climate sensors
- Replaced SMA bulkheads with Proxicast puck antenna
- Replaced cable glands with CNLINKO/SP13 weatherproof bulkheads
- Removed camera PTC heaters, added fans
- Added neoprene rubber for galvanic isolation
