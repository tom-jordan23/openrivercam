# Camera Options for RC-Box

**Updated:** 2026-01-06

---

## The Problem

We need sealed cameras that won't die in Indonesia. Our Indonesia deployment proved that humidity kills - we fried a unit when moisture condensed inside the camera bay after it was opened in 90%+ humidity. Cameras must be **factory sealed** - no field assembly, no desiccant maintenance, no "IP67 equivalent" housings that require careful sealing.

At the same time, power drives cost for solar sites. PoE cameras draw 10-12W each, which means bigger solar panels, bigger batteries, and higher unit costs. Every extra $100 in power system cost means fewer units deployed.

Unfortunately, there's no camera on the market that is factory-sealed, high-resolution, low-power, AND tropical-rated. Something has to give.

---

## Deployment Configurations

### Camera Count

| Configuration | Use Case | Camera Cost |
|---------------|----------|-------------|
| **2 cameras** | Stereo coverage, redundancy, wider field of view | 2× per-camera cost |
| **1 camera** | Budget-constrained, simple sites, adequate single-view coverage | 1× per-camera cost |

Single-camera deployment cuts camera costs in half and reduces power by ~40% (one less camera, smaller PoE injector or simpler USB setup). For sites where one camera provides adequate coverage, this is an easy cost save.

**Software note:** With 2 cameras, day and night settings can be applied to separate cameras. With a single camera, **ORC software may require modification** to dynamically switch between day and night capture settings on the same camera. This should be validated before committing to single-camera deployments with IR night monitoring.

### Power Source

| Configuration | Use Case | Power System Cost |
|---------------|----------|-------------------|
| **Solar** | Remote sites, no utility power | $230-580 depending on load |
| **Commercial (AC)** | Sites with 110V or 220V utility power | ~$100-150 |

**Commercial power simplifies everything.** If utility power is available, the power system becomes a basic AC-DC supply plus small UPS for brownouts. Camera power consumption becomes irrelevant - you can run PoE cameras 24/7 without worrying about solar panel sizing.

**Commercial power components:**
- Mean Well or similar industrial AC-DC supply (12V/10A or 24V/5A): ~$40-60
- Small UPS or supercapacitor backup for brief outages: ~$50-80
- Surge protector (essential in developing countries): ~$20-30
- Total: **~$100-150**

For sites with commercial power, **PoE cameras are the obvious choice** - proven, factory sealed, IR-capable, and power consumption doesn't matter.

---

## What We Need

| Requirement | Priority | Notes |
|-------------|----------|-------|
| Factory sealed IP67+ | **Critical** | Non-negotiable after Indonesia failure |
| 8MP resolution | High | Originally 12MP, flexible to 8MP |
| Operating temp ≥40°C | High | Indonesia regularly hits 35-40°C |
| Low power | High | Drives solar/battery sizing |
| Pi-controllable | High | Must trigger capture on schedule |
| Low unit cost | High | More units = more coverage |

---

## The Options

### Option 1: PoE IP Cameras (24/7 with IR)

**The proven path.** Factory-sealed surveillance cameras with integrated IR, running continuously.

| Spec | Value |
|------|-------|
| Cameras | ANNKE C1200 or similar 4K/8MP, $110-130 each |
| Sealed | IP67, factory |
| Temp range | -30°C to +60°C |
| Power | 10-12W each (with IR) |
| Control | RTSP stream, standard |
| IR | Integrated, 30-50m range typical |

**Power budget (24/7, IR enabled):**

| Component | 2-Camera | 1-Camera |
|-----------|----------|----------|
| Cameras | 24W (576 Wh) | 12W (288 Wh) |
| PoE injector | 3W (72 Wh) | 2W (48 Wh) |
| Pi (duty cycle) | 5W × 6h (30 Wh) | 5W × 6h (30 Wh) |
| Witty Pi | 0.5W (12 Wh) | 0.5W (12 Wh) |
| Modem | 2W (48 Wh) | 2W (48 Wh) |
| **Daily Total** | **~740 Wh** | **~430 Wh** |

**Solar system sizing:**

| Config | Solar Panel | Battery | PoE Injector | Camera Cost | Total |
|--------|-------------|---------|--------------|-------------|-------|
| 2 cameras | 300W ($180) | 200Ah ($400) | 2-port ($164) | $260 | **~$1,000** |
| 1 camera | 200W ($120) | 100Ah ($250) | Single ($40) | $130 | **~$540** |

