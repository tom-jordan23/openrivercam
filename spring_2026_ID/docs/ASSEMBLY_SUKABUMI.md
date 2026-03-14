# Assembly Guide - Sukabumi Site

**Site:** Sukabumi, Indonesia (foothills)
**Type:** Solar-powered, PoE camera with built-in IR (power-cycled with Pi)
**Purpose:** Replacement of failed river monitoring unit

---

## Pre-Assembly Checklist

Complete these steps BEFORE traveling to Indonesia:

### 1. Conformal Coating (Low Humidity Environment Required)

Apply MG 422C silicone conformal coating to all PCBs:

**Boards to Coat:**
- [ ] Raspberry Pi 5
- [ ] Geekworm G469 terminal block HAT

**Note:** No relay module needed - PoE camera has built-in IR.

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

- [ ] Flash ORC-OS image to MicroSD card using Raspberry Pi Imager
  - Follow the [ORC-OS README](https://github.com/localdevices/ORC-OS/blob/main/README.md) — section **"Getting the image on the SD card"**
  - Use the `.img.gz` file provided by Rainbow Sensing (do NOT unpack it)
  - In Pi Imager: choose Pi 5 as device, "Use custom" for OS, select the `.img.gz` file
  - When prompted for OS customisation: set hostname (e.g. `orc-sukabumi`), keep username as `pi`, enable SSH, skip WiFi (we use Ethernet/LTE)
  - **WARNING:** Do NOT change the username from `pi` — this will break ORC-OS
- [ ] Boot Pi 5 and verify ORC-OS runs
  - Follow the [ORC-OS README](https://github.com/localdevices/ORC-OS/blob/main/README.md) — section **"Test your installation"**
  - First boot takes 2-3 minutes (services compile, filesystem expands, then auto-reboots)
  - After reboot, navigate to `http://<hostname>.local` to verify the ORC-OS web dashboard loads
  - Set the ORC-OS web dashboard password when prompted
- [ ] Configure Pi 5 RTC wake schedule (15-minute wake cycle via ML-2020 coin cell)
- [ ] Test PoE camera FTP upload to Pi
- [ ] Configure WiFi hotspot for maintenance mode
- [ ] Set up LED relay control script (GPIO 17/27/22 → relay channels → 12V LEDs)
- [ ] Pre-configure Telkomsel APN (if known)
- [ ] Configure Pi eth0 static IP (192.168.50.1/24) and dnsmasq DHCP for camera network
- [ ] Configure camera FTP upload settings via web interface or camtool.py

### 3. Hardware Testing

- [ ] Test Pi 5 + Geekworm G469 stack boots correctly (2-board stack)
- [ ] Verify USB flash drive is recognized
- [ ] Test LTE modem connects (with test SIM)
- [ ] Test PoE camera FTP upload works
- [ ] Test PoE switch powers camera when relay energized
- [ ] Verify LEDs light up via relay channels (GPIO 17/27/22)

---

## Component Inventory

Verify all components before starting assembly:

### Compute Stack
- [ ] Raspberry Pi 5 8GB (coated)
- [ ] Geekworm G469 HAT (coated)
- [ ] SanDisk 256GB USB flash drive
- [ ] MicroSD card 64GB (with OS)
- [ ] Heatsink/cooler for Pi 5
- [ ] ML-2020 RTC battery for Pi 5

### Connectivity
- [ ] Quectel EG25-G modem + EXVIST Mini PCIe-USB adapter
- [ ] Proxicast ANT-122-S02 MIMO LTE puck antenna (IP67, 12mm hole mount)

### PoE Camera System
- [ ] ANNKE C1200 PoE camera (12MP, built-in IR, factory-sealed IP67)
- [ ] LINOVISION Industrial PoE Switch (Gigabit, 12V DC input)
- [ ] Electronics-Salon 4-channel SPDT DIN Rail relay module (GPIO-triggered via G469)
- [ ] DDR-60G-5 DC-DC converter (12V→5V for Pi 5 via USB-C)
- [ ] DDR-60G-12 DC-DC converter (12V→12V regulated for PoE switch)
- [ ] Cat6 outdoor shielded cable (to camera)
- [ ] CNLINKO weatherproof ethernet bulkhead, IP67 (enclosure feedthrough)
- [ ] Pole mount bracket (stainless steel)

### Climate Monitoring
- [ ] SHT40 temperature/humidity sensor (I2C, inside enclosure)
- [ ] DS18B20 waterproof temperature probe (1-Wire, outside enclosure)

### User Interface
- [ ] 12V IP67 panel-mount LEDs: Red, Yellow, Green
- [ ] IP67 momentary pushbutton (maintenance, 16mm panel mount)
- [ ] IP67 momentary pushbutton (power, 16mm panel mount — wired to Pi 5 J2 header)

### Enclosure & Mounting
- [ ] Outdoor enclosure (~300×200×150mm)
- [ ] DIN rail 35mm (×1-2)
- [ ] DIN rail clips for Pi
- [ ] Terminal blocks
- [ ] SP13 weatherproof DC power bulkhead (IP68, for 12V input)
- [ ] CNLINKO weatherproof ethernet bulkhead (IP67, for PoE camera)
- [ ] Gore M12 vents (×2 for enclosure)

### Rain Gauge
- [ ] Hydreon RG-15 optical rain gauge (UART RS232 TTL 3.3V)
- [ ] Built-in mounting holes (no separate bracket needed)
- [ ] Cable (5m)

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
   - 1× 12mm hole for Proxicast puck antenna (enclosure top)
   - 1× hole for CNLINKO ethernet bulkhead (PoE camera)
   - 1× hole for SP13 DC power bulkhead (12V input)
   - 3× 10mm holes for status LEDs
   - 2× 16mm holes for pushbuttons (maintenance + power)
   - 1× PG9 hole for rain gauge cable
   - 1× PG9 hole for DS18B20 temperature probe

2. **Drill holes:**
   - Use step bit for clean cuts in plastic/metal
   - Deburr all holes
   - Test-fit bulkheads, glands, and LEDs

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
   [Geekworm G469 HAT]
   ```

2. **Assembly:**
   - Install heatsink on Pi 5 CPU (thermal pad contact)
   - Install ML-2020 RTC coin cell in Pi 5 (for built-in RTC scheduling)
   - Align Geekworm G469 GPIO header with Pi 5 header
   - Press down firmly until fully seated
   - Secure stack with standoffs

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

2. **Mount DIN rail components:**
   - LINOVISION PoE switch
   - Electronics-Salon relay module
   - DDR-60G-5 buck converter (12V→5V)
   - DDR-60G-12 buck converter (12V→12V regulated)
   - Terminal blocks (snap onto rail)
   - Fuse holder (snap onto rail or screw mount)

3. **Mount items without DIN holes:**
   - Quectel modem: Use Velcro/Dual-Lock

4. **Layout:**
   ```
   ┌─────────────────────────────────────────┐
   │  [Gore Vent]              [Gore Vent]   │
   │              [Puck Antenna]             │
   │                                         │
   │  ┌──────────────────────────────────┐   │
   │  │         DIN RAIL                 │   │
   │  │ [Pi Stack] [PoE Sw] [Relay]      │   │
   │  │ [DDR-5] [DDR-12] [Fuse] [Term]  │   │
   │  └──────────────────────────────────┘   │
   │                                         │
   │  [Modem]                                │
   │  (velcro)                               │
   │                                         │
   │  ○ ○ ○  [●] [●]                          │
   │  LEDs   Mnt  Pwr                        │
   └─────────────────────────────────────────┘
   ```

### Step 4: Install User Interface (15 min)

**Tools needed:** Screwdriver, wire strippers

1. **Install LEDs:**
   - Insert LEDs into 10mm panel holes
   - Secure with provided nuts (inside)
   - Order: Red (error) | Yellow (working) | Green (OK)

2. **Install maintenance pushbutton:**
   - Insert into 16mm hole
   - Secure with nut from inside
   - Should be slightly recessed to prevent accidental press

3. **Install power pushbutton:**
   - Insert into second 16mm hole
   - Secure with nut from inside
   - Label clearly as "POWER" to distinguish from maintenance button

4. **Wire LEDs through relay channels:**
   ```
   LED Wiring (12V panel-mount LEDs switched by relay):

   Each LED is powered by 12V from TB1, switched through a relay channel:
   12V (TB1) → Relay COM → Relay NO → LED anode (+)
   LED cathode (-) → GND (TB1)

   Relay channel assignments (GPIO-triggered via G469):
   - Green LED:  GPIO 17 → Relay IN2 (COM2→NO2 → Green LED)
   - Yellow LED: GPIO 27 → Relay IN3 (COM3→NO3 → Yellow LED)
   - Red LED:    GPIO 22 → Relay IN4 (COM4→NO4 → Red LED)
   ```

5. **Wire maintenance pushbutton:**
   ```
   Maintenance Pushbutton Wiring:

   GPIO Pin (with internal pull-up) ← Button terminal 1
   GND terminal ← Button terminal 2

   Suggested: GPIO 23 (active low)
   ```

6. **Wire power pushbutton to Pi 5 J2 header:**
   ```
   Power Pushbutton Wiring:

   Pi 5 J2 header pin 1 ← Button terminal 1
   Pi 5 J2 header pin 2 ← Button terminal 2

   J2 is a dedicated 2-pin power button header on the Pi 5 board,
   located near the USB-C port. This is NOT a GPIO pin.
   Use 22 AWG wire. Route through the G469 stack but do NOT use
   G469 screw terminals — connect directly to the J2 header pins.

   Behavior:
   - Pi off (halted): Brief press → powers on
   - Pi running: Brief press → clean shutdown
   - Pi frozen: Hold ~10 seconds → force power off
   ```

7. **Use Geekworm G469 screw terminals:**
   - Strip wire ends 5-6mm
   - Insert into terminal
   - Tighten screw firmly
   - Tug to verify secure

### Step 5: Wire Power Distribution (20 min)

**Tools needed:** Wire strippers, screwdriver

1. **12V Input from solar controller:**
   - Run 18AWG wire from solar controller 12V output
   - Through SP13 DC power bulkhead into enclosure
   - To input terminal block

2. **Power distribution:**
   ```
   Solar 12V ──┬── Inline Fuse (5A) ── DDR-60G-5 (12V→5V) ──► USB-C ──► Pi 5
               │
               └── Inline Fuse (5A) ── DDR-60G-12 (12V→12V reg) ──► Relay CH1 ──► PoE Switch

   Note: DDR-60G converters regulate voltage from battery
   (which varies 10-14V depending on charge state).
   DDR-60G-5 provides clean 5V via USB-C directly to Pi 5.
   Pi 5 uses built-in RTC (ML-2020 coin cell) for wake scheduling.
   PoE switch receives regulated 12V through relay channel 1 (GPIO 24).
   Camera boots when Pi wakes and closes relay, powers down when relay opens.
   ```

3. **Terminal block connections:**
   - Use ferrules on all stranded wire ends
   - Label all terminals (12V+, 12V-, GND, etc.)

### Step 6: Wire PoE Camera Circuit (15 min)

**Tools needed:** Screwdriver, Ethernet cable

1. **Circuit overview:**
   ```
   Solar 12V ── Fuse ── DDR-60G-12 ──► Relay ──► LINOVISION PoE Switch
                                                       │
                                          Uplink port ──► Pi 5 Ethernet port
                                          PoE port ──► CNLINKO bulkhead ──► Camera
   ```

2. **Connections:**
   - 12V+ from terminal block → fuse holder input
   - Fuse holder output → DDR-60G-12 input (+)
   - DDR-60G-12 output (12V regulated) → relay CH1 COM input
   - Relay CH1 NO output → PoE switch 12V+ input
   - PoE switch GND → terminal block GND
   - Relay module VCC → G469 Pin 2 (5V)
   - Relay module GND → G469 Pin 6 (GND)
   - Relay IN1 → G469 GPIO 24
   - Short Ethernet patch cable: PoE switch uplink port → Pi 5 Ethernet
   - Cat6 outdoor cable: PoE switch PoE port → CNLINKO bulkhead → Camera

3. **Operation:**
   - Pi wakes (via RTC schedule), drives GPIO 24 HIGH → relay CH1 closes
   - 12V regulated flows to PoE switch
   - PoE switch provides 48V PoE to camera over Ethernet
   - Camera boots (~45-60s), built-in IR activates automatically at night
   - Camera uploads video/snapshot via FTP to Pi over Ethernet (camera has DHCP IP)
   - Pi drives GPIO 24 LOW → relay opens → camera powers down
   - Pi enters sleep via RTC until next scheduled wake

### Step 7: Connect Peripherals (15 min)

1. **USB flash drive:**
   - SanDisk 256GB directly into Pi 5 USB-A 3.0 port (blue)

2. **LTE Modem:**
   - USB cable from EXVIST adapter → Pi 5 USB 2.0 port
   - SMA pigtails from modem → puck antenna (via 12mm hole mount)

3. **Puck antenna:**
   - Mount Proxicast ANT-122-S02 in 12mm hole on enclosure top
   - Internal SMA cables route to modem U.FL connectors

4. **PoE Camera:**
   - Already connected via Step 6
   - Verify Ethernet from PoE switch uplink to Pi 5 port
   - Verify Cat6 cable routed to CNLINKO bulkhead

5. **Rain Gauge:**
   - UART cable through PG9 gland
   - Connect to Geekworm G469 terminals / TB1:
     - VCC → 12V (TB1, 7-24V input range)
     - GND → GND (TB1)
     - TX → GPIO 15 (Pi RX)
     - RX → GPIO 14 (Pi TX)

6. **SHT40 sensor (inside enclosure):**
   - STEMMA QT to bare wire cable to Geekworm G469:
     - VCC → 3.3V
     - GND → GND
     - SDA → GPIO 2
     - SCL → GPIO 3

7. **DS18B20 probe (outside enclosure):**
   - Route cable through PG9 gland
   - Connect to Geekworm G469:
     - Data → GPIO 4 (Pin 7) (with 4.7kΩ pull-up to 3.3V)
     - VCC → 3.3V
     - GND → GND

8. **Verify all connections before powering on.**

### Step 8: Configure Pi Camera Network (15 min)

The Pi serves as DHCP server for the camera network on eth0 using dnsmasq. This avoids the ANNKE's default 192.168.1.x subnet, which conflicts with most WiFi routers.

**Note:** The SADP utility (Hikvision's camera discovery tool) does not run on ARM Macs — neither natively nor under Parallels. The dnsmasq approach below eliminates the need for SADP entirely.

1. **Set Pi eth0 to a static IP on the camera network:**
   ```bash
   sudo nmcli con mod "Wired connection 1" ipv4.addresses 192.168.50.1/24
   sudo nmcli con mod "Wired connection 1" ipv4.method manual
   sudo nmcli con up "Wired connection 1"
   ```
   If the connection name differs, find it with `nmcli con show`.

2. **Install and configure dnsmasq as DHCP server on eth0:**
   ```bash
   sudo apt install dnsmasq
   ```
   Edit `/etc/dnsmasq.conf`:
   ```
   interface=eth0
   bind-interfaces
   dhcp-range=192.168.50.100,192.168.50.200,24h
   dhcp-host=<CAMERA_MAC>,192.168.50.139
   ```
   Replace `<CAMERA_MAC>` with the camera's MAC address (printed on the camera label, or found via `arp -a` after the camera boots).

   Restart dnsmasq:
   ```bash
   sudo systemctl restart dnsmasq
   sudo systemctl enable dnsmasq
   ```

3. **Connect and discover the camera:**
   - Connect camera to PoE switch, connect switch uplink port to Pi's Ethernet port
   - Wait 60-90 seconds for camera to boot
   - The camera will receive 192.168.50.139 via DHCP
   - Verify:
     ```bash
     ping 192.168.50.139
     ```
   - If you need to find the MAC address first, temporarily omit the `dhcp-host` line, restart dnsmasq, let the camera get any IP from the range, then check:
     ```bash
     cat /var/lib/misc/dnsmasq.leases
     ```

### Step 9: Configure PoE Camera Settings (15 min)

**Note:** ANNKE C1200 is factory-sealed IP67. No housing assembly required.

1. **Access camera web interface:**
   - From the Pi or a laptop on the same network: `http://192.168.50.139`
   - Default credentials: admin / admin (change password immediately)
   - Set camera to DHCP (if not already) so it picks up the dnsmasq-assigned address on every boot
   - Configure FTP upload: point camera at Pi's FTP server (192.168.50.1)
   - Set video resolution/framerate per ORC requirements
   - Configure scheduled snapshot/video capture interval
   - Configure IR to auto-enable in low light

   **Note:** The ANNKE web interface requires a Windows-only browser plugin for live view. Skip the live view — use FTP test upload or ISAPI snapshot to verify the camera image instead.

2. **Configure FTP upload via camtool.py:**
   ```bash
   # Push FTP config to camera (server = Pi IP, credentials from .env)
   python3 camtool.py push sukabumi-cam1 ftp
   ```

3. **Test FTP upload:**
   - Trigger a test snapshot from camera web interface or via ISAPI
   - Verify file appears in Pi's FTP upload directory
   - Check image quality meets ORC requirements

4. **Verify IR function:**
   - Cover camera lens (simulate darkness)
   - IR LEDs should illuminate (visible glow)
   - Trigger snapshot, verify IR-lit image in FTP directory

### Step 10: Mount External Components (30 min)

**Tools needed:** Adjustable wrench, stainless U-bolts

1. **Camera mounting:**
   - Select pole/mounting location with clear river view
   - Use stainless U-bolts to secure ANNKE C1200 bracket
   - Aim camera at target water area
   - Secure Cat6 cable along pole with UV-resistant cable ties
   - Connect Cat6 to CNLINKO bulkhead exterior connector

3. **Rain gauge mounting:**
   - Mount Hydreon RG-15 on pole arm, away from obstructions
   - Built-in mounting holes, no separate bracket needed
   - Level the gauge (critical for accuracy)
   - Route cable to enclosure

4. **Antenna:**
   - Puck antenna already mounted on enclosure top (Step 1)
   - Verify secure and weatherproof seal

### Step 11: Final Assembly & Sealing (15 min)

1. **Cable management:**
   - Route all internal cables neatly
   - Use cable ties to bundle
   - Ensure no cables block Gore vents

2. **Seal bulkheads and glands:**
   - Tighten all bulkheads and glands firmly
   - Apply thin silicone bead around each exterior connection

3. **Final checks:**
   - [ ] All connections secure
   - [ ] Gore vents unobstructed
   - [ ] LEDs visible from outside
   - [ ] Maintenance button accessible
   - [ ] Power button accessible and labeled
   - [ ] Power button wired to Pi 5 J2 header (not G469 terminals)
   - [ ] No loose items inside

4. **Close enclosure:**
   - Verify gasket is clean and seated
   - Close lid, secure all latches/screws

---

## Power-On Procedure

### First Boot

1. **Verify solar battery voltage:** Should be >12V
2. **Connect 12V input** to enclosure (SP13 bulkhead)
3. **Press the external power button** (brief press) to power on the Pi 5
4. **Observe:**
   - Pi 5 power LED should light (red)
   - Pi 5 should boot (activity LED flashing green)
   - Status LEDs should indicate boot sequence

5. **Wait 2-3 minutes** for full boot

6. **Check status LEDs:**
   - Green steady = OK
   - Yellow blinking = working (capture/upload)
   - Red = error (check logs)

### Verify Camera

1. Enter maintenance mode (long press button)
2. Connect to WiFi hotspot
3. SSH into Pi
4. Check camera is reachable: `ping 192.168.50.139`
5. Check FTP upload directory for images from camera
6. If no files, trigger a test snapshot via ISAPI: `curl --digest -u admin:PASSWORD http://192.168.50.139/ISAPI/Streaming/channels/101/picture -o test.jpg`
7. Verify image captured and quality is acceptable

### Verify IR Light

1. Cover camera lens with hand or cloth (simulate darkness)
2. Camera IR LEDs should illuminate automatically (visible red glow)
3. Capture test image, verify IR-lit scene
4. Uncover lens, IR should turn off

### Verify LTE Connection

1. Check modem detected: `mmcli -L`
2. Check signal: `mmcli -m 0 --signal-get`
3. Test data: `ping -c 3 8.8.8.8`

### Verify Rain Gauge

1. Check UART device: `ls /dev/ttyAMA0` or `ls /dev/serial0`
2. Test serial communication: `cat /dev/ttyAMA0` (tip bucket, check for data)
3. Manually tip bucket, verify data received
4. **Verify always-on power:** put Pi to sleep (via Witty Pi schedule or `sudo halt`),
   then measure 12V at TB1 with multimeter — it should still be present. The RG-15
   must stay powered during sleep to accumulate rainfall. If it loses power, rainfall
   between cycles is lost.

---

## Troubleshooting

See `TROUBLESHOOTING.md` for detailed diagnostics.

**Quick Checks:**

| Symptom | Check |
|---------|-------|
| No boot | Battery voltage, fuses, DDR-60G-5 output, USB-C connection to Pi, power button pressed? J2 header wiring secure? |
| No camera | PoE switch powered? GPIO 24 driving relay? Camera IP reachable? Ethernet cables? |
| No IR | Cover lens to trigger. Check camera IR settings in web UI. |
| No LTE | Antenna tight? SIM inserted? IMEI registered? |
| No rain data | UART connection? GPIO 14/15 wiring? |

---

## Maintenance Notes

### Monthly
- Visual inspection of enclosure seals
- Check antenna connection
- Verify status LEDs functioning

### Quarterly
- Clean camera lens (through housing if sealed)
- Check bulkhead tightness
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
| Camera IP address | 192.168.50.139 |
| Camera FTP target | Pi FTP server at 192.168.50.1 |
| GPS coordinates | |
| Installation date | |
| Installer name | |

---

**Document Version:** 3.1
**Last Updated:** March 12, 2026
**Changes from v3.0:**
- Removed Witty Pi 5 HAT+ from stack, parts list, coating list, power path, and troubleshooting
- Pi 5 built-in RTC (ML-2020 coin cell) handles scheduling directly
- DDR-60G-5 feeds Pi 5 directly via USB-C (no Witty Pi in power path)
- Stack reduced from 3-board (Pi 5 + Witty Pi + G469) to 2-board (Pi 5 + G469)
- Changed relay from USB-powered coil to GPIO-triggered (GPIO 24→IN1, powered by G469 Pin 2/Pin 6)
- Changed DS18B20 from GPIO 24 to GPIO 4 (Pin 7)
- Changed LEDs from direct 3.3V GPIO with 330 Ohm resistors to 12V panel-mount LEDs switched through relay channels (GPIO 17→IN2, GPIO 27→IN3, GPIO 22→IN4)
- Removed current-limiting resistors from parts list

**Changes from v2.0:**
- Renamed Pi-EzConnect → Geekworm G469
- Replaced M.2 SSD with SanDisk 256GB USB flash drive
- Replaced Planet IPOE-260-12V with LINOVISION PoE Switch + Electronics-Salon relay
- Added DDR-60G-5 (12V→5V) and DDR-60G-12 (12V→12V regulated) buck converters
- Replaced DFRobot SEN0575 I2C rain gauge with Hydreon RG-15 UART (GPIO 14/15)
- Added SHT40 temp/humidity sensor (I2C) and DS18B20 temperature probe (1-Wire)
- Replaced SMA bulkheads with Proxicast ANT-122-S02 puck antenna (12mm hole)
- Replaced cable glands with CNLINKO ethernet bulkhead and SP13 DC power bulkhead
- Removed USB-RS485 adapter
