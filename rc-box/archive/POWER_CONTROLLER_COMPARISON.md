# Power Management Controller Comparison - RC-Box

This document provides a framework for evaluating power management solutions for the RC-Box project.

## Comparison Matrix

| Feature | PiJuice | PiSugar 3 | PiSugar S | Custom MPPT Solution |
|---------|---------|-----------|-----------|----------------------|
| **Hardware Specifications** |
| Compatible RPi Models | 3/4/5 (check) | 4/5 | Zero/3/4 | Universal |
| Max Battery Capacity | 12,000mAh (check) | 5,000mAh | 1,200mAh | Unlimited |
| Battery Voltage | 3.7V LiPo | 5V (internal boost) | 5V (internal boost) | 12V/24V typical |
| Solar Input Voltage | 4.8-10V | 5V (micro-USB) | 5V (USB-C) | 12-100V+ |
| Max Solar Input Power | ~10W | ~10W | ~5W | 50-400W+ |
| Charge Current | 925/550mA (adjustable) | 2.5A max | 1A max | 10-40A typical |
| Output to RPi | 5V via GPIO | 5V via GPIO/USB-C | 5V via GPIO | 5V via DC-DC |
| **Features** |
| MPPT Charging | No (PWM) | No | No | Yes |
| RTC (Real-Time Clock) | Yes | Yes | Yes | External module needed |
| Programmable Wake/Sleep | Yes (software) | Yes (software) | Yes (software) | External MCU needed |
| UPS Function | Yes | Yes | Yes | With appropriate setup |
| I2C Monitoring | Yes | Yes | Yes | Depends on controller |
| Battery Protection | Yes | Yes | Yes | Yes (built-in) |
| Buttons/Switches | 3x programmable | 1x button | 1x button | External required |
| LED Indicators | RGB LED | LED | LED | External required |
| **Software & Integration** |
| Python API | Yes (mature) | Yes | Yes | Varies by controller |
| Linux Support | Excellent | Good | Good | N/A (separate from RPi) |
| Community Support | Strong | Growing | Moderate | Strong (MPPT general) |
| Documentation | Comprehensive | Good | Good | Varies |
| **Field Service Considerations** |
| Form Factor | HAT (mounts on GPIO) | HAT | HAT | Separate module |
| Installation Complexity | Simple (stack on RPi) | Simple | Simple | Moderate (wiring) |
| Field Replacement | Easy (unplug/plug) | Easy | Easy | Moderate (terminals) |
| Tools Required | None (maybe standoffs) | None | None | Screwdriver |
| Local Availability | Low | Low | Low | High (commercial product) |
| **Cost (Approximate)** |
| Controller Unit | $75-90 USD | $40-60 USD | $25-35 USD | $30-200 USD |
| Battery (if separate) | $20-40 | Included | Included | $50-150 |
| Solar Panel | $15-30 (10W) | $15-30 (10W) | $10-20 (5W) | $50-200 (50-100W) |
| Total System Cost | $110-160 | $95-120 | $60-85 | $130-550 |
| **Pros** |
| | Proven platform | Integrated battery | Compact | Scalable power |
| | Good software | Clean design | Low cost | Industry standard |
| | Extensive docs | USB-C input | | Handles large loads |
| | | | | Field serviceable |
| **Cons** |
| | Limited solar input | Limited battery size | Very limited power | More complex |
| | Cost | Limited solar input | Minimal expansion | Requires RTC module |
| | Availability | Availability | | More wiring |
| | | | | Higher initial cost |

## Evaluation Criteria

### 1. Power Scaling Requirements

**Question:** What is the expected power consumption range?

- **Low Power (<5W average):** PiSugar S or PiSugar 3 sufficient
- **Medium Power (5-15W average):** PiJuice or small custom MPPT
- **High Power (>15W average):** Custom MPPT solution required

**Recommendation pending:** Need to calculate actual power budget (see POWER_SYSTEM_DESIGN_QUESTIONS.md)

### 2. Deployment Duration Between Maintenance

**Question:** How many days without sun must the system survive?

- **1-2 days:** PiSugar 3 (5,000mAh) may suffice
- **3-5 days:** PiJuice (12,000mAh) or larger custom battery
- **7+ days:** Custom solution with large battery bank required

**Calculation Example:**
```
If daily consumption = 50Wh (10W avg over 5 hours active)
For 3 days autonomy = 150Wh
Battery at 12V = 150Wh / 12V = 12.5Ah (with 0% DoD)
With 50% DoD limit = 25Ah battery needed
With 80% DoD limit = 15.6Ah battery needed

PiJuice max battery: 12Ah at 3.7V = 44.4Wh (< 1 day!)
Custom 12V 20Ah battery = 240Wh (4.8 days at 50Wh/day)
```

### 3. Solar Panel Size & Mounting

**Question:** Can solar panel be large (>20W) or must be compact?

- **Compact required (<10W):** PiJuice or PiSugar work well
- **Medium (10-50W):** Custom MPPT more efficient
- **Large (>50W):** Custom MPPT required

**MPPT vs PWM Efficiency:**
- MPPT: 94-98% efficient, especially with voltage mismatch
- PWM: 70-80% efficient if panel voltage >> battery voltage
- For small panels, difference is minor
- For large panels, MPPT adds significant energy capture

### 4. Environmental Extremes

