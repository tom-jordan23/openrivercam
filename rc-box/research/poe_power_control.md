# PoE Power Control Solutions for Remote Camera Duty Cycling

**Research Date:** 2026-01-05
**Use Case:** Raspberry Pi 5 wakes every 15 minutes, powers on 2 PoE cameras for 2-3 minute capture cycle, then powers off cameras until next cycle.

---

## Executive Summary

**Key Findings:**

1. **Recommended Solution:** Relay-controlled PoE injector offers the best balance of simplicity, reliability, and field-serviceability for humanitarian deployments
2. **Expected Camera Boot Time:** 30-60 seconds typical (allow 60-90 seconds before capture)
3. **Simplest Implementation:** 12V relay module + passive PoE injector + GPIO control from Raspberry Pi
4. **Most Reliable Alternative:** Altronix PoE injectors with built-in voltage-triggered shutdown (no custom electronics)
5. **Budget Range:** $50-200 per solution depending on approach

**Critical Decision Factor:** For non-technical field service, prioritize solutions with pluggable connections (screw terminals) over soldered components or complex network configurations.

---

## Research Questions & Findings

### 1. What are the available PoE power control technologies?

Five primary approaches were identified:

1. **Managed PoE Switches** - Network-based per-port control
2. **PoE Injectors with Control Input** - Purpose-built trigger shutdown
3. **Relay-Switched PoE Injectors** - Simple power switching
4. **Smart PDUs/Network Power Controllers** - Network-based device management
5. **Industrial Automation Relays** - Modbus/Ethernet relay controllers

---

## Solution Analysis

### SOLUTION 1: Managed PoE Switch with API/SNMP Control

**How It Works:**
- Raspberry Pi connects to managed switch via network
- Controls per-port PoE power via SNMP commands, REST API, or web interface
- Cameras connect to switch PoE ports
- Pi sends commands to enable/disable specific ports

**Products Available:**
- **TP-Link Omada TL-SG2006P** (~$80-120): 6-port with Easy Smart management, 4 PoE+ ports, 65W budget
- **Ubiquiti USW-Flex** (~$80-100): 5-port managed, 46W PoE budget, UniFi controller API
- **Alta Labs S8-POE** (~$150): 8-port, 60W budget, Bluetooth setup, mobile app management
- **Netgear GS108PP/GS305EP** (~$100-150): Smart managed switches with web GUI and SNMP

**Control Method:**
```python
# Example SNMP control (pseudo-code)
import pysnmp
# Enable PoE on port 1
snmp_set('switch_ip', 'poe_port_admin_enable_OID', port=1, value=1)
# Disable PoE on port 1
snmp_set('switch_ip', 'poe_port_admin_enable_OID', port=1, value=0)
```

**Integration Complexity:**
- **High**: Requires network stack active on Pi (increases power consumption)
- Pi must stay awake longer to send network commands
- Need to install SNMP libraries or use REST API
- Switch requires configuration and IP address management
- More complex troubleshooting for field staff

**Boot Time Impact:**
- Network initialization: 5-15 seconds
- PoE enable command: 1-3 seconds
- Camera boot: 30-60 seconds
- **Total: 40-80 seconds**

**Reliability Considerations:**
- **Pros:** Industrial-grade switches designed for 24/7 operation, no moving parts (fanless models)
- **Cons:** Network dependency creates failure points, firmware bugs can affect PoE control, IP conflicts in field deployments
- MTBF: Typically 50,000-100,000 hours for quality switches

**Price Range:** $80-200

**Field Serviceability:**
- **Moderate**: Requires understanding of network configuration
- If switch fails, replacement needs IP reconfiguration
- SNMP OIDs vary by manufacturer (vendor lock-in)
- Diagnostic LEDs help identify port issues
- **Rating: 6/10** - Needs semi-technical person

**Pros:**
- Centralized power management for multiple cameras
- Can monitor PoE power consumption per port
- Scalable to more cameras without hardware changes
- Remote management if network available

**Cons:**
- Network overhead increases Pi wake time and power consumption
- More complex configuration and troubleshooting
- Overkill for 2-camera system
- Requires Pi network stack initialization

**Best For:** Deployments with 4+ cameras, existing network infrastructure, technical support available

---

### SOLUTION 2: PoE Injector with Voltage-Triggered Shutdown

**How It Works:**
- PoE injector has dedicated "shutdown" terminals
- Apply 5-24VDC to shutdown terminals to disable PoE output
- Raspberry Pi GPIO (3.3V) triggers transistor to provide 12V shutdown signal
- Completely hardware-based, no software needed

**Products Available:**

