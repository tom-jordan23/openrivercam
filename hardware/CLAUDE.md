# OpenRiverCam Hardware Build Project

## Project Overview
This project builds a low-cost, open-source river monitoring station using computer vision to measure water flow in Indonesian rivers. The hardware system will be deployed in collaboration with the Indonesian Red Cross (PMI) to improve flood monitoring and community disaster preparedness.

## Hardware Mission Statement
Build a weatherproof, solar-powered monitoring station that can operate autonomously in tropical jungle conditions for extended periods, capturing video data for the OpenRiverCam software to analyze river flow patterns.

## Core Hardware Requirements

### Primary Components
- **Raspberry Pi 5** - Main computing platform
- **Two (2) sealed IP67/IP68 cameras** - Factory-sealed cameras with USB or wireless connectivity (eliminates fogging/humidity issues)
- **4G cellular or WiFi connectivity** - For data transmission to remote servers
- **Solar power system** - Primary power source for autonomous operation (50-100% overbuilt for adverse weather)
- **LiFePO4 battery** - Long-life, environmentally friendly, no toxic materials
- **Weatherproof enclosure** - Protection for computing/power components

### Design Principles
- **Overbuild power:** 50-100% headroom for rainy season/winter cloud cover
- **Green choices:** LiFePO4 batteries (no lead, no acid, recyclable), solar primary power
- **Reliability first:** Excess capacity is cheap insurance for remote deployments

### Camera Strategy: Sealed Units (Primary Approach)
The system requires **two cameras** per station. The preferred approach uses factory-sealed IP67/IP68 cameras that connect via:
- **USB** - Most reliable for data integrity (up to 5m native, 30m with active repeater, 100m via USB-over-Ethernet)
- **WiFi** - Better for sites where cables cannot be run (use P2P wireless bridge for extended range)

**Advantages of sealed cameras:**
- Factory sealing eliminates condensation and fogging issues
- No desiccant maintenance required
- Industrial-grade environmental protection
- Simplified enclosure design (only computing/power needs protection)

**Fallback option:** Active dehumidification remains available for both cameras and compute enclosure if sealed camera options prove unsuitable for specific requirements.

**Next step:** Supplier research for sealed IP67/IP68 USB and WiFi cameras suitable for outdoor river monitoring (quantity: 2 per station).

### Environmental Considerations
- **Temperature variation** - System must handle day/night temperature swings
- **Weather resistance** - Must withstand heavy rainfall and storms
- **Remote deployment** - System must operate without maintenance for extended periods
- **Camera placement** - Sealed camera can be mounted separately from main enclosure

### Operational Requirements
- **Power cycling capability** - Automated system reboot and power management
- **Video capture scheduling** - Regular video recording with specific file naming conventions
- **Data processing** - Local processing of OpenRiverCam algorithms
- **Remote transmission** - Upload processed results to remote servers
- **Autonomous operation** - Minimal human intervention required

## Hardware Design Goals
- Cost-effective solution suitable for multiple deployments
- Locally buildable and maintainable in Indonesia
- Robust operation in challenging environmental conditions
- Integration with existing OpenRiverCam software stack
- Scalable design for network of monitoring stations

## Current Phase
**Multi-Budget Hardware Specification and Parts Sourcing** - Define detailed technical specifications and identify suitable commercial components for three distinct budget tiers, allowing for flexible deployment strategies based on available funding and operational requirements.

## Budget Tier Strategy

### Low Budget Tier (~$200-300 USD)
- **Target Use Case**: Basic monitoring for proof-of-concept or high-volume deployments
- **Focus**: Essential functionality with minimal features
- **Trade-offs**: Reduced redundancy, shorter operational life, manual intervention acceptable

### Mid Budget Tier (~$400-500 USD)
- **Target Use Case**: Standard deployment for reliable long-term monitoring
- **Focus**: Balanced cost-effectiveness with robust operation
- **Trade-offs**: Good reliability with reasonable feature set

