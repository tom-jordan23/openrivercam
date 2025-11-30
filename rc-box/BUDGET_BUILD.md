# RC-Box Budget Build (<$500)

**Target:** Complete unit under $500 including Raspberry Pi 5
**Optimized for:** Cost, volunteer assembly, field serviceability

---

## Bill of Materials

### Core Electronics

| Component | Model | Cost | Notes |
|-----------|-------|------|-------|
| Raspberry Pi 5 (4GB) | - | $60 | 4GB sufficient for video capture |
| Power Management | PiSugar 3 Plus | $46 | RTC wake, integrated battery management |
| Storage | Kingston A400 480GB M.2 SATA + USB adapter | $35 | 3+ weeks storage |
| Cellular Modem | Quectel EC25 USB dongle | $35 | Multi-band LTE, global compatibility |

**Subtotal: $176**

### Camera System (Option A: Entaniya Housing + Heater Kit)

| Component | Model | Cost | Notes |
|-----------|-------|------|-------|
| Pi Camera V3 | Raspberry Pi Camera Module 3 (x2) | $50 | $25 each |
| USB Adapter | Arducam B0370 (x2) | $40 | CSI to USB3 |
| Camera Housing | Entaniya WC-01 (x2) | $160 | IP67, purpose-built for Pi Camera |
| Heater Kit | Keenovo 10W silicone pad + STC-1000 thermostat (x2) | $50 | Pre-wired kit, $25 each |
| Breather Vent | Gore PMF200408 or Nitto TEMISH (x2) | $20 | Pressure equalization |
| Desiccant | Type 4A Molecular Sieve 100g (x2) | $10 | Backup moisture control |

**Subtotal: $330**

### Camera System (Option B: Integrated USB Camera - Simpler)

| Component | Model | Cost | Notes |
|-----------|-------|------|-------|
| Weatherproof USB Camera | SVPRO IP66 1080P with heater mod (x2) | $100 | $50 each, add DIY heater |
| Heater Kit | Keenovo 10W pad + thermostat (x2) | $50 | External wrap or internal mod |
| Breather Vent | Gore/Nitto (x2) | $20 | Add to housing |

**Subtotal: $170** (saves $160 vs Option A, but lower image quality)

### Power System (Solar Configuration)

| Component | Model | Cost | Notes |
|-----------|-------|------|-------|
| Battery | LiFePO4 12V 20Ah | $80 | ~2 days autonomy with heaters |
| Solar Panel | 50W polycrystalline | $40 | Minimum for ~180Wh/day consumption |
| Charge Controller | PWM 10A | $12 | Basic, reliable |

**Subtotal: $132**

### Power System (Grid Configuration)

| Component | Model | Cost | Notes |
|-----------|-------|------|-------|
| Power Supply | Mean Well 12V 3A | $18 | Universal input |
| UPS Battery | LiFePO4 12V 6Ah | $35 | Graceful shutdown only |

**Subtotal: $53**

### Enclosure & Mounting