**Altronix NetWay Series with Shutdown Trigger:**
- **NetWay1** (~$60-80): Single port, 15W, 24VAC/VDC input, shutdown trigger
- **NetWay1XP** (~$80-100): Single port, PoE/PoE+ 30W, shutdown trigger, includes transformer
- **NetWay8M** (~$200-300): 8-port, 150W total, programmable per-port shutdown, web browser config

**Specifications:**
- Shutdown input: 5-24VDC or 12-24VAC
- Trigger current: <50mA typical
- Power reset time: ~4 seconds after shutdown signal removed
- Operating temperature: 0°C to 49°C (standard models)

**Control Method:**
```python
import RPi.GPIO as GPIO
import time

# Simple GPIO control
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)

# Enable PoE (remove shutdown signal)
GPIO.output(17, GPIO.LOW)
time.sleep(60)  # Wait for camera boot

# Disable PoE (apply shutdown signal via transistor driving 12V)
GPIO.output(17, GPIO.HIGH)
GPIO.cleanup()
```

**Circuit Required:**
```
RPi GPIO 17 → 1kΩ resistor → NPN transistor (2N2222) base
12V supply → Transistor collector → Shutdown+ terminal
GND → Transistor emitter → Shutdown- terminal
```

**Integration Complexity:**
- **Low-Medium**: Requires simple transistor circuit (can be pre-built module)
- Very simple Python GPIO control
- No network dependencies
- Direct hardware control

**Boot Time Impact:**
- GPIO initialization: <1 second
- Transistor switching: <100ms
- PoE power-up: ~4 seconds (per Altronix specs)
- Camera boot: 30-60 seconds
- **Total: 35-65 seconds**

**Reliability Considerations:**
- **Pros:** Purpose-built feature, hardware-based control, proven in security industry
- **Cons:** Requires transistor circuit (additional failure point), limited to Altronix brand
- Transistor circuit is simple and highly reliable if properly designed
- Altronix products designed for security/access control installations

**Price Range:**
- Single port injector: $60-100
- Transistor circuit components: $5-10 (or pre-built module $15-30)
- **Total per camera: $65-130**

**Field Serviceability:**
- **Good**: If using pre-built transistor module with screw terminals
- Injector replacement: plug-and-play (same voltage terminals)
- Clear labeling helps: "12V IN", "SHUTDOWN", "PoE OUT"
- **Rating: 7/10** - Simple if pre-assembled, requires basic DC wiring knowledge

**Pros:**
- Purpose-built solution for this exact use case
- Fast response time (4 second reset)
- No software dependencies beyond GPIO
- Proven reliability in security installations
- Multiple cameras can share shutdown signal with proper circuit design

**Cons:**
- Requires custom transistor circuit (unless pre-built module used)
- Limited to specific brand (Altronix)
- NetWay1 models accept 24VAC/VDC input (need DC-DC converter from 12V battery)
- Some models require AC input (need inverter)

**Best For:** Professional installations where custom circuit board can be designed and tested, deployments with electrical engineering support

---

### SOLUTION 3: Relay Module + Standard PoE Injector (RECOMMENDED)

**How It Works:**
- Standard 12V-to-48V passive PoE injector
- Relay module switches 12V power supply to injector ON/OFF
- Raspberry Pi GPIO controls relay via simple HIGH/LOW signal
- Completely isolates PoE power from control signal

**Products Available:**

**12V-to-48V PoE Injectors:**
- **PoE Texas GPOE-48v10w** (~$35-45): 12-30V input, 48V/10W output, passive PoE
- **Tycon TP-DCDC-1224G** (~$60-80): 12V input, 24V/48V output, gigabit, DIN rail mount
- **AIR802 DC-DC + PoE Injector** (~$50-70): 10-26VDC input, 48V output, DIN rail, made in USA
- **Telco Antennas 12V-48V Injector** (~$40-60): Passive PoE Mode B, dual redundant inputs

**Relay Modules (Field-Serviceable, No Soldering):**
- **Digital Loggers IoT Relay** (~$30): SPDT 30A relay, 3-60VDC control input, screw terminals
- **SainSmart 4-Channel 12V Relay** (~$15): Opto-isolated, USB + GPIO control, screw terminals
- **Denkovi 10-Channel 12V Board** (~$40): 3-30V logic control, screw terminals, DIN rail
- **JemRF 1-Channel 5V Relay** (~$10): Ultra-simple, 2.5-12V input, no soldering required

**For Rugged Field Deployment:**
- **Waveshare Relay HAT** (~$25-35): 8 relays, screw terminals, configurable pins, ARK connectors
- **Power + Relay HAT (Pi Hut)** (~$30-40): 2x 10A relays, 7-16V DC input, integrated power supply

**System Architecture:**
```
12V Battery → Relay COM/NO terminals → PoE Injector 12V input → PoE to camera
              ↑
              Relay coil controlled by Pi GPIO (via optoisolator on module)
              ↑
Raspberry Pi GPIO 17 → Relay IN1 (triggers relay)
```

