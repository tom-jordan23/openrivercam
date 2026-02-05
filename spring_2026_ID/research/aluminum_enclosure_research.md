# Aluminum IP67/IP68 Enclosure Research Report

**Research Date:** January 28, 2026
**Purpose:** Identify aluminum IP67/IP68 enclosures for dual-enclosure strategy (inner sealed box)
**Requirements:** ~200x150x100mm internal dimensions, aluminum construction, DIN rail compatible, <$100 budget

---

## Executive Summary

Based on comprehensive research of industrial enclosure manufacturers, the following key findings emerged:

**Best Options for Your Application:**

1. **Hammond 1590Z231** - $155 (over budget, but excellent specs)
2. **Fibox ALU 1626** - Price on application, closest size match with DIN rail
3. **Bud Industries AN-A Series** - ~$80-120, IP67 die-cast aluminum

**Critical Finding:** Most aluminum enclosures in the 200x150x100mm range do NOT come with integrated DIN rail. You will need to either:
- Use the Hammond 1427DINCLIP ($5-8) to mount any enclosure to external DIN rail, OR
- Install DIN rail strips INSIDE the enclosure on the flat mounting plate

**Budget Reality Check:** High-quality aluminum IP67 enclosures in this size typically cost $100-200. Staying under $100 may require compromising on features or considering polycarbonate alternatives.

---

## Comparison Table

| Model | External Dims (mm) | Internal Dims (mm) | IP Rating | Material | DIN Rail | Gore Vent Ready | Price (USD) | Source |
|-------|-------------------|-------------------|-----------|----------|----------|-----------------|-------------|--------|
| **Hammond 1590Z231** | 230×200×112 | ~216×186×100 | IP66/67/68 | Die-cast aluminum | Flat surface for mounting rail | M12 holes can be added | $155 | DigiKey, Mouser |
| **Fibox ALU 1626** | 264×163×91 | ~245×150×75 | IP66/67/68 | Aluminum | Included base for DIN rail | Yes (M12) | POA | Newark, RS |
| **Bud AN-2867-A** | 200×120×75 | ~185×105×65 | IP67 | Die-cast aluminum | Flat surface | Can be drilled | $80-120 | Bud Industries |
| **Weidmuller Klippon K71** | 230×280×111 | ~210×260×95 | IP66/67/68 | Aluminum | Mounting plate option | Yes | POA | Newark, Farnell |
| **Rose Euromas Alu A-126** | 200×140×91 | ~185×125×80 | IP66 | Die-cast aluminum | Pre-cut threads for rail | Yes | POA | DigiKey |
| **Takachi DRB15-10-10** | 150×100×100 | ~135×85×90 | Not rated | Aluminum | Built-in DIN mounting brackets | No | $30-50 | Newark, MISUMI |

**POA = Price on Application (contact distributor)**

---

## Detailed Product Analysis

### 1. Hammond 1590Z231 (RECOMMENDED IF BUDGET ALLOWS)

**Specifications:**
- External: 230mm (W) × 200mm (H) × 112mm (D)
- Internal: ~216mm × 186mm × 100mm (fits your requirements)
- Wall thickness: 4.5mm die-cast aluminum
- Weight: Heavy-duty construction
- IP Rating: IP66/67/68 (independently tested, also NEMA 4/4X/6/6P/12/13)
- IK08 impact rating

**Key Features:**
- Two-piece tongue-and-groove construction with replaceable silicone rubber gasket
- Gasket temperature rating: -40°C to +150°C
- No internal ribs - flat mounting surface ideal for DIN rail installation
- Can be drilled for M12 Gore vents without compromising IP rating (if sealed properly)
- Textured black or smooth gray (RAL 7001) finish

**DIN Rail Compatibility:**
- Does NOT include DIN rail
- Flat internal surface allows easy screw mounting of 35mm DIN rail
- Use Hammond 1427DINCLIP ($5-8) if mounting entire enclosure TO external DIN rail

**Price:** $155.10 (DigiKey, January 2026)

**Pros:**
- Exact size match for your requirements
- Highest IP rating with testing certification
- Excellent build quality for harsh environments
- Flat interior - no interference for component mounting

