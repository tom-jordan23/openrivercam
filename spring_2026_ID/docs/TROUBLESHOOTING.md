# Troubleshooting Guide - Indonesia ORC Sites

**Applies to:** Sukabumi and Jakarta sites
**Audience:** Field technicians, PMI staff

---

## Quick Reference - Status LEDs

| LED Pattern | Meaning | Action |
|-------------|---------|--------|
| Green steady | System OK, idle | Normal operation |
| Green + Yellow blink | Capturing/uploading | Normal operation |
| Yellow steady | Processing | Wait for completion |
| Red blink | Warning (non-critical) | Check logs when convenient |
| Red steady | Error (needs attention) | Investigate immediately |
| All off | No power or not booted | Check power system |
| All on steady | Boot in progress | Wait 2-3 minutes |

---

## Diagnostic Flowcharts

### System Won't Power On

```
START: No status LEDs lit
         │
         ▼
    Check power source
    ┌─────────────────┐
    │ Sukabumi: Solar │
    │ Jakarta: AC     │
    └────────┬────────┘
             │
             ▼
┌────────────────────────────┐
│ Measure voltage at input   │
│ terminals (should be >11V) │
└────────────┬───────────────┘
             │
      ┌──────┴──────┐
      │             │
   <11V          >11V
      │             │
      ▼             ▼
┌──────────┐  ┌──────────────────┐
│ SUKABUMI │  │ Check fuses      │
│ Check    │  │ (main, Pi feed)  │
│ solar    │  └────────┬─────────┘
│ battery  │           │
└──────────┘     ┌─────┴─────┐
                 │           │
              Blown       OK
                 │           │
                 ▼           ▼
           Replace    ┌────────────────┐
           fuse       │ Check Witty Pi │
                      │ power LED      │
                      └───────┬────────┘
                              │
                        ┌─────┴─────┐
                        │           │
                      Off          On
                        │           │
                        ▼           ▼
                  ┌──────────┐  ┌──────────────┐
                  │ Check    │  │ Check Pi     │
                  │ USB-C    │  │ activity LED │
                  │ power    │  │ (should      │
                  │ cable    │  │ flash)       │
                  └──────────┘  └──────────────┘
```

### Pi eth0 Has Only IPv6 Address (No IPv4)

If `ip addr` shows only an `inet6` (IPv6) address on eth0 with no `inet` (IPv4) address, the Pi cannot reach the camera.

**Symptoms:**
- `ping <camera-ip>` fails with "Network is unreachable"
- `ip addr show eth0` shows `fe80::...` link-local IPv6 but no `192.168.x.x`

**Cause:** The Pi's Ethernet interface hasn't been assigned a static IPv4 address and dnsmasq hasn't been configured yet. Without a static IP, the Pi can't serve DHCP to cameras on the 192.168.50.0/24 network.

**Fix — assign a static IPv4 address and set up dnsmasq:**

Using NetworkManager (Raspberry Pi OS Bookworm):
```bash
# Set static IP on eth0
sudo nmcli con mod "Wired connection 1" ipv4.addresses 192.168.50.1/24
sudo nmcli con mod "Wired connection 1" ipv4.method manual
sudo nmcli con up "Wired connection 1"

# Verify
ip addr show eth0   # should now show 192.168.50.1
```

If the connection name differs, find it with:
```bash
nmcli con show
```

Then install and configure dnsmasq as DHCP server for cameras — see the assembly guide for your site (ASSEMBLY_SUKABUMI.md or ASSEMBLY_JAKARTA.md) for the full dnsmasq configuration.

This persists across reboots. The Pi acts as DHCP server on the camera network (192.168.50.0/24), assigning predictable IPs to each camera via MAC address reservation.

---

### Camera Not Working

#### Sukabumi (PoE Camera - Power-Cycled)

