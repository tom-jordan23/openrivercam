# Power Budget Calculation Template - RC-Box

This document provides a template for calculating power requirements and sizing the battery/solar system.

## Section 1: Component Power Consumption

### 1.1 Raspberry Pi 5 Base Power

| State | Voltage | Current | Power | Notes |
|-------|---------|---------|-------|-------|
| Idle (no peripherals) | 5V | _____ mA | _____ W | Measure with USB power meter |
| Active (CPU load) | 5V | _____ mA | _____ W | During video encoding |
| Standby/Sleep | 5V | _____ mA | _____ W | If sleep mode used |
| Off (RTC only) | 5V | _____ mA | _____ W | PiJuice/PiSugar RTC draw |

**Measurement method:** USB-C power meter inline with power supply

### 1.2 Camera Modules

| State | Quantity | Current Each | Total Current | Power | Notes |
|-------|----------|--------------|---------------|-------|-------|
| Both cameras recording | 2 | _____ mA | _____ mA | _____ W | Full resolution video |
| One camera recording | 1 | _____ mA | _____ mA | _____ W | If different usage |
| Cameras idle/standby | 2 | _____ mA | _____ mA | _____ W | Connected but not recording |
| Cameras unpowered | 2 | 0 mA | 0 mA | 0 W | If power can be cut |

**Spec reference:** Pi Camera Module V3 datasheet

### 1.3 Storage

| Type | Voltage | Current | Power | Notes |
|------|---------|---------|-------|-------|
| microSD card (class 10) | 3.3V | _____ mA | _____ W | During write |
| USB SSD (if used) | 5V | _____ mA | _____ W | Higher power but faster |
| M.2 SSD (if used) | 3.3V | _____ mA | _____ W | Via HAT |

**Decision needed:** microSD vs SSD for storage?

### 1.4 Connectivity

| Component | State | Current | Power | Notes |
|-----------|-------|---------|-------|-------|
| WiFi | Idle connected | _____ mA | _____ W | Background connection |
| WiFi | Active transfer | _____ mA | _____ W | Uploading data |
| WiFi | Hotspot mode | _____ mA | _____ W | For field configuration |
| WiFi | Disabled | 0 mA | 0 W | If not needed |
| Cellular (optional) | Idle | _____ mA | _____ W | If LTE/4G modem added |
| Cellular (optional) | Active | _____ mA | _____ W | During data upload |

**Design decision:** Is cellular needed, or WiFi only?

### 1.5 Power Management & Indicators

| Component | State | Current | Power | Notes |
|-----------|-------|---------|-------|-------|
| PiJuice/PiSugar HAT | Operating | _____ mA | _____ W | Controller overhead |
| RTC (if separate) | Always on | _____ mA | _____ W | Battery backup |
| LED indicators | All on | _____ mA | _____ W | Max LED current |
| LED indicators | Typical | _____ mA | _____ W | Pulsed/dimmed |

### 1.6 Other Peripherals

| Component | Current | Power | Notes |
|-----------|---------|-------|-------|
| USB accessories | _____ mA | _____ W | Any other USB devices |
| Sensors (if added) | _____ mA | _____ W | Temp, humidity, etc. |
| Cooling fan (if needed) | _____ mA | _____ W | For hot climates |

## Section 2: Operational Duty Cycle

### 2.1 Recording Schedule

Define the expected operational pattern:

| Activity | Duration | Frequency | Times per Day |
|----------|----------|-----------|---------------|
| Recording | _____ minutes | Every _____ hours | _____ times |
| Video processing/encoding | _____ minutes | After each recording | _____ times |
| Data upload/sync | _____ minutes | Every _____ hours | _____ times |
| Idle/standby | _____ hours | Between operations | N/A |
| Sleep/off | _____ hours | Nighttime | N/A |

**Example:**
- Recording: 10 minutes, every 6 hours, 4 times/day
- Processing: 5 minutes, after each recording, 4 times/day
- Upload: 10 minutes, every 12 hours, 2 times/day
- Idle: remaining active time
- Sleep: 10pm - 6am (8 hours)

### 2.2 Power State Timeline

Create a 24-hour timeline of power states:

