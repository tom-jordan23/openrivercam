# Weatherproof LTE Antenna Research Report - Tropical Deployment

**Research Date:** January 30, 2026
**Purpose:** Identify durable, weatherproof 4G LTE antenna solutions for outdoor tropical deployment on Indonesian river monitoring stations
**Current Setup:** 2× basic SMA male 3-5dBi stick antennas ($16) + SMA bulkhead connectors ($8) = $24 total
**Problem:** Listed as likely failure point due to UV degradation and connector corrosion in 95% humidity environment

---

## Executive Summary

The current $24 antenna setup (basic stick antennas + bulkhead connectors with dielectric grease) is inadequate for long-term deployment in tropical environments with 95% humidity, heavy rain, UV exposure, and possible salt air. Research identified several categories of solutions ranging from $30 to $500+ for a complete 2-antenna MIMO system.

### Key Findings:

1. **Best Value Upgrade (~$50-80 total):** Fiberglass radome antennas with nickel-plated connectors + improved weatherproofing
2. **Premium Marine Solution (~$100-180):** Marine-grade antennas with stainless steel hardware and sealed construction
3. **Industrial Puck/Dome (~$80-250):** Sealed panel-mount antennas that eliminate exposed SMA connections entirely
4. **Budget Improvement (~$30-50):** Better stick antennas + self-amalgamating tape instead of dielectric grease alone

### Critical Technical Findings:

- **Fiberglass radomes outlast plastic by 3-5 years** in tropical UV environments
- **Nickel-plated connectors** are essential for corrosion resistance (superior to chrome plating which bubbles in salt air)
- **N-type connectors are engineered for outdoor use**; SMA is designed for indoor/laboratory applications
- **Self-amalgamating silicone tape** provides better weatherproofing than dielectric grease alone
- **Indonesian LTE bands confirmed compatible** with standard wideband 698-2700 MHz antennas

---

## Indonesian LTE Band Requirements

### Required Bands (Telkomsel, Indosat, XL Axiata):

| Band | Frequency | Technology | Coverage |
|------|-----------|------------|----------|
| **B1** | 2100 MHz | UMTS/LTE | Urban primary |
| **B3** | 1800 MHz | LTE | Urban/suburban |
| **B5** | 850 MHz | LTE | Rural coverage |
| **B8** | 900 MHz | GSM/LTE | Nationwide backbone |
| **B40** | 2300 MHz | LTE TDD | Urban high-capacity |

### Antenna Requirement:
Dual-band or wideband coverage of **698-960 MHz** and **1710-2700 MHz** will cover all Indonesian LTE bands. Nearly all modern 4G antennas meet this specification.

### Quectel EG25-G Compatibility:
✅ **Confirmed compatible** - Module supports B1/B3/B5/B8/B40 with 50-ohm SMA connectors (main + diversity)

---

## Category 1: IP67/IP68 Rated Outdoor LTE Antennas

Professional outdoor antennas with sealed enclosures and weatherproof connectors.

### Option 1.1: Data Alliance 4G LTE Outdoor Weatherproof Antennas

**Multiple Models Available:**

| Model | Gain | Frequency | Connector | Price (est.) |
|-------|------|-----------|-----------|--------------|
| 3dBi Omni SMA | 3dBi | 700-2700 MHz | SMA-Male | $25-40 each |
| 5dBi Omni SMA | 5dBi | 700-2700 MHz | SMA-Male | $35-50 each |
| 2/5dBi Dual-Band | 2/5dBi | 698-960 / 1710-2700 MHz | N-Male/TNC | $45-65 each |

**Key Specifications:**
- **Materials:** UV-resistant ABS radome, nickel-plated brass connectors
- **IP Rating:** IP65 minimum, IP67 available
- **Temperature:** -40°C to +60°C operating range
- **Mounting:** Pole mount brackets included (stainless steel)
- **Cable:** Some models include pigtails with sealed connectors

**Pros:**
- Specifically designed for outdoor telecom applications
- UV-stabilized radome resists degradation
- Nickel-plated connectors resist corrosion
- Good coverage of Indonesian bands
- Professional industrial design

**Cons:**
- Higher cost than basic stick antennas (3-4× current budget)
- N-connector models require SMA adapter or cable assembly
- Must contact vendor for pricing (not transparent)
- Lead time may be 1-2 weeks

**Recommendation for Your Application:**
- 2× **3dBi SMA** models = ~$50-80 total (double current budget)
- Best value in this category for budget-conscious deployment

