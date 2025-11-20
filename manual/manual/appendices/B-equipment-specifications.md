# Appendix B: Equipment Specifications and Procurement

This appendix provides detailed specifications for all equipment needed to deploy an OpenRiverCam system, including purchasing guidance, cost estimates, compatible equipment lists, and alternative options at different price points.

---

## Complete System Overview

A complete OpenRiverCam deployment requires four main subsystems:

1. **Camera System**: For capturing river surface video
2. **Survey Equipment**: RTK GPS for ground control point measurements
3. **Power System**: Solar or utility power for continuous operation
4. **Network System**: Connectivity for data transmission (optional but recommended)

**Total System Cost Ranges (Equipment Only):**
- **Budget Tier**: $3,000-5,000 (used/basic equipment, DIY mounting, manual operation)
- **Standard Tier**: $7,000-10,000 (new mid-range equipment, professional mounting, semi-automated)
- **Premium Tier**: $12,000-15,000 (high-end equipment, engineered mounting, full automation)

**See COST_FRAMEWORK.md for complete cost analysis including:**
- First-year total costs (equipment + survey + installation + training)
- 5-year total cost of ownership (TCO)
- Regional cost variations
- Operating costs breakdown
- Budget planning worksheets

---

## 1. Camera System

### 1.1 IP Camera

**Purpose**: Capture video of river surface for velocity measurement

**Minimum Requirements:**
- Resolution: 1920×1080 (Full HD) minimum, 2560×1440 or higher preferred
- Frame rate: 15-30 fps (frames per second)
- Network: Ethernet (PoE preferred) or WiFi capability
- Environmental: IP66 or better weatherproof rating
- Lens: Adjustable focus, 4-12mm focal length typical
- Power: PoE (Power over Ethernet) or 12V DC
- Night capability: Not required (measurements during daylight only)

**Recommended Specifications:**
- Resolution: 2560×1440 (2K) or 3840×2160 (4K)
- Frame rate: 25-30 fps
- Codec: H.264 or H.265 compression
- PoE: IEEE 802.3af or 802.3at (simplifies installation)
- IR cut filter: Removable (improves daytime image quality)
- Housing: Metal, IP67 rated
- Operating temperature: -20°C to 60°C

**Compatible Camera Models:**

**Budget Option ($80-150):**
- Hikvision DS-2CD2043G0-I (4MP, PoE)
- Dahua IPC-HFW1431S (4MP, PoE)
- Reolink RLC-410 (4MP, PoE)
- TP-Link VIGI C340 (4MP, PoE)

**Mid-Range Option ($150-300):**
- Hikvision DS-2CD2343G0-I (4MP turret, excellent image quality)
- Dahua IPC-HFW2431T-AS (4MP, built-in mic)
- Axis M1065-L (1080p, professional grade)
- Hanwha QNO-7080R (4K, professional)

**Professional Option ($300-600):**
- Axis P1455-LE (1080p, excellent low-light)
- Bosch FLEXIDOME IP starlight 7000 VR (1080p, superior optics)
- Hikvision DS-2CD2783G0-IZS (4K, motorized zoom)

**Smartphone Alternative:**
For temporary deployments or testing, a weatherproof mount with smartphone (minimum 1080p video) can be used. Not recommended for permanent installations.

**Procurement Sources:**
- Security camera distributors (global: B&H Photo, Adorama; regional suppliers)
- Online: Amazon, AliExpress (verify seller reputation)
- Local security system installers (may offer installation services)

**Installation Accessories:**
- Mounting bracket: $20-50 (wall/pole mount)
- Ethernet cable: $0.50-1.00 per meter (outdoor-rated CAT6)
- PoE injector: $15-30 (if network switch does not provide PoE)
- Weatherproof junction box: $10-25 (for cable connections)
- Sunshade (if installing in direct sun): $30-60

**Estimated Camera System Cost: $150-600 + installation materials ($50-100)**

---

### 1.2 Video Recording and Processing