**Control Method:**
```python
#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

# Configuration
RELAY_PIN = 17  # BCM pin 17 (physical pin 11)
CAMERA_BOOT_TIME = 60  # seconds

def setup_relay():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RELAY_PIN, GPIO.OUT)
    GPIO.output(RELAY_PIN, GPIO.LOW)  # Cameras OFF initially

def power_on_cameras():
    print("Powering ON cameras...")
    GPIO.output(RELAY_PIN, GPIO.HIGH)  # Relay ON
    print(f"Waiting {CAMERA_BOOT_TIME}s for camera boot...")
    time.sleep(CAMERA_BOOT_TIME)

def power_off_cameras():
    print("Powering OFF cameras...")
    GPIO.output(RELAY_PIN, GPIO.LOW)  # Relay OFF

def cleanup():
    GPIO.cleanup()

# Main duty cycle
try:
    setup_relay()
    power_on_cameras()

    # Camera capture happens here (2-3 minutes)
    print("Cameras ready for capture")
    time.sleep(180)  # Capture window

    power_off_cameras()
    cleanup()
    print("Duty cycle complete")

except KeyboardInterrupt:
    print("Interrupted by user")
    cleanup()
```

**Integration Complexity:**
- **Very Low**: Standard RPi.GPIO library (pre-installed on Raspberry Pi OS)
- Simple 3-wire connection: GPIO, GND, and relay module
- Most relay modules have opto-isolation (protects Pi from voltage spikes)
- No custom circuits or PCBs needed

**Wiring Guide for Field Staff:**
```
Raspberry Pi → Relay Module
  GPIO 17 (Pin 11) → IN1
  GND (Pin 39)     → GND

Battery → Relay Module
  12V+ → VCC (relay coil power)

PoE Injector Power:
  Battery 12V+ → Relay COM
  Relay NO     → PoE Injector 12V+
  Battery GND  → PoE Injector GND

PoE Injector Network:
  Data IN  ← Switch/Network
  Data+PoE OUT → Camera
```

**Boot Time Impact:**
- GPIO initialization: <1 second
- Relay switching: ~10ms
- PoE injector stabilization: 2-5 seconds
- Camera boot: 30-60 seconds
- **Total: 33-66 seconds**

**Reliability Considerations:**
- **Pros:**
  - Mechanical relays: 100,000-400,000 switching cycles (Digital Loggers IoT: 400k at 12A)
  - Complete electrical isolation between control and power
  - Easy to diagnose (relay click audible, LED indicators)
  - Time-tested technology
- **Cons:**
  - Moving parts (relay contacts wear over time)
  - Inrush current from PoE injector capacitors (use relay rated >2A)
- Expected lifetime: 10+ years at 35,000 cycles/year (96 cycles/day)

**Price Range:**
- PoE Injector: $35-80
- Relay Module: $10-40
- Jumper wires: $5
- **Total per camera: $50-125** (can share relay for 2 cameras with 2-channel module)

**Field Serviceability:**
- **Excellent**: All connections via screw terminals or dupont connectors
- Color-coded wires can be used
- Clear labeling: "Battery+", "To PoE Injector", "From Pi GPIO"
- Visual indicators: Most relay modules have LED per channel
- Audible feedback: Relay "click" confirms switching
- Modular replacement: Each component swappable independently
- **Rating: 9/10** - Can be serviced by anyone who can use a screwdriver

**Pros:**
- Simplest possible implementation
- Completely hardware-based switching
- No network dependencies
- Highly reliable mechanical isolation
- Audible/visual feedback for troubleshooting
- Works with ANY PoE injector (not vendor-locked)
- Can use solid-state relay (SSR) for silent, unlimited-life operation
- Cheapest option for 2-camera setup
- Pre-made relay HATs available (plug directly onto Pi GPIO)

**Cons:**
- Requires physical relay module (small additional hardware)
- Relay contacts have finite lifespan (mitigated by proper sizing)
- Slight power draw for relay coil (~70-100mA at 12V = 1.2W)

**Best For:** Field deployments requiring maximum simplicity, reliability, and serviceability by non-technical staff

**Variations:**

**Option A: Solid State Relay (SSR) for Extended Life**
- **RPi PoE & SSR Board** (~$30-40): Combines PoE power for Pi + SSR control
- **CTRL HAT** (~$40-60): Professional SSR module, supports up to 30V control
- No moving parts, unlimited switching cycles
- Silent operation (no relay click)
- Faster switching (<1ms vs 10ms)

**Option B: Pre-Built Relay HAT (Easiest)**
- **Waveshare Relay HAT** (~$30): Plug directly onto Pi GPIO, 8 relay channels
- No wiring needed (other than power connections)
- Screw terminals for PoE injector connections
- Can control 8 cameras with single HAT

