# OpenRiverCam Cost Framework

**Version:** 1.0
**Date:** November 2025
**Status:** AUTHORITATIVE REFERENCE - Use these figures consistently throughout all manual chapters

---

## Purpose

This document provides the **standardized cost framework** for OpenRiverCam deployments. All chapters, appendices, and examples in the manual must reference these figures consistently.

---

## Three-Tier System Cost Model

### Budget Tier: $3,000 - $5,000

**Target Use Case:** Pilot deployments, low-risk monitoring, temporary installations

**Equipment Specifications:**
- **Camera:** Used/refurbished IP camera (1080p minimum), $150-300
- **RTK GPS:** ArduSimple simpleRTK2B base + rover kit, $600-800
- **Power:** Basic solar setup (50W panel, 50Ah battery), $300-500
- **Network:** Cellular USB modem, $50-100
- **Computing:** Raspberry Pi 4 or used mini PC, $75-150
- **Mounting:** DIY poles/brackets, basic tripod, $200-400
- **Accessories:** Cables, enclosures, grounding, $150-300
- **Shipping/Import:** ~15% of equipment cost, $200-400

**Total Equipment:** $2,700-$4,000

**Additional First-Year Costs:**
- Survey equipment rental (3 days): $200-400
- Installation labor (2-3 days): $500-1,500
- Training and commissioning: $300-800
- **First-Year Total: $3,700-$6,700**

**Annual Operating Costs (Years 2-5):**
- Cellular data (5GB/month): $150-400/year
- Maintenance visits (2x/year): $400-800/year
- Battery replacement (year 3-4): $100-200
- **Annual Operating: $650-1,400/year**

**5-Year Total Cost of Ownership: $6,400-$13,000**

---

### Standard Tier: $7,000 - $10,000

**Target Use Case:** Operational monitoring, community early warning, long-term deployments

**Equipment Specifications:**
- **Camera:** New mid-range IP camera (1080p-4K, PoE, weather-rated), $400-700
- **RTK GPS:** ArduSimple or Emlid Reach RS2+ base + rover, $1,200-2,000
- **Power:** Commercial solar (100W panel, 100Ah AGM battery, MPPT controller), $700-1,200
- **Network:** Industrial cellular router with external antenna, $200-400
- **Computing:** Intel NUC or equivalent mini PC, $300-500
- **Mounting:** Professional pole mount or engineered bracket, $600-1,000
- **Accessories:** Professional-grade cables, IP66 enclosures, grounding system, $400-700
- **Shipping/Import:** ~12% of equipment cost, $400-700

**Total Equipment:** $6,000-$9,000

**Additional First-Year Costs:**
- Survey equipment (owned or rental): $500-1,000
- Professional installation (3-5 days): $1,500-3,000
- Training and commissioning: $800-1,500
- **First-Year Total: $8,800-$14,500**

**Annual Operating Costs (Years 2-5):**
- Cellular data (10GB/month): $300-600/year
- Maintenance visits (3x/year): $800-1,500/year
- Component replacement reserve: $200-400/year
- **Annual Operating: $1,300-$2,500/year**

**5-Year Total Cost of Ownership: $14,000-$24,500**

---

### Premium Tier: $12,000 - $15,000

**Target Use Case:** Critical infrastructure monitoring, national met services, research deployments

**Equipment Specifications:**
- **Camera:** High-end IP camera (4K, advanced PoE, rated IP67+), $800-1,500
- **RTK GPS:** Emlid Reach RS2+ or Septentrio mosaic-go, $2,000-3,500
- **Power:** Robust solar (200W panels, 200Ah lithium battery, advanced controller), $1,500-2,500
- **Network:** Industrial router with bonded cellular + satellite backup, $500-800
- **Computing:** Fanless industrial PC or high-end NUC, $600-1,000
- **Mounting:** Engineered mounting structure with anti-vibration, $1,200-2,000
- **Accessories:** Professional installation kit, surge protection, monitoring, $800-1,200
- **Shipping/Import:** ~10% of equipment cost, $700-1,000