**Cons:**
- 55% over budget
- Heavy (shipping costs)
- No integrated DIN rail (need to add)

**Verdict:** Best technical fit, but budget stretch. Consider for critical deployments.

---

### 2. Fibox ALU 1626 (GOOD SIZE MATCH)

**Specifications:**
- External: 264mm (L) × 163mm (W) × 91mm (H)
- Internal: ~245mm × 150mm × 75mm (width matches, height is tight)
- Material: Aluminum alloy
- IP Rating: IP66/67/68, IK08
- Temperature: -50°C to +80°C

**Key Features:**
- Designed specifically to house DIN-rail mounted terminal blocks
- Base includes mounting provisions for DIN rail or mounting plate
- Cover secured with stainless steel screws
- PU (polyurethane) gasket included
- Powder-coated RAL 7001 gray

**DIN Rail Compatibility:**
- Base with screws for mounting plate/DIN-rail INCLUDED
- Specifically designed for industrial DIN rail applications

**Price:** Price on Application (POA) - typically $80-150 range

**Pros:**
- Width exactly matches your 150mm requirement
- DIN rail mounting built-in (rare feature)
- Industrial design for harsh environments
- Good IP rating

**Cons:**
- Height (75mm internal) may be tight for Pi stack + HAT
- Length (245mm) is longer than needed
- Must contact distributor for pricing

**Verdict:** Best option if internal height works. Measure your Pi stack first.

---

### 3. Bud Industries AN-A Series (BUDGET OPTION)

**Specifications:**
- Various sizes available, closest: AN-2867-A
- External: ~200mm × 120mm × 75mm (smaller than ideal)
- Material: ADC-12 alloy die-cast aluminum
- IP Rating: IP67 (TUV tested), IP68 capable
- Standards: NEMA Type 4X, 6, 12, 13 (UL listed)

**Key Features:**
- Rugged die-cast construction
- Silicone gasket
- Molded external mounting flanges (for wall/panel mount)
- Cover attaches with stainless screws (12 in-lb torque)
- Natural aluminum or powder-coated finishes

**DIN Rail Compatibility:**
- NO integrated DIN rail
- Flat internal base - DIN rail can be screwed in
- Mounting flanges on OUTSIDE (for mounting enclosure, not for internal DIN)

**Price:** $80-120 estimated (varies by size/finish)

**Pros:**
- Lower cost option
- Proven IP67 rating with testing certification
- Good availability in US

**Cons:**
- Smaller than ideal - may need larger size (higher price)
- No DIN rail mounting designed in
- Limited size options in the 200mm range

**Verdict:** Acceptable budget option if you can work with smaller dimensions.

---

### 4. Weidmuller Klippon K Series

**Specifications:**
- K71: 230mm × 280mm × 111mm (larger than needed)
- K51: 120mm × 220mm × 81mm (smaller)
- Material: Aluminum, unfinished or powder-coated
- IP Rating: IP66/67/68
- Impact: Extremely robust and impact resistant

**Key Features:**
- 22 different sizes available
- Suitable mounting plates for DIN rails available as ACCESSORIES
- Industrial-grade German engineering
- Two surface options: powder-coated or natural

**DIN Rail Compatibility:**
- DIN rail mounting plates sold separately
- Designed for industrial control applications

**Price:** Price on Application - expect $100-200 range

**Pros:**
- High quality German manufacturing
- Proven in industrial environments
- Optional accessories available

**Cons:**
- No exact size match - either too big or too small
- DIN rail mounting plate is extra cost
- Must contact distributor (pricing not transparent)

**Verdict:** Over-engineered for your application. Consider if other options unavailable.

---

### 5. Rose/Bopla Euromas Aluminum

**Specifications:**
- A-126 model: 200mm × 140mm × 91mm (close match)
- Material: Die-cast aluminum
- IP Rating: IP66 (IP67 available on request)
- Gasket: Foam rubber, tongue-and-groove seal

**Key Features:**
- Pre-cut threads in base for mounting PCBs and DIN rails
- Earthing screws included as standard
- 43 sizes available with IP66
- Silver-grey dust-proof jet-water-protected finish

**DIN Rail Compatibility:**
- Pre-cut threads for DIN rail mounting - BEST FEATURE
- No additional brackets needed

