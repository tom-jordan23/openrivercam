# IR Illumination Control Solution Research
## No-Solder, Plug-and-Play Solution for Solar-Powered River Monitoring Camera

**Date:** January 8, 2026
**Project:** Solar-powered Raspberry Pi 5 camera with Witty Pi 5 HAT+ power management
**Constraint:** NO cable cutting, NO soldering, NO custom wiring

---

## Executive Summary

**Key Findings:**

1. **Preferred Solution Identified:** IR flood lights with built-in photocell sensors ARE available (850nm, 12V, IP65+, screw terminals)
2. **Critical Challenge:** No true "plug-and-play" USB relay exists that automatically closes when USB power is detected without software commands
3. **Recommended Approach:** Two-relay series configuration OR software-controlled USB relay with boot script
4. **Best Product Match:** Tendelux AI4 or OOSSXX IR illuminators with integrated photocell + Numato Lab USB relay with systemd control
5. **Alternative:** XH-M131 photocell relay module in series with simple 5V-triggered relay powered by USB

---

## Research Scope

This investigation addresses the control of IR illumination for nighttime video capture on a Raspberry Pi 5 running intermittent duty cycles (wake every 15 minutes, capture 5s video, sleep). The solution must activate IR light ONLY when both conditions are met:

1. Raspberry Pi is powered/awake (USB port has 5V)
2. Ambient light is low (dusk/night/darkness)

All connections must use screw terminals, plugs, or standard connectors to enable assembly by non-technical staff.

---

## Section 1: IR Flood Lights with Built-in Photocell Sensors

### 1.1 Overview

Multiple manufacturers produce 850nm IR illuminators with integrated dusk-to-dawn photocell sensors specifically designed for security camera applications. These lights automatically turn ON when ambient light drops below ~10 lux and turn OFF at dawn.

### 1.2 Recommended Products

