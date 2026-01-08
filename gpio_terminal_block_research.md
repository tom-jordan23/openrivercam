# GPIO Terminal Block Riser/HAT Research for Raspberry Pi 5 + Witty Pi 4 Stack

**Research Date:** January 7, 2026
**Configuration:** Raspberry Pi 5 → Witty Pi 4 → GPIO Terminal Block HAT

---

## Executive Summary

**Key Findings:**

1. **True stackable GPIO screw terminal HATs exist** - Several manufacturers offer GPIO screw terminal boards with pass-through headers that can stack on top of other HATs like the Witty Pi 4.

2. **Top Recommendation: Adafruit Pi-EzConnect (ID 2711)** - This is the most robust stackable option with extended header pins specifically designed for stacking, overvoltage protection, and full Pi 5 compatibility.

3. **Budget Alternative: 52Pi/The Pi Hut GPIO Screw Terminal HAT (EP-0129)** - More affordable option with male pass-through header, though may require additional GPIO risers for reliable stacking.

4. **Critical Compatibility Note:** While Witty Pi 4 works with Pi 5, the manufacturer now recommends Witty Pi 5 HAT+ for Pi 5 configurations. This may affect long-term reliability and should be considered.

5. **Alternative Approach:** Ribbon cable breakout boards offer a cleaner solution when stacking becomes problematic, allowing off-Pi mounting of screw terminals.

---

## Research Questions & Findings

### 1. Does a stackable GPIO screw terminal HAT exist?

**Answer: YES** - Multiple products exist that combine screw terminal GPIO breakouts with stackable/pass-through capabilities.

