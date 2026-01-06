# Camera Options for RC-Box

**Updated:** 2026-01-06

---

## The Problem

We need sealed cameras that won't die in Indonesia. Our Indonesia deployment proved that humidity kills - we lost a unit when moisture condensed inside the camera bay after it was opened in 90%+ humidity. Cameras must be **factory sealed** - no field assembly, no desiccant maintenance, no "IP67 equivalent" housings that require careful sealing.

At the same time, power drives cost for solar sites. PoE cameras draw 10-12W each, which means bigger solar panels, bigger batteries, and higher unit costs. Higher unit costs for power system cost means fewer units deployed.

No camera on the market is factory-sealed, high-resolution, low-power, AND tropical-rated. We have to make tradeoffs.

---

## Deployment Configurations

### Camera Count

| Configuration | Use Case | Camera Cost |
|---------------|----------|-------------|
| **2 cameras** | Stereo coverage, redundancy, wider field of view | 2× per-camera cost |
| **1 camera** | Budget-constrained, simple sites, adequate single-view coverage | 1× per-camera cost |

Single-camera deployment cuts camera costs in half and reduces power by ~40% (one less camera, smaller PoE injector or simpler USB setup). For sites where one camera provides adequate coverage, this reduces costs significantly.

**Software note:** With 2 cameras, day and night settings can be applied to separate cameras. With a single camera, **ORC software may require modification** to dynamically switch between day and night capture settings on the same camera. This should be validated before committing to single-camera deployments with IR night monitoring.

### Power Source

| Configuration | Use Case | Power System Cost |
|---------------|----------|-------------------|
| **Solar** | Remote sites, no utility power | $230-580 depending on load |
| **Commercial (AC)** | Sites with 110V or 220V utility power | ~$100-150 |

**Commercial power simplifies the design.** If utility power is available, the power system becomes a basic AC-DC supply plus small UPS for brownouts. Camera power consumption becomes irrelevant - you can run PoE cameras 24/7 without worrying about solar panel sizing.

**Commercial power components:**
- Mean Well or similar industrial AC-DC supply (12V/10A or 24V/5A): ~$40-60
- Small UPS or supercapacitor backup for brief outages: ~$50-80
- Surge protector (essential in developing countries): ~$20-30
- Total: **~$100-150**