```
START: No video capture
         │
         ▼
┌─────────────────────────┐
│ Ping camera from Pi:    │
│ ping 192.168.50.139     │
│ (or configured IP)      │
└───────────┬─────────────┘
            │
     ┌──────┴──────┐
     │             │
  No reply      Reply OK
     │             │
     ▼             ▼
┌──────────────┐  ┌────────────────────┐
│ Check PoE    │  │ Test RTSP:         │
│ injector:    │  │ ffmpeg -i rtsp://  │
│ - 12V input? │  │ admin:pass@        │
│ - LED on?    │  │ 192.168.50.139:554/│
└──────┬───────┘  │ stream1 -frames:v 1│
       │          │ test.jpg           │
  ┌────┴────┐     └─────────┬──────────┘
  │         │               │
No LED    LED on      ┌─────┴─────┐
  │         │         │           │
  ▼         ▼       Fails      Success
┌─────┐  ┌────────┐   │           │
│Check│  │Check   │   ▼           ▼
│12V  │  │Cat6    │ ┌───────┐  ┌────────┐
│fuse │  │cable & │ │Check  │  │Camera  │
│& PoE│  │RJ45    │ │camera │  │OK,     │
│injec│  │connect-│ │creds &│  │check   │
│power│  │ions    │ │RTSP   │  │ORC     │
└─────┘  └────────┘ │config │  │config  │
                    └───────┘  └────────┘

NOTE: Camera takes ~45-60s to boot after Pi wakes.
Wait before testing if system just powered on.
```

#### Jakarta (PoE Cameras)

```
START: Camera offline
         │
         ▼
┌─────────────────────────┐
│ Ping camera from Pi:    │
│ ping 192.168.50.101     │
└───────────┬─────────────┘
            │
     ┌──────┴──────┐
     │             │
  No reply      Reply OK
     │             │
     ▼             ▼
┌──────────────┐  ┌────────────────────┐
│ Check PoE    │  │ Test RTSP:         │
│ injector LED │  │ ffmpeg -i rtsp://  │
│ and camera   │  │ admin:pass@        │
│ power LED    │  │ 192.168.50.101:554/│
└──────┬───────┘  │ stream1 -frames:v 1│
       │          │ test.jpg           │
  ┌────┴────┐     └─────────┬──────────┘
  │         │               │
No LED    LED on      ┌─────┴─────┐
  │         │         │           │
  ▼         ▼       Fails      Success
┌─────┐  ┌────────┐   │           │
│Check│  │Check   │   ▼           ▼
│12V  │  │Cat6    │ ┌───────┐  ┌────────┐
│to   │  │cable   │ │Check  │  │Camera  │
│PoE  │  │continu-│ │camera │  │OK,     │
│injec│  │ity     │ │creds &│  │check   │
│tor  │  └────────┘ │RTSP   │  │ORC     │
└─────┘             │config │  │config  │
                    └───────┘  └────────┘
```

### No LTE Connectivity

```
START: No data connection
         │
         ▼
┌────────────────────────────┐
│ Check modem detected:      │
│ mmcli -L                   │
└───────────┬────────────────┘
            │
     ┌──────┴──────┐
     │             │
  No modem     Modem found
     │             │
     ▼             ▼
┌──────────┐  ┌────────────────────┐
│ Check    │  │ Check SIM:         │
│ USB      │  │ mmcli -m 0         │
│ connection│ │ Look for SIM state │
│ Run:     │  └─────────┬──────────┘
│ lsusb    │            │
└──────────┘     ┌──────┴──────┐
                 │             │
              No SIM        SIM OK
                 │             │
                 ▼             ▼
           ┌──────────┐  ┌────────────────┐
           │ Check    │  │ Check signal:  │
           │ SIM      │  │ mmcli -m 0     │
           │ inserted │  │ --signal-get   │
           │ properly │  └────────┬───────┘
           └──────────┘           │
                           ┌──────┴──────┐
                           │             │
                        No signal    Has signal
                           │             │
                           ▼             ▼
                     ┌──────────┐  ┌────────────┐
                     │ Check    │  │ Check APN: │
                     │ antenna  │  │ May need   │
                     │ connect- │  │ Telkomsel  │
                     │ ions     │  │ APN config │
                     └──────────┘  └────────────┘
```

