# Rain Gauge Options for River Monitoring Station
## Research Report: Modbus vs Pulse-Output Rain Gauges

**Date:** January 9, 2026
**Context:** Optional sensor for river monitoring station in Indonesia
**Connection:** USB-RS485 adapter to Raspberry Pi (Modbus) or GPIO (pulse output)
**Environment:** Tropical climate, high humidity, outdoor deployment
**Budget Target:** Under $200

---

## Executive Summary

**Key Findings:**

1. **Modbus rain gauges are significantly more expensive** ($225-350 USD/EUR) and likely overkill for this application
2. **Pulse-output tipping bucket gauges** are the recommended solution: simpler, cheaper ($15-60), and well-documented with Raspberry Pi
3. **Best budget option:** DFRobot SEN0575 ($29.90) - includes I2C/UART interface, ready-to-go libraries, and weatherproof sensor
4. **Alternative budget option:** Misol WH-SP-RG ($14-30) - simple pulse output for GPIO, widely used in DIY weather stations
5. **For tropical environments:** 0.2-0.3mm resolution is adequate for flood monitoring; IP65+ rating and regular maintenance (every 3 months) are essential

**Recommendation:** Use a pulse-output tipping bucket gauge with GPIO interrupt counting. This approach is proven, cost-effective, and has extensive Python library support for Raspberry Pi.

---

## 1. Modbus RTU Rain Gauge Options

### 1.1 Seven Sensor 3S-RG-MB

**Specifications:**
- **Price:** £224.56 GBP (~$280 USD) - **OVER BUDGET**
- **Power:** 12-30V DC (24V nominal) - ✓ Meets requirements
- **Interface:** RS485 Modbus RTU (4800-38400 baud)
- **Resolution:** 0.2mm per tip (200 cm² collection area)
- **Measuring Range:** 600 mm/h
- **Protection:** IP rating not specified, but seawater-resistant anodized aluminum housing
- **Operating Temp:** Not specified in sources
- **Warranty:** 2 years

**Features:**
- Tipping bucket principle with reed relay
- Modbus register map based on SunSpec Alliance standards
- Common input register map available in user manual
- Reverse polarity and surge protection
- Isolated power supply and RS485 bus

**Modbus Implementation:**
- Supports subset of Modbus RTU commands
- Both holding and input registers supported
- Register map documentation available
- Compatible with Python libraries (minimalmodbus, pymodbus)

**Pros:**
- Professional-grade instrument
- Well-documented Modbus register map
- Industrial-quality construction
- Good warranty coverage
- Power supply meets requirements (12-30V)

**Cons:**
- **Price exceeds budget significantly**
- Overkill for non-scientific flood monitoring
- Requires RS485 interface and Modbus protocol implementation
- Lead time: 3-4 weeks for small orders
- No IP rating specified (aluminum housing suggests good protection)