#### **Option A: Tendelux AI4 IR Illuminator** (Premium Choice)
- **Wavelength:** 850nm (semi-covert, faint red glow >5ft away)
- **Power:** 4W (4x 1W Epistar LEDs)
- **Input:** DC 12V, 0.5A
- **Beam Angle:** 90° wide angle flood
- **Range:** 50-80 feet effective
- **Photocell:** Built-in CdS photocell, auto on <10 lux
- **Weatherproofing:** IP65 (aluminum housing, tempered glass)
- **Mounting:** Swivel bracket with screw holes
- **Lifespan:** 30,000 hours
- **Temperature Range:** -25°C to 55°C
- **Power Connection:** Standard 5.5mm x 2.1mm DC barrel connector
- **What's Included:** IR illuminator, 100-240VAC to 12VDC 0.5A power supply, mounting hardware, user manual
- **Price:** ~$30-40 USD
- **Sources:** [Amazon](https://www.amazon.com/Tendelux-Illuminator-AI4-Infrared-Security/dp/B075ZYG89D), [Tendelux Official](https://tendelux.com/products/ai4-ir-illuminator-for-security-cameras-vr-headsets)

**Note:** Once installed, photocell sensor automatically controls operation. To force daytime operation, cover photocell with black tape.

#### **Option B: OOSSXX 8-LED IR Illuminator** (Mid-range)
- **Wavelength:** 850nm
- **Power:** 8W (8x 1W high-power LEDs)
- **Input:** DC 12V, 2A
- **Beam Angle:** 90° wide angle
- **Range:** 100 feet effective
- **Photocell:** Built-in light sensor, auto dusk-to-dawn
- **Weatherproofing:** IP67 (aluminum + reinforced glass)
- **Power Connection:** DC barrel connector + 10ft cable
- **Price:** ~$20-30 USD
- **Sources:** [OOSSXX Direct](https://oossxx.com/products/ir-illuminator-850nm-8-led-ir-illuminators-ir-lights-for-security-cameras-10ft-12v-2a-power-supply-ohwoai-long-range-infrared-light-outdoor-ir-floodlight-wide-angle-for-cctv-ip-camera-night-vision), [Walmart](https://www.walmart.com/ip/IR-Illuminator-8-LED-Long-Range-Outdoor-Use-Infrared-Light-Night-Vision-850nm-12V-Waterproof-floodlight-CCTV-Cameras-IP-Security-Camera/1262566598)

#### **Option C: OOSSXX 12-LED IR Illuminator** (High output)
- **Wavelength:** 850nm
- **Power:** 12W (12x 1W LEDs)
- **Input:** DC 12V, 2A
- **Beam Angle:** 90°
- **Range:** 120-150 feet
- **Photocell:** Built-in, automatic operation
- **Weatherproofing:** IP67
- **Price:** ~$30-40 USD
- **Sources:** [OOSSXX](https://oossxx.com/products/ir-illuminator-850nm-12-led-ir-illuminators-ir-lights-for-security-cameras-10ft-12v-2a-power-supply-ohwoai-long-range-infrared-light-outdoor-ir-floodlight-wide-angle-for-cctv-ip-camera-night-vision)

#### **Option D: Univivi 20-LED IR Illuminator** (Maximum range)
- **Wavelength:** 850nm
- **Power:** 20W (20 LEDs)
- **Input:** DC 12V
- **Beam Angle:** 90°
- **Photocell:** Built-in, auto dusk-to-dawn
- **Weatherproofing:** IP67
- **Range:** Extended range for larger areas
- **Price:** ~$35-50 USD
- **Source:** [Amazon](https://www.amazon.com/Univivi-Illuminators-Illuminator-Infrared-Waterproof/dp/B0CKPFQR79)

### 1.3 Key Specifications Comparison

| Model | Power | LEDs | Range | Current Draw | Price |
|-------|-------|------|-------|--------------|-------|
| Tendelux AI4 | 4W | 4x1W | 80ft | 0.33A @ 12V | $30-40 |
| OOSSXX 8-LED | 8W | 8x1W | 100ft | 0.67A @ 12V | $20-30 |
| OOSSXX 12-LED | 12W | 12x1W | 150ft | 1.0A @ 12V | $30-40 |
| Univivi 20-LED | 20W | 20 LEDs | 200ft+ | 1.67A @ 12V | $35-50 |

**Recommendation for River Monitoring:** Tendelux AI4 or OOSSXX 8-LED provide adequate illumination for close-range (10-30ft) water surface monitoring while minimizing power consumption from solar battery.

### 1.4 Power Consumption Analysis

For a 5-second video capture:
- **Tendelux AI4:** 4W × 5s = 0.0056 Wh per capture
- **OOSSXX 8-LED:** 8W × 5s = 0.011 Wh per capture

With 96 captures per day (every 15 minutes), assuming 50% occur at night:
- **AI4 Daily:** 48 captures × 0.0056 Wh = 0.27 Wh/day
- **8-LED Daily:** 48 captures × 0.011 Wh = 0.53 Wh/day

This is negligible compared to Pi power consumption, making any of these options viable.

### 1.5 Power Connection Adaptations

All IR illuminators come with barrel connector power supplies. To enable screw terminal connections:

**Barrel Connector to Screw Terminal Adapters:**
- **Female DC Barrel to Screw Terminal** (5.5mm x 2.1mm)
  - Supports 12V 3A or 24V 1.5A
  - No soldering required - simply insert wires and tighten screws
  - Price: ~$1-2 each (sold in 10-packs for $10-15)
  - **Sources:** [Amazon 10-pack](https://www.amazon.com/DEMASLED-Connector-Terminal-Adapter-Electronics/dp/B07KX65JLR), [US LED Supply](http://www.usledsupply.com/shop/female-power-connector-12v-screw.html)

**Male DC Barrel to Screw Terminal** (for power supply side):
- JacobsParts 5.5mm x 2.1mm male plugs
- 10-pack available
- **Source:** [Amazon](https://www.amazon.com/JacobsParts-Barrel-Screw-Connector-Electronics/dp/B01N38H40P)

---

## Section 2: USB-Powered Relay Modules

### 2.1 The Challenge: "Plug-and-Play" USB Relay

**Critical Finding:** No commercially available USB relay module exists that simply closes contacts when USB 5V power is present WITHOUT requiring software commands. All USB relay modules on the market require either:

1. Serial commands via virtual COM port (CDC devices)
2. HID protocol commands
3. Custom software control applications
4. GPIO trigger signals

This means a truly "zero-configuration" solution is not available with current USB relay technology.

### 2.2 USB Relay Options (Require Software Control)

#### **Option A: Numato Lab 1-Channel USB Powered Relay** (Recommended)
- **Power:** USB-powered (5V from USB port)
- **Relay Type:** SPDT (Single Pole Double Throw)
- **Contacts:** Screw terminals for NO/NC/COM
- **Load Capacity:** 2A @ 125VAC or 2A @ 30VDC
- **Control:** USB CDC (Virtual COM port) - requires serial commands
- **Interface:** Simple ASCII commands (e.g., "relay on 0", "relay off 0")
- **Driver:** Built-in to Linux/Raspbian (no installation needed)
- **API Support:** Python, Bash, C++, any language with serial port access
- **Dimensions:** Compact PCB with USB Type-A connector
- **Price:** $31.99 USD
- **Source:** [Numato Lab](https://numato.com/product/1-channel-usb-powered-relay-module/), [Amazon](https://www.amazon.com/Numato-Channel-Powered-Relay-Module/dp/B00MY5I6BO)

**Commands:**
```bash
# Turn relay ON
echo "relay on 0" > /dev/ttyACM0

# Turn relay OFF
echo "relay off 0" > /dev/ttyACM0

# Read relay status
echo "relay read 0" > /dev/ttyACM0
```

#### **Option B: Numato Lab 2-Channel USB Powered Relay**
- Same specs as 1-channel, with 2 independent SPDT relays
- Price: $37.99 USD
- Useful if second relay needed for future expansion
- **Source:** [Numato Lab](https://numato.com/product/2-channel-usb-powered-relay-module/)

#### **Option C: LCTECH USB Relay Module (LCUS-1)**
- **Power:** USB-powered
- **Relay:** SPDT, 10A @ 250VAC or 10A @ 30VDC
- **Control:** USB-to-UART (CH340T chip)
- **Commands:** Hex serial commands (e.g., A0 01 01 A2 for ON)
- **Price:** ~$10-15 USD
- **Source:** [Amazon (SMAKN)](https://www.amazon.com/SMAKN%C2%AE-LCUS-1-module-intelligent-control/dp/B01CN7E0RQ), [LCTech Direct](http://www.chinalctech.com/cpzx/32.html)

**Note:** Less user-friendly than Numato (hex commands vs. ASCII), but lower cost.

#### **Option D: Yoctopuce Yocto-PowerRelay-V2**
- **Power:** USB-powered
- **Relay:** SPDT power relay
- **Control:** Software API (Python, C++, etc.)
- **Load:** Higher capacity than Numato
- **LEDs:** Status indicators for relay state
- **Price:** Higher cost (~$50+ USD)
- **Source:** [Yoctopuce](https://www.yoctopuce.com/EN/products/usb-actuators/yocto-powerrelay-v2)

**Advantage:** More robust for industrial applications, but overkill for this use case.

### 2.3 Automation Solution: systemd Boot Script

Since USB relays require software control, the solution is to create a systemd service that runs on boot and activates the relay automatically when the Pi powers on.

**Implementation Steps:**

1. **Create Python Control Script** (`/home/pi/ir_control.py`):
```python
#!/usr/bin/env python3
import serial
import time

# Open relay serial port
relay = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
time.sleep(2)  # Wait for relay to initialize

# Turn relay ON
relay.write(b'relay on 0\r\n')
time.sleep(0.5)

# Keep script running (optional - relay stays on)
relay.close()
```

2. **Create systemd Service File** (`/etc/systemd/system/ir-relay.service`):
```ini
[Unit]
Description=IR Illuminator Relay Control
After=multi-user.target dev-ttyACM0.device
Wants=dev-ttyACM0.device

[Service]
Type=oneshot
User=pi
ExecStart=/usr/bin/python3 /home/pi/ir_control.py
RemainAfterExit=yes
ExecStop=/bin/sh -c 'echo "relay off 0" > /dev/ttyACM0'
StandardOutput=journal

[Install]
WantedBy=multi-user.target
```

3. **Enable Service:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable ir-relay.service
sudo systemctl start ir-relay.service
```

**How It Works:**
- When Pi boots, systemd waits for USB device (`dev-ttyACM0.device`) to be available
- Python script runs once, sends "relay on" command
- Relay closes, providing 12V power to IR light circuit
- IR light's built-in photocell determines if LEDs illuminate (based on ambient light)
- On shutdown, ExecStop sends "relay off" command

**Sources:**
- [SparkFun - Run Programs on Startup](https://learn.sparkfun.com/tutorials/how-to-run-a-raspberry-pi-program-on-startup/all)
- [TheDigitalPictureFrame - systemd Guide](https://www.thedigitalpictureframe.com/ultimate-guide-systemd-autostart-scripts-raspberry-pi/)
- [PragmaticLinux - systemd Startup](https://www.pragmaticlinux.com/2020/08/raspberry-pi-startup-script-using-systemd/)

### 2.4 Witty Pi Compatibility Considerations

The Witty Pi 5 HAT+ manages power cycling of the Raspberry Pi. Important notes:

- **GPIO Usage:** Witty Pi uses GPIO17 and GPIO4 for shutdown/wake control
- **No Conflict:** USB relay modules don't use GPIO (USB connection only)
- **Power Sequence:** USB ports power on when Pi boots, power off during sleep
- **Relay Behavior:** Relay will lose power during Pi sleep (desired behavior)

**Source:** [Witty Pi 4 Documentation](https://www.uugear.com/product/witty-pi-4/)

---

## Section 3: Alternative Approach - Dual Relay Configuration

If software control is undesirable, a two-relay series configuration provides hardware-only logic.

### 3.1 Architecture

**Relay 1:** 5V-triggered relay (powered by USB 5V)
**Relay 2:** 12V photocell relay module (senses ambient light)
**Connection:** Both relays in series - BOTH must close for 12V to reach IR light

### 3.2 Component Selection

#### **Relay 1: Simple 5V Relay Module**

Since no "USB plug-and-play" relay exists, use a basic 5V relay module with USB power adapter:

**Option: 5V SPDT Relay Module**
- **Trigger:** 5V DC (powered from USB via adapter)
- **Relay:** SPDT, 10A capacity
- **Connections:** Screw terminals for NO/NC/COM
- **Required Adapter:** USB to screw terminal power cable
- **Price:** ~$3-5 for relay module + $5 for USB power cable
- **Sources:** [Smart Prototyping](https://www.smart-prototyping.com/USB-Relay-1-Channel), Generic suppliers

**USB Power Cable:**
- USB Type-A male to screw terminal wires (red +5V, black GND)
- Search: "USB to screw terminal power cable"
- Plug into Pi USB port → screw terminals connect to relay coil (5V input)

**Limitations:**
- Relay module may have trigger circuit requiring GPIO signal (not just power)
- Many modules are designed for microcontroller control, not simple power detection
- May require custom DIY adapter

**DIY Solution:**
- Use a standard 5V coil relay (SPDT)
- Wire USB +5V and GND directly to relay coil via screw terminals
- Ensure relay coil voltage matches USB 5V
- Add flyback diode across coil for protection

**Relay Specifications Needed:**
- Coil voltage: 5V DC
- Coil current: <500mA (USB 2.0 limit)
- Contacts: SPDT, rated for 12V 2A minimum
- **Source Example:** [Winford RLP104](https://www.winford.com/products/rlp104.php) (board with screw terminals, multiple coil voltages available including 5V)

#### **Relay 2: XH-M131 Photocell Relay Module** (Recommended)

- **Input Voltage:** DC 12V
- **Trigger:** Light-dependent resistor (LDR) with adjustable threshold
- **Relay:** SPDT, 10A @ 250VAC or 10A @ 30VDC
- **Operation:** Relay energizes when ambient light falls below set threshold
- **Adjustment:** Onboard potentiometer for sensitivity tuning
- **Indicators:** Red LED (power), Blue LED (relay active)
- **Connections:** Screw terminals for power (12V IN) and relay contacts (NO/NC/COM)
- **Mounting:** 4x M3 mounting holes
- **Dimensions:** Small PCB module
- **Price:** ~$3-8 USD
- **Sources:**
  - [Makerlab Electronics](https://www.makerlab-electronics.com/products/12v-xh-m131-light-control-switch-relay-photoresistor-module)
  - [Amazon (various sellers)](https://www.amazon.com/Adjustable-photoresistor-Module-Control-Detection/dp/B084JN2YQY)
  - [IG Electronics](https://www.igelectronics.com/products/d3935d53b3/1726810000000965042)

**How It Works:**
- LDR resistance increases in darkness
- When threshold exceeded, comparator triggers relay
- Relay closes, connecting COM to NO
- Adjustable sensitivity allows tuning for dawn/dusk levels

**Alternative:** Other 12V photocell relay modules
- Multiple brands available (Ninetonine, Solu, Yosoo, Taidacent 2-channel)
- All operate on same principle: LDR → comparator → relay
- **Source:** [Amazon variety](https://www.amazon.com/Photoresistor-Sensor-Control-Switch-Detection/dp/B01M9I2QT7)

### 3.3 Dual Relay Wiring Diagram

```
Solar Battery (12V)
    |
    +--[Fuse]--[Relay 1 (5V USB-powered) COM]
                  |
                  [Relay 1 NO]
                  |
                  +--[Relay 2 (XH-M131 Photocell) 12V IN]
                  |   [Relay 2 COM]
                  |      |
                  |      [Relay 2 NO]
                  |          |
                  |          +--[IR Illuminator 12V+]
                  |                   |
                  +---[GND]-----------[IR Illuminator 12V-]

USB 5V (from Pi)
    |
    +--[USB Cable]--[Relay 1 Coil 5V+]
    |                   |
    [USB GND]-----------[Relay 1 Coil GND]

IR Light Photocell
    |
    [Covered or bypassed - XH-M131 controls light sensing]
```

**Logic Flow:**
1. Pi powers on → USB 5V present → Relay 1 coil energized → Relay 1 closes
2. Relay 1 closed → 12V reaches XH-M131 photocell module
3. XH-M131 photocell senses darkness → Relay 2 closes → 12V reaches IR light power input
4. IR light receives 12V power, but built-in photocell determines if LEDs illuminate
5. When Pi sleeps → USB 5V absent → Relay 1 opens → No power to XH-M131 → System off

**Note:** If using IR light with built-in photocell AND XH-M131, you have redundant light sensing. Options:
- **Option A:** Cover IR light's photocell with tape, rely solely on XH-M131 for light sensing
- **Option B:** Use IR light without photocell (harder to find), let XH-M131 handle all light detection
- **Option C:** Keep both active (both must sense darkness for light to turn on - more conservative)

### 3.4 Pros and Cons: Dual Relay vs. Software-Controlled USB Relay

| Aspect | Dual Relay (Hardware Logic) | USB Relay + Software |
|--------|----------------------------|----------------------|
| **Setup Complexity** | More components, more wiring | Fewer components, cleaner wiring |
| **Software Required** | None (pure hardware) | Python script + systemd service |
| **Cost** | $10-20 (two relays + adapters) | $30-40 (Numato relay) |
| **Reliability** | Hardware only, no software failure | Requires OS boot, script execution |
| **Debugging** | Visual (LED indicators on modules) | Requires log checking, serial terminal |
| **Power Consumption** | Two relays = higher standby current | Single relay, lower consumption |
| **Flexibility** | Fixed logic, no remote control | Can be modified, remotely controllable |
| **Assembly** | More connections, more failure points | Fewer connections, simpler assembly |

**Recommendation:**
- **For truly no-software solution:** Dual relay (if 5V relay USB adapter can be sourced)
- **For cleaner, more professional solution:** Numato USB relay with systemd service

---

## Section 4: Complete System Recommendations

### 4.1 Solution A: Software-Controlled USB Relay (Recommended)

**Components:**

1. **IR Illuminator:** Tendelux AI4 (4W, 850nm, built-in photocell, $35)
2. **USB Relay:** Numato Lab 1-Channel USB Powered Relay ($32)
3. **Power Adapters:**
   - Female DC barrel to screw terminal adapter ($1-2)
   - IR light comes with 12V power supply (discard or repurpose)
4. **Wiring:**
   - 18-22 AWG wire for 12V connections
   - USB Type-A to Type-A cable (Pi to relay, if relay doesn't have built-in USB plug)

**Total Cost:** ~$70 USD

**Wiring Diagram:**

```
                    Raspberry Pi 5 + Witty Pi 5 HAT+
                              |
                         [USB Port]
                              |
                    [Numato USB Relay Module]
                    COM    NO    NC
                     |      |     |
                     |      |    (not used)
                     |      |
Solar Battery 12V ---+      |
(via Witty Pi)              |
                            |
           [Barrel-to-Screw Adapter]
                            |
                            +---- 12V+ to IR Illuminator
                            |
GND ---------------------+--------- 12V- to IR Illuminator
```

**Assembly Steps:**

1. Connect Numato relay to Pi USB port (plug-and-play)
2. Connect solar battery 12V output to Numato relay COM terminal
3. Connect Numato relay NO terminal to barrel-to-screw adapter positive (+)
4. Connect solar battery GND to barrel-to-screw adapter negative (-)
5. Plug barrel adapter into Tendelux AI4 DC power input
6. Mount IR illuminator aimed at river surface
7. Install Python control script on Pi
8. Create and enable systemd service
9. Test: Pi powers on → relay clicks → IR light receives power → photocell controls LEDs

**Software Setup:**

See Section 2.3 for systemd configuration. One-time setup, fully automatic thereafter.

**Pros:**
- Clean, professional implementation
- Only 1 relay (lower power consumption)
- Screw terminals on relay for easy 12V connections
- Proven, documented components
- Remote control capability (can SSH in and toggle relay)

**Cons:**
- Requires basic Linux/systemd knowledge for setup
- Software dependency (script must run on boot)

---

### 4.2 Solution B: Dual Relay Hardware Logic

**Components:**

1. **IR Illuminator:** OOSSXX 8-LED (8W, 850nm, WITH photocell, $25)
   - OR IR illuminator WITHOUT photocell if you can find one
2. **Relay 1:** 5V SPDT Relay Module + USB power adapter (~$10)
   - Alternative: Winford RLP104 board (5V coil version, $30+)
3. **Relay 2:** XH-M131 12V Photocell Relay Module ($5-8)
4. **Adapters:**
   - USB to screw terminal power cable ($5)
   - Female DC barrel to screw terminal ($1-2)
5. **Wiring:** 18-22 AWG wire

**Total Cost:** ~$45-75 USD (depending on relay 1 solution)

**Wiring Diagram:**

```
Raspberry Pi USB Port
    |
 [USB to Screw Terminal Cable]
    +5V    GND
     |      |
   [Relay 1: 5V Coil Module]
   COM  NO  NC
    |    |   |
    |    |  (not used)
    |    |
    |    +-----------------+
    |                      |
    |                 [XH-M131 Module]
    |                 12V+ 12V- COM NO NC
    |                  |    |    |   |  |
Solar 12V ------------+    |    |   | (not used)
    |                       |    |   |
    |                       |    |   +--[IR Light 12V+]
    |                       |    |             |
    +-----------------------+----+-----[IR Light 12V-]
```

**Assembly Steps:**

1. Connect USB power cable to Pi USB port
2. Wire USB +5V and GND to Relay 1 coil input screw terminals
3. Connect solar 12V+ to Relay 1 COM terminal
4. Connect Relay 1 NO to XH-M131 12V+ input terminal
5. Connect XH-M131 12V- to solar GND
6. Connect XH-M131 relay COM to solar 12V+ (or Relay 1 COM)
7. Connect XH-M131 relay NO to IR illuminator 12V+ (via barrel adapter)
8. Connect solar GND to IR illuminator 12V-
9. Adjust XH-M131 potentiometer to set dusk threshold
10. Cover IR illuminator's photocell with tape (if present) - XH-M131 controls light sensing

**Tuning XH-M131:**
- Power the system in daylight
- Slowly adjust potentiometer until relay just turns OFF (blue LED off)
- This sets the day/night threshold
- Verify at dusk that relay activates when desired

**Pros:**
- No software configuration required
- Pure hardware logic - "set and forget"
- Visual feedback via relay LEDs
- Independent of OS state

**Cons:**
- More components = more potential failure points
- More complex wiring
- Higher component count for non-technical assembly
- Finding suitable 5V relay with simple USB power may be challenging
- Two relays consume more standby power than one

---

### 4.3 Solution C: Simplified Single USB Relay (Photocell Bypassed)

If light sensing is not critical (e.g., IR can run during day with minimal consequence):

**Components:**
- Numato USB Relay
- IR illuminator (ANY type, photocell not needed)
- systemd script

**Operation:**
- Pi powers on → relay activates → IR light ON (regardless of ambient light)
- Pi sleeps → relay deactivates → IR light OFF

**Pros:**
- Simplest wiring
- Lowest component count
- Easiest for non-technical staff

**Cons:**
- IR light may run during daytime captures (wastes power, reveals installation)
- No light sensing

**Use Case:** Only viable if daytime IR operation is acceptable.

---

## Section 5: Power Budget and Solar Considerations

### 5.1 IR Illuminator Power Draw During Capture

Assuming 5-second video capture every 15 minutes:

**Duty Cycle:**
- Captures per day: 96
- Night captures (50%): ~48
- IR on-time per capture: 5 seconds
- Total IR on-time per night: 48 × 5s = 240 seconds = 4 minutes

**Energy Consumption (per IR illuminator):**

| Model | Power | Daily Energy (48 captures) | Monthly Energy |
|-------|-------|---------------------------|----------------|
| Tendelux AI4 | 4W | 0.27 Wh | 8.1 Wh |
| OOSSXX 8-LED | 8W | 0.53 Wh | 15.9 Wh |
| OOSSXX 12-LED | 12W | 0.8 Wh | 24 Wh |
| Univivi 20-LED | 20W | 1.3 Wh | 39 Wh |

**Comparison to Pi Power:**

Raspberry Pi 5 typical power consumption:
- Idle: 3-4W
- Active (video capture): 5-8W
- Per 5-second capture: ~0.01 Wh
- 96 captures per day: ~1 Wh (capture only, not including boot/shutdown/upload)

**Conclusion:** Even the 20W IR illuminator adds only ~1.3 Wh/day, which is minimal compared to Pi operations. IR power is NOT a limiting factor for solar budget.

### 5.2 Relay Standby Power

**Numato Relay:**
- USB-powered, standby current negligible (<50mA @ 5V = 0.25W)
- Only powered when Pi is awake
- Energy impact: 96 wake cycles × 30s avg × 0.25W = ~0.2 Wh/day

**XH-M131 Photocell Relay:**
- Powered continuously (if using dual-relay approach)
- Standby: ~100mA @ 12V = 1.2W
- Daily: 1.2W × 24h = 28.8 Wh/day

**Important:** In dual-relay configuration, XH-M131 only receives power when Relay 1 is closed (Pi awake), so it's NOT continuously powered. Standby impact is minimal.

### 5.3 Fusing and Protection

**Recommended:**
- Inline fuse on 12V line to IR illuminator: 2A or 3A blade fuse
- Prevents overcurrent damage to relay contacts
- Protects solar battery from short circuits

**Components:**
- Inline blade fuse holder with screw terminals
- 2A or 3A ATC/ATO automotive blade fuse
- **Source:** Auto parts stores, Amazon, electronics suppliers

---

## Section 6: Assembly Instructions for Non-Technical Staff

### 6.1 Tools Required

- Phillips head screwdriver (small, for screw terminals)
- Wire strippers (if cutting wire to length)
- Multimeter (for testing continuity and voltage)
- Marker or label maker (for labeling wires)

### 6.2 Assembly Steps (Solution A: USB Relay + Software)

**Step 1: Prepare Components**
- Numato USB relay module (with USB cable if separate)
- Tendelux AI4 IR illuminator
- Female barrel-to-screw adapter
- 12V power wires (red and black, 18-22 AWG, ~2-3 feet each)
- Zip ties or cable management clips

**Step 2: Connect IR Illuminator Power Adapter**
1. Plug barrel-to-screw adapter into IR illuminator's DC power jack
2. Note which terminal is positive (+) - usually has marking or red wire
3. Tighten adapter connection (some have locking ring)

**Step 3: Wire Relay to 12V Source**
1. Locate Numato relay screw terminals: COM, NO, NC
2. Connect solar battery 12V+ (red) wire to COM terminal
   - Insert wire, tighten screw clockwise until snug (don't overtighten)
3. Connect barrel adapter positive (+) terminal to NO terminal
   - Use red wire for clarity

**Step 4: Complete Ground Connection**
1. Connect solar battery GND (black) to barrel adapter negative (-) terminal
2. Ensure tight connection

**Step 5: Connect USB Relay to Pi**
1. Plug Numato relay USB connector into any available Raspberry Pi USB port
2. Secure USB cable with zip tie to prevent disconnection

**Step 6: Test Without Power**
1. Check all screw terminals are tight (gentle tug on wires)
2. Verify no exposed wire strands outside terminals
3. Label wires: "12V+ from Solar", "To IR Light", "GND", etc.

**Step 7: Power-On Test**
1. Power on Raspberry Pi (Witty Pi powers up)
2. Wait for Pi to boot (~30 seconds)
3. Listen for relay click (indicates relay activated)
4. Use multimeter to verify 12V present at IR illuminator input
5. Cover IR illuminator photocell with hand - IR LEDs should glow (faint red)

**Step 8: Software Installation** (One-time, requires SSH/keyboard)
1. Copy Python script to `/home/pi/ir_control.py`
2. Create systemd service file (see Section 2.3)
3. Enable service: `sudo systemctl enable ir-relay.service`
4. Reboot and verify relay activates automatically

**Step 9: Final Installation**
1. Mount IR illuminator on enclosure or separate bracket
2. Aim at water surface (90° beam covers wide area)
3. Ensure IR illuminator is weatherproof (IP65 rating allows outdoor use)
4. Route wires neatly, secure with zip ties
5. Label everything for future troubleshooting

### 6.3 Testing and Verification

**Daytime Test:**
1. Power on Pi
2. Relay should click (USB relay activates)
3. IR illuminator receives power BUT photocell keeps LEDs off (bright ambient light)
4. No red glow visible

**Night Test:**
1. Power on Pi (or wait for scheduled boot)
2. Relay should click
3. IR illuminator receives power AND photocell activates LEDs (dark ambient light)
4. Faint red glow visible from IR LEDs when close (<5 feet)
5. Camera captures video with IR illumination

**Failure Modes:**

| Symptom | Likely Cause | Solution |
|---------|--------------|----------|
| No relay click on boot | Systemd service not running | Check `systemctl status ir-relay.service` |
| Relay clicks but no IR light | Photocell threshold too high | Cover photocell or wait for darker conditions |
| IR light always on | Photocell failed or covered | Check IR illuminator, uncover photocell |
| Relay doesn't click after reboot | USB device enumeration delay | Add delay in systemd service (After=...) |
| 12V not reaching IR light | Loose screw terminal | Re-tighten all terminals |

---

## Section 7: Alternative Components and Suppliers

### 7.1 IR Illuminators (Beyond Primary Recommendations)

**940nm Wavelength (Completely Invisible):**
- No glow visible to humans
- Requires camera with better IR sensitivity
- Examples: CMVision CM-LD100 ($40-60), Univivi 940nm ($30-50)
- Trade-off: Lower camera response compared to 850nm

**Wide Angle vs. Narrow Beam:**
- 90° flood (recommended): Wide coverage for river surface monitoring
- 15-30° spot: Narrow beam for long-range, specific target
- Tendelux makes both variants

**PoE-Powered IR Illuminators:**
- If switching to PoE camera in future
- Combined power + data over Ethernet
- Example: Axton Tech professional series ($100+)
- Not viable for current USB-relay approach

### 7.2 Relay Module Alternatives

**Solid-State Relays (SSR):**
- No mechanical contacts, silent operation
- Longer lifespan than electromechanical
- Example: Numato 1-Channel USB Solid State Relay ($35)
- **Source:** [Numato Lab SSR](https://numato.com/product/1-channel-usb-powered-solid-state-relay-module/)
- Trade-off: Higher cost, some have minimum load requirements

**Industrial USB Relay Controllers:**
- NCD.io USB Relay Controllers ($60-100)
- Higher current ratings (15A+), more robust
- **Source:** [NCD.io](https://store.ncd.io/product/usb-relay-controller-high-power-relays/)
- Overkill for this application

**DIN Rail Mount Relay Modules:**
- ASI 14036 (5V DC SPDT, DIN rail, $20-30)
- Professional installation, screw terminals
- **Source:** [SourceASI](https://www.sourceasi.com/shop/14036-5v-dc-relay-module-led-coil-status-fixed-relay-10-amp-250v-ac-contact-24-12-awg-spdt-din-rail-mount-25583)
- Requires 5V trigger signal (not direct USB power)

### 7.3 Photocell Relay Modules (Alternatives to XH-M131)

**Taidacent 2-Channel Photosensor Relay:**
- 12V DC, 2 independent channels
- Screw terminals, adjustable threshold
- Price: ~$10-15
- **Source:** [Amazon](https://www.amazon.com/Taidacent-2-Channel-Photosensor-Photocell-Photoelectric/dp/B07RSJMG7D)

**Pre-wired Photocell Switches (AC, not suitable):**
- Many photocells designed for 120V AC (e.g., intermatic)
- NOT compatible with 12V DC system
- Avoid unless specifically rated for DC

**Build-Your-Own LDR Circuit:**
- LDR + comparator (LM393) + relay
- Requires soldering (violates no-solder constraint)
- Not recommended unless comfortable with electronics

### 7.4 Wire and Connectors

**Wire Gauge for 12V IR Connections:**
- 18 AWG: Good for runs up to 10 feet, 2A current
- 20 AWG: Lighter, suitable for 1A loads, up to 5 feet
- 22 AWG: Thin, only for very short runs (<2 feet)
- Recommendation: 18 AWG stranded copper for all 12V wiring

**Ferrule Terminals:**
- Crimp-on wire ferrules improve screw terminal connections
- Prevents wire strand breakage
- Requires ferrule crimping tool
- Price: $10-20 for crimper + assorted ferrules
- **Source:** Amazon, electrical suppliers

**Quick Disconnect Connectors:**
- Allows easy removal of IR illuminator for maintenance
- Example: 2-pin automotive connectors (12V rated)
- Price: ~$1-2 per connector
- **Source:** Auto parts stores, Amazon

---

## Section 8: Troubleshooting Guide

### 8.1 Common Issues and Solutions

**Issue: Relay doesn't activate on Pi boot**

Possible Causes:
1. Systemd service not enabled
2. USB device enumeration delayed
3. Script has error

Solutions:
- Check service status: `sudo systemctl status ir-relay.service`
- View logs: `journalctl -u ir-relay.service -b`
- Test script manually: `python3 /home/pi/ir_control.py`
- Add longer delay in systemd After= directive
- Verify USB relay appears as `/dev/ttyACM0` (check `ls /dev/ttyACM*`)

**Issue: IR light doesn't turn on at night**

Possible Causes:
1. Photocell threshold set too high (too sensitive)
2. Ambient light from nearby source
3. Photocell sensor damaged
4. No 12V power reaching illuminator

Solutions:
- Cover photocell with black tape to force ON
- Adjust XH-M131 potentiometer (if using dual relay)
- Check voltage at IR illuminator input with multimeter
- Verify relay is closed (listen for click, check with multimeter)
- Test IR illuminator with direct 12V connection (bypass relay)

**Issue: IR light stays on during day**

Possible Causes:
1. Photocell covered or failed
2. Photocell threshold set too low (not sensitive enough)
3. Mounting location too dark (shadow, inside box)

Solutions:
- Inspect photocell sensor for obstructions
- Adjust threshold (XH-M131 potentiometer or check Tendelux placement)
- Reposition IR illuminator so photocell sees ambient light
- Test photocell by shining flashlight directly on sensor - should turn off

**Issue: Relay activates but no 12V at IR light**

Possible Causes:
1. Loose screw terminal connection
2. Wire break
3. Relay contacts failed
4. Incorrect relay terminal used (check NO vs NC)

Solutions:
- Re-tighten all screw terminals
- Use multimeter to trace voltage from solar battery → relay COM → relay NO → IR light
- Verify continuity when relay activated
- Check that NO (normally open) terminal is used, not NC (normally closed)

**Issue: Pi doesn't boot or Witty Pi issues**

Causes:
- Relay or wiring drawing too much current from Pi USB
- Witty Pi protection triggered

Solutions:
- Disconnect USB relay temporarily
- Boot Pi, check Witty Pi logs
- Verify solar battery has sufficient charge
- Check 12V wiring for shorts (disconnect from relay before testing)

### 8.2 Testing with Multimeter

**Basic Multimeter Tests:**

1. **12V Solar Battery Output:**
   - Set multimeter to DC voltage (20V range)
   - Black probe to GND, red probe to 12V+
   - Should read 12-14V (depending on battery charge)

2. **Relay Contact Continuity:**
   - Set multimeter to continuity/resistance mode
   - Power on Pi (relay should activate)
   - Measure between relay COM and NO
   - Should beep or show 0 ohms (closed)
   - Power off Pi, should show open circuit (infinite resistance)

3. **IR Illuminator Input Voltage:**
   - Set multimeter to DC voltage
   - Pi powered on, night conditions (or photocell covered)
   - Measure at IR illuminator DC input
   - Should read 12V

4. **USB 5V Output:**
   - Set multimeter to DC voltage
   - Measure USB port on Pi (when powered)
   - Should read 5.0-5.2V

### 8.3 Debugging systemd Service

**Commands:**

```bash
# Check if service is enabled
systemctl is-enabled ir-relay.service

# Check service status
sudo systemctl status ir-relay.service

# View recent logs
journalctl -u ir-relay.service -n 50

# View logs since last boot
journalctl -u ir-relay.service -b

# Restart service
sudo systemctl restart ir-relay.service

# Stop service
sudo systemctl stop ir-relay.service

# Disable service (prevent boot startup)
sudo systemctl disable ir-relay.service

# Reload systemd after editing service file
sudo systemctl daemon-reload
```

**Manual Relay Control:**

```bash
# Turn relay on
echo "relay on 0" > /dev/ttyACM0

# Turn relay off
echo "relay off 0" > /dev/ttyACM0

# Read relay status
echo "relay read 0" > /dev/ttyACM0
```

---

## Section 9: Cost Summary and Purchasing

### 9.1 Solution A: USB Relay + Software (Recommended)

| Component | Model/Type | Quantity | Unit Price | Total |
|-----------|------------|----------|------------|-------|
| IR Illuminator | Tendelux AI4 | 1 | $35 | $35 |
| USB Relay | Numato Lab 1-Ch | 1 | $32 | $32 |
| Barrel Adapter | Female 5.5mm screw terminal | 1 | $1.50 | $1.50 |
| Wire | 18 AWG red/black pair | 10 ft | $5 | $5 |
| Inline Fuse Holder | Blade fuse holder + 2A fuse | 1 | $3 | $3 |
| USB Cable | Type-A extension (if needed) | 1 | $5 | $5 |
| **TOTAL** | | | | **$81.50** |

**Where to Buy:**
- IR Illuminator: Amazon, Tendelux direct
- USB Relay: Numato Lab direct, Amazon
- Adapters/wire: Amazon, local electronics store
- Fuse holder: Auto parts store, Amazon

### 9.2 Solution B: Dual Relay Hardware Logic

| Component | Model/Type | Quantity | Unit Price | Total |
|-----------|------------|----------|------------|-------|
| IR Illuminator | OOSSXX 8-LED | 1 | $25 | $25 |
| 5V Relay Module | Generic SPDT | 1 | $10 | $10 |
| USB Power Cable | USB to screw terminal | 1 | $5 | $5 |
| Photocell Relay | XH-M131 | 1 | $6 | $6 |
| Barrel Adapter | Female 5.5mm screw terminal | 1 | $1.50 | $1.50 |
| Wire | 18 AWG | 15 ft | $7 | $7 |
| Inline Fuse Holder | Blade fuse holder + 2A fuse | 1 | $3 | $3 |
| **TOTAL** | | | | **$57.50** |

**Note:** This assumes you can source a suitable 5V relay that works with simple USB power. If using Winford RLP104, add $20-30.

### 9.3 Bulk Purchasing Considerations

For multiple camera installations:

- **Barrel adapters:** Sold in 10-packs for $10-15 (save $5-10)
- **XH-M131 modules:** Often available in 2-packs for $10-12
- **Wire:** Buy 100ft spools for $15-20 instead of per-foot pricing
- **Fuse holders:** 5-packs for $10-12

**Estimated savings for 5+ installations:** 15-20% per unit

---

## Section 10: Final Recommendations

### 10.1 Recommended Solution: USB Relay + Software

**Rationale:**
1. **Simplicity:** Fewer components, cleaner wiring, easier assembly
2. **Reliability:** One relay point of failure vs. two
3. **Professional:** Proven components with good documentation
4. **Maintainability:** Easy to diagnose via SSH, check logs
5. **Flexibility:** Can add remote control, logging, or additional logic later

**Best Component Choices:**
- **IR Illuminator:** Tendelux AI4 (best balance of power, quality, reliability)
- **USB Relay:** Numato Lab 1-Channel (well-documented, easy control, screw terminals)

**Setup Time:**
- Assembly: 30 minutes
- Software configuration: 20 minutes (one-time)
- Testing: 15 minutes
- **Total:** ~65 minutes for first installation

### 10.2 When to Consider Dual Relay Approach

**Use Cases:**
1. Absolute requirement for zero software configuration
2. Installation site has no network access for SSH (can't troubleshoot remotely)
3. Multiple installations where setup time is critical
4. Non-technical staff who cannot handle systemd configuration

**Trade-offs:**
- Higher component count
- More complex wiring
- Finding suitable 5V USB relay may be difficult
- More failure points (two relays vs. one)

### 10.3 Critical Success Factors

Regardless of solution chosen:

1. **Test Before Deployment:**
   - Bench test entire system before field installation
   - Verify all connections, software (if applicable), light sensing
   - Document configuration (take photos of wiring)

2. **Label Everything:**
   - Use wire labels or tags
   - Mark polarity (red = +12V, black = GND)
   - Label relay terminals
   - Document in logbook

3. **Weatherproofing:**
   - IR illuminator is IP65 - suitable for outdoor mounting
   - Relay modules should be in weatherproof enclosure
   - Use waterproof cable glands for wire entry
   - Seal all connections with heat shrink or electrical tape

4. **Documentation for Staff:**
   - Create laminated quick-reference card
   - Include troubleshooting steps
   - List expected behaviors (relay click on boot, IR glow at night)
   - Contact info for technical support

5. **Spare Parts:**
   - Keep extra relay module
   - Spare IR illuminator (or at least spare LEDs if serviceable)
   - Extra wire, connectors, fuses

### 10.4 Future Enhancements

**Possible Upgrades:**

1. **Data Logging:**
   - Log relay activation times
   - Track IR on-time for maintenance prediction
   - Python script can write to CSV file

2. **Remote Monitoring:**
   - Integrate with existing monitoring system
   - Alert if relay fails to activate
   - Camera could capture IR LED reflection to verify operation

3. **Manual Override:**
   - Add physical switch to force IR on/off
   - Useful for testing, maintenance

4. **Power Monitoring:**
   - Add current sensor to measure IR power draw
   - Detect LED degradation over time
   - Alert if draw outside expected range

5. **Multi-Camera Support:**
   - Numato 2-channel or 4-channel relay can control multiple IR lights
   - Synchronized activation for multi-camera setups

---

## Section 11: Conclusion

### 11.1 Summary of Findings

This research has identified viable, no-solder solutions for controlling IR illumination on a solar-powered river monitoring camera. Key conclusions:

1. **IR illuminators with built-in photocell sensors are readily available** at consumer prices ($20-40), eliminating the need for external light sensing in most configurations.

2. **No true "plug-and-play" USB relay exists** that automatically closes contacts when USB power is present. All USB relay modules require software commands.

3. **Software control via systemd is straightforward** and provides a reliable, professional solution with minimal setup time for those comfortable with basic Linux administration.

4. **Dual relay configurations are possible** but add complexity without significant benefit, unless absolute zero-software operation is required.

5. **Power consumption of IR illumination is negligible** compared to Raspberry Pi operation, making even high-power IR illuminators viable for solar installations.

6. **Total solution cost is reasonable:** $60-85 for complete system depending on component choices.

### 11.2 Recommended Path Forward

**Immediate Next Steps:**

1. **Order Components:**
   - Tendelux AI4 IR Illuminator ($35)
   - Numato Lab 1-Channel USB Powered Relay ($32)
   - Barrel-to-screw terminal adapter ($1.50)
   - 18 AWG wire, fuse holder, misc. hardware (~$15)

2. **Bench Test:**
   - Assemble on workbench before field deployment
   - Test relay control with manual commands
   - Install and test systemd service
   - Verify IR activation in dark conditions

3. **Create Assembly Documentation:**
   - Take photos of each wiring step
   - Create laminated instruction sheet for field technicians
   - Include troubleshooting flowchart

4. **Field Installation:**
   - Mount IR illuminator with clear view of water surface
   - Route wiring through weatherproof enclosure
   - Verify 12V supply from solar system
   - Test full wake/capture/sleep cycle

5. **Monitor Performance:**
   - Check systemd logs after first week
   - Verify IR activation during nighttime captures
   - Assess video quality with IR illumination

### 11.3 Expected Outcomes

Upon successful implementation:

- **Nighttime video capture** will have consistent IR illumination
- **IR light will only activate** when Pi is awake AND ambient light is low
- **No manual intervention** required after initial setup
- **Power consumption** remains within solar budget
- **Assembly and maintenance** achievable by non-technical staff with proper documentation

### 11.4 Risk Assessment

**Low Risk:**
- Component availability (all items readily available, multiple suppliers)
- Power budget (IR power negligible)
- Weatherproofing (IP65 rated components)

**Medium Risk:**
- systemd service configuration (requires basic Linux knowledge, but well-documented)
- USB device enumeration timing (may require tuning After= directives)

**Mitigation:**
- Provide pre-configured SD card image with service already installed
- Include detailed troubleshooting guide
- Test extensively on bench before field deployment

**Overall Assessment:** Low risk, high feasibility solution.

---

## Appendix A: Product Links and Sources

### IR Illuminators

- **Tendelux AI4:** [Amazon](https://www.amazon.com/Tendelux-Illuminator-AI4-Infrared-Security/dp/B075ZYG89D) | [Tendelux Direct](https://tendelux.com/products/ai4-ir-illuminator-for-security-cameras-vr-headsets)
- **OOSSXX 8-LED:** [OOSSXX](https://oossxx.com/products/ir-illuminator-850nm-8-led-ir-illuminators-ir-lights-for-security-cameras-10ft-12v-2a-power-supply-ohwoai-long-range-infrared-light-outdoor-ir-floodlight-wide-angle-for-cctv-ip-camera-night-vision) | [Walmart](https://www.walmart.com/ip/IR-Illuminator-8-LED-Long-Range-Outdoor-Use-Infrared-Light-Night-Vision-850nm-12V-Waterproof-floodlight-CCTV-Cameras-IP-Security-Camera/1262566598)
- **OOSSXX 12-LED:** [OOSSXX](https://oossxx.com/products/ir-illuminator-850nm-12-led-ir-illuminators-ir-lights-for-security-cameras-10ft-12v-2a-power-supply-ohwoai-long-range-infrared-light-outdoor-ir-floodlight-wide-angle-for-cctv-ip-camera-night-vision)
- **Univivi 20-LED:** [Amazon](https://www.amazon.com/Univivi-Illuminators-Illuminator-Infrared-Waterproof/dp/B0CKPFQR79)

### USB Relay Modules

- **Numato Lab 1-Ch:** [Numato Direct](https://numato.com/product/1-channel-usb-powered-relay-module/) | [Amazon](https://www.amazon.com/Numato-Channel-Powered-Relay-Module/dp/B00MY5I6BO)
- **Numato Lab 2-Ch:** [Numato Direct](https://numato.com/product/2-channel-usb-powered-relay-module/)
- **LCTECH LCUS-1:** [Amazon (SMAKN)](https://www.amazon.com/SMAKN%C2%AE-LCUS-1-module-intelligent-control/dp/B01CN7E0RQ)
- **Yoctopuce PowerRelay-V2:** [Yoctopuce](https://www.yoctopuce.com/EN/products/usb-actuators/yocto-powerrelay-v2)

### Photocell Relay Modules

- **XH-M131:** [Makerlab Electronics](https://www.makerlab-electronics.com/products/12v-xh-m131-light-control-switch-relay-photoresistor-module) | [Amazon](https://www.amazon.com/Adjustable-photoresistor-Module-Control-Detection/dp/B084JN2YQY) | [IG Electronics](https://www.igelectronics.com/products/d3935d53b3/1726810000000965042)
- **Taidacent 2-Ch:** [Amazon](https://www.amazon.com/Taidacent-2-Channel-Photosensor-Photocell-Photoelectric/dp/B07RSJMG7D)

### Connectors and Adapters

- **Barrel to Screw Terminal (Female):** [Amazon 10-pack](https://www.amazon.com/DEMASLED-Connector-Terminal-Adapter-Electronics/dp/B07KX65JLR) | [US LED Supply](http://www.usledsupply.com/shop/female-power-connector-12v-screw.html)
- **Barrel to Screw Terminal (Male):** [Amazon](https://www.amazon.com/JacobsParts-Barrel-Screw-Connector-Electronics/dp/B01N38H40P)
- **CPS-x2ST Adapter:** [Super Bright LEDs](https://www.superbrightleds.com/cps-x2st-standard-barrel-connector-to-screw-terminal-adapter)

### Wire and Hardware

- **18 AWG Wire:** Local hardware stores, Amazon, electronics suppliers
- **Inline Fuse Holders:** Auto parts stores (AutoZone, O'Reilly), Amazon
- **Ferrule Crimp Kit:** Amazon, Harbor Freight Tools

---

## Appendix B: Technical Specifications Reference

### IR Illuminator Wavelengths

| Wavelength | Visibility | Camera Response | Use Case |
|------------|------------|-----------------|----------|
| 850nm | Faint red glow (<5ft) | Excellent | General purpose, best camera response |
| 940nm | Completely invisible | Good | Covert applications, lower camera sensitivity |

### Relay Ratings

| Type | Voltage | Current | Lifespan | Noise |
|------|---------|---------|----------|-------|
| Electromechanical SPDT | 12-250V AC/DC | 2-10A | 100k cycles | Audible click |
| Solid State Relay (SSR) | 12-250V AC/DC | 2-25A | 100M+ cycles | Silent |

### Photocell Activation Thresholds

- Typical activation: 5-10 lux (dusk/dawn)
- Adjustable range: 2-50 lux (varies by module)
- Daylight: 10,000+ lux
- Full moon: 0.1-1 lux
- Overcast day: 1,000 lux

### Power Connector Standards

| Connector | Voltage | Current | Common Use |
|-----------|---------|---------|------------|
| 5.5mm x 2.1mm barrel | 12V DC | 2-5A | Most common (CCTV, LED) |
| 5.5mm x 2.5mm barrel | 12V DC | 2-5A | Alternative standard |
| USB Type-A | 5V DC | 0.5-3A | Computer peripherals |
| Screw terminals | Any | 10-30A | Industrial, custom wiring |

---

## Appendix C: Python Script Example

**File: `/home/pi/ir_control.py`**

```python
#!/usr/bin/env python3
"""
IR Illuminator Relay Control Script
Activates USB relay on Raspberry Pi boot to enable IR light
Designed for Numato Lab 1-Channel USB Powered Relay
"""

import serial
import time
import sys
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/ir_control.log'),
        logging.StreamHandler()
    ]
)

# Configuration
RELAY_PORT = '/dev/ttyACM0'
BAUD_RATE = 9600
RELAY_CHANNEL = 0
INIT_DELAY = 2  # seconds to wait for relay initialization

def activate_relay():
    """
    Activate the USB relay to enable 12V power to IR illuminator.
    """
    try:
        logging.info(f"Opening relay serial port: {RELAY_PORT}")
        relay = serial.Serial(RELAY_PORT, BAUD_RATE, timeout=1)

        # Wait for relay to initialize
        time.sleep(INIT_DELAY)

        # Send activation command
        command = f'relay on {RELAY_CHANNEL}\r\n'
        logging.info(f"Sending command: {command.strip()}")
        relay.write(command.encode())

        # Wait for confirmation
        time.sleep(0.5)

        # Verify relay status (optional)
        status_command = f'relay read {RELAY_CHANNEL}\r\n'
        relay.write(status_command.encode())
        time.sleep(0.2)
        response = relay.read(100).decode('utf-8', errors='ignore')
        logging.info(f"Relay status: {response.strip()}")

        # Close serial connection
        relay.close()
        logging.info("Relay activated successfully")
        return True

    except serial.SerialException as e:
        logging.error(f"Serial port error: {e}")
        return False
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return False

def deactivate_relay():
    """
    Deactivate the USB relay (called on shutdown).
    """
    try:
        logging.info(f"Opening relay serial port: {RELAY_PORT}")
        relay = serial.Serial(RELAY_PORT, BAUD_RATE, timeout=1)
        time.sleep(1)

        # Send deactivation command
        command = f'relay off {RELAY_CHANNEL}\r\n'
        logging.info(f"Sending command: {command.strip()}")
        relay.write(command.encode())
        time.sleep(0.5)

        relay.close()
        logging.info("Relay deactivated successfully")
        return True

    except Exception as e:
        logging.error(f"Error deactivating relay: {e}")
        return False

if __name__ == "__main__":
    # Check command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == "off":
        logging.info("Shutdown mode - deactivating relay")
        success = deactivate_relay()
    else:
        logging.info("Startup mode - activating relay")
        success = activate_relay()

    sys.exit(0 if success else 1)
```

**Make executable:**
```bash
chmod +x /home/pi/ir_control.py
```

---

## Appendix D: systemd Service File Example

**File: `/etc/systemd/system/ir-relay.service`**

```ini
[Unit]
Description=IR Illuminator Relay Control
Documentation=https://github.com/your-repo/ir-control
After=multi-user.target
# Wait for USB device to be available
After=dev-ttyACM0.device
Wants=dev-ttyACM0.device

[Service]
Type=oneshot
User=pi
Group=pi

# Activate relay on startup
ExecStart=/usr/bin/python3 /home/pi/ir_control.py

# Deactivate relay on shutdown
ExecStop=/usr/bin/python3 /home/pi/ir_control.py off

# Keep service marked as active after ExecStart completes
RemainAfterExit=yes

# Restart policy
Restart=no

# Logging
StandardOutput=journal
StandardError=journal
SyslogIdentifier=ir-relay

# Security settings
NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

**Installation:**
```bash
# Copy service file
sudo cp ir-relay.service /etc/systemd/system/

# Reload systemd
sudo systemctl daemon-reload

# Enable service (start on boot)
sudo systemctl enable ir-relay.service

# Start service now
sudo systemctl start ir-relay.service

# Check status
sudo systemctl status ir-relay.service
```

---

## Appendix E: Wiring Diagrams

### Diagram 1: USB Relay + IR Illuminator (Recommended Solution)

```
┌─────────────────────────────────────────────────────────────────┐
│                    RASPBERRY PI 5 + WITTY PI 5                  │
│                                                                 │
│  ┌────────────────────────┐         ┌───────────────────┐     │
│  │   Solar Power Input    │         │    USB Port       │     │
│  │   12V from Witty Pi    │         └─────────┬─────────┘     │
│  └───────────┬────────────┘                   │               │
│              │                                 │               │
└──────────────┼─────────────────────────────────┼───────────────┘
               │                                 │
               │                                 │ USB Cable
               │                                 │
               │                          ┌──────▼──────┐
               │                          │  NUMATO LAB │
               │                          │  USB RELAY  │
               │                          │  1-CHANNEL  │
               │                          └──────┬──────┘
               │                                 │
               │                          ┌──────┴──────┐
               │                          │ COM  NO  NC │
               │                          └──┬───┬──┬───┘
               │                             │   │  │
               │                             │   │  (not used)
               │                             │   │
               │12V+                         │   │
               └─────────────────────────────┘   │
                                                 │
                                          ┌──────▼──────┐
                                          │  Barrel to  │
                                          │  Screw Term │
                                          │  Adapter    │
                                          └──────┬──────┘
                                                 │
                                          ┌──────▼──────────┐
                                          │  TENDELUX AI4   │
                                          │  IR ILLUMINATOR │
                                          │  (with photocell)│
                                          └─────────────────┘
                                                 │
                                                 │
                                          ┌──────▼──────┐
                                          │     GND     │
                                          └─────────────┘

LEGEND:
  12V+ = Red wire
  GND  = Black wire
  USB  = Standard USB Type-A cable
```

### Diagram 2: Dual Relay Configuration (Alternative)

```
┌─────────────────────────────────────────────────────────────────┐
│                    RASPBERRY PI 5 + WITTY PI 5                  │
│                                                                 │
│  ┌────────────────────────┐         ┌───────────────────┐     │
│  │   Solar Power Input    │         │    USB Port       │     │
│  │   12V from Witty Pi    │         └─────────┬─────────┘     │
│  └───────────┬────────────┘                   │               │
│              │                                 │               │
└──────────────┼─────────────────────────────────┼───────────────┘
               │                                 │
               │12V+                             │ USB to Screw
               │                                 │ Terminal Cable
               │                                 │
               │                          ┌──────▼──────────┐
               │                          │   5V RELAY #1   │
               │                          │  (USB-powered)  │
               │                          └──────┬──────────┘
               │                                 │
               │                          ┌──────┴──────┐
               │                          │ COM  NO  NC │
               │                          └──┬───┬──┬───┘
               │                             │   │  │
               │                             │   │  (not used)
               └─────────────────────────────┘   │
                                                 │
                                          ┌──────▼───────────┐
                                          │   XH-M131        │
                                          │   PHOTOCELL      │
                                          │   RELAY #2       │
                                          │                  │
                                          │ 12V+ ─┐          │
                                          │ 12V- ─┼─ (from Relay 1 NO)
                                          │       │          │
                                          │ COM   NO   NC    │
                                          └───┬────┬───┬─────┘
                                              │    │   │
                                       (to 12V+)   │  (not used)
                                                   │
                                            ┌──────▼──────┐
                                            │  Barrel to  │
                                            │  Screw Term │
                                            │  Adapter    │
                                            └──────┬──────┘
                                                   │
                                            ┌──────▼──────────┐
                                            │  IR ILLUMINATOR │
                                            │  (no photocell) │
                                            │  OR photocell   │
                                            │  covered w/tape │
                                            └─────────────────┘
                                                   │
                                                   │
                                            ┌──────▼──────┐
                                            │     GND     │
                                            └─────────────┘

LOGIC:
  - Pi ON → USB 5V present → Relay 1 closes
  - Relay 1 closed → 12V reaches XH-M131
  - XH-M131 senses darkness → Relay 2 closes
  - Relay 2 closed → 12V reaches IR illuminator
  - Both relays must be closed for IR to receive power
```

---

## Appendix F: References and Further Reading

### Technical Documentation

1. **Numato Lab USB Relay Documentation:** [https://numato.com/docs/nl-usbr-c-001/](https://numato.com/docs/nl-usbr-c-001/)
2. **Tendelux AI4 User Manual:** Included with product, also available on Tendelux website
3. **Raspberry Pi systemd Guide:** [https://www.raspberrypi.org/documentation/linux/usage/systemd.md](https://www.raspberrypi.org/documentation/linux/usage/systemd.md)
4. **Witty Pi 4 Documentation:** [https://www.uugear.com/product/witty-pi-4/](https://www.uugear.com/product/witty-pi-4/)

### Tutorial Resources

5. **SparkFun - Run Program on Startup:** [https://learn.sparkfun.com/tutorials/how-to-run-a-raspberry-pi-program-on-startup/all](https://learn.sparkfun.com/tutorials/how-to-run-a-raspberry-pi-program-on-startup/all)
6. **Grant Trebbin - USB Relay Control:** [https://www.grant-trebbin.com/2015/07/controlling-usb-relay-with-raspberry-pi.html](https://www.grant-trebbin.com/2015/07/controlling-usb-relay-with-raspberry-pi.html)
7. **Electronics For You - IR Illuminator Circuit:** [https://www.electronicsforu.com/electronics-projects/hardware-diy/infrared-illuminator](https://www.electronicsforu.com/electronics-projects/hardware-diy/infrared-illuminator)
8. **ETechnoG - Photocell Sensor Wiring:** [https://www.etechnog.com/2025/05/photocell-sensor-relay-wiring-diagram.html](https://www.etechnog.com/2025/05/photocell-sensor-relay-wiring-diagram.html)

### Product Reviews and Comparisons

9. **Network Camera Tech - Tendelux AI4 Review:** [https://networkcameratech.com/tendelux-ai4-ir-illuminator-review/](https://networkcameratech.com/tendelux-ai4-ir-illuminator-review/)
10. **DSE CCTV - IR Illuminator Guide:** [https://www.dsecctv.com/prod_illuminatori.htm](https://www.dsecctv.com/prod_illuminatori.htm)

### Community Forums

11. **Raspberry Pi Forums - USB Relay Discussion:** [https://forums.raspberrypi.com/viewtopic.php?t=45516](https://forums.raspberrypi.com/viewtopic.php?t=45516)
12. **Raspberry Pi Forums - systemd Services:** [https://forums.raspberrypi.com/viewtopic.php?t=335441](https://forums.raspberrypi.com/viewtopic.php?t=335441)

### Source Citations

This research report includes information from the following sources:

**IR Illuminators:**
- [OHWOAI IR Illuminator Product Page](https://www.ohwoai.net/products/ir-illuminator-850nm-8-led-ir-illuminators-ir-lights-for-security-cameras-10ft-12v-2a-power-supply-ohwoai-long-range-infrared-light-outdoor-ir-floodlight-wide-angle-for-cctv-ip-camera-night-vision)
- [OOSSXX IR Illuminator](https://oossxx.com/products/ir-illuminator-850nm-12-led-ir-illuminators-ir-lights-for-security-cameras-10ft-12v-2a-power-supply-ohwoai-long-range-infrared-light-outdoor-ir-floodlight-wide-angle-for-cctv-ip-camera-night-vision)
- [Amazon - Tendelux AI4](https://www.amazon.com/Tendelux-Illuminator-AI4-Infrared-Security/dp/B075ZYG89D)
- [Tendelux Official Website](https://tendelux.com/products/ai4-ir-illuminator-for-security-cameras-vr-headsets)
- [Walmart IR Illuminator](https://www.walmart.com/ip/IR-Illuminator-8-LED-Long-Range-Outdoor-Use-Infrared-Light-Night-Vision-850nm-12V-Waterproof-floodlight-CCTV-Cameras-IP-Security-Camera/1262566598)

**USB Relay Modules:**
- [Numato Lab 1-Channel USB Relay](https://numato.com/product/1-channel-usb-powered-relay-module/)
- [Numato Lab Documentation](https://numato.com/docs/nl-usbr-c-001/)
- [Amazon - Numato Lab Relay](https://www.amazon.com/Numato-Channel-Powered-Relay-Module/dp/B00MY5I6BO)
- [Yoctopuce PowerRelay-V2](https://www.yoctopuce.com/EN/products/usb-actuators/yocto-powerrelay-v2)
- [DFRobot USB-RLY16L](https://www.dfrobot.com/product-563.html)

**Photocell Relay Modules:**
- [Makerlab Electronics XH-M131](https://www.makerlab-electronics.com/products/12v-xh-m131-light-control-switch-relay-photoresistor-module)
- [Amazon - XH-M131](https://www.amazon.com/Adjustable-photoresistor-Module-Control-Detection/dp/B084JN2YQY)
- [Amazon - Taidacent 2-Channel](https://www.amazon.com/Taidacent-2-Channel-Photosensor-Photocell-Photoelectric/dp/B07RSJMG7D)

**Raspberry Pi and systemd:**
- [SparkFun Learn - Run Programs on Startup](https://learn.sparkfun.com/tutorials/how-to-run-a-raspberry-pi-program-on-startup/all)
- [TheDigitalPictureFrame - systemd Guide](https://www.thedigitalpictureframe.com/ultimate-guide-systemd-autostart-scripts-raspberry-pi/)
- [PragmaticLinux - systemd Startup Script](https://www.pragmaticlinux.com/2020/08/raspberry-pi-startup-script-using-systemd/)
- [Raspberry Pi Forums - systemd service](https://forums.raspberrypi.com/viewtopic.php?t=335441)

**Power Management:**
- [Witty Pi 4 Product Page](https://www.uugear.com/product/witty-pi-4/)
- [Adafruit Witty Pi 4](https://www.adafruit.com/product/5704)
- [Raspberry Pi Spy - Witty Pi Review](https://www.raspberrypi-spy.co.uk/2015/06/witty-pi-a-realtime-clock-and-power-management-for-your-raspberry-pi/)

**Connectors and Wiring:**
- [Amazon - DC Barrel Connectors](https://www.amazon.com/DEMASLED-Connector-Terminal-Adapter-Electronics/dp/B07KX65JLR)
- [US LED Supply - Power Connectors](http://www.usledsupply.com/shop/female-power-connector-12v-screw.html)
- [Super Bright LEDs - CPS Adapter](https://www.superbrightleds.com/cps-x2st-standard-barrel-connector-to-screw-terminal-adapter)

---

**Document Version:** 1.0
**Last Updated:** January 8, 2026
**Author:** Research conducted for OpenRiverCam project
**License:** This research document is provided for project use. Product recommendations are based on publicly available information and do not constitute endorsements.