### IR Light Not Working (Sukabumi Only)

```
START: No IR illumination at night
         │
         ▼
┌─────────────────────────────┐
│ Cover Tendelux photocell    │
│ with hand (simulate dark)   │
└───────────┬─────────────────┘
            │
     ┌──────┴──────┐
     │             │
  IR off        IR on
     │             │
     ▼             ▼
┌──────────────┐  ┌────────────┐
│ Check relay  │  │ Photocell  │
│ - Listen for │  │ working,   │
│   click on   │  │ check      │
│   Pi boot    │  │ threshold  │
└──────┬───────┘  │ adjustment │
       │          └────────────┘
  ┌────┴────┐
  │         │
No click  Click heard
  │         │
  ▼         ▼
┌─────────┐ ┌──────────────────┐
│ Check   │ │ Check 12V to IR: │
│ USB     │ │ Measure voltage  │
│ relay   │ │ at Tendelux      │
│ power & │ │ terminals        │
│ control │ └────────┬─────────┘
└─────────┘          │
              ┌──────┴──────┐
              │             │
           No 12V        12V OK
              │             │
              ▼             ▼
        ┌──────────┐  ┌──────────┐
        │ Check    │  │ Tendelux │
        │ fuse in  │  │ may be   │
        │ IR       │  │ faulty,  │
        │ circuit  │  │ replace  │
        └──────────┘  └──────────┘
```

### Rain Gauge Not Reporting

```
START: No rain data
         │
         ▼
┌────────────────────────────┐
│ I2C scan:                  │
│ i2cdetect -y 1             │
└───────────┬────────────────┘
            │
     ┌──────┴──────┐
     │             │
  Not found     Found at address
     │             │
     ▼             ▼
┌──────────────┐  ┌────────────────┐
│ Check wiring │  │ Test reading:  │
│ VCC: 3.3V    │  │ (use library   │
│ GND: Ground  │  │ test script)   │
│ SDA: GPIO 2  │  └────────┬───────┘
│ SCL: GPIO 3  │           │
└──────────────┘     ┌─────┴─────┐
                     │           │
                  No data     Data OK
                     │           │
                     ▼           ▼
               ┌──────────┐  ┌────────────┐
               │ Manually │  │ Check ORC  │
               │ tip      │  │ rain gauge │
               │ bucket,  │  │ config     │
               │ check    │  │            │
               │ response │  └────────────┘
               └──────────┘
```

---

## Camera Network Setup

Both sites use the Pi as a DHCP server (dnsmasq) on the 192.168.50.0/24 camera network. Cameras receive predictable IPs via MAC address reservation. See the assembly guides for full setup instructions.

| Site | Pi IP | Camera IPs |
|------|-------|------------|
| Sukabumi | 192.168.50.1 | 192.168.50.139 |
| Jakarta | 192.168.50.1 | 192.168.50.101, 192.168.50.102 |

**Note:** The SADP utility (Hikvision/ANNKE) does not run on ARM Macs — neither natively nor under Parallels. The dnsmasq approach eliminates the need for SADP entirely.

**Note:** The ANNKE web interface requires a Windows-only browser plugin for live view. Use RTSP via VLC or ffmpeg to verify the camera image instead.

### Camera not getting expected IP

1. Check dnsmasq leases: `cat /var/lib/misc/dnsmasq.leases`
2. Verify the camera's MAC address in `/etc/dnsmasq.conf` matches the label on the camera
3. Restart dnsmasq: `sudo systemctl restart dnsmasq`
4. Power-cycle the camera (unplug/replug PoE cable) and wait 60-90s

### Finding camera MAC address

If you don't have the MAC address yet:

1. Temporarily remove any `dhcp-host=` lines from `/etc/dnsmasq.conf`
2. Restart dnsmasq: `sudo systemctl restart dnsmasq`
3. Connect camera to PoE injector, wait 60-90s for boot
4. Check leases: `cat /var/lib/misc/dnsmasq.leases`
5. The camera will have received an IP from the 192.168.50.100-200 range
6. Note the MAC address, add it to `/etc/dnsmasq.conf` as a `dhcp-host=` line
7. Restart dnsmasq and power-cycle the camera