---

### SOLUTION 4: Smart PDU / Network Power Controller

**How It Works:**
- Networkable power distribution unit with individually controlled outlets
- Raspberry Pi sends HTTP/TCP commands to enable/disable outlets
- PoE injectors plugged into controlled outlets
- Can power-cycle remotely via network or cloud

**Products Available:**
- **Dataprobe iBoot-PoE** (~$200-250): PoE pass-through with auto-reboot, cloud control, API
- **Digital Loggers Web Power Switch** (~$100-150): 4-8 outlets, REST API, MQTT, Amazon Echo
- **CyberPower Switched PDU** (~$200-400): Rack-mount, SNMP, per-outlet control
- **Domotz Platform** (subscription): Manages PoE switches/PDUs, cloud-based control

**Control Method:**
```python
import requests

# Digital Loggers Web Power Switch example
def control_outlet(outlet_num, state):
    # state: 'on', 'off', or 'ccl' (cycle)
    url = f"http://192.168.1.100/outlet?{outlet_num}={state}"
    auth = ('admin', 'password')
    response = requests.get(url, auth=auth)
    return response.status_code == 200

# Power on cameras
control_outlet(1, 'on')
time.sleep(60)  # Camera boot

# Power off cameras
control_outlet(1, 'off')
```

**Integration Complexity:**
- **Medium-High**: Requires network initialization on Pi
- HTTP/REST API relatively simple
- Network configuration required (IP addresses, credentials)
- More power consumption (Pi network stack must stay active)

**Boot Time Impact:**
- Network initialization: 5-15 seconds
- HTTP request: 1-3 seconds
- Outlet switching: 1-2 seconds
- PoE injector stabilization: 2-5 seconds
- Camera boot: 30-60 seconds
- **Total: 40-85 seconds**

**Reliability Considerations:**
- **Pros:**
  - Enterprise-grade products designed for remote management
  - Watchdog features (auto-reboot on ping failure)
  - Dataprobe iBoot-PoE specifically designed for PoE camera management
- **Cons:**
  - Network dependency (IP conflicts, cable issues)
  - More complex failure modes
  - Firmware updates required
- **iBoot-PoE specific:** Monitors bandwidth, auto-reboots on communication failure

**Price Range:** $100-250 per unit (controls multiple cameras)

**Field Serviceability:**
- **Moderate**: Requires network knowledge for troubleshooting
- Web interface helps diagnostics
- IP address must be documented
- Factory reset procedures needed for failed configs
- **Rating: 6/10** - Needs someone comfortable with network devices

**Pros:**
- Professional remote management features
- Watchdog/auto-recovery capabilities (iBoot-PoE)
- Can control multiple devices
- Web interface for manual control
- Detailed logging and monitoring
- Cloud control options available (iBoot-PoE)

**Cons:**
- Expensive for 2-camera deployment
- Network overhead and complexity
- Requires IP network configuration
- Overkill for simple duty-cycle application
- Network stack increases Pi power consumption

**Best For:** Installations with existing network infrastructure, multiple devices to manage, requirement for remote cloud-based management

---

### SOLUTION 5: Industrial Ethernet Relay Controller

**How It Works:**
- Industrial relay modules with Ethernet/PoE power
- Modbus TCP, HTTP, or custom protocols for control
- Often DIN-rail mountable for professional installations
- Can be powered by PoE and control other PoE devices

**Products Available:**
- **DFRobot 8-Channel Ethernet Relay** (~$120-150): PoE powered, HTTP/Modbus control
- **Numato Lab 16-Channel PoE Relay** (~$150-200): PoE powered, ASCII commands over TCP
- **ControlByWeb WebRelay** (~$150-200): 1 relay, cellular/WiFi/Ethernet, 9-28VDC or PoE, REST API
- **8-Channel Ethernet Relay Module (Pi Hut)** (~$100-130): PoE support, Modbus RTU/TCP

**Control Method:**
```python
import socket

# Numato Lab ASCII command example
def control_relay(ip, relay_num, state):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, 23))  # Telnet port

    if state:
        command = f"relay on {relay_num}\r"
    else:
        command = f"relay off {relay_num}\r"

    sock.send(command.encode())
    sock.close()

control_relay('192.168.1.50', 0, True)  # Turn on relay 0
```

**Integration Complexity:**
- **Medium**: Network required, but simpler protocols than SNMP
- TCP socket programming straightforward
- Some models offer HTTP REST API
- Modbus requires additional libraries

**Boot Time Impact:**
- Network initialization: 5-15 seconds
- TCP connection: 1-2 seconds
- Relay switching: <100ms
- PoE injector stabilization: 2-5 seconds
- Camera boot: 30-60 seconds
- **Total: 38-82 seconds**