**Why choose this:**
- Proven technology, no surprises
- Industrial temp range handles Indonesia
- Simple RTSP integration with ORC
- Factory sealed, no assembly risk
- IR-ready for night monitoring
- Cameras stay powered = 6-10 year lifespan (no power cycling wear)

**Why not:**
- Highest power consumption
- Most expensive power system
- Needs 12V→48V PoE conversion

**Risk: LOW**

---

### Option 2: GoPro Hero 13 + Labs Firmware

**Would be great if it didn't overheat.**

| Spec | Value |
|------|-------|
| Camera | GoPro Hero 13, ~$400 each |
| Sealed | IP68 to 10m, factory |
| Temp range | **-10°C to 35°C** |
| Power | ~5W recording |
| Control | BLE/WiFi via Open GoPro SDK |

**The problem:** Indonesia regularly exceeds 35°C. GoPro will overheat and shut down. This isn't a reliability concern - it's a guaranteed failure mode. GoPro's own documentation says the camera shuts down at 50°C internal temp, which is easily reached in direct sunlight at 35°C+ ambient.

Also:
- USB power trigger has reliability issues (voltage drops, power bank quality)
- Control requires BLE/WiFi, not wired
- No direct video capture over USB

**Total camera + power system: ~$1,030**

**Risk: HIGH** - Temperature incompatibility is a showstopper

---

### Option 3: DJI Osmo Action 5 Pro

**Better temp tolerance, but no Python SDK.**

| Spec | Value |
|------|-------|
| Camera | DJI Osmo Action 5 Pro, ~$350 each |
| Sealed | IP68 to 20m, factory |
| Temp range | **-20°C to 45°C** |
| Power | ~5W recording |
| Control | BLE via DJI R SDK (ESP32 only) |

**The good:** 45°C operating temp actually works for Indonesia. Best thermal management of any action camera - can record 4K/60 continuously without overheating.

**The bad:** No Python SDK. DJI only provides an ESP32 demo using their proprietary BLE protocol. You'd need to either:
- Build a custom ESP32 bridge that Pi controls via serial
- Reverse-engineer the protocol for Python

Also, USB power may still drain the internal battery (not true pass-through charging).

**Total camera + power system: ~$980**

**Risk: MEDIUM-HIGH** - Significant development effort for BLE integration

---

### Option 4: Insta360 Ace Pro 2 (USB Webcam Mode)

**Interesting angle - may work as a UVC device.**

| Spec | Value |
|------|-------|
| Camera | Insta360 Ace Pro 2, ~$400 each |
| Sealed | IP68 to 12m, factory |
| Temp range | **-20°C to 45°C** |
| Power | ~2-3W in webcam mode (estimated) |
| Control | USB (appears as UVC webcam) |

**The idea:** Insta360 has a USB webcam mode that presents the camera as a standard UVC device. If it works on the Pi, we could capture directly with `ffmpeg` - no API needed.

**The catch:** Webcam mode is limited to **1080p30 (2MP)**. That's a big step down from 8MP.

**Unknowns:**
- Does it actually work on Raspberry Pi?
- Can it run continuously on USB power?
- Does it survive power cycling?
- Will it overheat at 40°C+ ambient?

**Total camera + power system: ~$1,030**

**Risk: MEDIUM** - Needs testing, and resolution is a significant tradeoff

---

### Option 5: Industrial Nitrogen-Purged Housing + USB Camera

**Factory-sealed the industrial way.**

| Spec | Value |
|------|-------|
| Camera | 4K/8MP USB camera module, ~$50-70 each |
| Housing | Industrial nitrogen-purged enclosure, ~$200-400 each |
| Sealed | IP67/IP68, factory nitrogen fill |
| Temp range | -40°C to +60°C typical |
| Power | ~1W per camera |
| Control | USB (UVC) |

**The idea:** Industrial camera housings used in offshore, marine, and harsh environments are factory-sealed with nitrogen purge. Nitrogen displaces moisture entirely - no humidity, no condensation, ever. These are used on oil rigs, ships, and in corrosive industrial environments.

**How it works:**
- Housing is assembled in controlled environment
- Purged with dry nitrogen gas
- Sealed with industrial-grade gaskets
- Pressure-tested before shipping
- Some include pressure relief valves with desiccant backup

**Vendors to investigate:**
- Videotec (NXW series) - stainless steel, IP66/67/68/69
- Pelco (ExSite series) - explosion-proof, nitrogen-purged
- Axis (industrial housings) - some models nitrogen-compatible
- Dotworkz (D2/D3 series) - climate-controlled housings

