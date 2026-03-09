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
- [ ] Witty Pi 5 HAT+
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

- [ ] Flash OS image to MicroSD card
- [ ] Boot Pi 5 and verify ORC software runs
- [ ] Configure Witty Pi 5 schedule (15-minute wake cycle)
- [ ] Test PoE camera RTSP capture (ffmpeg)
- [ ] Configure WiFi hotspot for maintenance mode
- [ ] Set up LED GPIO control script
- [ ] Pre-configure Telkomsel APN (if known)
- [ ] Configure Pi eth0 static IP (192.168.50.1/24) and dnsmasq DHCP for camera network
- [ ] Configure camera RTSP settings via web interface

### 3. Hardware Testing

- [ ] Test Pi 5 + Witty Pi 5 + Geekworm G469 stack boots correctly (3-board stack)
- [ ] Verify USB flash drive is recognized
- [ ] Test LTE modem connects (with test SIM)
- [ ] Test PoE camera RTSP stream works
- [ ] Test PoE switch powers camera when relay energized
- [ ] Verify LEDs light up on GPIO control

---

## Component Inventory

Verify all components before starting assembly:

### Compute Stack
- [ ] Raspberry Pi 5 8GB (coated)
- [ ] Witty Pi 5 HAT+ (coated)
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
- [ ] Electronics-Salon DIN Rail relay module (USB-powered coil)
- [ ] DDR-60G-5 DC-DC converter (12V→5V for Witty Pi/Pi power)
- [ ] DDR-60G-12 DC-DC converter (12V→12V regulated for PoE switch)
- [ ] Cat6 outdoor shielded cable (to camera)
- [ ] CNLINKO weatherproof ethernet bulkhead, IP67 (enclosure feedthrough)
- [ ] Pole mount bracket (stainless steel)

### Climate Monitoring
- [ ] SHT40 temperature/humidity sensor (I2C, inside enclosure)
- [ ] DS18B20 waterproof temperature probe (1-Wire, outside enclosure)

### User Interface
- [ ] IP67 LEDs: Red, Yellow, Green
- [ ] IP67 momentary pushbutton
- [ ] Current-limiting resistors (330Ω)

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
   - 1× 16mm hole for pushbutton
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
   [Witty Pi 5 HAT+]
        ↑
   [Geekworm G469 HAT]
   ```

2. **Assembly:**
   - Install heatsink on Pi 5 CPU (thermal pad contact)
   - Install ML-2020 RTC battery in Pi 5
   - Align Witty Pi 5 HAT+ GPIO header with Pi 5 header
   - Press down firmly until fully seated
   - Secure with standoffs if provided
   - Align Geekworm G469 on top of Witty Pi 5
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

3. **Wire LEDs to Geekworm G469:**
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

5. **Use Geekworm G469 screw terminals:**
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
   Solar 12V ──┬── Inline Fuse (5A) ── DDR-60G-5 (12V→5V) ──► Witty Pi 5 ──► Pi 5
               │
               └── Inline Fuse (5A) ── DDR-60G-12 (12V→12V reg) ──► Relay ──► PoE Switch

   Note: DDR-60G converters regulate voltage from battery
   (which varies 10-14V depending on charge state).
   Witty Pi 5 receives clean 5V, passes through to Pi 5.
   PoE switch receives regulated 12V through relay.
   Camera boots when Pi wakes (relay closes), powers down when Pi sleeps.
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
   - DDR-60G-12 output (12V regulated) → relay NO input
   - Relay COM output → PoE switch 12V+ input
   - PoE switch GND → terminal block GND
   - USB cable from relay coil → Pi 5 USB port
   - Short Ethernet patch cable: PoE switch uplink port → Pi 5 Ethernet
   - Cat6 outdoor cable: PoE switch PoE port → CNLINKO bulkhead → Camera

3. **Operation:**
   - When Pi/Witty Pi wakes, USB powers relay coil → relay closes
   - 12V regulated flows to PoE switch
   - PoE switch provides 48V PoE to camera over Ethernet
   - Camera boots (~45-60s), built-in IR activates automatically at night
   - Pi captures video via RTSP over Ethernet (camera has DHCP IP)
   - When Pi sleeps, USB power lost → relay opens → camera powers down

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
     - Data → GPIO 24 (with 4.7kΩ pull-up to 3.3V)
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
   - Enable RTSP stream
   - Set video resolution/framerate per ORC requirements
   - Configure IR to auto-enable in low light

   **Note:** The ANNKE web interface requires a Windows-only browser plugin for live view. Skip the live view — use RTSP via VLC or ffmpeg to verify the camera image instead.

2. **Test RTSP stream with VLC:**
   ```
   Open VLC → Media → Open Network Stream →
   rtsp://admin:password@192.168.50.139:554/stream1
   ```
   This works on macOS and Linux without any plugins. You should see a live camera feed.

3. **Test RTSP capture with ffmpeg:**
   ```bash
   ffmpeg -i rtsp://admin:password@192.168.50.139:554/stream1 -frames:v 1 test.jpg
   ```

4. **Verify IR function:**
   - Cover camera lens (simulate darkness)
   - IR LEDs should illuminate (visible glow)
   - Capture test image via ffmpeg, verify IR-lit scene

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
   - [ ] Button accessible
   - [ ] No loose items inside

4. **Close enclosure:**
   - Verify gasket is clean and seated
   - Close lid, secure all latches/screws

---

## Power-On Procedure

### First Boot

1. **Verify solar battery voltage:** Should be >12V
2. **Connect 12V input** to enclosure (SP13 bulkhead)
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
4. Check camera is reachable: `ping 192.168.50.139`
5. Test RTSP capture: `ffmpeg -i rtsp://admin:password@192.168.50.139:554/stream1 -frames:v 1 test.jpg`
6. Verify image captured

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

---

## Troubleshooting

See `TROUBLESHOOTING.md` for detailed diagnostics.

**Quick Checks:**

| Symptom | Check |
|---------|-------|
| No boot | Battery voltage, fuses, Witty Pi power LED |
| No camera | PoE switch powered? Relay USB connected? Camera IP reachable? Ethernet cables? |
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
| Camera RTSP URL | rtsp://admin:PASSWORD@192.168.50.139:554/stream1 |
| GPS coordinates | |
| Installation date | |
| Installer name | |

---

**Document Version:** 3.0
**Last Updated:** March 9, 2026
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