| Component | Model | Cost | Notes |
|-----------|-------|------|-------|
| Main Enclosure | Polycase WC-42 (10"x8"x6") | $35 | IP67 polycarbonate |
| Display | 1.3" I2C OLED (128x64) | $8 | Button-activated |
| Switches | 4x IP67 toggle switches | $16 | Power, mode, WiFi, reset |
| Status LEDs | 3x 10mm LEDs | $3 | Power, mode, network |
| Cable Glands | 6x PG9 IP67 | $12 | Camera cables, power, antenna |
| Pole Mount | Stainless hose clamps (x2) | $8 | 3-6" diameter |
| Camera Mounts | Ball head with 1/4-20 thread (x2) | $20 | Adjustable, lockable |
| Internal Mounting | Standoffs, foam, wire ties | $8 | Organization |
| Camera Cables | USB 3.0, 3m, waterproof ends (x2) | $24 | Shielded |

**Subtotal: $134**

---

## Total Cost Summary

### Option A: Pi Camera V3 + Entaniya Housing (Best Image Quality)

| Configuration | Cost |
|---------------|------|
| Core Electronics | $176 |
| Camera System (Option A) | $330 |
| Power - Solar | $132 |
| Enclosure & Mounting | $134 |
| **TOTAL (Solar)** | **$772** |
| **TOTAL (Grid)** | **$693** |

**Over budget by $272-293.** Need to cut costs.

### Option B: Integrated USB Camera (Simpler, Lower Quality)

| Configuration | Cost |
|---------------|------|
| Core Electronics | $176 |
| Camera System (Option B) | $170 |
| Power - Solar | $132 |
| Enclosure & Mounting | $134 |
| **TOTAL (Solar)** | **$612** |
| **TOTAL (Grid)** | **$533** |

**Still over budget by $33-112.**

---

## Cost Reduction Options

### To hit $500 target, choose from:

| Cut | Savings | Trade-off |
|-----|---------|-----------|
| Use 2GB Pi 5 instead of 4GB | $10 | Minimal impact |
| Use single camera instead of two | $85-165 | Reduced coverage/stereo capability |
| Smaller battery (12V 10Ah) | $30 | ~1 day autonomy |
| Smaller solar panel (30W) | $15 | Marginal in cloudy conditions |
| Skip display, LEDs only | $8 | Less status info |
| Cheaper enclosure | $15 | May sacrifice IP rating |
| DIY heater (resistors) instead of kit | $30 | Requires assembly skill |

---

## Recommended Budget Build ($499 Solar / $420 Grid)

**Compromise:** Single camera for proof-of-concept, option to add second later.

| Component | Model | Cost |
|-----------|-------|------|
| **Core Electronics** | | |
| Raspberry Pi 5 (4GB) | - | $60 |
| PiSugar 3 Plus | - | $46 |
| Kingston A400 480GB + USB adapter | - | $35 |
| Quectel EC25 USB modem | - | $35 |
| **Camera System (1 camera)** | | |
| Pi Camera V3 | - | $25 |
| Arducam B0370 USB adapter | - | $20 |
| Entaniya WC-01 housing | - | $80 |
| Keenovo heater + thermostat kit | - | $25 |
| Gore vent + desiccant | - | $15 |
| **Power (Solar)** | | |
| LiFePO4 12V 15Ah | - | $65 |
| 40W solar panel | - | $35 |
| PWM 10A controller | - | $12 |
| **Enclosure & Mounting** | | |
| Polycase WC-42 | - | $35 |
| 1.3" OLED display | - | $8 |
| 4x IP67 switches | - | $16 |
| 3x LEDs | - | $3 |
| Cable glands, mounts, cables | - | $44 |
| **TOTAL (Solar, 1 camera)** | | **$499** |
| **TOTAL (Grid, 1 camera)** | | **$420** |

### To add second camera later: +$165

---

## Alternative: Dual Camera Budget Build ($489)

**Use cheaper USB cameras instead of Pi Camera + Entaniya:**

| Component | Model | Cost |
|-----------|-------|------|
| **Core Electronics** | | $176 |
| **Camera System** | | |
| SVPRO IP66 USB Camera (x2) | - | $100 |
| DIY heater wrap (resistor-based, x2) | - | $20 |
| Gore vent (x2) | - | $20 |
| **Power (Solar)** | | |
| LiFePO4 12V 15Ah | - | $65 |
| 40W solar panel | - | $35 |
| PWM 10A controller | - | $12 |
| **Enclosure & Mounting** | | $126 |
| **TOTAL (Solar, 2 cameras)** | | **$489** |

**Trade-off:** Lower image quality (1080P USB vs 12MP Pi Camera), but:
- Two cameras included
- No housing assembly required
- Simpler for volunteers
- Under $500

---

## Anti-Fog Solution Summary

All configurations include active anti-fog:

| Component | Purpose | Field Service |
|-----------|---------|---------------|
| Keenovo silicone heater OR resistor wrap | Keeps lens above dew point | Replace if failed |
| STC-1000 thermostat | Auto on/off at 25°C | Adjust setpoint if needed |
| Gore/Nitto breather vent | Pressure equalization | No maintenance |
| Type 4A molecular sieve | Backup moisture control | Replace every 6 months |

**Power draw:** ~5-10W per camera when heating (thermostat-controlled)
**Effectiveness:** 95%+ fog-free in tropical conditions

---

## Recommendation

**For proof-of-concept / limited budget:**
- Single Pi Camera V3 + Entaniya housing: **$499 solar**
- Best image quality, add second camera when budget allows

**For maximum simplicity / volunteer deployment:**
- Dual SVPRO USB cameras with heater mod: **$489 solar**
- Lower image quality but easier assembly, two cameras included

**Question for you:**
1. Is single camera acceptable for initial deployment?
2. Is lower image quality (1080P USB) acceptable if it means simpler assembly and two cameras?