**Reliability Considerations:**
- **Pros:**
  - Industrial-grade components
  - Wide temperature ranges (-40°C to 75°C common)
  - DIN-rail mounting for vibration resistance
  - Designed for 24/7 operation
- **Cons:**
  - Network dependency
  - More expensive than simple relay modules
- MTBF: Typically 50,000+ hours

**Price Range:** $100-200 per controller (8-16 channels)

**Field Serviceability:**
- **Moderate**: DIN-rail mounting professional but accessible
- Network configuration required
- Web interface on some models
- **Rating: 7/10** - Good for electricians, challenging for general field staff

**Pros:**
- Industrial ruggedness
- Multiple control channels
- Professional mounting options (DIN-rail)
- Wide temperature tolerance
- Can be PoE-powered (one less power supply)
- Scalable to many relays/devices

**Cons:**
- Expensive for 2-camera application
- Network complexity and power overhead
- Modbus protocol learning curve
- Requires Ethernet infrastructure

**Best For:** Professional installations, harsh environments, scalable deployments (10+ cameras), integration with existing industrial control systems

---

## Comparative Summary Table

| Solution | Complexity | Boot Time | Reliability | Price/2cam | Serviceability | Network Req'd |
|----------|-----------|-----------|-------------|------------|----------------|---------------|
| **Managed PoE Switch** | High | 40-80s | High | $80-200 | Moderate (6/10) | Yes |
| **Altronix Shutdown** | Low-Med | 35-65s | High | $130-200 | Good (7/10) | No |
| **Relay + Injector** | Very Low | 33-66s | High | $50-125 | Excellent (9/10) | No |
| **Smart PDU** | Med-High | 40-85s | Medium-High | $100-250 | Moderate (6/10) | Yes |
| **Industrial Relay** | Medium | 38-82s | Very High | $150-300 | Good (7/10) | Yes |

---

## Detailed Camera Boot Time Analysis

Based on field reports and manufacturer data:

**Typical IP Camera PoE Boot Sequence:**
1. PoE power applied: 0s
2. PoE negotiation (802.3af/at): 0-3s
3. Hardware initialization: 3-15s
4. Bootloader: 15-25s
5. Linux kernel boot: 25-45s
6. Camera application start: 45-60s
7. Network services ready: 60-90s

**Recommendations:**
- **Minimum wait time:** 60 seconds
- **Conservative wait time:** 90 seconds (recommended for field reliability)
- **Factors that increase boot time:**
  - PoE+ cameras (higher power, more features): +10-15s
  - PTZ cameras: +15-30s
  - Cameras with IR illumination: +5-10s
  - Cold temperatures: +10-20s

**Optimization Strategies:**
- Use DHCP with reserved IP addresses (faster than static config)
- Disable unused camera features (analytics, multi-stream)
- Use cameras with "quick boot" modes if available

---

## Recommendations for Humanitarian Field Deployment

### PRIMARY RECOMMENDATION: Relay Module + PoE Injector

**Reasoning:**
1. **Simplicity:** Only 3 wires from Pi to relay (GPIO, GND, optional VCC)
2. **Reliability:** Mechanical relays proven over decades, 100k+ cycle lifetime
3. **Serviceability:** Screw terminals, color-coded wires, visual LED indicators
4. **Cost-Effective:** $50-100 total for complete solution
5. **No Network Dependency:** Reduces complexity and power consumption
6. **Field-Testable:** Relay "click" provides audible confirmation
7. **Flexibility:** Works with any PoE injector (not vendor-locked)

**Recommended Bill of Materials (per 2-camera system):**

| Component | Product | Price | Notes |
|-----------|---------|-------|-------|
| Relay Module | Waveshare Relay HAT or SainSmart 2-Channel 12V | $15-35 | Screw terminals, LED indicators |
| PoE Injector #1 | PoE Texas GPOE-48v10w | $35-45 | 12V input, passive PoE |
| PoE Injector #2 | PoE Texas GPOE-48v10w | $35-45 | Second camera |
| Jumper Wires | Dupont female-female (if not using HAT) | $5 | GPIO connections |
| Wire | 18AWG stranded, red/black | $10 | 12V power distribution |
| Labels | Brady/DYMO label maker labels | $5 | Wire identification |
| **TOTAL** | | **$105-145** | Complete 2-camera solution |

**Pre-Deployment Preparation:**
1. Assemble and test complete system
2. Create laminated wiring diagram with photos
3. Label all wires with source and destination
4. Pre-configure Pi GPIO script with tested timing values
5. Include spare relay module and PoE injector in field kit