**Total Equipment:** $10,000-$14,000

**Additional First-Year Costs:**
- Professional survey equipment (owned): $2,000-4,000
- Expert installation and commissioning (5-7 days): $3,000-5,000
- Comprehensive training program: $1,500-2,500
- **First-Year Total: $16,500-$25,500**

**Annual Operating Costs (Years 2-5):**
- Cellular + satellite backup data: $600-1,200/year
- Professional maintenance (4x/year): $1,500-3,000/year
- Component replacement and upgrades: $400-800/year
- **Annual Operating: $2,500-$5,000/year**

**5-Year Total Cost of Ownership: $26,500-$45,500**

---

## Cost Breakdown by Subsystem

### Camera Subsystem

| Tier | Equipment | Cost Range | Notes |
|------|-----------|------------|-------|
| Budget | Used 1080p IP camera, basic PoE, mounting bracket | $150-$400 | Test thoroughly before deployment |
| Standard | New 1080p-4K IP camera, PoE+, weatherproof housing | $400-$900 | Recommended for operational use |
| Premium | High-end 4K IP camera, advanced features, industrial rating | $800-$1,700 | Critical infrastructure applications |

**Key Specifications Across Tiers:**
- Minimum resolution: 1920x1080 (1080p)
- Frame rate: 10-30 fps
- Power: PoE (Power over Ethernet) preferred
- Weather rating: IP66 minimum (IP67+ for harsh environments)
- Compression: H.264 or H.265
- Mounting: Adjustable bracket for 15-45° angle

---

### RTK GPS Subsystem

| Tier | Equipment | Cost Range | Notes |
|------|-----------|------------|-------|
| Budget | ArduSimple simpleRTK2B kit (base + rover) | $600-$800 | Excellent value, proven performance |
| Standard | ArduSimple or Emlid Reach RS2+ | $1,200-$2,000 | Reliable, widely used |
| Premium | Emlid RS2+ or Septentrio mosaic-go | $2,000-$3,500 | Professional-grade accuracy |

**Survey Accuracy Targets:**
- RTK relative accuracy: 1-3 cm horizontal, 2-4 cm vertical
- Post-processed (PPP) absolute accuracy: 2-5 cm
- Survey-in accuracy: ~25 cm (improved to 2-5 cm with PPP)

**Operating Requirements:**
- Clear sky view >15° elevation
- Distance from metal/reflective surfaces: >10m
- Radio link or cellular connection for base-rover communication
- RINEX logging capability for PPP post-processing

---

### Power Subsystem

| Tier | Equipment | Cost Range | Notes |
|------|-----------|------------|-------|
| Budget | 50W solar panel, 50Ah AGM battery, basic controller | $300-$600 | 3-4 days autonomy typical |
| Standard | 100W solar, 100Ah AGM/LiFePO4, MPPT controller | $700-$1,400 | 5-7 days autonomy |
| Premium | 200W solar, 200Ah LiFePO4, advanced monitoring | $1,500-$3,000 | 10+ days autonomy, extreme conditions |

**Power Budget Calculations:**

**Typical Daily Consumption:**
- Camera (PoE): 5-10W continuous = 120-240 Wh/day
- Computing (Pi/NUC): 5-15W continuous = 120-360 Wh/day
- RTK Rover (survey only): 3W for 8 hours = 24 Wh/day
- Cellular router: 2-5W continuous = 48-120 Wh/day
- **Total daily: 300-750 Wh/day** (varies by configuration)

**Solar Sizing:**
- Budget tier: 50W × 5 sun-hours × 0.7 efficiency = 175 Wh/day generation
- Standard tier: 100W × 5 sun-hours × 0.7 efficiency = 350 Wh/day generation
- Premium tier: 200W × 5 sun-hours × 0.7 efficiency = 700 Wh/day generation

**Autonomy Calculation:**
- Battery capacity × 0.5 (50% DOD limit) / daily consumption
- Example: 100Ah × 12V × 0.5 / 350 Wh = 1.7 days minimum, 5-7 days typical with solar

