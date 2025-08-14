# OpenRiverCam Hardware Specification & Parts Sourcing

You are a hardware engineering specialist focused on designing rugged field monitoring systems for tropical environments. Your task is to create a complete hardware specification and source suitable parts for an autonomous river monitoring station.

## System Requirements

### Core Function
Design a solar-powered monitoring station that captures video of river flow for computer vision analysis, transmits data via 4G, and operates autonomously in Indonesian jungle conditions.

### Technical Specifications Needed

#### Computing Platform
- **Primary**: Raspberry Pi 5 (confirmed requirement)
- Define minimum RAM, storage, and cooling requirements
- Specify case/heatsink needs for tropical operation

#### Camera System
- High-quality camera module compatible with Raspberry Pi 5
- Weatherproof housing with optical clarity
- Field of view suitable for river monitoring (typically 20-50m width)
- Low-light performance for dawn/dusk operation
- Anti-condensation measures for lens clarity

#### Power Management
- Solar panel sizing for continuous operation (consider latitude ~6°S)
- Battery capacity for 3-5 days backup power
- Charge controller with MPPT capability
- Power distribution and monitoring
- Low-power operation modes

#### Connectivity Options
Design separate connectivity solutions with individual pricing:
- **WiFi Connectivity**: WiFi modules, range extenders, outdoor antennas
- **Cellular Connectivity**: 4G/5G modems/HATs, carrier-compatible antennas
- **Satellite Connectivity**: Satellite modems, directional antennas, subscription hardware

#### Environmental Protection
- **Weatherproof enclosure** rated for tropical conditions
- **Humidity control** - active dehumidification or desiccant systems
- **Ventilation** without compromising waterproofing
- **Mounting hardware** for pole or structure installation

#### Grounding & Lightning Protection
- **Grounding systems** - rods, conductors, and connections
- **Lightning arrestors** - surge protection for power and data lines
- **Surge suppressors** - equipment protection from electrical spikes
- **Bonding hardware** - proper electrical grounding implementation

#### Security & Anti-Theft
- **Tamper-evident enclosures** - detect unauthorized access
- **Security fasteners** - specialized bolts and locks
- **Anti-theft mounting** - secure attachment systems
- **Intrusion detection** - sensors for unauthorized access alerts

#### Additional Components
- Power cycling/watchdog systems
- Status indicator LEDs
- Maintenance access ports
- Cable management and strain relief

### Sourcing Requirements

#### Regional Considerations
- Parts available from US suppliers preferred
- Standard US domestic shipping
- US technical support availability
- No customs or import considerations for build phase

#### Budget Tier Requirements
Design solutions for three distinct budget categories to enable flexible deployment strategies:

**Low Budget Tier ($200-300 USD)**
- Essential components only
- Basic functionality with manual intervention acceptable
- 3-6 months operational life expectancy
- Suitable for proof-of-concept or high-volume basic deployments

**Mid Budget Tier ($400-500 USD)**
- Balanced cost-effectiveness with reliable operation
- 6-12 months autonomous operation capability
- Standard deployment tier for most monitoring locations
- Good reliability with reasonable feature set

**High Budget Tier ($600-800 USD)**
- Premium components with redundant systems
- 12+ months autonomous operation
- Maximum reliability for critical monitoring locations
- Advanced features like self-diagnostics and remote monitoring

#### Quality Standards
- Industrial/commercial grade components preferred
- IP65/IP67 ratings for outdoor components
- Operating temperature range: 20-40°C
- Humidity tolerance up to 95% RH

## Deliverables Required

For each budget tier (Low, Mid, High), provide:

1. **Complete Bill of Materials (BOM)** for each tier with:

**Required BOM Format - CSV Output:**
Save all BOMs as CSV files in the project directory:

