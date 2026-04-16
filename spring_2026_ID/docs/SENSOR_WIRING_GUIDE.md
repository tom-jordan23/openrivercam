# Sensor Wiring Guide — Temperature Probe & Rain Gauge

**Both stations (Sukabumi and Jakarta) use identical wiring.**

Print and laminate for field reference.

---

## DS18B20 Waterproof Temperature Probe (1-Wire)

| Connection | Pin | Notes |
|------------|-----|-------|
| Data | GPIO 4 / Pin 7 | 1-Wire data line |
| Power | 3V3 / Pin 17 | |
| Ground | GND / Pin 39 | |

- 4.7k ohm pull-up resistor between data (GPIO 4) and 3V3
- Pull-up resistor mounts on Geekworm G469 terminals
- Cable enters enclosure through **PG9 cable gland**
- Requires `dtoverlay=w1-gpio` in `/boot/firmware/config.txt`

```
3V3 (Pin 17) ──[4.7kΩ]──┬── GPIO 4 (Pin 7)
                          │
                     ┌────┴────────────┐
                     │  DS18B20 probe   │
                     │  (stainless, 1m) │
                     └────┬────────────┘
                          │
GND (Pin 39) ─────────────┘
```

---

## Hydreon RG-15 Rain Gauge (UART)

| Connection | Pin | Notes |
|------------|-----|-------|
| RG-15 TX (out) | GPIO 15 / RX / Pin 10 | Pi receives data |
| RG-15 RX (in) | GPIO 14 / TX / Pin 8 | Pi sends commands |
| Power | 12V from TB1 | RG-15 accepts 7-24V input |
| Ground | GND from TB1 | |

- Serial port: `/dev/ttyAMA0` at 9600 baud
- No level shifter needed — RG-15 signal is 3.3V TTL
- Power and ground from **TB1 terminal block** (not GPIO header)
- Cable enters enclosure through **PG9 cable gland**

```
Hydreon RG-15              Geekworm G469 / TB1
┌──────────────┐           ┌─────────────┐
│  VCC         │───────────│  12V (TB1)  │
│  GND         │───────────│  GND (TB1)  │
│  TX (out)    │───────────│  GPIO 15/RX │  Pin 10
│  RX (in)     │───────────│  GPIO 14/TX │  Pin 8
└──────────────┘           └─────────────┘
```

---

## Quick Reference

| Sensor | Data Pin(s) | Power | Ground | Gland |
|--------|------------|-------|--------|-------|
| DS18B20 temp probe | GPIO 4 / Pin 7 (+ 4.7k pull-up to 3V3) | 3V3 / Pin 17 | GND / Pin 39 | PG9 |
| RG-15 rain gauge | GPIO 14 (TX) / Pin 8, GPIO 15 (RX) / Pin 10 | 12V (TB1) | GND (TB1) | PG9 |

---

## Software Configuration

- DS18B20 config: `/etc/orc-sensors/ds18b20.conf`
- RG-15 config: `/etc/orc-sensors/rg15.conf`
- Sensor logging service: `orc-sensors`

---

## See Also

- [WIRING_SUKABUMI.md](WIRING_SUKABUMI.md) — full system wiring diagram
- [WIRING_JAKARTA.md](WIRING_JAKARTA.md) — full system wiring diagram
- [GPIO_WIRING.md](../diagrams/sukabumi/GPIO_WIRING.md) — complete GPIO pin map