**PtBox (Hardware Option):**
- Small computer (Raspberry Pi or similar) configured for video recording
- Stores video locally and transmits to processing server
- Can trigger recordings at scheduled intervals
- Cost: $100-200 (DIY assembly) or [INFO NEEDED: Commercial PtBox pricing]

**Cloud/Server Recording:**
- Record directly to network video recorder (NVR) or server
- Standard security camera NVR: $150-500 (4-channel models)
- Cloud storage subscriptions: $5-20/month depending on retention period

**Software:**
- pyOpenRiverCam (free, open-source) - https://github.com/localdevices/pyorc
- Requires Python 3.8+ environment
- Processing can run on modest hardware (8GB RAM, modern CPU)

---

## 2. RTK GPS Survey Equipment

### 2.1 GNSS Receivers (Base and Rover)

**Purpose**: Centimeter-accurate surveying of ground control points, camera position, and cross-sections

**System Requirements:**
- Two receivers required: one base station, one rover
- Multi-constellation tracking: GPS + GLONASS + Galileo (+ BeiDou preferred)
- RTK capable with carrier phase tracking
- RTCM3 correction support
- 1-3 cm horizontal accuracy, 2-4 cm vertical accuracy

**Budget Option: ArduSimple simpleRTK Series ($300-500 per receiver)**

**ArduSimple simpleRTK2B Kit:**
- Receiver: u-blox ZED-F9P (multi-band, multi-constellation)
- Base + Rover bundle: ~$600-800
- Accuracy: 1-2 cm RTK
- Radio: Separate purchase required ($100-150)
- Pros: Excellent value, open-source friendly, good documentation
- Cons: Basic housing (not ruggedized), DIY assembly, limited support
- Source: https://www.ardusimple.com/

**What's included:**
- Receiver boards (base + rover)
- Basic antennas
- USB cables

**What's needed additionally:**
- Survey-grade antennas: $100-250 each (recommended upgrade)
- Radio modems: $100-150 total
- Enclosures/housing: $50-100
- Survey pole: $80-150
- Batteries: $50-100
- Data collector (Android device): $150-300

**Total ArduSimple system: $1,500-2,500**

**Mid-Range Option: Commercial RTK Systems ($2,000-4,000 per receiver)**

**Emlid Reach RS2+ Kit:**
- Complete RTK base + rover system: ~$4,000-5,000
- Receiver: Multi-frequency GNSS
- Accuracy: 1 cm + 1 ppm horizontal
- Built-in radio: LoRa long-range
- Rugged housing: IP67, field-ready
- Battery: 22 hours rover, 16 hours base
- Software: ReachView app (iOS/Android)
- Pros: Plug-and-play, excellent support, rugged
- Cons: Higher cost than ArduSimple
- Source: https://emlid.com/

**Tersus Oscar GNSS:**
- Base + Rover bundle: ~$3,500-4,500
- Multi-constellation, RTK
- Built-in radio
- Android app for data collection
- Good value in commercial category
- Source: https://www.tersus-gnss.com/

**CHC Nav Series:**
- Various models: $2,500-5,000 per receiver
- Professional-grade accuracy and reliability
- Widely available internationally
- Source: https://chcnav.com/ or regional distributors

**Professional Option: Survey-Grade Systems ($6,000-12,000 per receiver)**

**Trimble R2/R10/R12 Series:**
- Survey industry standard
- Exceptional accuracy and reliability
- Full support and warranty
- Integration with Trimble software ecosystem
- Premium pricing: $12,000-25,000 for base+rover system
- Source: Authorized Trimble dealers

**Leica GS18:**
- Tilt-compensated (no need to level pole)
- Self-learning technology
- Professional survey accuracy
- Premium pricing: $15,000-30,000 for complete system
- Source: Authorized Leica dealers

**Topcon HiPer Series:**
- Professional accuracy and reliability
- Good international support
- $10,000-20,000 for complete system
- Source: Authorized Topcon dealers

**Recommendation for Humanitarian Deployments:**
- **For most organizations**: Emlid Reach RS2+ or Tersus Oscar (balance of cost, quality, support)
- **For limited budgets**: ArduSimple (requires more technical setup but excellent value)
- **For professional operations**: CHC Nav or entry-level Trimble/Leica

