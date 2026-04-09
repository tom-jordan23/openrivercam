# ORC Station Operator Guide

**For:** PMI field staff responsible for monitoring and maintaining ORC stations
**Sites:** Sukabumi (solar) and Jakarta (AC power)
**Version:** 1.0 — April 2026

---

## What the Station Does

The station automatically records short videos of the river every 15 minutes,
measures water velocity from the video, and calculates river flow (discharge).
Results upload to a central server over LTE cellular data.

**You do not need to operate the station day-to-day.** It runs unattended.
This guide covers what to check, how to tell if something is wrong, and what
to do about it.

---

## 1. Status LED — Is the Station OK?

The LED is visible through the enclosure window without opening the box.

| LED Color | Pattern | Meaning | Action |
|-----------|---------|---------|--------|
| **Green** | Steady | Healthy, waiting for next capture | None — normal |
| **Green** | Flashing | Capturing video right now | None — normal |
| **White** | Steady | Booting up | Wait 2-3 minutes |
| **Cyan** | Steady | Maintenance mode | Intentional — see Section 5 |
| **Green** | Slow pulse | Shutting down | Normal (Sukabumi between cycles) |
| **Red** | Steady | Camera offline | May be normal (see note below) |
| **Red** | Flashing | Capture failed | See Section 7 |
| **Blue** | Steady/flash | Network/LTE problem | See Section 7 |
| **Yellow** | Steady/flash | Storage problem | See Section 7 |
| **Magenta** | Steady | Power problem | See Section 7 |
| **OFF** | — | No power or sleeping | Normal for Sukabumi between cycles |

**Note on solid red:** A steady red LED means the camera is offline. On
Sukabumi this is **normal between capture cycles** — the camera powers down
with the PoE relay to save solar energy. Solid red is only a problem if the
camera should be on at that time (e.g., Jakarta where the camera runs 24/7,
or Sukabumi during an active capture cycle).

**Rule of thumb:** Green = good. Any other color for more than 10 minutes =
investigate.

---

## 2. Normal Operation

### Sukabumi (Solar)

The station wakes every 15 minutes, captures a video, processes it, uploads
results, then goes back to sleep. A complete cycle takes about 3 minutes.

What you'll see:
1. LED turns white (booting) — ~25 seconds
2. LED turns green flashing (capturing) — ~1 minute
3. LED turns green steady (processing/uploading) — ~1-2 minutes
4. LED turns off (sleeping) — ~12 minutes
5. Repeat

**Between cycles, the station is OFF.** This is normal — it saves solar power.

### Jakarta (AC Power)

The station runs continuously. It captures a video every 15 minutes but stays
powered on between captures.

What you'll see:
- LED is green steady most of the time
- LED flashes green briefly every 15 minutes during capture
- Station reboots itself once per day (health check) — you'll see white LED
  briefly

---

## 3. Checking the Station Remotely

### Web Dashboard (ORC-OS) — Local Access Only

Connect to the station's WiFi hotspot (maintenance mode), then open:

- **Sukabumi:** `http://orc-sukabumi.local:5173/`
- **Jakarta:** `http://orc-jakarta.local:5173/`

The dashboard shows recent videos, processing status, and sensor data.
Login password is stored separately (ask Tom).

### Remote Access (Pangolin)

From anywhere with internet, without needing to be physically at the site:

- **Jakarta:** `https://arc-00001.openrivercam.com`
- **Sukabumi:** `https://arc-00002.openrivercam.com`

This provides HTTPS access to the ORC-OS web dashboard via a tunneled
reverse proxy. Credentials stored separately.

**Note:** We are also evaluating Tailscale as an alternative remote access
solution. Tailscale may be a better fit in some situations but is not usable
in countries that restrict third-party VPN services.

### LiveORC Server

All processed data uploads to: `https://openrivercam.endlessprojects.info/`

Login to see discharge measurements, time series, and video thumbnails from
all stations.

---

## 4. Power Button

Each station has a single waterproof button on the enclosure.

| Action | What happens |
|--------|-------------|
| **Brief press** (Pi is off) | Powers on the station |
| **Brief press** (Pi is running) | Clean shutdown |
| **Long press** (3 seconds) | Enters maintenance mode |
| **Hold 10 seconds** | Forces power off (emergency only) |

**Sukabumi note:** You normally do NOT need the power button. The Witty Pi
schedule handles wake/sleep automatically. Only use the button for maintenance.

---

## 5. Maintenance Mode

Maintenance mode keeps the station awake and stops video capture so you can
work on it without interference.

### Entering Maintenance Mode

**Option A — Power button:** Long press (3 seconds). LED turns cyan.

**Option B — Remote (GitHub):** Someone with repository access changes the
station's mode file from "production" to "maintenance" at:

`https://github.com/tom-jordan23/orc-pmi-stations`

Use the "Set Station Mode" workflow (Actions tab) to toggle a station between
production and maintenance. The station picks up the change on next boot.

### What Changes in Maintenance Mode

