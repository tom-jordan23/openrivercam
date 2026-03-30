# Sukabumi Station — Enclosure Reference

**Print, laminate, and attach to the inside of the enclosure door.**

---

## Site Information

| Field | Value |
|-------|-------|
| Site | Sukabumi, Indonesia |
| Power | 12V Solar (existing 200W panel / 50Ah battery) |
| Station hostname | *(fill after install)* |
| Camera IP | 192.168.50.139 |
| Pi IP (camera network) | 192.168.50.1 |
| WiFi hotspot SSID | *(fill after install)* |
| WiFi hotspot password | *(fill after install)* |
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

**Replacement fuses:** 5x20mm, 5A, slow blow (time-delay). For ML or LIR
chemistry RTC battery replacement info, see GPIO_WIRING.md Step 8.

---

## Wire Color Code

| Color | Purpose |
|-------|---------|
| **Red** | 12V positive |
| **Black** | Ground (GND) |
| **Yellow** | 5V power (buck converter to Pi, Pi to relay VCC) |
| **Blue** | GPIO signal — relay IN1 (PoE switch, GPIO 24) |
| **Green** | GPIO signal — relay IN2 (Green LED, GPIO 17) |
| **Blue stripe** | GPIO signal — relay IN3 (Yellow LED, GPIO 27) |
| **Green stripe** | GPIO signal — relay IN4 (Red LED, GPIO 22) |

---

## GPIO Pin Assignments

| GPIO | Pin | Function |
|------|-----|----------|
| — | 2 | 5V power IN (from DDR-60G-5) |
| — | 4 | 5V power OUT (to relay VCC) |
| GPIO 2 | 3 | I2C SDA (SHT40 sensor) |
| GPIO 3 | 5 | I2C SCL (SHT40 sensor) |
| — | 9 | GND (SHT40, rain gauge) |
| GPIO 14 | 8 | UART TX → RG-15 RX |
| GPIO 15 | 10 | UART RX ← RG-15 TX |
| GPIO 17 | 11 | Relay IN2 (Green LED) |
| GPIO 22 | 15 | Relay IN4 (Red LED) |
| GPIO 23 | 16 | Available |
| GPIO 24 | 18 | Relay IN1 (PoE switch) |
| — | 20 | GND (relay module) |
| — | 25 | GND (buck converter) |
| GPIO 27 | 13 | Relay IN3 (Yellow LED) |

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
| 1 | GPIO 24 | PoE switch (camera) | **OFF** (fail-safe: camera unpowered) |
| 2 | — | Available for future use | OFF |
| 3 | — | Available for future use | OFF |
| 4 | — | Available for future use | OFF |

All relays use **NO (Normally Open)** contacts. When the Pi loses power or
crashes, all relays open and all loads lose power. This is intentional —
it prevents the camera from draining the solar battery.

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
| Green | Slow blink | OK, on battery (if applicable) |
| Red | Fast blink | Critical error |
| OFF | — | Pi is off / sleeping |

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
           GPIO TBD → WS2812B data (status LED)
```

---

## RTC Battery

- **Type:** ML-2020 (rechargeable manganese lithium, 3.0V)
- **Connector:** J5 (BAT) on Pi 5, between USB-C and HDMI
- **Charging:** Enabled via `/boot/firmware/config.txt`:
  `dtparam=rtc_bbat_vchg=3000000`
- **NEVER use CR2020/CR2032** (non-rechargeable — will leak if charged)

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