### WiFi subnet conflict (laptop direct access)

The ANNKE C1200 ships with a default IP on 192.168.1.x — the same subnet used by most WiFi routers. If you ever need to access a camera directly from a laptop (before dnsmasq is set up), disable WiFi first:
```bash
# macOS:
networksetup -setairportpower en0 off
# Linux:
nmcli radio wifi off
```
Then set your laptop to 192.168.1.50/24 and use `arp -a` to find the camera. Re-enable WiFi when done.

---

## Common Issues & Solutions

### Power Issues

| Problem | Possible Cause | Solution |
|---------|---------------|----------|
| System won't boot | Dead battery (Sukabumi) | Charge battery, check solar panel |
| System won't boot | Blown fuse | Replace fuse, investigate cause |
| System won't boot | Faulty USB-C cable | Replace power cable to Pi |
| Intermittent shutdowns | Low battery voltage | Check BatteryProtect setting |
| Intermittent shutdowns | Loose connection | Check all terminal connections |

### Camera Issues (Both Sites Use PoE Cameras)

| Problem | Possible Cause | Solution |
|---------|---------------|----------|
| PoE camera offline | PoE injector fault | Check injector power/data LEDs |
| PoE camera offline | Cat6 cable fault | Test cable continuity |
| PoE camera offline | 12V power to injector | Check fuse, terminal connections |
| PoE camera offline (Sukabumi) | Camera still booting | Wait 60s after Pi wakes |
| PoE camera not reachable | Wrong IP address | Verify camera static IP setting |
| PoE camera not reachable | Network config | Check Pi and camera on same subnet |
| PoE camera not reachable | Pi eth0 IPv6-only | Pi has no IPv4 address — see "Pi eth0 Has Only IPv6 Address" above |
| Camera image blurry | Focus issue | Adjust lens focus ring |
| Camera image dark | Exposure settings | Adjust via camera web interface |
| Camera image washed out | Overexposure | Reduce exposure in settings |

### Connectivity Issues

| Problem | Possible Cause | Solution |
|---------|---------------|----------|
| No LTE signal | Antenna disconnected | Check SMA connections |
| No LTE signal | Wrong bands | Verify EG25-G band config |
| No LTE data | APN not configured | Set Telkomsel APN |
| No LTE data | IMEI not registered | Register with POSTEL |
| No LTE data | SIM deactivated | Check with carrier |
| Slow upload | Poor signal | Relocate antenna, add gain |

### Environmental Issues

| Problem | Possible Cause | Solution |
|---------|---------------|----------|
| Condensation inside enclosure | Gore vent blocked | Clear vent obstruction |
| Condensation inside enclosure | Failed seal | Reseal cable glands |
| Condensation inside enclosure | PTC heater fault (Jakarta) | Check heater wiring |
| Corrosion on connectors | Missing dielectric grease | Clean, apply grease |
| High internal temp | Direct sun exposure | Add shade, improve ventilation |
| Water ingress | Failed cable gland | Replace gland, reseal |

---

## Command Reference

### System Status

```bash
# Check system uptime
uptime

# Check CPU temperature
vcgencmd measure_temp

# Check disk usage
df -h

# Check memory
free -h

# Check running services
systemctl status orc
systemctl status wittypi
```

### USB Devices

```bash
# List USB devices
lsusb

# List video devices
ls /dev/video*

# Test camera capture (USB)
ffmpeg -f v4l2 -i /dev/video0 -frames:v 1 /tmp/test.jpg
```

### LTE Modem

```bash
# List modems
mmcli -L

# Modem status
mmcli -m 0

# Signal strength
mmcli -m 0 --signal-get

# Check connection
ping -c 3 8.8.8.8

# Restart modem
mmcli -m 0 --disable && sleep 5 && mmcli -m 0 --enable
```

### Network (PoE cameras)

