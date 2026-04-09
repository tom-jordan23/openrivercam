# Sukabumi Station — Enclosure Reference

**Version:** 1.0 — April 2026
**Print, laminate, and attach to the inside of the enclosure door.**

---

## Site Information

| Field | Value |
|-------|-------|
| Site | Sukabumi, Indonesia |
| Power | 12V Solar (existing 200W panel / 50Ah battery) |
| Station hostname | *(fill after install)* |
| Camera IP | 192.168.50.100 |
| Pi IP (camera network) | 192.168.50.1 |
| WiFi hotspot SSID | N/A (hotspot not available) |
| WiFi hotspot password | N/A (hotspot not available) |
| Installed by | |
| Install date | |

---

## Fuse Map

All fuses are **5x20mm glass tube** type. Do NOT use US automotive blade fuses
(AGA/AGC) — they are 6.3mm diameter and will not fit these holders.

| Fuse | Rating | Protects | What Happens If It Blows |
|------|--------|----------|--------------------------|
| F1 (5V rail) | 5A | DDR-60G-5 buck converter and Pi | Pi loses power, camera stops |
| F2 (12V PoE) | 5A | Relay CH1 and PoE switch | Camera loses power, Pi stays running |

**Replacement fuses:** 5x20mm, 5A, slow blow (time-delay). RTC battery:
CR2032 coin cell in the Witty Pi 5 HAT+ holder (non-rechargeable, no
config.txt charging settings needed).

---

## Wire Color Code

| Color | Purpose |
|-------|---------|
| **Red** | 12V positive |
| **Black** | Ground (GND) |
| **Yellow** | 5V power (buck converter to Pi, Pi to relay VCC) |
| **Blue** | GPIO signal — relay IN1 (PoE switch, GPIO 24) |
| **Green** | GPIO 18 data — WS2812B status LED |

---

## GPIO Pin Assignments

| GPIO | Pin | Function |
|------|-----|----------|
| — | 2 | 5V power IN (from DDR-60G-5) |
| — | 4 | 5V power OUT (to relay VCC) |
| GPIO 2 | 3 | I2C SDA (SHT40 sensor) |
| GPIO 3 | 5 | I2C SCL (SHT40 sensor) |
| GPIO 4 | 7 | 1-Wire data (DS18B20 probe) |
| — | 9 | GND (SHT40, rain gauge) |
| GPIO 14 | 8 | UART TX → RG-15 RX |
| GPIO 15 | 10 | UART RX ← RG-15 TX |
| GPIO 18 | 12 | WS2812B data (status LED) |
| — | 17 | 3V3 power (DS18B20 + pull-up) |
| GPIO 24 | 18 | Relay IN1 (PoE switch) |
| — | 20 | GND (relay module) |
| — | 25 | GND (buck converter) |
| — | 39 | GND (DS18B20) |

---

## Terminal Block (TB1) Labels

```
TB1 — 12V DISTRIBUTION (from solar battery)
┌──────┬──────┬──────┬──────┬──────┬──────┐
│ 12V+ │ 12V+ │ 12V+ │ GND  │ GND  │ GND  │
│ F1   │ F2   │ RG15 │      │      │      │
│(5V)  │(PoE) │(pwr) │      │      │      │
└──────┴──────┴──────┴──────┴──────┴──────┘
```

---

## Bulkhead Connectors (outside → inside)

| Connector | Type | Carries | Pin Map |
|-----------|------|---------|---------|
| SP13 | DC power | 12V solar input | + / − |
| CNLINKO | Ethernet IP67 | PoE camera data+power | Standard RJ45 |
| SD16 4-pin | Rain gauge | 12V + GND + UART TX/RX | 1:12V, 2:GND, 3:TX→RX, 4:RX→TX |

---

## Relay Channels

| CH | GPIO | Load | State when Pi is OFF |
|----|------|------|----------------------|
| 1 | GPIO 24 (Pin 18) | PoE switch (camera) | **OFF** (fail-safe — loads turn off when power is lost: camera unpowered) |
| 2 | GPIO 17 (Pin 11) | Available — GPIO wired, no load | OFF |
| 3 | GPIO 27 (Pin 13) | Available — GPIO wired, no load | OFF |
| 4 | GPIO 22 (Pin 15) | Available — GPIO wired, no load | OFF |

All relays use **NO (Normally Open)** contacts. When the Pi loses power or
crashes, all relays open and all loads lose power. This is intentional —
it prevents the camera from draining the solar battery.

## Status LED

Single WS2812B (NeoPixel) RGB LED behind sealed acrylic light window.
Driven by 1 GPIO data pin + 5V power. No relay channels used.

| Color | Pattern | Meaning |
|-------|---------|---------|
| Green | Solid | System OK, idle |
| Green | Flash | Capturing video |
| Green | Slow pulse | Shutting down |
| White | Solid | Boot in progress |
| Cyan | Solid | Maintenance mode active |
| Red | Solid | Camera offline (normal between cycles) |
| Red | Flash | Capture failed |
| Blue | Solid/flash | Network/LTE problem |
| Yellow | Solid/flash | Storage problem |
| Magenta | Solid | Power issue |
| OFF | — | Pi is off / sleeping (normal between cycles) |

---

## Simplified Wiring Schematic

```
SOLAR 12V ──► SP13 bulkhead ──► TB1
                                  │
                 ┌────────────────┼────────────────┐
                 │                │                │
              [F1 5A]          [F2 5A]        RG-15 12V
                 │                │           (always on)
            DDR-60G-5        Fuse holder
            (12V→5.1V)           │
                 │            Relay CH1
           Pin 2 (5V)        (GPIO 24)
           Pin 25 (GND)         │
                 │           PoE Switch
              Pi 5              │
                 │           Camera
           Pin 4 → Relay VCC
           Pin 20 → Relay GND
           Pin 18 → Relay IN1 (PoE)
           GPIO 18 → WS2812B data (status LED)
```

---

## RTC (Witty Pi 5 HAT+)

- **Type:** CR2032 coin cell (non-rechargeable, on Witty Pi 5 board)
- **I2C address:** 0x51
- **Software:** `wp5` CLI, `wp5d` daemon (auto-starts at boot)
- **Pi 5 native RTC (J5):** Not used — ML-2020 connector failed on both boards
- **No `dtparam=rtc_bbat_vchg` needed** — Witty Pi 5 has its own RTC

---

## Power Button

The power button (Pi 5 J2 header) handles all power and maintenance functions:

- **Brief press:** power on (from halted) or clean shutdown (while running)
- **Long press (3 seconds):** enter maintenance mode (access via Pangolin or Tailscale)
- **10-second hold:** force power off (if frozen)

## Maintenance Mode

1. Long press power button (3 seconds)
2. Pi enters maintenance mode (prevents auto-shutdown)
3. Connect via Pangolin (`https://arc-00002.openrivercam.com`) or Tailscale
4. SSH to Pi for diagnostics

---

## Emergency Contacts

| Role | Name | Phone | Email |
|------|------|-------|-------|
| Project lead | | | |
| Local contact | | | |
| ORC support | | | |
