# 8.2 Power Equipment Installation - Utility/Hybrid

## Overview

Grid-powered and hybrid systems provide reliable power for OpenRiverCam installations where utility electricity is available. Hybrid systems combine grid power with battery backup and optional solar, ensuring continuous operation during power outages. This section covers installation procedures for grid connection, voltage regulation, backup power integration, and safety systems.

**Time Required:** 3-5 hours for complete installation

**Prerequisites:**
- Site survey and power assessment completed (Chapter 7)
- Utility power availability confirmed
- Required permits obtained
- All equipment delivered and inspected
- Qualified electrician available if required by local regulations

## Safety Considerations

**CRITICAL SAFETY WARNINGS:**

- **Electrical Shock Hazard:** Grid voltage can cause serious injury or death. Always assume wires are energized unless verified with proper testing equipment.
- **Arc Flash Hazard:** Use appropriate PPE when working with energized circuits. Turn off power at source whenever possible.
- **Licensed Electrician Required:** Many jurisdictions require licensed electricians for grid connection work. Verify local requirements before beginning work.
- **Permit Requirements:** Grid connections typically require electrical permits and utility approval. Never connect to grid without proper authorization.
- **Grounding Essential:** Proper grounding is critical for safety. All metal components must be grounded.

**Personal Protective Equipment (PPE) Required:**
- Insulated gloves rated for working voltage
- Safety glasses with side shields
- Rubber-soled shoes (non-conductive)
- Flame-resistant clothing (for work on energized circuits)
- Insulated tools rated for voltage

## Regulatory Requirements

### Electrical Permits

**Before Beginning Work:**
1. Contact local electrical authority to determine permit requirements
2. Submit electrical plans and equipment specifications if required
3. Obtain all necessary permits
4. Schedule inspections as required
5. Verify insurance requirements for electrical work

**Common Requirements:**
- Licensed electrician for certain work
- Electrical drawings and load calculations
- Equipment listings and certifications (UL, CE, etc.)
- Inspection before energization
- Final inspection after completion

### Utility Coordination

**For Grid Connection:**
1. **Contact Utility Company:**
   - Notify utility of installation plans
   - Verify service capacity available
   - Request meter installation or modification if needed
   - Confirm connection requirements

2. **Service Agreement:**
   - Review utility rate structure
   - Understand billing for monitoring station loads
   - Clarify responsibilities for maintenance
   - Obtain written approval for connection

3. **Technical Requirements:**
   - Verify voltage and phase requirements
   - Confirm grounding requirements
   - Understand disconnection procedures
   - Review overcurrent protection requirements

## Equipment and Tools Checklist

**Utility Power System Components:**
- Power supply unit (AC to DC converter)
- Voltage regulator or UPS (if required)
- Backup battery (for hybrid systems)
- Automatic transfer switch or changeover relay
- Distribution panel or circuit breaker box
- Circuit breakers (appropriate amperage)
- Weatherproof enclosure (NEMA 4 or IP65 minimum)
- Grounding rod and wire
- Conduit and fittings (if required by code)
- Junction boxes
- Cable glands and strain relief
- Surge protector (whole-system protection)
- AC and DC cables (appropriate gauge)

**For Hybrid Systems (Add):**
- Solar charge controller (if adding solar)
- Battery charge controller or charger
- Battery bank with appropriate capacity
- Battery disconnect switch
- Additional fuses and overcurrent protection

**Tools Required:**
- Multimeter (AC and DC voltage, current)
- Non-contact voltage tester
- Wire strippers and crimpers
- Screwdrivers (insulated)
- Wrenches and socket set
- Drill with appropriate bits
- Cable pulling tools
- Conduit bending tools (if using conduit)
- Cable ties and management supplies
- Silicone sealant
- Thread-locking compound
- Labeling materials

## Step 1: Grid Power Connection

### 1.1 Verify Power Availability

**SAFETY:** Use non-contact voltage tester before touching any wires.

**Procedure:**

1. **Locate Power Source:**
   - Identify connection point (outlet, junction box, or distribution panel)
   - Verify voltage with multimeter (should match system requirements)
   - Measure voltage during different times of day
   - Record minimum and maximum voltages observed