---

### Network Subsystem

| Tier | Equipment | Cost Range | Notes |
|------|-----------|------------|-------|
| Budget | USB cellular modem, basic SIM | $50-$150 | Adequate for most deployments |
| Standard | Industrial cellular router, external antenna | $200-$500 | Improved reliability |
| Premium | Bonded cellular + satellite backup | $500-$1,000 | Maximum uptime assurance |

**Data Requirements:**
- Video uploads: 10-50 MB per sample (depends on resolution, compression)
- Metadata and results: <1 MB per sample
- Typical frequency: Every 5-15 minutes (configurable)
- **Monthly data usage: 2-20 GB** (varies by configuration)

**Monthly Connectivity Costs:**
- Budget (2-5 GB): $10-25/month
- Standard (5-15 GB): $25-50/month
- Premium (15-30 GB + satellite backup): $50-100/month

---

### Computing and Software Subsystem

| Tier | Equipment | Cost Range | Notes |
|------|-----------|------------|-------|
| Budget | Raspberry Pi 4 (4GB) or used mini PC | $75-$200 | DIY PtBox assembly |
| Standard | Intel NUC (8GB RAM, 256GB SSD) | $300-$600 | Reliable performance |
| Premium | Fanless industrial PC | $600-$1,200 | Extreme temperature tolerance |

**Software Stack (All Open Source - No License Costs):**
- pyOpenRiverCam (pyORC): Free, open source
- OpenCV, Python ecosystem: Free, open source
- Operating system (Linux): Free
- QGIS (survey processing): Free, open source
- RTKLIB (GNSS processing): Free, open source

**Optional Commercial Software:**
- SW Maps (survey app): ~$25-50/year per user
- Advanced PIV algorithms: Varies (research license may be needed)

---

### Mounting and Installation Hardware

| Tier | Equipment | Cost Range | Notes |
|------|-----------|------------|-------|
| Budget | DIY pole mount, basic brackets | $200-$500 | User fabrication or local welding |
| Standard | Commercial pole mount, professional brackets | $600-$1,200 | Engineered for stability |
| Premium | Custom engineered mounting structure | $1,200-$2,500 | Anti-vibration, high wind loads |

**Typical Mounting Requirements:**
- Camera height: 5-10 meters above water
- Viewing angle: 15-45° downstream
- Stability: Withstand wind loads, minimize vibration
- Accessibility: Serviceable with ladder or lift
- Security: Theft/vandalism deterrence

---

## Non-Equipment Costs

### Survey and Installation Services

**Initial Site Survey (One-Time):**
- Equipment rental (if not owned): $200-1,000 for 3-5 days
- Labor (surveyor or trained IM officer): $500-2,000 (2-5 days)
- Travel and logistics: $200-800
- **Total survey cost: $900-$3,800**

**Equipment Installation (One-Time):**
- Installation labor: $500-3,000 (varies by complexity, 2-7 days)
- Specialized equipment (lift, crane if needed): $200-1,000
- Permits and approvals: $0-500 (varies by location)
- **Total installation cost: $700-$4,500**

**Training and Commissioning (One-Time):**
- Software configuration and setup: $300-1,000
- User training (1-3 people, 1-3 days): $500-2,000
- Documentation and handover: $200-500
- **Total training cost: $1,000-$3,500**

### Annual Operating Costs

**Connectivity:**
- Budget tier: $120-300/year (2-5 GB/month at $10-25/month)
- Standard tier: $300-600/year (5-15 GB/month at $25-50/month)
- Premium tier: $600-1,200/year (15-30 GB/month + backup at $50-100/month)

**Maintenance:**
- Routine inspections: 2-4 visits per year
- Labor: $200-500 per visit (cleaning, checks, minor repairs)
- Travel: $100-300 per visit
- **Total maintenance: $600-3,200/year**

