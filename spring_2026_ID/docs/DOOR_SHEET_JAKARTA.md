# Jakarta Station — Enclosure Reference

**Print, laminate, and attach to the inside of the enclosure door.**

---

## Site Information

| Field | Value |
|-------|-------|
| Site | Jakarta, Indonesia |
| Power | 220V AC mains with 12V LiFePO4 UPS (100Ah) |
| Station hostname | *(fill after install)* |
| Camera IP | 192.168.50.101 |
| Pi IP (camera network) | 192.168.50.1 |
| WiFi hotspot SSID | *(fill after install)* |
| WiFi hotspot password | *(fill after install)* |
| AC circuit breaker # | *(fill after install)* |
| Ground rod resistance | *(fill after install)* Ohm |
| Installed by | |
| Install date | |

---

## Fuse Map

All fuses are **5x20mm glass tube** type. Do NOT use US automotive blade fuses
(AGA/AGC) — they are 6.3mm diameter and will not fit these holders.

| Fuse | Rating | Protects | What Happens If It Blows |
|------|--------|----------|--------------------------|
| F2 (PoE) | 5A | Relay CH1 and PoE switch | Camera loses power, Pi stays running |
| F3 (Pi) | 5A | DDR-60G-5 buck converter and Pi | Pi loses power |
| F4 (Heater) | 5A | PTC heater and fans | Climate control stops, system continues |

**Replacement fuses:** 5x20mm, rated amperage, slow blow (time-delay).

---

## AC Mains Wiring

**DANGER: 220V AC inside this enclosure. Disconnect AC breaker before servicing.**

| Terminal | Label | Wire Color | Function |
|----------|-------|------------|----------|
| L | Line | Brown | 220V hot |
| N | Neutral | Blue | Return |
| PE | Protective Earth | Green/Yellow | Ground (to rod) |

**Path:** Building 220V → SP13 AC bulkhead → Surge suppressor → Mean Well SDR-120-12 → 12V DC

---

## Wire Color Code

| Color | Purpose |
|-------|---------|
| **Brown** | AC Line (220V hot) |
| **Blue (thick)** | AC Neutral |
| **Green/Yellow** | Earth ground (PE) |
| **Red** | 12V positive |
| **Black** | Ground (GND) |
| **Yellow** | 5V power (buck converter to Pi, Pi to relay VCC) |
| **Blue (thin)** | GPIO signal — relay IN1 (PoE switch, GPIO 24) |
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
| — | 9 | GND (SHT40, rain gauge, DS18B20) |
| GPIO 14 | 8 | UART TX → RG-15 RX |
| GPIO 15 | 10 | UART RX ← RG-15 TX |
| GPIO 18 | 12 | WS2812B data (status LED) |
| GPIO 23 | 16 | Available |
| GPIO 24 | 18 | Relay IN1 (PoE switch) |
| — | 20 | GND (relay module) |
| — | 25 | GND (buck converter) |

---

## Terminal Block (TB1) Labels

```
TB1 — 12V DISTRIBUTION (from PSU / Battery)
┌──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┐
│ 12V+ │ 12V+ │ 12V+ │ 12V+ │ GND  │ GND  │ GND  │ GND  │
│ F2   │ F3   │ F4   │ RG15 │      │      │      │      │
│(PoE) │(Pi)  │(Heat)│(pwr) │      │      │      │      │
└──────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┘
```

---

## Bulkhead Connectors (outside → inside)

| Connector | Type | Carries | Pin Map |
|-----------|------|---------|---------|
| SP13 | AC mains input | 220V AC (L, N, PE) | L / N / PE |
| CNLINKO | Ethernet IP67 | PoE camera | Standard RJ45 |
| SD16 4-pin | Rain gauge | 12V + GND + UART TX/RX | 1:12V, 2:GND, 3:TX→RX, 4:RX→TX |
| M16 | Ground cable | 6 AWG earth ground | Single conductor |

---

## Relay Channels

| CH | GPIO | Load | State when Pi is OFF |
|----|------|------|----------------------|
| 1 | GPIO 24 | PoE switch (camera) | **OFF** (fail-safe) |
| 2 | — | Available for future use | OFF |
| 3 | — | Available for future use | OFF |
| 4 | — | Available for future use | OFF |