**File Names:**
- `bom_low_budget.csv` - Low budget tier BOM
- `bom_mid_budget.csv` - Mid budget tier BOM  
- `bom_high_budget.csv` - High budget tier BOM
- `bom_connectivity_wifi.csv` - WiFi connectivity add-on pricing
- `bom_connectivity_cellular.csv` - Cellular connectivity add-on pricing
- `bom_connectivity_satellite.csv` - Satellite connectivity add-on pricing

**CSV Headers:**
```
Component_Category,Item_Description,Critical_Specs,Quantity,Unit_Cost_USD,Total_Cost_USD,Supplier,Product_Link,Notes
```

**Example CSV Row:**
```
Computing Platform,Raspberry Pi 5 8GB,ARM Cortex-A76 8GB RAM WiFi6 BT5.0,1,80.00,80.00,Element14,https://...,Primary computing unit
```

**Required Information for Each Item:**
   - **Critical Specs**: Key technical specifications (power consumption, operating temp, IP rating, etc.)
   - **Quantity**: Exact quantity needed per system
   - **Unit Cost**: Individual component cost in USD including any applicable taxes
   - **Total Cost**: Unit cost × quantity
   - **Supplier**: Primary supplier name with regional availability
   - **Product Link**: Direct URL to product page for verification and ordering

**BOM Categories to Include:**
   - Computing Platform (Pi 5, storage, cooling)
   - Camera System (module, housing, optics)
   - Power Management (solar, battery, charge controller)
   - Connectivity Options (separate pricing for WiFi, Cellular, Satellite)
   - Environmental Protection (enclosure, humidity control, mounting)
   - Grounding & Lightning Protection (rods, arrestors, surge protection)
   - Security & Anti-Theft (tamper-evident, locks, intrusion detection)
   - Monitoring & Control (watchdog, indicators)
   - Assembly Hardware (cables, connectors, fasteners)

**Cost Calculation Requirements:**
   - Include US domestic shipping costs
   - Use US supplier pricing
   - Provide alternative US suppliers for critical components
   - Include 10% contingency in total cost calculations

2. **Comparative System Integration Plans**:
   - Assembly instructions for each budget tier
   - Wiring diagrams and connections
   - Mounting and installation requirements by tier
   - Testing and validation procedures
   - Upgrade path considerations between tiers

3. **Tiered Environmental Design Solutions**:
   - Basic vs. advanced condensation prevention strategies
   - Humidity management approaches by budget level
   - Thermal management solutions (passive vs. active)
   - Weatherproofing methodology variations
   - Grounding and lightning protection by budget tier
   - Security and anti-theft measures by budget level

4. **Budget-Specific Operational Specifications**:
   - Power consumption analysis for each tier
   - Battery life and solar sizing by budget level
   - Data transmission capabilities and limitations by connectivity type
   - Maintenance schedule recommendations per tier
   - Performance trade-offs documentation
   - Security and theft deterrent effectiveness

5. **Connectivity Options Analysis**:
   - Separate BOMs and pricing for WiFi, Cellular, and Satellite options
   - Coverage area and reliability comparison
   - Data throughput and latency specifications
   - Power consumption differences between connectivity types
   - Installation and maintenance requirements for each option

6. **Budget Tier Comparison Matrix**:
   - Feature comparison across all three tiers
   - Cost-benefit analysis with detailed cost breakdowns
   - Deployment scenario recommendations
   - Risk assessment for each budget level
   - Component upgrade/downgrade paths between tiers
   - Connectivity option recommendations by budget and use case

7. **Supplier Verification and Sourcing Plan**:
   - Verified availability from US suppliers
   - Lead times and minimum order quantities
   - US domestic shipping costs and delivery timeframes
   - Distributor contacts and support availability
   - Bulk pricing analysis for multiple unit orders
   - Alternative sourcing options for critical components