**Price:** Price on Application - typically $90-140

**Pros:**
- Pre-threaded for DIN rail (unusual feature)
- Good size match
- Earthing provisions built-in

**Cons:**
- Standard IP66 (must request IP67 upgrade)
- Limited US availability (easier in Europe)
- 140mm width slightly narrow

**Verdict:** Excellent if you can source it. Pre-threaded for DIN rail is huge advantage.

---

### 6. Takachi DRB Series (BUDGET, NO IP RATING)

**Specifications:**
- DRB15-10-10: 150mm × 100mm × 100mm
- Material: Aluminum
- IP Rating: NOT RATED (designed for DIN rail mount, not weatherproof standalone)
- Mount: Built-in brackets for 35mm DIN rail

**Key Features:**
- Designed to mount entire enclosure ONTO DIN rail
- Aluminum construction
- Screw-down cover

**DIN Rail Compatibility:**
- Built-in DIN rail mounting brackets (attaches enclosure TO rail)
- Can also install DIN rail INSIDE for components

**Price:** $30-50

**Pros:**
- Lowest cost aluminum option
- Compact size
- True DIN rail enclosure

**Cons:**
- NO IP RATING - not suitable for weatherproof application
- Smaller than needed
- Not designed for standalone outdoor use

**Verdict:** NOT recommended for your application. Lacks weatherproofing.

---

## DIN Rail Mounting Strategies

Since most enclosures DON'T include integrated DIN rail, you have three options:

### Option A: Screw DIN Rail Inside Enclosure (RECOMMENDED)

**Process:**
1. Purchase 35mm DIN rail separately ($5-15 for 1m length)
2. Cut to length with hacksaw
3. Drill mounting holes in enclosure base
4. Attach with M4 or M5 stainless screws

**Pros:**
- Most flexible approach
- Works with any flat-bottomed enclosure
- Can position rail exactly where needed
- Professional appearance

**Cons:**
- Drilling through enclosure base (must reseal holes)
- Need to calculate rail position for your components

**DIN Rail to Purchase:**
- Phoenix Contact NS35/7.5 (~$12/meter)
- Weidmuller TS35 (~$10/meter)
- Generic 35mm rail (~$5/meter on Amazon)

---

### Option B: Use Adhesive DIN Rail Mounts

**Process:**
1. Purchase DIN rail end-stop clips with adhesive backing
2. Attach to enclosure base
3. Snap in DIN rail

**Pros:**
- No drilling required (preserves IP rating)
- Quick installation
- Removable if needed

**Cons:**
- Adhesive may fail in high heat/humidity
- Not as secure as screw mounting
- May not support heavy components

**Not recommended for tropical outdoor deployment.**

---

### Option C: Mount Components Directly (No DIN Rail)

**Process:**
1. Use standoffs and screws to mount PCBs directly to enclosure base
2. Use Velcro/Dual-Lock for items without mounting holes (SSD, modem)

**Pros:**
- No DIN rail cost
- Potentially more compact
- Direct mounting can be more secure

**Cons:**
- Less modular (hard to swap components)
- Need to drill holes for each component's specific mounting pattern
- Not field-serviceable by semi-technical staff

**Verdict:** Acceptable, but defeats your "field serviceable" requirement.

---

## Gore Vent Integration

All enclosures can accommodate Gore protective vents, but integration varies:

### Pre-Drilled Options
- **Fibox ALU series** - Some models have M12 threaded holes
- **Weidmuller Klippon** - Can specify vent provisions when ordering

### Drill-and-Tap Required
- **Hammond 1590Z** - Must drill 10mm hole, tap M12x1.5 threads
- **Bud AN series** - Must drill and tap
- **Rose Euromas** - Must drill and tap

### Gore Vent Specifications
- **Thread:** M12x1.5 (most common for electronics enclosures)
- **Hole size:** 10mm diameter (before tapping)
- **Part examples:**
  - Gore PMF200350 (M12 screw-in, IP68)
  - Amphenol LTW VENT-PS1NGY-M12 (M12, IP68)
- **Price:** $10-15 each
- **Quantity:** 1 vent minimum, 2 recommended for cross-ventilation