---

### 2.2 GNSS Antennas

**Purpose**: Receive satellite signals for base station and rover

**Antenna Types:**

**Basic Patch Antennas (included with budget systems):**
- Cost: Included or $30-60
- Performance: Adequate for good sky view conditions
- Size: Compact (10-15 cm diameter)
- Multipath rejection: Moderate

**Survey-Grade Antennas (recommended upgrade):**
- Cost: $150-400 each
- Performance: Superior signal quality and multipath rejection
- Size: Larger (15-20 cm diameter)
- Choke ring design reduces multipath errors

**Recommended Models:**
- Tallysman TW3710/TW3740: $200-300 (excellent value)
- Trimble Zephyr 2/3: $300-500 (professional grade)
- Harxon HX-CSX601A: $150-250 (good budget survey antenna)

**Base vs Rover Antenna:**
- Base: Can use larger, heavier antenna (stationary setup)
- Rover: Needs lightweight antenna for pole mounting
- Using identical antennas for both simplifies calibration

**Antenna Cables:**
- Length: Base: 3-5m typical; Rover: 0.5-1.5m
- Type: Low-loss coaxial (RG58 or better)
- Connectors: TNC or SMA (match receiver)
- Cost: $20-60 depending on length and quality

---

### 2.3 Radio Modems (for RTK corrections)

**Purpose**: Transmit RTCM3 corrections from base station to rover in real-time

**Radio Specifications:**

**Frequency:**
- 433 MHz (Europe, Asia, Africa - check local regulations)
- 915 MHz (Americas, Australia - check local regulations)
- Use license-free ISM bands where permitted

**Range:**
- Required: 1-2 km minimum
- Recommended: 5-10 km for flexibility
- Actual range depends on terrain, antennas, power

**Data Rate:**
- Minimum: 9600 bps
- Recommended: 19200-57600 bps
- RTCM3 data: ~500-1000 bytes/second (easily supported)

**Recommended Radio Models:**

**Budget: Serial Radio Modules ($50-80 per pair):**
- HC-12 modules: $15-25 each, 1 km range, basic
- RFD900 compatible: $50-80 each, 15+ km range, excellent
- Pros: Very low cost
- Cons: Require DIY integration, basic antennas

**Mid-Range: Integrated Radio Modems ($100-200 per pair):**
- ArduSimple XBee radio kit: $100-150
- RFD900x: $150-200 (long range, robust)
- Pacific Crest PDL: $200-300 (professional telemetry)
- Pros: Easier integration, better range
- Cons: Higher cost than DIY modules

**LoRa (Long Range) Alternative:**
- ArduSimple SimpleRTK LoRa: $100-150 per module
- Excellent range (10-20 km possible)
- Low power consumption
- Growing ecosystem
- Recommended for most deployments

**Professional: Survey-Grade Radios ($400-800):**
- Usually included with professional RTK systems
- Superior range and reliability
- May require radio license depending on region

**Alternative: NTRIP via Cellular**
- No radio hardware needed
- Rover uses smartphone cellular connection
- Unlimited range (within cell coverage)
- Data cost: Minimal ($1-5/month typical usage)
- Requires cell coverage (not available in all humanitarian contexts)

---

### 2.4 Survey Accessories

**Survey Pole:**
- Length: 2-2.5 meters (telescoping or fixed)
- Material: Carbon fiber (lightweight) or aluminum
- Circular bubble level: Essential for keeping pole vertical
- Cost: $80-200
- Sources: Survey equipment suppliers, Amazon

**Tripod (for base station):**
- Height: 1.5-2.0 meters
- Type: Standard camera/survey tripod
- Stability: Critical - must not move during survey
- Cost: $50-150
- Lightweight carbon fiber: $100-200 (recommended if transporting frequently)

**Measuring Tape:**
- Type: Steel tape (cloth stretches - not suitable)
- Length: 3-5 meters
- Precision: Millimeter graduations
- Cost: $10-25