8. **Pre-Integrated Solutions and Open Source Analysis**:
   - **Commercial Solutions**: Research existing weather stations, IoT platforms, and monitoring systems that could be adapted
   - **Open Source Projects**: Identify relevant GitHub repositories, community projects, and maker solutions
   - **Cost-Benefit Analysis**: Compare pre-integrated vs. custom build costs and effort
   - **Adaptation Assessment**: Evaluate modification requirements for OpenRiverCam integration
   - **Community Support**: Document active development, user base, and maintenance status
   - **Reference Documentation**: Provide URLs, project status, and compatibility notes

## Success Criteria by Budget Tier

### Low Budget Tier Success Criteria
- System operates for 3-6 months with minimal intervention
- Basic video capture in good weather conditions
- Periodic data transmission capability
- Total cost under $300 per unit
- Simple assembly and testing in US

### Mid Budget Tier Success Criteria
- System operates autonomously for 6-12 months
- Clear video capture in most weather conditions
- Reliable 4G data transmission
- Total cost under $500 per unit
- Assembly and testing capability in US

### High Budget Tier Success Criteria
- System operates autonomously for 12+ months
- Clear video capture in all weather conditions including storms
- Continuous reliable 4G data transmission with redundancy
- Advanced monitoring and self-diagnostic capabilities
- Total cost under $800 per unit
- Assembly and testing in US with minimal maintenance design

Focus on practical, field-tested solutions suitable for remote deployment in challenging environmental conditions. Prioritize reliability and maintainability over advanced features.

## Research Requirements for Pre-Integrated Solutions

### Commercial Solution Categories to Research
1. **Weather Monitoring Stations** - Davis Instruments, Campbell Scientific, Onset HOBO
2. **Industrial IoT Platforms** - Particle, Arduino Pro, Adafruit IO systems
3. **Environmental Sensor Networks** - NEON, LoRaWAN platforms, cellular IoT gateways
4. **Educational/Maker Platforms** - SparkFun weather kits, Adafruit environmental systems
5. **Solar Power Kits** - Goal Zero, Renogy, BattleBorn systems with data logging

### Open Source Project Research Areas
1. **River/Water Monitoring** - Search GitHub for "river monitoring", "water level sensor", "stream gauge"
2. **Environmental Sensing** - Arduino weather stations, Raspberry Pi sensor networks
3. **Solar Power Management** - Open source MPPT controllers, battery monitoring systems
4. **Cellular/WiFi Data Logging** - Remote sensor data transmission projects
5. **Computer Vision Water Flow** - OpenCV flow analysis, particle tracking systems

### Documentation Format for References
Create additional CSV file: `reference_solutions.csv` with columns:
```
Solution_Type,Project_Name,URL,Budget_Tier_Fit,Cost_Estimate,Adaptation_Effort,Active_Status,Notes
```

## BOM Quality Assurance Requirements

### Supplier Link Verification
- All product links must be active and lead to correct items
- Verify pricing accuracy within 30 days of BOM creation
- Confirm product availability and stock status
- Include alternative product links for critical components

### Technical Specification Validation
- Verify all critical specs meet operational requirements
- Cross-reference power consumption with solar/battery sizing
- Confirm environmental ratings (IP65/67, temperature, humidity)
- Validate compatibility between components (voltage, connectors, etc.)

### Regional Sourcing Priorities
1. **Primary**: Major US electronics distributors (Digi-Key, Mouser, Element14)
2. **Secondary**: Direct manufacturer sales within US
3. **Tertiary**: Amazon Business or other US commercial suppliers
4. **Emergency**: Alternative US suppliers for critical components

### Cost Accuracy Standards
- Include all applicable US taxes and fees
- Use current USD pricing at time of BOM creation
- Add realistic US domestic shipping estimates
- Account for standard US sales tax considerations
- Provide cost range estimates (±10%) to account for price fluctuations

### CSV File Output Requirements
- Save all BOMs and reference data as CSV files in project directory
- Use consistent naming convention: `bom_[tier]_[type].csv`
- Include header row with standardized column names
- Ensure all URLs are active and properly formatted
- Validate CSV format for easy import/analysis