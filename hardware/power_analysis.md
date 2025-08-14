# OpenRiverCam Power Consumption Analysis and Solar Sizing Validation

## Power Consumption Components Analysis

### Computing Platform Power Consumption

**Raspberry Pi 5 4GB (Low Budget Tier):**
- Idle: 2.7W
- Under load with camera recording: 4.4W (2.7W + 1.7W camera)
- Average operation (40% load): 3.2W

**Raspberry Pi 5 8GB (Mid/High Budget Tiers):**
- Idle: 2.7W
- Under load with camera recording: 4.4W (2.7W + 1.7W camera)
- With active cooling fan: +3W
- Average operation (50% load): 3.8W (mid tier), 4.2W (high tier with fan)

### Additional System Components Power Draw

**Low Budget Tier Additional Components:**
- Basic LED indicator: 0.02W
- DC-DC converter efficiency loss: 15% = 0.5W
- Total system power: 3.2W + 0.5W + 0.02W = 3.72W

**Mid Budget Tier Additional Components:**
- Status LED array: 0.1W
- Watchdog timer: 0.5W
- Cooling fan (intermittent 30%): 1W
- DC-DC converter efficiency loss: 10% = 0.4W
- Total system power: 3.8W + 0.4W + 0.1W + 0.5W + 1W = 5.8W

**High Budget Tier Additional Components:**
- Advanced status display: 0.8W
- Environmental sensors: 0.3W
- UPS HAT: 0.2W
- Cooling/heating system: 5W
- Dehumidification: 3W
- DC-DC converter efficiency loss: 8% = 0.4W
- Total system power: 4.2W + 0.4W + 0.8W + 0.3W + 0.2W + 5W + 3W = 14W

## Solar Panel and Battery Sizing Validation

### Indonesian Tropical Solar Conditions
- Latitude: ~6°S (near equator)
- Peak sun hours: 4.5-5.5 hours per day (tropical climate with cloud cover)
- Design assumption: 4.5 peak sun hours (conservative for reliability)

### Low Budget Tier Power System Validation

**Daily Energy Requirement:**
- Average power: 3.72W
- Daily energy: 3.72W × 24h = 89.3Wh

**Solar Panel (10W):**
- Daily generation: 10W × 4.5h = 45Wh
- Charge controller efficiency (PWM): 85%
- Actual daily generation: 45Wh × 0.85 = 38.25Wh

**Battery (12V 4.5Ah = 54Wh):**
- Usable capacity (50% DOD for SLA): 27Wh
- Backup days without sun: 27Wh ÷ 89.3Wh = 0.3 days

**Analysis:** UNDERSIZED - Solar panel only provides 43% of daily needs. 
**Recommendation:** Increase to 20W solar panel for 76.5Wh daily generation.

### Mid Budget Tier Power System Validation

**Daily Energy Requirement:**
- Average power: 5.8W
- Daily energy: 5.8W × 24h = 139.2Wh

**Solar Panel (50W):**
- Daily generation: 50W × 4.5h = 225Wh
- Charge controller efficiency (MPPT): 95%
- Actual daily generation: 225Wh × 0.95 = 213.75Wh

**Battery (12V 12Ah = 144Wh):**
- Usable capacity (70% DOD for AGM): 100.8Wh
- Backup days without sun: 100.8Wh ÷ 139.2Wh = 0.72 days

**Analysis:** ADEQUATE - Solar provides 154% of daily needs with nearly 1 day backup.
**Status:** PROPERLY SIZED for 6-12 month operation target.

### High Budget Tier Power System Validation

**Daily Energy Requirement:**
- Average power: 14W
- Daily energy: 14W × 24h = 336Wh

**Solar Panel (100W):**
- Daily generation: 100W × 4.5h = 450Wh
- Charge controller efficiency (MPPT): 96%
- Actual daily generation: 450Wh × 0.96 = 432Wh

**Battery (12V 35Ah LiFePO4 = 420Wh):**
- Usable capacity (90% DOD for LiFePO4): 378Wh
- Backup days without sun: 378Wh ÷ 336Wh = 1.13 days

**Analysis:** WELL SIZED - Solar provides 129% of daily needs with 1+ day backup.
**Status:** PROPERLY SIZED for 12+ month operation target.

## Connectivity Power Impact Analysis

### WiFi Connectivity Addition
- USB WiFi adapter: +1-2W
- WiFi range extender (if used): +5-8W via POE

### Cellular Connectivity Addition
- USB 4G modem: +2-4W during transmission
- 4G HAT: +1.5-3W during transmission
- 5G HAT: +3-6W during transmission
- Signal booster: +5-15W continuous

### Power System Adjustments for Connectivity

**Low Budget + Basic WiFi:**
- Additional power: 1.5W average
- New daily energy: (3.72W + 1.5W) × 24h = 125.3Wh
- Recommended: Upgrade to 30W solar panel

**Mid Budget + Enhanced Cellular:**
- Additional power: 2.5W average
- New daily energy: (5.8W + 2.5W) × 24h = 199.2Wh
- Current 50W solar provides: 213.75Wh
- Status: Still adequate but reduced margin

**High Budget + Premium Cellular:**
- Additional power: 4W average
- New daily energy: (14W + 4W) × 24h = 432Wh
- Current 100W solar provides: 432Wh
- Status: Exactly matched - consider 120W solar for margin

## Recommended Power System Revisions

### Low Budget Tier - Revised Solar Sizing
- **Original:** 10W solar + 4.5Ah battery = INSUFFICIENT
- **Revised:** 20W solar + 7Ah battery for basic operation
- **With connectivity:** 30W solar + 9Ah battery

### Mid Budget Tier - Current Sizing Validated
- **Current:** 50W solar + 12Ah AGM = ADEQUATE
- **With cellular:** Add 10W solar margin (60W total)

### High Budget Tier - Current Sizing Validated  
- **Current:** 100W solar + 35Ah LiFePO4 = WELL SIZED
- **With premium cellular:** Consider 120W solar for extended operation

## Climate-Specific Considerations for Indonesia

### Monsoon Season Impact
- Reduced solar generation during rainy season (June-September)
- Recommend 1.5x battery capacity during monsoon months
- Alternative: Implement power-saving sleep modes during low sun periods

### Temperature Effects
- Battery capacity reduction at high temperatures (>35°C)
- Solar panel efficiency reduction at high temperatures
- Include 15% temperature derating in calculations

### Humidity Impact
- Electronics consume additional power for humidity management
- Dehumidification systems add 2-5W continuous load
- Critical for preventing condensation on camera optics

## Final Validation Summary

✅ **Mid Budget Tier:** Power system properly sized for 6-12 month operation
✅ **High Budget Tier:** Power system well-sized for 12+ month operation  
❌ **Low Budget Tier:** Power system undersized - requires revision to 20W solar + 7Ah battery

**Critical Success Factor:** All tiers must account for monsoon season solar reduction and implement power management strategies for extended autonomous operation in tropical conditions.