All relays use **NO (Normally Open)** contacts. When the Pi loses power or
crashes, all relays open and all loads lose power. This prevents uncontrolled
battery drain on UPS power.

## Status LED

Single WS2812B (NeoPixel) RGB LED behind sealed acrylic light window.
Driven by 1 GPIO data pin + 5V power. No relay channels used.

| Color | Pattern | Meaning |
|-------|---------|---------|
| Green | Solid | System OK, idle |
| Blue | Solid | Capturing / uploading |
| Yellow | Solid | Warning (degraded) |
| Red | Solid | Error |
| Cyan | Solid | Maintenance mode active |
| White | Solid | Boot in progress |
| Green | Slow blink | OK, on battery/UPS |
| Red | Fast blink | Critical error |
| OFF | — | Pi is off / sleeping |

---

## Simplified Wiring Schematic

```
220V AC ──► SP13 bulkhead
                │
          Surge Suppressor (L, N, PE)
                │           PE ──► Ground bar ──► Ground rod
                │
          Mean Well SDR-120-12
          (88-264VAC → 12V DC)
                │
         ┌──────┼──────────────────────────────────────┐
         │      │                                      │
         │    TB1 12V bus                          LiFePO4
         │      │                                  Charger
         │      │                                      │
         │   ┌──┼──────┬──────┬──────┐            Battery
         │   │  │      │      │      │            100Ah
         │   │ [F1   [F2    [F3    [F4           (UPS backup)
         │   │ 15A]   5A]   5A]    5A]
         │   │  │      │      │      │
         │   │  │   Fuse    DDR    PTC heater
         │   │  │   holder  60G-5  + Fans
         │   │  │      │   (→5.1V)
         │   │  │   Relay     │
         │   │  │   CH1    Pi 5
         │   │  │      │
         │   │  │   PoE Switch
         │   │  │      │
         │   │  │      │
         │   │  │    Cam1
         │   │  │
         │  RG-15 12V (always on, through SD16 bulkhead)
```

---

## UPS Behavior

| Condition | What Happens |
|-----------|-------------|
| **AC present** | Mean Well powers loads, charger maintains battery |
| **AC fails** | Battery powers all loads through TB1 |
| **Battery low** | BMS disconnects to protect battery |
| **AC restored** | Mean Well resumes, charger recharges battery |

**Battery runtime:** ~39 hours at typical load (~33W)

---

## RTC (Witty Pi 5 HAT+)

- **Type:** CR2032 coin cell (non-rechargeable, on Witty Pi 5 board)
- **I2C address:** 0x51
- **Software:** `wp5` CLI, `wp5d` daemon (auto-starts at boot)
- **Pi 5 native RTC (J5):** Not used — ML-2020 connector failed on both boards
- **No `dtparam=rtc_bbat_vchg` needed** — Witty Pi 5 has its own RTC

---

## Climate Control

| Component | Function | Control |
|-----------|----------|---------|
| PTC heater (15W) | Reduces humidity in enclosure | Hygrostat (>70% RH) |
| Fans (2x 40 CFM) | Internal air circulation | Always on |
| Gore vents (2x M12) | Pressure equalization | Passive |
| SHT40 sensor | Internal temp/humidity monitoring | I2C to Pi |
| DS18B20 probe | External ambient temperature | 1-Wire to Pi |

---

## Power Button

The power button (Pi 5 J2 header) handles all power and maintenance functions:

- **Brief press:** power on (from halted) or clean shutdown (while running)
- **Long press (3 seconds):** enter maintenance mode (WiFi hotspot + SSH)
- **10-second hold:** force power off (if frozen)

## Maintenance Mode

1. Long press power button (3 seconds)
2. Pi starts WiFi hotspot
3. Connect to hotspot with laptop/phone
4. SSH to Pi for diagnostics

---

## Emergency Contacts

| Role | Name | Phone | Email |
|------|------|-------|-------|
| Project lead | | | |
| Local contact | | | |
| ORC support | | | |