**Question:** Temperature range at deployment sites?

- **Mild (0-40C):** Any solution works
- **Cold (<0C):** Need temperature-compensated charging
  - PiJuice: supports temp sensor input (verify implementation)
  - PiSugar: check specifications
  - Custom MPPT: most support temp compensation
- **Hot (>45C):** Check component ratings
  - LiPo batteries: generally max 60C
  - Electronics: 70-85C typical

### 5. Field Serviceability Priority

**Question:** How critical is ease of field replacement?

**PiJuice/PiSugar Pros:**
- Plug-and-play, no wiring
- Single unit replacement
- Less to go wrong mechanically

**PiJuice/PiSugar Cons:**
- Proprietary form factor
- Limited local availability
- If unit fails, entire controller is replaced

**Custom MPPT Pros:**
- Industry-standard components
- Widely available (marine, RV, solar suppliers)
- Modular: replace only failed component
- Local procurement in many countries

**Custom MPPT Cons:**
- Screw terminals (must get polarity right)
- More components = more potential failure points
- Requires basic electrical knowledge

### 6. Cost at Scale

**Question:** How many units will be deployed?

- **1-10 units:** Cost difference is minor, prioritize reliability/ease
- **10-100 units:** Cost becomes factor, but still secondary to function
- **100+ units:** Cost optimization important, custom MPPT may save money at this scale

**Lifecycle Cost Considerations:**
- Battery replacement frequency (PiJuice/PiSugar: integrated battery simpler but whole unit cost)
- Shipping cost for replacements (smaller is cheaper)
- Training cost (simpler reduces training needs)

## Hybrid Approach: Custom Power Board

### Concept
Design a custom PCB that:
- Mounts as HAT on Raspberry Pi 5 GPIO
- Uses commercial MPPT charge controller IC (e.g., CN3722, BQ24650)
- Includes RTC (DS3231 or PCF8523)
- Adds hardware switches (power, maintenance mode, WiFi)
- Includes LED indicators
- Has screw terminals for external battery and solar panel

### Advantages
- Optimized for RC-Box requirements
- Scalable power (supports larger batteries/panels)
- Integrates all features in one board
- Can be manufactured in quantity

### Disadvantages
- Requires PCB design effort
- Initial prototyping cost
- Need to certify design
- No existing community support
- Higher risk (untested platform)

### Decision Point
Only pursue if:
1. PiJuice/PiSugar are clearly insufficient for power requirements, AND
2. Deployment volume justifies NRE (non-recurring engineering) cost, AND
3. Timeline allows for design/test/iterate cycles (6+ months)

Otherwise, use commercial solution (PiJuice, PiSugar, or MPPT controller).

## Recommended Approach

### Phase 1: Power Budget Analysis (IMMEDIATE)
1. Measure actual Raspberry Pi 5 power consumption with:
   - 2x Camera Module V3 active
   - WiFi active
   - Video encoding
   - Storage write
2. Define operational duty cycle (based on humanitarian monitoring needs)
3. Calculate daily energy consumption (Wh/day)
4. Define autonomy requirement (days without sun)
5. Calculate required battery capacity

### Phase 2: Controller Selection (AFTER PHASE 1)
Based on Phase 1 results:

**If daily consumption < 40Wh:**
- Consider PiSugar 3 (5,000mAh = ~25Wh with inefficiencies)
- Or PiJuice with larger external battery

**If daily consumption 40-100Wh:**
- PiJuice with max battery (44Wh)
- Or custom MPPT with ~100Wh battery

**If daily consumption > 100Wh:**
- Custom MPPT solution required
- Large battery bank (200-400Wh)
- Larger solar panel (50-100W)

### Phase 3: Prototype Testing
1. Build test unit with selected controller
2. Run 30-day test with realistic duty cycle
3. Monitor battery voltage daily
4. Test in simulated low-sun conditions (cover panel)
5. Verify autonomy meets requirements

### Phase 4: Field Trial
1. Deploy prototype in actual location
2. Monitor remotely (if connectivity available)
3. Measure:
   - Days of successful operation
   - Battery min/max voltage
   - Any shutdowns or issues
4. Iterate on design if needed

## Additional Resources Needed

To complete this comparison, gather:

1. **Datasheets:**
   - PiJuice HAT datasheet
   - PiSugar 3 / PiSugar S specifications
   - Raspberry Pi 5 power requirements
   - Pi Camera Module V3 power specs

2. **Software Documentation:**
   - PiJuice Python API examples
   - PiSugar GitHub repository and examples
   - Scheduling/sleep mode implementation guides

3. **Real-World Data:**
   - Deployment site solar irradiance data
   - Temperature profiles for target regions
   - Availability of components in target countries

4. **Regulatory Information:**
   - Battery shipping restrictions (UN38.3)
   - Solar panel import duties
   - Electronic device certifications required

## Next Steps

1. Answer questions in POWER_SYSTEM_DESIGN_QUESTIONS.md
2. Perform power consumption measurements (Phase 1)
3. Create detailed power budget spreadsheet
4. Select controller based on data
5. Procure components for prototype
6. Begin testing

---

**Document Version:** 1.0
**Date:** 2025-11-28
**Related Documents:**
- POWER_SYSTEM_DESIGN_QUESTIONS.md
- CLAUDE.md (project requirements)
