# IP67/IP68 Camera Housing Research Report
## For RC-Box Small USB Camera Boards (32-38mm)

**Research Date:** November 28, 2025
**Purpose:** Identify weatherproof camera housings for ELP and Arducam USB camera boards with heater integration capability
**Target Price Range:** $15-60 per housing

---

## Executive Summary

This research identifies commercially available and DIY options for weatherproof camera housings suitable for the RC-Box humanitarian river monitoring project. Key findings include:

- **Best Commercial Options:** VA Imaging machine vision housings (€249/$270) and Entaniya WC-01 for Pi cameras (price TBD) offer purpose-built IP67 protection
- **Budget-Friendly Options:** LeMotech transparent junction boxes ($15-35 on Amazon) and similar generic IP67 boxes require minimal modification
- **DIY Solutions:** PVC pipe enclosures ($10-20 materials) and 3D printed housings offer maximum customization
- **Heater Integration:** Most options have sufficient internal space for 10-20W silicone heater pads (available $10-25)
- **Key Challenge:** Few off-the-shelf solutions specifically designed for 32-38mm USB camera boards in the target price range

---

## 1. PURPOSE-BUILT CAMERA HOUSINGS

### 1.1 VA Imaging Machine Vision Housings

**Product:** Machine Vision Camera Housing - IP67 Rated
**Manufacturer:** VA Imaging (formerly GeT Cameras)
**Website:** https://va-imaging.com

#### Specifications
- **Internal Dimensions:** Fits 29x29mm cameras (Regular), 44x44mm cameras (XL)
- **IP Rating:** IP67 (tested in conditions with GigE, USB3, and I/O cables)
- **Price:** €249 (~$270 USD) for aluminum version
- **Optical Window:** Glass lens tube (transmits 400-1000nm), 40mm diameter (Regular), 74mm (XL)
- **Mounting:** Includes adapter plates for various camera brands, bayonet lens tube fitting

#### Key Features
- Aluminum + industrial polymer construction
- Aluminum serves as heatsink for camera cooling
- Pressure equalization vent prevents condensation
- Modular lens tube system with 20mm tube + two 15mm extension tubes
- Most affordable machine vision housing on market (per manufacturer)
- Waterproof up to 1 meter depth for 30 minutes

#### Heater Integration
- **Ease:** Moderate - aluminum body conducts heat well; internal space adequate
- **Recommendation:** Mount heater pad to aluminum body for anti-fog, or near optical window

#### Compatibility with 32-38mm Boards
- Regular version too small (29mm max)
- XL version would work but oversized for typical USB camera boards
- Would require custom adapter plate

#### Where to Purchase
- VA Imaging website (va-imaging.com, va-imaging.us)
- 3-year warranty included

#### Assessment
**Pros:** Professional IP67 rating, excellent heat dissipation, proven design
**Cons:** Above budget ($270), designed for industrial cameras not USB boards, may require custom adapter

---

### 1.2 Components Express (CEI) IP67 Enclosures

**Product:** 29mm-IP67 Series Round/Extruded Camera Enclosure
**Manufacturer:** Components Express Inc. (CEI)

#### Specifications
- **Internal Dimensions:** 29mm cameras (too small for 32-38mm boards)
- **IP Rating:** IP67
- **Price:** Not publicly listed; available through distributors only
- **Optical Window:** Modular with optional windows and filters
- **Mounting:** Built-in adjustable mount with two tapped holes

#### Key Features
- Lightweight, low-profile design
- Type 2 anodized aluminum construction
- Integrated connector design (no cord grips needed)
- Excellent heat dissipation
- Tool-free access for maintenance
- U.S.-made

#### Availability
- 1stVision, Aegis Electronic Group, Stemmer Imaging USA, Phase 1 Vision
- **Not available through DigiKey or Mouser**

#### Assessment
**Pros:** Industrial quality, good heat management
**Cons:** Too small for 32-38mm boards, pricing not transparent, specialized distributor network only

---

### 1.3 Basler IP67 Housing

**Product:** IP67 Housing for ace/racer cameras
**Manufacturer:** Basler AG
**Website:** https://www.baslerweb.com

#### Specifications
- **Internal Dimensions:** Varies by camera model (ace 2, ace U, ace Classic, racer 2)
- **IP Rating:** IP67
- **Price:** Not publicly listed
- **Components:** Three-part system (camera housing, lens housing, cable gland)
- **Material:** Aluminum

#### Key Features
- Complete dust and water protection
- Excellent heat dissipation via aluminum construction
- Available for GigE, 5GigE, CoaXPress, USB 3.0 interfaces

#### Assessment
**Pros:** High-quality industrial solution
**Cons:** Designed for specific Basler cameras only, not adaptable to generic USB boards, price unknown but likely above budget

---

### 1.4 Entaniya WC-01 All-Weather Camera Case

**Product:** WC-01 Waterproof Case for Raspberry Pi Camera Modules
**Manufacturer:** Entaniya
**Website:** https://e-products.entaniya.co.jp

#### Specifications
- **Internal Dimensions:** Fits 24x25mm PCB camera modules (Raspberry Pi Camera V2/V3)
- **IP Rating:** IP67 equivalent
- **Price:** Not clearly listed; available on Amazon Japan, The Pi Hut, DigiKey (obsolete)
- **Optical Window:** Highly transparent, low-distortion dome cover
- **Mounting:** Included (various mounting hardware available)

#### Key Features
- ASA resin construction (UV resistant, weather durable)
- O-ring seal between dome and base
- Dome-shaped clear cover
- Minimal image distortion

#### Compatibility
- Raspberry Pi Camera Module V2, V3, V3 Wide
- Raspberry Pi AI Camera
- Sony SPRESENSE Camera Board
- **May fit some 32x38mm boards if PCB size is close to 24x25mm**

#### Heater Integration
- **Ease:** Difficult - small internal volume, plastic construction
- Limited space for heater; would need careful placement

#### Where to Purchase
- The Pi Hut: https://thepihut.com/products/entaniya-waterproof-case-for-raspberry-pi-camera-modules
- Amazon Japan
- **Note:** DigiKey lists as obsolete/discontinued