**Field Supplies:**
- Spray paint or markers: Mark base station position, GCPs
- Field notebook (waterproof): Record measurements, observations
- Carabiners/clips: Secure equipment
- Cable ties: Organize cables
- Duct tape/electrical tape: Field repairs
- Sunscreen, water, first aid: Field safety
- Cost: $50-100 for complete field kit

---

### 2.5 Data Collection Device

**Purpose**: Run SW Maps or similar GIS app to record RTK survey points

**Android Smartphone or Tablet:**

**Minimum Requirements:**
- Android 7.0 or newer
- 2GB RAM minimum, 4GB+ recommended
- GPS not required (using RTK via GNSS Master)
- USB OTG support (for connecting to RTK rover)
- Screen: 5-inch minimum, 7-10 inch tablet preferred for field visibility

**Recommended Devices:**
- Samsung Galaxy Tab A series: $150-250 (good screen size, affordable)
- Lenovo Tab M series: $100-200 (budget option)
- Samsung Galaxy S or A series phone: $200-400 (if tablet not needed)
- Rugged options: $300-600 (if field conditions are harsh)

**Accessories:**
- USB OTG cable: $5-10 (connect RTK receiver to Android)
- Screen protector: $10-20
- Protective case: $20-50
- Power bank: $20-50 (10,000+ mAh for all-day field use)
- Car charger: $10-20

**Software (Free):**
- GNSS Master: Free from Google Play Store
- SW Maps: Free version adequate, Pro version $50/year (adds features)
- Alternative: QField (free, open-source QGIS-based)

**Total Data Collection Cost: $200-400**

---

## 3. Power System

### 3.1 Solar Power System (Off-Grid)

**Purpose**: Provide continuous power to camera and networking equipment in locations without utility power

**System Sizing:**

**Power Requirements (example for typical deployment):**
- IP camera: 5-10W continuous
- Network switch/router: 5-10W
- Recording device (if used): 5-10W
- Total: 15-30W continuous = 360-720 Wh per day

**Solar Panel:**
- Size: 100-200W panel
- Type: Monocrystalline (more efficient) or polycrystalline
- Voltage: 12V or 24V system
- Cost: $80-200
- Mounting: Pole or ground mount ($50-150)

**Battery:**
- Type: Deep cycle AGM or lithium (lithium preferred but more expensive)
- Capacity: 100-200Ah @ 12V (1200-2400 Wh storage)
- Autonomy: 3-5 days without sun (recommended for reliability)
- Cost: AGM $150-300; Lithium $300-600
- Lifespan: AGM 3-5 years; Lithium 8-10 years

**Charge Controller:**
- Type: MPPT (more efficient than PWM)
- Rating: Match panel voltage and current (20-30A typical)
- Cost: $50-150
- Features: Load control, battery protection

**Inverter (if AC power needed):**
- Size: 300-500W pure sine wave
- Cost: $80-200
- Note: Not needed if all equipment runs on DC (PoE camera = DC)

**Enclosure:**
- Weatherproof box for batteries and electronics
- Ventilation for battery off-gassing (AGM) or heat (lithium)
- Lockable for security
- Cost: $50-150

**Complete Solar System Examples:**

**Basic System (12V, 100W panel, AGM battery): $500-800**
- 100W solar panel: $100
- 100Ah AGM battery: $180
- 20A MPPT controller: $60
- Cables, fuses, connectors: $50
- Enclosure and mounting: $100
- Installation materials: $50

**Standard System (12V, 150W panel, Lithium battery): $800-1,200**
- 150W solar panel: $150
- 100Ah lithium battery: $400
- 30A MPPT controller: $100
- Cables, fuses, connectors: $70
- Enclosure and mounting: $150
- Installation materials: $80

**Professional System (24V, dual panels, large lithium): $1,500-2,500**
- 2× 200W solar panels: $400
- 200Ah lithium battery: $800
- 40A MPPT controller: $200
- Complete electrical system: $200
- Professional enclosure: $300
- Installation and grounding: $200