| Time | State | Components Active | Notes |
|------|-------|-------------------|-------|
| 00:00 - 06:00 | Sleep | RTC only | Night time, no recording |
| 06:00 - 06:15 | Recording | RPi + Cameras + Storage | Morning recording |
| 06:15 - 06:20 | Processing | RPi + Storage | Video encoding |
| 06:20 - 12:00 | Idle | RPi + WiFi | Waiting for next cycle |
| 12:00 - 12:15 | Recording | RPi + Cameras + Storage | Midday recording |
| 12:15 - 12:25 | Processing + Upload | RPi + Storage + WiFi | Encode and upload |
| 12:25 - 18:00 | Idle | RPi + WiFi | Waiting |
| ... | ... | ... | Complete for 24 hours |

## Section 3: Power Budget Calculation

### 3.1 Power Consumption by State

Calculate average power for each operational state:

**State: Recording**
- Raspberry Pi 5 active: _____ W
- Camera modules (2x): _____ W
- Storage (writing): _____ W
- WiFi idle: _____ W
- Power management: _____ W
- LEDs: _____ W
- **Total:** _____ W

**State: Processing**
- Raspberry Pi 5 (high CPU): _____ W
- Cameras (idle/off): _____ W
- Storage (writing): _____ W
- WiFi idle: _____ W
- Power management: _____ W
- LEDs: _____ W
- **Total:** _____ W

**State: Upload**
- Raspberry Pi 5: _____ W
- Cameras (off): _____ W
- Storage (reading): _____ W
- WiFi active: _____ W
- Power management: _____ W
- LEDs: _____ W
- **Total:** _____ W

**State: Idle**
- Raspberry Pi 5 (idle): _____ W
- All peripherals (low power): _____ W
- WiFi (background): _____ W
- Power management: _____ W
- LEDs: _____ W
- **Total:** _____ W

**State: Sleep**
- RTC only: _____ W
- All else off: 0 W
- **Total:** _____ W

### 3.2 Daily Energy Consumption

Calculate total energy used in 24 hours:

| State | Power (W) | Duration (hours) | Energy (Wh) |
|-------|-----------|------------------|-------------|
| Recording | _____ W | _____ h | _____ Wh |
| Processing | _____ W | _____ h | _____ Wh |
| Upload | _____ W | _____ h | _____ Wh |
| Idle | _____ W | _____ h | _____ Wh |
| Sleep | _____ W | _____ h | _____ Wh |
| **TOTAL** | - | **24 h** | **_____ Wh/day** |

**Example calculation:**
```
Recording: 12W × (4 × 10min / 60min/h) = 12W × 0.67h = 8.0 Wh
Processing: 15W × (4 × 5min / 60min/h) = 15W × 0.33h = 5.0 Wh
Upload: 10W × (2 × 10min / 60min/h) = 10W × 0.33h = 3.3 Wh
Idle: 5W × 8h = 40.0 Wh
Sleep: 0.1W × 8h = 0.8 Wh
TOTAL = 57.1 Wh/day
```

### 3.3 Seasonal Variation

Adjust for seasonal differences:

| Season | Recording Frequency | Daily Energy | Notes |
|--------|---------------------|--------------|-------|
| Wet/Flood (critical) | _____ recordings/day | _____ Wh/day | More frequent monitoring |
| Dry/Normal | _____ recordings/day | _____ Wh/day | Standard schedule |
| Minimal monitoring | _____ recordings/day | _____ Wh/day | Low activity period |

**Use worst-case (highest consumption) for sizing.**

## Section 4: Battery Sizing

### 4.1 Autonomy Requirement

| Parameter | Value | Notes |
|-----------|-------|-------|
| Daily energy consumption | _____ Wh/day | From Section 3.2 |
| Required autonomy | _____ days | Days without solar input |
| Total energy needed | _____ Wh | Daily × Autonomy |
| Battery efficiency | 90% | Round-trip efficiency |
| Energy from battery | _____ Wh | Total / Efficiency |

### 4.2 Depth of Discharge Limit