#### Assessment
**Pros:** Purpose-built for Pi cameras, proven IP67 equivalent rating, transparent dome
**Cons:** Too small for most 32-38mm boards, availability uncertain, likely above budget, limited heater space

---

### 1.5 ELP Pre-Built Weatherproof Cameras

**Product:** Outdoor Waterproof IP67 Rated Dome USB Camera
**Manufacturer:** ELP/SVPRO
**Website:** https://www.svpro.cc, https://elpcctv.com

#### Specifications
- **Model:** ELP-USBFHD01M-DL36 (and similar)
- **IP Rating:** IP67
- **Price:** $47.25 (complete camera with housing)
- **Features:** 1080P, 30/60/120fps, OV2710 CMOS sensor, night vision IR LEDs

#### Key Features
- Pre-assembled camera with weatherproof dome housing
- Vandal-resistant design
- USB interface
- Day/night vision capability

#### Assessment
**Pros:** Complete solution in budget, proven weatherproof design, ready to deploy
**Cons:** Fixed camera module (can't use with existing ELP/Arducam boards), limited customization

**Note:** ELP also offers "Mini Housing for ELP USB Camera Module" on AliExpress - specific for their board cameras, but dimensions/pricing unclear

---

### 1.6 Arducam Waterproof Metal Cases

**Product:** USB Camera Modules with Waterproof Metal Case
**Manufacturer:** Arducam
**Website:** https://www.arducam.com

#### Available Options

**Option A: 2MP IMX291 Low Light USB Camera with Waterproof Metal Case**
- 120° wide angle fixed focus M12 lens
- Metal case provides protection and heat dissipation
- Compatible with Windows, Linux, Android, Mac OS
- **Price:** Check Arducam website or Amazon

**Option B: 8MP IMX179 Autofocus USB Camera with Metal Case**
- 3264×2448 resolution
- Sturdy metal housing for protection and heat dissipation
- Suitable for home surveillance, 3D printer monitoring, object recognition

#### Key Features
- Metallic housing for durability
- Various lens options
- Waterproof and fog-proof options available
- Custom IP6x waterproof solutions available

#### Assessment
**Pros:** Purpose-built for Arducam boards, proven designs, good heat dissipation
**Cons:** Complete camera packages (can't use housing separately with other boards), pricing not fully clear, may be above budget

---

### 1.7 Dotworkz BASH IP68 Housing

**Product:** BASH Rugged Security Camera Housing
**Manufacturer:** Dotworkz
**Website:** https://dotworkz.com/bash-ip68-camera-housing/

#### Specifications
- **IP Rating:** IP68, IK10+ (vandal resistant)
- **Price:** Not listed (likely well above $60)
- **Compatibility:** Mini PTZ cameras, AI cameras, 360° cameras

#### Key Features
- Compact, ultra-durable
- Aluminum rear plate acts as thermal heat sink
- 2024 Product of the Year
- Built for transit, law enforcement, marine applications

#### Assessment
**Pros:** Extreme durability, IP68 rating
**Cons:** Designed for complete cameras not board modules, likely expensive ($100+), overkill for humanitarian deployment

---

## 2. ADAPTABLE ENCLOSURES

### 2.1 LeMotech Transparent Junction Boxes

**Product:** IP67 Waterproof Junction Box with Clear Cover
**Manufacturer:** LeMotech
**Website/Retailer:** Amazon (various sellers)

#### Available Sizes and Pricing

| Model | External Dimensions | Internal Dimensions (approx) | Amazon Price (est) |
|-------|-------------------|------------------------------|-------------------|
| Small | 3.9" x 3.9" x 3.0" (100x100x75mm) | ~90x90x65mm | $15-20 |
| Medium-Small | 3.3" x 3.2" x 2.2" (83x81x56mm) | ~73x71x46mm | $12-18 |
| Medium | 4.7" x 3.5" x 2.7" (120x90x68mm) | ~110x80x58mm | $18-25 |
| Large | 8.7" x 6.7" x 4.3" (220x170x110mm) | ~200x160x100mm | $30-40 |

**Product Link:** https://www.amazon.com/LeMotech-Waterproof-Dustproof-Electrical-Transparent/dp/B0CZR9C9Y5

#### Specifications
- **IP Rating:** IP67 (waterproof and dustproof)
- **Material:** ABS plastic base, polycarbonate (PC) transparent lid
- **Mounting:** Includes mounting plate, wall brackets, cable glands (1/2" NPT on some models)
- **Lid:** Hinged clear cover with stainless steel latch

#### Key Features
- High-quality ABS plastic (impact resistant)
- Transparent lid allows visual inspection without opening
- Hinged design for easy access
- Pre-installed mounting plate
- Cable glands for sealed cable entry
- Suitable for indoor/outdoor use

#### Heater Integration
- **Ease:** Excellent - ample internal space in all sizes
- Can easily mount 20x70mm silicone heater pad
- Mounting plate provides attachment point
- Sufficient airspace to prevent overheating

#### Modifications Needed
1. **Optical Window:** Need to cut/drill hole in front for camera lens
   - Use hole saw matching lens diameter
   - Install clear acrylic or glass window with silicone seal
   - Alternatively, position camera behind existing clear lid (may limit viewing angle)
2. **Camera Mounting:** Use internal mounting plate or custom bracket
3. **Cable Management:** Use included cable glands for USB cable

#### Best Size for 32-38mm Boards
- **Recommended:** Small (100x100x75mm) or Medium (120x90x68mm)
- Provides room for camera board, heater pad, and air circulation
- Not oversized for pole/wall mounting

#### Customer Reviews
- Positive feedback on build quality
- Easy to drill/modify without cracking
- Good seal integrity
- Clear lid useful for viewing status LEDs

#### Assessment
**Pros:** Budget-friendly ($15-25), readily available on Amazon, easy to modify, good internal space, includes mounting hardware
**Cons:** Requires DIY modification for lens port, not purpose-built for cameras, no built-in anti-fog features

---

### 2.2 Polycase IP67 Enclosures

**Product:** IP67 Rated Waterproof Boxes (various series)
**Manufacturer:** Polycase
**Website:** https://www.polycase.com/ip67-enclosures

#### Key Series

**WC Series (Clear Cover Options)**
- **WC-28:** Gray base with clear cover
- **WC-44:** Outdoor enclosure with clear cover
- Multiple size options available
- Polycarbonate construction
- UV-stable material

#### Specifications
- **IP Rating:** IP67 (some models IP68)
- **Material:** Polycarbonate or aluminum
- **Price Range:** Varies by model ($30-80+)
- **Features:** Wall mount flanges, transparent covers, optional powder coat finish

#### Key Features
- Molded from UV-stable polycarbonate
- Designed for outdoor use
- Waterproof and UV-resistant
- Various configuration options
- Made in USA

#### Availability
- Direct from Polycase website
- Distributors (check website for list)

#### Assessment
**Pros:** High-quality USA-made, excellent UV resistance, proven IP67 rating
**Cons:** Pricing often above $60, requires modification for camera lens, need to verify specific dimensions for each model

---

### 2.3 Hammond IP67 Enclosures

**Product:** 1554 and 1555F Series Polycarbonate Enclosures
**Manufacturer:** Hammond Manufacturing
**Website:** https://www.hammfg.com

#### 1555F Series

**Size Range:** Six sizes from 4.7" x 2.60" x 1.65" (120x66x42mm) to 6.30" x 3.60" x 2.44" (159x91x62mm)

**Specifications:**
- **IP Rating:** IP66, IP67, IP68 (independently tested)
- **NEMA Rating:** Type 4, 4X, 6, 6P, 12, 13
- **Material:** Gray polycarbonate (UL94-5VA), clear/smoked lids (UL94V-0)
- **Gasket:** One-piece high-temperature silicone (replaceable)
- **Mounting:** Wall-mount for PCB or DIN rail

**Where to Purchase:**
- DigiKey: https://www.digikey.com/en/product-highlight/h/hammond/1555f-series-ip67-sealed-enclosures
- Other electronics distributors

#### 1554 Series

**Specifications:**
- **IP Rating:** IP66, IP67, IP68 (independently tested)
- **NEMA Rating:** Type 4, 4X, 6, 6P, 12, 13
- **Lid Options:** Gray, clear, or smoked polycarbonate lids
- **Construction:** Gasketed lid with two-piece tongue and groove
- **Gasket:** Replaceable one-piece silicone

**Example Model:**
- 1554VB2GY: 240x160x120mm
- Available from Farnell/CPC and other distributors

#### Key Features
- Exceptionally high IP ratings (tested to IP68)
- High-quality silicone gaskets
- Clear lid options available
- Tongue and groove construction for reliable sealing
- Protection against oil, dust, and water

#### Pricing
- Varies by size and distributor
- Generally $40-100+ depending on model
- Check DigiKey, Newark, Mouser for current pricing

#### Assessment
**Pros:** Excellent IP ratings, clear lid options available, high quality, readily available through major distributors
**Cons:** Often above budget, requires modification for lens port, smallest sizes may be tight for 38mm boards + heater

---

### 2.4 Generic IP67 Junction Boxes (eBay, AliExpress)

**Products:** Various IP67 waterproof electrical junction boxes with clear covers
**Sources:** eBay, AliExpress, Amazon (various sellers)

#### Typical Specifications
- **IP Rating:** IP67
- **Material:** ABS base, polycarbonate clear lid
- **Sizes:** Wide range (50x50mm to 300x200mm+)
- **Price Range:** $8-30 depending on size
- **Features:** Hinged clear lid, waterproof polycarbonate construction, UV stabilized

#### Key Features
- Very affordable
- Many size options
- Similar construction to name-brand boxes
- Often include mounting hardware and cable glands

#### Considerations
- Quality can vary by seller
- May not have independently tested IP rating
- Shipping times can be long (especially AliExpress)
- Less reliable customer support

#### Assessment
**Pros:** Very budget-friendly, wide selection
**Cons:** Variable quality, unverified IP ratings, longer shipping, requires same modifications as other junction boxes

---

### 2.5 Europa IP67 Adaptable Box

**Product:** 320 x 240 x 180mm IP67 Adaptable Box with Clear Lid
**Manufacturer:** Europa
**Website:** https://www.europa-plc.com

#### Specifications
- **Dimensions:** 320 x 240 x 180mm (large)
- **IP Rating:** IP67, IK10 protection
- **Lid:** Clear polycarbonate with quick-turn screws
- **Features:** Hinged lid, easy installation

#### Assessment
**Pros:** High impact resistance (IK10), clear lid
**Cons:** Too large for camera housing application, overkill for project needs

---

## 3. DIY-FRIENDLY OPTIONS

### 3.1 Halogen Floodlight Housing Conversion

**Approach:** Repurpose old halogen floodlight housings as camera enclosures
**Source:** Hardware stores, recycled fixtures

#### Specifications
- **IP Rating:** Many outdoor floodlights are IP65-IP67
- **Material:** Typically aluminum or heavy plastic
- **Cost:** $10-30 for new fixture, free for recycled
- **Optical Window:** Existing glass front (may need replacement with clear glass/acrylic)

#### Conversion Process
1. Remove electrical components (socket, wiring)
2. Clean interior thoroughly
3. Install camera mounting bracket
4. Seal cable entry points
5. Optionally replace/modify front glass for optimal camera view

#### Heater Integration
- **Ease:** Good - ample internal space, metal housing conducts heat
- Existing fixture may have heat dissipation features

#### Assessment
**Pros:** Very affordable, readily available, metal construction for heat dissipation, already weatherproofed
**Cons:** Requires significant modification, may be bulky, appearance not professional, existing glass may affect image quality

**Project Example:** Mentioned on Raspberry Pi forums and DIY blogs
**Source:** https://www.raspberrypi.org/forums/viewtopic.php?t=51187

---

### 3.2 PVC Pipe Enclosures

**Approach:** Build custom weatherproof housing from PVC pipe and fittings
**Materials:** PVC drain pipe, end caps, clear acrylic/glass lens port

#### Design Options

**Option A: Simple PVC Tube**
- **Materials:**
  - 3" PVC drain pipe (5' section ~$10)
  - PVC end cap ($2-5)
  - 72mm UV filter or clear acrylic disc ($5-15)
  - PVC glue ($5)
  - Clear silicone sealant ($5)
- **Total Cost:** $15-25

**Construction:**
1. Cut PVC pipe to desired length (6-12")
2. Mount camera inside using brackets or foam
3. Glue UV filter or acrylic to one end for optical window
4. Use rubber end cap or threaded cleanout for access
5. Seal cable entry with silicone/cable gland

**Option B: Compact Underwater Housing Style**
- **Materials:**
  - 1.5" PVC pipe (4.5" section)
  - 1.5" end cap
  - 1.5" threaded clean out
  - 10mm thick acrylic sheet
  - PVC adhesive + JB Weld epoxy
- **Total Cost:** $10-20

**Construction:**
1. Cut hole in end cap for acrylic window
2. Epoxy acrylic to end cap
3. Mount camera inside
4. Use threaded cleanout for weatherproof access

#### Heater Integration
- **Ease:** Excellent - lots of internal space
- Can easily mount heater pad to inside wall
- PVC provides electrical insulation

#### Assessment
**Pros:** Very affordable ($10-25), highly customizable, available at any hardware store, easy to work with
**Cons:** DIY construction (not certified IP rating), appearance is utilitarian, requires careful sealing, acrylic lens may scratch

**Project Examples:**
- PVC camera housing: https://k1vra.com/projects/camera/
- Compact PVC underwater housing: https://www.instructables.com/A-Compact-PVC-Camera-Uderwater-Enclosure/

---

### 3.3 3D Printable Camera Housings

**Approach:** Design and print custom weatherproof camera enclosures
**Sources:** Thingiverse, Printables, STLFinder, custom design

#### Available Designs

**Option A: Customizable IP65/IP67 Electronics Case**
- **Source:** Printables.com - https://www.printables.com/model/72839
- **Features:**
  - Highly scalable parametric design
  - OpenSCAD customization
  - Groove and ridge for silicone sealing cord (1-3mm diameter)
  - Designed for IP65/IP67 standards
- **Material:** ABS recommended for weather resistance
- **Sealing:** Requires silicone cord gasket

**Option B: Unifi G3 Camera Outdoor Housing**
- **Source:** Printables.com - https://www.printables.com/model/80980
- **Features:**
  - Remix of weatherproof designs
  - Clear acrylic window (2mm thick)
  - Epoxy sealing
- **Material:** ABS or PETG

**Option C: Generic Camera Enclosures**
- **Sources:** Thingiverse, STLFinder, Cults3D
- **Options:** 157,725+ camera enclosure models on STLFinder
- Many designs for Raspberry Pi cameras that could be adapted

#### Material Requirements
- **Filament:** ABS (best weather resistance) or PETG
- **Post-Processing:** May need acetone vapor smoothing (ABS) or epoxy coating for water resistance
- **Window:** 2mm clear acrylic or polycarbonate sheet
- **Sealing:** Silicone gasket cord, epoxy adhesive

#### Printing Considerations
- Layer adhesion critical for waterproofing
- 100% infill or thick walls recommended
- Print orientation affects water resistance
- Post-processing usually required for true IP67

#### Heater Integration
- **Ease:** Excellent - design can include heater mounting features
- Can customize internal geometry for optimal heater placement

#### Cost Estimate
- **Filament:** $5-10 per enclosure
- **Clear acrylic window:** $3-8
- **Gasket material:** $5-10
- **Total:** $15-30 (excluding printer)

#### Assessment
**Pros:** Highly customizable, can be optimized for exact camera size, low material cost, iterative design possible
**Cons:** Requires 3D printer access, achieving true IP67 rating difficult, time-intensive, post-processing needed, ABS printing requires heated chamber

**Note:** Most 3D printed designs require additional waterproofing measures (epoxy coating, gaskets) to achieve IP67 equivalent protection.

---

### 3.4 Garden Lamp/Outdoor Light Conversion

**Approach:** Repurpose inexpensive outdoor garden lights/lamps as camera housings
**Source:** Hardware stores, discount retailers

#### Process
- Similar to floodlight conversion
- Remove light socket and wiring
- Install camera mount
- Modify or replace front glass/lens
- Seal cable entries

#### Cost
- $10-30 for suitable outdoor light fixture

#### Assessment
**Pros:** Affordable, already weatherproofed, often aesthetically acceptable
**Cons:** Limited internal space in some models, requires modification, variable quality

**Project Example:** Instructables - "Outdoor IP Camera Housing from garden lamps"
**Source:** https://www.instructables.com/Outdoor-IP-Camera-Housing-from-garden-lamps/

---

## 4. ANTI-FOG HEATER SOLUTIONS

### 4.1 Silicone Heating Elements

**Product:** Camera Lens Anti-Fog Heater - Silicone Heating Pad
**Manufacturers:** Keenovo, Hongtai, others

#### Keenovo Specifications
- **Size:** 20mm x 70mm
- **Power:** 10W @ 12V
- **Price:** ~$15-25
- **Features:**
  - 3M adhesive backing
  - 0.5m power cable
  - Suitable for GoPro and small camera lenses

**Website:** https://keenovo.store/products/keenovo-tiny-small-silicone-heating-element-camera-lens-anti-fog-heater-20mm-x-70mm-10w-12v

#### Hongtai Specifications
- **Material:** Silicone rubber with heating wire
- **Thickness:** 1.5-4mm maximum
- **Features:**
  - 3M adhesive backing
  - Certifications: RoHS, ISO9001, CE
  - Custom sizes available

**Website:** https://hongtai.en.made-in-china.com

#### Installation in Housing
1. Clean mounting surface
2. Apply heater to camera front near lens or inside housing near window
3. Route power cable to control circuit
4. Connect to 12V power supply
5. Optional: Use thermostat for temperature control

#### Power Requirements
- 10W @ 12V = 0.83A
- 20W @ 12V = 1.67A
- Compatible with typical 12V DC systems

#### Assessment
**Pros:** Inexpensive ($15-25), easy to install, low power consumption, proven anti-fog technology
**Cons:** Requires power management, adds to system complexity, may need thermostat for temperature control

---

### 4.2 USB Lens Heaters/Warmers

**Products:** USB-powered lens warmers for photography
**Brands:** Neewer, Losharp, generic brands

#### Neewer USB Lens Heater
- **Lengths:** 12"/300mm, 16"/400mm, 20"/500mm
- **Power:** USB powered
- **Features:**
  - Wrap-around design
  - Adjustable strap
  - Eliminates dew, fog, condensation
- **Price:** ~$20-30

**Website:** https://neewer.com/products/neewer-usb-lens-heater-for-dslr-camera-and-telescope-66602321

#### Losharp USB Lens Heater
- **Features:**
  - Fast startup (5 seconds)
  - Maximum temperature: 122°F (50°C)
  - USB powered (compatible with power banks)
  - Prevents freezing, fog, dew
- **Price:** ~$15-25

**Available:** Amazon and photography retailers

#### Applicability to RC-Box
- Designed for camera lenses, not enclosures
- Could potentially wrap around small housing
- USB power convenient for Raspberry Pi integration

#### Assessment
**Pros:** Readily available, USB powered (easy integration), proven anti-fog performance
**Cons:** Designed for external lens use (not internal housing), may not fit small enclosures, less precise than fixed heater pads

---

### 4.3 Built-in Camera Heater Features

**Approach:** Some security cameras include built-in heaters

#### Examples
- eufy eufyCam S3 Pro (IP67 with environmental controls)
- Various CCTV cameras with heater/blower options

#### Automotive ADAS Camera Heaters
**Manufacturer:** Oribay Group
**Product:** Printed heated foils for windshield-mounted ADAS cameras
**Features:**
  - Custom heating solution
  - Integrated into glass during production
  - Keeps lens free of moisture, ice, fog

**Website:** https://oribay.com/automotive/windshield/electronics/heaters/

#### Assessment
- Not directly applicable to board camera housing project
- Demonstrates various anti-fog heating approaches
- Custom solutions possible for larger deployments

---

### 4.4 Anti-Fog Recommendations for RC-Box

**Best Approaches:**

1. **Silicone Heater Pad (Recommended)**
   - Use Keenovo 20x70mm, 10W @ 12V ($15-25)
   - Mount inside housing near optical window
   - Connect to 12V supply with simple on/off control or thermostat
   - Adequate for most fog conditions

2. **Desiccant Packets**
   - Include silica gel packets inside housing
   - Change during maintenance visits
   - Low-cost backup to heater
   - Useful for humidity control

3. **Pressure Equalization**
   - Include small vent with Gore-Tex membrane
   - Prevents pressure differential that can draw moisture
   - Reduces condensation risk

4. **Lens Coating**
   - Apply anti-fog coating to optical window
   - Inexpensive additional measure
   - Reduces but doesn't eliminate fogging

**Combined Approach:**
- 10W silicone heater + desiccant packet + pressure vent = most reliable anti-fog system
- Total added cost: ~$20-30 per housing

---

## 5. RECOMMENDED SOLUTIONS BY BUDGET

### Budget Option 1: LeMotech Junction Box (~$20 total)

**Housing:** LeMotech IP67 Junction Box (Small or Medium)
**Price:** $15-25 on Amazon
**Link:** https://www.amazon.com/LeMotech-Waterproof-Dustproof-Electrical-Transparent/dp/B0CZR9C9Y5

**Additional Components:**
- Clear acrylic window (cut to size): $3-5
- Silicone sealant: $5
- Optional: Keenovo 10W heater: $15-25
- **Total:** $23-60

**Modifications Required:**
1. Cut/drill hole for camera lens
2. Install clear acrylic window with silicone seal
3. Mount camera board to internal mounting plate
4. Install heater pad (optional)
5. Route USB cable through cable gland

**Assessment:**
- **Best for:** Budget-conscious deployments, field testing
- **Pros:** Affordable, readily available, easy to modify, includes mounting hardware
- **Cons:** Requires DIY skills, not as elegant as purpose-built solutions

---

### Budget Option 2: PVC Pipe Housing (~$15-25 total)

**Housing:** 3" PVC drain pipe + fittings
**Materials Cost:** $15-25

**Components:**
- 3" PVC drain pipe (cut to length): $10
- End cap: $3
- 72mm UV filter or acrylic disc: $5-10
- PVC glue + silicone: $10
- Optional: Keenovo 10W heater: $15-25
- **Total:** $28-50 (with heater)

**Construction:**
- Full DIY build following online tutorials
- Requires basic tools (saw, drill)

**Assessment:**
- **Best for:** Maximum customization, very low budget
- **Pros:** Extremely affordable, highly customizable, materials universally available
- **Cons:** Most DIY effort required, least professional appearance, no certified IP rating

---

### Mid-Range Option: 3D Printed Custom Housing (~$15-30 materials)

**Housing:** Custom 3D printed enclosure (ABS or PETG)

**Requirements:**
- Access to 3D printer
- OpenSCAD or CAD skills (or use existing designs)

**Materials:**
- Filament: $5-10
- Clear acrylic window: $3-8
- Silicone gasket cord: $5-10
- Heater pad: $15-25
- **Total:** $28-55

**Design Sources:**
- Printables: https://www.printables.com/model/72839 (customizable IP67 case)
- Thingiverse: Multiple camera housing designs
- Custom design using OpenSCAD

**Assessment:**
- **Best for:** Deployments with 3D printing access, iterative prototyping
- **Pros:** Optimized for exact camera size, can include custom features, low material cost
- **Cons:** Requires printer access and skills, post-processing needed, uncertain IP rating

---

### Premium Option: VA Imaging Housing (~$270)

**Housing:** VA Imaging Machine Vision Camera Housing (XL version for 38mm boards)
**Price:** €249 (~$270)
**Link:** https://va-imaging.com/products/machine-vision-aluminium-camera-housing-enclosure-waterproof-ip67

**Additional Components:**
- Custom adapter plate for USB camera board: Custom fabrication required
- Heater (optional - aluminum body helps): $15-25
- **Total:** $270-300+

**Assessment:**
- **Best for:** Professional deployments, long-term reliability critical
- **Pros:** Certified IP67, excellent build quality, superior heat dissipation, 3-year warranty
- **Cons:** Above budget, requires custom adapter, designed for industrial cameras

---

### Alternative: ELP Pre-Built Camera (~$47)

**Product:** ELP Outdoor Waterproof IP67 Dome USB Camera (complete unit)
**Price:** $47.25
**Link:** https://www.svpro.cc/product/svpro-outdoor-waterproof-ip67-rated-camera-1080p-full-hd-night-vision-cctv-surveillance-mini-high-speed-30-60-120fps-ov2710-cmos-dome-usb-camera/

**Assessment:**
- **Best for:** Quick deployment, no DIY required
- **Pros:** Complete solution in budget, proven design, ready to use
- **Cons:** Can't use with existing camera boards, limited to ELP camera specs

---

## 6. FINAL RECOMMENDATIONS FOR RC-BOX PROJECT

### Primary Recommendation: LeMotech Junction Box Solution

**Why This Solution:**

1. **Budget-Friendly:** $23-60 per housing (with heater), well within $15-60 range
2. **Readily Available:** Amazon Prime delivery, no specialized suppliers
3. **Field Serviceable:** Simple construction, easy to repair/replace
4. **Good Internal Space:** Room for 32-38mm boards, heater, air circulation
5. **Proven IP67 Rating:** Manufactured with certified IP67 protection
6. **Includes Mounting:** Comes with brackets and cable glands
7. **DIY-Friendly:** Requires only basic tools (drill, hole saw, silicone)

**Recommended Model:**
- LeMotech Medium size (4.7" x 3.5" x 2.7" / 120x90x68mm)
- Provides adequate space without being oversized
- Price: ~$18-25

**Complete Bill of Materials:**
1. LeMotech junction box: $20
2. Clear acrylic disc (3" diameter, 3mm thick): $5
3. Silicone sealant: $5
4. Keenovo 20x70mm 10W heater: $20
5. Silica gel desiccant packet: $2
6. **Total per housing:** $52

**Assembly Instructions Summary:**
1. Drill hole in front of box matching camera lens diameter
2. Cut acrylic disc slightly larger than hole
3. Apply silicone sealant around hole
4. Press acrylic disc in place, ensure good seal
5. Let cure 24 hours
6. Mount camera board to internal mounting plate using standoffs
7. Attach heater pad near acrylic window
8. Route USB cable through cable gland
9. Install desiccant packet
10. Close and latch lid
11. Test seal by submerging in water (without electronics)

---

### Secondary Recommendation: PVC Pipe Solution

**Best for:** Extremely tight budgets or locations where junction boxes unavailable

**Cost:** $15-25 (housing), $28-50 (with heater)

**Advantages:**
- Materials available at any hardware store globally
- Highly customizable dimensions
- Very low cost
- Proven in DIY camera projects

**Disadvantages:**
- Requires more fabrication skill
- Less professional appearance
- No certified IP rating (DIY seal quality critical)

---

### Not Recommended (But Worth Noting)

**VA Imaging Housing:**
- Excellent quality but above budget
- Consider for future "premium" RC-Box variant

**3D Printed Solutions:**
- Useful for prototyping
- Not recommended for field deployment due to uncertain waterproofing

**Hammond/Polycase Boxes:**
- Good quality but often above $60
- Similar to LeMotech but higher cost without clear advantages for this application

---

## 7. PROCUREMENT SOURCES SUMMARY

### Recommended Suppliers

| Component | Supplier | Link | Availability |
|-----------|----------|------|--------------|
| LeMotech Junction Box | Amazon | [Search Link](https://www.amazon.com/s?k=LeMotech+IP67+junction+box) | Prime shipping |
| Keenovo Heater Pad | Keenovo Store | https://keenovo.store | Direct order |
| PVC Pipe & Fittings | Local hardware | Home Depot, Lowe's, etc. | Universal |
| Clear Acrylic Sheet | Amazon, TAP Plastics | [Amazon Acrylic](https://www.amazon.com/s?k=clear+acrylic+sheet) | Widely available |
| Silicone Sealant | Local hardware | Any hardware store | Universal |
| Desiccant Packets | Amazon | [Search Link](https://www.amazon.com/s?k=silica+gel+packets) | Widely available |

### Alternative Suppliers (If Budget Allows)

| Product | Supplier | Link | Price Range |
|---------|----------|------|-------------|
| VA Imaging Housing | VA Imaging | https://va-imaging.com | €249 (~$270) |
| Polycase Enclosures | Polycase | https://www.polycase.com/ip67-enclosures | $40-100+ |
| Hammond Enclosures | DigiKey, Newark, Mouser | [DigiKey Hammond](https://www.digikey.com) | $40-100+ |
| Entaniya WC-01 | The Pi Hut | https://thepihut.com | Price TBD |

---

## 8. TESTING & VALIDATION RECOMMENDATIONS

### IP67 Rating Verification

Even with certified enclosures, modifications (drilling holes, adding windows) may compromise IP rating. Recommend field testing:

**Water Immersion Test:**
1. Assemble housing without electronics
2. Place tissue paper inside
3. Submerge in water 1 meter deep for 30 minutes
4. Check for moisture on tissue paper
5. Repeat test after any modifications

**Dust Test:**
1. Expose housing to fine dust/sand for extended period
2. Open and inspect for ingress
3. Especially important for cable gland sealing

### Heater Performance Test

**Anti-Fog Validation:**
1. Place housing in refrigerator overnight
2. Remove and expose to warm, humid air
3. Observe fogging on optical window
4. Activate heater and measure time to clear
5. Monitor temperature to ensure safe operating range

**Power Consumption:**
- Measure actual power draw of heater
- Calculate battery impact for solar/battery systems
- Consider thermostat control to reduce power usage

---

## 9. CONSIDERATIONS FOR HUMANITARIAN DEPLOYMENT

Based on CLAUDE.md project requirements, housing solution must address:

### Field Serviceability
- **LeMotech Solution:** Excellent - common tools, replaceable components
- **PVC Solution:** Good - materials universally available
- **VA Imaging:** Poor - requires specialized parts

### Resilience to Shipping/Handling
- **LeMotech:** Good - ABS plastic durable but may crack if dropped
- **PVC:** Excellent - very impact resistant
- **VA Imaging:** Excellent - aluminum construction

### Local Procurement
- **LeMotech:** Amazon available in most countries, or similar IP67 boxes locally
- **PVC:** Available anywhere with plumbing supplies
- **VA Imaging:** Requires international shipping

### Training Requirements
- **LeMotech:** Minimal - basic DIY skills
- **PVC:** Moderate - cutting, sealing techniques
- **VA Imaging:** Minimal (pre-built) but camera installation requires care

### Recommendation for Humanitarian Context

**Best Approach:** Pre-assemble LeMotech housings before shipping

**Pre-Deployment Preparation:**
1. Assemble housing with optical window
2. Test waterproofing
3. Install heater pad
4. Package with camera board (not installed)
5. Include simple installation instructions with photos
6. Ship with spare housing and consumables (sealant, desiccant)

**On-Site Assembly:**
1. Install camera board to mounting plate (4 screws)
2. Connect heater power (2 wires)
3. Route USB cable through gland
4. Close lid and latch
5. Mount to bracket/pole

**Advantages:**
- Reduces on-site complexity
- Allows pre-testing in controlled environment
- Easier quality control
- Minimizes risk of assembly errors in field

---

## 10. LONG-TERM CONSIDERATIONS

### Maintenance Schedule

**Monthly (Remote Visual Check):**
- Verify camera image quality
- Check for fogging or condensation
- Monitor heater operation

**Quarterly (Physical Inspection):**
- Clean optical window
- Check seal integrity
- Inspect for cracks or damage
- Replace desiccant packet
- Verify mounting security

**Annually:**
- Full disassembly and inspection
- Replace gaskets/seals if needed
- Deep clean all components
- Re-test waterproofing

### Spare Parts Kit (Per Deployment)

**Minimum:**
- 1x complete spare housing
- 2x optical window (acrylic disc)
- 1x tube silicone sealant
- 5x desiccant packets
- 2x cable glands
- 1x spare heater pad

**Estimated Cost:** $75-100

### Upgrades/Improvements

**Future Enhancements:**
1. **Thermostat Control:** Add temperature sensor + relay for heater efficiency
2. **Ventilation:** Install Gore-Tex vent for pressure equalization
3. **Lens Wiper:** Mechanical wiper for cleaning (complex but useful)
4. **Anti-Reflective Coating:** Apply to optical window for better image quality
5. **Sun Shield:** External shade to reduce heating and glare

---

## APPENDIX A: SIZING GUIDE

### Camera Board Dimensions Reference

| Manufacturer | Model | PCB Size (mm) | Will Fit In |
|--------------|-------|---------------|-------------|
| ELP | Various USB modules | ~32x32 to 38x38 | LeMotech Small/Medium, PVC 3" |
| Arducam | Most USB modules | ~25x24 to 38x38 | LeMotech Small/Medium, PVC 3" |
| Raspberry Pi | Camera Module V3 | 25x24 | Entaniya WC-01, LeMotech Small |
| Generic | Board cameras | 32x32 standard | LeMotech Small/Medium |

### Housing Size Selection

**For 32x32mm boards:**
- LeMotech Small (100x100x75mm) - adequate
- 3" PVC pipe - adequate

**For 38x38mm boards:**
- LeMotech Medium (120x90x68mm) - recommended
- 3" PVC pipe - tight but workable

**With heater (20x70mm):**
- LeMotech Medium or larger - recommended
- 3" PVC with careful layout - workable

---

## APPENDIX B: ANTI-FOG SYSTEM DESIGN

### Heating Requirements Calculation

**Assumptions:**
- Optical window area: ~50 cm²
- Target temperature differential: 10°C above ambient
- Heat loss to environment: ~2W per 10cm² at 10°C differential

**Estimated Heat Required:**
- Minimum: 5W (light fogging prevention)
- Moderate: 10W (typical conditions)
- Heavy: 15-20W (extreme humidity/cold)

**Recommendation:** 10W heater adequate for most deployments

### Heater Placement

**Option 1: Near Optical Window (Recommended)**
- Mount heater pad 5-10mm from acrylic window
- Prevents fog formation directly on camera lens view
- Most efficient anti-fog solution

**Option 2: On Housing Wall**
- Mount to side or back of housing
- Heats entire enclosure volume
- Good for general moisture control

**Option 3: On Camera PCB (Not Recommended)**
- Could damage camera electronics
- Inefficient for anti-fog
- Risk of overheating sensor

### Power Control Options

**Manual On/Off:**
- Simple switch
- User controlled
- Wastes power when not needed

**Thermostat:**
- Temperature sensor + relay
- Activates heater only when needed
- Saves significant power
- Added cost: $10-15

**Humidity Sensor:**
- RH sensor + microcontroller
- Most sophisticated approach
- Optimal power efficiency
- Added cost: $20-30

**Recommendation for RC-Box:**
- Start with manual control or simple thermostat (set to activate below 5°C)
- Monitor power consumption
- Upgrade to humidity sensing if power budget allows

---

## APPENDIX C: USEFUL LINKS & RESOURCES

### Commercial Products

**VA Imaging:**
- Main site: https://va-imaging.com/collections/enclosures-ip67-cameras
- US site: https://va-imaging.us/

**Entaniya:**
- Product page: https://e-products.entaniya.co.jp/en/list/raspberry-pi/interchangeable-lens-camera-module/waterproof-case-for-raspberrypi-v2-camera-module/
- The Pi Hut: https://thepihut.com/products/entaniya-waterproof-case-for-raspberry-pi-camera-modules

**LeMotech:**
- Amazon store: https://www.amazon.com/s?k=LeMotech+IP67
- Direct: https://lemotech.com/

**Polycase:**
- IP67 Enclosures: https://www.polycase.com/ip67-enclosures
- Clear cover options: https://www.polycase.com/clear-cover-enclosures

**Hammond:**
- 1554 Series: https://www.hammfg.com/electronics/small-case/plastic/1554
- 1555F Series: https://www.hammfg.com/electronics/small-case/plastic/1555f

### Heater Suppliers

**Keenovo:**
- Camera heater: https://keenovo.store/products/keenovo-tiny-small-silicone-heating-element-camera-lens-anti-fog-heater-20mm-x-70mm-10w-12v

**Neewer:**
- USB lens heater: https://neewer.com/products/neewer-usb-lens-heater-for-dslr-camera-and-telescope-66602321

### DIY Guides

**PVC Camera Housing:**
- K1VRA guide: https://k1vra.com/projects/camera/
- Instructables underwater housing: https://www.instructables.com/A-Compact-PVC-Camera-Uderwater-Enclosure/

**Garden Lamp Conversion:**
- Instructables: https://www.instructables.com/Outdoor-IP-Camera-Housing-from-garden-lamps/

**3D Printing:**
- Customizable IP67 case: https://www.printables.com/model/72839-customizable-parametric-stable-and-waterproof-elec
- Unifi housing: https://www.printables.com/model/80980-unifi-g3-instant-camera-outdoor-housing

### General Resources

**Raspberry Pi Forums:**
- Outdoor enclosures: https://forums.raspberrypi.com/viewtopic.php?t=51187

**Distributors:**
- DigiKey: https://www.digikey.com
- Mouser: https://www.mouser.com
- Newark: https://www.newark.com

---

## DOCUMENT CHANGELOG

**Version 1.0 - November 28, 2025**
- Initial comprehensive research completed
- Evaluated 15+ housing options across 3 categories
- Primary recommendation: LeMotech junction box solution
- Budget analysis: $23-60 per housing achievable
- Anti-fog heater integration documented

---

## SOURCES

### Machine Vision & Industrial Housings
- [VA Imaging IP67 Enclosures](https://va-imaging.com/collections/enclosures-ip67-cameras)
- [VA Imaging Machine Vision Camera Housing](https://va-imaging.com/products/machine-vision-camera-housing-enclosure-waterproof-ip67)
- [Basler IP67 Housing](https://www.baslerweb.com/en-us/accessories/ip67-housing/)
- [Components Express CEI Enclosures](https://www.componentsexpress.com/_Enclosures)
- [IP Elements Machine Vision Housings](https://www.ipelements.com/)

### Raspberry Pi Camera Solutions
- [Entaniya WC-01 Waterproof Case](https://e-products.entaniya.co.jp/en/list/raspberry-pi/interchangeable-lens-camera-module/waterproof-case-for-raspberrypi-v2-camera-module/)
- [The Pi Hut - Entaniya Case](https://thepihut.com/products/entaniya-waterproof-case-for-raspberry-pi-camera-modules)

### USB Camera Solutions
- [ELP Outdoor Waterproof Camera](https://www.svpro.cc/product/svpro-outdoor-waterproof-ip67-rated-camera-1080p-full-hd-night-vision-cctv-surveillance-mini-high-speed-30-60-120fps-ov2710-cmos-dome-usb-camera/)
- [Arducam 2MP IMX291 with Waterproof Case](https://www.arducam.com/2mp-imx291-low-light-120-wide-angle-usb-camera-module-with-waterproof-metal-case-for-windows-linux-android-and-mac-os.html)
- [Arducam 8MP IMX179 with Metal Case](https://www.arducam.com/8mp-imx179-autofocus-usb-camera-module-with-waterproof-protection-case-for-windows-linux-android-and-mac-os.html)

### Adaptable Enclosures
- [LeMotech IP67 Junction Box on Amazon](https://www.amazon.com/LeMotech-Waterproof-Dustproof-Electrical-Transparent/dp/B0CZR9C9Y5)
- [LeMotech Product Page](https://lemotech.com/product/waterproof-transparent-cover-electrical-box/)
- [Polycase IP67 Enclosures](https://www.polycase.com/ip67-enclosures)
- [Polycase Clear Cover Enclosures](https://www.polycase.com/clear-cover-enclosures)
- [Hammond 1554 Series](https://www.hammfg.com/electronics/small-case/plastic/1554)
- [Hammond 1555F Series](https://www.hammfg.com/electronics/small-case/plastic/1555f)
- [DigiKey Hammond 1555F](https://www.digikey.com/en/product-highlight/h/hammond/1555f-series-ip67-sealed-enclosures)

### DIY Solutions
- [K1VRA PVC Camera Housing](https://k1vra.com/projects/camera/)
- [Instructables - Compact PVC Underwater Housing](https://www.instructables.com/A-Compact-PVC-Camera-Uderwater-Enclosure/)
- [Instructables - Garden Lamp Camera Housing](https://www.instructables.com/Outdoor-IP-Camera-Housing-from-garden-lamps/)
- [Raspberry Pi Forum - Outdoor Enclosures](https://forums.raspberrypi.com/viewtopic.php?t=51187)
- [Printables - Customizable IP67 Case](https://www.printables.com/model/72839-customizable-parametric-stable-and-waterproof-elec)
- [Printables - Unifi Camera Housing](https://www.printables.com/model/80980-unifi-g3-instant-camera-outdoor-housing)

### Anti-Fog Heater Solutions
- [Keenovo Camera Lens Heater](https://keenovo.store/products/keenovo-tiny-small-silicone-heating-element-camera-lens-anti-fog-heater-20mm-x-70mm-10w-12v)
- [Hongtai Silicone Heating Elements](https://hongtai.en.made-in-china.com/product/tfvYWblUgMcD/China-Camera-Lens-Anti-Fog-Heater-Silicone-Heating-Element-with-3m-Adhesive-Backing.html)
- [Neewer USB Lens Heater](https://neewer.com/products/neewer-usb-lens-heater-for-dslr-camera-and-telescope-66602321)
- [Oribay ADAS Camera Heaters](https://oribay.com/automotive/windshield/electronics/heaters/)

### Security Camera Housings
- [Dotworkz BASH IP68 Housing](https://dotworkz.com/bash-ip68-camera-housing/)
- [CCTV Camera Pros IP67 Cameras](https://www.cctvcamerapros.com/IP67-Cameras-s/1757.htm)

---

**End of Report**