2. **Verify Power Quality:**
   - Check voltage stability (should not vary more than ±10%)
   - Verify frequency matches equipment specifications (50 Hz or 60 Hz)
   - Observe for voltage fluctuations or interruptions
   - Consider power quality monitor for problematic supplies

3. **Assess Circuit Capacity:**
   - Identify circuit breaker size
   - Calculate existing load on circuit
   - Verify adequate capacity for camera system
   - Consider dedicated circuit if shared circuit is heavily loaded

**Example Calculation:**
- 20A circuit breaker at 230V = 4,600W maximum capacity
- Existing load: 500W
- Camera system load: 30W
- Available capacity: 4,600 - 500 - 30 = 4,070W (adequate)

### 1.2 Install Electrical Enclosure

**Location Requirements:**
- Protected from weather (if outdoors)
- Accessible for maintenance
- Close to power source (minimize cable runs)
- Secure from tampering
- Adequate ventilation for heat dissipation
- Above flood risk elevation

**Procedure:**

1. **Select Enclosure Location:**
   - Mark mounting position
   - Verify level mounting surface
   - Check clearance for door opening
   - Ensure adequate working space (minimum 1 meter in front)

2. **Install Enclosure:**
   - Drill mounting holes using appropriate bit
   - Install mounting anchors or bolts
   - Attach enclosure securely
   - Use level to verify enclosure is plumb
   - Seal mounting holes with silicone

3. **Prepare Cable Entry Points:**
   - Mark locations for conduit or cable glands
   - Drill holes appropriate size for fittings
   - Install conduit fittings or cable glands
   - Ensure all entry points will be weatherproof

**Quality Check:**
- Enclosure is securely mounted
- Level and plumb
- Door operates properly
- Cable entry points sealed
- Adequate space inside for components

### 1.3 Install Circuit Protection

**Main Circuit Breaker:**

1. **Select Breaker Rating:**
   - Calculate maximum expected load
   - Add 25% safety margin
   - Round up to next standard breaker size
   - Verify breaker does not exceed supply circuit rating

**Example:**
- Camera system load: 30W at 12V DC = 2.5A DC
- AC side with 90% efficient power supply: 30W ÷ 0.9 = 33W
- Current at 230V AC: 33W ÷ 230V = 0.14A
- Minimum breaker: 0.14A × 1.25 = 0.18A
- Use: 1A or 2A circuit breaker (appropriate for small load)

2. **Install Circuit Breaker:**
   - Mount breaker in enclosure or use external disconnect
   - Connect supply side from grid source
   - Connect load side to power supply input
   - Verify breaker operates smoothly (test open/close)
   - Leave breaker in OFF position until installation complete

**Quality Check:**
- Breaker rating is appropriate
- Connections are tight
- Breaker operates correctly
- Proper wire routing (no strain on terminals)

## Step 2: Voltage Regulation

### 2.1 Install AC to DC Power Supply

**Power Supply Selection Verification:**
- Input voltage range covers grid voltage variations
- Output voltage matches camera system requirements (typically 12V or 24V DC)
- Current rating exceeds maximum system load plus 25% margin
- Efficiency rating >85% preferred
- Overcurrent and short-circuit protection built in

**Procedure:**

1. **Mount Power Supply:**
   - Select mounting location inside enclosure
   - Ensure adequate clearance for ventilation (check specifications)
   - Mark mounting holes
   - Install mounting hardware
   - Secure power supply firmly

2. **Connect AC Input:**
   - **POWER OFF:** Verify power is disconnected at breaker
   - Connect AC neutral wire to power supply neutral terminal
   - Connect AC line (hot) wire through circuit breaker to power supply
   - Connect ground wire to power supply ground terminal
   - Verify all connections are tight
   - Double-check polarity (use wiring diagram)

3. **Connect DC Output:**
   - Identify positive and negative DC terminals
   - Route DC cables to load or battery (for hybrid systems)
   - Install appropriate fuses in positive DC line
   - Connect negative DC line
   - Connect positive DC line through fuse
   - Verify polarity before energizing

**Quality Check:**
- AC wiring matches power supply specifications
- All connections are tight
- Polarity is correct
- Fuses are properly rated
- No loose wire strands

