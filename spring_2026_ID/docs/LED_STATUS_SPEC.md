# LED Status Indicator Specification

**Hardware:** Single WS2812B (NeoPixel) addressable RGB LED
**Data pin:** 1 GPIO pin (BCM number set in config)
**Power:** 5V from Pi rail via G469 (Pin 2 or Pin 4)
**Mount:** Inside enclosure behind sealed acrylic light window

---

## Status States

### Normal Operation

| State | Color | Pattern | Notes |
|-------|-------|---------|-------|
| Booting | White | Solid | Set early in boot sequence |
| Idle / healthy | Green | Solid | System OK, waiting for next capture |
| Capture running | Green | Flash (2 Hz) | RTSP pull in progress |
| Maintenance mode | Cyan | Solid | Maintenance mode active |
| Shutting down | Green | Single slow pulse | Clean shutdown in progress |
| Off / sleeping | OFF | — | Pi halted or between wake cycles |

### Error States (by subsystem)

Errors are color-coded by subsystem. Within a subsystem, steady vs blinking
distinguishes the failure mode.

| Subsystem | Color | Steady | Blinking (4 Hz) |
|-----------|-------|--------|------------------|
| Camera/PoE | Red | Camera unreachable | Capture/RTSP failed |
| Network/LTE | Blue | Modem down | Upload failed |
| Storage | Yellow | Disk space low | Write error |
| Power | Magenta | Undervoltage detected | — |

### Error Priority and Cycling

When multiple subsystems are in error simultaneously, the LED cycles through
all active (non-suppressed) errors, showing each for `cycle_interval_s`
seconds (default: 3s) before switching to the next.

Cycle order is fixed: Camera > Network > Storage > Power. This is display
order only, not a severity ranking.

If a normal-operation event occurs during error display (e.g., capture
starts), the normal state takes priority for its duration, then error
cycling resumes.

---

## Configuration

The LED service reads a YAML config file at startup. Changes require a
service restart to take effect.

**Config file location:** `/etc/orc/led-status.yaml`

### Reference Configuration

```yaml
# LED Status Indicator Configuration
# ===================================
# Restart led-status.service after editing.

led:
  gpio_pin: 18          # BCM pin number for WS2812B DIN
  brightness: 200       # 0-255 (200 is good for daylight through acrylic)

# Normal operation states
# Colors are [R, G, B] 0-255
states:
  boot:
    color: [255, 255, 255]   # white
    pattern: solid
  idle:
    color: [0, 255, 0]       # green
    pattern: solid
  capture:
    color: [0, 255, 0]       # green
    pattern: flash
    flash_hz: 2
  maintenance:
    color: [0, 255, 255]     # cyan
    pattern: solid
  shutdown:
    color: [0, 255, 0]       # green
    pattern: pulse

# Error subsystems
# Set suppressed: true to ignore a subsystem (e.g., bench testing without LTE)
errors:
  camera:
    color: [255, 0, 0]       # red
    suppressed: false
  network:
    color: [0, 0, 255]       # blue
    suppressed: false
  storage:
    color: [255, 255, 0]     # yellow
    suppressed: false
  power:
    color: [255, 0, 255]     # magenta
    suppressed: false

# Error display behavior
error_display:
  cycle_interval_s: 3        # seconds per error when cycling
  blink_hz: 4                # blink rate for blinking error patterns
```

### Bench Testing Example

When testing on the bench without cellular connectivity, suppress the
network subsystem so the LED stays green instead of cycling through a
blue error:

```yaml
errors:
  network:
    color: [0, 0, 255]
    suppressed: true
```

Multiple subsystems can be suppressed simultaneously. A suppressed error
is still logged — it just doesn't drive the LED.

---

## Wiring

```
G469 Pin 2 (5V)  ──► WS2812B VCC
G469 GND          ──► WS2812B GND
G469 GPIO 18      ──► WS2812B DIN (data in)
```

One LED draws ~60 mA max (all white, full brightness). Typical draw during
normal operation (single color) is ~20 mA.

**Note:** On Pi 5, the LED is driven via the RP1 PIO peripheral
(`/dev/pio0`), not PWM/DMA as on earlier Pis. Any free GPIO pin works —
just update `gpio_pin` in the config.

**Pi 5 compatibility:** The commonly-referenced `rpi-ws281x` library does
NOT work on Pi 5 (error -3: "Hardware revision is not supported"). This
build uses `adafruit-blinka-raspberry-pi5-neopixel` instead, which drives
the WS2812B protocol through the RP1's PIO block. See `pi/PACKAGES.md`.

---

## Design Decisions

1. **Single RGB LED vs 3 separate LEDs:** Frees relay channels CH2-CH4
   for future PMI use. One WS2812B replaces three 12V relay-driven LEDs
   with simpler wiring (1 data pin vs 3 GPIO + 3 relay channels + 12V
   power routing).

2. **Config-file-driven:** Colors, patterns, and suppression are all in
   YAML so field teams can adjust without code changes. Suppression is
   the key feature — it prevents known-absent subsystems from creating
   noise during bench testing or staged deployment.

3. **Cycle through errors (not priority-only):** Showing only the
   highest-priority error would hide secondary failures. Cycling ensures
   all active errors are visible to a field technician standing at the
   enclosure.

4. **Steady vs blink within a subsystem:** Distinguishes "subsystem is
   down" (steady — check hardware/connections) from "subsystem is up but
   an operation failed" (blink — check software/config). A technician
   can tell the difference without opening the enclosure.

---

**Document Version:** 1.0
**Created:** April 1, 2026