| Battery Chemistry | Max DoD | Recommended DoD | Cycle Life |
|-------------------|---------|-----------------|------------|
| LiFePO4 | 80% | 50% | 3000-5000 cycles |
| Li-ion | 90% | 80% | 500-1000 cycles |
| SLA (AGM) | 50% | 30% | 200-300 cycles |

**Selection:** _____ chemistry with _____ % DoD

### 4.3 Battery Capacity Calculation

```
Required battery capacity (Wh) = Energy from battery / DoD

Example:
Daily consumption: 57 Wh/day
Autonomy: 3 days
Total energy: 57 × 3 = 171 Wh
With 90% efficiency: 171 / 0.9 = 190 Wh
With 50% DoD (LiFePO4): 190 / 0.5 = 380 Wh

At 12V: 380 Wh / 12V = 31.7 Ah
At 5V: 380 Wh / 5V = 76 Ah
```

**Your calculation:**
- Required capacity: _____ Wh
- At _____ V: _____ Ah

### 4.4 Temperature Derating

Battery capacity decreases in cold temperatures:

| Temperature | Capacity % | Derating Factor |
|-------------|-----------|-----------------|
| +25°C | 100% | 1.0 |
| +10°C | ~95% | 1.05 |
| 0°C | ~85% | 1.18 |
| -10°C | ~70% | 1.43 |
| -20°C | ~50% | 2.0 |

**Minimum operating temperature:** _____ °C
**Derating factor:** _____ ×
**Adjusted battery capacity:** _____ Ah × _____ = _____ Ah

## Section 5: Solar Panel Sizing

### 5.1 Solar Irradiance Data

Gather data for deployment location:

| Location | Latitude | Worst Month | Solar Irradiance (kWh/m²/day) |
|----------|----------|-------------|--------------------------------|
| Example: Jakarta, Indonesia | 6°S | December (rainy) | 3.5 |
| Example: Oslo, Norway | 60°N | December (winter) | 0.5 |
| Your location: _____ | _____ | _____ | _____ |

**Source:** NASA POWER, PVGIS, local meteorological data

### 5.2 Panel Output Calculation

```
Panel output (Wh/day) = Panel wattage × Solar hours × System efficiency

System efficiency factors:
- Panel orientation (vertical vs optimal tilt): 0.5 - 1.0
- Temperature derating: 0.85 - 0.95
- Dust/soiling: 0.90 - 0.95
- Charge controller efficiency: 0.85 (PWM) or 0.95 (MPPT)
- Battery charge efficiency: 0.90
- Overall: ~0.65 for suboptimal, ~0.75 for good, ~0.85 for optimal

Example:
20W panel, 3.5 sun hours/day, 0.70 efficiency
Output = 20W × 3.5h × 0.70 = 49 Wh/day
```

**Your calculation:**
- Panel wattage: _____ W
- Solar hours: _____ h/day (worst case)
- System efficiency: _____ (estimate)
- Expected output: _____ Wh/day

### 5.3 Panel Sizing with Safety Factor

```
Required panel output = Daily consumption × Safety factor

Safety factor accounts for:
- Cloudy days (still partial charging)
- Panel degradation over time (~0.5%/year)
- Unexpected consumption increases

Typical safety factors:
- 1.5× for good solar locations
- 2.0× for moderate solar
- 2.5 - 3.0× for poor solar or high reliability need
```

**Your sizing:**
- Daily consumption: _____ Wh/day
- Safety factor: _____ ×
- Required output: _____ Wh/day
- Solar hours: _____ h/day
- System efficiency: _____
- **Required panel wattage: _____ W**

```
Panel wattage = Required output / (Solar hours × Efficiency)
```

### 5.4 Panel Selection

| Panel Option | Wattage | Voltage | Dimensions | Weight | Cost | Available? |
|--------------|---------|---------|------------|--------|------|------------|
| Option 1 | _____ W | _____ V | ___ × ___ cm | ___ kg | $ ___ | Y/N |
| Option 2 | _____ W | _____ V | ___ × ___ cm | ___ kg | $ ___ | Y/N |
| Option 3 | _____ W | _____ V | ___ × ___ cm | ___ kg | $ ___ | Y/N |

**Selected panel:** _____ W, _____ V