**Procurement Sources:**
- Renogy: Complete solar kits - https://www.renogy.com/
- Victron Energy: Premium charge controllers and inverters
- Local solar equipment suppliers
- Amazon/AliExpress: Individual components (verify ratings)

---

### 3.2 Utility Power System (Grid-Connected)

**Purpose**: Power camera system from existing electrical grid

**Requirements:**
- AC power available at installation site
- Reliable service (minimal outages) or UPS backup

**Components:**

**Power Supply/PoE Injector:**
- Input: 110-240V AC (match local grid)
- Output: 48V PoE or 12V DC depending on camera
- Cost: $15-40

**Surge Protector:**
- Protects equipment from voltage spikes/lightning
- Cost: $20-60
- Essential for outdoor installations

**UPS (Uninterruptible Power Supply) - Recommended:**
- Capacity: 500-1000VA (provides 2-4 hours backup)
- Maintains operation during brief power outages
- Cost: $80-200
- Highly recommended in areas with unreliable power

**Electrical Installation:**
- Outdoor-rated electrical box
- Conduit for cable protection
- GFCI outlet (ground fault protection)
- Installation cost: $100-300 if hiring electrician

**Total Utility Power Cost: $200-600 (including backup)**

---

### 3.3 Hybrid System (Solar + Utility Backup)

**Configuration:**
Primary power from solar, utility power charges batteries when solar insufficient or serves as backup.

**Additional Components:**
- AC-DC battery charger: $50-150
- Automatic transfer switch: $100-200
- Combined system cost: Add $150-350 to solar system cost

**Advantages:**
- Maximum reliability
- Utility power compensates for cloudy periods
- Solar reduces ongoing electricity costs

---

## 4. Network and Connectivity

### 4.1 Local Network Equipment

**Purpose**: Transmit video from camera to recording/processing device

**Network Switch (if multiple devices):**
- 5-8 port Ethernet switch
- PoE support (to power camera)
- Outdoor-rated or enclosed indoors
- Cost: $40-150

**Recommended Models:**
- TP-Link TL-SG1005P (5-port with PoE): $40
- Netgear GS305P (5-port with PoE): $60
- Ubiquiti USW-Flex (5-port, outdoor, PoE): $80

**WiFi Router (if wireless needed):**
- 2.4 + 5 GHz dual-band
- Outdoor model if mounting outside
- Cost: $50-200

---

### 4.2 Cellular Connectivity (Optional)

**Purpose**: Transmit data to remote server, enable remote monitoring

**4G/LTE Router:**
- SIM card slot for cellular data
- Ethernet ports for local network
- External antenna support
- Cost: $100-300

**Recommended Models:**
- GL.iNet Mudi (GL-E750): $140 (compact, good value)
- Teltonika RUT240/RUT950: $150-300 (industrial grade)
- Cradlepoint IBR200: $400+ (professional, expensive)

**Cellular Data Plan:**
- Monthly cost: $10-50 depending on region and data allowance
- Data usage: 1-10 GB/month typical (depends on video upload frequency)
- Prepaid SIM often most economical for humanitarian deployments

**Antenna (if signal weak):**
- External 4G/LTE antenna: $30-80
- Cable: $20-40
- Can significantly improve connection in rural areas

---

## 5. Physical Installation Materials

### 5.1 Camera Mounting

**Pole/Mast:**
- Galvanized steel pipe: 3-6 meters height
- Diameter: 50-100mm (2-4 inches)
- Cost: $100-300 depending on height and local pricing
- Foundation: Concrete base or ground anchor

**Bridge/Structure Mounting:**
- Heavy-duty brackets: $30-80
- Stainless steel hardware (corrosion resistance): $20-50
- U-bolts or clamps for attaching to railings: $15-40

**Installation Labor:**
- DIY possible with basic tools
- Professional installation: $200-800 depending on complexity
- Includes: Pole installation, mounting, cable routing, weatherproofing

---

### 5.2 Staff Gauge

**Purpose**: Visible water level measurement in camera view