The key requirement is a board with:
- 40-pin female header on bottom (connects to Witty Pi 4's pass-through)
- Screw terminals for GPIO access
- Male header on top OR extended female headers for future expansion

---

## Specific Product Recommendations

### OPTION 1: Adafruit Pi-EzConnect Terminal Block Breakout HAT (RECOMMENDED)

**Product Details:**
- **Part Number:** Adafruit ID 2711
- **Price:** $19.95 USD (as of January 2026)
- **Availability:** In stock at Adafruit, also available from The Pi Hut, PiShop.us, Newark, Amazon

**Key Features:**
- **Stackable Design:** "Extended header pins allow other HATs to be stacked to Pi-EzConnect without any loss of functionality"
- **Protection:** Resettable 8V, 1.6A fuse for 3.3V and 5V power rails
- **Full Documentation:** Fully documented pins - easily connect to pin numbers or GPIO numbers without external charts
- **Pi 5 Compatible:** Explicitly listed as compatible with Pi 5, Pi 4, Pi 3, Pi 2, Model B+, and Model A+
- **Screw Terminals:** All GPIO pins available via screw terminals
- **Additional Connectivity:** Header connections can use 0.1" (2.54mm) spaced headers, male or female

**Dimensions:** 68.8mm x 56.6mm x 23.3mm (2.7" x 2.2" x 0.9")

**Why This is the Top Choice:**
1. Explicitly designed for stacking with extended headers
2. Built-in overvoltage protection critical for field deployments
3. Official Pi 5 support confirmed
4. Well-documented by reputable manufacturer (Alchemy Power Inc. via Adafruit)
5. Available from multiple trusted retailers

**Retailers:**
- Adafruit: https://www.adafruit.com/product/2711
- The Pi Hut: https://thepihut.com/products/pi-ezconnect-terminal-block-breakout-hat
- PiShop.us: https://www.pishop.us/product/pi-ezconnect-terminal-block-breakout-hat/
- Amazon: Search "Alchemy Power Pi-EzConnect"

---

### OPTION 2: 52Pi / The Pi Hut GPIO Screw Terminal HAT

**Product Details:**
- **Part Number:** 52Pi EP-0129
- **Price:** £13 (The Pi Hut) / $14.44 USD (52Pi direct)
- **Availability:** The Pi Hut, 52Pi Store, Micro Center, RobotShop

**Key Features:**
- **Stackable:** "Pre-soldered with upper male GPIO section enabling jumper wire usage or additional HAT fitting (may require GPIO riser)"
- **LED Status Indicators:** Color-coded LEDs for each GPIO pin
  - 5V power pins: Red
  - 3.3V power pins: Pink
  - Special function pins: Dark blue
  - Regular GPIO pins: Light blue
- **Labels:** Pin information on top of terminal and on the side
- **Compatibility:** Listed for Pi 4B, 3B+, 3B, 2B, B+, Zero, Zero W (Pi 5 not explicitly mentioned)

**Technical Specifications:**
- Terminal block pitch: 2.54mm/0.1"
- Wire size range: 28AWG to 18AWG
- Strip length: 4.5mm
- PCB: FR-4 fiber glass, dual copper layers
- 2x20 positions header

**Package Includes:**
- 1x GPIO Screw Terminal Hat
- 4x M2.5 Copper pillars
- 4x M2.5 Screws
- 1x Screwdriver
- 1x GPIO pinout reference tape

**Considerations:**
- Pi 5 compatibility not explicitly stated (though 40-pin header should work)
- May require additional GPIO riser for reliable stacking
- No built-in overvoltage protection mentioned
- More budget-friendly option

**Retailers:**
- The Pi Hut: https://thepihut.com/products/gpio-screw-terminal-hat
- 52Pi Store: https://52pi.com/products/52pi-gpio-screw-terminal-hat-for-raspberry-pi
- Micro Center (in-store/online)
- RobotShop: https://www.robotshop.com/products/52pi-gpio-screw-terminal-hat-raspberry-pi

---

### OPTION 3: Seeed Studio GPIO Screw Terminal HAT

**Product Details:**
- **Part Number:** Product #4808 / SKU 114992565
- **Price:** Not found in research (check Seeed Studio website)
- **Availability:** Seeed Studio, The Pi Hut, Fab.to.Lab (India)

**Key Features:**
- "Pre-soldered with upper male GPIO section enabling jumper wire usage or additional HAT fitting"
- Compatible with all 40-pin Raspberry Pi boards
- No soldering required
- Stackable design

**Considerations:**
- Less detailed documentation available
- Pricing information not readily available
- Similar to 52Pi option but less information on Pi 5 compatibility

**Retailers:**
- Seeed Studio: https://www.seeedstudio.com/GPIO-Screw-Terminal-Hat-for-Raspberry-Pi-p-4808.html
- The Pi Hut (may stock this variant)
- Fab.to.Lab: https://www.fabtolab.com/ (India)

---

### OPTION 4: Geekworm G470 GPIO Test Terminal Block Breakout HAT

**Product Details:**
- **Part Number:** Geekworm G470
- **Price:** Not specified in research
- **Availability:** Geekworm.com, Central Computer

**Key Features:**
- All 40 GPIO pins available through labeled screw terminals
- Pi 5 compatible (explicitly listed: "Pi 5, Pi 4B, Pi 3B, 3B+")
- Clear labeling to avoid wiring errors
- Sturdy screw terminals for long-term reliability

**Considerations:**
- **Stackability NOT confirmed** in product documentation
- May not have pass-through headers
- Best suited as top-most HAT in stack

**Retailers:**
- Geekworm: https://geekworm.com/products/g470
- Central Computer: https://www.centralcomputer.com/

---

## Products That DON'T Meet Requirements

### Adafruit Pi T-Cobbler Plus (ID 2028)
- **Why it doesn't work:** This is a BREADBOARD breakout, not a stackable HAT
- **Design:** Uses 40-pin ribbon cable to connect Pi to a breadboard-mounted breakout
- **Price:** Various (check Adafruit)
- **Note:** Does NOT have screw terminals, only breadboard pins

### SparkFun Pi Wedge
- **Why it doesn't work:** Also a breadboard/ribbon cable breakout, not a stackable HAT
- **Design:** Connects via ribbon cable
- **Note:** Some versions have screw terminals, but not in stackable HAT format

### Pimoroni Breakout Garden HAT
- **Why it doesn't work:** Designed for Pimoroni's proprietary breakout boards with edge connectors
- **Design:** 6 slots for I2C/SPI breakout boards, not general-purpose GPIO screw terminals
- **Price:** ~$20-25 USD
- **Note:** While stackable, it doesn't provide screw terminal access to all GPIO pins

### ModMyPi GPIO Breakout Products
- **Status:** DISCONTINUED
- **Note:** ModMyPi Paddle Breakout Kit and Prototyping Plate are no longer available

---

## Critical Compatibility Considerations

### Raspberry Pi 5 + Witty Pi 4 Stack

**Important Finding:** While Witty Pi 4 is compatible with Pi 5, the manufacturer (UUGear) now offers **Witty Pi 5 HAT+** specifically designed for Pi 5.

From UUGear website:
- "Using a Pi 5? The Witty Pi 5 HAT+ is now available!"
- Witty Pi 5 HAT+ is the first Witty Pi board complying with Raspberry Pi HAT+ specification
- As a Mode 1 Power HAT+ board, Witty Pi 5 can deliver up to 5A current

**Recommendation:** Consider upgrading to Witty Pi 5 HAT+ for Pi 5 projects to ensure:
- Proper HAT+ compliance
- Adequate power delivery (up to 5A)
- Better EEPROM compatibility when stacking

### HAT Stacking Best Practices

**EEPROM Conflicts:**
- HATs use I2C bus (pins 27 & 28) for identification via EEPROM
- Multiple HATs with EEPROMs at same address will conflict
- **Solution:** Most GPIO screw terminal HATs do NOT have EEPROM, making them safe to stack

**GPIO Pin Conflicts:**
- Must verify that Witty Pi 4 and terminal block HAT don't use same GPIO pins
- Check pinout documentation for both boards
- Good news: Most screw terminal HATs are passive breakouts with no active GPIO usage

**Power Budget:**
- Witty Pi 4 acts as power management/distribution
- Verify total current draw is within Witty Pi 4's capabilities
- Pi 5 can draw significant current (up to 5A under full load with peripherals)

**HAT+ Standard:**
- Can stack up to 3 boards following HAT+ standard: one 'standard' (legacy), one 'stackable', and one 'power'
- Witty Pi 5 HAT+ would be 'power' HAT
- GPIO screw terminal would be 'stackable' or 'standard'

### Physical Stacking Considerations

**Header Heights:**
- Witty Pi 4 recent revision (since 2025.05.13): Changed SMT header from 2mm to 3.5mm plastic
- This increased thickness by 1.5mm but reduced protruding pin length
- Verify that female headers on terminal block HAT have adequate pin length for secure connection

**Mechanical Support:**
- Use standoffs to prevent flexing of stacked boards
- Adafruit Pi-EzConnect includes mounting holes for this purpose
- 52Pi EP-0129 includes copper pillars and screws

---

## Alternative Approaches

### Ribbon Cable Breakout Boards

If stacking becomes problematic, consider ribbon cable breakout solutions:

**Advantages:**
- No stacking conflicts
- Can mount terminal block remotely from Pi
- Easier access to terminals in enclosures
- No mechanical stress on GPIO header

**Products:**
1. **RasPiO Breakout**
   - Can add screw terminal headers
   - Mounting holes for off-Pi installation
   - Use with ribbon cable

2. **Sequent Microsystems GPIO Breakout Board**
   - Heavy-duty pluggable terminal blocks
   - Accepts 24-14 AWG wires
   - Rated 8A/300V
   - Can plug into Pi OR stackable expansion cards

3. **KEYESTUDIO GPIO Breakout Kit**
   - Includes 40-pin rainbow ribbon cable
   - GPIO T-type shield
   - Breadboard (not screw terminals, but could modify)

**Ribbon Cable Specifications:**
- 40-pin IDC ribbon cable
- 2.54mm pitch
- Available in various lengths (15cm, 30cm, 50cm common)
- Cost: $3-8 USD typically

---

## Final Recommendation

### For Your Pi 5 + Witty Pi 4 Configuration:

**Best Option: Adafruit Pi-EzConnect Terminal Block Breakout HAT (ID 2711)**

**Rationale:**
1. **Proven stackability** - Explicitly designed with extended headers for stacking
2. **Overvoltage protection** - Critical for outdoor/field deployment with power management
3. **Pi 5 compatible** - Officially listed
4. **Reliability** - From reputable manufacturer (Alchemy Power/Adafruit)
5. **Documentation** - Well-documented pins, no external reference needed
6. **Price-to-feature ratio** - $19.95 is reasonable for the protection and quality

**Budget Alternative: 52Pi EP-0129 GPIO Screw Terminal HAT**
- If budget is constrained ($14.44 vs $19.95)
- May need extra tall stacking headers (~$3-5 additional)
- Less robust but functional

### Implementation Notes:

1. **Verify Witty Pi 4 pass-through header** - Ensure it provides full 40-pin pass-through
2. **Check GPIO pin usage** - Confirm Witty Pi 4 doesn't actively use GPIO pins needed for your project
3. **Consider upgrading to Witty Pi 5 HAT+** - For optimal Pi 5 compatibility and HAT+ standard compliance
4. **Plan wire gauge** - Both recommended options accept 18-28 AWG wire
5. **Test power budget** - Ensure total current draw is within Witty Pi's power delivery capability

### Ordering Information:

**Option 1: Adafruit Pi-EzConnect**
- Direct: https://www.adafruit.com/product/2711
- Price: $19.95 USD
- Stock: Available (8 units as of research date)

**Option 2: 52Pi EP-0129**
- Direct: https://52pi.com/products/52pi-gpio-screw-terminal-hat-for-raspberry-pi
- Price: $14.44 USD
- Also at The Pi Hut: £13

**If stacking proves problematic:**
- Consider Sequent Microsystems ribbon cable terminal block
- Or use Pi-EzConnect with very short ribbon cable for semi-stackable configuration

---

## Sources & References

### Primary Sources:
1. [Adafruit Pi-EzConnect Terminal Block Breakout HAT](https://www.adafruit.com/product/2711)
2. [The Pi Hut - GPIO Screw Terminal HAT](https://thepihut.com/products/gpio-screw-terminal-hat)
3. [52Pi GPIO Screw Terminal HAT Official](https://52pi.com/products/52pi-gpio-screw-terminal-hat-for-raspberry-pi)
4. [Geekworm G470 Product Page](https://geekworm.com/products/g470)
5. [Witty Pi 4 - UUGear](https://www.uugear.com/product/witty-pi-4/)
6. [Witty Pi 5 HAT+ - UUGear](https://www.uugear.com/product/witty-pi-5/)
7. [Seeed Studio GPIO Screw Terminal HAT](https://www.seeedstudio.com/GPIO-Screw-Terminal-Hat-for-Raspberry-Pi-p-4808.html)

### Technical References:
8. [Raspberry Pi Forums - Stacking Multiple HATs](https://forums.raspberrypi.com/viewtopic.php?t=372508)
9. [Adafruit Learning - Stacking HATs Guide](https://learn.adafruit.com/adafruit-16-channel-pwm-servo-hat-for-raspberry-pi/stacking-hats)
10. [52Pi Wiki - EP-0129](https://wiki.52pi.com/index.php/EP-0129)
11. [GPIO Pinout Reference](https://pinout.xyz/)

### Retailer Links:
12. [PiShop.us - Pi-EzConnect](https://www.pishop.us/product/pi-ezconnect-terminal-block-breakout-hat/)
13. [Kiwi Electronics - GPIO Screw Terminal HAT](https://www.kiwi-electronics.com/en/gpio-screw-terminal-hat-10762)
14. [Amazon - GeeekPi GPIO Terminal Block](https://www.amazon.com/GeeekPi-Screw-Terminal-Raspberry-Extension/dp/B08GKQMC72)
15. [RobotShop - 52Pi GPIO Screw Terminal](https://www.robotshop.com/products/52pi-gpio-screw-terminal-hat-raspberry-pi)

---

## Appendix: Technical Specifications Comparison

| Feature | Pi-EzConnect (2711) | 52Pi EP-0129 | Seeed Studio | Geekworm G470 |
|---------|---------------------|--------------|--------------|---------------|
| **Price** | $19.95 | $14.44 / £13 | Unknown | Unknown |
| **Stackable** | Yes (extended headers) | Yes (may need riser) | Yes | Not confirmed |
| **Pi 5 Compatible** | Yes (explicit) | Not stated | Not stated | Yes (explicit) |
| **Overvoltage Protection** | Yes (8V, 1.6A fuse) | No | No | No |
| **LED Indicators** | No | Yes (color-coded) | Yes | Unknown |
| **Wire Gauge** | 18-28 AWG (est.) | 18-28 AWG | Unknown | Unknown |
| **Screw Size** | Unknown | M1.6 | Unknown | Unknown |
| **Terminal Pitch** | 2.54mm | 2.54mm | Unknown | Unknown |
| **Includes Hardware** | No | Yes (standoffs, screws, screwdriver) | Unknown | Unknown |
| **Documentation** | Excellent | Good | Fair | Fair |
| **Manufacturer** | Alchemy Power (via Adafruit) | 52Pi | Seeed Studio | Geekworm |

---

## Research Methodology

This research was conducted on January 7, 2026, using web searches for:
- Product specifications from manufacturer websites
- Retailer listings (Adafruit, The Pi Hut, Amazon, etc.)
- Technical documentation and wikis
- Raspberry Pi community forums
- HAT compatibility and stacking best practices

All pricing and availability information is current as of the research date and should be verified before purchase.

---

**End of Research Report**