- Video capture stops (no RTSP pulls, no relay cycling)
- ORC-OS web dashboard stays accessible
- Station stays awake (won't auto-shutdown even on Sukabumi)
- LED shows cyan

### Exiting Maintenance Mode

- Brief press of power button, OR
- Change mode back to "production" on GitHub and reboot, OR
- Reboot the Pi (`sudo reboot` via SSH)

---

## 6. Routine Maintenance

### Monthly

- [ ] **Visual check:** LED is green? Enclosure intact? No water intrusion?
- [ ] **Camera lens:** Clean with microfiber cloth if dirty (insects, dust, rain spots)
- [ ] **Rain gauge dome:** Wipe clean if debris has accumulated (leaves, bird droppings)
- [ ] **Cable glands:** Visually inspect — no cracking, no loose fittings
- [ ] **Check LiveORC:** Log in and verify recent data is uploading

### Quarterly

- [ ] **Open enclosure** — read the warning below first:

  **WARNING: Opening the enclosure in humid conditions can cause damage.**
  The enclosure uses GORE vents to equalize pressure while keeping water
  out. The air inside the box is drier than the outside air. When you open
  the lid, humid tropical air rushes in. If the electronics are cooler than
  the incoming air (e.g., after a cool night or rain), moisture will
  **condense on the circuit boards** — this can cause shorts and corrosion.

  **Rules for opening the enclosure:**
  - **Do not open if ambient humidity is above 70% RH** (use a weather app
    or the SHT40 reading from the dashboard to check)
  - **Never** open during or immediately after rain
  - Open during the **warmest, driest** part of the day (midday sun)
  - Take your time once open — the air exchange happens immediately when
    the lid opens, so rushing won't help
  - If you see condensation on any component, close the lid immediately
    and let the GORE vents do their job over the next 24 hours
  - Enter maintenance mode before opening (prevents capture cycles
    during service)

  Once open, check:
  - Moisture, insects, corrosion inside
  - Terminal blocks — no loose wires
  - Fuses — no discoloration
  - LED and sensors are clean
- [ ] **Sukabumi solar:** Clean solar panel if dirty. Check battery voltage
  (should be >12V). Inspect cable connections at battery terminals.

### After Storms

- [ ] Check station is still operating (LED green)
- [ ] Check camera is still aimed correctly (hasn't shifted)
- [ ] Check rain gauge hasn't been knocked off mount
- [ ] Check enclosure for water intrusion
- [ ] **Jakarta:** Check AC power is on (building may have tripped breaker)

---

## 7. Troubleshooting — Quick Fixes

### Station LED is OFF (no light at all)

1. **Sukabumi:** May be sleeping between cycles. Wait 15 minutes — if LED
   doesn't come on, press power button briefly.
2. **Jakarta:** Check AC power is on at the building breaker.
3. Press power button briefly. If nothing happens, open enclosure and check
   fuses (see door sheet inside lid).

### LED is RED (camera problem)

1. Camera may need time to boot. Wait 5 minutes.
2. Check that the ethernet cable between enclosure and camera is connected.
3. Open enclosure → check the PoE switch has power (green LED on the switch).
4. If PoE switch is dark, check fuse F2 (5A).

### LED is BLUE (network problem)

1. LTE modem may need time to connect. Wait 5 minutes.
2. Check antenna — is it connected and not damaged?
3. If problem persists, check SIM card (open enclosure, inspect modem).
4. Verify cell coverage at site hasn't changed.

### LED is YELLOW (storage problem)

1. Storage may be full. Connect to web dashboard and check disk space.
2. If disk is full, old videos should auto-clean. If not, contact Tom.

### LED is MAGENTA (power problem)

1. **Sukabumi:** Battery may be low. Check if solar panel is clean and
   unobstructed. Check battery voltage (should be >12V).
2. **Jakarta:** Check AC power. May be a brownout or voltage sag.

### No data on LiveORC server

1. Station may be working but LTE upload is slow. Wait 1 hour.
2. Check station LED — if green, station is healthy. Problem is connectivity.
3. Check if SIM card has data remaining (prepaid plans expire).
4. Remote-access the station via Pangolin and check upload status.

### Camera image is dark or blurry

1. Clean the camera lens (microfiber cloth).
2. Check that nothing is blocking the camera view (new vegetation, spider webs).
3. IR LEDs handle night vision automatically — no adjustment needed.

---

## 8. What NOT to Do

| Do NOT | Why |
|--------|-----|
| Disconnect wires inside the enclosure | You may connect them wrong and damage the Pi |
| Change any software settings without guidance | The system is carefully configured |
| Open the enclosure in rain | Water intrusion damages electronics |
| Force-hold the power button regularly | Use brief press for clean shutdown |
| Unplug the rain gauge cable | It accumulates data that would be lost |
| Point the camera at a different angle | Requires complete recalibration (field survey) |
| Swap SD cards between stations | Each card is configured for its station |
| Connect power to any terminal marked "GPIO" | 12V on GPIO pins destroys the Pi instantly |

---

## 9. Sensor Reference

### Rain Gauge (Hydreon RG-15)

- Mounted outside the enclosure
- Optical sensor — no moving parts, self-cleaning dome
- Measures rainfall intensity and accumulation
- Stays powered 24/7 (even when Pi sleeps on Sukabumi)
- **Cleaning:** Wipe dome with damp cloth. Do not use solvents.
- **Disconnect:** SD16 4-pin connector (keyed, waterproof). Unplug to replace
  gauge without opening enclosure.

### Temperature/Humidity (SHT40)

- Mounted inside the enclosure
- Monitors internal conditions (humidity alert threshold)
- No maintenance required

### Outside Temperature (DS18B20)

- Waterproof probe mounted outside the enclosure
- Passes through PG9 cable gland
- No maintenance required

---

## 10. Extending the Station — Available Relay Channels

Each station has a 4-channel relay module. Only **channel 1** is used
(PoE camera power). **Channels 2, 3, and 4 are available** for future use.

### What the Relays Can Do

Each relay channel is an electrically isolated switch that the Pi controls
via a GPIO pin. When the Pi sets the pin HIGH, the relay closes and connects
power to whatever is wired to it. When the pin goes LOW (or the Pi loses
power), the relay opens and the load loses power.

- **Switching capacity:** 12V DC from the station's power bus (TB1)
- **Each channel is independent** — they can be on/off in any combination
- **Fail-safe:** All relays open (loads off) if the Pi crashes or loses power
- **Control:** Any script or service on the Pi can toggle a relay by setting
  a GPIO pin high or low

### Ideas for Future Use

**Alerting and notification:**
- Wire a relay to a siren, strobe light, or warning beacon. Trigger it from
  software when the river level exceeds a threshold. The relay can power a
  12V alarm device directly from TB1.
- Wire a relay to a cellular SMS gateway module (12V powered). Send automated
  text messages during flood events.

**Additional instruments:**
- Power a water level sensor on a duty cycle (turn on to take a reading, turn
  off to save power). Useful for Sukabumi where solar budget is limited.
- Power a second camera for a different view angle or a wider scene.
- Power a 12V solenoid for automated water sampling.

**Integration with other systems:**
- Use a relay as a dry-contact output to interface with existing telemetry or
  SCADA systems. The relay's NO/NC terminals can signal to any system that
  reads contact closures.
- Power a 12V radio or LoRa transmitter for local data relay to a nearby
  station or gateway.

### How to Connect a New Load

**This requires opening the enclosure. Only trained personnel should do
this. See Section 6 for humidity warnings about opening the enclosure.**

The GPIO control wiring from the Pi to relay inputs IN2, IN3, and IN4 is
**already done** on both stations. You only need to wire the 12V load side.

Each unused relay channel has three screw terminals on the 12V output side:

| Terminal | Function |
|----------|----------|
| **COM** (Common) | Connect to 12V+ from TB1 (through a fuse) |
| **NO** (Normally Open) | Connect to your 12V load (+) |
| **NC** (Normally Closed) | Not used (leave empty for fail-safe behavior) |

The load's ground wire returns to TB1 GND.

**Always add a fuse** between TB1 and the relay COM terminal. Match the fuse
to the load's current draw (e.g., 2A fuse for a 20W load at 12V).

To control the relay from the Pi (command line):
```
# Turn on relay channel 2 (GPIO 17)
gpioset gpiochip0 17=1

# Turn off
gpioset gpiochip0 17=0
```

### Relay Channel Assignments

| Channel | GPIO | G469 Pin | Status |
|---------|------|----------|--------|
| CH1 | GPIO 24 | Pin 18 | **In use** — PoE camera power |
| CH2 | GPIO 17 | Pin 11 | Available — GPIO wired, no load |
| CH3 | GPIO 27 | Pin 13 | Available — GPIO wired, no load |
| CH4 | GPIO 22 | Pin 15 | Available — GPIO wired, no load |

These assignments are the same on both stations.

### Important Notes

- **Do not exceed 12V or 10A per channel** on the relay contacts
- **Always use NO (Normally Open)** contacts for fail-safe behavior — loads
  turn off if the Pi loses power
- **Add a fuse** on every new load circuit
- **Label all new wiring** clearly at both ends
- **Document what you connected** — update the door sheet inside the enclosure
- **Test before leaving the site** — verify the relay toggles and the load
  responds

---

## 11. Emergency Contacts

| Role | Name | Phone | Email |
|------|------|-------|-------|
| Technical lead | Tom Jordan | *(fill in)* | *(fill in)* |
| PMI site contact (Sukabumi) | | | |
| PMI site contact (Jakarta) | | | |

### If the station is completely unresponsive:

1. Note the LED color (or that it's off) and the time
2. Take a photo of the station and any visible damage
3. Contact Tom with the photo and description
4. **Do not open the enclosure or disconnect anything** unless instructed

