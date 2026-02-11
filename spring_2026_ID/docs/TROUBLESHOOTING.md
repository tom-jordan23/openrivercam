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

### Camera Not Working

#### Sukabumi (PoE Camera - Power-Cycled)

```
START: No video capture
         │
         ▼
┌─────────────────────────┐
│ Ping camera from Pi:    │
│ ping 192.168.100.10     │
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
│ - LED on?    │  │ 192.168.100.10:554/│
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
│ ping 192.168.1.101      │
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
│ power LED    │  │ 192.168.1.101:554/ │
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

### Network (Jakarta PoE cameras)

```bash
# Ping cameras
ping -c 3 192.168.1.101
ping -c 3 192.168.1.102

# Test RTSP stream
ffmpeg -i rtsp://admin:PASSWORD@192.168.1.101:554/stream1 -frames:v 1 /tmp/cam1.jpg

# Check network interfaces
ip addr

# Check route table
ip route
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