**Field Service Manual (1-page quick reference):**
```
CAMERA POWER TROUBLESHOOTING

1. Check relay module LED:
   - LED ON when cameras should be powered
   - LED OFF when cameras should be off
   - If LED doesn't change: Check Pi GPIO connection

2. Listen for relay click:
   - Should hear "click" when cameras power on/off
   - No click = bad relay (replace module)

3. Check PoE injector:
   - Green LED = power output active
   - Check 12V input terminals with multimeter
   - If no 12V: Check relay output terminals

4. Replacement procedure:
   - Power off entire system
   - Photo document wire connections
   - Remove wire from screw terminal (turn counter-clockwise)
   - Install new component
   - Reconnect wires matching photo
   - Power on and test

WIRING:
Pi GPIO 17 (Pin 11) → Relay IN1
Pi GND (Pin 39) → Relay GND
Battery 12V+ → Relay COM (or VCC)
Relay NO → PoE Injector 12V+
Battery GND → PoE Injector GND
```

---

### ALTERNATIVE RECOMMENDATION: Altronix NetWay1XP (If Engineering Support Available)

**When to choose this:**
- Engineering team can design and test transistor circuit
- Need integrated solution with fewer separate components
- Willing to commit to Altronix vendor
- Professional installation planned

**Recommended Implementation:**
- Design custom PCB with transistor circuit, screw terminals, and status LEDs
- Test extensively before field deployment
- Include pre-built spare PCB in field kit
- Requires 24VAC/VDC input (use DC-DC converter from 12V battery)

**Bill of Materials:**

| Component | Product | Price | Notes |
|-----------|---------|-------|-------|
| PoE Injector | Altronix NetWay1XP | $80-100 | Built-in shutdown trigger |
| DC-DC Converter | 12V to 24V, 2A | $15-25 | For Altronix 24V input |
| Transistor Circuit | Custom PCB or module | $20-40 | 2N2222, resistors, screw terminals |
| **TOTAL** | | **$115-165** | Per camera |

---

### NOT RECOMMENDED for This Use Case:

**Managed PoE Switch:**
- Overkill for 2 cameras
- Network complexity increases failure modes
- Higher power consumption (Pi network stack must stay active longer)
- More difficult field troubleshooting

**Smart PDU/iBoot-PoE:**
- Expensive for 2-camera system
- Network dependency adds complexity
- Best for 24/7 monitoring with cloud management (not scheduled duty cycle)

**Industrial Ethernet Relay:**
- Unnecessary cost and complexity
- Network overhead
- Better suited for large-scale deployments

---

## Implementation Code Example

**Complete Python script for relay-controlled PoE cameras:**

```python
#!/usr/bin/env python3
"""
PoE Camera Power Control for Duty Cycle Operation
Raspberry Pi 5 + Relay Module + PoE Injectors

Hardware:
- Relay module connected to GPIO 17 (BCM)
- 2x PoE injectors powered through relay
- 2x IP cameras connected via PoE

Timing:
- Wake every 15 minutes (controlled by external RTC or cron)
- Power on cameras: 0s
- Camera boot: 60-90s
- Capture window: 120-180s
- Power off cameras
- Shutdown Pi
"""

import RPi.GPIO as GPIO
import time
import logging
import sys
from datetime import datetime

# Configuration
RELAY_GPIO = 17  # BCM pin numbering
CAMERA_BOOT_TIME = 75  # seconds (conservative estimate)
CAPTURE_DURATION = 180  # seconds (3 minutes)
LOG_FILE = '/var/log/poe_camera_control.log'

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)

class PoECameraController:
    def __init__(self, relay_pin=RELAY_GPIO):
        self.relay_pin = relay_pin
        self.setup_gpio()

    def setup_gpio(self):
        """Initialize GPIO for relay control"""
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.relay_pin, GPIO.OUT, initial=GPIO.LOW)
        logging.info(f"GPIO {self.relay_pin} initialized for relay control")

    def power_on(self):
        """Power on cameras via relay"""
        logging.info("Powering ON cameras (relay activated)")
        GPIO.output(self.relay_pin, GPIO.HIGH)

    def power_off(self):
        """Power off cameras via relay"""
        logging.info("Powering OFF cameras (relay deactivated)")
        GPIO.output(self.relay_pin, GPIO.LOW)

    def wait_for_boot(self):
        """Wait for cameras to complete boot sequence"""
        logging.info(f"Waiting {CAMERA_BOOT_TIME}s for camera boot...")
        for i in range(CAMERA_BOOT_TIME):
            if i % 10 == 0:
                logging.debug(f"Boot progress: {i}/{CAMERA_BOOT_TIME}s")
            time.sleep(1)
        logging.info("Camera boot complete - ready for capture")

    def cleanup(self):
        """Clean up GPIO resources"""
        GPIO.cleanup()
        logging.info("GPIO cleanup complete")

def main():
    """Main duty cycle execution"""
    logging.info("="*60)
    logging.info(f"Camera duty cycle started at {datetime.now()}")

    controller = PoECameraController()

    try:
        # Step 1: Power on cameras
        controller.power_on()

        # Step 2: Wait for camera boot
        controller.wait_for_boot()

        # Step 3: Capture window (your capture script runs here)
        logging.info(f"Capture window: {CAPTURE_DURATION}s")
        logging.info(">>> START YOUR CAMERA CAPTURE SCRIPT HERE <<<")

        # Example: call your capture script
        # import subprocess
        # subprocess.run(['/usr/local/bin/capture_script.sh'])

        time.sleep(CAPTURE_DURATION)

        logging.info("Capture window complete")

        # Step 4: Power off cameras
        controller.power_off()

        logging.info("Duty cycle complete - ready for shutdown")
        logging.info("="*60)

    except KeyboardInterrupt:
        logging.warning("Duty cycle interrupted by user")
        controller.power_off()

    except Exception as e:
        logging.error(f"Error during duty cycle: {str(e)}", exc_info=True)
        controller.power_off()

    finally:
        controller.cleanup()

if __name__ == "__main__":
    main()
```