**The catch:**
- Expensive ($200-500 per housing, plus camera)
- May be overkill for this application
- Need to verify USB camera compatibility
- Some are designed for specific camera models

**Total camera + power system: ~$700-1,100**

**Why consider this:**
- True factory seal with nitrogen = zero humidity risk
- Industrial temp range
- Proven in much harsher environments than river monitoring
- Could use lower-power USB cameras inside

**Why not:**
- Cost approaches PoE cameras anyway
- More complex sourcing
- May need custom integration

**Risk: MEDIUM** - Proven technology, but integration effort unknown

---

## Comparison

### Specs

| Option | Resolution | Sealed | Temp Range | Power | Control |
|--------|------------|--------|------------|-------|---------|
| PoE IP Camera (24/7) | 8-12MP | IP67 | -30 to 60°C | 24W | RTSP |
| GoPro Hero 13 | 27MP | IP68 | -10 to 35°C | 5W | BLE/WiFi |
| DJI Osmo Action 5 | 40MP | IP68 | -20 to 45°C | 5W | BLE (ESP32) |
| Insta360 Ace Pro 2 | **2MP*** | IP68 | -20 to 45°C | 2.5W | USB/UVC |
| N2-Purged Housing + USB | 8MP | IP67/68 | -40 to 60°C | 2W | USB/UVC |

*Webcam mode only; native is 50MP

### Cost (Solar Power)

**2-Camera Configuration:**

| Option | Cameras (×2) | Power System | Total |
|--------|--------------|--------------|-------|
| PoE IP Camera (24/7) | $260 | $580 | **$840** |
| GoPro Hero 13 | $800 | $230 | $1,030 |
| DJI Osmo Action 5 | $700 | $230 | $930 |
| Insta360 Ace Pro 2 | $800 | $230 | $1,030 |
| N2-Purged Housing + USB | $500-940 | $230 | $730-1,170 |

**1-Camera Configuration:**

| Option | Camera (×1) | Power System | Total |
|--------|-------------|--------------|-------|
| PoE IP Camera (24/7) | $130 | $420 | **$550** |
| GoPro Hero 13 | $400 | $200 | $600 |
| DJI Osmo Action 5 | $350 | $200 | $550 |
| Insta360 Ace Pro 2 | $400 | $200 | $600 |
| N2-Purged Housing + USB | $250-470 | $200 | $450-670 |

### Cost (Commercial AC Power)

**2-Camera Configuration:**

| Option | Cameras (×2) | Power System | Total |
|--------|--------------|--------------|-------|
| PoE IP Camera (24/7) | $260 | $120 | **$380** |
| GoPro Hero 13 | $800 | $120 | $920 |
| DJI Osmo Action 5 | $700 | $120 | $820 |
| Insta360 Ace Pro 2 | $800 | $120 | $920 |
| N2-Purged Housing + USB | $500-940 | $120 | $620-1,060 |

**1-Camera Configuration:**

| Option | Camera (×1) | Power System | Total |
|--------|-------------|--------------|-------|
| PoE IP Camera (24/7) | $130 | $100 | **$230** |
| GoPro Hero 13 | $400 | $100 | $500 |
| DJI Osmo Action 5 | $350 | $100 | $450 |
| Insta360 Ace Pro 2 | $400 | $100 | $500 |
| N2-Purged Housing + USB | $250-470 | $100 | $350-570 |

**Summary:** Single PoE camera + commercial power = **~$230**. That's the floor for a reliable, factory-sealed deployment.

### Risk

| Option | Tech Risk | Field Risk | Dev Risk | Overall |
|--------|-----------|------------|----------|---------|
| PoE IP Camera (24/7) | Low | Low | None | **LOW** |
| GoPro Hero 13 | Medium | **High** (temp) | Low | **HIGH** |
| DJI Osmo Action 5 | Medium | Low | **High** | **MEDIUM-HIGH** |
| Insta360 Ace Pro 2 | Medium | Low | Medium | **MEDIUM** |
| N2-Purged Housing + USB | Low | Low | Medium | **MEDIUM** |

---

## Recommendations

### Sites with commercial power (110V/220V)

**PoE IP cameras. No question.**

When utility power is available, the calculus is simple. PoE cameras are the cheapest, most reliable option. Power consumption doesn't matter. You get factory-sealed IP67, industrial temp range, integrated IR, and proven RTSP integration.