**Source:** [Data Alliance Weatherproof Antennas](https://www.data-alliance.net/weatherproof-antennas/)

---

### Option 1.2: L-com IP67 Rubber Duck Antennas

**Model:** HG72703RDR90-SM (or similar)

**Specifications:**
- **Frequency:** 698-960 MHz / 1710-2700 MHz (covers all Indonesian bands)
- **Gain:** 1-3 dBi
- **Connector:** 90-degree rigid SMA male
- **IP Rating:** IP67 waterproof
- **Form Factor:** Portable rubber duck style
- **Price:** ~$35-50 each

**Pros:**
- True IP67 rating with testing certification
- 90-degree connector reduces stress on bulkhead mount
- Rubber construction is durable and impact-resistant
- L-com is reputable US manufacturer with technical support

**Cons:**
- Lower gain (1-3 dBi) may reduce signal strength in marginal coverage areas
- Rubber can degrade over time in UV (though UV-stabilized)
- Still uses SMA connector (not as robust as N-type)

**Total Cost:** 2× antennas = ~$70-100

**Source:** [L-com IP67 Cellular Antennas](https://www.l-com.com/698-mhz-960-mhz-1710-mhz-2700-mhz-1-3-dbi-ip67-4g-lte-cellular-portable-rubber-duck-antenna-90-degrees-rigid-sma-male-connector-hg72703rdr90-sm)

---

### Option 1.3: LM YN LTE 4G Omnidirectional Antenna

**Specifications:**
- **Frequency:** 700/800/900/1800/1900/2100/2600/2700 MHz (covers all Indonesian bands)
- **Gain:** 5.0 dBi
- **Connector:** SMA male
- **Compatibility:** 2G/3G/GSM terminal frequency
- **Price:** ~$20-35 each on Amazon

**Pros:**
- Affordable upgrade from current antennas
- Good gain (5 dBi)
- Wide frequency coverage
- Available on Amazon (fast shipping)

**Cons:**
- No explicit IP rating mentioned in specs
- Unclear if UV-stabilized
- Quality/durability unknown (consumer-grade product)

**Total Cost:** 2× antennas = ~$40-70

**Risk Assessment:** Medium - May not last long in 95% RH tropical environment without explicit weatherproof rating.

**Source:** [Amazon - LM YN Antenna](https://www.amazon.com/LM-YN-Omnidirectional-Compatible-Frequency/dp/B01N6GO584)

---

### Option 1.4: Maswell GSM-046 MIMO Antenna Set

**Specifications:**
- **Frequency:** 700-2700 MHz (covers all Indonesian bands)
- **Gain:** 2 dBi omnidirectional
- **IP Rating:** IP67 waterproof
- **Cables:** 2× 9.8ft (3m) low-loss cables with SMA male connectors
- **Mounting:** Screw-mount bracket included
- **Price:** ~$40-60 for complete 2-antenna set on Amazon

**Pros:**
- ✅ **Best value option** - Complete MIMO set with cables and mounting hardware
- IP67 waterproof rating
- Cables already attached (eliminates exposed bulkhead connection point)
- Good cable length (3m) for typical installations
- Low-loss cables reduce signal attenuation
- Ready to install (minimal assembly)

**Cons:**
- Lower gain (2 dBi) than some alternatives
- Fixed cable length (cannot extend without adding connectors)
- Consumer brand (less established than industrial suppliers)
- Unclear if connectors are nickel-plated

**Total Cost:** $40-60 for complete 2-antenna system

**Recommendation:** ✅ **Top budget choice** for moderate upgrade from current setup. The integrated cables eliminate the vulnerable bulkhead connector failure point.

**Source:** [Amazon - Maswell GSM-046](https://www.amazon.com/MASWELL-Cellular-Antenna-cirucular-700-2700MHz/dp/B0BPLHWP69)

---

## Category 2: Marine-Grade LTE Antennas

Designed for salt water environments, these antennas inherently resist the harshest corrosion conditions.

### Option 2.1: weBoost (Wilson) Wide-Band Omni Marine Antenna

**Model:** 304420

**Specifications:**
- **Frequency:** 617-6000 MHz (covers all cellular + WiFi)
- **Gain:** +3 dBi average
- **Construction:** Stainless steel base + fiberglass radome
- **Cable:** 20 ft (6m) RG-58 coax with SMA-male connector
- **Mounting:** Marine deck mount (stainless steel)
- **Waterproof:** Yes, salt water resistant
- **Price:** ~$120-150

**Pros:**
- Designed specifically for marine/salt water use (perfect for coastal/river)
- Stainless steel hardware won't corrode
- Fiberglass radome has excellent UV resistance (10-15 year lifespan)
- Long cable included (reduces need for extensions)
- Proven in harsh environments (marine installations worldwide)
- weBoost is reputable brand

**Cons:**
- High cost (~$240-300 for 2 antennas)
- Single antenna (need to buy 2 for MIMO)
- 20 ft cable may be too long (can't shorten coax without re-terminating)
- Marine deck mount may not fit pole/enclosure mounting

**Total Cost:** 2× antennas = ~$240-300

**Verdict:** Premium solution if budget allows. Ideal for coastal deployments with salt air exposure.

**Source:** [Waveform - weBoost Marine Antenna](https://www.waveform.com/products/weboost-4g-marine-antenna)

---

### Option 2.2: Top Signal TS210461 Marine Antenna

**Specifications:**
- **Frequency:** 600-4000 MHz (covers 5G + 4G + WiFi)
- **Gain:** +2.0 to +4.5 dBi (frequency dependent)
- **Connector:** SMA-male (20 ft RG58 coax cable)
- **Construction:** Marine-rated, corrosion resistant
- **Mount:** Deck/pole mount
- **Price:** ~$90-120

**Pros:**
- Lower cost than weBoost while maintaining marine rating
- Wide frequency coverage (future-proof for 5G)
- 20 ft cable with SMA termination included
- Corrosion-resistant materials

**Cons:**
- Need 2 for MIMO (~$180-240 total)
- Fixed cable length
- Less established brand than weBoost

**Total Cost:** 2× antennas = ~$180-240

**Source:** [Powerful Signal - Top Signal Marine Antenna](https://powerfulsignal.com/top-signal-ts210461-4g-3g-marine-omnidirectional-antenna-with-sma-male-connector-50-ohm/)

---

### Option 2.3: Bingfu 4G LTE Marine Antenna

**Specifications:**
- **Frequency:** 698-960 MHz, 1710-2170 MHz, 2300-2700 MHz
- **Gain:** 5 dBi
- **IP Rating:** Rainproof (not full IP67, but water resistant)
- **Connector:** SMA male with RP-SMA adapter included
- **Cable:** 3m (10 ft) included
- **Price:** ~$25-40 each on Amazon

**Pros:**
- Budget-friendly option with marine-type design
- Good gain (5 dBi)
- Includes cable and adapters
- Wall/pole mount bracket included
- Available on Amazon (fast shipping)

**Cons:**
- Not true marine-grade (more "outdoor consumer" level)
- "Rainproof" is vague (no IP rating)
- Connector quality unknown (may not be nickel-plated)
- Bingfu is consumer brand (less proven than industrial)

**Total Cost:** 2× antennas = ~$50-80

**Verdict:** Good mid-tier option. Better than basic stick antennas, not as robust as true marine gear.

**Source:** [Amazon - Bingfu Marine Antenna](https://www.amazon.com/Bingfu-Waterproof-T-Mobile-Cellular-Amplifier/dp/B07R9JGLV5)

---

### Option 2.4: C&T RF Marine Boat Antenna

**Specifications:**
- **Type:** Waterproof outdoor 4G antenna designed for marine boats
- **Length:** 165mm fiberglass antenna
- **Gain:** 5 dBi high gain
- **Connector:** SMA male
- **Environment:** Robust environment, marine boat application
- **Price:** Contact manufacturer (likely $40-70 each)

**Pros:**
- Designed specifically for marine environment
- Fiberglass construction (long UV life)
- Compact 165mm length
- Manufacturer specializes in antenna design

**Cons:**
- Pricing not transparent (must contact vendor)
- Lead time unknown
- International shipping from China (C&T RF is Chinese manufacturer)

**Total Cost:** Estimated 2× antennas = ~$80-140

**Source:** [C&T RF Waterproof Marine Antenna](https://lcantennas.com/outdoor-4g-antenna-sma/)

---

## Category 3: Puck/Dome Antennas (Panel Mount)

Low-profile sealed units that mount directly to enclosure panels, eliminating exposed SMA connections entirely.

### Option 3.1: Poynting PUCK-2 2-in-1 MIMO Antenna ⭐ RECOMMENDED

**Model:** A-PUCK-0002-V2-01 (Black) or A-PUCK-0002-V2-01-W (White)

**Specifications:**
- **Type:** 2-in-1 MIMO (both main + diversity in single unit)
- **Frequency:** 617-960 MHz / 1427-1517 MHz / 1710-2700 MHz / 3400-4200 MHz
- **Bands Covered:** 2G, 3G, 4G, 5G (all Indonesian LTE bands)
- **Gain:** 6 dBi average, omnidirectional
- **IP Rating:** IP69K (highest waterproof rating - withstands high-pressure steam cleaning)
- **Connectors:** 2× SMA-male pigtails (sealed cable entry)
- **Mounting:** Through-hole panel mount with 3 screw holes
- **Vandal Resistant:** Robust construction
- **Temperature:** -40°C to +85°C
- **Applications:** IoT/M2M, transportation, marine, agriculture
- **Price:** ~£46.50 (~$58 USD) for single unit with 2 antennas

**Pros:**
- ✅ **Single unit solution** - Eliminates need for 2 separate antennas
- ✅ **IP69K rating** - Highest weatherproof standard (exceeds IP68)
- ✅ **No exposed connectors** - Pigtails enter through single sealed hole
- ✅ **All Indonesian bands covered** - Future-proof for 5G
- ✅ **Low profile** - Less wind load, less visible
- ✅ **Vandal resistant** - Robust construction for public installations
- ✅ **Pattern diversity** - 2×2 MIMO with spatial separation in single housing
- Long lifespan in harsh environments
- Reputable manufacturer (Poynting is South African company specializing in mobile/IoT antennas)

**Cons:**
- Higher upfront cost (~$60 vs $24 current setup)
- Requires drilling hole in enclosure panel (typically 35-45mm diameter)
- Fixed pigtail length (usually 3m) - cannot easily extend
- Must source from specialty distributors (not on Amazon)

**Total Cost:** ~$58 USD for complete MIMO system (single unit)

**Mounting Requirements:**
- Panel cutout: Check datasheet (typically 30-40mm diameter)
- 3× M4 or M5 screws for secure mounting
- Gasket/O-ring included for IP69K seal

**Recommendation:** ✅ **Best technical solution if budget allows.** Eliminates the main failure point (exposed bulkhead connectors) and provides highest environmental protection.

**Sources:**
- [Poynting PUCK-2 Product Page](https://poynting.tech/antennas/puck-2/)
- [Westward Sales - PUCK-2](https://westwardsales.com/poynting-puck-2-mimo-lte-antenna)
- [Amazon - PUCK-2](https://www.amazon.com/Poynting-Puck-2-Transportation-Antenna-617-4200/dp/B0BQWW9MVJ)
- [BroadbandBuyer - £46.50](https://www.broadbandbuyer.com/products/36007-poynting-a-puck-0002/)

---

### Option 3.2: C&T RF Puck Antenna 4G (Panel Mount)

**Model:** CTRF-ANTENNA-EX-7027-4615-SMA-S (46×15mm) or CTRF-ANTENNA-EX-7027-8115-SMA-1M (81×15mm)

**Specifications:**
- **Frequency:** 698-960 MHz, 1710-2700 MHz
- **Gain:** 5-7 dBi
- **IP Rating:** IP67 waterproof
- **Mounting:** Through-hole screw mount
- **Size:** 46×15mm (compact) or 81×15mm (larger)
- **Connector:** SMA standard connector with 1m cable
- **Cable:** RG174 coax, 1 meter length
- **Price:** Contact manufacturer for pricing (estimated $25-45 each)

**Pros:**
- Compact low-profile design (especially 46mm model)
- IP67 rated for outdoor use
- Through-hole mount eliminates external connector exposure
- Covers all Indonesian LTE bands
- Good gain (5-7 dBi)

**Cons:**
- Need 2 separate units for MIMO (~$50-90 total)
- Must contact manufacturer for pricing (not transparent)
- International shipping from China
- 1m cable may be too short (requires extension)

**Total Cost:** Estimated 2× antennas = ~$50-90

**Sources:**
- [C&T RF Puck Antenna 4G](https://ctrfantennasinc.com/puck-antenna-4g/)
- [C&T RF Through-hole Mount](https://lcantennas.com/puck-antenna-4g/)

---

### Option 3.3: CMO 4G LTE MIMO Puck Antenna

**Specifications:**
- **Frequency:** 690-2700 MHz
- **Type:** 2× 4G/LTE/Multiband elements in single housing
- **Mounting:** Permanent through-hole mount
- **Waterproof:** Sealed against flat mounting surfaces
- **Applications:** Continuous outdoor deployment
- **Price:** Contact manufacturer (estimated $60-100)

**Pros:**
- Single unit with MIMO capability
- Designed for continuous outdoor use
- Discreet, robust housing
- Wide frequency coverage

**Cons:**
- Pricing not transparent
- Less information available than Poynting PUCK-2
- May have minimum order quantities

**Total Cost:** Estimated ~$60-100 for single unit

**Source:** [EAD - CMO MIMO Puck](https://www.ead-ltd.com/products/5g-lte-4g-antennas/cmo-4g-lte-mimo-puck-antenna)

---

### Option 3.4: Proxicast Low Profile 4G/5G Puck Antenna

**Specifications:**
- **Height:** ~3 inches (low profile)
- **Frequency:** Supports 5G & 4G/LTE multi-antenna systems
- **Mount:** Fixed mount, omnidirectional
- **IP Rating:** IP67 waterproof
- **Price:** ~$50-80 each (estimated)

**Pros:**
- Low profile design (~3 inches tall)
- IP67 waterproof
- 5G ready (future-proof)
- US-based company (Proxicast)

**Cons:**
- Need 2 for MIMO (~$100-160 total)
- Limited technical specs available
- Pricing not confirmed

**Total Cost:** Estimated 2× antennas = ~$100-160

**Source:** [Proxicast Low Profile Puck](https://www.proxicast.com/shopping/ultra-low-profile-mimo-4g-5g-omni-directional-magnetic-adhesive-mount-puck-antenna-with-sma-ts9-connectors.html)

---

## Category 4: Weatherproof Antenna Boot/Cover Solutions

If keeping basic antennas, enhance weatherproofing with professional-grade sealing methods.

### Option 4.1: Self-Amalgamating Silicone Tape ⭐ RECOMMENDED

**Best practice for outdoor antenna connections** - Superior to dielectric grease alone.

**Products:**
- **Proxicast Pro-Grade 30mil** - $12-15 for 1.5" × 15' roll
- **Times Microwave Professional** - $12-18 for 1.5" × 15'
- **3M Temflex 2155** - $10-15 (rubber splicing tape)
- **Rokland RokTape** - $12-15

**Application Process:**
1. Clean connector thoroughly with isopropyl alcohol
2. Apply dielectric grease to threads and contact surfaces
3. Tighten connector to proper torque
4. Stretch tape to 2-3× its original length while wrapping
5. Wrap in overlapping spiral (50% overlap) for 2-3 layers
6. Tape bonds to itself within 15 minutes at room temperature
7. Forms completely waterproof, air-tight seal

**Key Features:**
- **Temperature range:** -65°F to +500°F (-54°C to +260°C)
- **UV resistant:** Will not dry out or crack like electrical tape
- **Non-adhesive:** Only sticks to itself, leaves no residue
- **Waterproof:** Impervious to moisture, dust, chemicals
- **Removable:** Can be peeled off years later without damage

**Pros:**
- ✅ Low cost ($12-15 per roll = many connections)
- ✅ Professional standard for outdoor RF installations
- ✅ Simple to apply (no special tools)
- ✅ Works with any SMA/N-type connector
- ✅ Significantly better than dielectric grease alone
- ✅ Proven in telecom/broadcast industry

**Cons:**
- Still relies on SMA bulkhead connectors (potential failure point)
- Requires manual application (labor)
- Must be inspected/replaced periodically (~1-2 years in harsh environment)

**Cost to Upgrade Current Setup:**
- Self-amalgamating tape: $12-15 (one roll covers many antennas)
- Total upgrade: **~$12-15** added to current $24 setup

**Recommendation:** ✅ **Minimum viable upgrade** if budget is very tight. Significantly improves weatherproofing of existing SMA connectors.

**Sources:**
- [Proxicast Self-Fusing Tape - Amazon](https://www.amazon.com/Proxicast-Pro-Grade-Weatherproof-Self-Fusing-Electrical/dp/B00K5GW67O)
- [Times Microwave Sealing Tape - Amazon](https://www.amazon.com/Times-Microwave-Professional-Weatherproof-Self-Bonding/dp/B00K4PZ9NO)
- [Proxicast Tape - Direct](https://www.proxicast.com/shopping/proxicast-pro-grade-extra-strong-weatherproof-self-bonding-30mil-silicone-sealing-tape-for-coax-connectors-1.5-x-15-roll-black-en.html)

**Professional Notes:**
- RadioReference forum members recommend **2-3 layers** for outdoor permanent installations
- Telecom installers prefer silicone tape over PVC electrical tape (which dries out)
- Some installers use rubber tape first, then PVC tape over top for UV protection and color coding

---

### Option 4.2: IP67 SMA Bulkhead Connectors (Upgrade)

Replace standard bulkhead connectors with professional IP67-rated versions.

**Key Features:**
- **O-ring sealed:** Silicone O-rings achieve IP67 when properly compressed (15-30% compression)
- **Nickel-plated:** Corrosion-resistant finish (stainless steel also available)
- **Panel mount:** Nut-mounted or flange-mounted
- **Torque spec:** 0.34-0.57 N·m (8mm wrench)
- **Panel thickness:** 1.5-3.2mm standard (extended threads for thicker walls)

**Recommended Upgrade Path:**
1. Replace current bulkhead connectors with IP67 SMA bulkheads
2. Apply self-amalgamating tape to both ends (inside and outside enclosure)
3. Use dielectric grease on threads

**Cost:**
- IP67 SMA bulkhead connectors: ~$8-15 each (vs $4 for standard)
- Total for 2: ~$16-30

**Manufacturers:**
- **Amphenol RF** - Compact waterproof IP67 SMA connectors
- **Lighthorse Technologies** - IP67 bulkhead cable assemblies
- **Tejte** - IP67 SMA panel mount solutions

**Sources:**
- [Amphenol IP67 SMA Connectors](https://www.amphenolrf.com/news/safeguard-your-system-with-compact-waterproof-ip67-sma-connectors)
- [DigiKey - IP67 RF Connectors](https://www.digikey.com/en/product-highlight/a/amphenol-rf-division/sealed-solutions)
- [Tejte SMA Bulkhead Guide](https://tejte.com/blog/sma-bulkhead-panel-ip67-sealing-guide/)

---

### Option 4.3: Heat Shrink Boot (Lower Protection)

**Not recommended** - Heat shrink boots provide minimal weatherproofing for outdoor permanent installations.

**Why not recommended:**
- Heat shrink still allows moisture ingress at cable entry points
- UV degrades adhesive layer over time
- Not rated for continuous water exposure
- SMA connector threads remain vulnerable

**Only acceptable for:** Indoor applications or temporary outdoor setups

---

## Material Science: Radome and Connector Longevity

### Radome Materials Comparison

| Material | UV Life (Tropical) | Cost | Notes |
|----------|-------------------|------|-------|
| **Fiberglass + resin** | 10-15 years | $$$ | Best for harsh outdoor environments |
| **UV-stabilized HDPE** | 5-8 years | $$ | Good budget option |
| **ABS plastic** | 3-5 years | $ | Degrades faster, needs UV stabilizers |
| **Polycarbonate** | 3-5 years | $$ | Yellows and cracks in UV |
| **Standard plastic** | 1-3 years | $ | Not suitable for outdoor use |

**Key Finding:** Fiberglass radomes exceed plastic by 3-5 years in tropical environments with high UV exposure. For long-term outdoor deployment, fiberglass is worth the added cost.

**Source:** [Curbell Plastics - Radome Materials](https://www.curbellplastics.com/materials/industries/radomes/)

---

### Connector Plating Comparison

| Plating | Corrosion Resistance | Cost | Outdoor Life | Notes |
|---------|---------------------|------|--------------|-------|
| **Nickel** | Excellent | $$ | 10+ years | Most weather-resistant |
| **Stainless steel** | Excellent | $$$ | 15+ years | Marine-grade applications |
| **Gold (over brass)** | Good | $$ | 5-10 years | Better conductivity, indoor use |
| **Chrome** | Poor | $ | 1-3 years | Bubbles and peels in salt air |
| **Bare brass** | Poor | $ | <1 year | Corrodes rapidly outdoors |

**Critical for Marine/Tropical:** Nickel-plated brass or stainless steel connectors are essential. Chrome-plated connectors (common in cheap antennas) fail within 1-2 years in high humidity.

**Source:** [Data Alliance - Nickel vs Gold Plating](https://www.data-alliance.net/blog/nickel-and-goldplated-brass-compared-as-platings-for-antenna-cable-connectors-and-adapters/)

---

### Connector Type: SMA vs N-Type for Outdoor Use

| Feature | SMA | N-Type |
|---------|-----|--------|
| **Design purpose** | Lab/indoor | Outdoor/RF transmission |
| **Mating cycles** | 500 | 1000+ |
| **Weather resistance** | Fair (with sealing) | Excellent (inherent design) |
| **Coupling** | Threaded | Threaded (larger, more robust) |
| **Size** | Compact | Larger |
| **Typical use** | Consumer/indoor | Professional outdoor telecom |

**Key Finding:** N-type connectors are engineered for longevity and reliability in harsh outdoor environments. SMA connectors can work outdoors but require additional weatherproofing measures.

**For Your Application:** Since Quectel EG25-G uses SMA, you're limited to SMA connectors. Mitigation: Use IP67 SMA bulkheads + self-amalgamating tape, or switch to puck antennas that eliminate external connectors entirely.

**Source:** [Data Alliance - Marine Antennas](https://www.data-alliance.net/weatherproof-antenna-connectors/)

---

## Budget Comparison & Recommendations

### Current Setup (Baseline)
- 2× Basic 3-5dBi SMA stick antennas: $16
- 2× SMA bulkhead connectors: $8
- Dielectric grease: Included
- **Total: $24**

**Failure Risk:** HIGH - UV degradation of antenna housing, connector corrosion, bulkhead seal failure in 95% humidity

---

### Tier 1: Minimal Viable Upgrade (~$36-40)

**Option A: Better Antennas + Improved Sealing**
- 2× LM YN 5dBi antennas (better construction): $40-70
- Replace dielectric grease with self-amalgamating tape: $12-15
- Keep existing bulkhead connectors
- **Total: ~$52-85**

**Improvement:** Moderate. Better antenna construction, professional weatherproofing tape. Still relies on bulkhead connectors.

**Option B: Self-Amalgamating Tape Only (Current Antennas)**
- Keep current $24 antenna setup
- Add self-amalgamating silicone tape: $12-15
- **Total: ~$36-40**

**Improvement:** Minor. Significantly better weatherproofing of connectors, but antennas themselves still vulnerable to UV.

**Verdict:** Only if budget is extremely tight. Extends life by 1-2 years but not a long-term solution.

---

### Tier 2: Good Value Upgrade (~$50-90) ⭐ RECOMMENDED

**Option A: Maswell GSM-046 Complete MIMO Kit**
- Maswell GSM-046 2×2 MIMO antenna set: $40-60
- Includes 2 antennas + cables + mounting hardware
- IP67 rated
- **Total: $40-60**

**Pros:**
- ✅ Integrated cables eliminate bulkhead connector failure point
- ✅ IP67 rated complete system
- ✅ Good value (under 3× current budget)
- ✅ Ready to install

**Cons:**
- Fixed 3m cable length
- Lower gain (2 dBi)

**Verdict:** ✅ **Best budget upgrade** - Doubles budget but eliminates main failure point (bulkhead connectors).

---

**Option B: Data Alliance 3dBi Outdoor Antennas**
- 2× Data Alliance 3dBi SMA outdoor antennas: $50-80
- 2× IP67 SMA bulkheads: $16-30
- Self-amalgamating tape: $12-15
- **Total: ~$78-125**

**Pros:**
- Professional-grade outdoor antennas
- UV-stabilized radome
- Nickel-plated connectors
- Modular (can replace antenna or cable separately)

**Cons:**
- Higher cost
- Still uses bulkhead connectors (though upgraded)

**Verdict:** Good if you need higher gain or want modular system.

---

### Tier 3: Premium Solution (~$60-180)

**Option A: Poynting PUCK-2 (SINGLE UNIT MIMO)** ⭐ BEST TECHNICAL SOLUTION
- Poynting PUCK-2 2-in-1 MIMO antenna: ~$58 USD
- IP69K panel mount installation
- **Total: ~$58**

**Pros:**
- ✅ Eliminates external connectors entirely (sealed panel mount)
- ✅ IP69K rating (highest weatherproof standard)
- ✅ Single unit = both main + diversity antennas
- ✅ Vandal-resistant construction
- ✅ Future-proof (5G ready)
- ✅ 10+ year lifespan expected

**Cons:**
- Requires drilling large hole in enclosure panel
- Fixed pigtail length (typically 3m)
- Must source from specialty distributor

**Verdict:** ✅ **Best long-term solution** - Eliminates failure points, highest environmental protection, only 2.5× current budget.

---

**Option B: Marine-Grade Antennas (weBoost or Top Signal)**
- 2× Marine omnidirectional antennas: $180-300
- Stainless steel hardware
- Fiberglass radomes
- **Total: $180-300**

**Pros:**
- Highest corrosion resistance (designed for salt water)
- Long fiberglass radome life (10-15 years)
- Proven in harshest environments
- Includes long cables (6m)

**Cons:**
- Expensive (7.5-12.5× current budget)
- Overkill for river monitoring (not ocean deployment)
- May exceed project budget

**Verdict:** Only if deployment is in coastal area with direct salt spray exposure.

---

## Final Recommendations

### Immediate Action Items:

1. **Assess Budget Flexibility:**
   - Can you increase antenna budget from $24 to $50-60? → Proceed to Tier 2
   - Must stay under $40? → Proceed to Tier 1
   - Can stretch to $60-80? → Consider Poynting PUCK-2 (best technical solution)

2. **Evaluate Installation Constraints:**
   - Can you drill 35-45mm hole in enclosure panel? → Puck antennas viable
   - Must use existing SMA bulkhead holes? → Stick with external antennas + improved weatherproofing

3. **Assess Site Conditions:**
   - **Coastal (salt air):** Marine-grade or Poynting PUCK-2 strongly recommended
   - **Inland river (high humidity, UV):** Fiberglass radome antennas or puck style
   - **Budget-critical:** Maswell GSM-046 or self-amalgamating tape upgrade

---

### Recommended Solutions by Budget:

| Budget | Recommendation | Total Cost | Expected Life |
|--------|---------------|------------|---------------|
| **$36-50** | Current antennas + self-amalgamating tape | $36-40 | 1-2 years |
| **$50-90** | **Maswell GSM-046 MIMO kit** ⭐ | $40-60 | 2-4 years |
| **$60-100** | **Poynting PUCK-2** ⭐⭐ | ~$58 | 10+ years |
| **$80-150** | Data Alliance 3dBi + IP67 bulkheads + tape | $78-125 | 4-6 years |
| **$180-300** | 2× Marine-grade (weBoost/Top Signal) | $180-300 | 10+ years |

---

### Specific Recommendation for Sukabumi Site:

**Site Context:**
- Inland foothills location (not coastal)
- 95% humidity, heavy rain, UV exposure
- Current $24 setup identified as failure point
- Solar power budget (no active cooling)
- Aluminum enclosure reuse plan

**Recommended Solution: Poynting PUCK-2 ($58)**

**Rationale:**
1. **Eliminates connector vulnerability:** No external SMA bulkhead connections = no corrosion failure point
2. **Fits dual-enclosure strategy:** Panel mount through outer aluminum enclosure, pigtails enter inner sealed box through cable gland
3. **Single hole = minimal enclosure penetration:** Easier to seal than 2 separate antenna bulkheads
4. **IP69K rating:** Exceeds requirements for 95% humidity environment
5. **Future-proof:** Covers 5G bands if network upgrades in future
6. **Cost-effective long-term:** $58 upfront vs replacing failed $24 setup every 1-2 years

**Installation Notes:**
- Mount PUCK-2 on top surface of outer aluminum enclosure (optimal omnidirectional pattern)
- Route 2× SMA pigtails through single PG9 cable gland into inner sealed box
- Connect pigtails directly to Quectel EG25-G main + diversity ports
- Apply self-amalgamating tape to SMA connections inside inner box (extra protection)

**Alternative if Budget Constrained: Maswell GSM-046 ($40-60)**
- Integrated cables eliminate bulkhead connector failure
- IP67 rated
- Quick install
- Acceptable 2-4 year lifespan for test deployment

---

### DO NOT RECOMMEND:

❌ **Keeping current $24 setup** - High failure risk in 95% humidity
❌ **Adding only dielectric grease** - Insufficient for tropical environment
❌ **Chrome-plated connectors** - Corrode rapidly in high humidity
❌ **Plastic radome antennas without UV stabilization** - Degrade in 1-3 years
❌ **Heat shrink boots** - Inadequate weatherproofing for permanent outdoor

---

## Implementation Notes

### For Puck Antenna Installation (Poynting PUCK-2):

**Tools Required:**
- Step drill bit or hole saw (35-45mm diameter, check PUCK-2 datasheet)
- Deburring tool
- Silicone sealant
- M4 or M5 screws (stainless steel)
- Torque wrench (low torque, 0.5-1 Nm)

**Process:**
1. Mark mounting location on enclosure top panel (away from edges, clear of internal components)
2. Drill pilot hole (6-8mm)
3. Enlarge to final diameter with step bit or hole saw
4. Deburr and clean hole edges
5. Apply silicone gasket sealant to PUCK-2 base (thin bead)
6. Insert pigtails through hole
7. Position PUCK-2 over hole, align screw holes
8. Install 3× mounting screws with washers
9. Torque evenly to compress gasket (do not overtighten aluminum)
10. Allow sealant to cure 24 hours before testing
11. Test IP rating if possible (hose test or submersion)

---

### For External Antenna Weatherproofing (Self-Amalgamating Tape):

**Tools Required:**
- Isopropyl alcohol wipes (99%)
- Dielectric grease
- Self-amalgamating silicone tape
- Clean lint-free cloth
- Gloves (tape is sticky)

**Process:**
1. Clean SMA connector threads and mating surfaces with alcohol wipe
2. Allow to dry completely (2-3 minutes)
3. Apply thin layer of dielectric grease to threads and contact pin
4. Thread connector together, torque to spec (finger-tight + 1/4 turn for SMA)
5. Wipe exterior clean of excess grease
6. Start tape wrap 1-2" below connector on cable
7. Stretch tape to 2-3× original width while wrapping
8. Wrap in ascending spiral with 50% overlap
9. Continue over connector body and onto antenna base
10. Complete 2-3 full layers
11. Press final end firmly (tape will bond to itself in 15 minutes)
12. Do NOT use electrical tape over silicone tape (traps moisture)

**Inspection Schedule:**
- Visual inspection every 6 months
- Look for cracks, tape separation, or discoloration
- Rewrap if tape appears degraded
- Expect 2-3 year service life in tropical environment

---

## Sources

### IP67/IP68 Outdoor Antennas:
- [Amazon - 4G LTE Outdoor Directional Antenna](https://www.amazon.com/Antenna-Outdoor-Directional-2600MHz-W-CDMA-Waterproof/dp/B09C7LP1P5)
- [2J Antennas - Medusa Series](https://www.2j-antennas.com/antennas/combination-external-antennas/2j7050mgfc-medusa-4g-lte-3g-2g-mimo-wifi-ism-gnss-magnetic-mount-antenna/507)
- [Amazon - LM YN LTE Antenna](https://www.amazon.com/LM-YN-Omnidirectional-Compatible-Frequency/dp/B01N6GO584)
- [Data Alliance - Outdoor Weatherproof Antennas](https://www.data-alliance.net/antenna-4g-lte-700-960-1700-2700-mhz-2dbi-outdoor-weatherproof-sma/)
- [L-com - IP67 Rubber Duck](https://www.l-com.com/698-mhz-960-mhz-1710-mhz-2700-mhz-1-3-dbi-ip67-4g-lte-cellular-portable-rubber-duck-antenna-90-degrees-rigid-sma-male-connector-hg72703rdr90-sm)
- [Amazon - Maswell GSM-046](https://www.amazon.com/MASWELL-Cellular-Antenna-cirucular-700-2700MHz/dp/B0BPLHWP69)

### Marine-Grade Antennas:
- [Getic - 4G LTE Outdoor Marine Antenna](https://www.getic.com/product/4g-lte-outdoor-omni-antenna-6dbi-marine-grade)
- [Waveform - weBoost Marine Antenna](https://www.waveform.com/products/weboost-4g-marine-antenna)
- [Data Alliance - Marine Grade Antenna](https://www.data-alliance.net/antenna-4g-lte-6dbi-698-960-1710-2700mhz-omnidirectional-w-n-f-marine-grade/)
- [Amazon - Bingfu Marine Antenna](https://www.amazon.com/Bingfu-Waterproof-T-Mobile-Cellular-Amplifier/dp/B07R9JGLV5)
- [Proxicast - Marine Antenna](https://www.proxicast.com/shopping/proxicast-8-5-dbi-pro-gain-bullet-4g-5g-lte-wifi-omni-directional-wideband-antenna-with-stainless-outdoor-marine-deck-mount-black.html)
- [C&T RF - Waterproof Marine Antenna](https://lcantennas.com/outdoor-4g-antenna-sma/)
- [Powerful Signal - Top Signal Marine Antenna](https://powerfulsignal.com/top-signal-ts210461-4g-3g-marine-omnidirectional-antenna-with-sma-male-connector-50-ohm/)

### Puck/Dome Antennas:
- [C&T RF - Puck Antenna 4G](https://ctrfantennasinc.com/puck-antenna-4g/)
- [Poynting - PUCK-2 Product Page](https://poynting.tech/antennas/puck-2/)
- [Westward Sales - Poynting PUCK-2](https://westwardsales.com/poynting-puck-2-mimo-lte-antenna)
- [Amazon - Poynting PUCK-2](https://www.amazon.com/Poynting-Puck-2-Transportation-Antenna-617-4200/dp/B0BQWW9MVJ)
- [BroadbandBuyer - PUCK-2](https://www.broadbandbuyer.com/products/36007-poynting-a-puck-0002/)
- [Proxicast - Low Profile Puck](https://www.proxicast.com/shopping/ultra-low-profile-mimo-4g-5g-omni-directional-magnetic-adhesive-mount-puck-antenna-with-sma-ts9-connectors.html)
- [Aboosty - Low Profile Puck](https://www.aboosty.com/product/ultra-low-profile-4g-cellular-lte-indoor-outdoor-puck-antenna/)
- [EAD - CMO MIMO Puck](https://www.ead-ltd.com/products/5g-lte-4g-antennas/cmo-4g-lte-mimo-puck-antenna)
- [C&T RF - Puck Through-hole](https://lcantennas.com/puck-antenna-4g/)

### Weatherproofing Solutions:
- [Data Alliance - Weatherproof Connectors](https://www.data-alliance.net/antenna-connectors-weatherproofing/)
- [Proxicast - Self-Fusing Tape](https://www.proxicast.com/shopping/proxicast-pro-grade-extra-strong-weatherproof-self-bonding-30mil-silicone-sealing-tape-for-coax-connectors-1.5-x-15-roll-black-en.html)
- [Amazon - Proxicast Tape](https://www.amazon.com/Proxicast-Pro-Grade-Weatherproof-Self-Fusing-Electrical/dp/B00K5GW67O)
- [Amazon - Times Microwave Tape](https://www.amazon.com/Times-Microwave-Professional-Weatherproof-Self-Bonding/dp/B00K4PZ9NO)
- [Atlavox - Self-Fusing Tape](https://atlavox.com/products/self-fusing-tape)
- [RadioReference - Weatherproof Connection Wraps](https://forums.radioreference.com/threads/looking-for-best-weatherproof-connection-to-coax-wrap.458260/)
- [Amazon - Lysignal Waterproof Tape](https://www.amazon.com/Lysignal-Waterproof-Self-Fusing-Electrical-Connectors/dp/B07GV7BRGY)
- [Rokland - RokTape](https://store.rokland.com/products/tape-helium-antenna-and-coaxial-cable-self-fusing-silicone-heat-water-resistant)

### Connector Specifications:
- [Tejte - SMA Panel Mount Guide](https://tejte.com/blog/sma-male-panel-mount-connector-cutout-nut-ip67/)
- [Tejte - SMA Bulkhead Connector Guide](https://tejte.com/blog/sma-bulkhead-connector-panel-flange-waterproof/)
- [Amphenol - IP67 SMA Connectors](https://www.amphenolrf.com/news/safeguard-your-system-with-compact-waterproof-ip67-sma-connectors)
- [DigiKey - IP67 RF Connectors](https://www.digikey.com/en/product-highlight/a/amphenol-rf-division/sealed-solutions)
- [Data Alliance - Nickel vs Gold Plating](https://www.data-alliance.net/blog/nickel-and-goldplated-brass-compared-as-platings-for-antenna-cable-connectors-and-adapters/)

### Material Science:
- [Curbell Plastics - Radome Materials](https://www.curbellplastics.com/materials/industries/radomes/)
- [Data Alliance - Weatherproof Antennas](https://www.data-alliance.net/weatherproof-antennas/)
- [Sanny Telecom - Antenna Radome](https://www.sannytelecom.com/what-is-an-antenna-radome/)
- [DOFRP - Fiberglass Radome](https://www.dofrp.com/portfolio-items/frp-radome-fiberglass-radome-radome-antenna/)

### Indonesia-Specific:
- [Tokopedia - Outdoor 4G Antennas](https://www.tokopedia.com/find/antena-outdoor-4g)
- [InHand Networks - 4G Outdoor Antenna](https://inhandgo.com/products/4g-lte-outdoor-wall-mount-waterproof-antenna)

---

**Report Compiled By:** Claude Sonnet 4.5 (comprehensive-researcher agent)
**Date:** January 30, 2026
**File:** `/home/tjordan/code/git/openrivercam/spring_2026_ID/research/lte_antenna_weatherproof_research.md`
