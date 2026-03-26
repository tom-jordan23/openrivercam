# PoE Switch Power Relay Research

**Date:** March 2, 2026
**Purpose:** Select a DIN-rail-mountable relay to control 12V power to the PoE switch, enabling camera power cycling during Pi sleep/wake cycles
**Constraint:** No soldering - screw terminal connections only, DIN rail mountable

---

## Requirements

- **Load:** 12V DC, up to 3-5A (LINOVISION Industrial PoE switch + camera)
- **Trigger:** Either GPIO (3.3V from Pi) or passive USB (relay follows Pi power state)
- **Form factor:** DIN rail mountable
- **Connections:** Screw terminals only (no soldering)
- **Available on Amazon**

---

## How Power Cycling Works with Witty Pi 5

The Witty Pi 5 HAT+ performs a full hard power cut when the Pi sleeps — the 5V rail, all GPIO outputs, and all USB ports go completely dead. This means:

- **GPIO approach:** Pin goes to 0V when Pi sleeps, relay opens automatically
- **USB approach:** USB power disappears when Pi sleeps, relay opens automatically

Both trigger methods work cleanly. No software timing or shutdown hooks needed — the Witty Pi handles it at the hardware level.

---

## Recommendation: Electronics-Salon DIN Rail 4-SPDT 10A Relay Module (5V)

| Spec | Value |
|------|-------|
| Model | Electronics-Salon DIN Rail Mount 4 SPDT 10A Power Relay Interface Module, DC 5V |
| Amazon | B00M1MW5BW |
| Price | ~$18 |
| Trigger | 3.3V GPIO compatible (5V coil with Darlington transistor driver) |
| Load | 10A / 30V DC per channel (2x headroom over PoE switch) |
| Channels | 4 (only 1 needed; extras available for future use) |
| Contacts | SPDT (NO/NC/COM) per channel |
| Screw terminals | Yes — both signal input and relay output (DINKLE terminals) |
| DIN rail | Built-in 35mm snap mount |
| LED indicators | Yes, per channel |
| Relay type | JS1-5V-F |

### Trigger Option 1: GPIO Control

Wire from Geekworm G469 GPIO breakout screw terminals to relay module screw terminals:

| Relay Terminal | Pi Connection |
|---------------|---------------|
| VCC | Pi 5V (Pin 2) |
| GND | Pi GND (Pin 6) |
| IN1 | GPIO 24 (Pin 18) |

> **Note:** This research originally proposed GPIO 17, but the final wiring
> (see `diagrams/sukabumi/circuit_diagram.txt` Rev 3.0) assigns GPIO 17 to
> the Green LED relay (CH2). The PoE relay (CH1) uses **GPIO 24**.
> The legacy sysfs interface (`/sys/class/gpio/`) is also replaced by
> `pinctrl` on Pi 5.

Manual control via the `poe-relay` utility (see `pi/shared/usr/local/bin/poe-relay`):

```
poe-relay on      # GPIO 24 HIGH → relay closed → PoE switch ON
poe-relay off     # GPIO 24 LOW  → relay open   → PoE switch OFF
poe-relay status  # show current state + eth0 IP
```

**Note:** The relay will be open for ~30-60s during Pi boot before the service runs. The camera needs this time to boot anyway (~45-60s), so this aligns naturally with the existing 150s active cycle.

### Trigger Option 2: Passive USB (Zero Software)

Power the relay module's VCC from a Pi USB-A port and bridge IN1 to GND on the screw terminal block. The relay energizes the instant USB power appears (Pi wakes) and drops out when USB power disappears (Pi sleeps). No GPIO pin used, no software needed.

This works because the module uses active-low logic — the relay energizes when IN is pulled LOW. Bridging IN1 to GND means the relay is always on when powered.

### Relay Output Wiring

| Relay Terminal | Connection |
|---------------|------------|
| COM | 12V from DDR-60G-12 buck converter output |
| NO | 12V input on LINOVISION PoE switch |
| NC | Not used |

When the relay is energized (Pi awake), the NO contact closes and 12V reaches the PoE switch. When the relay opens (Pi sleeping), the PoE switch loses power.

---

## Runner-Up: Industrial 1-Channel DIN Relay

| Spec | Value |
|------|-------|
| Amazon | B0F8B7V8GR |
| Price | ~$12-18 |
| Trigger | 3-24V signal, selectable HIGH/LOW active mode |
| Load | 10A |
| Screw terminals | Yes |
| DIN rail | Yes, ABS housing |
| Opto-isolated | Yes |

Good single-channel alternative if 4 channels is overkill. Selectable active mode removes polarity ambiguity. Less documentation than Electronics-Salon.

---

## Alternatives Evaluated and Rejected

### Numato 1-Channel USB Powered Relay (B00MY5I6BO)
- **Rejected:** 2A contact rating — insufficient for PoE switch at full load (up to 5.5A)
- Requires USB serial commands (not passive)

### DC-DC Solid State Relays (TRD060D10K, SSR-25DD)
- **Rejected:** Off-state leakage current may prevent the PoE switch from fully powering down, defeating the power-cycling purpose
- Voltage drop of 0.5-1.5V at load reduces voltage to PoE switch

### MOSFET Switch Modules (NOYITO B07F5JPXYS)
- **Rejected:** Not DIN-rail mountable
- IRF520-based modules are NOT 3.3V compatible — avoid these entirely

### Waveshare RPi Relay Board (B01FZ7XLJ4)
- **Rejected:** Not DIN-rail mountable
- HAT form factor conflicts with Witty Pi 5 on the 40-pin header

### LIVISN USB HID Relay (B07XNTHGT6)
- **Rejected:** Requires active HID commands to toggle — does NOT auto-energize on USB power

---

## Summary

The Electronics-Salon DIN Rail relay module is the best fit: industrial quality, DIN-native, 10A contacts with 2x headroom, screw terminals throughout, and it supports both GPIO and passive USB trigger approaches. The extra 3 channels provide expansion options (rain gauge power control, future sensors, etc.).