**Important:** After drilling, apply thread sealant or silicone to threads when installing vent. Test IP rating after modification.

---

## Budget Analysis

### Target: Under $100

| Component | Cost | Notes |
|-----------|------|-------|
| **Enclosure** (200x150x100mm) | $80-155 | Hammond $155, Fibox ~$100, Bud ~$80 |
| **DIN Rail** (1m, cut to length) | $5-15 | Generic to Phoenix Contact |
| **DIN Rail end stops** (pair) | $3-5 | Prevent components sliding off |
| **Gore Vent** (M12) | $12 | Pressure equalization |
| **Cable Glands** (PG7/PG9/PG11) | $15-25 | 4-6 glands estimated |
| **Mounting Hardware** | $10-15 | Stainless screws, standoffs |
| **TOTAL ESTIMATE** | **$125-227** | **Over budget** |

### Budget Options to Stay Under $100

1. **Use polycarbonate enclosure instead** - Transparent/opaque ABS/PC boxes with IP67 rating: $30-60
2. **Smaller aluminum enclosure** - Bud AN-2856-A or similar: $60-80, but may be too small
3. **Source locally in Indonesia** - Avoid international shipping markup
4. **Buy used/surplus** - eBay, industrial liquidators

---

## Polycarbonate Alternative (If Budget Critical)

If aluminum is cost-prohibitive, consider high-quality polycarbonate:

| Model | Dims (mm) | IP Rating | Material | DIN Rail | Price |
|-------|-----------|-----------|----------|----------|-------|
| **Bud NBF-32240** | 230×180×130 | IP67 | Polycarbonate | Flat base | $40-60 |
| **Fibox PC 200/150** | 200×150×100 | IP66/67 | Polycarbonate | Optional | $35-55 |
| **Gainta G223MF** | 200×150×75 | IP67 | ABS+PC | Clips available | $25-40 |

**Pros:**
- 50-70% cost reduction
- Lighter weight (easier to mount, cheaper shipping)
- Easier to drill/modify
- Transparent lids available (see components without opening)

**Cons:**
- Less durable than aluminum
- Poorer heat dissipation (concern for Pi 5)
- UV degradation over time (needs UV-stabilized plastic)
- Less professional appearance

**Verdict:** Acceptable compromise if budget is hard constraint. Ensure UV-stabilized for outdoor use.

---

## Sourcing Strategy

### US Distributors (Ship to Indonesia)

| Distributor | Stock | Lead Time | Shipping to ID | Notes |
|-------------|-------|-----------|----------------|-------|
| **DigiKey** | Excellent | 1-3 days | DHL/FedEx 5-7 days | Best for Hammond, small items |
| **Mouser** | Excellent | 1-3 days | DHL/FedEx 5-7 days | Similar to DigiKey |
| **Newark** | Good | 3-5 days | FedEx 7-10 days | Good for Fibox, Weidmuller |
| **Amazon** | Variable | 2-5 days | 10-20 days | Budget options, hit-or-miss quality |

### Local Indonesia Sourcing

Check these options to avoid import duties and shipping costs:

- **Tokopedia** - Indonesian marketplace, search "box aluminium IP67"
- **Bukalapak** - Similar to Tokopedia
- **RS Components Indonesia** - Industrial supplier, carries Fibox and others
- **Schneider Electric Indonesia** - Industrial enclosures
- **Local electronics markets** - Glodok (Jakarta), Pasar Genteng (Sukabumi)

**Estimated savings:** 20-40% vs. US pricing + no import duty

---

## Recommendations

### Best Overall: Fibox ALU 1626 ($100-120 estimated)

**Rationale:**
- Width matches requirement (150mm internal)
- DIN rail mounting designed in (rare feature)
- Proven IP67/68 rating for harsh environments
- Industrial quality

**Action:** Contact Newark or RS Components for pricing. If height (75mm) is tight, measure your Pi stack first.

---

### Best Budget: Bud Industries AN-2867-A (~$80-100)

**Rationale:**
- Closest to budget target
- Proven IP67 rating
- Good availability
- Acceptable size (may be tight)

**Action:** Verify internal dimensions work for your Pi stack + components. Order from Bud directly or DigiKey.

---

