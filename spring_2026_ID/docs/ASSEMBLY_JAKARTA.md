# Assembly Guide - Jakarta Site

**Site:** Jakarta, Indonesia (coastal/urban)
**Type:** AC-powered with 24hr UPS, 1x PoE camera
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
  - [Step 13: Mount Camera](#step-13-mount-camera-30-min)
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
- [ ] Configure Witty Pi 5 HAT+ wake/sleep schedule (CR2032 coin cell provides RTC)
- [ ] **Do NOT change timezone from UTC** — ORC-OS requires UTC (see REBOOT_CHECKLIST.md)
- [ ] Install and configure chrony as NTP server for camera network
- [ ] Format USB drive as ext4, mount at /mnt/usb, add to fstab
- ~~Configure vsftpd~~ — not needed; capture is via RTSP pull (orc-capture)
- [ ] Configure camera via camtool.py (1080p, 16Mbps CBR, IR-only, NTP from Pi)
- [ ] Insert and format MicroSD in camera, set recording to continuous (CMR)
- [ ] Test video capture pipeline (download 5s clip from camera SD via RTSP)
- [ ] Enable sensor logging (`orc-sensors.timer`) — see "Enable sensor logging service" section
- [ ] Verify SHT40 readings in `/var/log/orc/sensors/sht40_*.csv`
- [ ] Configure WiFi hotspot for maintenance mode
- [ ] Set up WS2812B status LED service (GPIO 18, config in /etc/orc/led-status.yaml)
- [ ] Pre-configure Telkomsel APN (if known)

### 2. Hardware Testing (Dry-Fit)

Assemble, wire, and test the complete system **before** conformal coating.
You need to verify all connections work and identify every contact point
that must be masked during coating.

- [ ] Test Pi 5 + Witty Pi 5 HAT+ + Geekworm G469 stack boots correctly (3-board stack)
- [ ] Verify USB flash drive is recognized
- [ ] Test LTE modem connects (with test SIM)
- [ ] Test PoE switch powers camera
- [ ] Test SHT40 sensor: `i2cdetect -y 1` shows 0x44, `orc-sensors` returns readings
- [ ] Verify WS2812B status LED cycles colors on GPIO 18
- [ ] Test relay switches PoE switch power on/off (GPIO 24)

### 3. Conformal Coating (After Testing, Before Travel)

Apply conformal coating only after the full system has been assembled, tested,
and verified working. This ensures you know exactly which contact points
need to be masked — coating over a connection you missed will cause failures
that are difficult to diagnose in the field.

**Do this in a low-humidity environment. Allow 24 hours cure time.**

**Boards to Coat:**
- [ ] Raspberry Pi 5
- [ ] Witty Pi 5 HAT+ PCB
- [ ] Geekworm G469 terminal block HAT

**Masking (Use Kapton tape on all contact points):**
- GPIO header pins (all 40 pins — Pi 5, Witty Pi 5, and G469)
- USB-A and USB-C ports
- HDMI ports
- Ethernet port
- MicroSD card slot
- Witty Pi 5 CR2032 battery holder
- J2 power button through-holes (or bolt terminals if installed)
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

Configure the ANNKE C1200 camera BEFORE deployment. The Pi acts as DHCP server on the camera network using dnsmasq, assigning a predictable IP to the camera.

**Note:** The SADP utility (Hikvision's camera discovery tool) does not run on ARM Macs — neither natively nor under Parallels. The dnsmasq approach below eliminates the need for SADP entirely.

**Note:** The ANNKE web interface requires a Windows-only browser plugin for live view. Use ISAPI snapshot to verify the camera image instead.

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
   ```
   **Important:** Use `bind-dynamic` (not `bind-interfaces`). This allows dnsmasq to start
   before eth0 has carrier — required because the PoE relay may not be on at boot time.
   Replace `<CAMERA_1_MAC>` with the camera's MAC address (printed on the camera label). If you don't have the MAC yet, omit the `dhcp-host` line, let the camera get any IP from the range, then check `cat /var/lib/misc/dnsmasq.leases` to find the MAC and update the config.

   Restart dnsmasq:
   ```bash
   sudo systemctl restart dnsmasq
   sudo systemctl enable dnsmasq
   ```

**Prepare USB storage:**

The USB flash drive stores camera uploads and ORC data. Format as ext4 and mount persistently.

1. Insert the USB flash drive into Pi 5 USB-A 3.0 port (blue).
2. Identify and unmount if auto-mounted:
   ```bash
   lsblk                    # find device (e.g. /dev/sda1)
   sudo umount /dev/sda1    # if auto-mounted
   ```
3. Format as ext4:
   ```bash
   sudo mkfs.ext4 -L orc-data /dev/sda1
   ```
4. Get the UUID and add to fstab:
   ```bash
   sudo blkid /dev/sda1     # copy UUID value
   sudo mkdir -p /mnt/usb
   echo 'UUID=<paste-uuid-here>  /mnt/usb  ext4  defaults,noatime,nofail  0  2' | sudo tee -a /etc/fstab
   ```
5. Mount and verify:
   ```bash
   sudo mount /mnt/usb
   df -h /mnt/usb
   ```
6. Create incoming directory and symlink `/home/pi/Videos` to USB:
   ```bash
   sudo mkdir -p /mnt/usb/incoming
   rmdir /home/pi/Videos
   ln -s /mnt/usb/incoming /home/pi/Videos
   ```
   ORC-OS watches `/home/pi/Videos` for incoming files. The symlink ensures
   video data is stored on the USB drive, not the OS SD card.

**Configure NTP server for camera time sync:**

The camera is on an isolated network with no internet. The Pi must serve NTP.

1. Install chrony:
   ```bash
   sudo apt install chrony -y
   ```
2. Deploy the camera-net NTP config:
   ```bash
   sudo mkdir -p /etc/chrony/conf.d
   sudo cp pi/shared/etc/chrony/conf.d/camera-net.conf /etc/chrony/conf.d/
   sudo systemctl restart chrony
   sudo systemctl enable chrony
   ```
3. **Timezone: leave as UTC (do NOT change).**
   ORC-OS requires UTC. Changing to a regional timezone (e.g. Asia/Jakarta)
   breaks the ORC API's timestamp parsing. Verify with:
   ```bash
   timedatectl | grep "Time zone"   # should show Etc/UTC or GMT
   ```

**~~FTP server setup~~ — REMOVED:**

> FTP server (vsftpd) is not needed. Video capture uses RTSP pull via the
> `orc-capture` script, not camera FTP push. See ISS-003 in ISSUE_LOG.md.

**Configure each camera:**

1. Connect camera to PoE switch, connect switch uplink port to Pi Ethernet
2. Wait 60-90 seconds for camera to boot and receive DHCP lease
3. Verify: `ping 192.168.50.101`
4. Access web interface at `http://192.168.50.101` (default credentials: admin / admin)
5. Test ISAPI snapshot (works on macOS/Linux without plugins):
   ```bash
   curl --digest -u admin:password http://192.168.50.101/ISAPI/Streaming/channels/101/picture -o cam1_test.jpg
   ```

- [ ] Change admin password (record in secure location — must match `CAMERA_PASSWORD` in `.env`)
- [ ] Set camera to DHCP so it picks up the dnsmasq-assigned address on every boot
- [ ] Insert MicroSD card into camera (required for local recording)
- [ ] Format MicroSD via ISAPI:
  ```bash
  curl --digest -u admin:<password> -X PUT \
    http://192.168.50.101/ISAPI/ContentMgmt/Storage/hdd/1/format
  ```
- [ ] Push camera config via camtool.py:
  ```bash
  python3 camtool.py push jakarta-cam1
  ```
  This sets: 1920x1080 H.264 at 16 Mbps CBR, 12.5fps, audio off, IR-only
  illumination, motion detection off, NTP from Pi, UTC timezone.

  > **Warning — supplement light reverts on power cycle:** The ANNKE C1200
  > resets `supplementLightMode` from `irLight` to `eventIntelligence` after
  > every reboot, causing bright white LED flashes. The `orc-capture` script
  > re-applies `irLight` automatically on each wake cycle. If testing manually,
  > verify with: `curl --digest -u admin:<password> http://<cam-ip>/ISAPI/Image/channels/1 | grep supplementLightMode`

- [ ] Set recording schedule to continuous (CMR):
  ```bash
  curl --digest -u admin:<password> \
    http://192.168.50.101/ISAPI/ContentMgmt/record/tracks/101 > /tmp/track.xml
  sed -i 's/ActionRecordingMode>MOTION/ActionRecordingMode>CMR/g' /tmp/track.xml
  curl --digest -u admin:<password> -X PUT \
    -H "Content-Type: application/xml" -d @/tmp/track.xml \
    http://192.168.50.101/ISAPI/ContentMgmt/record/tracks/101
  ```
- [ ] Verify configs: `python3 camtool.py diff jakarta-cam1`
- [ ] Test video capture pipeline (download 5s clip from SD via RTSP playback):
  ```bash
  START=$(date -d '15 seconds ago' +%Y%m%dT%H%M%S)
  ffmpeg -y -rtsp_transport tcp \
    -i "rtsp://admin:<password>@192.168.50.101:554/Streaming/tracks/101?starttime=${START}" \
    -t 5 -c:v copy -an /mnt/usb/incoming/test_cam1.mp4
  ffprobe /mnt/usb/incoming/test_cam1.mp4  # verify 1080p, ~16 Mbps
  ```
- [ ] Verify camera records and downloads correctly
- [ ] Verify IR function: cover lens, IR LEDs should illuminate, download clip shows grayscale

**Enable capture service:**

Deploy and enable `orc-capture`, which handles PoE relay control and video
capture on each boot cycle. The ORC-OS `orc-gpio-relays` service must stay
disabled (active-low/active-high incompatibility with our relay module).

```bash
sudo cp pi/shared/usr/local/bin/orc-capture /usr/local/bin/orc-capture
sudo chmod +x /usr/local/bin/orc-capture
sudo cp pi/shared/etc/systemd/system/orc-capture.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable orc-capture
sudo systemctl disable orc-gpio-relays
```

- [ ] `orc-capture` service enabled
- [ ] `orc-gpio-relays` service disabled
- [ ] Test: `poe-relay off && orc-capture --dry-run` completes with quality gate PASS

**Enable sensor logging service:**

Deploy and enable `orc-sensors`, which reads the SHT40 temperature/humidity
sensor (and any future sensors) on a configurable interval and appends readings
to daily CSV files.

```bash
sudo mkdir -p /etc/orc-sensors /usr/local/lib/orc-sensors /var/log/orc/sensors
sudo cp pi/shared/etc/orc-sensors/sht40.conf /etc/orc-sensors/
sudo cp pi/shared/usr/local/bin/orc-sensors /usr/local/bin/
sudo chmod +x /usr/local/bin/orc-sensors
sudo cp pi/shared/usr/local/lib/orc-sensors/sensors_logger.py /usr/local/lib/orc-sensors/
sudo cp pi/shared/etc/systemd/system/orc-sensors.service /etc/systemd/system/
sudo cp pi/shared/etc/systemd/system/orc-sensors.timer /etc/systemd/system/
sudo chown pi:pi /var/log/orc/sensors
sudo systemctl daemon-reload
sudo systemctl enable orc-sensors.timer
sudo systemctl start orc-sensors.timer
```

- [ ] `orc-sensors.timer` enabled and started
- [ ] Test: `orc-sensors` produces CSV at `/var/log/orc/sensors/sht40_*.csv`
- [ ] `systemctl list-timers orc-sensors.timer` shows next activation

---

## Component Inventory

### Compute Stack
- [ ] Raspberry Pi 5 8GB (coated)
- [ ] Witty Pi 5 HAT+ (coated) — RTC with CR2032 coin cell, I2C (0x51), passes through all 40 GPIO pins
- [ ] Geekworm G469 terminal block HAT (coated)
- [ ] SanDisk 256GB USB flash drive
- [ ] MicroSD card 64GB (with OS)
- [ ] Active cooler for Pi 5
- [ ] CR2032 coin cell for Witty Pi 5 HAT+ RTC
- [ ] 16mm standoffs (for 3-board stack: Pi 5 bottom, Witty Pi 5 middle, G469 top)

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
- [ ] Blade fuse holders + fuses (5A, 15A)

### Camera System
- [ ] ANNKE C1200 PoE camera (x1, factory-sealed IP67)
- [ ] LINOVISION Industrial PoE Switch (Gigabit, 12V DC input)
- [ ] Electronics-Salon 4-channel SPDT DIN Rail relay module (GPIO-triggered via G469)
- [ ] Cat6 outdoor shielded cables, 10ft pre-terminated (x2: 1 internal patch + 1 external to camera)
- [ ] CNLINKO weatherproof ethernet bulkhead, IP67 (x1)
- [ ] Camera pole mount bracket (x1)

### Humidity Control & Climate Monitoring
- [ ] PTC heater 15W (for enclosure)
- [ ] SHT40 temperature/humidity sensor (I2C, inside enclosure)
- [ ] DS18B20 waterproof temperature probe (1-Wire, outside enclosure)
- [ ] Amphenol Gore vents, IP68 (x2)
- [ ] 40 CFM fans (x2, for internal air circulation)

### User Interface
- [ ] WS2812B (NeoPixel) individual RGB pixel PCB (1 per site)
- [ ] Clear cast acrylic sheet (small offcuts, ~2-3mm thick)
- [ ] Clear neutral-cure silicone sealant (GE Silicone II or equivalent — NOT acetoxy)
- [ ] 1x momentary pushbutton, normally open (power). Any panel-mount momentary NO switch works — common options include Gebildet 16mm stainless (Amazon, ~$9, IP67), C&K AP Series (~$12, IP67), or generic 12mm metal momentary (~$3-5, IP65-67). Match hole size to the button you purchase.

### Enclosure & Mounting
- [ ] VEVOR NEMA 4x enclosure (16"x12"x8")
- [ ] DIN rail 35mm (x2)
- [ ] DIN rail clips
- [ ] CNLINKO weatherproof ethernet bulkhead (x1, for camera)
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
   - Bottom rail: AC power — surge suppressor, AC terminal blocks (L/N/PE), Mean Well PSU
   - Top rail: 12V DC — TB1 distribution block, fuse holders, DDR-60G-5, relay, PoE switch, Pi stack
   - Leave clearance for cable routing between rails

### Step 4: Assemble Compute Stack (15 min)

1. **Stack order (bottom to top):**
   ```
   [Raspberry Pi 5]         (bottom)
        |
   [Witty Pi 5 HAT+]       (middle — RTC, CR2032, I2C 0x51)
        |
   [Geekworm G469 HAT]     (top — screw terminals)
   ```
   3-board stack with 16mm standoffs. The Witty Pi 5 HAT+ passes through all
   40 GPIO pins, so the G469 terminal block HAT works unchanged on top.

   **Why Witty Pi 5 instead of Pi 5 built-in RTC:** The Pi 5 ML-2020 battery
   connector (J5) broke on both Sukabumi and Jakarta boards — the Molex
   connector cannot handle any mechanical stress. The Witty Pi 5 uses a
   standard CR2032 coin cell holder, which is far more robust.

2. Install active cooler on Pi 5

3. **Install RTC battery:**
   Insert a CR2032 coin cell into the Witty Pi 5 HAT+ battery holder.
   Standard non-rechargeable CR2032 — the Witty Pi 5 does not trickle-charge
   the battery. No `config.txt` changes needed for the RTC battery.

4. Seat Witty Pi 5 HAT+ onto Pi 5 GPIO header, secure with 16mm standoffs

5. Seat Geekworm G469 onto Witty Pi 5 header, press down firmly, secure with standoffs

6. Mount stack on lower DIN rail using DIN rail clip

### Step 5: Mount Components on DIN Rails (30 min)

**Tools needed:** Screwdriver, DIN rail clips

1. **Bottom DIN rail (AC power — already mounted in Step 6):**
   - AC terminal blocks (L/N/PE, bridged pairs)
   - Heschen HS-40-N surge suppressor
   - Mean Well SDR-120-12 PSU

2. **Top DIN rail (12V DC distribution):**
   - Terminal block TB1 (12V distribution)
   - Fuse holders (F1-F4)
   - DDR-60G-5 buck converter
   - Electronics-Salon relay module
   - LINOVISION PoE switch
   - Pi stack (from Step 4)

3. **Mount items without DIN rail clips:**
   - Quectel modem: sits inside the EXVIST WWAN USB carrier, which is
     Velcro/Dual-Lock attached to a DIN rail clip
   - SHT40 breakout board: double-sided tape to a nearby DIN-mounted
     component's carrier tray or flat surface. Position away from heat
     sources (Pi CPU, DC-DC converters) for accurate readings.

### Step 6: Install Power System (45 min)

**Tools needed:** Screwdriver, wire strippers

**AC wire spec:** Use **2.5 mm² (14 AWG) stranded** wire for all AC mains wiring
inside the enclosure (L, N, and PE runs between terminal blocks, PSU, and surge
suppressor). This meets IEC 60364 and Indonesian SNI 04-0225 standards for
circuits up to 20A at 220V. Do not use wire thinner than 1.5 mm² (16 AWG) for
any AC connection.

**AC wire colors:** Use the IEC standard colors — **brown** for L (line),
**blue** for N (neutral), **green/yellow** for PE (ground). Do not use tape
to re-color wire — tape peels in tropical humidity and someone servicing the
box will see the base color and make wrong assumptions. If you don't have
the correct color, use bare copper for PE (acceptable inside an enclosure)
and get proper colored wire before final assembly. Never use red or black
for AC wiring — those are reserved for DC 12V and DC ground.

**DC wire spec:** Use solid core wire (18-22 AWG) for all 12V DC internal DIN
rail wiring (same as Sukabumi).

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

7. **First AC power-on test:**
   - Plug in AC cord
   - Mean Well PSU green LED should light
   - No sparks, smoke, or buzzing
   - Measure DC output: V+ to V- should read ~12V (expect 12.0-12.2V)
   - Unplug AC cord before proceeding

8. **Wire 12V distribution (PSU to TB1):**

   Run two wires from the Mean Well PSU DC output (bottom rail) up to TB1
   (top rail):

   | Wire | From | To | Color | Gauge |
   |------|------|----|-------|-------|
   | 1 | PSU V+ (12V) | TB1 12V+ | Red | 18 AWG solid |
   | 2 | PSU V- (GND) | TB1 GND | Black | 18 AWG solid |

9. **12V distribution continuity checks:**

   With AC cord **unplugged**:

   **Should beep:**
   - [ ] PSU V+ ↔ TB1 12V+ — beep
   - [ ] PSU V- ↔ TB1 GND — beep

   **Should NOT beep:**
   - [ ] TB1 12V+ ↔ TB1 GND — **NO beep**
   - [ ] TB1 12V+ ↔ L terminal block — **NO beep** (AC/DC isolation)
   - [ ] TB1 12V+ ↔ N terminal block — **NO beep** (AC/DC isolation)
   - [ ] TB1 12V+ ↔ PE terminal block — **NO beep** (DC ground is floating)
   - [ ] TB1 GND ↔ PE terminal block — **NO beep** (DC ground is NOT connected to AC earth)

   **The last two checks are critical — they verify that DC ground and AC
   earth are separate. If TB1 GND beeps to PE, you have a ground fault
   that must be fixed before proceeding.**

10. **Second power-on test (verify 12V at TB1):**
    - Plug in AC cord
    - Measure DC at TB1: 12V+ to GND should read ~12V
    - Unplug AC cord before proceeding to downstream wiring

11. **Wire battery system (deferred — battery sourced in-country):**
    ```
    Mean Well 12V+ --+---> Charger input (+)
                      |
                      +---> Terminal block TB1 (system 12V+)

    Charger output ---> Battery (+)
    Battery (+) ---> Terminal block TB1 (backup 12V+)
    Battery (-) ---> Terminal block TB1 (system GND)
    ```
    Battery BMS handles low-voltage cutoff automatically.

12. **Wire DDR-60G-5 buck converter:**

    **Input (12V from TB1 through fuse):**

    | Wire | From | To | Color | Gauge |
    |------|------|----|-------|-------|
    | 1 | TB1 12V+ | Fuse holder input (F3) | Red | 18 AWG solid |
    | 2 | Fuse holder output (F3) | DDR-60G-5 V+ input | Red | 18 AWG solid |
    | 3 | TB1 GND | DDR-60G-5 V- input | Black | 18 AWG solid |

    **Trim output voltage:**
    - Install 5A fuse in F3
    - Power on AC
    - Measure DDR-60G-5 output with multimeter — adjust trim pot to **5.10V**
    - Power off AC

    **Output (5V to Pi via G469):**

    | Wire | From | To | Color | Gauge |
    |------|------|----|-------|-------|
    | 4 | DDR-60G-5 V+ output | G469 Pin 2 (5V) | Yellow | 18 AWG solid |
    | 5 | DDR-60G-5 V- output | G469 Pin 25 (GND) | Black | 18 AWG solid |

    **Continuity checks (AC unplugged):**

    Should beep:
    - [ ] TB1 12V+ ↔ Fuse holder input — beep
    - [ ] Fuse holder output ↔ DDR-60G-5 V+ input — beep
    - [ ] TB1 GND ↔ DDR-60G-5 V- input — beep
    - [ ] DDR-60G-5 V+ output ↔ G469 Pin 2 — beep
    - [ ] DDR-60G-5 V- output ↔ G469 Pin 25 — beep

    Should NOT beep:
    - [ ] G469 Pin 2 ↔ G469 Pin 25 — **NO beep**
    - [ ] TB1 12V+ ↔ G469 Pin 2 — **NO beep** (12V/5V isolation)
    - [ ] DDR-60G-5 V+ input ↔ V- input — **NO beep**

13. **Fuse summary (3 fuse holders):**
    - F2: 5A — PoE relay/switch feed
    - F3: 5A — Pi/DDR-60G-5 feed (already installed)
    - F4: 5A — Heater/fan feed

### Step 7: Wire Relay Module and PoE System (30 min)

**Wire spec:** Use solid core wire (18-22 AWG) for all internal DIN rail wiring.

**Wire routing:** Route all DC low-voltage wires (5V, GPIO signals) **over the
top of the upper DIN rail**. Keep them physically separated from the AC mains
wiring that runs between the two rails. This prevents accidental contact
between AC and DC during service and makes it easy to visually trace each
domain.

1. **Wire relay module input side (via Geekworm G469 terminals):**

   | Wire | From (G469) | To (Relay) | Color | Gauge |
   |------|-------------|------------|-------|-------|
   | 6 | Pin 4 — 5V | VCC | Yellow | 22 AWG solid |
   | 7 | Pin 20 — GND | GND | Black | 22 AWG solid |
   | 8 | Pin 18 — GPIO 24 | IN1 (PoE) | Blue | 22 AWG solid |

   Only relay channel CH1 (PoE switch) is wired. Channels CH2-CH4
   are unused and available for future expansion.

   **Relay input continuity checks (AC unplugged):**

   Should beep:
   - [ ] G469 Pin 4 ↔ Relay VCC — beep
   - [ ] G469 Pin 20 ↔ Relay GND — beep
   - [ ] G469 Pin 18 ↔ Relay IN1 — beep

   Should NOT beep:
   - [ ] Relay VCC ↔ Relay GND — **NO beep**
   - [ ] Relay IN1 ↔ VCC or GND — **NO beep**

2. **Wire PoE switch power through fuse and relay:**
   - 12V+ from TB1 -> inline fuse (5A) -> relay CH1 COM input
   - Relay CH1 NO output -> LINOVISION PoE switch 12V+ input
   - TB1 GND -> PoE switch GND input

   **Why NO (Normally Open) instead of NC (Normally Closed):** Using NO is a
   deliberate fail-safe. If the Pi crashes, hangs, or fails to shut down
   cleanly, GPIO pins float LOW and the relay falls open. The PoE switch and
   camera **loses power automatically**, preventing the system's largest power
   consumer from draining the battery. With NC, a Pi crash would leave the
   camera powered indefinitely, which could drain the UPS battery and leave
   the station non-functional until someone physically visits the site. The
   ~15-20 second delay (Pi boots -> GPIO HIGH -> relay closes -> camera begins
   booting) is an acceptable tradeoff for this protection.

3. **Connect Ethernet cables:**
   - Short patch cable: PoE switch uplink port -> Pi 5 Ethernet
   - PoE Port 1 -> internal Cat6 patch cable (connects to CNLINKO bulkhead later)

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
5. **WS2812B status LED:** Wire from Geekworm G469 to WS2812B NeoPixel:
     - 5V (Pin 2) -> WS2812B VDD
     - GND (Pin 14) -> WS2812B GND
     - GPIO 18 (Pin 12) -> WS2812B DIN (data in)
6. **Relay GPIO:** Already wired in Step 7 (VCC, GND, IN1 from G469)

### Step 9: Test Mounting Plate Assembly

Power on and verify the complete mounting plate assembly works before
proceeding to enclosure work. This is your last chance to fix wiring issues
before final assembly.

- [ ] 12V supply -> DDR-60G-5 -> Pi boots
- [ ] GPIO 24 -> relay CH1 -> PoE switch powers on
- [ ] Camera boots and is reachable via Pi
- [ ] Video capture from camera SD to /mnt/usb/incoming works
- [ ] LTE modem detected
- [ ] SHT40 sensor readable via I2C
- [ ] DS18B20 temperature probe readable
- [ ] WS2812B status LED lights up on GPIO 18 (test with led-status service)
- [ ] All connections secure, no loose wires

**Once the mounting plate assembly is fully tested, proceed to enclosure
preparation.**

---

### Step 10: Prepare Enclosure and Install Bulkheads

**Do not drill the enclosure until the mounting plate assembly is tested.**
**Drill all holes with the mounting plate removed** — avoids metal shavings
landing on wired components. (See Sukabumi build note in ASSEMBLY_SUKABUMI.md.)

**Tools needed:** Drill, sized drill bits or hole saws, step bit (backup), marker

> **Drilling tip:** Use a sized drill bit or hole saw matched to each hole
> diameter whenever possible. Step bits are convenient but it's easy to
> overshoot by one step, and an oversized hole means a sloppy gasket seal.
> Bulkhead connectors, Gore vents, and antenna mounts all rely on a snug
> fit to maintain IP rating — slop is the enemy. If you have access to a
> drill press or a drill guide, use it.

1. **Mark hole positions:**
   - 2x M12 holes for Gore vents
   - 1x 12mm hole for Proxicast puck antenna (enclosure top)
   - 1x hole for CNLINKO ethernet bulkhead (camera cable)
   - 1x hole for SP13 AC mains input bulkhead (220V AC input)
   - 1x M16 hole for ground cable
   - 2x holes for 40 CFM fans
   - 1× 10-12mm hole for status LED light window
   - 1x hole for power button — hole size depends on
     the button you purchased (12mm, 16mm, 19mm, or 22mm are common)
   - 1x 16mm hole for rain gauge SD16 bulkhead connector
   - 1x PG9 hole for DS18B20 temperature probe

2. **Drill holes:**
   - Use step bit for clean cuts
   - Deburr all holes
   - Test-fit all bulkheads, glands, and vents

3. **Install bulkheads and glands:**
   - Gore M12 vents (hand-tight plus 1/4 turn, position for cross-ventilation)
   - SP13 AC mains input bulkhead
   - CNLINKO ethernet bulkhead (x1)
   - SD16 4-pin bulkhead connector for rain gauge

4. **Install status LED light window:**

   Same silicone-filled acrylic sandwich procedure as Sukabumi — see
   ASSEMBLY_SUKABUMI.md Step 8 item 3 for the detailed procedure.

   Single WS2812B NeoPixel, 1 GPIO data pin, 5V power. No relay channels
   used — all relay channels remain free for future use.

5. **Install power button:**
   - Install power button, secure with nut
   - Label power button clearly as "POWER"

6. **Wire external power button to Pi 5 J2 header:**

   J2 is a dedicated 2-pin power button header on the Pi 5, located near the
   USB-C port. This is NOT a GPIO pin — it is hardware-level power control.

   **J2 connector:** J2 is **unpopulated** — it's two bare through-holes at
   2.54mm pitch on the Pi 5 board.

   **Bolt-through method (recommended):** Use small bolts through the J2
   through-holes with O-ring terminal crimps on 18 AWG solid wire. This is
   mechanically robust, requires no soldering, and holds up well to vibration.

   **Hardware:** The J2 through-holes are standard PCB size (~1.0mm). Use
   **M1.6 bolts** (1.6mm shaft) or **#0-80 bolts** (1.52mm, US equivalent)
   with matching nuts and washers. Verify fit on your board before buying in
   quantity — bring the Pi to the hardware store if possible.

   **O-ring terminals:** Use crimp-on O-ring (ring) terminals sized for the
   bolt diameter (M1.6 or #0) and rated for 18 AWG wire.

   1. Insert a small bolt through each J2 through-hole from the bottom of
      the board
   2. Crimp an O-ring terminal onto each 18 AWG solid wire
   3. Place the O-ring terminal over the bolt on the top side of the board
   4. Secure with a nut — finger-tight plus a quarter turn (don't overtorque
      and crack the PCB)
   5. Route the wires to the external power button's screw terminals

   **Alternative:** Solder a standard 2-pin 2.54mm header into J2.

   Polarity does not matter (momentary short between the two pins).

   Behavior:
   - Brief press powers on (from halted)
   - Brief press initiates clean shutdown (while running)
   - ~10s hold forces power off (if frozen)

### Step 11: Install Mounting Plate and Connect External Peripherals

1. **Install mounting plate** into enclosure with provided screws

2. **Install CNLINKO ethernet bulkheads:**
   - Connect internal Cat6 patch cable from PoE switch port to bulkhead
   - External Cat6 cable connects to camera

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

### Step 13: Mount Camera (30 min)

1. **Install camera bracket** on pole:
   - Position for optimal river view
   - Use stainless U-bolts

2. **Mount camera:**
   - Attach camera to bracket
   - Connect Cat6 cable to CNLINKO bulkhead exterior connector
   - Aim and focus camera

3. **Protect connections:**
   - CNLINKO bulkhead provides IP67 weatherproofing
   - Secure cables with UV-resistant ties

### Step 14: Mount Rain Gauge (20 min)

1. **Mount Hydreon RG-15** on pole (separate from camera)
   - Built-in mounting holes, no separate bracket needed
2. **Mount with dome facing up**, away from overhanging surfaces that could drip onto it (no leveling needed — the RG-15 is optical, not a tipping bucket)
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
3. WS2812B status LED should indicate (colors configured in /etc/orc/led-status.yaml):
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

### Verify Camera

1. Enter maintenance mode (long press power button, 3 seconds)
2. Connect laptop to WiFi hotspot
3. SSH into Pi
4. Ping camera:
   ```
   ping 192.168.50.101
   ```
5. Test video capture:
   ```bash
   START=$(date -d '15 seconds ago' +%Y%m%dT%H%M%S)
   ffmpeg -y -rtsp_transport tcp \
     -i "rtsp://admin:PASSWORD@192.168.50.101:554/Streaming/tracks/101?starttime=${START}" \
     -t 5 -c:v copy -an /mnt/usb/incoming/test_cam1.mp4
   ffprobe /mnt/usb/incoming/test_cam1.mp4  # verify 1080p, ~16 Mbps
   ```

### Verify LTE Connection

1. Check modem: `mmcli -L`
2. Check signal: `mmcli -m 0 --signal-get`
3. Test data: `ping -c 3 8.8.8.8`

### Optional: Install Tailscale (Remote Access)

Tailscale provides secure remote SSH access over LTE without port forwarding or
a public IP. Useful for field maintenance and troubleshooting.

1. Install: `curl -fsSL https://tailscale.com/install.sh | sh`
2. Authenticate: `sudo tailscale up --ssh`
3. Follow the login URL to authorize the device on your tailnet
4. Verify: `tailscale status` — node should appear as online
5. Test remote SSH from another device on the same tailnet

The Pi will be reachable by its Tailscale hostname (e.g., `ssh pi@orc-jakarta`)
from any device on your tailnet, regardless of LTE carrier NAT.

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
| PoE camera (x1) | ~8W | |
| PoE switch | ~5W | |
| Modem (idle) | ~1W | |
| PTC heater (avg) | ~8W | |
| Fans (x2) | ~3W | |
| **Total average** | **~33W** | |

**Battery runtime:** 1280Wh / 33W = ~39 hours (theoretical)

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
| Camera IP | 192.168.50.101 |
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

**Document Version:** 3.2
**Last Updated:** April 3, 2026
**Changes from v3.1:**
- Reinstated Witty Pi 5 HAT+ — Pi 5 ML-2020 battery connector (J5) broke on both boards
- Stack reverted to 3-board: Pi 5 (bottom) + Witty Pi 5 HAT+ (middle) + G469 (top) with 16mm standoffs
- RTC now uses Witty Pi 5 CR2032 coin cell (I2C 0x51) instead of Pi 5 built-in RTC
- Removed Pi 5 RTC battery charging config (dtparam=rtc_bbat_vchg) — not needed with Witty Pi
- Removed rechargeable ML/LIR battery from parts list; replaced with CR2032
- Added Witty Pi 5 HAT+ PCB to conformal coating list
- Updated masking list: Witty Pi CR2032 holder replaces J5 (BAT) connector

**Changes from v3.0:**
- Reduced Jakarta from 2 cameras to 1 camera (matches project decision)
- Reduced CNLINKO ethernet bulkheads from 2 to 1
- Reduced Cat6 cables from 4 to 2 (1 internal patch + 1 external to camera)
- Reduced camera pole mount brackets from 2 to 1
- Reduced PoE fuse F2 from 10A to 5A (1 camera draws less current)
- Removed Camera 2 IP (192.168.50.102) and second dhcp-host line from dnsmasq config
- Updated power budget: camera power ~8W (was ~15W for 2), total ~33W (was ~40W), battery runtime ~39hr (was ~32hr)
- Updated all verification steps to single-camera language

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