For sites with commercial power, **PoE cameras make the most sense** - proven, factory sealed, IR-capable, and power consumption doesn't matter.

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
| Cameras | [ANNKE C1200](https://www.annke.com/products/c1200-12mp-poe-ip-camera) or [Reolink RLC-810A](https://reolink.com/us/product/rlc-810a/), $110-150 each |
| Sealed | IP67, factory |
| Temp range | -30°C to +60°C |
| Power | 10-12W each (with IR) |
| Control | RTSP stream, standard |
| IR | Integrated, 30-50m range typical |
| PoE Injector | [Planet IPOE-260-12V](https://www.amazon.com/dp/B0B5LXKZ7P) (12V to 48V), ~$40-164 |

**Why run 24/7 instead of duty cycling?**

PoE IP cameras are designed for continuous operation. Power cycling them creates problems:

- **Startup delay:** Cameras take 15-45 seconds to boot, initialize sensors, and establish network connection. If you're capturing on a schedule, you lose the first part of each window.
- **Mechanical wear:** Each power cycle stresses internal components - capacitors, voltage regulators, moving IR-cut filters. Cameras rated for 10+ years continuous operation may fail in 2-3 years with frequent cycling.
- **PoE negotiation:** The 802.3af/at handshake between injector and camera adds latency and can fail intermittently, especially with long cable runs or cheap injectors.
- **IR calibration:** Some cameras recalibrate IR LEDs on startup, causing inconsistent illumination in early frames.

Running continuously avoids all of this. The tradeoff is higher power consumption, which drives up solar/battery costs.

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

**Advantages:**
- Proven technology
- Industrial temp range handles Indonesia
- Simple RTSP integration with ORC
- Factory sealed, no assembly risk
- IR-ready for night monitoring
- Cameras stay powered = 6-10 year lifespan (no power cycling wear)

**Challenges:**
- Highest power consumption
- Most expensive power system
- Needs 12V→48V PoE conversion

**Risk: LOW**

---

### Option 2: Action Cameras (GoPro, DJI, Insta360)

**Factory sealed and low power, but each has significant drawbacks.**

Action cameras are attractive because they're factory-sealed IP68, relatively low power (~3-5W), and designed for outdoor use. We evaluated three options:

| Camera | Price | Temp Range | Control | Main Problem |
|--------|-------|------------|---------|--------------|
| [GoPro Hero 13](https://gopro.com/en/us/shop/cameras/hero13-black/CHDHX-131-master.html) | ~$400 | -10 to 35°C | BLE/WiFi via [Open GoPro SDK](https://gopro.github.io/OpenGoPro/python_sdk/) | **Overheats above 35°C** |
| [DJI Osmo Action 5 Pro](https://store.dji.com/product/osmo-action-5-pro) | ~$350 | -20 to 45°C | BLE via [ESP32 SDK](https://github.com/dji-sdk/Osmo-GPS-Controller-Demo) | **No Python SDK** |
| [Insta360 Ace Pro 2](https://store.insta360.com/product/ace-pro-2) | ~$400 | -20 to 45°C | USB ([UVC webcam mode](https://onlinemanual.insta360.com/acepro2/en-us/camera/appuse/webcammode)) | **1080p only in webcam mode** |

**Why we're not pursuing this path:**

- **GoPro:** 35°C max operating temp is incompatible with Indonesia. Camera shuts down at 50°C internal temp, easily reached in direct sunlight. Also requires BLE/WiFi control (not wired), and USB power trigger has reliability issues.

- **DJI:** Better thermal management (45°C), but no Python SDK. Would need to build custom ESP32 bridge or reverse-engineer their proprietary BLE protocol. Too much development effort.

- **Insta360:** Has USB webcam mode that works as standard UVC device, but limited to 1080p30 (2MP). Too big a resolution tradeoff from our 8MP target. Also untested on Pi, unknown thermal behavior at 40°C+.

All three also lack integrated IR for night monitoring.

**Total camera + power system: ~$930-1,030**

**Risk: HIGH** - Temperature, SDK, or resolution issues make these unsuitable

---

### Option 3: Machine Vision Housing + Gore Vent + USB Camera

**Good sealing at low cost, but requires assembly.**

| Spec | Value |
|------|-------|
| Camera | [ELP 4K USB](https://www.amazon.com/dp/B08R5TCMQG) or [Arducam 8MP](https://www.arducam.com/product/8mp-1080p-usb-camera-module-1-4-cmos-imx219-mini-uvc-usb2-0-webcam-board-with-1-64ft-0-5m-usb-cable-for-windows-linux-android-and-mac-os/), ~$50-70 each |
| Housing | [VA Imaging MVEC167](https://va-imaging.com/en-us/products/machine-vision-camera-housing-enclosure-waterproof-ip67) or [Entaniya WC-01](https://thepihut.com/products/entaniya-waterproof-case-for-raspberry-pi-camera-modules), ~$60-150 each |
| Gore Vent | [GORE Protective Vent](https://www.gore.com/products/gore-protective-vents) (M12 screw-in), ~$10-15 each |
| Sealed | IP67, with Gore vent for pressure equalization |
| Temp range | -20°C to +60°C |
| Power | ~1W per camera |
| Control | USB (UVC) |

True nitrogen-purged housings cost $500-5,000+ (Dotworkz, Pelco, 2bSecurity). Gore protective vents + desiccant provide equivalent moisture protection at a fraction of the cost.

**How Gore vents work:**
- ePTFE membrane allows continuous pressure equalization
- Blocks liquid water while allowing vapor transport
- Prevents condensation from temperature cycling
- No maintenance, no refilling, $5-15 per vent
- Used in industrial applications for decades

For tropical sites with big temperature swings, continuous pressure equalization matters more than initial nitrogen fill.

**Configurations:**

| Config | Housing | Vent | Desiccant | Total Housing Cost |
|--------|---------|------|-----------|-------------------|
| Budget | Entaniya WC-01 ($25-45) | Gore snap-in ($10) | 40g silica ($12) | **~$50-70** |
| Standard | VA Imaging MVEC167 (~$100) | Gore screw-in ($12) | 100g silica ($20) | **~$130-150** |

**VA Imaging advantages:**
- Aluminum construction = excellent heat dissipation (critical for tropics)
- IP67 tested specifically with USB3 cables
- Supports cameras up to 29x29mm
- Mount to metal structure for temps >35°C

**Entaniya advantages:**
- Lowest cost option
- Proven with Raspberry Pi cameras
- Compact form factor
- Good for prototypes or budget deployments

**Total system cost (1 camera, solar):**

| Config | Camera | Housing | Power System | Total |
|--------|--------|---------|--------------|-------|
| Entaniya + USB | $60 | $60 | $200 | **~$320** |
| VA Imaging + USB | $60 | $140 | $200 | **~$400** |

**Advantages:**
- Significant cost savings vs PoE cameras on solar deployments
- Gore vents are proven moisture management technology
- Low power (~1W vs 12W for PoE)
- Smaller solar/battery system
- Aluminum housing handles tropical heat

**Challenges:**
- Requires assembly (housing + vent + desiccant + camera)
- Not factory sealed - assembled in controlled environment
- No integrated IR (need separate illuminator for night)
- Quarterly desiccant checks recommended
- Less proven than off-the-shelf PoE cameras

**Risk: MEDIUM** - Proven components, but requires careful assembly and testing

**Vendors:**
- VA Imaging: [va-imaging.com](https://va-imaging.com/en-us/products/machine-vision-camera-housing-enclosure-waterproof-ip67)
- Entaniya: [thepihut.com](https://thepihut.com/products/entaniya-waterproof-case-for-raspberry-pi-camera-modules) or [e-products.entaniya.co.jp](https://e-products.entaniya.co.jp/en/list/cube-case/waterproof-camera-cases-items/wp-camera-case-100/)
- Gore vents: [Digi-Key](https://www.digikey.com/en/products/filter/vents/779) or [Mouser](https://www.mouser.com/c/?q=gore%20vent)
- Desiccant: [Camtraptions](https://store.camtraptions.com/products/reusable-silica-moisture-absorbing-pack) or [Dry-Packs](https://www.amazon.com/Dry-Packs-Camera-Moisture-Absorbing-Indicating/dp/B004AR1S3M)
- USB Cameras: [ELP Camera Store](https://www.amazon.com/stores/page/F0903B26-79A9-4E82-B6A3-52EA55C0C0E9) or [Arducam](https://www.arducam.com/product-category/usb-camera/)

---

### Option 4: Industrial Nitrogen-Purged Housing + USB Camera

**Best moisture protection, but expensive and overkill for most sites.**

| Spec | Value |
|------|-------|
| Camera | 4K/8MP USB camera module, ~$50-70 each |
| Housing | [Dotworkz D2 Heater/Blower](https://shop.dotworkz.com/products/dotworkz-d2-heater-blower-camera-enclosure-ip68-with-poe), $600-850 each |
| Sealed | IP68, IK10, nitrogen-pressurized |
| Temp range | -40°C to +60°C |
| Power | ~2W camera + 5-25W heater/blower |
| Control | USB (UVC) |

Nitrogen-purged housings from [Dotworkz](https://dotworkz.com/), [2bSecurity](https://www.2bsecurity.com/), and [Videotec/Pelco](https://www.pelco.com/videotec) use factory nitrogen pressurization to eliminate moisture. These are proven in offshore oil platforms, marine environments, and arctic deployments.

Features: IP68 submersible, IK10 impact resistance, active heater/blower, 20+ year track records.

**Typical costs:**
- Dotworkz D2 Base: $525-600
- Dotworkz D2 with Heater/Blower: $600-850
- 2bSecurity PH-850/PH-860: $500-1,500+ (316L stainless, quote required)
- Custom USB camera adapter: $50-100

**Tradeoffs:**
- Proven in harsh environments, no maintenance
- But 3-5× the cost of Gore vent approach
- Heater/blower draws 5-25W (problematic for solar)
- Still needs custom USB camera mounting

**Risk: LOW** (proven tech, high cost)

**Vendors:**
- Dotworkz: [shop.dotworkz.com](https://shop.dotworkz.com/)
- 2bSecurity: [www.2bsecurity.com](https://www.2bsecurity.com/)
- Pelco/Videotec: [www.pelco.com](https://www.pelco.com/products/accessories/camera-enclosures)

---

## Comparison

### Specs

| Option | Resolution | Sealed | Temp Range | Power | Control |
|--------|------------|--------|------------|-------|---------|
| PoE IP Camera (24/7) | 8-12MP | IP67 | -30 to 60°C | 24W | RTSP |
| Action Cameras | 2-40MP* | IP68 | -20 to 45°C | 3-5W | BLE/USB |
| Gore Vent Housing + USB | 8MP | IP67 | -20 to 60°C | 2W | USB/UVC |
| Nitrogen-Purged (Dotworkz) | 8MP | IP68/IK10 | -40 to 60°C | 2W | USB/UVC |

*Resolution varies by model and mode; Insta360 webcam mode limited to 2MP

### Cost (Solar Power)

**2-Camera Configuration:**

| Option | Cameras (×2) | Power System | Total |
|--------|--------------|--------------|-------|
| PoE IP Camera (24/7) | $260 | $580 | **$840** |
| Action Cameras | $700-800 | $230 | $930-1,030 |
| Gore Vent (Entaniya) + USB | $240 | $230 | **$470** |
| Gore Vent (VA Imaging) + USB | $400 | $230 | **$630** |
| Nitrogen-Purged (Dotworkz) + USB | $1,400-1,840 | $230 | $1,630-2,070 |

**1-Camera Configuration:**

| Option | Camera (×1) | Power System | Total |
|--------|-------------|--------------|-------|
| PoE IP Camera (24/7) | $130 | $420 | **$550** |
| Action Cameras | $350-400 | $200 | $550-600 |
| Gore Vent (Entaniya) + USB | $120 | $200 | **$320** |
| Gore Vent (VA Imaging) + USB | $200 | $200 | **$400** |
| Nitrogen-Purged (Dotworkz) + USB | $700-920 | $200 | $900-1,120 |

### Cost (Commercial AC Power)

**2-Camera Configuration:**

| Option | Cameras (×2) | Power System | Total |
|--------|--------------|--------------|-------|
| PoE IP Camera (24/7) | $260 | $120 | **$380** |
| Action Cameras | $700-800 | $120 | $820-920 |
| Gore Vent (Entaniya) + USB | $240 | $120 | **$360** |
| Gore Vent (VA Imaging) + USB | $400 | $120 | **$520** |
| Nitrogen-Purged (Dotworkz) + USB | $1,400-1,840 | $120 | $1,520-1,960 |

**1-Camera Configuration:**

| Option | Camera (×1) | Power System | Total |
|--------|-------------|--------------|-------|
| PoE IP Camera (24/7) | $130 | $100 | **$230** |
| Action Cameras | $350-400 | $100 | $450-500 |
| Gore Vent (Entaniya) + USB | $120 | $100 | **$220** |
| Gore Vent (VA Imaging) + USB | $200 | $100 | **$300** |
| Nitrogen-Purged (Dotworkz) + USB | $700-920 | $100 | $800-1,020 |

**Summary:** Gore Vent (Entaniya) + commercial power at ~$220 is the cheapest. Single PoE camera + commercial power at ~$230 is the cheapest factory-sealed option.

### Risk

| Option | Tech Risk | Field Risk | Dev Risk | Overall |
|--------|-----------|------------|----------|---------|
| PoE IP Camera (24/7) | Low | Low | None | **LOW** |
| Action Cameras | Medium | High (temp/SDK) | Medium-High | **HIGH** |
| Gore Vent Housing + USB | Low | Low | Medium | **MEDIUM** |
| Nitrogen-Purged (Dotworkz) | Low | Low | Medium | **LOW** |

---

## Recommendations

### Sites with commercial power (110V/220V)

**Use PoE IP cameras.**

When utility power is available, PoE cameras are the cheapest reliable option. Power consumption doesn't matter. Factory-sealed IP67, industrial temp range, integrated IR, proven RTSP integration.

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

Single camera + commercial power runs about $240.

**Risk: LOW**

---

### Solar sites - prioritizing reliability

**Use PoE IP cameras (Option 1).**

Accept the higher power system cost for proven, factory-sealed cameras with industrial temperature ratings. Cameras run 24/7 with IR enabled.

No development risk, no field assembly risk, no temperature surprises. Continuous operation means 6-10 year camera lifespan (no power cycling wear).

| Configuration | Cameras | Solar | Battery | Total |
|---------------|---------|-------|---------|-------|
| 2 cameras | $260 | 300W ($180) | 200Ah ($400) | **~$840** |
| 1 camera | $130 | 200W ($120) | 100Ah ($250) | **~$550** |

**Risk: LOW**

---

### Solar sites - cost savings

**Consider testing Gore Vent Housing approach (Option 3).**

True nitrogen-purged housings cost $500-5,000+ and are more than we need for river monitoring. Gore protective vents + desiccant provide equivalent moisture protection at lower cost.

Gore vents use ePTFE membrane (same material as GORE-TEX). They allow continuous pressure equalization while blocking liquid water. For tropical sites with temperature cycling, continuous pressure management matters more than initial nitrogen fill.

**Test path:**

| Config | Housing | Camera | Vent | Total |
|--------|---------|--------|------|-------|
| Budget | Entaniya WC-01 ($40) | USB 4K ($60) | Gore ($10) | **~$120** |
| Standard | VA Imaging MVEC167 ($100) | USB 4K ($60) | Gore ($12) | **~$175** |

**Advantages:**
- Lowest total system cost ($220-320 per camera with commercial power)
- ~1W power vs 12W for PoE
- Smaller solar/battery system
- Gore vents proven in industrial use for decades
- VA Imaging aluminum housing handles tropical heat

**Challenges:**
- Requires careful assembly in controlled environment
- Not factory sealed - you're building the sealed unit
- No integrated IR (need separate illuminator)
- Quarterly desiccant checks recommended
- Less field-proven than PoE cameras

**Test cost: ~$150 | Potential savings: ~$100-200/unit**

---

### Not recommended

- **Action cameras (Option 2):** GoPro overheats above 35°C, DJI has no Python SDK, Insta360 limited to 1080p. None have integrated IR. Not worth the tradeoffs.

---

## Next Steps

1. **If proceeding with PoE cameras:**
   - Source 4K/8MP cameras with good IR range (30m+)
   - Verify RTSP compatibility with ORC
   - Update BOM for Indonesia rainy season (300W panel, 200Ah battery)
   - Test IR image quality for river surface detection

2. **If testing Gore Vent housing approach:**
   - Order VA Imaging MVEC167 housing (~$100) or Entaniya WC-01 (~$40)
   - Order Gore screw-in vent (M12 thread, ~$12) from Digi-Key/Mouser
   - Order 4K USB camera module (~$60)
   - Order silica gel desiccant packs (100g, indicating type)
   - Assemble in controlled, low-humidity environment
   - Seal test: Submerge in water bath for 30 minutes
   - Thermal cycle test: 15°C to 45°C cycles for 1 week
   - Humidity test: Place in >90% RH chamber, check for internal condensation
   - Document assembly procedure for field replication
   - Validate USB camera works with Pi and ORC software

3. **If pursuing nitrogen-purged housing (for critical installations):**
   - Contact [Dotworkz](https://shop.dotworkz.com/) for D2 series pricing and lead times
   - Request quotes from [2bSecurity](https://www.2bsecurity.com/) for PH-850/PH-860 housings
   - Evaluate heater/blower power requirements for solar deployments
   - Design custom USB camera mounting adapter
   - Confirm nitrogen maintenance schedule (or if factory-sealed is permanent)
   - Note: Best suited for commercial power sites due to heater/blower power draw

---

## References

### Action Cameras
- [GoPro Labs USB Power Trigger](https://gopro.github.io/labs/control/usb/)
- [Open GoPro Python SDK](https://gopro.github.io/OpenGoPro/python_sdk/)
- [DJI Osmo Action 5 Pro Specs](https://www.dji.com/osmo-action-5-pro/specs)
- [DJI R SDK (ESP32)](https://github.com/dji-sdk/Osmo-GPS-Controller-Demo)
- [Insta360 Ace Pro 2 Webcam Mode](https://onlinemanual.insta360.com/acepro2/en-us/camera/appuse/webcammode)

### Gore Vent Housing Approach
- [VA Imaging Camera Housings](https://va-imaging.com) - MVEC167 and similar aluminum housings
- [Entaniya WC-01 Housing](https://e-products.entaniya.co.jp) - Budget option, proven with Pi cameras
- [GORE Protective Vents](https://www.gore.com/products/gore-protective-vents) - ePTFE membrane technology
- [Gore Vents at Digi-Key](https://www.digikey.com) - Search "Gore protective vent"
- [Gore Vents at Mouser](https://www.mouser.com) - Search "Gore vent"

### PoE Cameras
- [ANNKE C1200 4K PoE Camera](https://www.annke.com/products/c1200-12mp-poe-ip-camera) - 12MP, IP67, -30°C to 60°C
- [Reolink RLC-810A](https://reolink.com/us/product/rlc-810a/) - 8MP, IP66, good IR range
- [Hikvision DS-2CD2083G2-IU](https://www.hikvision.com/en/products/IP-Products/Network-Cameras/Pro-Series-EasyIP-/ds-2cd2083g2-iu/) - 8MP, IP67, industrial grade
- [IPVM Camera Power Consumption Testing](https://ipvm.com/reports/ip-camera-power-use-rankings)

### Nitrogen-Purged Housings
- [Dotworkz D2 Series](https://shop.dotworkz.com/collections/all) - IP68, heater/blower options, Made in USA
- [Dotworkz D2 Heater/Blower](https://shop.dotworkz.com/products/dotworkz-d2-heater-blower-camera-enclosure-ip68-with-poe) - ~$600-850
- [2bSecurity PH-850](https://www.2bsecurity.com/product/ph-850-nitrogen-pressurized-large-camera-housing/) - 316L stainless, nitrogen-pressurized
- [2bSecurity PH-860](https://www.2bsecurity.com/product/ph-860-pressurized-camera-housing-with-wiper/) - with wiper option
- [Pelco/Videotec Camera Enclosures](https://www.pelco.com/products/accessories/camera-enclosures) - industrial/marine grade

### USB Camera Modules
- [ELP 4K USB Camera](https://www.amazon.com/dp/B08R5TCMQG) - Sony IMX317, ~$60-80
- [Arducam 8MP USB Camera](https://www.arducam.com/product/8mp-1080p-usb-camera-module-1-4-cmos-imx219-mini-uvc-usb2-0-webcam-board-with-1-64ft-0-5m-usb-cable-for-windows-linux-android-and-mac-os/) - IMX219, ~$40
- [Kayeton 4K USB Camera](https://www.amazon.com/dp/B0B4J6HZ4V) - Sony IMX415, ~$70

### Desiccant
- [Camtraptions Reusable Silica Pack](https://store.camtraptions.com/products/reusable-silica-moisture-absorbing-pack) - 100g, rechargeable, indicator
- [Dry-Packs Indicating Silica Gel](https://www.amazon.com/Dry-Packs-Camera-Moisture-Absorbing-Indicating/dp/B004AR1S3M) - 40g canister
- [Ewa-Marine CD5 Desiccant](https://www.bhphotovideo.com/c/product/17351-REG/Ewa_Marine_EM_CD_5_CD5_Camera_Dry_Desiccant.html) - reusable 5×

### Research Documents
- See `/rc-box/research/nitrogen_sealed_enclosures.md` for detailed housing research
