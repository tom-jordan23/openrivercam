# Assembly Guide - Jakarta Site

**Site:** Jakarta, Indonesia (coastal/urban)
**Type:** AC-powered with 24hr UPS, 2x PoE cameras
**Purpose:** New training/demo installation

---

## Table of Contents

- [Pre-Assembly Checklist](#pre-assembly-checklist)
  - [1. Software Configuration](#1-software-configuration)
  - [2. Hardware Testing (Dry-Fit)](#2-hardware-testing-dry-fit)
  - [3. Conformal Coating (After Testing, Before Travel)](#3-conformal-coating-after-testing-before-travel)
- [Component Inventory](#component-inventory)
- [Assembly Steps](#assembly-steps)
  - [Step 1: Install Grounding System](#step-1-install-grounding-system-1-hour)
  - [Step 2: Install Mounting Pole](#step-2-install-mounting-pole-2-3-hours)
  - [Step 3: Prepare Mounting Plate and DIN Rails](#step-3-prepare-mounting-plate-and-din-rails)
  - [Step 4: Assemble Compute Stack](#step-4-assemble-compute-stack-15-min)
  - [Step 5: Mount Components on DIN Rails](#step-5-mount-components-on-din-rails-30-min)
  - [Step 6: Install Power System](#step-6-install-power-system-45-min)
  - [Step 7: Install PoE System](#step-7-install-poe-system-30-min)
  - [Step 8: Connect Peripherals on Mounting Plate](#step-8-connect-peripherals-on-mounting-plate-15-min)
  - [Step 9: Test Mounting Plate Assembly](#step-9-test-mounting-plate-assembly)
  - [Step 10: Prepare Enclosure and Install Bulkheads](#step-10-prepare-enclosure-and-install-bulkheads)
  - [Step 11: Install Mounting Plate and Connect External Peripherals](#step-11-install-mounting-plate-and-connect-external-peripherals)
  - [Step 12: Mount Enclosure on Pole](#step-12-mount-enclosure-on-pole-30-min)
  - [Step 13: Mount Cameras](#step-13-mount-cameras-45-min)
  - [Step 14: Mount Rain Gauge](#step-14-mount-rain-gauge-20-min)
  - [Step 15: Final Assembly and Testing](#step-15-final-assembly--testing-30-min)
- [Power-On Procedure](#power-on-procedure)
- [Power Budget Verification](#power-budget-verification)
- [Troubleshooting](#troubleshooting)
- [Site-Specific Configuration](#site-specific-configuration)

---

## Pre-Assembly Checklist

Complete these steps BEFORE traveling to Indonesia:

### 1. Software Configuration

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
- [ ] **Enable RTC battery charging** in `/boot/firmware/config.txt` — this is OFF by default because the Pi cannot detect whether the battery is rechargeable. Without this line, the RTC battery will silently drain and the clock will lose time. Set `dtparam=rtc_bbat_vchg=3000000` for ML cells or `dtparam=rtc_bbat_vchg=4200000` for LIR cells. See the RTC battery section in Step 4 for chemistry options and charge voltage settings.
- [ ] Configure for 2-camera FTP capture (Pi FTP server + camera FTP upload config)
- [ ] Configure WiFi hotspot for maintenance mode
- [ ] Set up LED GPIO control script
- [ ] Pre-configure Telkomsel APN (if known)

### 2. Hardware Testing (Dry-Fit)

Assemble, wire, and test the complete system **before** conformal coating.
You need to verify all connections work and identify every contact point
that must be masked during coating.

- [ ] Test Pi 5 + Geekworm G469 stack boots correctly (2-board stack)
- [ ] Verify USB flash drive is recognized
- [ ] Test LTE modem connects (with test SIM)
- [ ] Test PoE switch powers both cameras
- [ ] Verify LEDs light up on GPIO control
- [ ] Test relay switches PoE switch power on/off (GPIO 24)

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

### 4. Camera Pre-Configuration

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
   bind-dynamic
   dhcp-range=192.168.50.100,192.168.50.200,24h
   dhcp-host=<CAMERA_1_MAC>,192.168.50.101
   dhcp-host=<CAMERA_2_MAC>,192.168.50.102
   ```
   **Important:** Use `bind-dynamic` (not `bind-interfaces`). This allows dnsmasq to start
   before eth0 has carrier — required because the PoE relay may not be on at boot time.
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
  - Camera 1 (192.168.50.101) -> check FTP directory
  - Camera 2 (192.168.50.102) -> check FTP directory
- [ ] Adjust image settings (exposure, focus) if needed

---

## Component Inventory

### Compute Stack
- [ ] Raspberry Pi 5 8GB (coated)
- [ ] Geekworm G469 terminal block HAT (coated)
- [ ] SanDisk 256GB USB flash drive
- [ ] MicroSD card 64GB (with OS)
- [ ] Active cooler for Pi 5
- [ ] Rechargeable RTC battery for Pi 5 with 2-pin JST-SH connector (ML-2020, ML-2032, LIR2032, or LIR2020 — see Step 4 for chemistry options and charge voltage settings)

### Connectivity
- [ ] Quectel EG25-G modem + EXVIST Mini PCIe-USB adapter
- [ ] Proxicast ANT-122-S02 MIMO LTE puck antenna (IP67, 12mm hole mount)

### Power System
- [ ] Mean Well SDR-120-12 DIN rail PSU
- [ ] Heschen HS-40-N 2P surge protector (40kA, 275V)
- [ ] DDR-60G-5 DC-DC buck converter (12V->5V for Pi power)
- [ ] LiFePO4 100Ah battery (source locally)
- [ ] 20A LiFePO4 charger (source locally or carry)
- [ ] Power distribution blocks (12-position, DIN rail)
- [ ] Blade fuse holders + fuses (5A, 10A, 15A)

### Camera System
- [ ] ANNKE C1200 PoE cameras (x2, factory-sealed IP67)
- [ ] LINOVISION Industrial PoE Switch (Gigabit, 12V DC input)
- [ ] Electronics-Salon 4-channel SPDT DIN Rail relay module (GPIO-triggered via G469)
- [ ] Cat6 outdoor shielded cables, 10ft pre-terminated (x4)
- [ ] CNLINKO weatherproof ethernet bulkheads, IP67 (x2)
- [ ] Camera pole mount brackets (x2)

### Humidity Control & Climate Monitoring
- [ ] PTC heater 15W (for enclosure)
- [ ] SHT40 temperature/humidity sensor (I2C, inside enclosure)
- [ ] DS18B20 waterproof temperature probe (1-Wire, outside enclosure)
- [ ] Amphenol Gore vents, IP68 (x2)
- [ ] 40 CFM fans (x2, for internal air circulation)

### User Interface
- [ ] 12V IP67 panel-mount LEDs: Red, Yellow, Green
- [ ] 2x momentary pushbuttons, normally open (maintenance + power). Any panel-mount momentary NO switch works — common options include Gebildet 16mm stainless (Amazon, ~$9, IP67), C&K AP Series (~$12, IP67), or generic 12mm metal momentary (~$3-5, IP65-67). Match hole size to the button you purchase.

### Enclosure & Mounting
- [ ] VEVOR NEMA 4x enclosure (16"x12"x8")
- [ ] DIN rail 35mm (x2)
- [ ] DIN rail clips
- [ ] CNLINKO weatherproof ethernet bulkheads (x2, for cameras)
- [ ] SP13 weatherproof AC mains input bulkhead (IP68, for 220V AC input)
- [ ] Neoprene rubber (galvanic isolation for mounting)

### Grounding (source locally)
- [ ] Copper grounding rod (1.5m)
- [ ] Ground cable 6 AWG (10m)
- [ ] Ground lugs and clamps

### Mounting (source locally)
- [ ] Galvanized pole (4m x 50mm)
- [ ] Pole base flange + anchors
- [ ] U-bolts for enclosure mounting

### Rain Gauge
- [ ] Hydreon RG-15 optical rain gauge (UART RS232 TTL 3.3V)
- [ ] Built-in mounting holes (no separate bracket needed)
- [ ] SD16 4-pin IP68 bulkhead connector (16mm hole) for rain gauge cable
- [ ] 18/4 stranded jacketed external cable (measure from rain gauge to enclosure, add 30cm slack on each end)

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
   - Measure resistance to earth (<25 ohm acceptable)
   - If >25 ohm, add second rod 2m away, bond together

### Step 2: Install Mounting Pole (2-3 hours)

**Tools needed:** Shovel, level, concrete mix, wrenches

1. **Dig foundation:**
   - 50cm x 50cm x 60cm deep hole
   - Position for optimal camera view of river

2. **Set pole base:**
   - Install base flange on pole bottom
   - Set pole in hole, verify vertical with level
   - Pour concrete, allow 24 hours cure

3. **Alternative (existing structure):**
   - Use U-bolts to mount to existing pole/structure
   - Ensure mounting is stable and rated for wind

### Step 3: Prepare Mounting Plate and DIN Rails

**Complete all mounting plate work before drilling the enclosure box.** The
mounting plate is where all DIN rail components live. Get everything mounted,
wired, and tested on the plate first — then drill the enclosure for
bulkheads, LEDs, and buttons once you know the layout works.

**Tools needed:** Drill, marker, saw (for cutting DIN rail), screwdriver

1. **Mark and drill DIN rail mounting holes on the plate:**
   - Remove the mounting plate from the enclosure
   - Mark positions for two horizontal DIN rails
   - Drill screw holes for rail mounting

2. **Cut and install DIN rails:**
   - Cut rails to fit plate width
   - Mount horizontally using screws
   - Upper rail: PSU, surge protector, terminal block, fuse holders
   - Lower rail: Pi stack, PoE switch, relay module, DDR-60G-5
   - Leave clearance for cable routing below

### Step 4: Assemble Compute Stack (15 min)

1. **Stack order (bottom to top):**
   ```
   [Raspberry Pi 5]
        |
   [Geekworm G469 HAT]
   ```
   2-board stack. Pi 5 built-in RTC with rechargeable coin cell provides timekeeping.

2. Install active cooler on Pi 5

3. **Install rechargeable RTC battery:**
   Install the rechargeable coin cell in the Pi 5 J5 (BAT) connector — a small
   white 2-pin JST-SH socket between the USB-C and HDMI ports. Clicks in one
   way only.

   **Must be a rechargeable cell — NEVER a non-rechargeable CR cell.** The Pi 5
   has a built-in trickle charger. If charging is enabled with a non-rechargeable
   cell installed, the cell can leak, vent, or rupture.

   **Compatible rechargeable battery types:**

   | Battery | Chemistry | Nominal V | Charge V | `config.txt` Setting | Capacity |
   |---------|-----------|-----------|----------|----------------------|----------|
   | **ML-2020** | Manganese lithium | 3.0V | 3.0V | `dtparam=rtc_bbat_vchg=3000000` | ~45 mAh |
   | **ML-2032** | Manganese lithium | 3.0V | 3.0V | `dtparam=rtc_bbat_vchg=3000000` | ~65 mAh |
   | **LIR2032** | Lithium-ion | 3.6V | 4.2V | `dtparam=rtc_bbat_vchg=4200000` | ~40 mAh |
   | **LIR2020** | Lithium-ion | 3.6V | 4.2V | `dtparam=rtc_bbat_vchg=4200000` | ~20 mAh |

   Setting the wrong charge voltage can damage the battery: ML cells charged
   above 3.2V can be damaged; LIR cells charged to only 3.0V will work but
   won't fully charge. The 20 vs 32 in the name refers to thickness (2.0mm
   vs 3.2mm) — either size works since the battery connects via a JST-SH cable.

   **The Pi 5 ships with RTC battery charging DISABLED.** The Pi has no way
   to detect whether the battery is rechargeable, so it defaults to not
   charging. You MUST add the correct `dtparam=rtc_bbat_vchg` line to
   `/boot/firmware/config.txt` manually. If you skip this, the battery will
   silently drain and the RTC will lose time during power outages.

4. Mount stack on lower DIN rail using DIN rail clip

### Step 5: Mount Components on DIN Rails (30 min)

**Tools needed:** Screwdriver, DIN rail clips

1. **Mount on upper DIN rail:**
   - Heschen HS-40-N surge protector
   - Mean Well SDR-120-12 PSU
   - Terminal block TB1
   - Fuse holders (F1-F4)

2. **Mount on lower DIN rail:**
   - Pi stack (from Step 4)
   - LINOVISION PoE switch
   - Electronics-Salon relay module
   - DDR-60G-5 buck converter

3. **Mount items without DIN rail clips:**
   - Quectel modem: sits inside the EXVIST WWAN USB carrier, which is
     Velcro/Dual-Lock attached to a DIN rail clip
   - SHT40 breakout board: double-sided tape to a nearby DIN-mounted
     component's carrier tray or flat surface. Position away from heat
     sources (Pi CPU, DC-DC converters) for accurate readings.

### Step 6: Install Power System (45 min)

**Tools needed:** Screwdriver, wire strippers

**Wire spec:** Use solid core wire (18-22 AWG) for all internal DIN rail wiring.

**IMPORTANT: Do NOT connect AC power until all wiring is complete.**

**Understanding the AC layout:** The surge suppressor is a **parallel** device —
it does not pass power through. It sits across the AC line and clamps voltage
spikes. The PSU and surge suppressor both connect to the same AC bus via DIN
rail terminal blocks.

1. **Set up AC distribution terminal blocks on the bottom DIN rail:**

   Use DIN rail feed-through terminal blocks (rated 600V+ / 20A+) to create
   an AC distribution point. You need 4 blocks total:
   - **2 blocks for L (line)** — use brown blocks if available
   - **2 blocks for N (neutral)** — use blue blocks if available

   **How to assemble the terminal block pairs:**
   1. Snap 2 blocks side by side onto the DIN rail
   2. Add end stops on each side to prevent sliding
   3. Insert a bridge bar to connect the pair — look for a narrow slot or
      removable plastic cover on top of each block between the two screws.
      Break off a 2-segment piece of bridge bar, drop it into the slots so
      each U-segment sits in its block, and tighten the bridge screw. This
      electrically connects all 4 lugs (2 per block) together.
   4. Repeat for the second pair

   ```
   Bottom DIN Rail:
   [end stop] [BROWN][BROWN] [BLUE][BLUE] [end stop] ... [SURGE] [MEAN WELL PSU]
                 L1     L2     N1    N2
                bridged        bridged
   ```

2. **Wire L (line) terminal blocks — 3 connections:**
   - Lug 1: AC input line wire (from SP13 bulkhead, brown)
   - Lug 2: Mean Well PSU L terminal
   - Lug 3: Surge suppressor L terminal
   - Lug 4: spare (leave empty)

3. **Wire N (neutral) terminal blocks — 3 connections:**
   - Lug 1: AC input neutral wire (from SP13 bulkhead, blue)
   - Lug 2: Mean Well PSU N terminal
   - Lug 3: Surge suppressor N terminal
   - Lug 4: spare (leave empty)

4. **Wire PE (ground) — direct, no terminal block needed:**
   - AC input PE wire (from SP13 bulkhead, green/yellow) →
     surge suppressor PE terminal → building ground wire back
     out through the SP13 bulkhead
   - DC ground (TB1) is a separate floating ground — do NOT
     connect DC ground to AC PE

5. **Verify Mean Well SDR-120-12:**
   - No input voltage selector needed — it is auto-ranging (88-264V AC)
   - 12V DC output goes to terminal block TB1 (wired in a later step)

6. **Pre-power AC wiring verification (DO THIS BEFORE PLUGGING IN):**

   With the AC cord **unplugged from the wall**, use your multimeter to verify
   the wiring is correct and safe.

   **Continuity checks (should beep):**
   - [ ] AC cord L wire ↔ L terminal block — beep
   - [ ] L terminal block ↔ PSU L terminal — beep
   - [ ] L terminal block ↔ Surge suppressor L — beep
   - [ ] AC cord N wire ↔ N terminal block — beep
   - [ ] N terminal block ↔ PSU N terminal — beep
   - [ ] N terminal block ↔ Surge suppressor N — beep
   - [ ] AC cord PE wire ↔ Surge suppressor PE — beep

   **Short checks (should NOT beep):**
   - [ ] L terminal block ↔ N terminal block — **NO beep**
   - [ ] L terminal block ↔ PE wire — **NO beep**
   - [ ] N terminal block ↔ PE wire — **NO beep**
   - [ ] PSU L ↔ PSU N — **NO beep**

   **Cord end verification (with cord unplugged, test at the plug end):**
   - [ ] Narrow blade (hot) ↔ L terminal block — beep
   - [ ] Wide blade (neutral) ↔ N terminal block — beep
   - [ ] Round prong (ground) ↔ Surge suppressor PE — beep

   **If ALL continuity checks pass and ALL short checks are silent, the AC
   wiring is safe to energize.**

3. **Wire battery system:**
   ```
   Mean Well 12V+ --+---> Charger input (+)
                     |
                     +---> Terminal block TB1 (system 12V+)

   Charger output ---> Battery (+)
   Battery (+) ---> Terminal block TB1 (backup 12V+)
   Battery (-) ---> Terminal block TB1 (system GND)
   ```
   Battery BMS handles low-voltage cutoff automatically.

4. **Install DDR-60G-5 buck converter:**
   ```
   TB1 12V+ --[FUSE 5A]--> DDR-60G-5 input (+)
   TB1 GND --> DDR-60G-5 input (-)
   DDR-60G-5 output (5V) --> hardwired 5V/GND --> Pi 5 GPIO pins
   ```

5. **Install fuses:**
   - Main 12V feed: 15A fuse
   - PoE relay/switch feed: 10A fuse (includes inline fuse between TB1 and relay)
   - Pi/DDR-60G-5 feed: 5A fuse
   - Heater/fan feed: 5A fuse

### Step 7: Install PoE System (30 min)

**Wire spec:** Use solid core wire (18-22 AWG) for all internal DIN rail wiring.

1. **Wire relay module (via Geekworm G469 terminals):**
   - Relay VCC -> G469 Pin 4 (5V)
   - Relay GND -> G469 Pin 20 (GND)
   - GPIO 24 (Pin 18) -> IN1 (PoE switch power)
   - GPIO 17 (Pin 11) -> IN2 (Green LED)
   - GPIO 27 (Pin 13) -> IN3 (Yellow LED)
   - GPIO 22 (Pin 15) -> IN4 (Red LED)

2. **Wire PoE switch power through fuse and relay:**
   - 12V+ from TB1 -> inline fuse (10A) -> relay CH1 COM input
   - Relay CH1 NO output -> LINOVISION PoE switch 12V+ input
   - TB1 GND -> PoE switch GND input

   **Why NO (Normally Open) instead of NC (Normally Closed):** Using NO is a
   deliberate fail-safe. If the Pi crashes, hangs, or fails to shut down
   cleanly, GPIO pins float LOW and the relay falls open. The PoE switch and
   cameras **lose power automatically**, preventing the system's largest power
   consumers from draining the battery. With NC, a Pi crash would leave both
   cameras powered indefinitely, which could drain the UPS battery and leave
   the station non-functional until someone physically visits the site. The
   ~15-20 second delay (Pi boots -> GPIO HIGH -> relay closes -> cameras begin
   booting) is an acceptable tradeoff for this protection.

3. **Connect Ethernet cables:**
   - Short patch cable: PoE switch uplink port -> Pi 5 Ethernet
   - PoE Port 1 -> internal Cat6 patch cable (connects to CNLINKO bulkhead later)
   - PoE Port 2 -> internal Cat6 patch cable (connects to CNLINKO bulkhead later)

### Step 8: Connect Peripherals on Mounting Plate (15 min)

1. **USB flash drive:** SanDisk 256GB directly into Pi 5 USB-A 3.0 port
2. **LTE Modem:** USB cable from EXVIST adapter -> Pi 5 USB 2.0 port.
   SMA pigtails from modem (antenna connects later during enclosure step)
3. **SHT40 sensor (inside enclosure):**
   - STEMMA QT to bare wire cable to Geekworm G469:
     - VCC -> 3.3V
     - GND -> GND
     - SDA -> GPIO 2
     - SCL -> GPIO 3
4. **DS18B20 waterproof temperature probe:**
   - Connect to Geekworm G469 (internal wiring only — probe routes outside
     through PG9 gland during enclosure step):
     - Data -> GPIO 4 / Pin 7 (with 4.7k ohm pull-up to 3.3V)
     - VCC -> 3.3V
     - GND -> GND
5. **Relay GPIO:** Already wired in Step 7 (VCC, GND, IN1-IN4 from G469)

### Step 9: Test Mounting Plate Assembly

Power on and verify the complete mounting plate assembly works before
proceeding to enclosure work. This is your last chance to fix wiring issues
before final assembly.

- [ ] 12V supply -> DDR-60G-5 -> Pi boots
- [ ] GPIO 24 -> relay CH1 -> PoE switch powers on
- [ ] Both cameras boot and are reachable via Pi
- [ ] FTP upload from both cameras to Pi works
- [ ] LTE modem detected
- [ ] SHT40 sensor readable via I2C
- [ ] DS18B20 temperature probe readable
- [ ] LEDs light up via relay channels (GPIO 17/27/22)
- [ ] All connections secure, no loose wires

**Once the mounting plate assembly is fully tested, proceed to enclosure
preparation.**

---

### Step 10: Prepare Enclosure and Install Bulkheads

**Do not drill the enclosure until the mounting plate assembly is tested.**

**Tools needed:** Drill, step bit, marker

1. **Mark hole positions:**
   - 2x M12 holes for Gore vents
   - 1x 12mm hole for Proxicast puck antenna (enclosure top)
   - 2x holes for CNLINKO ethernet bulkheads (camera cables)
   - 1x hole for SP13 AC mains input bulkhead (220V AC input)
   - 1x M16 hole for ground cable
   - 2x holes for 40 CFM fans
   - 3x 10mm holes for status LEDs
   - 2x holes for pushbuttons (maintenance + power) — hole size depends on
     the buttons you purchased (12mm, 16mm, 19mm, or 22mm are common)
   - 1x 16mm hole for rain gauge SD16 bulkhead connector
   - 1x PG9 hole for DS18B20 temperature probe

2. **Drill holes:**
   - Use step bit for clean cuts
   - Deburr all holes
   - Test-fit all bulkheads, glands, and vents

3. **Install bulkheads and glands:**
   - Gore M12 vents (hand-tight plus 1/4 turn, position for cross-ventilation)
   - SP13 AC mains input bulkhead
   - CNLINKO ethernet bulkheads (x2)
   - SD16 4-pin bulkhead connector for rain gauge

4. **Install user interface components:**
   - Insert LEDs into 10mm panel holes, secure with nuts
   - Install pushbuttons, secure with nuts
   - Label power button clearly as "POWER"
   - Wire LEDs through relay channels (12V switched by relay):
     - Green LED: 12V from TB1 -> relay CH2 COM -> CH2 NO -> LED -> GND (GPIO 17 -> IN2)
     - Yellow LED: 12V from TB1 -> relay CH3 COM -> CH3 NO -> LED -> GND (GPIO 27 -> IN3)
     - Red LED: 12V from TB1 -> relay CH4 COM -> CH4 NO -> LED -> GND (GPIO 22 -> IN4)
   - Wire maintenance pushbutton to Geekworm G469 terminals:
     - Button: GPIO 23 (Pin 16) -> Button -> GND (Pin 14)

5. **Wire external power button to Pi 5 J2 header:**

   J2 is a dedicated 2-pin power button header on the Pi 5, located near the
   USB-C port. This is NOT a GPIO pin — it is hardware-level power control.

   **J2 connector:** J2 is **unpopulated** — it's two bare through-holes at
   2.54mm pitch, not header pins. You need to add pins before you can connect
   wires.

   **No-solder method (recommended):** Use **through-hole pogo pins** (Adafruit
   product 5381, or equivalent). These are spring-loaded pins with thin stems
   that press-fit into through-holes without soldering.

   1. Snap 2 pogo pins off the strip
   2. Press the thin stems into the J2 through-holes from the top of the board
   3. The stems friction-fit into the holes; the spring tips protrude above
   4. Push **Dupont female jumper wires** onto the spring tips
   5. Cut the other ends of the Dupont wires, strip them, and connect to the
      button's screw terminals

   **Vibration resistance:** Apply a small dab of **hot glue** over the pogo
   pins and Dupont connections after verifying everything works. Hot glue holds
   firmly but can be peeled off for service — do not use superglue or epoxy.

   Polarity does not matter (momentary short between the two pins).

   Behavior:
   - Brief press powers on (from halted)
   - Brief press initiates clean shutdown (while running)
   - ~10s hold forces power off (if frozen)

### Step 11: Install Mounting Plate and Connect External Peripherals

1. **Install mounting plate** into enclosure with provided screws

2. **Install CNLINKO ethernet bulkheads:**
   - Connect internal Cat6 patch cables from PoE switch ports to bulkheads
   - External Cat6 cables connect to cameras

3. **Connect antenna:**
   - Mount Proxicast ANT-122-S02 puck antenna in 12mm hole on enclosure top
   - Route internal SMA cables to modem U.FL connectors

4. **Connect rain gauge (inside wiring):**
   - Rain gauge connects through the 4-pin SD16 bulkhead connector (16mm hole)
   - Inside: solid core 22 AWG from bulkhead socket to G469/TB1:
     - Bulkhead pin 1 (12V) -> TB1 12V output
     - Bulkhead pin 2 (GND) -> G469 Pin 9 (GND)
     - Bulkhead pin 3 (TX->RX) -> G469 Pin 8 (GPIO 14 / TXD)
     - Bulkhead pin 4 (RX->TX) -> G469 Pin 10 (GPIO 15 / RXD)
   - Outside: 18/4 stranded jacketed cable from RG-15 pigtail to bulkhead plug
   - SD16 contacts require solder termination
   - **No-solder alternative:** Use a PG9 cable gland instead. The rain gauge
     pigtail passes through the gland directly into the enclosure. Simpler but
     requires opening the enclosure to disconnect the rain gauge.

5. **Route DS18B20 temperature probe** cable through PG9 gland to outside enclosure

6. **Install PTC heater and fans:**
   - Mount 15W PTC heater on enclosure interior wall
   - Wire to 12V through thermostat/hygrostat
   - Set to activate when humidity >70% or temp <25C
   - Mount fans in pre-drilled enclosure holes
   - Wire to 12V from TB1 (through heater/fan fuse)
   - Fans run whenever system is powered

7. **Verify Gore vents clear:**
   - No obstruction
   - Cross-ventilation path available

### Step 12: Mount Enclosure on Pole (30 min)

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

### Step 13: Mount Cameras (45 min)

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

### Step 14: Mount Rain Gauge (20 min)

1. **Mount Hydreon RG-15** on pole (separate from cameras)
   - Built-in mounting holes, no separate bracket needed
2. **Level the gauge** (critical for accuracy)
3. **Route 18/4 stranded jacketed cable** from rain gauge to SD16 bulkhead plug
4. **Connect to bulkhead:**
   - Pin 1: VCC (12V)
   - Pin 2: GND
   - Pin 3: TX->RX (GPIO 14)
   - Pin 4: RX->TX (GPIO 15)

### Step 15: Final Assembly & Testing (30 min)

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
   - [ ] Inline fuse installed between TB1 and relay CH1

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
3. Status LEDs should indicate:
   - Green = OK
   - Yellow blink = working
   - Red = error

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
| PoE cameras (x2) | ~15W | |
| PoE switch | ~5W | |
| Modem (idle) | ~1W | |
| PTC heater (avg) | ~8W | |
| Fans (x2) | ~3W | |
| **Total average** | **~40W** | |

**Battery runtime:** 1280Wh / 40W = 32 hours (theoretical)

---

## Troubleshooting

See `TROUBLESHOOTING.md` for detailed diagnostics.

**Quick Checks:**

| Symptom | Check |
|---------|-------|
| No power | AC voltage? Surge protector? PSU LED? |
| No Pi boot | Fuse? 12V at terminals? DDR-60G-5 output? 5V at GPIO pins? Power button pressed? J2 wiring? |
| Cameras offline | PoE switch powered? Relay GPIO wiring correct? Inline fuse intact? Cable continuity? Ping test? |
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
| Ground resistance | ohm |
| GPS coordinates | |
| AC circuit breaker # | |
| Installation date | |
| Installer name | |

---

**Document Version:** 3.0
**Last Updated:** March 24, 2026
**Changes from v2.0:**
- Reordered conformal coating to AFTER hardware testing (dry-fit) — you need to test first to identify all contact points that need masking
- Added J5 (BAT) and J2 pogo pins to conformal coating masking list
- Separated mounting plate work from enclosure drilling — all DIN rail/plate work comes first, then enclosure holes
- Added "Test Mounting Plate Assembly" step between plate wiring and enclosure prep
- Replaced ferrule crimper / stranded wire with solid core wire (18-22 AWG) throughout for internal DIN rail wiring
- Fixed relay pin assignments: VCC to Pin 4 (5V), GND to Pin 20 (avoids doubling up wires in screw terminals)
- Added inline fuse between TB1 and relay CH1 COM on PoE switch 12V path
- Fixed SP13 bulkhead labeling: carries 220V AC mains, not DC
- Changed rain gauge from PG9 cable gland to SD16 4-pin IP68 bulkhead connector with 18/4 stranded jacketed external cable (PG9 is a no-solder alternative)
- Expanded RTC battery section: supports ML-2020, ML-2032, LIR2032, LIR2020 with chemistry-specific charge voltages; added CR cell warning; added dtparam config.txt line with note that charging is OFF by default
- Updated pushbuttons: any momentary NO switch works, with common options and hole sizes
- Updated J2 power button: pogo pin no-solder method, Dupont jumper wires, hot glue for vibration resistance
- Added SHT40 mounting note (double-sided tape to nearby DIN-mounted component carrier tray)
- Added NO vs NC fail-safe explanation in PoE relay section
- Added Table of Contents