### Best Quality (Budget Stretch): Hammond 1590Z231 ($155)

**Rationale:**
- Exact size match
- Highest IP rating with test certification
- Best build quality for long-term outdoor deployment
- Flat interior ideal for custom DIN rail mounting

**Action:** Consider for critical installations where reliability justifies cost.

---

### Best Pre-Threaded DIN Rail: Rose Euromas A-126 ($90-140)

**Rationale:**
- Pre-cut threads for DIN rail (saves time and preserves IP rating)
- Good size match
- Quality German engineering

**Action:** Check availability through European distributors or US sources.

---

## Installation Notes

### DIN Rail Installation (Screw Method)

1. **Measure your components:**
   - Pi 5 + Witty Pi 5 + Pi-EzConnect stack height
   - SSD, modem, relay dimensions
   - Required spacing between components

2. **Calculate rail position:**
   - Components on DIN rail are typically 90mm tall
   - Leave 10-15mm clearance to enclosure lid
   - Position rail to avoid interference with cable glands

3. **Mark and drill:**
   - Use DIN rail as template
   - Drill pilot holes (3mm)
   - Drill mounting holes (4.5mm for M4, 5.5mm for M5)
   - Deburr holes

4. **Apply sealant:**
   - Put thread sealant on screw threads
   - Or use bonded washers
   - Prevents water ingress through mounting holes

5. **Secure rail:**
   - Use stainless steel screws (A2 or A4 grade)
   - Torque to 2-3 Nm (don't over-tighten aluminum)

---

## Summary of Key Findings

1. **Budget Reality:** Quality aluminum IP67 enclosures in 200x150x100mm size cost $100-200. Staying under $100 requires compromise or polycarbonate alternative.

2. **DIN Rail Not Standard:** Almost no enclosures include integrated DIN rail. Budget $5-15 for rail + mounting.

3. **Best Value:** Fibox ALU 1626 if dimensions work, or Bud AN-series for tighter budget.

4. **Gore Vents:** All enclosures can be modified for M12 vents. Budget $12 per vent, test IP rating after drilling.

5. **Local Sourcing:** Consider Indonesia suppliers (Tokopedia, RS Components ID) to save 20-40% and avoid customs.

6. **Dual-Enclosure Strategy:** Your "inner sealed box" approach is sound. Aluminum provides EMI shielding and heat dissipation that polycarbonate lacks.

---

## Sources

- [Hammond 1590Z Series - Hammond Mfg](https://www.hammfg.com/electronics/small-case/diecast/1590z)
- [Hammond 1590Z231 - DigiKey](https://www.digikey.com/en/products/detail/hammond-manufacturing/1590Z231/409876)
- [Fibox ALU Series - Fibox](https://www.fibox.com/products/alun)
- [Fibox AL 162609 - Newark](https://www.newark.com/fibox/al-162609/enclosure-din-rail-aluminium-gray/dp/39C7527)
- [Bud AN Series - Bud Industries](https://www.budind.com/product/nema-ip-rated-boxes/an-a-series-enclosure-mounting-flanges/an-2867/)
- [Weidmuller Klippon Enclosures - Weidmuller](https://www.weidmuller.com/en/products/connectivity/enclosure_systems_and_components/klippon_aluminium_enclosures.jsp)
- [Rose Euromas Aluminum - BOPLA](https://www.bopla.de/en/enclosure-technology/euromas-aluminium-euromas-f05)
- [Takachi DIN Rail Enclosures - Takachi](https://www.takachi-enclosure.com/cat/din_rail_enclosures)
- [Hammond 1427DINCLIP - DigiKey](https://www.digikey.com/en/products/detail/hammond-manufacturing/1427DINCLIP/685981)
- [Gore Protective Vents - Gore](https://www.gore.com/products/screw-protective-vents-outdoor-electronics-enclosures)
- [IP67 Junction Boxes - DirectIndustry](https://www.directindustry.com/industrial-manufacturer/ip67-junction-box-159129.html)

---

**Report Compiled By:** Claude Sonnet 4.5 (comprehensive-researcher agent)
**Date:** January 28, 2026
**File:** `/home/tjordan/code/git/openrivercam/spring_2026_ID/research/aluminum_enclosure_research.md`