### High Budget Tier (~$600-800 USD)
- **Target Use Case**: Critical monitoring locations requiring maximum reliability
- **Focus**: Premium components and redundant systems
- **Trade-offs**: Higher cost for enhanced durability and autonomous operation

## Success Criteria by Budget Tier

### Low Budget Success Criteria
- 3-6 months autonomous operation
- Basic video capture in good weather conditions
- Periodic data transmission capability
- Cost under $300 per unit
- Simple assembly and testing in US

### Mid Budget Success Criteria
- 6-12 months autonomous operation
- Clear video capture in most weather conditions
- Reliable data transmission to remote servers
- Cost under $500 per unit
- Assembly and testing capability in US

### High Budget Success Criteria
- 12+ months autonomous operation
- Clear video capture in all weather conditions
- Continuous reliable data transmission
- Advanced monitoring and self-diagnostics
- Cost under $800 per unit
- Minimal maintenance requirements

## Bill of Materials (BOM) Requirements

Each budget tier must include a complete BOM with the following format:

### BOM Output Format - CSV Files
Save all BOMs as CSV files in the project directory with the following structure:

**File Names:**
- `bom_low_budget.csv` - Low budget tier BOM
- `bom_mid_budget.csv` - Mid budget tier BOM  
- `bom_high_budget.csv` - High budget tier BOM
- `bom_connectivity_wifi.csv` - WiFi connectivity options
- `bom_connectivity_cellular.csv` - Cellular connectivity options
- `bom_connectivity_satellite.csv` - Satellite connectivity options

**CSV Column Headers:**
```
Component_Category,Item_Description,Critical_Specs,Quantity,Unit_Cost_USD,Total_Cost_USD,Supplier,Product_Link,Notes
```

### Required BOM Categories
1. **Computing Platform**
   - Raspberry Pi 5 and accessories
   - Storage (microSD/SSD)
   - Cooling solutions

2. **Camera System**
   - Camera module and housing
   - Lens protection and anti-condensation

3. **Power Management**
   - Solar panels with specifications
   - Battery systems with capacity ratings
   - Charge controllers and power distribution

4. **Connectivity Options** (Separate pricing for each)
   - **WiFi Option**: WiFi modules, range extenders, antennas
   - **Cellular Option**: 4G/5G modems, carrier-compatible antennas
   - **Satellite Option**: Satellite modems, directional antennas, subscription considerations

5. **Environmental Protection**
   - Weatherproof enclosures with IP ratings
   - Humidity control systems
   - Mounting hardware

6. **Grounding & Lightning Protection**
   - Grounding rods and conductors
   - Lightning arrestors and surge protectors
   - Grounding hardware and connections

7. **Security & Anti-Theft**
   - Tamper-evident enclosures
   - Security locks and fasteners
   - Anti-theft mounting systems
   - Intrusion detection sensors

8. **Monitoring & Control**
   - Watchdog systems
   - Status indicators
   - Maintenance access components

### Pre-Integrated Solutions and Open Source Projects
For each budget tier, research and include:

**Pre-Integrated Hardware Solutions:**
- Commercial weather monitoring stations that could be adapted
- Industrial IoT platforms with suitable components
- Educational/maker platforms with relevant features
- Complete kits that meet subset of requirements

**Open Source Project References:**
- Existing open source river monitoring projects
- Environmental sensor networks and platforms
- Solar-powered remote monitoring solutions
- Community-developed weather station designs
- Relevant GitHub repositories and documentation

**Documentation Requirements:**
- Project URLs and active status
- Component compatibility assessment
- Cost comparison with custom build
- Adaptation requirements and effort estimation
- Community support and maintenance status

### BOM Validation Requirements
- All costs based on US suppliers and shipping
- Supplier links must be active and verified
- Critical specs must match operational requirements
- Quantities must account for assembly needs
- Alternative suppliers required for critical components
- Save all data as CSV files in project directory