### 2.2 Install Voltage Regulator or UPS (If Required)

**When to Use:**
- Grid voltage varies more than ±10%
- Frequent voltage spikes or sags
- Sensitive equipment requiring clean power
- Short-term backup required during brief outages

**UPS Installation:**

1. **Select UPS Type:**
   - **Line-Interactive:** Good for voltage regulation, moderate backup time
   - **Online (Double-Conversion):** Best power quality, continuous operation
   - Size for load plus 25% margin

2. **Install UPS:**
   - Mount in enclosure or place in protected location
   - Connect grid power to UPS input
   - Connect power supply to UPS output
   - Connect battery if external battery UPS
   - Configure UPS settings per manufacturer instructions

3. **Configure UPS:**
   - Set input voltage range
   - Set output voltage
   - Configure battery backup time
   - Enable any alarm or notification features
   - Test UPS operation

**Voltage Regulator Installation:**

1. **Install Regulator:**
   - Mount voltage regulator between grid supply and power supply
   - Connect input from grid (through breaker)
   - Connect output to power supply input
   - Ground regulator chassis

2. **Set Output Voltage:**
   - Adjust regulator to provide stable output voltage
   - Typical setting: Nominal grid voltage (e.g., 230V)
   - Test regulation under load
   - Verify output remains stable with input variations

**Quality Check:**
- Output voltage is stable and correct
- UPS or regulator operates during input variations
- Battery backup functions (if applicable)
- Alarm systems functional

## Step 3: Backup Power Integration (Hybrid Systems)

### 3.1 Install Backup Battery

**Battery Selection Considerations:**
- Capacity for required backup time (calculate from load and desired runtime)
- Deep-cycle or UPS-rated battery
- Maintenance-free sealed type preferred
- Temperature tolerance for installation environment

**Procedure:**

1. **Prepare Battery Location:**
   - Install battery shelf or platform in enclosure
   - Ensure adequate ventilation
   - Allow clearance around battery
   - Install battery tie-down brackets

2. **Install Battery:**
   - Position battery on platform
   - Connect battery to charger/charge controller
   - Install fuses in battery positive cable
   - Secure battery with tie-down straps
   - Label battery with voltage and capacity

**Quality Check:**
- Battery is secure and cannot move
- Adequate ventilation
- Fuses properly rated
- Connections tight and correct polarity

### 3.2 Install Automatic Transfer Switch

**Purpose:** Automatically switches between grid power and battery backup during outages.

**Types:**
- **Relay-Based Transfer Switch:** Simple, reliable, fast switching
- **Integrated in UPS:** Automatic in most UPS systems
- **Charge Controller with Load Control:** For solar/battery hybrid systems

**Installation Procedure:**

1. **Mount Transfer Switch:**
   - Install in enclosure
   - Position for easy wiring access
   - Ensure heat dissipation

2. **Connect Power Sources:**
   - **Input 1 (Primary):** Grid power supply output
   - **Input 2 (Backup):** Battery or solar charge controller output
   - **Output:** Camera system load

3. **Connect Control Signals:**
   - Some switches require voltage sensing connections
   - Connect voltage sense wires to monitor grid power
   - Configure switching voltage thresholds
   - Set transfer delay times if applicable

4. **Configure Switching Logic:**
   - **Grid Available:** Use grid power, charge battery
   - **Grid Failed:** Switch to battery within 50ms or less
   - **Grid Restored:** Return to grid, resume battery charging

**Quality Check:**
- All power connections correct and tight
- Control wiring properly connected
- Switching operates as designed
- No delay in power to load during transfer

### 3.3 Integrate Solar Charging (Optional)

**For systems with both grid and solar:**

1. **Install Solar Charge Controller:**
   - Mount controller in enclosure
   - Connect solar panel to controller solar input
   - Connect battery to controller battery terminals
   - Connect grounding

2. **Configure Charge Priority:**
   - **Option 1:** Solar charges battery, grid powers load directly
   - **Option 2:** Solar and grid both charge battery, load runs from battery
   - **Option 3:** Grid charges when solar insufficient

3. **Install Charge Source Selection:**
   - Use diodes or relay to prevent backfeed
   - Ensure grid charger and solar controller do not conflict
   - Set charge voltages to match battery specifications
   - Configure so both sources can charge simultaneously if designed for this