**Verification:**
- Output in worst case: _____ Wh/day
- Meets/Exceeds daily consumption? YES / NO
- Can recharge battery after autonomy period? YES / NO (calculate days to recharge)

## Section 6: Charge Controller Selection

### 6.1 Controller Requirements

| Parameter | Value | Notes |
|-----------|-------|-------|
| Battery voltage | _____ V | System voltage |
| Battery capacity | _____ Ah | From Section 4 |
| Solar panel voltage (Vmp) | _____ V | Panel specification |
| Solar panel current (Imp) | _____ A | Panel specification |
| Solar panel max power | _____ W | Panel specification |
| Charge current required | _____ A | C/10 to C/5 typical |

### 6.2 Controller Options

| Controller | Type | Max Solar (W) | Max Battery (Ah) | Features | Cost |
|------------|------|---------------|------------------|----------|------|
| PiJuice | PWM | 10W | 12Ah (3.7V) | RTC, RPi integration | $75 |
| PiSugar 3 | PWM | 10W | 5Ah (5V internal) | RTC, RPi integration | $50 |
| Generic MPPT | MPPT | 50-400W | Unlimited | No RTC, external | $30-150 |

**Selection:** _____ based on power requirements and integration needs

## Section 7: Energy Balance Verification

### 7.1 Daily Energy Balance

| Parameter | Value | Units |
|-----------|-------|-------|
| Daily consumption | _____ | Wh/day |
| Daily solar generation (worst case) | _____ | Wh/day |
| Net energy balance | _____ | Wh/day |
| Battery capacity | _____ | Wh |

**Check:**
- [ ] Solar generation ≥ Daily consumption (sustainable)
- [ ] If negative balance, how many days until battery depleted?
- [ ] Can battery recharge after autonomy period?

### 7.2 Recharge Time After Autonomy

```
After X days of no sun, battery is depleted by:
Energy deficit = Daily consumption × Autonomy days

When sun returns, excess energy per day:
Excess = Solar generation - Daily consumption

Days to recharge = Energy deficit / Excess

Example:
Daily consumption: 57 Wh/day
Autonomy: 3 days
Deficit: 57 × 3 = 171 Wh
Solar generation (normal conditions): 100 Wh/day
Excess: 100 - 57 = 43 Wh/day
Recharge time: 171 / 43 = 4.0 days
```

**Your calculation:**
- Energy deficit: _____ Wh
- Excess generation (normal sun): _____ Wh/day
- Recharge time: _____ days

**Check:** Is recharge time acceptable?

## Section 8: Summary & Recommendations

### 8.1 System Specifications

| Component | Specification | Rationale |
|-----------|---------------|-----------|
| Battery | _____ V, _____ Ah, _____ Wh | Based on _____ days autonomy |
| Solar Panel | _____ W, _____ V | Sized for worst-case solar conditions |
| Charge Controller | _____ (model/type) | Selected based on _____ |
| Total System Cost | $ _____ | Battery + Panel + Controller |

### 8.2 Performance Predictions

| Scenario | Solar Conditions | Expected Performance |
|----------|------------------|----------------------|
| Best case | Full sun, optimal season | Battery at 100%, excess energy |
| Normal case | Average conditions | Battery 80-100%, balanced |
| Worst case | Prolonged clouds/rain | Battery survives _____ days |

### 8.3 Risks & Mitigations

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Prolonged cloudy weather | Medium | High | Oversized battery/panel |
| Battery degradation over time | High | Medium | Plan replacement every ___ years |
| Higher than expected consumption | Medium | High | Monitor and optimize software |
| Panel damage/theft | Low | High | Secure mounting, spare panel |

### 8.4 Next Steps

- [ ] Procure components for prototype
- [ ] Build test setup
- [ ] Measure actual power consumption (validate Section 1)
- [ ] Run 30-day bench test
- [ ] Deploy field trial unit
- [ ] Monitor and iterate on design

---

**Document Version:** 1.0
**Date:** 2025-11-28
**Completed By:** _____
**Reviewed By:** _____
**Related Documents:**
- POWER_SYSTEM_DESIGN_QUESTIONS.md
- POWER_CONTROLLER_COMPARISON.md
