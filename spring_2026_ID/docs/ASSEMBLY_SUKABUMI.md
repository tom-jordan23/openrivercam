# Assembly Guide - Sukabumi Site

**Site:** Sukabumi, Indonesia (foothills)
**Type:** Solar-powered, PoE camera with built-in IR (power-cycled with Pi)
**Purpose:** Replacement of failed river monitoring unit

---

## Table of Contents

- [Pre-Assembly Checklist](#pre-assembly-checklist)
  - [1. Software Configuration](#1-software-configuration)
  - [2. Hardware Testing (Dry-Fit)](#2-hardware-testing-dry-fit)
  - [3. Conformal Coating](#3-conformal-coating-after-testing-before-travel)
- [Component Inventory](#component-inventory)
- [Assembly Steps](#assembly-steps)
  - [Step 1: Prepare Mounting Plate and DIN Rails](#step-1-prepare-mounting-plate-and-din-rails)
  - [Step 2: Assemble Compute Stack](#step-2-assemble-compute-stack-15-min)
  - [Step 3: Mount Components on DIN Rail](#step-3-mount-components-on-din-rail-20-min)
  - [Step 4: Wire Power Distribution](#step-4-wire-power-distribution-20-min)
  - [Step 5: Wire PoE Camera Circuit](#step-5-wire-poe-camera-circuit-on-mounting-plate-15-min)
  - [Step 6: Connect Peripherals](#step-6-connect-peripherals-on-mounting-plate-15-min)
  - [Step 7: Test Mounting Plate Assembly](#step-7-test-mounting-plate-assembly)
  - [Step 8: Prepare Enclosure and Install Bulkheads](#step-8-prepare-enclosure-and-install-bulkheads)
  - [Step 9: Install Mounting Plate and Connect External Peripherals](#step-9-install-mounting-plate-and-connect-external-peripherals)
  - [Step 10: Configure Pi Camera Network](#step-10-configure-pi-camera-network-15-min)
  - [Step 11: Configure PoE Camera Settings](#step-11-configure-poe-camera-settings-15-min)
  - [Step 12: Mount External Components](#step-12-mount-external-components-30-min)
  - [Step 13: Final Assembly and Sealing](#step-13-final-assembly--sealing-15-min)
- [Power-On Procedure](#power-on-procedure)
- [Troubleshooting](#troubleshooting)
- [Maintenance Notes](#maintenance-notes)
- [Site-Specific Configuration](#site-specific-configuration)

---

## Pre-Assembly Checklist

Complete these steps BEFORE traveling to Indonesia:

### 1. Software Configuration

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
- [ ] **Enable RTC battery charging** in `/boot/firmware/config.txt` — this is OFF by default because the Pi cannot detect whether the battery is rechargeable. Without this line, the RTC battery will silently drain and the clock will lose time. Set `dtparam=rtc_bbat_vchg=3000000` for ML cells or `dtparam=rtc_bbat_vchg=4200000` for LIR cells. See GPIO_WIRING.md Step 9.
- [ ] Configure Pi 5 RTC wake schedule (15-minute wake cycle via ML-2020 coin cell)
- [ ] Test PoE camera FTP upload to Pi
- [ ] Configure WiFi hotspot for maintenance mode
- [ ] Set up LED relay control script (GPIO 17/27/22 → relay channels → 12V LEDs)
- [ ] Pre-configure Telkomsel APN (if known)
- [ ] Configure Pi eth0 static IP (192.168.50.1/24) and dnsmasq DHCP for camera network
- [ ] Configure camera FTP upload settings via web interface or camtool.py

### 2. Hardware Testing (Dry-Fit)

Assemble, wire, and test the complete system **before** conformal coating.
You need to verify all connections work and identify every contact point
that must be masked during coating.

- [ ] Test Pi 5 + Geekworm G469 stack boots correctly (2-board stack)
- [ ] Verify USB flash drive is recognized
- [ ] Test LTE modem connects (with test SIM)
- [ ] Test PoE camera FTP upload works
- [ ] Test PoE switch powers camera when relay energized
- [ ] Verify LEDs light up via relay channels (GPIO 17/27/22)

### 3. Conformal Coating (After Testing, Before Travel)

Apply conformal coating only after the full system has been assembled, tested,
and verified working. This ensures you know exactly which contact points
need to be masked — coating over a connection you missed will cause failures
that are difficult to diagnose in the field.

**Do this in a low-humidity environment. Allow 24 hours cure time.**

**Boards to Coat:**
- [ ] Raspberry Pi 5
- [ ] Geekworm G469 terminal block HAT

**Masking (Use Kapton tape on all contact points):**
- GPIO header pins (all 40 pins)
- USB-A and USB-C ports
- HDMI ports
- Ethernet port
- MicroSD card slot
- J5 (BAT) RTC battery connector
- J2 power button through-holes (or pogo pins if installed)
- Heat sink mounting holes / thermal pad contact area
- Any other connector or contact point used during testing

**Procedure:**
1. Disassemble the tested stack (remove G469 from Pi)
2. Clean boards with IPA wipe, let dry completely
3. Apply Kapton tape to all masked areas listed above
4. Brush thin, even coat of MG 422C silicone on exposed PCB areas
5. Allow 24 hours cure time at room temperature
6. Remove Kapton tape after cure
7. Inspect for complete coverage, recoat bare spots if needed
8. Label each board "COATED" with date
9. Reassemble the stack and verify it still boots

---

## Component Inventory

<a href="images/sukabumi/parts-inventory-layout.png"><img src="images/sukabumi/parts-inventory-layout.png" alt="All Sukabumi build components laid out on desk: enclosure mounting plate, DIN rails, fuse holders, ANNKE camera, Pi stack, relay module, DDR-60G-5 buck converter, Proxicast puck antenna, and Quectel modem" width="400"></a>

Verify all components before starting assembly:

### Compute Stack
- [ ] Raspberry Pi 5 8GB (coated)
- [ ] Geekworm G469 HAT (coated)
- [ ] SanDisk 256GB USB flash drive
- [ ] MicroSD card 64GB (with OS)
- [ ] Heatsink/cooler for Pi 5
- [ ] Rechargeable RTC battery for Pi 5 with 2-pin JST-SH connector (ML-2020, ML-2032, LIR2032, or LIR2020 — see GPIO_WIRING.md Step 10 for chemistry options and charge voltage settings)

### Connectivity
- [ ] Quectel EG25-G modem + EXVIST Mini PCIe-USB adapter
- [ ] Proxicast ANT-122-S02 MIMO LTE puck antenna (IP67, 12mm hole mount)

### PoE Camera System
- [ ] ANNKE C1200 PoE camera (12MP, built-in IR, factory-sealed IP67)
- [ ] LINOVISION Industrial PoE Switch (Gigabit, 12V DC input)
- [ ] Electronics-Salon 4-channel SPDT DIN Rail relay module (GPIO-triggered via G469)
- [ ] DDR-60G-5 DC-DC converter (12V→5V for Pi 5 via hardwired 5V/GND GPIO)
- [ ] DDR-60G-12 DC-DC converter (12V→12V regulated for PoE switch)
- [ ] Cat6 outdoor shielded cable (to camera)
- [ ] CNLINKO weatherproof ethernet bulkhead, IP67 (enclosure feedthrough)
- [ ] Pole mount bracket (stainless steel)

### Climate Monitoring
- [ ] SHT40 temperature/humidity sensor (I2C, inside enclosure)

### User Interface
- [ ] 12V IP67 panel-mount LEDs: Red, Yellow, Green
- [ ] 2× momentary pushbuttons, normally open (maintenance + power). Any panel-mount momentary NO switch works — see GPIO_WIRING.md Step 5 for requirements and options. Match hole size to the button you purchase.

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

### Step 1: Prepare Mounting Plate and DIN Rails

**Complete all mounting plate work before drilling the enclosure box.** The
mounting plate is where all DIN rail components live. Get everything mounted,
wired, and tested on the plate first — then drill the enclosure for
bulkheads, LEDs, and buttons once you know the layout works.

**Tools needed:** Drill, marker, saw (for cutting DIN rail), screwdriver

1. **Mark and drill DIN rail mounting holes on the plate:**

   <a href="images/sukabumi/drilling-mounting-plate.png"><img src="images/sukabumi/drilling-mounting-plate.png" alt="Drilling DIN rail mounting holes in enclosure plate with DeWalt drill" width="300"></a>

   - Remove the mounting plate from the enclosure
   - Mark positions for two horizontal DIN rails
   - Drill screw holes for rail mounting

2. **Cut and install DIN rails:**

   <a href="images/sukabumi/din-rails-marked-for-cutting.png"><img src="images/sukabumi/din-rails-marked-for-cutting.png" alt="Two 35mm DIN rails on workbench with pink marker lines showing where to cut to fit enclosure width" width="300"></a>  <a href="images/sukabumi/din-rails-clamped-to-plate.png"><img src="images/sukabumi/din-rails-clamped-to-plate.png" alt="Two cut DIN rails clamped to mounting plate with bar clamps for alignment before screwing down" width="300"></a>

   - Cut rails to fit plate width
   - Mount horizontally using screws
   - Leave clearance for cable routing below

### Step 2: Assemble Compute Stack (15 min)

**Tools needed:** Phillips screwdriver

1. **Stack order (bottom to top):**

   <a href="images/sukabumi/pi5-and-g469-before-assembly.png"><img src="images/sukabumi/pi5-and-g469-before-assembly.png" alt="Raspberry Pi 5 and Geekworm G469 breakout board side by side on cutting mat before assembly, showing relative sizes" width="400"></a>

   ```
   [Raspberry Pi 5]
        ↑
   [Geekworm G469 HAT]
   ```

2. **Assembly:**
   - Install heatsink on Pi 5 CPU (thermal pad contact)
   - Install rechargeable RTC coin cell in Pi 5 J5 (BAT) connector — small
     white 2-pin JST-SH socket between USB-C and HDMI ports. Clicks in one way
     only. **Must be a rechargeable cell (ML-2020, ML-2032, LIR2032, or
     LIR2020) — NEVER a non-rechargeable CR cell.** The charge voltage in
     config.txt must match your battery chemistry. See GPIO_WIRING.md Step 10
     for the full compatibility table and config.txt settings.
   - Align Geekworm G469 GPIO header with Pi 5 header
   - Press down firmly until fully seated
   - Secure stack with standoffs

3. **Verify:**

   <a href="images/sukabumi/pi5-active-cooler-installed.png"><img src="images/sukabumi/pi5-active-cooler-installed.png" alt="Raspberry Pi 5 with official active cooler (heatsink and fan) installed, top view" width="300"></a>  <a href="images/sukabumi/pi5-g469-stack-assembled.png"><img src="images/sukabumi/pi5-g469-stack-assembled.png" alt="Completed Pi 5 and G469 stack assembled, top-down view showing G469 screw terminals accessible from above" width="300"></a>

   - All headers fully seated
   - No bent pins
   - Heatsink secure

### Step 3: Mount Components on DIN Rail (20 min)

**Tools needed:** Screwdriver, DIN rail clips

1. **Mount Pi stack:**

   <a href="images/sukabumi/pi5-stack-in-din-bracket.png"><img src="images/sukabumi/pi5-stack-in-din-bracket.png" alt="Pi 5 with G469 HAT mounted in C4Labs DIN rail bracket, angled view showing full assembly ready to snap onto rail" width="400"></a>

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

3. **Mount items without DIN rail clips:**
   - Quectel modem: sits inside the EXVIST WWAN USB carrier, which is
     Velcro/Dual-Lock attached to a DIN rail clip
   - Small breakout boards (SHT40, etc.): double-sided tape to a nearby
     DIN-mounted component's carrier tray or flat surface

4. **Layout:**

   <a href="images/sukabumi/din-rail-full-layout.png"><img src="images/sukabumi/din-rail-full-layout.png" alt="All components mounted on DIN rails: PoE switch and Pi stack on top rail, relay module, DDR-60G-5 buck converter, and distribution block on bottom rail" width="400"></a>

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

### Step 4: Wire Power Distribution (20 min)

**Tools needed:** Wire strippers, screwdriver

See **GPIO_WIRING.md** for detailed step-by-step wiring instructions,
pin assignments, continuity verification checklists, and build photos.

1. **Power distribution:**
   ```
   Solar 12V ──┬── Inline Fuse (5A) ── DDR-60G-5 (12V→5V) ──► hardwired 5V/GND ──► Pi 5 GPIO
               │
               └── Inline Fuse (5A) ── DDR-60G-12 (12V→12V reg) ──► Relay CH1 ──► PoE Switch

   Note: DDR-60G converters regulate voltage from battery
   (which varies 10-14V depending on charge state).
   DDR-60G-5 provides clean 5V hardwired to Pi 5 GPIO pins.
   Pi 5 uses built-in RTC (ML-2020 coin cell) for wake scheduling.
   PoE switch receives regulated 12V through relay channel 1 (GPIO 24).
   Camera boots when Pi wakes and closes relay, powers down when relay opens.
   ```

2. **Terminal block connections:**
   - Use solid core wire (18-22 AWG) for all internal DIN rail wiring
   - Label all terminals (12V+, 12V-, GND, etc.)

### Step 5: Wire PoE Camera Circuit on Mounting Plate (15 min)

**Tools needed:** Screwdriver, Ethernet cable

1. **Connections (all on the mounting plate):**
   - 12V+ from terminal block → fuse holder input
   - Fuse holder output → relay CH1 COM input
   - Relay CH1 NO output → PoE switch 12V+ input
   - PoE switch GND → terminal block GND
   - Relay module VCC → G469 Pin 4 (5V)
   - Relay module GND → G469 Pin 20 (GND)
   - Relay IN1 → G469 GPIO 24
   - Short Ethernet patch cable: PoE switch uplink port → Pi 5 Ethernet

2. **Operation:**
   - Pi wakes (via RTC schedule), drives GPIO 24 HIGH → relay CH1 closes
   - 12V flows to PoE switch
   - PoE switch provides 48V PoE to camera over Ethernet
   - Camera boots (~45-60s), built-in IR activates automatically at night
   - Camera uploads video/snapshot via FTP to Pi over Ethernet
   - Pi drives GPIO 24 LOW → relay opens → camera powers down
   - Pi enters sleep via RTC until next scheduled wake

### Step 6: Connect Peripherals on Mounting Plate (15 min)

1. **USB flash drive:**
   - SanDisk 256GB directly into Pi 5 USB-A 3.0 port (blue)

2. **LTE Modem:**
   - USB cable from EXVIST adapter → Pi 5 USB 2.0 port
   - SMA pigtails from modem (antenna connects later during enclosure step)

3. **SHT40 sensor (inside enclosure):**
   - STEMMA QT to bare wire cable to Geekworm G469:
     - VCC → 3.3V
     - GND → GND
     - SDA → GPIO 2
     - SCL → GPIO 3

4. **Verify all connections before powering on.**

### Step 7: Test Mounting Plate Assembly

Power on and verify the complete mounting plate assembly works before
proceeding to enclosure work. This is your last chance to fix wiring issues
before conformal coating and final assembly.

- [ ] 12V supply → DDR-60G-5 → Pi boots
- [ ] GPIO 24 → relay CH1 → PoE switch powers on
- [ ] Camera boots and is reachable via Pi
- [ ] FTP upload from camera to Pi works
- [ ] LTE modem detected
- [ ] SHT40 sensor readable via I2C
- [ ] All continuity and isolation checks pass (see GPIO_WIRING.md)

**Once the mounting plate assembly is fully tested, proceed to conformal
coating (Pre-Assembly Checklist Step 3), then enclosure preparation.**

---

### Step 8: Prepare Enclosure and Install Bulkheads

**Do not drill the enclosure until the mounting plate assembly is tested.**

<a href="images/sukabumi/enclosure-opened.png"><img src="images/sukabumi/enclosure-opened.png" alt="NEMA 4X enclosure opened showing interior with removable mounting plate, gasket seal on door, and latch" width="400"></a>

**Tools needed:** Drill, step bit or hole saw, marker

1. **Mark and drill enclosure holes:**
   - 2× M12 holes for Gore vents (opposite sides for airflow)
   - 1× 12mm hole for Proxicast puck antenna (enclosure top)
   - 1× hole for CNLINKO ethernet bulkhead (PoE camera)
   - 1× hole for SP13 DC power bulkhead (12V input)
   - 3× 10mm holes for status LEDs
   - 2× holes for pushbuttons (maintenance + power) — hole size depends on
     the buttons you purchased (12mm, 16mm, 19mm, or 22mm are common)
   - 1× 16mm hole for rain gauge SD16 bulkhead connector

2. **Install bulkheads and glands:**
   - Gore M12 vents (hand-tight plus 1/4 turn)
   - SP13 DC power bulkhead
   - CNLINKO ethernet bulkhead
   - SD16 4-pin bulkhead connector for rain gauge

3. **Install user interface components:**
   - Insert LEDs into 10mm panel holes, secure with nuts
   - Install pushbuttons, secure with nuts
   - Label power button clearly as "POWER"

   See **GPIO_WIRING.md** for detailed wiring instructions:
   - **Step 4** — LED wiring (12V, relay-switched)
   - **Step 5** — Maintenance pushbutton (GPIO 23 to GND)
   - **Step 6** — Power button (Pi 5 J2 header)

### Step 9: Install Mounting Plate and Connect External Peripherals

1. **Install mounting plate** into enclosure with provided screws

2. **Connect antenna:**
   - Mount Proxicast ANT-122-S02 puck antenna in 12mm hole
   - Route internal SMA cables to modem U.FL connectors

3. **Connect 12V input:**
   - Wire from SP13 DC power bulkhead to TB1 terminal block

4. **Connect rain gauge:**
   - Rain gauge connects through a 4-pin SD16 bulkhead connector (16mm hole)
   - Outside: 18/4 stranded jacketed cable from RG-15 pigtail to bulkhead plug
   - Inside: solid core 22 AWG from bulkhead socket to G469/TB1
   - Pin 1: 12V (TB1), Pin 2: GND (G469 Pin 9), Pin 3: TX→RX (GPIO 14),
     Pin 4: RX→TX (GPIO 15)
   - See GPIO_WIRING.md Step 7 for full pin map, connector details, and
     verification checklists

5. **Connect Cat6 outdoor cable:**
   - PoE switch PoE port → CNLINKO bulkhead → Camera

### Step 10: Configure Pi Camera Network (15 min)

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
   bind-dynamic
   dhcp-range=192.168.50.100,192.168.50.200,24h
   dhcp-host=<CAMERA_MAC>,192.168.50.139
   ```
   **Important:** Use `bind-dynamic` (not `bind-interfaces`). This allows dnsmasq to start
   before eth0 has carrier — required because the PoE relay may not be on at boot time.
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

### Step 11: Configure PoE Camera Settings (15 min)

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

### Step 12: Mount External Components (30 min)

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

### Step 13: Final Assembly & Sealing (15 min)

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

### Run Preflight Checks

After SSH'ing into the Pi, run the preflight script to verify all packages,
configs, services, and hardware are correct:

```bash
orc-preflight
```

Review the output — all items should be PASS (WARN is informational). If there
are FAILs, run with `--fix` to attempt automatic fixes:

```bash
orc-preflight --fix
```

Key checks include: required packages, dnsmasq/NetworkManager config, RTC
battery charging enabled, PoE relay script in PATH, and hardware detection
(modem, sensors, USB drive). Fix any remaining FAILs manually before
proceeding.

### Verify Camera

<a href="images/sukabumi/camera-live-view-working.png"><img src="images/sukabumi/camera-live-view-working.png" alt="ANNKE camera live view displayed on monitor via PoE switch and Pi, showing successful end-to-end bench test of camera system" width="400"></a>

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
4. **Verify always-on power:** put Pi to sleep (`sudo halt`), then measure 12V
   at TB1 with multimeter — it should still be present. The RG-15 must stay
   powered during sleep to accumulate rainfall. If it loses power, rainfall
   between cycles is lost.

---

## Troubleshooting

See `TROUBLESHOOTING.md` for detailed diagnostics.

**Quick Checks:**

| Symptom | Check |
|---------|-------|
| No boot | Battery voltage, fuses, DDR-60G-5 output, 5V/GND wiring to Pi GPIO, power button pressed? J2 header wiring secure? |
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

**Document Version:** 3.2
**Last Updated:** March 21, 2026
**Changes from v3.1:**
- Pushbutton wiring moved to GPIO_WIRING.md (Steps 5-6) with detailed button requirements and equivalent options
- RTC battery section expanded: supports ML-2020, ML-2032, LIR2032, LIR2020 with chemistry-specific charge voltages
- Relay module pin assignments updated: VCC → Pin 4, GND → Pin 20 (avoids doubling up with buck converter on Pin 2/Pin 6)
- Removed Witty Pi reference from rain gauge verification
- Hole sizes for pushbuttons no longer hardcoded (depends on button purchased)
- Solid core wire specified throughout (no ferrules)

**Changes from v3.0:**
- Removed Witty Pi 5 HAT+ from stack, parts list, coating list, power path, and troubleshooting
- Pi 5 built-in RTC (ML-2020 coin cell) handles scheduling directly
- DDR-60G-5 feeds Pi 5 directly via hardwired 5V/GND GPIO pins (no Witty Pi in power path)
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