**Component Replacement:**
- Budget tier: $200-500/year (higher failure rate, lower component costs)
- Standard tier: $300-800/year (moderate replacement cycle)
- Premium tier: $400-1,000/year (lower failure rate, higher component costs)

**Contingency and Unexpected:**
- Vandalism/theft insurance or reserve: $100-500/year
- Extreme weather damage reserve: $100-400/year
- **Total contingency: $200-900/year**

---

## Regional Cost Variations

**Note:** Costs vary significantly by region due to import duties, local labor rates, shipping, and market availability.

### Regional Multipliers (Approximate)

| Region | Equipment Multiplier | Labor Multiplier | Notes |
|--------|---------------------|------------------|-------|
| North America / Western Europe | 1.0x | 1.5-2.0x | Base reference, high labor costs |
| Eastern Europe / Latin America | 0.9-1.1x | 0.6-1.0x | Moderate costs overall |
| Sub-Saharan Africa | 1.2-1.5x | 0.4-0.8x | High import duties, lower labor |
| South Asia | 0.8-1.0x | 0.3-0.6x | Lower equipment and labor costs |
| Southeast Asia | 0.9-1.1x | 0.4-0.7x | Variable by country |

### Regional Considerations:

**Import and Shipping:**
- Import duties: 0-30% (varies widely by country and equipment classification)
- Shipping: $200-1,000 depending on origin, destination, and freight method
- Customs clearance: $100-500 (documentation, broker fees if needed)

**Local Procurement:**
- Solar panels and batteries: Often available locally, can reduce shipping
- Cameras: May be available locally but verify specifications
- RTK GPS: Usually imported (specialized equipment)
- Mounting hardware: Often fabricated locally at lower cost

**Labor Rates:**
- Technical staff (IM officer, surveyor): $20-100/day depending on region
- Installation crew: $15-80/day per person
- Training: $30-150/hour for expert trainer

---

## Comparison with Traditional Methods

**Traditional Stream Gauging Station:**

| Component | Cost Range | Notes |
|-----------|------------|-------|
| Staff gauge or pressure transducer | $500-3,000 | Water level measurement only |
| Datalogger and telemetry | $2,000-8,000 | Basic recording and transmission |
| Installation (concrete, mounting) | $5,000-15,000 | Permanent structure in river |
| Rating curve development | $3,000-10,000 | Multiple ADCP/current meter surveys |
| Ongoing ADCP surveys (annual) | $2,000-5,000/year | Maintain rating curve validity |
| **Total first year** | **$12,500-$41,000** | |
| **5-year total** | **$20,500-$61,000** | |

**Advantages of Traditional Gauging:**
- Proven technology, long track record
- Direct water level measurement (no camera/image processing)
- Less affected by lighting and surface conditions
- Established protocols and standards

**Disadvantages vs OpenRiverCam:**
- Higher installation costs (permanent structure)
- Requires in-stream construction (environmental permits)
- Dangerous during floods (manual measurements)
- Rating curve maintenance requires recurring ADCP surveys

---

## Budget Planning Worksheet

### Step 1: Determine Site Requirements

- [ ] Camera viewing angle achievable? (15-45°, 5-10m height)
- [ ] Adequate surface features (tracers) present?
- [ ] Power available (grid, solar, hybrid)?
- [ ] Network connectivity (cellular signal strength)?
- [ ] Security considerations (theft/vandalism risk)?

### Step 2: Select Equipment Tier

Based on requirements and risk tolerance:
- [ ] **Budget tier** ($3-5K equipment) - Pilot or temporary deployment
- [ ] **Standard tier** ($7-10K equipment) - Operational monitoring
- [ ] **Premium tier** ($12-15K equipment) - Critical infrastructure

### Step 3: Calculate Total First-Year Cost

| Item | Budget Tier | Standard Tier | Premium Tier | Your Cost |
|------|-------------|---------------|--------------|-----------|
| Equipment | $2,700-4,000 | $6,000-9,000 | $10,000-14,000 | |
| Survey | $900-2,000 | $1,500-2,500 | $2,000-3,800 | |
| Installation | $700-2,000 | $1,500-3,000 | $3,000-4,500 | |
| Training | $1,000-2,000 | $1,500-2,500 | $1,500-3,500 | |
| **TOTAL YEAR 1** | **$5,300-10,000** | **$10,500-17,000** | **$16,500-25,800** | |