**Quality Check:**
- No conflicts between charging sources
- Battery charging properly from both sources
- No backfeed between sources
- All voltage settings correct

## Step 4: Electrical Safety Systems

### 4.1 Install Grounding System

**Grounding Requirements:**
- All metal enclosures grounded
- Power supply grounded
- Equipment frames grounded
- Single-point ground to earth

**Procedure:**

1. **Install Ground Rod:**
   - Drive ground rod (minimum 1.5m, copper or copper-clad)
   - Install within 3 meters of installation
   - Use ground rod clamp
   - Verify good connection

2. **Run Grounding Conductors:**
   - Use appropriate gauge copper wire (minimum 6 AWG / 16 mm²)
   - Green or green/yellow insulation
   - Connect from ground rod to:
     - Electrical enclosure
     - Power supply chassis
     - Transfer switch (if metal)
     - Any other metal equipment

3. **Bond All Components:**
   - Ensure all metal parts are electrically connected
   - Use star washers under connections
   - Apply anti-corrosion compound
   - Verify continuity with multimeter

**Quality Check:**
- Ground rod firmly installed
- All connections tight
- Continuity verified between all grounded components
- Resistance to earth <25 ohms (measure with ground resistance tester if available)

### 4.2 Install Surge Protection

**Surge Protection Required:**
- Grid supply is susceptible to lightning and switching surges
- Protects expensive camera and communication equipment
- Two stages recommended: service entrance and equipment

**Installation:**

1. **Service Entrance Surge Protector:**
   - Install at main connection point (grid supply entry)
   - Connect between line and neutral
   - Connect ground to grounding system
   - Use Type 1 or Type 2 SPD (Surge Protective Device)

2. **Equipment-Level Surge Protection:**
   - Install surge protector for DC power to camera
   - Install network surge protection for Ethernet (if applicable)
   - Ground all surge protectors properly

**Quality Check:**
- Surge protectors rated for voltage and current
- Properly grounded
- Indicator lights show operational status
- Installed per manufacturer instructions

### 4.3 Install Safety Labels and Warnings

**Required Labels:**
- "CAUTION: GRID VOLTAGE" on AC sections
- "BATTERY: ELECTRIC SHOCK HAZARD" on battery compartment
- Voltage ratings on all sections
- Emergency shutdown instructions
- Contact information for maintenance

## Step 5: Testing and Commissioning

### 5.1 Pre-Commissioning Checks

**Visual Inspection Checklist:**
- [ ] All connections tight and secure
- [ ] Correct polarity on all DC connections
- [ ] No exposed conductors
- [ ] All cable glands sealed
- [ ] Grounding connections complete
- [ ] Fuses and breakers properly rated
- [ ] Labels installed
- [ ] Enclosure clean and free of tools or materials
- [ ] Adequate clearance around ventilation openings

### 5.2 Initial Power-Up Test

**SAFETY:** Verify all personnel clear before energizing.

**Procedure:**

1. **Energize Grid Supply:**
   - Turn on circuit breaker at source
   - Verify voltage at enclosure input
   - Measure: ______V AC (expected: grid voltage ±10%)

2. **Activate System Circuit Breaker:**
   - Turn on main system circuit breaker
   - Verify power supply input LED illuminates
   - Check for any unusual sounds or smells

3. **Verify DC Output:**
   - Measure DC output voltage: ______V (expected: 12V or 24V ±5%)
   - Verify voltage is stable
   - Check power supply temperature (should be warm, not hot)

4. **Connect Load:**
   - Connect camera system load
   - Verify equipment powers on
   - Measure load current: ______A
   - Compare to expected current

### 5.3 Backup System Testing (Hybrid Systems)

**Battery Charge Test:**
1. Monitor battery voltage over 24 hours
2. Verify battery reaches full charge
3. Record charging current and time to full charge
4. Expected full charge voltage: 13.6-14.4V for 12V lead-acid

**Transfer Switch Test:**
1. **Simulate Grid Failure:**
   - Turn off grid circuit breaker
   - Verify immediate transfer to battery
   - Confirm load continues operating
   - Verify transfer occurs within specified time