**Commercial Staff Gauge:**
- Material: Aluminum or PVC with clear markings
- Length: 2-4 meters depending on water level range
- Graduations: Centimeter markings minimum
- Cost: $80-200
- Sources: Hydrological equipment suppliers

**DIY Option:**
- PVC pipe or treated wood
- Waterproof paint and stencils for markings
- Clear coat for durability
- Cost: $20-50 materials + labor

**Mounting:**
- Secure to stable structure (bridge pier, anchored post)
- Must remain fixed position (any movement invalidates readings)
- Hardware: $20-50

---

### 5.3 Enclosures and Protection

**Equipment Enclosures:**
- Weatherproof NEMA boxes for electronics
- Sizes: Varies by equipment
- Cost: $30-150 each

**Cable Protection:**
- Conduit: $1-3 per meter
- Cable glands/grommets: $2-10 each
- UV-resistant cable ties: $10-20 per package

**Lightning Protection:**
- Grounding rod and wire: $30-60
- Surge arrestors: $40-100
- Professional grounding recommended for permanent installations

---

## 6. Complete System Cost Summaries

### 6.1 Minimal Deployment

**Suitable for**: Temporary installations, pilot testing, limited budgets

**Components:**
- IP Camera (budget): $120
- ArduSimple RTK base + rover: $1,800
- Survey pole and accessories: $200
- Android tablet: $150
- Solar power (basic): $600
- Mounting and installation: $300
- Network: $100
- **Total: $3,270**

**Limitations:**
- Basic equipment may have shorter lifespan
- Less automation (more manual operation)
- Limited remote monitoring

---

### 6.2 Standard Deployment

**Suitable for**: Most humanitarian deployments, good balance of cost and capability

**Components:**
- IP Camera (mid-range): $250
- Emlid Reach RS2+ RTK system: $4,500
- Survey pole and accessories: $300
- Android tablet (ruggedized): $300
- Solar power (standard): $1,000
- Mounting and installation: $600
- Network and connectivity: $300
- Staff gauge: $150
- **Total: $7,400**

**Advantages:**
- Reliable equipment with good support
- Semi-automated operation
- Remote monitoring capable
- Expected lifespan: 5-8 years

---

### 6.3 Professional Deployment

**Suitable for**: Permanent installations, critical monitoring, well-funded programs

**Components:**
- IP Camera (professional): $500
- Professional RTK system: $8,000
- Survey pole and accessories: $500
- Rugged Android tablet: $600
- Solar power (professional): $2,000
- Professional mounting and installation: $1,500
- Network and 4G connectivity: $600
- Staff gauge (commercial): $200
- Lightning protection and grounding: $400
- **Total: $14,300**

**Advantages:**
- Maximum reliability and accuracy
- Full automation and remote management
- Robust construction for harsh environments
- Expected lifespan: 10+ years
- Professional support and warranty

---

## 7. Procurement Guidance

### 7.1 Vendor Evaluation Criteria

**When selecting equipment vendors, consider:**

1. **Local availability**: Can you source locally or must import?
2. **Technical support**: Is support available in your language/region?
3. **Warranty**: What warranty terms are provided?
4. **Spare parts**: Are parts available for repairs?
5. **Training**: Does vendor provide training materials?
6. **References**: Can vendor provide references from similar deployments?

### 7.2 Import Considerations

**For equipment imported to humanitarian deployment locations:**

**Customs and Duties:**
- Research import duties in destination country
- Humanitarian exemptions may be available
- Documentation requirements (invoices, technical specifications)
- Budget 10-30% additional for duties/taxes (varies by country)

**Shipping:**
- Air freight: Faster (3-7 days) but expensive
- Sea freight: Slower (4-8 weeks) but economical for large shipments
- Courier (FedEx, DHL): Good for small, high-value items (RTK equipment)
- Insurance recommended for valuable equipment

**Documentation:**
- Commercial invoice
- Packing list
- Technical specifications (for customs classification)
- End-user certificate (if required for certain electronics)

### 7.3 Bulk Purchasing