### Step 4: Calculate Annual Operating Costs (Years 2-5)

| Item | Budget Tier | Standard Tier | Premium Tier | Your Cost |
|------|-------------|---------------|--------------|-----------|
| Connectivity | $120-300 | $300-600 | $600-1,200 | |
| Maintenance | $600-1,600 | $1,000-2,400 | $1,500-3,200 | |
| Replacement | $200-500 | $300-800 | $400-1,000 | |
| Contingency | $200-500 | $300-700 | $400-900 | |
| **ANNUAL OPERATING** | **$1,120-2,900** | **$1,900-4,500** | **$2,900-6,300** | |

### Step 5: Calculate 5-Year Total Cost of Ownership

| Item | Budget Tier | Standard Tier | Premium Tier | Your Cost |
|------|-------------|---------------|--------------|-----------|
| Year 1 (see above) | $5,300-10,000 | $10,500-17,000 | $16,500-25,800 | |
| Years 2-5 (4 years) | $4,480-11,600 | $7,600-18,000 | $11,600-25,200 | |
| **5-YEAR TCO** | **$9,780-21,600** | **$18,100-35,000** | **$28,100-51,000** | |

### Step 6: Apply Regional Adjustments

If deploying outside North America/Western Europe:
- Equipment costs × regional multiplier (see table above)
- Labor costs × regional multiplier
- Add import duties and shipping (10-30% of equipment cost typical)

---

## Procurement Strategies

### For Humanitarian Organizations

**Budget Optimization:**
1. **Phased procurement:** Buy survey equipment first, test methodology, then commit to camera/power
2. **Shared resources:** Share RTK GPS equipment across multiple deployment sites (use sequentially)
3. **Local fabrication:** Mounting hardware often cheaper if fabricated locally
4. **Refurbished equipment:** Used cameras and computing hardware can reduce costs 30-50%
5. **Bulk purchasing:** Discounts available for multi-site deployments

**Humanitarian Procurement Programs:**
- **UNHCR Supply Division:** Pre-approved vendors, negotiated pricing
- **WFP Global Commodity Management Facility:** Bulk procurement assistance
- **IFRC Supply Chain Services:** Consolidated shipping and customs clearance
- **UNICEF Supply Division:** Electronic equipment sourcing

**Grant Funding Sources:**
- **Climate adaptation funds:** Green Climate Fund, Adaptation Fund
- **Humanitarian Innovation Fund:** Early-stage technology deployment
- **Tech for humanitarian aid:** Microsoft AI for Humanitarian Action, Google.org
- **Start Network Innovation Lab:** Pilot funding for early warning systems

### For National Meteorological Services

**Considerations:**
1. **Standards compliance:** Verify WMO standards alignment (GCOS, WIGOS)
2. **Interoperability:** Ensure data formats compatible with national hydrological databases
3. **Long-term support:** Prioritize equipment with established support networks
4. **Calibration traceability:** Document survey procedures for quality assurance
5. **Multi-site networks:** Plan for centralized data management and QC

**Potential Funding:**
- **WMO HydroHub:** Technology deployment support
- **GEO (Group on Earth Observations):** Earth observation infrastructure
- **World Bank Climate Resilience Programs:** Infrastructure investment
- **Bilateral development assistance:** USAID, DFID, GIZ, AFD programs

---

## Cost-Effectiveness Analysis

### Per-Site Cost Comparison (5-Year TCO)