**Sources:** [Seven Sensor Product Page](https://www.sevensensor.com/rain-gauge-with-modbus-rtu-output), [User Manual](https://manuals.plus/seven/3s-rg-rain-gauge-manual)

---

### 1.2 Linovision Modbus RS485 Metal Tipping Bucket

**Specifications:**
- **Price:** Not confirmed in search results (estimated $150-250 based on industrial pricing)
- **Interface:** RS485 Modbus RTU
- **Construction:** Stainless steel shell
- **Features:**
  - High precision and good stability
  - Mesh at funnel to prevent debris blockage
  - Sensitive reversing parts

**Applications:** Meteorological stations, hydrological stations, environmental protection, flood prevention, agriculture/forestry

**Pros:**
- Stainless steel construction (corrosion resistant for tropical environments)
- Designed for flood prevention applications
- Modbus RTU protocol

**Cons:**
- Price not confirmed (likely over budget)
- Limited documentation available
- Specifications not fully detailed in search results

**Sources:** [Linovision Global Store](https://global.linovision.com/products/modbus-rs485-metal-tipping-bucket-rain-sensor)

---

### 1.3 Other Modbus Options

**DFRobot RS485 7-in-1 Ultrasonic Weather Station:**
- **Price:** Not specified (likely $200+)
- **Features:** Wind speed/direction, temperature, humidity, pressure, light, rainfall
- **Rain Gauge:** Optical tipping bucket, 0.1mm resolution, ±4% accuracy
- **Protection:** IP54, UV-resistant ABS housing
- **Interface:** RS485 Modbus RTU

**Note:** Multi-sensor weather station may be overkill if you only need rainfall data.

**Source:** [DFRobot Product Page](https://www.dfrobot.com/product-2941.html)

---

### 1.4 Modbus Summary & Raspberry Pi Compatibility

**Python Libraries for Modbus on Raspberry Pi:**

1. **MinimalModbus**
   - Easy-to-use Python module for Modbus RTU/ASCII
   - Only dependency: pySerial
   - Supports Python 3.8-3.12
   - Ideal for simple Modbus implementations
   - Installation: `pip install minimalmodbus`
   - **Recommended for beginners** - simpler API

2. **PyModbus**
   - Full Modbus protocol implementation
   - Client and server with sync/async API
   - More comprehensive but more complex
   - Current version: 3.11.4
   - Installation: `pip install pymodbus`
   - **Recommended for advanced users** - more features

**Sources:** [MinimalModbus PyPI](https://pypi.org/project/minimalmodbus/), [PyModbus GitHub](https://github.com/pymodbus-dev/pymodbus), [Modbus on Raspberry Pi Tutorial](https://techsparx.com/energy-system/modbus/linux-modbus-usb-rs485.html)

---

## 2. Pulse-Output Tipping Bucket Rain Gauges (Recommended)

### 2.1 DFRobot SEN0575 - Gravity: Tipping Bucket Rainfall Sensor (TOP RECOMMENDATION)

**Specifications:**
- **Price:** $29.90 USD - ✓ **WELL WITHIN BUDGET**
  - Volume discounts: $29.00 (3+), $28.50 (5+), $27.50 (10+)
- **Power:** 3.3-5.5V DC, <3mA current - ✓ Perfect for Raspberry Pi
- **Interface:** I2C or UART (Gravity connector)
- **Resolution:** 0.28mm per tip
- **Operating Temp:** -40°C to 85°C - ✓ Excellent for tropical environments
- **Dimensions:** 118mm x 59mm x 80mm
- **Weight:** 119g (sensor), 5.3g (PCB)

**Features:**
- Based on tipping bucket principle
- No electronic components inside the bucket (increased reliability)
- Hollow bottom design for automatic water drainage
- Compatible with micro:bit, Arduino, ESP32, Raspberry Pi
- **Ready-to-go libraries provided** for Arduino and Raspberry Pi
- Easy-to-use Gravity interface

**Data Available from Sensor:**
- Current rainfall in millimeters
- 24-hour rainfall accumulation
- System operating time
- Total accumulated rainfall during operation

**Pros:**
- **Excellent value** - professional features at hobby price
- I2C/UART interface is more robust than simple pulse counting
- **Extensive software support** with example code
- Wide temperature range suitable for tropical climates
- Automatic drainage design prevents water accumulation
- Low power consumption (<3mA)
- Compatible with existing Raspberry Pi projects
- No need for RS485 adapter (uses I2C/UART directly)

**Cons:**
- Signal adapter board is NOT waterproof (must be protected)
- Slightly lower resolution (0.28mm vs 0.2mm for professional gauges)
- Limited information on IP rating for outdoor exposure
- May require enclosure for adapter board

**Implementation Notes:**
- Connect via I2C to Raspberry Pi GPIO pins
- Use provided Python libraries from DFRobot GitHub
- Can retrieve 24-hour rainfall data programmatically
- No need for interrupt handling (handled by sensor's MCU)

**Sources:** [DFRobot Product Page](https://www.dfrobot.com/product-2689.html), [DFRobot Wiki](https://wiki.dfrobot.com/SKU_SEN0575_Gravity_Rainfall_Sensor), [GitHub Library](https://github.com/DFRobot/DFRobot_RainfallSensor)

---

### 2.2 Misol WH-SP-RG Weather Station Rain Gauge

**Specifications:**
- **Price:** $14-30 USD - ✓ **EXCELLENT BUDGET OPTION**
- **Power:** Passive (reed switch only, no power required)
- **Interface:** Simple pulse output (reed switch)
- **Resolution:** 0.3mm per tip (some sources indicate 0.2794mm calibration)
- **Material:** ABS plastic
- **Weight:** 270 grams
- **Output:** Momentary contact closure (reed switch)

**Features:**
- Tipping bucket with magnet-activated reed switch
- Simple two-wire connection
- Precision die-casting process for dimensional accuracy
- Weather resistant, corrosion resistant, water resistant
- Widely used in DIY weather stations

**Raspberry Pi GPIO Connection:**
- Connect to GPIO pin (commonly GPIO 6 or GPIO 17)
- Connect other wire to ground
- Enable internal pull-up resistor in software
- Detect falling edge (3.3V to 0V transition)

**Example Python Code (using RPi.GPIO):**
```python
import RPi.GPIO as GPIO

PIN = 17  # or GPIO 6
CALIBRATION = 0.2794  # mm per tip

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def bucket_tipped(channel):
    global rain_count
    rain_count += 1
    rainfall_mm = rain_count * CALIBRATION
    print(f"Rainfall: {rainfall_mm:.2f} mm")

GPIO.add_event_detect(PIN, GPIO.FALLING,
                     callback=bucket_tipped,
                     bouncetime=300)  # 300ms debounce
```

**Example Python Code (using gpiozero - simpler):**
```python
from gpiozero import DigitalInputDevice

BUCKET_SIZE = 0.2794  # mm per tip
rain_sensor = DigitalInputDevice(6)
rain_count = 0

def bucket_tipped():
    global rain_count
    rain_count += 1
    print(f"Rainfall: {rain_count * BUCKET_SIZE:.2f} mm")

rain_sensor.when_activated = bucket_tipped
```

**Pros:**
- **Lowest cost option**
- No power required (passive reed switch)
- Simple GPIO connection - no special interface needed
- **Extensively documented** in Raspberry Pi community
- Used in official Raspberry Pi weather station project
- No protocol complexity
- Very low complexity for troubleshooting
- Proven reliability in DIY applications

**Cons:**
- No built-in data processing (must implement in software)
- Requires careful debounce timing (typically 150-300ms)
- May have false readings from wind or vibration
- Basic ABS construction (less robust than metal housings)
- No IP rating specified
- Reed switch may have limited lifespan vs. optical sensors

**Implementation Notes:**
- Use interrupts (not polling) for accurate counting
- Set appropriate debounce time (150-300ms recommended)
- For heavy tropical rain, 150ms debounce may be better than 300ms
- Regular cleaning recommended (debris can block tipping mechanism)

**Sources:** [Misol Rain Gauge](https://www.robotics.org.za/WH-SP-RG), [Raspberry Pi Tutorial](https://pi.gate.ac.uk/posts/2014/01/25/raingauge/), [Raspberry Pi Foundation Guide](https://github.com/raspberrypilearning/sensing-the-weather/blob/master/guides/rain_gauge.md)

---

### 2.3 Ecowitt WH40 Wireless Self-Emptying Rain Gauge

**Specifications:**
- **Price:** Approximately $50-80 USD (price not confirmed in search)
- **Power:** 1× AA battery (approximately 1 year life)
- **Interface:** Wireless 433/868/915/920 MHz (proprietary protocol)
- **Resolution:** 0.1mm
- **Accuracy:** ±5%
- **Operating Temp:** -40°C to 60°C
- **Protection:** IPX4
- **Dimensions:** 185×185×178mm
- **Weight:** 365g
- **Material:** ABS+PC plastic
- **Wireless Range:** Over 100 meters in open areas
- **Data Reporting Interval:** ~49 seconds

**Features:**
- Self-emptying design
- Wireless transmission (no wiring needed)
- WH40H version available with 3.5cm extension and bird spikes for heavy rainfall areas

**Pros:**
- True wireless (no cables to sensor)
- Self-emptying mechanism
- Better resolution than most budget options (0.1mm)
- Suitable for tropical temperature range
- Enhanced version available for heavy rainfall
- Good for remote placement

**Cons:**
- **Requires proprietary wireless gateway** (not direct Raspberry Pi connection)
- Would need to integrate with Ecowitt gateway or reverse-engineer protocol
- IPX4 is lower than ideal (IP65+ preferred for tropical environments)
- Battery replacement required annually
- More expensive than simple pulse gauges
- Not straightforward to integrate with Raspberry Pi

**Tropical Environment Notes:**
- Requires cleaning every 3 months
- Remove funnel and clean with damp cloth
- May need light insecticide spray to prevent insect interference
- Operating range suitable for tropical climates

**Not Recommended for This Project** due to proprietary wireless protocol and need for gateway device.

**Sources:** [Ecowitt WH40 Product Page](https://shop.ecowitt.com/products/wh40), [WH40 Manual](https://osswww.ecowitt.net/uploads/20220803/WH40%20Manual.pdf), [Accuracy Check Guide](https://ecowitt-subgqs9hhsx.gorgias.help/en-US/ws69wh40-rain-gauge-accuracy-issue-check-listing-564827)

---

## 3. Comparison: Modbus vs Pulse Output

### 3.1 Technical Comparison

| Feature | Modbus RTU (RS485) | Pulse Output (GPIO) |
|---------|-------------------|---------------------|
| **Cost** | $225-350 | $15-60 |
| **Complexity** | High (protocol, RS485 hardware) | Low (simple interrupt) |
| **Power** | 12-24V DC | 3.3-5V DC or passive |
| **Wiring** | RS485 A/B + Power (3+ wires) | Signal + Ground (2 wires) |
| **Python Libraries** | minimalmodbus, pymodbus | RPi.GPIO, gpiozero (built-in) |
| **Multi-sensor** | Yes (RS485 bus) | No (one sensor per GPIO) |
| **Data Available** | Rich (status, diagnostics) | Simple (pulse count only) |
| **Setup Complexity** | Moderate to high | Very low |
| **Debugging** | Protocol analyzer helpful | Simple multimeter sufficient |
| **Community Support** | Industrial/professional | Extensive DIY/maker community |

### 3.2 Advantages of Modbus RTU

**From Search Results:**
- Rain data transmitted digitally (no signal degradation over distance)
- Multiple probes on same network with minimal cabling
- Device status, serial number, and security hash available
- Tamper detection possible via security hash checking
- Data in both mm and pulse formats
- Industry-standard protocol with wide support
- Better for multi-sensor installations

**Source:** [Modbus Benefits](https://www.vaisala.com/en/blog/2021-10/benefits-digital-modbus-communication-compared-analog-signal-transmission)

### 3.3 Advantages of Pulse Output (GPIO)

**From Search Results:**
- Each bucket tip identical to button press (simple to interface)
- GPIO interrupts make implementation "dirt simple"
- RPi.GPIO library has built-in interrupt support
- Much simpler hardware (no RS485 adapter needed)
- Lower cost sensors widely available
- Extensive documentation in maker/DIY communities
- No protocol compatibility issues
- Easier troubleshooting

**Sources:** [GPIO Connection Guide](https://pi.gate.ac.uk/posts/2014/01/25/raingauge/), [Pulse Counter Discussion](https://www.letscontrolit.com/forum/viewtopic.php?t=1092)

### 3.4 Disadvantages of Modbus RTU

- Significantly higher cost ($225+ vs $15-60)
- Requires RS485-USB adapter (~$10-20 additional)
- Protocol implementation complexity
- Potential multi-vendor compatibility issues on RS485 bus
- Longer lead times (3-4 weeks typical)
- Overkill for single rain gauge application

### 3.5 Disadvantages of Pulse Output

- Debounce timing requires careful tuning
- Possible false readings from wind or vibration
- Foreign objects (leaves) can block sensor
- No built-in diagnostics or status information
- One sensor per GPIO pin (not easily expandable)
- Software must handle all data processing
- Reed switches have finite lifespan

---

## 4. Tropical Environment Considerations

### 4.1 Climate Challenges in Indonesia

**Key Findings:**
- Indonesia experiences higher rainfall than most countries
- Traditional tools unable to send data in real-time (problem this project solves)
- Humidity considerations important for electronics

**Research from Indonesia:**
A study on rain detection in Indonesia showed that microcontroller-based systems achieved 99% accuracy transmitting rainfall data over nearly 1 kilometer in 699ms, demonstrating feasibility of electronic rain monitoring in tropical conditions.

**Source:** [Indonesian Rain Detection Research](https://ieeexplore.ieee.org/document/10427783/)

### 4.2 Specifications for Tropical Deployment

**ABS Tipping Bucket Rain Gauges (Indonesia market):**
- Inner diameter: Φ200mm/8 inch
- Resolution: 0.2mm
- **Operating Temperature:** 0-50°C
- **Working Humidity:** <95% (at 40°C) - critical specification
- Measuring range: 0-4mm/min
- Accuracy: ≤±7%

**Source:** [Indonesian Supplier](https://www.microthings.id/product/abs-tipping-bucket-rain-gauge/)

### 4.3 Maintenance Requirements

**For Tropical/Humid Environments:**
1. **Cleaning Schedule:** Every 3 months minimum
2. **Procedure:**
   - Rotate funnel counterclockwise and lift
   - Clean funnel and bucket with damp cloth
   - Remove dirt, debris, and insects
   - Apply light insecticide spray if insect issues present
3. **Testing:**
   - Use syringe to slowly drip water onto bucket
   - Verify each tip registers correctly (0.1-0.3mm)
   - Do NOT pour water quickly (causes measurement errors)

**Sources:** [Ecowitt Maintenance Guide](https://ecowitt-subgqs9hhsx.gorgias.help/en-US/ws69wh40-rain-gauge-accuracy-issue-check-listing-564827), [Tipping Bucket Best Practices](https://pmc.ncbi.nlm.nih.gov/articles/PMC10302425/)

### 4.4 Protection Requirements

**Minimum Recommendations:**
- **Tipping bucket mechanism:** IP65+ (dust-tight, water jets)
- **Electronics enclosure:** IP66+ (dust-tight, powerful water jets)
- **Material:** UV-resistant ABS or stainless steel preferred
- **Corrosion resistance:** Important for coastal/humid areas
- **Mounting:** Secure against high winds (tropical storms)

**Note:** Many budget sensors don't specify IP ratings. Plan to:
- Mount electronics in separate weatherproof enclosure
- Use cable glands for wire entry
- Apply conformal coating to PCBs if possible
- Regular inspection and maintenance

---

## 5. Accuracy Requirements for Flood Monitoring

### 5.1 Resolution Standards

**Common Resolutions:**
- **0.1mm:** High precision (research-grade, optical sensors)
- **0.2mm:** Standard meteorological (WMO recommendations)
- **0.28mm:** Adequate for environmental monitoring
- **0.3mm (0.01"):** Common in DIY/budget sensors
- **0.5mm:** Lower precision but acceptable for some applications

**For Flood Monitoring:**
Research indicates that 0.2-0.3mm resolution is adequate for flood warning systems, as flood events typically involve substantial rainfall (10+ mm/hour). Real-time data transmission is more critical than ultra-high precision.

**Source:** [Tipping Bucket Research](https://pmc.ncbi.nlm.nih.gov/articles/PMC10302425/)

### 5.2 Accuracy Considerations

**Tipping Bucket Limitations:**
- Tend to underestimate rainfall, especially in heavy rain
- High winds can affect measurement
- Temperature variations may affect accuracy
- Regular calibration essential

**Adequate Accuracy for This Application:**
- ±5-7% accuracy typical for budget sensors
- ±3-5% for professional sensors
- For flood monitoring context, these are acceptable
- More important: consistent measurements and real-time data

**Sources:** [Tipping Bucket Applications](https://www.niubol.com/Product-knowledge/tipping-bucket-type-rain-gauge.html), [Accuracy Research](https://ntrs.nasa.gov/api/citations/20070016690/downloads/20070016690.pdf)

### 5.3 Data Requirements

**For Effective Flood Monitoring:**
1. **Temporal Resolution:** 1-5 minute intervals (GPIO interrupt provides real-time)
2. **Cumulative Rainfall:** 1-hour, 6-hour, 24-hour totals
3. **Rainfall Intensity:** mm/hour calculation
4. **Data Reliability:** More important than precision
5. **Long-term Operation:** Months without maintenance

**Implementation Recommendation:**
Store tip timestamps in database, calculate accumulations in software. This provides flexibility for different time intervals and intensity calculations.

---

## 6. Final Recommendations

### 6.1 Recommended Solution: DFRobot SEN0575

**Why This is the Best Choice:**
1. **Price:** $29.90 - excellent value, well under budget
2. **Interface:** I2C/UART - simple, no RS485 adapter needed
3. **Software:** Ready-to-go Python libraries for Raspberry Pi
4. **Resolution:** 0.28mm - adequate for flood monitoring
5. **Temperature Range:** -40°C to 85°C - excellent for tropical use
6. **Features:** Built-in data processing (24h totals, operating time)
7. **Power:** Low power (3.3-5V, <3mA) - can run from Pi directly
8. **Documentation:** Extensive, with example code

**Implementation:**
```python
# Example using DFRobot library
from DFRobot_RainfallSensor import *

sensor = DFRobot_RainfallSensor_I2C(bus=1, addr=0x1D)
sensor.set_rain_accumulated_value(0.0)  # Reset accumulation

while True:
    rainfall_1h = sensor.get_rainfall_hour()
    rainfall_24h = sensor.get_rainfall_day()
    print(f"1h: {rainfall_1h}mm, 24h: {rainfall_24h}mm")
    time.sleep(60)
```

**Important Notes:**
- Signal adapter board must be protected from rain (mount in enclosure)
- Consider conformal coating on PCB for humidity protection
- Test thoroughly before deployment

**Purchase Links:**
- [DFRobot Official](https://www.dfrobot.com/product-2689.html)
- [The Pi Hut (UK)](https://thepihut.com/products/gravity-tipping-bucket-rainfall-sensor)
- [Evelta (India)](https://evelta.com/rainfall-sensor-module-with-tipping-bucket-12c-uart/)

---

### 6.2 Budget Alternative: Misol WH-SP-RG

**If you need the absolute lowest cost:**
- **Price:** $14-30
- **Interface:** Simple GPIO pulse
- **Resolution:** 0.3mm (0.2794mm calibrated)
- **Power:** None (passive reed switch)

**Implementation:**
```python
from gpiozero import DigitalInputDevice
from datetime import datetime
import sqlite3

BUCKET_SIZE = 0.2794  # mm per tip
rain_sensor = DigitalInputDevice(6)

def log_rainfall():
    timestamp = datetime.now()
    # Store in database
    conn = sqlite3.connect('rainfall.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tips (timestamp, amount) VALUES (?, ?)',
                   (timestamp, BUCKET_SIZE))
    conn.commit()
    conn.close()

rain_sensor.when_activated = log_rainfall
```

**Trade-offs:**
- More manual coding required
- No built-in 24h totals (calculate in software)
- Simpler hardware but requires careful debounce tuning
- Proven reliability in thousands of DIY installations

---

### 6.3 Do NOT Recommend: Modbus Solutions

**Reasons:**
1. **Over Budget:** Minimum $225, typically $280-350
2. **Overkill:** Modbus advantages (multi-sensor bus, diagnostics) not needed for single rain gauge
3. **Complexity:** Requires RS485 adapter, protocol implementation
4. **Lead Time:** 3-4 weeks typical vs. immediate availability for pulse gauges
5. **No Significant Advantage:** For single sensor, pulse counting is simpler and equally reliable

**When Modbus WOULD Make Sense:**
- Deploying 5+ sensors on same RS485 bus
- Need for tamper detection and device diagnostics
- Industrial installation with existing Modbus infrastructure
- Budget >$500 for instrumentation
- Requirement for scientific-grade accuracy

**None of these apply to your river monitoring station.**

---

## 7. Implementation Checklist

### 7.1 Hardware Setup (DFRobot SEN0575)

- [ ] Purchase DFRobot SEN0575 rain gauge sensor ($29.90)
- [ ] Obtain weatherproof enclosure for signal adapter board (IP66+)
- [ ] Prepare mounting hardware (secure against winds)
- [ ] Install cable glands for wire entry to enclosure
- [ ] Test I2C communication on bench before deployment
- [ ] Apply conformal coating to adapter PCB (optional but recommended)

### 7.2 Software Setup

- [ ] Install Python dependencies: `pip install smbus2` (for I2C)
- [ ] Clone DFRobot library: `git clone https://github.com/DFRobot/DFRobot_RainfallSensor`
- [ ] Test with example code
- [ ] Implement data logging to database
- [ ] Create functions for 1h, 6h, 24h rainfall calculations
- [ ] Set up automatic data upload to server
- [ ] Implement error handling for sensor disconnection

### 7.3 Deployment Considerations

- [ ] Mount sensor at least 1m above ground
- [ ] Clear area around sensor (no trees/buildings blocking rainfall)
- [ ] Level the sensor (critical for tipping bucket accuracy)
- [ ] Secure cables against wind and animals
- [ ] Mount adapter board in weatherproof enclosure
- [ ] Test with known water volume (calibration check)
- [ ] Document installation date and location
- [ ] Schedule 3-month maintenance reminders

### 7.4 Testing Protocol

1. **Bench Test:**
   - Connect to Raspberry Pi
   - Verify I2C communication (check with `i2cdetect -y 1`)
   - Run example code
   - Manually tip bucket, verify count increments

2. **Calibration Test:**
   - Use graduated syringe or measuring cup
   - Slowly drip exactly 2.8ml of water (should = 10 tips = 2.8mm)
   - Compare measured vs. actual
   - Adjust calibration constant if needed

3. **Environmental Test:**
   - Deploy in test location for 1 week
   - Compare with nearby rain gauge if available
   - Check for false readings during no-rain periods
   - Verify data logging and upload working correctly

### 7.5 Maintenance Schedule

**Monthly:**
- Visual inspection (debris, insects, damage)
- Check cable connections
- Verify data is being logged correctly

**Quarterly (Every 3 Months):**
- Remove and clean funnel and bucket
- Check for corrosion or wear
- Perform calibration test
- Inspect enclosure seals

**Annually:**
- Complete disassembly and cleaning
- Replace any worn components
- Full calibration verification
- Check mounting hardware security

---

## 8. Cost Breakdown

### 8.1 Recommended Solution (DFRobot SEN0575)

| Item | Quantity | Unit Price | Total |
|------|----------|-----------|-------|
| DFRobot SEN0575 Rain Gauge | 1 | $29.90 | $29.90 |
| Weatherproof Enclosure (IP66) | 1 | $15-25 | $20.00 |
| Cable Glands (PG7 or PG9) | 2 | $2 | $4.00 |
| Mounting Hardware | 1 set | $5-10 | $7.50 |
| Conformal Coating (optional) | 1 | $10 | $10.00 |
| **TOTAL** | | | **$71.40** |

**Well under $200 budget with room for additional sensors or spares.**

### 8.2 Budget Alternative (Misol WH-SP-RG)

| Item | Quantity | Unit Price | Total |
|------|----------|-----------|-------|
| Misol WH-SP-RG Rain Gauge | 1 | $14-30 | $22.00 |
| Weatherproof Enclosure | 0 | - | $0.00 |
| Mounting Hardware | 1 set | $5-10 | $7.50 |
| **TOTAL** | | | **$29.50** |

**Extreme budget option - no enclosure needed as passive sensor. Could buy 3 units for redundancy under $100.**

### 8.3 Modbus Solution (Not Recommended)

| Item | Quantity | Unit Price | Total |
|------|----------|-----------|-------|
| Seven Sensor 3S-RG-MB | 1 | $280 | $280.00 |
| USB-RS485 Adapter | 1 | $15 | $15.00 |
| Weatherproof Enclosure | 1 | $20 | $20.00 |
| Mounting Hardware | 1 set | $7.50 | $7.50 |
| **TOTAL** | | | **$322.50** |

**Significantly over budget for no practical advantage in this application.**

---

## 9. Additional Resources

### 9.1 Raspberry Pi Rain Gauge Tutorials

- [Connecting a Rain Gauge (Gate AC UK)](https://pi.gate.ac.uk/posts/2014/01/25/raingauge/)
- [Raspberry Pi Foundation: Sensing the Weather](https://github.com/raspberrypilearning/sensing-the-weather/blob/master/guides/rain_gauge.md)
- [Gordon's Projects: Weather Station Wind and Rain](https://projects.drogon.net/raspberry-pi-weather-station-5-wind-and-rain/)

### 9.2 Technical References

- [Tipping Bucket Rain Gauges in Hydrological Research (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC10302425/)
- [Estimating Rain Rates from Tipping-Bucket Rain Gauge Measurements (NASA)](https://ntrs.nasa.gov/api/citations/20070016690/downloads/20070016690.pdf)
- [Seven Sensor 3S-RG User Manual](https://manuals.plus/seven/3s-rg-rain-gauge-manual)

### 9.3 Python Libraries

- [MinimalModbus Documentation](https://minimalmodbus.readthedocs.io/en/stable/)
- [PyModbus Documentation](https://pymodbus.readthedocs.io/en/latest/)
- [DFRobot RainfallSensor Library](https://github.com/DFRobot/DFRobot_RainfallSensor)
- [gpiozero Documentation](https://gpiozero.readthedocs.io/)

### 9.4 Product Documentation

- [DFRobot SEN0575 Wiki](https://wiki.dfrobot.com/SKU_SEN0575_Gravity_Rainfall_Sensor)
- [Ecowitt WH40 Manual PDF](https://osswww.ecowitt.net/uploads/20220803/WH40%20Manual.pdf)
- [Seven Sensor Product Page](https://www.sevensensor.com/rain-gauge-with-modbus-rtu-output)

---

## 10. Conclusion

**For your Indonesian river monitoring station, a pulse-output tipping bucket rain gauge with GPIO interrupt counting is strongly recommended over Modbus alternatives.**

**Top Choice: DFRobot SEN0575 ($29.90)**
- I2C interface eliminates debounce complexity
- Ready-to-go libraries save development time
- 0.28mm resolution adequate for flood monitoring
- Wide temperature range suitable for tropics
- Includes 24-hour rainfall totals in firmware
- Total project cost ~$70 vs. $320+ for Modbus

**Budget Alternative: Misol WH-SP-RG ($14-30)**
- Proven in thousands of DIY installations
- Simple GPIO pulse counting
- Extensive documentation in Raspberry Pi community
- Could deploy multiple units for redundancy
- Total project cost ~$30

**Modbus is Overkill:**
- 10x cost increase ($280+ vs $30)
- No meaningful advantage for single sensor
- Added complexity (RS485, protocol implementation)
- Longer lead times
- Save Modbus for multi-sensor installations or industrial requirements

**Critical Success Factors:**
1. Regular maintenance (quarterly cleaning)
2. Proper weatherproof enclosure for electronics
3. Secure mounting against tropical storms
4. Database logging with timestamps for flexible analysis
5. Test calibration before and after deployment

**The simplicity, cost-effectiveness, and extensive community support of pulse-output rain gauges make them the clear winner for this application.**

---

## Document Information

**Research Conducted:** January 9, 2026
**Researcher:** Claude (Anthropic)
**Project:** OpenRiverCam - Indonesia River Monitoring Station
**File Location:** `/home/tjordan/code/git/openrivercam/spring_2026_ID/research/rain_gauge_research.md`

---

## Sources

### Modbus Rain Gauge Products
- [Seven Sensor 3S-RG-MB Rain Gauge](https://www.sevensensor.com/rain-gauge-with-modbus-rtu-output)
- [Seven Sensor User Manual](https://manuals.plus/seven/3s-rg-rain-gauge-manual)
- [Linovision Modbus Rain Sensor](https://global.linovision.com/products/modbus-rs485-metal-tipping-bucket-rain-sensor)
- [DFRobot 7-in-1 Weather Station](https://www.dfrobot.com/product-2941.html)

### Pulse Output Rain Gauges
- [DFRobot SEN0575 Product Page](https://www.dfrobot.com/product-2689.html)
- [DFRobot SEN0575 Wiki](https://wiki.dfrobot.com/SKU_SEN0575_Gravity_Rainfall_Sensor)
- [DFRobot GitHub Library](https://github.com/DFRobot/DFRobot_RainfallSensor)
- [Misol WH-SP-RG Specifications](https://www.robotics.org.za/WH-SP-RG)
- [Ecowitt WH40 Product Page](https://shop.ecowitt.com/products/wh40)
- [Ecowitt WH40 Manual](https://osswww.ecowitt.net/uploads/20220803/WH40%20Manual.pdf)

### Raspberry Pi Integration
- [Raspberry Pi Rain Gauge Connection Guide](https://pi.gate.ac.uk/posts/2014/01/25/raingauge/)
- [Raspberry Pi Foundation: Sensing the Weather](https://github.com/raspberrypilearning/sensing-the-weather/blob/master/guides/rain_gauge.md)
- [Gordon's Weather Station Project](https://projects.drogon.net/raspberry-pi-weather-station-5-wind-and-rain/)
- [MinimalModbus PyPI](https://pypi.org/project/minimalmodbus/)
- [PyModbus GitHub](https://github.com/pymodbus-dev/pymodbus)
- [Modbus on Raspberry Pi Tutorial](https://techsparx.com/energy-system/modbus/linux-modbus-usb-rs485.html)

### Technical Research
- [Tipping Bucket Rain Gauges Research (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC10302425/)
- [Rain Rate Estimation (NASA)](https://ntrs.nasa.gov/api/citations/20070016690/downloads/20070016690.pdf)
- [Indonesian Rain Detection Research (IEEE)](https://ieeexplore.ieee.org/document/10427783/)
- [Indonesia ABS Rain Gauge](https://www.microthings.id/product/abs-tipping-bucket-rain-gauge/)
- [Modbus vs Analog Communication Benefits](https://www.vaisala.com/en/blog/2021-10/benefits-digital-modbus-communication-compared-analog-signal-transmission)
- [Tipping Bucket Applications Guide](https://www.niubol.com/Product-knowledge/tipping-bucket-type-rain-gauge.html)

### Community Forums
- [Raspberry Pi Forums: Rain Sensor Discussion](https://forums.raspberrypi.com/viewtopic.php?t=371715)
- [Let's Control It: Pulse Counter Discussion](https://www.letscontrolit.com/forum/viewtopic.php?t=1092)
- [MySensors Rain Gauge Build](https://www.mysensors.org/build/rain)