**For organizations deploying multiple systems:**

**Volume Discounts:**
- Most vendors offer 10-30% discounts for orders of 5+ units
- Negotiate with vendors - humanitarian work may qualify for educational/NGO pricing
- Emlid, ArduSimple, and others have educational/humanitarian programs

**Standardization Benefits:**
- Common spare parts across all sites
- Simplified training (staff learn one system)
- Bulk procurement of accessories (cables, poles, etc.)

### 7.4 Local Procurement vs Import

**Procure Locally When Possible:**
- Mounting hardware, poles, electrical materials
- Solar panels and batteries (widely available)
- Network switches and basic electronics
- Reduces shipping costs and import delays

**Import Specialized Items:**
- RTK GPS receivers (limited local availability)
- Survey-grade antennas
- Specialized software or licensed components

---

## 8. Maintenance and Spare Parts

### 8.1 Recommended Spare Parts Inventory

**For each deployment site, maintain:**

**Critical Spares (keep on-site):**
- Ethernet cables (3-5 extra): $30
- PoE injector: $20
- Power cables/connectors: $20
- Cable ties, electrical tape: $10
- USB cables: $10
- Fuses for solar system: $10
- **Total critical spares: $100**

**System-Level Spares (keep regionally, support multiple sites):**
- Backup camera (same model): $150-500
- Backup RTK receiver: $300-4,000 (depends on system)
- Spare battery for solar system: $150-400
- Network switch: $50-100
- Charge controller: $60-150

**Annual Maintenance Budget:**
- Plan $200-500 per site per year
- Covers: Battery replacement (every 3-5 years), cable replacement, minor repairs
- Major component replacement (camera, solar panel) budget every 5-8 years

---

## 9. Equipment Comparison Tables

### 9.1 RTK GPS Systems Comparison

| System | Cost | Accuracy | Support | Best For |
|--------|------|----------|---------|----------|
| ArduSimple | $1,500-2,500 | 1-2 cm | Community | Budget-conscious, technical users |
| Emlid Reach RS2+ | $4,000-5,000 | 1 cm + 1ppm | Excellent | Standard humanitarian deployments |
| Tersus Oscar | $3,500-4,500 | 1-2 cm | Good | Good value commercial option |
| CHC Nav | $5,000-10,000 | <1 cm | Professional | Professional operations |
| Trimble/Leica | $12,000-30,000 | <1 cm | Premium | Critical/permanent installations |

### 9.2 Camera Comparison

| Category | Resolution | Cost | Reliability | Use Case |
|----------|-----------|------|-------------|----------|
| Budget IP | 1080p-4MP | $80-150 | Good | Temporary, testing |
| Mid-Range IP | 4MP-4K | $150-300 | Very Good | Standard deployments |
| Professional IP | 1080p-4K | $300-600 | Excellent | Permanent, critical sites |
| Smartphone | 1080p+ | $200-600 | Good | Mobile, temporary only |

### 9.3 Power System Comparison

| System Type | Initial Cost | Operating Cost | Reliability | Best For |
|-------------|--------------|----------------|-------------|----------|
| Solar (Basic) | $500-800 | $0 | Good (80-95% uptime) | Remote, sunny climates |
| Solar (Standard) | $800-1,200 | $0 | Excellent (95-99%) | Most off-grid sites |
| Utility | $200-600 | $3-10/month | Varies by grid | Grid-accessible sites |
| Hybrid | $1,000-1,800 | $2-5/month | Excellent (99%+) | Critical monitoring |

---

## 10. Country-Specific Procurement Notes

### [INFO NEEDED]

This section should include specific procurement guidance for common humanitarian deployment regions:

- **East Africa** (Kenya, Uganda, Ethiopia, Somalia)
  - Local suppliers for solar equipment
  - Import procedures for electronics
  - Typical customs duties

- **West Africa** (Nigeria, Mali, Niger, Chad)
  - Equipment availability
  - Shipping logistics
  - Local technical support options

- **Middle East** (Jordan, Lebanon, Iraq, Yemen)
  - Regional distributors
  - Import restrictions on GPS/surveying equipment
  - Local solar equipment suppliers