2. **Measure Backup Runtime:**
   - Record battery voltage at start: ______V
   - Allow system to run on battery
   - Record voltage every 30 minutes
   - Calculate actual runtime to low voltage cutoff
   - Compare to designed backup time

3. **Grid Restoration Test:**
   - Turn grid power back on
   - Verify automatic transfer back to grid
   - Confirm battery begins charging
   - Check load remains powered during transfer

**Quality Check:**
- Transfer occurs automatically
- No interruption to load
- Battery charges properly after use
- All indicators functioning correctly

### 5.4 Voltage Regulation Testing

**Test Grid Voltage Variations:**
1. Measure output voltage with various input voltages (if possible to vary)
2. Verify output remains stable
3. Test with load variations
4. Confirm regulation within ±5% under all conditions

**UPS Testing (if applicable):**
- Verify UPS input and output voltages
- Test battery backup activation
- Check UPS alarms and indicators
- Verify runtime matches specifications

## Step 6: Documentation and Compliance

### 6.1 Installation Documentation

**Record the Following:**
- Installation date and installer
- Equipment specifications (make, model, serial numbers)
- Circuit breaker sizes and locations
- Wire gauges and routing
- Grounding resistance measurement
- Test results and measured values
- Configuration settings
- Inspection results and approvals

### 6.2 Compliance Documentation

**Retain Copies of:**
- Electrical permits
- Utility approval letters
- Inspection reports
- Equipment certifications and listings
- As-built electrical drawings
- Operating manuals for all equipment

### 6.3 Operating Instructions

**Create Site-Specific Procedures For:**
- Normal operation
- Emergency shutdown
- Grid power failure response
- Battery replacement procedure
- Maintenance schedule
- Troubleshooting common issues
- Emergency contact information

## Troubleshooting Guide

### Problem: No Power from Grid

**Solutions:**
1. Check main circuit breaker at source
2. Verify utility power with voltage tester
3. Check system circuit breaker
4. Inspect for tripped GFI or RCD
5. Verify correct voltage at enclosure input

### Problem: Power Supply Not Producing DC Output

**Solutions:**
1. Check AC input voltage to power supply
2. Verify power supply is turned on (if switch present)
3. Check output fuse
4. Inspect for overload condition
5. Verify output is not short-circuited
6. Replace power supply if defective

### Problem: Voltage Fluctuation or Instability

**Solutions:**
1. Measure grid voltage over time
2. Install voltage regulator if grid unstable
3. Check for loose connections
4. Verify power supply capacity adequate for load
5. Consider UPS for sensitive equipment

### Problem: Transfer Switch Not Switching

**Solutions:**
1. Verify battery is charged and voltage adequate
2. Check transfer switch control voltage sensing
3. Test manual operation of switch
4. Verify switching thresholds correctly set
5. Check for control wiring issues

### Problem: Battery Not Charging

**Solutions:**
1. Verify charger or charge controller operating
2. Check battery fuse
3. Inspect battery connections
4. Test battery condition (may be failed)
5. Verify charging voltage setpoints

## Maintenance Schedule

**Weekly (First Month):**
- Check voltage readings
- Verify backup systems functional
- Inspect for any issues

**Monthly:**
- Test backup system transfer
- Check battery voltage and charge
- Tighten all electrical connections
- Inspect for corrosion

**Quarterly:**
- Complete system inspection
- Test UPS or battery backup runtime
- Verify surge protector status
- Check grounding connections

**Annually:**
- Professional electrical inspection recommended
- Test ground resistance
- Review permits and compliance
- Update documentation
- Consider battery replacement (typically 3-5 year lifespan)

## Summary

Utility and hybrid power installations provide reliable, low-maintenance power for OpenRiverCam systems. Key success factors include:

1. **Regulatory Compliance:** Obtain all required permits and approvals
2. **Electrical Safety:** Follow all safety codes and use appropriate PPE
3. **Proper Grounding:** Essential for safety and equipment protection
4. **Surge Protection:** Protects investment in equipment
5. **Backup Systems:** Ensure continuous operation during outages
6. **Documentation:** Complete records for maintenance and compliance

**Next Step:** Proceed to camera installation (Section 8.3) once power system is verified operational and stable.