| Method | Equipment | Installation | Annual Ops | 5-Year Total |
|--------|-----------|--------------|------------|--------------|
| **ORC Budget** | $3,000-5,000 | $2,600-6,000 | $1,100-2,900 | $10,000-22,000 |
| **ORC Standard** | $7,000-10,000 | $4,500-8,000 | $1,900-4,500 | $18,000-36,000 |
| **ORC Premium** | $12,000-15,000 | $6,500-11,000 | $2,900-6,300 | $28,000-51,000 |
| **Traditional Gauge** | $2,500-11,000 | $10,000-30,000 | $2,000-6,000 | $21,000-61,000 |
| **ADCP Mobile** | $20,000-35,000 | $2,000-5,000 | $3,000-8,000 | $34,000-67,000 |

**Cost per Data Point:**
- OpenRiverCam: Continuous (every 5-15 minutes) = ~35,000-100,000 measurements/year
- Traditional gauge: Continuous (every 15 minutes) = ~35,000 measurements/year (water level only, discharge via rating curve)
- ADCP mobile: Discrete (monthly surveys) = ~12 measurements/year

**Labor Intensity:**
- OpenRiverCam: 2-4 maintenance visits/year (low labor requirement)
- Traditional gauge: 2-4 maintenance visits/year + annual rating curve survey
- ADCP mobile: 12 site visits/year (high labor requirement)

---

## Total Cost of Ownership: Detailed Example

**Example: Standard Tier Deployment in East Africa**

### Year 1 (Deployment Year)

**Equipment (Regional adjustment: 1.2x):**
- Camera system: $600 × 1.2 = $720
- RTK GPS: $1,800 × 1.2 = $2,160
- Power system: $1,000 × 1.2 = $1,200
- Network: $350 × 1.2 = $420
- Computing: $450 × 1.2 = $540
- Mounting: $800 × 1.2 = $960
- Accessories: $550 × 1.2 = $660
- **Subtotal equipment:** $6,660

**Import and Shipping:**
- Shipping: $600
- Import duties (15%): $1,089
- Customs broker: $150
- **Subtotal import:** $1,839

**Survey (local rates: 0.5x):**
- Equipment rental: $400
- Labor (surveyor, 4 days): $160
- Travel/logistics: $300
- **Subtotal survey:** $860

**Installation (local rates: 0.5x):**
- Installation crew (3 days, 2 people): $540
- Equipment rental (lift): $200
- Local permits: $100
- **Subtotal installation:** $840

**Training:**
- Software setup (remote): $500
- On-site training (2 days): $400
- Documentation: $200
- **Subtotal training:** $1,100

**YEAR 1 TOTAL: $11,299**

### Years 2-5 (Operations)

**Annual Connectivity:**
- Cellular data (8GB/month): $384/year

**Annual Maintenance (local rates: 0.5x):**
- Routine visits (3x/year): $450/year
- Cleaning and inspection: $300/year
- Travel: $450/year
- **Subtotal maintenance:** $1,200/year

**Component Replacement Reserve:**
- Annual reserve: $500/year

**Contingency:**
- Insurance/reserve: $400/year

**ANNUAL OPERATING (Years 2-5): $2,484/year**

### 5-Year TCO Summary

- Year 1: $11,299
- Years 2-5: $2,484 × 4 = $9,936
- **5-YEAR TOTAL: $21,235**

**Cost per year (amortized): $4,247/year**
**Cost per discharge measurement (@ 35,000/year): $0.12**

---

## Key Takeaways for Budget Planning

1. **Equipment represents 50-60% of Year 1 costs** - Focus procurement efforts here
2. **Regional multipliers significantly affect total cost** - Plan for 20-50% variation
3. **Operating costs are substantial** - Budget $1,000-6,000/year ongoing
4. **Labor costs vary 5x by region** - Local rates strongly influence TCO
5. **5-year TCO ranges $10K-50K per site** - Plan multi-year funding accordingly

---

## Version History

**Version 1.0 (November 2025):**
- Initial standardized cost framework
- Three-tier system model established
- Regional variations documented
- Comparison with traditional methods included

**Next Review:** January 2026 or upon significant equipment price changes

---

**For questions or updates to this cost framework, contact:** [INFO NEEDED: Project finance/procurement contact]