**Systemd service for automatic execution:**

```ini
# /etc/systemd/system/poe-camera-control.service
[Unit]
Description=PoE Camera Power Control
After=multi-user.target

[Service]
Type=oneshot
ExecStart=/usr/bin/python3 /home/pi/poe_camera_control.py
User=pi
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

**Cron job for 15-minute intervals:**

```bash
# Edit with: crontab -e
# Run every 15 minutes
*/15 * * * * /usr/bin/python3 /home/pi/poe_camera_control.py
```

---

## Additional Considerations

### Power Budget Analysis

**Per Duty Cycle (15 minutes):**
- Raspberry Pi 5 active: 3-5W × 5 min = 0.25-0.42 Wh
- Relay module: 1-2W × 5 min = 0.08-0.17 Wh
- PoE Injectors: 1W (idle) × 3 min + 10W (active) × 3 min = 0.55 Wh
- IP Cameras: 5W × 2 cameras × 3 min = 0.5 Wh
- **Total per cycle: ~1.4-1.7 Wh**
- **Daily (96 cycles): ~134-163 Wh**

### Temperature Considerations

**Operating Ranges:**
- Raspberry Pi 5: 0°C to 50°C (throttles at 80°C)
- Relay modules: -10°C to 70°C (typical)
- PoE Injectors:
  - Standard: 0°C to 50°C
  - Industrial: -40°C to 75°C
- IP Cameras: -30°C to 60°C (outdoor rated)

**Recommendations:**
- Use industrial-grade PoE injectors for extreme environments
- Insulated enclosure with passive cooling for moderate climates
- Active heating for sub-zero deployments (increases power budget)

### Failure Mode Analysis

| Component | Failure Mode | Impact | Detection | Recovery |
|-----------|--------------|--------|-----------|----------|
| Relay Module | Contacts weld closed | Cameras always powered | No relay click, high power consumption | Replace relay module |
| Relay Module | Coil open circuit | Cameras never power on | No relay click, no LED | Replace relay module |
| PoE Injector | No output | One camera offline | Camera not visible | Replace injector |
| GPIO Connection | Wire disconnected | No relay control | Relay doesn't click | Check/reconnect wire |
| Camera | Won't boot | No video | Check network ping | Power cycle, replace |
| Raspberry Pi | Software crash | Missed duty cycle | Check logs | Watchdog timer, auto-reboot |

**Reliability Improvements:**
- Watchdog timer on Pi (auto-reboot if hung)
- Dual relay channels (redundancy)
- LED indicators for each stage (power, relay, PoE)
- Log all state changes to SD card for diagnostics

---

## Bill of Materials Summary

### Recommended Solution: Relay + PoE Injector

**Option A: Pre-Built HAT (Easiest Field Service)**
- Waveshare Relay HAT: $30-35
- 2× PoE Texas GPOE-48v10w: $70-90
- Wire and labels: $10
- **Total: $110-135**

**Option B: Modular Relay (Most Flexible)**
- SainSmart 2-Channel 12V Relay: $15
- 2× PoE Texas GPOE-48v10w: $70-90
- Jumper wires: $5
- Wire and labels: $10
- **Total: $100-120**

**Option C: Industrial Rugged (Harsh Environments)**
- Digital Loggers IoT Relay: $30
- 2× Tycon TP-DCDC-1224G: $120-160
- DIN rail and enclosure: $30
- Wire and labels: $10
- **Total: $190-230**

---

## Sources & References

### Managed PoE Switches & Network Control
- [Pi PoE Switch HAT GPIO Pinout](https://pinout.xyz/pinout/pi_poe_switch_hat)
- [Waveshare PoE HAT for Raspberry Pi 5](https://www.jeffgeerling.com/blog/2024/waveshares-poe-hat-first-raspberry-pi-5/)
- [NETGEAR SNMP PoE Port Control](https://community.netgear.com/discussions/business-managed-switches/m4250-poe-control-via-snmp/2332670)
- [TP-Link SNMP Switch Management](https://www.tp-link.com/us/configuration-guides/key_points_of_managing_the_switch_via_snmp/)
- [Domotz Remote PoE Power Cycling](https://www.domotz.com/features/remote-power-management.php)

### PoE Injectors with Control Input
- [IPVM Discussion: PoE Injector with Trigger](https://ipvm.com/forums/video-surveillance/topics/poe-injector-with-trigger-in-to-turn-poe-on-off)
- [Dataprobe iBoot-PoE Product Page](https://www.dataprobe.com/products/iboot-poe)
- [Digital Loggers Gigabit Midspan Injector User Guide](http://www.digital-loggers.com/gpoeman.pdf)

### Relay Control Solutions
- [Digital Loggers IoT Power Relay](https://www.digital-loggers.com/iot2.html)
- [DFRobot 8-Channel Ethernet Relay Controller](https://www.dfrobot.com/product-1218.html)
- [ControlByWeb WebRelay](https://controlbyweb.com/webrelay/)
- [Numato Lab PoE Relay Modules](https://numato.com/product-category/automation/relay-modules/power-over-ethernet-relay/)

### 12V to 48V PoE Converters
- [PoE Texas GPOE-48v10w](https://shop.poetexas.com/products/wt-gpoe-48v10w)
- [Telco Antennas 12V-48V PoE Injector](https://www.telcoantennas.com.au/12vdc-to-48vdc-poe-passive-power-over-ethernet-inj)
- [AIR802 DC-DC Converter + PoE Injector](https://www.air802.com/dc-dc-converter-poe-injector-adapter-with-10-26vdc-input-48vdc-poe-output-din-rail-mount.html)
- [Tycon Systems PoE Solar Charge Controllers](https://www.tyconsystems.com/articles/post/new-product-spotlight-tycon-systems-poe-solar-charge-controllers-now-available)

### Field Deployment & Reliability
- [Allied Telesis Remote Power Cycle](https://www.alliedtelesis.com/us/en/about/technology/remote-power-cycle)
- [Phihong Outdoor PoE Injector Guide](https://www.phihong.com/outdoor-poe-injector-understanding-poe-ratings-for-ensuring-reliable-poe-systems/)
- [Industrial PoE Temperature Requirements](https://www.procetpoe.com/product-news/poeinjector.html)
- [TRENDnet Outdoor IP67 PoE Injector](https://www.trendnet.com/store/products/outdoor-poeplusplus-injector/outdoor-ip67-gigabit-poeplusplus-injector-24-60V-TI-O119GI-v1)

### Raspberry Pi GPIO & Relay Control
- [Opensource.com: Control GPIO and Relays](https://opensource.com/article/17/3/operate-relays-control-gpio-pins-raspberry-pi)
- [howchoo: Relay with Raspberry Pi](https://howchoo.com/pi/how-to-use-a-relay-with-a-raspberry-pi)
- [GitHub: Python Relay Control Script](https://gist.github.com/elktros/e98d4410fcb0fcfe279e0f8ad6cd9c3c)
- [Raspberry Pi Guide: Control Electronics with Relay](https://raspberrypi-guide.github.io/electronics/control-electronics-with-a-relay)

### Camera Boot Times & PoE Specifications
- [Surveillance Guides: IP Camera Installation with PoE](https://surveillanceguides.com/how-to-install-ip-camera-with-nvr-and-poe-switch-a-complete-guide/)
- [IPVM: Camera Troubleshooting Tips](https://ipvm.com/reports/top-10-camera-troubleshooting-tips)
- [Hanwha Vision: PoE Power Cycling Cameras](https://support.hanwhavisionamerica.com/hc/en-us/articles/40014497885595-HealthPro-PoE-Power-Cycling-Cameras-via-an-Allied-Telesis-Network-Switch)

### Rugged Hardware Solutions
- [Hackaday: Ruggedized Raspberry Pi for Sailors](https://hackaday.com/2025/09/20/a-ruggedized-raspberry-pi-for-sailors/)
- [Waveshare Relay HAT](https://www.waveshare.com/product/raspberry-pi/hats/motors-relays.htm)
- [The Pi Hut Power + Relay HAT](https://thepihut.com/products/raspberry-pi-power-relay-hat)

---

**Document Version:** 1.0
**Last Updated:** 2026-01-05
**Author:** Research compiled for OpenRiverCam RC-Box project
**Next Review:** Before field deployment pilot