**2-Camera Setup:**

| Component | Cost |
|-----------|------|
| 2× PoE cameras (8MP, IR) | $260 |
| PoE injector (2-port) | $164 |
| AC-DC supply (12V) | $50 |
| UPS/surge protection | $70 |
| **Total** | **~$550** |

**1-Camera Setup:**

| Component | Cost |
|-----------|------|
| 1× PoE camera (8MP, IR) | $130 |
| PoE injector (single) | $40 |
| AC-DC supply (12V) | $40 |
| Surge protection | $30 |
| **Total** | **~$240** |

Single camera + commercial power is the **lowest-cost reliable deployment** at ~$240.

**Risk: LOW**

---

### Solar sites - if reliability is the priority

**Go with PoE IP cameras (Option 1).**

Accept the higher power system cost for proven, factory-sealed cameras with industrial temperature ratings. Cameras run 24/7 with IR enabled - ready for night monitoring when ORC supports it.

This is the safe choice. No development risk, no field assembly risk, no temperature surprises. Continuous operation also means 6-10 year camera lifespan (no power cycling wear).

| Configuration | Cameras | Solar | Battery | Total |
|---------------|---------|-------|---------|-------|
| 2 cameras | $260 | 300W ($180) | 200Ah ($400) | **~$840** |
| 1 camera | $130 | 200W ($120) | 100Ah ($250) | **~$550** |

**Risk: LOW**

---

### Solar sites - if you want to try for cost savings

**Test the Insta360 Ace Pro 2 (Option 4) before committing.**

Buy one camera (~$400) and validate:
1. Does USB webcam mode work on Raspberry Pi?
2. Can it run continuously on USB power without draining battery?
3. Does it survive power cycling (boot on USB power)?
4. Does it overheat at 40°C+ ambient (test in hot car or oven)?

If all four pass, you have a factory-sealed, low-power option with simple USB integration. Resolution drops to 1080p, but that may be acceptable.

If any fail, fall back to PoE cameras.

**Test cost: ~$400 | Potential savings: ~$200-400/unit on power system**

---

### Worth investigating

**N2-Purged Housing + USB Camera (Option 5)**

If you want lower power than PoE but more reliability than action cameras, industrial nitrogen-purged housings are worth a look. The sealing approach is proven in offshore/marine environments far harsher than river monitoring. Cost overlaps with PoE cameras, but power consumption is much lower.

Next step: Get quotes from Videotec, Dotworkz, or similar vendors. Confirm USB camera compatibility.

---

### Not recommended

- **GoPro Hero 13:** Temperature limit (35°C) is incompatible with Indonesia
- **DJI Osmo Action 5:** Development effort for BLE integration is too high

---

## Next Steps

1. **If proceeding with PoE cameras:**
   - Source 4K/8MP cameras with good IR range (30m+)
   - Verify RTSP compatibility with ORC
   - Update BOM for Indonesia rainy season (300W panel, 200Ah battery)
   - Test IR image quality for river surface detection

2. **If testing Insta360:**
   - Order one Insta360 Ace Pro 2 (~$400)
   - Test USB webcam mode on Pi
   - Test continuous power operation
   - Test high-temp survival (40°C+)
   - Note: No IR capability - night monitoring would require separate IR illuminator
   - Document results before committing

3. **If investigating N2-purged housings:**
   - Contact Videotec, Dotworkz, Pelco for quotes on nitrogen-purged housings
   - Confirm compatibility with 4K USB camera modules
   - Ask about IR window options for night monitoring
   - Get lead times and MOQs
   - Compare total cost vs PoE camera approach

---

## References

- [GoPro Labs USB Power Trigger](https://gopro.github.io/labs/control/usb/)
- [Open GoPro Python SDK](https://gopro.github.io/OpenGoPro/python_sdk/)
- [DJI Osmo Action 5 Pro Specs](https://www.dji.com/osmo-action-5-pro/specs)
- [DJI R SDK (ESP32)](https://github.com/dji-sdk/Osmo-GPS-Controller-Demo)
- [Insta360 Ace Pro 2 Webcam Mode](https://onlinemanual.insta360.com/acepro2/en-us/camera/appuse/webcammode)
- [Entaniya WC-01 Housing](https://thepihut.com/products/entaniya-waterproof-case-for-raspberry-pi-camera-modules)
- [IPVM Camera Power Consumption Testing](https://ipvm.com/reports/ip-camera-power-use-rankings)
