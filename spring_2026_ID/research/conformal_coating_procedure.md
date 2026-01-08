# Conformal Coating Application Procedure
## Raspberry Pi 5 and Associated HATs

**Document Version:** 1.0
**Date:** January 8, 2026
**Coating Material:** MG Chemicals 422C Silicone Conformal Coating

---

## Table of Contents

1. [Overview](#overview)
2. [Materials and Equipment](#materials-and-equipment)
3. [Safety Requirements](#safety-requirements)
4. [Workspace Setup](#workspace-setup)
5. [Component-Specific Masking Guidelines](#component-specific-masking-guidelines)
6. [Pre-Application Preparation](#pre-application-preparation)
7. [Coating Application Procedure](#coating-application-procedure)
8. [Curing Process](#curing-process)
9. [Post-Coating Inspection](#post-coating-inspection)
10. [Functional Testing](#functional-testing)
11. [Troubleshooting](#troubleshooting)
12. [References](#references)

---

## 1. Overview

This procedure provides step-by-step instructions for applying MG Chemicals 422C silicone conformal coating to Raspberry Pi 5 boards and associated HATs for environmental protection in outdoor/harsh conditions. The 422C coating is a 1-part acrylic-silicone blend that provides protection against moisture, corrosion, dirt, dust, thermal shock, and electrical hazards.

**Target Components:**
- Raspberry Pi 5 PCB
- Witty Pi 5 HAT+ PCB
- Adafruit Pi-EzConnect Terminal Block HAT
- Relay modules
- Other exposed PCBs in the assembly

**Coating Properties:**
- **Type:** Acrylic-silicone blend, UV-traceable
- **Service Temperature Range:** -55°C to +200°C
- **Handling Time:** 10 minutes
- **Full Cure Time:** 24-48 hours at room temperature (or accelerated with heat)
- **Target Dry Film Thickness:** 1-3 mils (25-76 µm)

---

## 2. Materials and Equipment

### 2.1 Coating Materials

**MG Chemicals 422C Conformal Coating:**

For coating approximately 10 complete board sets (Raspberry Pi 5 + 2-3 HATs each):

- **Quantity Required:** 2-3 bottles of 55mL (part number: 422C-55MLCA)
- **Coverage Estimate:** Each 55mL bottle covers approximately 7080 cm² (7.6 ft²) at recommended thickness
- **Raspberry Pi 5 board area:** ~85 cm² (8.5 x 5.6 cm)
- **Typical HAT area:** ~80-90 cm² each
- **Total area per assembly:** ~250-350 cm² (accounting for both sides and components)
- **Practical coverage:** Approximately 3-4 complete assemblies per 55mL bottle

**Note:** Purchase 3 bottles to ensure adequate material for 10 assemblies plus some margin for practice/rework.

### 2.2 Masking Materials

- **Kapton/Polyimide tape** (various widths):
  - 1/4" (6mm) width - for fine masking around small connectors
  - 1/2" (12mm) width - for general masking
  - 1" (25mm) width - for large areas like GPIO headers
  - **Recommended:** Purchase at least 2 rolls of each size
  - **Alternative:** Low-ESD polyimide tape preferred for reduced static discharge

- **Precision masking caps/boots** (optional but recommended):
  - USB-A port dust caps
  - HDMI micro dust caps
  - Ethernet RJ45 dust caps
  - USB-C dust caps

- **Latex finger cots or small balloons** (for masking cylindrical connectors)

- **Liquid latex or peelable masking compound** (optional, for complex geometries):
  - Loctite 3705 high-viscosity gel (UV-curable) for connector bases

### 2.3 Application Tools

- **Brushes:**
  - 6-12mm horse-hair or synthetic conformal coating brushes (quantity: 3-5 brushes)
  - Keep brushes dedicated to conformal coating only
  - Do not use brushes for other chemicals

- **Brush storage container:**
  - Small glass jar with lid
  - MG Chemicals thinner/cleaner for brush storage

- **Coating work pot:**
  - Small glass or metal container for working quantity of coating
  - Do not pour coating back into original bottle

### 2.4 Cleaning Supplies

- **Isopropyl Alcohol (IPA):** 99% concentration, minimum 500mL
- **Lint-free wipes:** Cleanroom-grade or Kimwipes
- **Cotton swabs:** For precision cleaning
- **ESD-safe brushes:** For removing dust/debris before coating
- **MG Chemicals #824 cleaner** (alternative to IPA)

### 2.5 Inspection Tools

- **UV-A flashlight:** 365nm wavelength for inspecting coating coverage (422C fluoresces under UV)
- **Magnifying glass or loupe:** 5-10x magnification
- **Digital calipers or thickness gauge:** For spot-checking coating thickness (optional)
- **Continuity tester/multimeter:** For post-coating electrical testing

### 2.6 Workspace Equipment

- **ESD-safe work surface:** Grounded ESD mat
- **PCB holders/fixtures:** Adjustable angle stands (30-60° angle recommended)
- **Adequate ventilation:** Fume extractor or well-ventilated area
- **Good lighting:** Bright white light plus UV light source
- **Convection oven** (optional): For accelerated curing at 65°C

### 2.7 Personal Protective Equipment (PPE)

- Nitrile or latex gloves
- Safety glasses
- Lab coat or protective clothing
- Respirator with organic vapor cartridges (if ventilation is inadequate)

---

## 3. Safety Requirements

### 3.1 Chemical Hazards

**MG Chemicals 422C contains volatile organic compounds (VOCs):**

- **Inhalation:** Can cause respiratory irritation, dizziness, and drowsiness
- **Skin Contact:** May cause mild irritation
- **Eye Contact:** May cause irritation
- **Ingestion:** Harmful if swallowed

### 3.2 Safety Precautions

1. **Ventilation:**
   - Work in a well-ventilated area
   - Use local exhaust ventilation (fume hood or extraction fan)
   - Maintain airflow rate of at least 60 cubic feet per minute

2. **Personal Protection:**
   - Always wear nitrile gloves when handling coating
   - Wear safety glasses to protect eyes from splashes
   - Use respirator with organic vapor cartridges if working without adequate ventilation
   - Wear long sleeves to minimize skin exposure

3. **Fire Safety:**
   - Keep away from open flames and heat sources
   - Coating is flammable when wet
   - Have fire extinguisher readily available
   - Do not smoke in work area

4. **First Aid:**
   - **Eye contact:** Rinse immediately with water for 15 minutes, seek medical attention
   - **Skin contact:** Wash with soap and water
   - **Inhalation:** Move to fresh air immediately
   - **Ingestion:** Do not induce vomiting, seek medical attention

5. **Disposal:**
   - Dispose of used coating materials according to local regulations
   - Used rags/wipes should be disposed of in sealed metal containers
   - Do not pour coating down drains

### 3.3 ESD Precautions

- Work on grounded ESD mat
- Wear ESD wrist strap when handling boards
- Store boards in ESD-safe bags when not being processed
- Use ESD-safe tools and containers

---

## 4. Workspace Setup

### 4.1 Workspace Organization

1. **Clean work area:** Remove all unnecessary items and thoroughly clean work surface
2. **Set up ESD mat:** Connect to proper ground
3. **Position lighting:** Arrange both white LED light and UV light for good visibility
4. **Set up ventilation:** Position fume extractor or ensure adequate airflow
5. **Organize materials:** Arrange all materials within easy reach in logical order:
   - Left side: Cleaning supplies, uncoated boards
   - Center: Work area with PCB holder
   - Right side: Coating materials, masking supplies, coated boards (drying area)

### 4.2 Board Holder Setup

- Set PCB holder at 30-60° angle to minimize drips and runs
- Angle can be adjusted during application to reach different areas
- Ensure holder is stable and won't tip during application

### 4.3 Environmental Conditions

**Optimal conditions for coating application:**

- **Temperature:** 15-25°C (59-77°F)
- **Relative Humidity:** 30-60%
- **Cleanliness:** Dust-free environment

**Note:** Coating outside these ranges may result in poor adhesion, orange-peel texture, or extended cure times.

---

## 5. Component-Specific Masking Guidelines

### 5.1 Raspberry Pi 5 - Areas to MASK (Do Not Coat)

**Critical masking areas (these MUST be masked):**

1. **USB Ports (4x USB 3.0/2.0 ports):**
   - Mask all four USB-A ports completely
   - Use pre-cut dust caps OR Kapton tape to cover entire opening
   - Ensure no coating can enter the port

2. **HDMI Ports (2x micro-HDMI):**
   - Mask both micro-HDMI ports
   - Use micro-HDMI dust caps OR carefully applied Kapton tape
   - Cover entire connector opening

3. **Ethernet Port (Gigabit RJ45):**
   - Mask RJ45 jack completely
   - Use RJ45 dust cap OR Kapton tape over opening
   - Ensure metal shield and internal contacts are protected

4. **3.5mm Audio/Video Jack:**
   - Mask circular opening with Kapton tape
   - Ensure internal contacts are protected

5. **MicroSD Card Slot:**
   - Mask entire card slot opening
   - Use Kapton tape to cover slot entrance
   - Alternative: Insert dummy SD card during coating, then remove after curing

6. **USB-C Power Connector:**
   - Mask USB-C port opening
   - Use USB-C dust cap OR Kapton tape
   - Ensure internal contacts are protected

7. **40-Pin GPIO Header:**
   - **Method 1 (Recommended):** Apply 1" wide Kapton tape over entire header, covering all pins
   - **Method 2:** Use pre-cut conformal coating discs designed for 40-pin headers
   - Mask both the pins and the plastic housing
   - If HAT will be permanently installed, coating pins may be acceptable, but NOT recommended for field-serviceable assemblies

8. **CSI Camera Connector (2x):**
   - Mask both 15-pin flex cable connectors
   - Use Kapton tape to cover connector opening and locking mechanism
   - Ensure no coating enters the flex cable socket

9. **DSI Display Connector (2x):**
   - Mask both 15-pin flex cable connectors
   - Use Kapton tape to cover connector opening and locking mechanism
   - Ensure no coating enters the flex cable socket

10. **PCIe Connector (FPC):**
    - Mask the PCIe FPC connector
    - Use Kapton tape over connector opening

11. **PoE Header (4-pin):**
    - If using PoE HAT, mask this 4-pin header near GPIO
    - If not using PoE, coating is acceptable

12. **Fan Connector (4-pin JST):**
    - Mask the 4-pin JST fan connector (located between GPIO and USB ports)
    - Use Kapton tape or small latex finger cot over connector

13. **RTC Battery Connector (2-pin JST):**
    - Mask the 2-pin JST connector for RTC battery (near SD card slot)
    - Use Kapton tape or small latex finger cot

14. **Heat Sink Mounting Points:**
    - Mask the four spring-loaded push-pin mounting holes/standoffs
    - These are located at corners near the SoC
    - If thermal pads are already installed, mask them completely

15. **PMIC Chip (DA9121):**
    - If thermal pad is installed on PMIC, mask the thermal pad area
    - Located near center of board

16. **Status LEDs:**
    - **Option 1:** Mask LEDs to maintain full visibility (recommended for debugging)
    - **Option 2:** Apply very thin coating for some protection while maintaining some visibility
    - Power LED (red) and Activity LED (green) are located near USB-C port

17. **Test Points:**
    - Mask any test points (TP1, TP2, etc.) if they may be needed for debugging
    - Use small pieces of Kapton tape

**Additional considerations:**

- **SoC (BCM2712):** The main processor chip may be coated unless a heatsink/thermal pad will be installed
- **RAM Chip:** May be coated unless thermal pad will be installed
- **Wireless Module:** May be coated, but ensure antenna connector (if present) is masked

### 5.2 Witty Pi 5 HAT+ - Areas to MASK

**Critical masking areas:**

1. **40-Pin GPIO Header - Bottom (Female):**
   - Mask the female GPIO header on the bottom of the HAT that connects to Raspberry Pi
   - Use 1" wide Kapton tape or conformal coating disc
   - Ensure all pins are fully covered

2. **40-Pin GPIO Header - Top (Male, Pass-through):**
   - Mask the male GPIO header on top of the HAT (if present)
   - Use 1" wide Kapton tape or conformal coating disc

3. **Power Input Terminal Block (VIN):**
   - Mask the 2-position screw terminal for power input
   - Use Kapton tape to cover screw terminals and wire insertion points
   - Ensure no coating can enter contact areas

4. **VUSB Terminal Block (if present):**
   - Mask any additional power terminal blocks
   - Cover screw terminals and contact areas

5. **Battery Holder (CR2032):**
   - **Battery contacts:** Mask the metal contacts inside battery holder
   - **Method:** Apply Kapton tape strips over contacts
   - **Alternative:** Insert battery during masking, coat around it, then replace battery after curing
   - Battery holder plastic housing may be coated

6. **Push Buttons:**
   - Mask any tactile switches/buttons
   - Cover button tops to maintain functionality
   - Use small pieces of Kapton tape

7. **LEDs:**
   - **Option 1:** Mask all LEDs to maintain full brightness (recommended)
   - **Option 2:** Apply thin coating for protection with reduced brightness
   - Witty Pi 5 has status LEDs for power, RTC, and system activity

8. **Mounting Holes:**
   - Mask PCB mounting holes to allow proper standoff installation
   - Use small Kapton tape pieces or masking dots

9. **I2C EEPROM:**
   - Generally safe to coat, no masking needed

10. **Microcontroller (RP2350):**
    - Generally safe to coat, no masking needed

11. **RTC Chip:**
    - Generally safe to coat, no masking needed

12. **Temperature Sensor:**
    - Generally safe to coat, may slightly affect readings but typically negligible
    - If high-precision temperature sensing is critical, consider masking

### 5.3 Adafruit Pi-EzConnect Terminal Block HAT - Areas to MASK

**Critical masking areas:**

1. **All Screw Terminals:**
   - Mask ALL screw terminal blocks completely
   - Cover screw heads, wire insertion points, and internal contacts
   - Use Kapton tape strips along terminal rows
   - Ensure no coating can enter terminal contact areas
   - These are the most critical areas on this board

2. **40-Pin GPIO Header - Bottom (Female):**
   - Mask the female GPIO header connecting to Raspberry Pi
   - Use 1" wide Kapton tape or conformal coating disc

3. **40-Pin GPIO Header - Top (Male, Pass-through, if present):**
   - Mask any pass-through GPIO header on top

4. **Mounting Holes:**
   - Mask PCB mounting holes
   - Use small Kapton tape pieces

5. **I2C EEPROM (if present):**
   - Generally safe to coat

6. **Test Points (if present):**
   - Mask any labeled test points that may be needed for debugging

**Note:** Most of the Pi-EzConnect board can be coated since the terminal blocks are the primary interface points. Ensure thorough masking of all terminals.

### 5.4 Relay Modules - Areas to MASK

**Critical masking areas:**

1. **Relay Contact Terminals:**
   - Mask all screw terminals and wire connection points
   - Cover NO (Normally Open), NC (Normally Closed), and COM terminals
   - Use Kapton tape over terminal blocks

2. **Control Input Terminals:**
   - Mask control signal input terminals and connectors
   - Cover any JST connectors, pin headers, or screw terminals

3. **Power Input Terminals:**
   - Mask power supply connection terminals
   - Cover both positive and negative/ground connections

4. **Status LEDs:**
   - Mask LEDs to maintain visibility
   - Or apply thin coating if visibility is not critical

5. **Jumpers and Configuration Headers:**
   - Mask any configuration jumpers or DIP switches
   - These need to remain accessible for field configuration

6. **Relay Mechanism:**
   - **Important:** The relay mechanism itself (inside the relay housing) should NOT be coated
   - The sealed relay cans are typically already protected
   - Only coat the PCB areas, not the relay body
   - If relay is not fully sealed, mask entire relay

7. **Test Points:**
   - Mask any test points needed for troubleshooting

### 5.5 General Masking Guidelines for All PCBs

**Do NOT coat these areas on any board:**

1. **Any connector that needs to be serviceable**
2. **Mating surfaces between stacked boards**
3. **Heatsink mounting points and thermal interfaces**
4. **Switches and buttons**
5. **LEDs (unless visibility reduction is acceptable)**
6. **Test points required for field diagnostics**
7. **Mounting holes**
8. **Battery contacts**
9. **Adjustable components** (potentiometers, trimmers)

**Safe to coat (unless otherwise specified):**

1. Most SMD resistors, capacitors, inductors
2. ICs with proper lead spacing (coating is solderable-through)
3. PCB traces and solder joints
4. Crystal oscillators (typically okay, verify for high-precision applications)
5. Board edges and mounting pad areas

---

## 6. Pre-Application Preparation

### 6.1 Board Inspection (Before Cleaning)

1. **Visual inspection:**
   - Inspect all boards under good lighting
   - Check for physical damage, cracked solder joints, or manufacturing defects
   - Verify all components are properly seated and soldered
   - Take photos for documentation

2. **Functional testing:**
   - Power up and test all boards before coating
   - Verify GPIO functionality, connectivity, and all features
   - Document any issues found
   - **Do not coat defective boards** - repair first

3. **Component verification:**
   - Verify all required components are installed
   - Check that no temporary components (test fixtures, etc.) are on the board
   - Remove any labels, stickers, or adhesive residue

### 6.2 Board Cleaning

**Goal:** Remove all contaminants that could interfere with coating adhesion, including flux residues, oils, dust, and particulates.

**Procedure:**

1. **Initial dust removal:**
   - Use ESD-safe brush or compressed air to remove loose dust
   - Hold board at angle so debris falls away
   - Do not use high-pressure air that could damage components

2. **Isopropyl Alcohol (IPA) cleaning:**
   - Pour small amount of 99% IPA into clean container
   - Dip lint-free wipe in IPA and wring out excess
   - Gently wipe entire PCB surface in one direction
   - Use cotton swabs for tight areas between components
   - Pay special attention to areas around solder joints and component leads
   - Do not scrub aggressively on delicate components

3. **Stubborn flux removal:**
   - For visible flux residues, use additional IPA and gentle scrubbing
   - May use soft-bristle brush with IPA for stubborn areas
   - Alternative: MG Chemicals #824 flux remover for difficult residues

4. **Drying:**
   - Allow board to air dry completely (minimum 15 minutes)
   - May use gentle compressed air to speed drying
   - Ensure no IPA remains in crevices or under components
   - Verify dryness before proceeding

5. **Final inspection:**
   - Inspect board under bright light and UV light
   - Check for remaining contamination
   - Surface should be clean, dry, and free of residues
   - Any remaining oils or residues will show under UV light

**Important Notes:**

- Do not use water-based cleaners unless flux is water-soluble
- Do not use aggressive solvents that might damage components or markings
- Work in ESD-safe environment to prevent static damage during handling
- Use clean gloves to prevent transferring oils from hands

### 6.3 Masking Application

**Preparation:**

1. Cut Kapton tape into appropriate lengths before starting
2. Pre-position all dust caps and masking materials
3. Work in a clean, well-lit area
4. Have both white light and UV light available

**Masking Procedure:**

1. **Start with large areas first:**
   - Begin with GPIO headers using wide tape
   - Apply tape smoothly without wrinkles or air bubbles
   - Press down firmly to ensure good seal

2. **Move to medium-sized connectors:**
   - Mask USB ports, HDMI ports, Ethernet jack
   - Use dust caps if available, or carefully applied tape
   - Ensure complete coverage with no gaps

3. **Finish with small/precision areas:**
   - Mask small JST connectors, test points, LEDs
   - Use narrow tape for precise masking
   - Use cotton swab or toothpick to press tape into corners

4. **Connector base protection (optional but recommended):**
   - Apply thin bead of Loctite 3705 or similar gel around connector bases
   - This prevents coating from wicking under connectors
   - Cure per gel manufacturer's instructions

5. **Tape application tips:**
   - Cut tape with clean, straight edges
   - Apply tape with slight tension to avoid wrinkles
   - Overlap tape edges by 1-2mm for complete coverage
   - Press down all edges firmly to create seal
   - For cylindrical connectors, wrap tape around 1.5 times
   - Trim excess tape cleanly with sharp blade

6. **Inspection:**
   - Inspect all masked areas under bright light
   - Check for gaps, wrinkles, or poorly adhered tape
   - Verify complete coverage of all critical areas
   - Test tape adhesion by lightly pulling corners

7. **Documentation:**
   - Take photos of masked board for reference
   - Note any special masking approaches used
   - Keep photos for training and quality records

**Common Masking Mistakes to Avoid:**

- Leaving gaps between tape strips
- Not pressing tape down firmly, allowing coating to seep underneath
- Using too much tape (makes removal difficult and leaves residue)
- Masking too late (contaminants can get on masked areas)
- Not masking mounting holes (prevents proper assembly)

---

## 7. Coating Application Procedure

### 7.1 Pre-Application Setup

1. **Prepare coating material:**
   - Gently roll or invert bottle to remix coating (do not shake vigorously)
   - Pour small working quantity (5-10mL) into clean glass work pot
   - Keep main bottle tightly sealed to prevent solvent evaporation
   - Work pot should only contain enough coating for 2-3 boards

2. **Prepare brushes:**
   - Select appropriate brush size (6-12mm width)
   - If brush is stored in thinner, wipe excess thinner on clean cloth
   - Allow any remaining thinner to evaporate (1-2 minutes)
   - Brush should be clean and free of dried coating

3. **Position board:**
   - Place board in holder at 30-60° angle
   - Position so you can easily reach all areas
   - Ensure good lighting on work surface
   - Have UV light ready for coverage verification

### 7.2 Coating Application Technique

**General Principles:**

- **Thin coats are better than thick coats**
- Target thickness: 1-3 mils (25-76 µm)
- Apply in smooth, even strokes
- Do not over-brush areas that have started to dry
- Work systematically across the board

**Step-by-Step Application:**

1. **Load brush:**
   - Dip brush about 1/3 of bristle length into coating
   - Gently tap brush on side of container to remove excess
   - Brush should be wet but not dripping

2. **Apply coating - First pass (top side):**
   - Start at one corner of the board
   - Apply coating in long, smooth strokes in one direction
   - Use light pressure - let coating flow rather than pushing it
   - Cover entire exposed PCB surface systematically
   - Work from center outward toward edges

3. **Detail areas:**
   - Use lighter strokes around components
   - Ensure coating flows under component bodies and around leads
   - Pay attention to solder joints - ensure good coverage
   - Use tip of brush for tight spaces between components

4. **Edge coverage:**
   - Lightly pull brush over PCB edges for wrap-around protection
   - Avoid heavy buildup on edges
   - Do not allow coating to drip over edge to bottom side

5. **Cross-hatching (optional for critical areas):**
   - For critical high-voltage or high-moisture areas
   - After first coat direction, apply second pass at 90° angle
   - This ensures complete coverage with no thin spots

6. **Inspect coverage with UV light:**
   - Immediately check coverage using UV-A (365nm) light
   - 422C fluoresces bright blue/green under UV
   - Look for dark areas indicating missing coverage
   - Look for shadowed areas under tall components
   - Touch up any missed areas while coating is still wet

7. **Address shadowed areas:**
   - Tall components may create shadows preventing coating from reaching behind them
   - Angle board and reapply to reach shadowed zones
   - May need to apply coating from multiple angles
   - Use small brush or carefully reposition board

8. **Flash-off time:**
   - Allow board to sit for 5-10 minutes at room temperature
   - Coating will begin to tack up and become less mobile
   - Do not disturb board during this period
   - Solvent will evaporate, coating will thicken

9. **Bottom side coating (if required):**
   - After top side has tacked up (10-15 minutes), carefully flip board
   - Remove from holder, flip, and reposition
   - Repeat coating process on bottom side
   - Note: Many assemblies only require top-side coating
   - Bottom side typically has fewer components and less exposure

10. **Final UV inspection:**
    - After coating both sides, perform final UV inspection
    - Check for uniform coverage and thickness
    - Look for runs, drips, or excessive buildup
    - Verify coating extends to board edges

### 7.3 Brush Technique Best Practices

**Brush stroke technique:**

- Hold brush at 30-45° angle to board surface
- Use smooth, even strokes 2-4 inches long
- Lift brush at end of stroke (don't drag back)
- Reload brush frequently to maintain even wet film
- Do not press hard - let coating flow from brush

**Managing coating thickness:**

- Single thin coat is better than one thick coat
- If additional thickness is needed, apply second coat after first has fully cured (24-48 hours)
- Typical application requires only one coat at 1-2 mils dry film thickness

**Avoiding common defects:**

- **Runs/drips:** Keep board angled, don't over-load brush, work quickly
- **Orange peel texture:** Don't over-brush, maintain proper temperature/humidity, don't work coating as it's drying
- **Fisheyes/craters:** Ensure surface is clean and oil-free, check brush cleanliness
- **Bubbles:** Don't shake bottle, brush gently, don't over-work the coating
- **Thin spots:** Check coverage with UV light, reload brush more frequently

### 7.4 Working with Stacked Assemblies

For Raspberry Pi with HATs already assembled:

**Option 1: Coat before assembly (RECOMMENDED):**
- Coat each board separately before stacking
- Allows best access to all areas
- Easier masking and inspection
- Assemble after coating is fully cured

**Option 2: Coat after assembly:**
- More challenging to reach all areas
- Requires careful masking of mating connectors
- Risk of coating connector interfaces
- May need to partially disassemble for coating access
- Only recommended if disassembly is not practical

### 7.5 Multiple Board Processing

When coating multiple boards in sequence:

1. **Batch preparation:**
   - Clean and mask all boards before starting coating
   - Line up boards in order of processing
   - Prepare adequate coating in work pot

2. **Assembly line approach:**
   - Coat first board, start flash-off timer
   - Move to second board and begin coating
   - Continue through batch
   - Return to first board to check cure status
   - Flip and coat bottom sides in same sequence

3. **Brush maintenance:**
   - Clean brush every 3-4 boards or when loading fresh coating
   - Store brush in thinner between sessions
   - Never let coating dry on brush

4. **Coating freshness:**
   - Replace work pot coating if it becomes thick or tacky
   - Monitor coating viscosity - should flow easily
   - Pour fresh coating from main bottle as needed

---

## 8. Curing Process

### 8.1 Cure Options

MG Chemicals 422C offers flexible curing options:

**Option 1: Room Temperature Cure (Recommended for field/low-volume)**

- **Tack-free time:** 5-7 minutes
- **Handling time:** 10 minutes (board can be carefully moved)
- **Functional time:** 24 hours (board can be powered and tested)
- **Full cure:** 48 hours (maximum properties achieved)
- **Conditions:** 20-25°C (68-77°F), 40-60% relative humidity

**Option 2: Accelerated Oven Cure (Recommended for production)**

After initial flash-off (10 minutes at room temperature), use one of these cure schedules:

- **Standard cure:** 65°C (149°F) for 60 minutes
- **Fast cure:** 65°C (149°F) for 20 minutes (minimum)
- **Very fast cure:** 85°C (185°F) for 10 minutes

**Equipment required:**
- Convection oven with accurate temperature control
- Do not use ovens with exposed heating elements (fire hazard)
- Ensure adequate ventilation in oven (VOCs will be released)

**Option 3: Infrared Cure (Alternative)**

- Use infrared heat lamps positioned 8-12 inches from board
- Monitor board temperature with IR thermometer
- Target board surface temperature: 60-70°C
- Cure time: 20-30 minutes
- Risk of uneven heating - monitor carefully

### 8.2 Cure Process Steps

**For Room Temperature Cure:**

1. After coating application, place board on clean surface in drying area
2. Ensure area is dust-free and level
3. Do not disturb board for first 15 minutes
4. Cover loosely with clean container if dust is a concern (do not seal)
5. Allow full 24-48 hours before handling, testing, or removing masking
6. Verify cure by gently touching non-critical area - should be dry and non-tacky

**For Oven Cure:**

1. After coating application, allow 10-minute flash-off at room temperature
2. Preheat convection oven to desired temperature (65°C or 85°C)
3. Place boards on clean oven-safe rack or tray
4. Do not stack boards - allow air circulation around all surfaces
5. Place boards in preheated oven
6. Set timer for appropriate cure duration
7. After cure time, turn off oven and allow boards to cool gradually (10-15 minutes)
8. Remove boards from oven when cooled to <40°C
9. Allow boards to reach room temperature before handling (5-10 minutes)

### 8.3 Cure Verification

**Visual inspection:**
- Coating should appear uniform and glossy
- No tacky or wet areas
- No visible runs or excessive buildup

**Touch test:**
- Gently touch non-critical coated area with gloved finger
- Should be completely dry and non-tacky
- Should not transfer to glove
- Should feel smooth and slightly flexible

**UV verification:**
- Under UV light, coating should fluoresce uniformly
- Consistent color indicates even thickness
- No dark spots or gaps

**Cure indicator:**
- 422C will develop its full mechanical and protective properties after full cure
- Flexibility and moisture resistance continue to improve during full cure period

### 8.4 Curing Environmental Conditions

**Temperature:**
- Room cure: 15-25°C (59-77°F)
- Below 15°C: Cure time significantly increases
- Above 30°C: May cause surface defects

**Humidity:**
- Optimal: 30-60% RH
- Above 70% RH: May cause blushing or extended cure time
- Below 30% RH: Faster solvent evaporation, may cause surface defects

**Airflow:**
- Gentle airflow aids curing by removing solvent vapors
- Do not use high-speed fans that could deposit dust
- Do not cure in stagnant, enclosed spaces

---

## 9. Post-Coating Inspection

### 9.1 Visual Inspection Checklist

Perform detailed inspection after coating is fully cured:

**Coverage verification:**
- [ ] Entire PCB surface is coated except masked areas
- [ ] No visible gaps, shadows, or uncoated zones
- [ ] Coating extends to board edges
- [ ] Areas under components are coated
- [ ] Solder joints are fully covered

**Quality inspection:**
- [ ] Coating appears uniform in thickness and color
- [ ] No runs, drips, or excessive buildup
- [ ] No orange-peel texture or rough areas
- [ ] No bubbles, voids, or pinholes
- [ ] No fisheyes, craters, or contamination
- [ ] Coating is glossy and smooth

**UV fluorescence inspection:**
- [ ] Under UV light, coating fluoresces uniformly
- [ ] Color is consistent across entire board
- [ ] No dark spots indicating missing coverage
- [ ] Edges and corners show fluorescence

**Masking removal and inspection:**
- [ ] All masking tape has been removed cleanly
- [ ] No tape residue remains on connectors
- [ ] Masked areas are clean and free of coating
- [ ] No coating has wicked under masking
- [ ] Connectors are clean and functional

### 9.2 Thickness Verification (Optional)

For critical applications, verify coating thickness:

**Methods:**

1. **Destructive testing (sample boards):**
   - Use coating thickness gauge on test coupons
   - Target: 1-3 mils (25-76 µm)
   - Cross-section and measure under microscope

2. **Non-destructive estimation:**
   - UV fluorescence intensity correlates with thickness
   - Compare to reference standard of known thickness
   - Very bright fluorescence may indicate excessive thickness

3. **Weight measurement:**
   - Weigh board before coating (after cleaning and masking)
   - Weigh board after coating (after cure and masking removal)
   - Calculate coating weight and estimate coverage area

### 9.3 Defect Identification and Rework

**Common defects and solutions:**

| Defect | Appearance | Cause | Rework Solution |
|--------|-----------|-------|-----------------|
| **Thin spots/holidays** | Dark areas under UV, visible gaps | Insufficient coverage, shadowing | Strip and recoat, or touch up with brush |
| **Excessive thickness** | Very bright UV fluorescence, visible buildup | Over-application, too many coats | Strip and recoat thinner |
| **Runs/sags** | Drips, thick areas on vertical surfaces | Board angle, over-loading brush, working too slowly | Strip and recoat |
| **Orange peel** | Rough, textured surface | Working coating as it dries, poor environmental conditions | Strip and recoat |
| **Fisheyes** | Circular voids/craters | Surface contamination (oil, silicone) | Strip, clean thoroughly, recoat |
| **Bubbles** | Air pockets in coating | Vigorous brushing, shaking bottle, trapped air | Strip and recoat |
| **Blushing** | Milky or hazy appearance | High humidity during cure | May cure out over time; if persistent, strip and recoat |
| **Coating on masked areas** | Coating on connectors, ports | Poor masking, wicking under tape | Remove with appropriate stripper |

### 9.4 Coating Removal for Rework

If coating must be removed:

**Materials:**
- MG Chemicals 421B or 421C conformal coating remover
- Lint-free wipes
- Cotton swabs
- Soft bristle brush

**Procedure:**
1. Mask any areas that should remain coated (if partial removal)
2. Apply remover to affected areas with brush or swab
3. Allow remover to penetrate coating (1-5 minutes)
4. Gently wipe away softened coating with lint-free wipe
5. Repeat as necessary until coating is removed
6. Clean area with IPA to remove remover residue
7. Allow to dry completely
8. Reapply coating following standard procedure

**Safety notes:**
- Coating removers contain strong solvents
- Use in well-ventilated area
- Wear chemical-resistant gloves
- Follow remover product safety data sheet

### 9.5 Touch-Up Application

For small areas requiring additional coating:

1. Clean area with IPA if necessary
2. Mask adjacent areas to create clean edge (optional)
3. Apply thin coat of 422C with small brush
4. Feather edges to blend with existing coating
5. Allow to cure following standard cure schedule
6. Inspect with UV light for uniform coverage

### 9.6 Documentation

Record inspection results:

- Board serial number or batch ID
- Date coated and date inspected
- Inspector initials
- Pass/Fail status
- Any defects noted and corrective actions taken
- Photos of any issues or rework
- UV inspection photos for quality records

---

## 10. Functional Testing

After coating has fully cured and passed visual inspection, perform functional testing to verify operation:

### 10.1 Pre-Power Inspection

Before applying power to coated boards:

- [ ] Verify all masking has been removed
- [ ] Check that no coating is present in connectors or on terminals
- [ ] Inspect for any shorts caused by coating bridging components
- [ ] Verify no coating on battery contacts, terminal blocks, or power inputs
- [ ] Use continuity tester to check for unexpected shorts

### 10.2 Power-Up Test

1. **Visual inspection during power-up:**
   - Connect power supply (appropriate voltage for board)
   - Observe board during power-up
   - Look for any signs of overheating, smoking, or abnormal behavior
   - Check that status LEDs illuminate (if not masked)

2. **Thermal inspection:**
   - After 5-10 minutes of operation, check for hot spots
   - Use thermal camera or IR thermometer if available
   - Verify normal operating temperatures for all components
   - Coating should not affect thermal performance significantly

### 10.3 Raspberry Pi 5 Functional Test

**Basic functionality:**
- [ ] Board boots normally (activity LED blinks)
- [ ] HDMI output functions (connect to display)
- [ ] USB ports function (connect USB devices)
- [ ] Ethernet connectivity works
- [ ] MicroSD card is readable
- [ ] GPIO pins are accessible (if not coated) and functional
- [ ] CSI/DSI connectors function if used
- [ ] Audio output works

**Advanced testing:**
- [ ] Run standard Raspberry Pi diagnostics
- [ ] Test network connectivity and data transfer
- [ ] Verify USB 3.0 speeds
- [ ] Test GPIO functionality with simple LED circuit
- [ ] Verify RTC functionality if RTC battery is installed

### 10.4 Witty Pi 5 HAT+ Functional Test

**Basic functionality:**
- [ ] Witty Pi boots and initializes
- [ ] Real-time clock keeps accurate time
- [ ] Power management functions work (on/off control)
- [ ] Temperature sensor provides readings
- [ ] Status LEDs illuminate correctly
- [ ] I2C communication with Raspberry Pi works
- [ ] Power input voltage monitoring functions
- [ ] Battery-backed RTC maintains time during power loss

**Testing procedure:**
1. Install Witty Pi software on Raspberry Pi
2. Verify I2C communication: `sudo i2cdetect -y 1`
3. Read current time: `./wittyPi.sh` (run Witty Pi script)
4. Set schedule and verify power cycling works
5. Check temperature readings for reasonable values
6. Test both power input channels (VUSB and VIN)

### 10.5 Pi-EzConnect Terminal Block HAT Test

**Basic functionality:**
- [ ] GPIO passthrough works (signals reach terminals)
- [ ] Screw terminals accept wire and make good contact
- [ ] No shorts between adjacent terminals
- [ ] Terminal-to-GPIO mapping is correct

**Testing procedure:**
1. Use multimeter to verify continuity from each terminal to corresponding GPIO pin
2. Connect simple LED circuit to test GPIO output
3. Connect button/switch to test GPIO input
4. Verify ground and power rails are correctly connected
5. Check for shorts between terminals using continuity tester

### 10.6 Relay Module Functional Test

**Basic functionality:**
- [ ] Relay coils energize when control signal applied
- [ ] Relay contacts switch properly (NO and NC)
- [ ] No excessive heating during operation
- [ ] Status LEDs indicate relay state correctly
- [ ] Contact resistance is acceptable

**Testing procedure:**
1. Apply control voltage to relay input
2. Verify relay click/activation sound
3. Use multimeter to verify contact closure/opening
4. Measure contact resistance (should be <0.1Ω when closed)
5. Test relay under load (appropriate to relay rating)
6. Verify isolation between control and load circuits

### 10.7 Electrical Performance Verification

**Insulation resistance test (optional but recommended):**

For high-reliability applications, verify coating provides adequate insulation:

1. **Equipment needed:**
   - Megohmmeter (insulation resistance tester)
   - Typically test at 100V DC or 500V DC

2. **Test procedure:**
   - Power off and disconnect board
   - Test between adjacent traces or pads
   - Test between power and ground planes
   - Test between high-voltage and low-voltage circuits

3. **Acceptance criteria:**
   - Insulation resistance should be >100 MΩ (ideally >1000 MΩ)
   - Lower values indicate contamination or coating defects

**High-voltage testing (for specific applications):**

If board will operate in high-voltage environment:

1. Apply voltage between circuits at 1.5x operating voltage
2. Hold for 1 minute
3. Monitor for breakdown or arcing
4. Acceptance: No breakdown, flashover, or current leakage

### 10.8 Environmental Stress Testing (Optional)

For critical applications, perform accelerated testing:

**Humidity exposure:**
1. Place coated board in humidity chamber
2. Set to 85°C / 85% RH
3. Operate board under power for 24-168 hours
4. Inspect for signs of moisture intrusion or corrosion
5. Verify continued functionality

**Thermal cycling:**
1. Place board in thermal chamber
2. Cycle between -40°C and +85°C
3. Perform 10-100 cycles
4. Inspect coating for cracks or delamination
5. Verify continued functionality

**Salt spray (for marine applications):**
1. Expose to ASTM B117 salt spray environment
2. Duration: 24-96 hours
3. Inspect for corrosion on exposed metal surfaces
4. Verify coating integrity and electrical function

### 10.9 Test Documentation

Record all test results:

- [ ] Board ID and test date
- [ ] All functional tests performed and results (Pass/Fail)
- [ ] Any anomalies or issues discovered
- [ ] Electrical test measurements (if performed)
- [ ] Environmental test results (if performed)
- [ ] Tester initials and signature
- [ ] Final disposition (Accept / Reject / Rework)

**Test record retention:**
- Keep test records for lifetime of product
- Include with product documentation
- Reference for troubleshooting and warranty claims

---

## 11. Troubleshooting

### 11.1 Application Problems

| Problem | Possible Causes | Solutions |
|---------|----------------|-----------|
| **Coating won't flow from brush** | Coating too thick, old coating, cold temperature | Thin with MG thinner (up to 50%), use fresh coating, warm to room temperature |
| **Excessive runs and drips** | Board angle too steep, coating too thin, over-loading brush, working too slowly | Reduce board angle, work faster, load less coating on brush |
| **Bubbles in coating** | Shaking bottle, vigorous brushing, trapped air under components | Roll bottle gently, brush lightly, angle board to release air |
| **Orange peel texture** | Over-brushing, low humidity, high temperature, coating drying too fast | Work quickly, don't over-work, maintain proper environment, thin coating slightly |
| **Fisheyes/craters** | Surface contamination (oil, silicone, flux), dirty brush | Clean surface thoroughly, use clean brush, avoid silicone-containing products |
| **Coating not sticking to board** | Surface contamination, moisture on board | Clean with IPA, ensure complete drying, verify no mold release agents |
| **Coating under masking tape** | Low-viscosity coating, poor tape adhesion, tape gaps | Press tape down firmly, use higher quality tape, apply gel at connector bases |

### 11.2 Curing Problems

| Problem | Possible Causes | Solutions |
|---------|----------------|-----------|
| **Coating stays tacky** | Insufficient cure time, high humidity, cold temperature, contamination | Allow longer cure time, reduce humidity, increase temperature, verify coating is not contaminated |
| **Milky/cloudy appearance (blushing)** | High humidity during cure | Allow extended cure time, may self-correct; if not, strip and recoat in lower humidity |
| **Coating cracking** | Too thick application, rapid temperature change during cure | Apply thinner coats, avoid thermal shock, allow gradual cooling |
| **Poor adhesion after cure** | Surface contamination before coating, coating applied over flux residue | Strip, clean thoroughly with IPA or #824, recoat |

### 11.3 Functional Problems After Coating

| Problem | Possible Causes | Solutions |
|---------|----------------|-----------|
| **Connector not working** | Coating in connector, poor masking | Remove coating with stripper, reapply with better masking |
| **Component overheating** | Coating too thick reducing thermal dissipation | Strip and recoat thinner, verify heatsink thermal path is clear |
| **Intermittent operation** | Coating stress on sensitive components, coating on crystal | Strip and recoat, mask sensitive components |
| **Reduced signal quality** | Coating on high-frequency traces, excessive thickness | Strip and recoat thinner, mask critical RF areas |
| **Battery not working** | Coating on battery contacts | Remove coating from contacts with stripper |
| **LEDs too dim** | Heavy coating on LEDs | Strip coating from LEDs, reapply with masking or very thin coat |
| **Switch/button not working** | Coating preventing button actuation | Remove coating from button area |

### 11.4 Quality Issues

| Problem | Possible Causes | Solutions |
|---------|----------------|-----------|
| **Uneven UV fluorescence** | Variable coating thickness | Touch up thin areas, strip and recoat if severe |
| **Dark spots under UV** | Missing coverage, shadowing | Touch up with additional coating |
| **Excessively bright UV fluorescence** | Coating too thick | Strip and recoat thinner if electrical properties affected |
| **Coating peeling off** | Poor adhesion, surface contamination | Strip completely, clean thoroughly, recoat |
| **Discoloration over time** | UV exposure, high temperature | Normal for some coatings; verify electrical properties maintained |

### 11.5 Rework Challenges

| Problem | Possible Causes | Solutions |
|---------|----------------|-----------|
| **Coating difficult to remove** | Fully cured silicone, thick application | Use stronger stripper, allow longer soak time, mechanical removal with scraping |
| **Component damaged during removal** | Aggressive mechanical removal | Use chemical stripper, work carefully, protect adjacent components |
| **Residue after coating removal** | Incomplete removal, stripper residue | Clean thoroughly with IPA, use ultrasonic cleaner if available |
| **Solder won't flow through coating for repair** | Coating too thick, wrong coating type | Remove coating from repair area, verify 422C is solderable-through type |

### 11.6 When to Consult Manufacturer

Contact MG Chemicals technical support if:

- Coating properties are not as specified in datasheet
- Unusual adhesion or compatibility issues
- Need guidance on specific component compatibility
- Batch-to-batch variation in coating performance
- Need assistance with removal or rework of problematic coating

**MG Chemicals Contact:**
- Website: https://mgchemicals.com
- Technical support available for product questions

---

## 12. References

### 12.1 Technical Documentation

**MG Chemicals 422C Resources:**
- Product Page: [422C Silicone Conformal Coating](https://mgchemicals.com/products/conformal-coatings/silicone-conformal-coatings/conformal-coating-waterproof/)
- Technical Data Sheet: [422C TDS](https://mgchemicals.com/downloads/tds/tds-422c-l.pdf)
- Application Guide: [Conformal Coating Ultimate Application Guide](https://mgchemicals.com/knowledgebase/white-papers/conformal-coating-ultimate-application-guide/)

**Industry Standards:**
- IPC-CC-830C: Qualification and Performance of Electrical Insulating Compound for Printed Board Assemblies
- IPC-A-610: Acceptability of Electronic Assemblies (Section 10: Conformal Coating)
- UL94: Standard for Safety of Flammability of Plastic Materials (422C rated V-0)

### 12.2 Component Documentation

**Raspberry Pi 5:**
- [Raspberry Pi 5 Documentation](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html)
- [Raspberry Pi GPIO Pinout](https://pinout.xyz/)
- [Raspberry Pi 5 Heatsink/Cooling Guide](https://www.raspberrypi.com/news/heating-and-cooling-raspberry-pi-5/)

**Witty Pi 5 HAT+:**
- [Witty Pi 5 Product Page](https://www.uugear.com/product/witty-pi-5/)
- [Witty Pi 5 User Manual](https://www.uugear.com/doc/WittyPi5_UserManual.pdf)

**Adafruit Pi-EzConnect:**
- [Adafruit Product Page](https://www.adafruit.com/) (search for Pi-EzConnect)

### 12.3 General Conformal Coating Resources

**Application Techniques:**
- [How to Brush Coat a PCB](https://www.conformalcoating.co.uk/knowledge-hub/technical-articles/conformal-coating-processes-hub/how-to-brush-coat-a-pcb-with-conformal-coating/)
- [Essential Guide to Conformal Coating (Techspray)](https://www.techspray.com/the-essential-guide-to-conformal-coating)
- [Ultimate Guide to Conformal Coating (Chemtronics)](https://www.chemtronics.com/the-ultimate-guide-to-conformal-coating)
- [Manual Brushing Coatings Best Practices](https://blog.chasecorp.com/humiseal/manual-brushing-coatings)

**Masking Techniques:**
- [How to Mask PCBs Before Conformal Coating](https://www.echosupply.com/blog/how-to-mask-pcbs-before-conformal-coating/)
- [Samtec Conformal Coating Connectors Guide](https://suddendocs.samtec.com/processing/conformal_coating.pdf)
- [Kapton vs Blue Painter's Tape](https://gizmodorks.com/blog/kapton-vs-blue-painters-tape/)

**Discussion Forums:**
- [Raspberry Pi Forums - Waterproofing Discussion](https://forums.raspberrypi.com/viewtopic.php?t=116609)
- [DigiKey TechForum - Masking Tape Recommendations](https://forum.digikey.com/t/tape-recommendation-for-masking-conformal-coating/29190)

### 12.4 Safety Information

**Material Safety Data Sheets (SDS):**
- MG Chemicals 422C SDS - available from MG Chemicals website
- Isopropyl Alcohol SDS
- MG Chemicals 421B/421C Stripper SDS

**Regulatory Information:**
- OSHA regulations on VOC exposure and ventilation
- EPA regulations on VOC emissions and disposal
- Local fire code requirements for flammable material storage

### 12.5 Supplier Information

**Coating and Chemicals:**
- MG Chemicals: https://mgchemicals.com
- DigiKey Electronics: https://www.digikey.com
- Mouser Electronics: https://www.mouser.com
- Techni-Tool: https://www.techni-tool.com

**Masking Materials:**
- KaptonTape.com: https://kaptontape.com
- AI Technology Inc: https://www.aitechnology.com
- DigiKey Electronics (Kapton tape section)

**Tools and Equipment:**
- Techspray: https://www.techspray.com
- Chemtronics: https://www.chemtronics.com
- General electronics suppliers (brushes, IPA, etc.)

---

## Document Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-01-08 | Initial | Initial release of procedure |

---

## Appendix A: Quick Reference Checklist

### Pre-Coating Checklist

- [ ] All materials and tools gathered
- [ ] Workspace set up with proper ventilation
- [ ] PPE worn (gloves, safety glasses)
- [ ] Boards cleaned with IPA and fully dried
- [ ] Boards functionally tested and verified working
- [ ] All critical areas masked per Section 5
- [ ] Masking inspected for gaps and proper adhesion
- [ ] Coating material mixed (rolled, not shaken)
- [ ] Working quantity poured into clean pot
- [ ] Brush prepared and clean

### Coating Application Checklist

- [ ] Board positioned at 30-60° angle
- [ ] Coating applied in thin, even strokes
- [ ] All exposed areas covered systematically
- [ ] Coverage verified with UV light
- [ ] No runs, drips, or excessive buildup
- [ ] Board allowed to flash-off for 10 minutes
- [ ] Bottom side coated if required
- [ ] Final UV inspection performed

### Post-Coating Checklist

- [ ] Coating fully cured (24-48 hours room temp OR oven cured)
- [ ] Visual inspection passed (uniform, smooth, no defects)
- [ ] UV inspection passed (even fluorescence, no gaps)
- [ ] All masking tape removed cleanly
- [ ] Masked areas verified clean and coating-free
- [ ] Functional testing passed (all features working)
- [ ] Documentation completed (photos, test records)
- [ ] Board labeled with coating date and batch ID
- [ ] Board ready for assembly or storage

---

## Appendix B: Common Coating Defects - Photo Reference Guide

*Note: This section would include photos in a production document. Descriptions provided for reference.*

**Photo 1: Good Coverage**
- Description: Even coating thickness, uniform UV fluorescence, smooth glossy surface, complete coverage to edges

**Photo 2: Thin Spots/Holidays**
- Description: Dark areas under UV light indicating missing coverage, typically in shadowed areas under tall components

**Photo 3: Excessive Thickness**
- Description: Very bright UV fluorescence, visible buildup, may show runs or drips

**Photo 4: Orange Peel Texture**
- Description: Rough, dimpled surface texture resembling orange peel, caused by over-brushing or poor environmental conditions

**Photo 5: Fisheyes/Craters**
- Description: Circular voids in coating caused by surface contamination (oil, silicone)

**Photo 6: Runs and Sags**
- Description: Drips on vertical surfaces and edges, uneven thickness

**Photo 7: Coating on Masked Areas**
- Description: Coating present on connectors, terminals, or other masked areas due to poor masking or wicking

**Photo 8: Good Masking Technique**
- Description: Clean, sharp edges between coated and uncoated areas, no coating on connectors

---

## Appendix C: Material Quantities Calculator

### Coating Coverage Calculator

**Given Information:**
- MG Chemicals 422C coverage: 7080 cm² per 55mL bottle (at recommended thickness)
- Raspberry Pi 5 board area: ~85 cm² (8.5 x 5.6 cm)
- Typical HAT area: ~85 cm² (same footprint)

**Coverage Calculation:**

For a complete assembly with Raspberry Pi 5 + 2 HATs:
- Raspberry Pi 5: 85 cm² (top side) + 60 cm² (bottom side, less dense) = 145 cm²
- Witty Pi 5 HAT+: 85 cm² (top) + 40 cm² (bottom) = 125 cm²
- Pi-EzConnect HAT: 85 cm² (top) + 40 cm² (bottom) = 125 cm²
- **Total per assembly: ~395 cm²**

**Accounting for waste, overspray, and inefficiency (multiply by 1.5):**
- Effective coverage per assembly: ~600 cm²

**Bottles needed for 10 assemblies:**
- Total area: 10 assemblies × 600 cm² = 6000 cm²
- Bottles needed: 6000 cm² ÷ 7080 cm²/bottle = 0.85 bottles
- **Recommended: 2-3 bottles** (provides margin for practice, touch-ups, rework)

### Masking Tape Quantities

**For 10 assemblies (30 boards total):**

Per board:
- 40-pin GPIO header: 6" of 1" wide tape
- USB ports (4×): 12" of 1/2" wide tape
- Other connectors: 24" of 1/4" wide tape
- Total per board: ~42" (~1.1 meters)

For 30 boards:
- 1" wide tape: ~5 meters (recommend 2 rolls)
- 1/2" wide tape: ~10 meters (recommend 2 rolls)
- 1/4" wide tape: ~20 meters (recommend 2-3 rolls)

---

## Appendix D: Cure Schedule Reference Table

| Cure Method | Flash-Off Time | Cure Temperature | Cure Time | Total Time | Handling Time | Full Cure |
|-------------|----------------|------------------|-----------|------------|---------------|-----------|
| **Room Temperature** | None | 20-25°C | - | 24-48 hrs | 10 min | 48 hrs |
| **Standard Oven** | 10 min | 65°C | 60 min | 70 min | 10 min | Complete |
| **Fast Oven** | 10 min | 65°C | 20 min | 30 min | 10 min | Complete |
| **Very Fast Oven** | 10 min | 85°C | 10 min | 20 min | 10 min | Complete |

**Recommendations:**
- Use room temperature cure for field applications, low-volume production, or when oven is not available
- Use standard oven cure for production environments to ensure consistent results
- Use fast/very fast cure when schedule demands, but standard cure provides best results
- Always allow flash-off time before oven cure to prevent bubbling

---

## Appendix E: Troubleshooting Flowchart

```
Issue: Coating Not Adhering
├─ Is surface clean?
│  ├─ NO → Clean with IPA, dry completely, retest
│  └─ YES → Continue
├─ Is board completely dry?
│  ├─ NO → Dry thoroughly (min 15 min), retest
│  └─ YES → Continue
├─ Is there flux residue visible?
│  ├─ YES → Clean with flux remover, IPA rinse, dry, retest
│  └─ NO → Continue
├─ Is coating contaminated or old?
│  ├─ YES → Use fresh coating, retest
│  └─ NO → Continue
└─ Surface may have mold release or silicone contamination
   └─ Clean with specialized cleaner, consider light abrasion, recoat

Issue: Functional Problems After Coating
├─ Connector not working
│  └─ Check for coating in connector → Remove with stripper
├─ Component overheating
│  └─ Check thermal path → Strip coating from thermal areas
├─ Intermittent operation
│  └─ Check for coating stress → Strip and recoat thinner
└─ LED too dim
   └─ Check LED coating → Remove coating from LED or apply thinner

Issue: Poor Coating Appearance
├─ Orange peel texture
│  └─ Don't over-brush, maintain proper environment → Strip & recoat
├─ Runs and drips
│  └─ Reduce board angle, work faster, less coating on brush → Touch up or strip & recoat
├─ Fisheyes/craters
│  └─ Clean surface thoroughly, use clean brush → Strip & recoat
└─ Bubbles
   └─ Don't shake bottle, brush gently → Strip & recoat
```

---

**END OF PROCEDURE DOCUMENT**

---

*This procedure is a living document and should be updated based on operational experience and lessons learned. All users should be trained on this procedure before performing conformal coating operations. Any deviations from this procedure should be documented and reviewed.*

*For questions or clarifications, contact the technical lead or refer to MG Chemicals technical support.*