```bash
# Ping cameras (Sukabumi)
ping -c 3 192.168.50.139

# Ping cameras (Jakarta)
ping -c 3 192.168.50.101
ping -c 3 192.168.50.102

# Test RTSP stream
ffmpeg -i rtsp://admin:PASSWORD@192.168.50.101:554/stream1 -frames:v 1 /tmp/cam1.jpg

# Check DHCP leases
cat /var/lib/misc/dnsmasq.leases

# Check network interfaces
ip addr

# Check route table
ip route

# Check dnsmasq status
sudo systemctl status dnsmasq
```

### I2C (Rain gauge)

```bash
# Scan I2C bus
i2cdetect -y 1

# Read from I2C device (address varies)
i2cget -y 1 0x20
```

### GPIO (LEDs, button)

```bash
# Export GPIO pin
echo 17 > /sys/class/gpio/export

# Set as output
echo out > /sys/class/gpio/gpio17/direction

# Turn on
echo 1 > /sys/class/gpio/gpio17/value

# Turn off
echo 0 > /sys/class/gpio/gpio17/value
```

### Relay Control (Sukabumi IR)

```bash
# List USB serial devices
ls /dev/ttyUSB* /dev/ttyACM*

# Control Numato relay (example)
echo "relay on 0" > /dev/ttyACM0
echo "relay off 0" > /dev/ttyACM0
```

### Witty Pi

```bash
# Check Witty Pi status
cd /home/pi/wittypi
./wittyPi.sh

# View schedule
cat schedule.wpi

# Check RTC time
./utilities.sh get_rtc_time

# Sync system time to RTC
./utilities.sh system_to_rtc
```

### Logs

```bash
# System log
journalctl -xe

# ORC application log
tail -f /var/log/orc/orc.log

# Boot messages
dmesg | tail -50

# Kernel messages (USB issues)
dmesg | grep -i usb
```

---

## Maintenance Mode

### Entering Maintenance Mode

1. **Long press** maintenance button (3+ seconds)
2. Wait for **yellow LED** steady on
3. System will:
   - Start WiFi hotspot
   - Prevent auto-shutdown
   - Enable SSH access

### Connecting to Maintenance Mode

1. On laptop/phone, connect to WiFi:
   - SSID: `ORC-SITENAME-MAINT`
   - Password: `[configured password]`

2. SSH into Pi:
   ```bash
   ssh pi@192.168.4.1
   ```

3. Default credentials:
   - User: `pi`
   - Password: `[configured password]`

### Exiting Maintenance Mode

- **Short press** button, OR
- Reboot: `sudo reboot`, OR
- Wait 30 minutes (auto-timeout)

---

## When to Escalate

Contact technical support if:

1. **Hardware failure** - Component needs replacement
2. **Software bug** - ORC application error not in logs
3. **Network config** - Can't establish LTE connection
4. **Physical damage** - Enclosure, pole, or cable damage
5. **Repeated failures** - Same component fails multiple times

**Before escalating, collect:**
- Site name and location
- Description of problem
- Status LED pattern
- Relevant log excerpts
- Photos if physical damage
- Last known working date

---

## Preventive Maintenance Schedule

### Monthly

- [ ] Visual inspection of enclosure (no damage, sealed)
- [ ] Check status LEDs functioning
- [ ] Verify data uploads occurring
- [ ] Check antenna connections (finger-tight)

### Quarterly

- [ ] Clean camera lens (if accessible)
- [ ] Check all cable gland seals
- [ ] Verify Gore vents not blocked
- [ ] Check rain gauge funnel (clear debris)
- [ ] Test maintenance mode access
- [ ] Review system logs for warnings

### Annually

- [ ] Inspect conformal coating on PCBs
- [ ] Check battery health (Jakarta: UPS, Sukabumi: solar)
- [ ] Replace degraded cable ties
- [ ] Test full system shutdown and restart
- [ ] Verify ground resistance <25Ω (Jakarta)
- [ ] Update OS and ORC software if available

---

**Document Version:** 1.0
**Last Updated:** January 9, 2026