- **Southeast Asia** (Indonesia, Philippines, Myanmar, Bangladesh)
  - Electronics availability (often good)
  - Solar equipment (widely available)
  - Camera and network equipment sources

- **Latin America** (Colombia, Venezuela, Honduras, Guatemala)
  - Regional distributors
  - Import considerations
  - Local alternatives

**Note**: Project team should populate this section based on deployment experience in specific countries.

---

## 11. Total Cost of Ownership

### 5-Year TCO Comparison

**Standard Deployment (7 sites, 5-year period):**

| Cost Component | Year 1 | Year 2-4 (annual) | Year 5 | Total |
|----------------|--------|-------------------|--------|-------|
| Equipment (7 systems @ $7,400) | $51,800 | - | - | $51,800 |
| Installation (7 sites @ $600) | $4,200 | - | - | $4,200 |
| Cellular data (7 sites @ $30/mo) | $2,520 | $2,520 | $2,520 | $12,600 |
| Maintenance (7 sites @ $300/yr) | $2,100 | $2,100 | $2,100 | $10,500 |
| Battery replacement | - | - | $2,800 | $2,800 |
| Training and support | $3,000 | $500 | $500 | $4,500 |
| **Annual Total** | **$63,620** | **$5,120** | **$7,920** | **$86,400** |
| **Per site per year** | **$9,089** | **$731** | **$1,131** | **$2,469** |

**Key Insights:**
- Equipment costs are front-loaded (Year 1)
- Ongoing costs are modest ($700-1,000/site/year)
- Major battery replacement needed Year 5
- Total cost per site over 5 years: ~$12,340 ($2,468/year average)

**Compare to Traditional Gauging:**
- Traditional hydrological gauge station: $50,000-200,000 per site
- Annual maintenance: $5,000-15,000 per site
- Requires specialized technician visits

**OpenRiverCam TCO is 10-20× lower than traditional methods while providing comparable data quality for humanitarian decision-making.**

---

## 12. Funding and Procurement Resources

### 12.1 Potential Funding Sources

**Humanitarian Innovation Funds:**
- UNHCR Innovation Fund
- UNICEF Innovation Fund
- WFP Innovation Accelerator
- Start Network Innovation Lab

**Climate Adaptation Funding:**
- Green Climate Fund
- Adaptation Fund
- Climate Investment Funds

**Water/WASH-Specific:**
- Global Water Partnership
- Water.org
- Conrad N. Hilton Foundation (WASH)

**Disaster Risk Reduction:**
- GFDRR (Global Facility for Disaster Reduction and Recovery)
- UNDRR funding mechanisms
- Asian Development Bank (for Asia-Pacific)

### 12.2 Procurement Best Practices

**Competitive Bidding:**
- Solicit quotes from 3+ vendors when possible
- Clearly specify requirements (reference this appendix)
- Include evaluation criteria beyond price (support, warranty, delivery time)

**Phased Procurement:**
- Pilot deployment (1-2 sites) before scaling
- Allows field testing and refinement
- Builds operational experience
- Validates cost estimates

**Partnerships:**
- Partner with academic institutions (may have equipment to loan/share)
- Coordinate with other NGOs deploying similar systems
- National meteorological services may provide base station data (NTRIP)

---

## Appendix B Summary

This appendix has provided:

1. Complete equipment specifications for all system components
2. Budget, mid-range, and professional options with cost ranges
3. Specific product recommendations and procurement sources
4. Installation materials and accessories lists
5. Complete system cost summaries ($3,000-15,000 depending on specification)
6. Procurement guidance including import considerations
7. Spare parts and maintenance planning
8. Equipment comparison tables
9. 5-year total cost of ownership analysis

**For most humanitarian deployments, the Standard Deployment ($7,000-8,000) provides the best balance of cost, reliability, and capability.**

**Questions or updates needed? Contact the OpenRiverCam project team or consult the online documentation at [INFO NEEDED: Project website/documentation URL]**
