# USB Camera Options for Outdoor River Monitoring with IR Night Vision

**Research Date:** January 8, 2026
**Application:** OpenRiverCam (ORC) outdoor river monitoring - Indonesia deployment
**Researcher:** Claude (Comprehensive Research Agent)

---

## Executive Summary

**Key Findings:**

1. **Critical Issue:** Most 8MP USB cameras include IR-cut filters that BLOCK infrared light, making them incompatible with 850nm IR illumination for night vision.

2. **Limited Options:** True 8MP USB cameras without IR-cut filters (NoIR versions) are rare. Most NoIR cameras use the Raspberry Pi CSI interface, not USB.

3. **Recommended Solution:** Either (a) use a 2MP USB camera with automatic IR-cut switching, or (b) contact manufacturers for custom 8MP NoIR USB cameras, or (c) use RGB-IR cameras that handle both spectrums.

4. **Budget Reality:** Meeting all requirements (8MP, USB, IR-sensitive, wide angle, under $100) is challenging. Trade-offs required.

5. **Best Match:** e-con Systems See3CAM_CU83 (8MP RGB-IR) is technically ideal but exceeds budget at $249. ELP/SVPRO 8MP cameras with standard IR filters can work with custom NoIR configuration.

---

## Research Questions Investigated

1. **Do USB cameras exist with 8MP resolution and IR sensitivity (NoIR)?**
2. **What sensors (IMX317, IMX219, IMX179) are available in USB NoIR versions?**
3. **Can standard 8MP USB cameras be modified or ordered without IR-cut filters?**
4. **What are the alternatives if 8MP NoIR USB cameras don't exist?**
5. **Which options are Linux/V4L2 compatible and work with Raspberry Pi 5?**
6. **What is the price and availability of viable options?**

---

## Understanding IR Sensitivity

### The IR-Cut Filter Problem

**Standard cameras block infrared light** using an IR-cut filter (typically 650±10nm cutoff) to produce accurate color images in daylight. This filter:
- Improves color accuracy in visible spectrum
- Prevents IR contamination of color channels
- **Blocks 850nm IR illumination needed for night vision**

### What "NoIR" Means

**NoIR = No Infrared filter**
- Sensor has no IR-cut filter, allowing IR wavelengths to pass
- Daytime photos appear reddish/magenta due to IR contamination
- Night vision works with 850nm or 940nm IR illuminators
- Used by Raspberry Pi official NoIR camera module

### Day/Night Vision Solutions

**Motorized IR-Cut Filter:**
- Mechanically moves IR filter in/out based on light levels
- Day mode: Filter IN (blocks IR, normal colors)
- Night mode: Filter OUT (allows IR, enables night vision)
- Requires photosensor and motorized mechanism
- Available in some 2MP USB cameras, rare in 8MP

**RGB-IR Separation:**
- Sensor captures both RGB and IR simultaneously
- Software separates RGB and IR frames
- No mechanical parts needed
- Example: e-con Systems See3CAM_CU83 (AR0830 sensor)

---

## Camera Options Analysis

### Option 1: 8MP RGB-IR USB Camera (Premium)

**e-con Systems See3CAM_CU83**

| Specification | Details |
|--------------|---------|
| **Sensor** | onsemi AR0830 (1/2.9", 8MP, BSI) |
| **Resolution** | 3840 × 2160 (4K) |
| **Frame Rate** | 4K @ 15fps, 1080p @ 30fps |
| **IR Capability** | RGB-IR separation (proprietary algorithm) |
| **IR-Cut Filter** | None - software separates RGB and IR |
| **Interface** | USB 3.2 Gen 1 (Type-C), backward compatible with USB 2.0 |
| **UVC Compliant** | Yes - no drivers needed |
| **Lens** | M12 mount, 80.86° H FOV (included lens) |
| **Output Format** | Uncompressed UYVY, Y16, Y8 |
| **OS Support** | Windows, Linux, Android, Mac |
| **Dynamic Range** | 73dB |
| **SNR** | 39.9dB |
| **Operating Temp** | -20°C to +65°C |
| **Size** | 30 × 30 mm |
| **Price** | **$249** (sample qty 1) |
| **Availability** | Direct from e-con Systems |

**Pros:**
- True day/night capability with no mechanical parts
- High quality sensor with BSI technology
- 4K resolution meets ORC requirements
- USB 3.0 for high frame rates
- Wide temperature range for tropical use
- UVC compliant for Linux V4L2
- Includes wake-on-motion feature

**Cons:**
- **Exceeds $100 budget significantly**
- Requires custom algorithm for RGB-IR separation
- May not provide separate IR stream (need to verify with vendor)
- Overkill for ORC's 5-second capture use case

**Recommendation:** Ideal technically, but budget prohibitive. Consider for Jakarta reference site if budget allows.

**Sources:**
- [e-con Systems See3CAM_CU83 Product Page](https://www.e-consystems.com/usb-cameras/8mp-4k-rgb-ir-usb3-camera.asp)
- [e-con Systems Launch Announcement](https://www.e-consystems.com/blog/camera/products/e-con-systems-launches-see3cam_cu83-a-4k-rgb-ir-usb-camera-delivering-stunning-visuals-day-and-night/)

---

### Option 2: 8MP USB Camera with Standard IR Filter (Requires Customization)

**ELP 8MP IMX179 USB Camera**

| Specification | Details |
|--------------|---------|
| **Sensor** | Sony IMX179 (1/3.2", 8MP) |
| **Resolution** | 3264 × 2448 @ 15fps (MJPEG) |
| **Frame Rate** | 3264×2448 @ 15fps, 1080p @ 30fps, 640×480 @ 30fps |
| **IR-Cut Filter** | **Fixed IR filter @ 650±10nm (BLOCKS IR)** |
| **IR Sensitivity** | Manufacturer states "Night vision optional, can support IR Cut and IR board for IR night vision" |
| **Interface** | USB 2.0 |
| **UVC Compliant** | Yes - plug and play |
| **Lens Options** | 2.1mm (wide), 2.8mm, 3.6mm, 5-50mm varifocal, 75°, 180° fisheye |
| **Wide Angle** | 115° (H) diagonal, 75° no-distortion, 180° fisheye available |
| **Output Format** | MJPEG, YUY2 |
| **OS Support** | Windows, Linux, Mac, Android |
| **Adjustable** | Brightness, contrast, saturation, sharpness, gamma, white balance |
| **Operating Temp** | -20°C to +70°C |
| **Board Size** | 38×38mm or 32×32mm |
| **Price** | **$57.75 - $69.50** (varies by lens) |
| **Availability** | Amazon, ELP direct (svpro.cc), AliExpress |

**Pros:**
- Meets 8MP requirement
- Wide angle options (115°-180°)
- Within budget
- UVC compliant for Linux V4L2
- Good temperature range
- OEM/ODM services available for customization

**Cons:**
- **Standard version has IR-cut filter (blocks IR)**
- Custom NoIR version requires contacting manufacturer
- USB 2.0 limits frame rate at full resolution
- Minimum illumination 0.5 lux (not great for night vision)

**Path Forward:**
Contact ELP (sales@elpcctv.com) to request:
- 8MP IMX179 camera WITHOUT IR-cut filter (NoIR version)
- Wide angle lens (115° or wider)
- Pricing for custom order
- Minimum order quantity
- Lead time

**Sources:**
- [ELP 8MP IMX179 Product Line](https://www.svpro.cc/product-category/elp-products/8mp-sony-imx179-usb-cameras/)
- [ELP High Resolution IMX179 USB Camera](https://www.svpro.cc/product/high-resolution-sony-imx179-sensor-8mp-0-5lux-mini-usb-camera-module-for-android-linux-windows-industrial-webcam-usb8mp02g-l28/)
- [Amazon ELP 8MP Wide Angle](https://www.amazon.com/ELP-Camera-Module-Resolution-8megapixel/dp/B01HD1V1Z6)

---

**SVPRO 8MP IMX179 USB Camera**

Similar to ELP (appears to be same manufacturer/OEM). Same specifications and pricing.

| Specification | Details |
|--------------|---------|
| **Sensor** | Sony IMX179 (1/3.2", 8MP) |
| **Resolution** | 3264 × 2448 @ 15fps |
| **IR-Cut Filter** | Fixed (650±10nm) - blocks IR |
| **Wide Angle** | 170° or 180° fisheye available |
| **Price** | **$57.75 - $121.80** (170° fisheye more expensive) |
| **Availability** | Amazon, SVPRO direct |

**Note:** Same customization path as ELP - contact for NoIR version.

**Sources:**
- [SVPRO 170° Fisheye USB Camera](https://www.svpro.cc/product/svpro-170degree-fisheye-lens-wide-angle-mini-security-usb-camera-module-8mp-sony-imx179-sensor/)
- [Amazon SVPRO 8MP USB Camera](https://www.amazon.com/SVPRO-Camera-Machine-Computer-Raspberry/dp/B0BW3RHVPX)

---

**Arducam 8MP IMX179 USB Camera**

| Specification | Details |
|--------------|---------|
| **Sensor** | Sony IMX179 (1/3.2", 8MP) |
| **Resolution** | 3264 × 2448 @ 30fps (max) |
| **IR-Cut Filter** | Fixed IR filter (blocks IR) |
| **Interface** | USB 2.0 |
| **UVC Compliant** | Yes |
| **Lens** | M12 mount, 115° (H) wide angle or metal case version |
| **Price** | **~$60-80** (estimate based on similar models) |
| **Availability** | Arducam.com, Amazon |

**Note:** Arducam offers NoIR versions for Raspberry Pi CSI cameras, but no USB NoIR version found in research. May be available on request.

**Sources:**
- [Arducam 8MP IMX179 Wide Angle USB Camera](https://www.arducam.com/product/8mp-imx179-usb-camera-module-with-wide-angle-115h-m12-lens-for-windows-linux-android-and-mac-os/)
- [Arducam IMX179 USB Camera with Case](https://www.arducam.com/product/arducam-imx179-usb-camera-with-case-ub022901/)

---

### Option 3: 8MP USB Camera - IMX219 Sensor

**Arducam 8MP IMX219 Autofocus USB Camera (B0292)**

| Specification | Details |
|--------------|---------|
| **Sensor** | Sony IMX219 (1/4", 8MP) |
| **Resolution** | 3280 × 2464 @ 30fps (MJPEG), 3264 × 2448 @ 15fps |
| **Frame Rate** | MJPG 15fps @ 3264×2448, 30fps @ 1080p; YUY2 15fps @ 720p |
| **IR-Cut Filter** | Standard version has IR filter |
| **Interface** | USB 2.0 |
| **UVC Compliant** | Yes - plug and play |
| **Focus** | Autofocus (40mm to infinity) |
| **FOV** | 60° (H) × 72° (D) × 47° (V) - **NOT wide angle** |
| **Features** | Microphone included |
| **OS Support** | Windows, Linux, Mac, Android |
| **Price** | **~$40-60** (Amazon pricing varies) |
| **Availability** | Amazon, Arducam direct, Newegg |

**Pros:**
- 8MP resolution
- Autofocus capability
- Within budget
- UVC compliant
- Raspberry Pi ecosystem (same sensor as Pi Camera V2)

**Cons:**
- **NOT wide angle** (60° H vs. 120° target)
- Standard version has IR filter
- Smaller sensor (1/4" vs 1/3.2" IMX179)
- No USB NoIR version found

**NoIR Availability:**
Arducam makes **8MP IMX219 NoIR cameras for Raspberry Pi CSI interface**, but NOT USB versions. CSI cameras include:
- [Arducam 8MP IMX219 NoIR for Raspberry Pi (B0395)](https://www.arducam.com/8mp-imx219-noir-for-raspberry-pi-b0395.html) - $15-25
- Wide angle NoIR version available (175° ultra-wide)

**Recommendation:** If CSI interface is acceptable (direct Pi connection, not USB), the Pi NoIR camera is viable. For USB, would need custom order.

**Sources:**
- [Arducam 8MP IMX219 Autofocus USB Camera](https://www.arducam.com/product/arducam-usb-autofocus-imx219-b0292/)
- [Amazon Arducam IMX219 USB Camera](https://www.amazon.com/Arducam-Autofocus-Microphone-Computer-Raspberry/dp/B08RHTG845)
- [Arducam 8MP IMX219 NoIR for Pi](https://www.arducam.com/8mp-imx219-noir-for-raspberry-pi-b0395.html)

---

### Option 4: 8MP USB Camera - IMX317 Sensor (4K)

**ELP 4K USB Camera IMX317**

| Specification | Details |
|--------------|---------|
| **Sensor** | Sony IMX317 (1/2.5", 8.42MP) |
| **Resolution** | 3840 × 2160 @ 30fps (4K) |
| **Technology** | BSI (Back-Side Illuminated) for better low light |
| **IR-Cut Filter** | Standard models include IR filter |
| **Interface** | USB 2.0 or USB 3.0 (varies by model) |
| **Frame Rate** | 4K @ 30fps (vs. most 8MP limited to 15fps) |
| **Lens** | 3.6mm M12 with IR filter (standard) |
| **Low Light** | Some models use STARVIS technology (0.001 lux) |
| **Price** | **~$60-90** (estimate) |
| **Availability** | Amazon, ELP direct, e-con Systems |

**Pros:**
- True 4K resolution
- 30fps at full resolution (vs. 15fps for IMX179)
- BSI technology for better low light
- Some models with STARVIS (excellent night vision with IR)

**Cons:**
- **Standard version has IR filter**
- NoIR version not found in research
- May be above $100 for STARVIS models

**Note:** e-con Systems offers an 8MP IMX317 camera (e-CAM83_USB) with HDR and dual stream support. Check if NoIR version available.

**Sources:**
- [e-con Systems 8MP IMX317 USB Camera](https://www.e-consystems.com/usb-cameras/4k-sony-imx317-8mp-usb-camera.asp)
- [Amazon ELP 4K IMX317 USB Camera](https://www.amazon.com/ELP-Camera-3840x2160-Windows-Raspberry/dp/B09BJPNHJV)

---

### Option 5: Lower Resolution with Proven IR Capability

**Arducam 2MP/2.4MP Day & Night Vision USB Camera (B0506)**

| Specification | Details |
|--------------|---------|
| **Sensor** | OV2710 (1/2.7", 2MP) |
| **Resolution** | 1920 × 1080 @ 30fps |
| **IR-Cut Filter** | **Motorized/automatic switching** |
| **IR LEDs** | 6× 850nm IR LEDs built-in |
| **Photoresistor** | Automatic day/night mode |
| **Interface** | USB 2.0 |
| **UVC Compliant** | Yes - plug and play |
| **Lens** | 105° wide-angle F1.6 starlight lens |
| **OS Support** | Windows, Linux, Mac, Android |
| **Price** | **~$60-80** |
| **Availability** | Amazon, Arducam direct |

**Pros:**
- **Proven day/night operation** with automatic IR-cut switching
- **Built-in IR illumination** (850nm LEDs)
- Wide angle (105°)
- UVC compliant
- No custom configuration needed
- Within budget

**Cons:**
- **Only 2MP resolution** (below 8MP requirement)
- May not meet ORC software requirements for 4K/8MP

**Use Case:** If ORC software can work with 1080p, this is a turnkey solution requiring no modification.

**Sources:**
- [Arducam 1080P Day & Night USB Camera](https://www.arducam.com/arducam-1080p-day-night-vision-usb-camera-2mp-infrared-webcam-with-automatic-ir-cut-switching-and-ir-leds.html)
- [Amazon Arducam Day/Night USB Camera](https://www.amazon.com/Arducam-Computer-Automatic-Switching-All-Day/dp/B0829HZ3Q7)

---

**ELP 5MP IR USB Camera (Global Shutter)**

| Specification | Details |
|--------------|---------|
| **Sensor** | 5MP global shutter |
| **IR LEDs** | 850nm built-in |
| **Lens** | 85° no-distortion |
| **Frame Rate** | 1080p @ 60fps, 1944p @ 50fps |
| **Use Case** | License plate recognition, high-speed capture |
| **Price** | **$152.25** |

**Note:** Exceeds budget but offers high frame rate for motion capture.

**Sources:**
- [ELP 5MP IR USB Camera](https://www.svpro.cc/product/5mp-ir-usb-camera-global-shutter/)

---

### Option 6: Ultra Low Light Sensors (IMX291, IMX462)

**Sony STARVIS Sensors for Night Vision**

| Sensor | Resolution | Low Light Capability | USB Availability |
|--------|-----------|---------------------|------------------|
| **IMX291** | 2MP (1080p) | 0.001 lux (STARVIS) | Yes - multiple vendors |
| **IMX462** | 2MP (1080p) | 0.0005 lux (STARVIS 2) | Limited USB options |

**e-con Systems See3CAM_CU27 (IMX462)**

| Specification | Details |
|--------------|---------|
| **Sensor** | Sony IMX462 (1/2.8", 2MP, STARVIS 2) |
| **Resolution** | 1920 × 1080 (Full HD) |
| **Frame Rate** | MJPEG 100fps @ 1080p, UYVY 60fps @ 1080p |
| **IR Sensitivity** | Near-infrared sensitive, 0 lux capability |
| **Interface** | USB 3.1 Gen 1, backward compatible USB 2.0 |
| **UVC Compliant** | Yes |
| **Low Light** | Captures at 0 lux with IR illumination |
| **Pixel Size** | 2.9 µm (large for excellent light gathering) |
| **Dynamic Range** | 120dB (DOL-HDR) |
| **Price** | **Not listed** (contact e-con Systems) |

**Pros:**
- Exceptional low-light performance
- IR sensitive (no IR-cut filter issue)
- High frame rate
- UVC compliant

**Cons:**
- Only 2MP (not 8MP)
- Price likely exceeds budget

**Sources:**
- [e-con Systems See3CAM_CU27 IMX462](https://www.e-consystems.com/usb-cameras/sony-starvis-imx462-ultra-low-light-camera.asp)
- [Arducam IMX462 for Raspberry Pi](https://www.amazon.com/Arducam-STARVIS-Wide-Angle-Sensitivity-Raspberry/dp/B0C3V6KHZT)

---

## Comparison Table: Top Options

| Camera | Sensor | Resolution | IR Capability | Wide Angle | USB Type | V4L2 | Price | Status |
|--------|--------|-----------|---------------|------------|----------|------|-------|--------|
| **e-con See3CAM_CU83** | AR0830 | 8MP (4K) | RGB-IR separation | 81° H | USB 3.2 | Yes | **$249** | Available |
| **ELP IMX179** | IMX179 | 8MP | IR filter (custom NoIR?) | 115°-180° | USB 2.0 | Yes | **$58-70** | Custom order |
| **SVPRO IMX179** | IMX179 | 8MP | IR filter (custom NoIR?) | 170°-180° | USB 2.0 | Yes | **$58-122** | Custom order |
| **Arducam IMX179** | IMX179 | 8MP | IR filter (custom NoIR?) | 115° | USB 2.0 | Yes | **$60-80** | Custom order |
| **Arducam IMX219 USB** | IMX219 | 8MP | IR filter (no USB NoIR) | 60° only | USB 2.0 | Yes | **$40-60** | Not wide angle |
| **Arducam IMX219 CSI NoIR** | IMX219 | 8MP | **NoIR available** | 175° option | **CSI only** | Yes | **$15-30** | Not USB |
| **ELP IMX317** | IMX317 | 8MP (4K) | IR filter (NoIR unknown) | Varies | USB 2.0 | Yes | **$60-90** | Research needed |
| **Arducam Day/Night USB** | OV2710 | **2MP** | **Motorized IR-cut** | 105° | USB 2.0 | Yes | **$60-80** | Turnkey solution |
| **e-con See3CAM_CU27** | IMX462 | **2MP** | **IR sensitive** | Varies | USB 3.1 | Yes | **Unknown** | Low-light specialist |

---

## Key Findings by Sensor

### IMX317 (8MP, 4K)
- **Availability:** Multiple USB cameras available
- **IR Sensitivity:** Standard models have IR filter; NoIR version not confirmed
- **Advantage:** 30fps @ 4K (vs. 15fps for IMX179)
- **BSI Technology:** Better low-light than IMX179
- **Recommendation:** Contact e-con Systems or ELP for NoIR option

### IMX219 (8MP)
- **Availability:** USB cameras exist (Arducam B0292)
- **IR Sensitivity:** NoIR versions available for **Raspberry Pi CSI only**, not USB
- **Advantage:** Raspberry Pi ecosystem, autofocus options
- **Wide Angle:** Standard USB version is 60° (not wide); CSI NoIR has 175° option
- **Recommendation:** Use CSI NoIR if USB requirement can be relaxed

### IMX179 (8MP)
- **Availability:** Many USB cameras (ELP, SVPRO, Arducam)
- **IR Sensitivity:** Standard models have IR filter @ 650nm
- **Wide Angle:** 115°-180° options widely available
- **Customization:** Manufacturers (ELP, SVPRO) offer OEM/ODM services
- **Recommendation:** **Best bet for custom 8MP NoIR USB camera** - contact ELP

### AR0830 (8MP, RGB-IR)
- **Availability:** e-con Systems See3CAM_CU83 only
- **IR Sensitivity:** Proprietary RGB-IR separation, no filter needed
- **Advantage:** Day/night without mechanical parts
- **Price:** $249 (exceeds budget)
- **Recommendation:** Premium option if budget allows

### IMX291/IMX462 (2MP, STARVIS)
- **Availability:** Multiple USB cameras
- **IR Sensitivity:** Excellent (designed for low light)
- **Advantage:** Best night vision performance
- **Limitation:** Only 2MP (not 8MP)
- **Recommendation:** If resolution requirement can be lowered

---

## Recommendations

### Recommendation 1: Custom 8MP NoIR USB Camera (Best Technical Match)

**Approach:** Contact ELP or SVPRO for custom 8MP IMX179 camera without IR-cut filter.

**Specifications:**
- Sensor: Sony IMX179 (1/3.2", 8MP)
- Resolution: 3264 × 2448 @ 15fps
- IR-Cut Filter: **NONE (NoIR version)**
- Lens: Wide angle 115° or 180° fisheye
- Interface: USB 2.0
- UVC Compliant: Yes
- Estimated Price: $70-100 (depends on MOQ)

**Contact Information:**
- **ELP:** sales@elpcctv.com (Ms. Lizzy Liu, Sales Manager)
- **SVPRO:** Check svpro.cc for contact form

**Questions to Ask:**
1. Can you provide 8MP IMX179 USB camera WITHOUT IR-cut filter (NoIR version)?
2. What lens options available (need 120°+ field of view)?
3. Pricing for quantities: 2 units, 5 units, 10 units?
4. Minimum order quantity (MOQ)?
5. Lead time for custom order?
6. Compatibility confirmed for Linux V4L2/UVC?
7. Operating temperature range specification?

**Pros:**
- Meets all technical requirements
- Likely within budget for small quantities
- Proven USB camera platform
- Wide angle options available
- OEM/ODM services established

**Cons:**
- Requires custom order (lead time)
- May have MOQ requirement
- No off-the-shelf availability for testing

---

### Recommendation 2: RGB-IR Camera (Premium Option)

**Product:** e-con Systems See3CAM_CU83 (AR0830 sensor)

**Use Case:** Jakarta reference site with AC power (budget less constrained)

**Specifications:**
- 8MP (4K) RGB-IR camera
- 15fps @ 4K, 30fps @ 1080p
- USB 3.2 Gen 1
- M12 lens (81° H FOV)
- $249 per camera

**Pros:**
- Turnkey day/night solution
- No mechanical IR-cut filter
- High quality sensor
- Professional support from e-con Systems

**Cons:**
- Exceeds $100 budget by 2.5×
- May require custom software for RGB-IR separation

**Recommendation:** Consider for Jakarta site only if budget allows.

---

### Recommendation 3: Proven Day/Night Camera (Lower Resolution)

**Product:** Arducam 2MP Day & Night Vision USB Camera (B0506)

**Use Case:** If ORC software can work with 1080p instead of 4K/8MP

**Specifications:**
- 2MP (1920 × 1080) @ 30fps
- Motorized IR-cut filter (automatic switching)
- Built-in 850nm IR LEDs
- 105° wide angle lens
- USB 2.0, UVC compliant
- $60-80

**Pros:**
- **Turnkey solution** - works out of box
- Automatic day/night switching
- Built-in IR illumination (no external IR light needed)
- Wide angle
- Within budget

**Cons:**
- Only 2MP (not 8MP)
- Requires ORC software to accept lower resolution

**Recommendation:** If ORC can be modified to accept 1080p, this is the **lowest-risk option**.

---

### Recommendation 4: Raspberry Pi CSI NoIR Camera (Interface Change)

**Product:** Arducam 8MP IMX219 NoIR Camera for Raspberry Pi

**Use Case:** If USB requirement can be relaxed (use CSI ribbon cable instead)

**Specifications:**
- 8MP IMX219 sensor (NoIR version)
- 3280 × 2464 resolution
- Wide angle option: 175° ultra-wide
- CSI interface (direct to Pi)
- $15-30
- V4L2 compatible (libcamera)

**Pros:**
- **Proven NoIR solution** (official Pi NoIR camera)
- Ultra-wide angle available
- Cheapest option
- No IR-cut filter issue

**Cons:**
- **Not USB** - uses CSI ribbon cable
- Limited cable length (15-30cm typical)
- Camera must be near Pi (not suitable for long cable runs)

**Recommendation:** Only if camera can be mounted very close to Pi enclosure (Sukabumi site might work).

---

## Technical Considerations

### V4L2 / UVC Compatibility

All USB cameras researched are **UVC (USB Video Class) compliant**, which means:
- Plug and play on Linux
- Works with V4L2 (Video4Linux2) drivers
- Compatible with Raspberry Pi OS
- No custom drivers needed
- Works with ffmpeg, v4l2-ctl, OpenCV, etc.

**Verification:** Confirm with `v4l2-ctl --list-devices` after connecting camera.

---

### IR Illuminator Compatibility

**850nm vs 940nm IR LEDs:**
- **850nm:** Brighter, better range, slight red glow visible
- **940nm:** Completely invisible, lower range

**Camera Requirements for 850nm IR:**
- Sensor must detect 850nm wavelength
- No IR-cut filter blocking IR
- CMOS sensors (IMX179, IMX219, IMX317) are IR-sensitive if filter removed

**Spectrum Response:**
- IMX179: Sensitive to ~400-1000nm (includes 850nm)
- IMX219: Sensitive to ~400-1000nm (includes 850nm)
- IMX317: Sensitive to ~400-1000nm (includes 850nm)
- AR0830: Designed for RGB-IR, excellent 850nm response

**Conclusion:** All sensors are inherently IR-sensitive; the IR-cut filter is the only barrier.

---

### Wide Angle Requirements

**ORC River Monitoring Target:** 120°+ field of view (horizontal)

**Available Wide Angle Options:**

| Lens Type | HFOV | Distortion | Best For |
|-----------|------|------------|----------|
| **3.6mm standard** | ~60-75° | Low | General purpose (too narrow) |
| **2.8mm** | ~90° | Low | Good compromise |
| **2.1mm** | ~105-115° | Low | Wide angle, minimal distortion |
| **Fisheye 170°** | ~155-170° | High | Ultra-wide, requires correction |
| **Fisheye 180°** | ~180° | Very high | Maximum coverage, heavy correction |

**Recommendation:**
- **Ideal:** 115° (2.1mm) - wide coverage with manageable distortion
- **Acceptable:** 105° (2.8mm) if 115° not available
- **Avoid:** Standard 60° lens (too narrow for river monitoring)

**Note:** Fisheye lenses (170°-180°) provide maximum coverage but require software distortion correction, which ORC software may not support.

---

### Power Consumption

USB cameras draw power from USB port:

| Camera Type | Typical Power | Notes |
|-------------|--------------|-------|
| **8MP USB 2.0** | 0.5-1W (100-200mA @ 5V) | Standard UVC camera |
| **8MP USB 3.0** | 1-2.5W (200-500mA @ 5V) | Higher due to USB 3.0 |
| **With IR LEDs** | +2-5W for LEDs | If built-in IR illumination |

**Raspberry Pi 5 USB Power:**
- Each USB 3.0 port: 5V @ 600mA max (3W)
- Total USB power budget: Depends on power supply

**Recommendation:** 8MP USB 2.0 camera (0.5-1W) fits within Pi USB power budget. External IR illuminator should use separate 12V power, not USB.

---

### Temperature Range

**Indonesia Tropical Environment:**
- Ambient: 25-40°C (typical)
- Direct sun on camera housing: 50-70°C (possible)
- Humidity: 80-95% RH

**Camera Operating Ranges:**

| Camera | Operating Temp | Storage Temp | Humidity | Notes |
|--------|---------------|--------------|----------|-------|
| **ELP/SVPRO IMX179** | -20°C to +70°C | N/A | Not specified | Good for tropics |
| **Arducam IMX219** | Typical Pi range | N/A | Not specified | May need testing |
| **e-con See3CAM_CU83** | -20°C to +65°C | N/A | Not specified | Adequate |

**Recommendation:** All cameras meet temperature requirements. Thermal management should focus on housing (Gore vent + PTC heater per Jakarta design).

---

## Linux / Raspberry Pi 5 Compatibility

### UVC Driver Support

**All researched cameras are UVC compliant**, meaning they work with the standard Linux UVC driver (uvcvideo kernel module).

**Verification Steps:**
1. Connect camera to Raspberry Pi 5
2. Run: `lsusb` (should show USB camera device)
3. Run: `v4l2-ctl --list-devices` (should list /dev/video0 or similar)
4. Run: `v4l2-ctl -d /dev/video0 --list-formats-ext` (shows supported formats)
5. Test capture: `ffmpeg -f v4l2 -i /dev/video0 -frames 1 test.jpg`

### Resolution and Format Support

**Typical UVC Camera Formats:**
- **MJPEG:** Hardware-compressed, high frame rates, larger bandwidth
- **YUYV (YUV422):** Uncompressed, lower frame rates, high bandwidth
- **H.264:** Some cameras (e-con IMX317) support hardware H.264 encoding

**ORC Software Requirements:**
- Check if ORC uses ffmpeg or v4l2 API
- Verify supported resolutions (4K, 1080p, etc.)
- Confirm MJPEG or raw YUV acceptable

---

## Cost Analysis

### Budget Breakdown (Per Camera)

| Option | Camera | IR Illuminator | Cables | Housing | Total | Status |
|--------|--------|---------------|--------|---------|-------|--------|
| **Custom IMX179 NoIR** | $70-100 | $30-40 | $15 | $40-100 | **$155-255** | Requires custom order |
| **e-con RGB-IR** | $249 | Not needed | $15 | $40-100 | **$304-364** | Off-shelf, premium |
| **Arducam 2MP Day/Night** | $70 | Built-in | $15 | $40-100 | **$125-185** | Turnkey, lower res |
| **Pi CSI NoIR** | $25 | $30-40 | N/A | $40-100 | **$95-165** | Not USB |

**Note:** Budget target is **under $100 per camera**. Only the CSI NoIR option meets this when camera is standalone.

**Housing Cost:**
- Gore vent housing: $40 (Entaniya WC-01) to $100 (VA Imaging MVEC167)
- See `sealed_camera_module_research.md` for housing details

**IR Illuminator Cost:**
- 850nm IR flood light: $20-40 (12V, 20-30W)
- With built-in dusk sensor: +$10-20

**Total System Cost (2 cameras for Sukabumi):**
- Custom IMX179 NoIR option: $310-510
- Pi CSI NoIR option: $190-330

---

## Availability and Lead Times

### Off-Shelf Availability (Ships Immediately)

| Product | Vendor | Lead Time | Stock Status |
|---------|--------|-----------|--------------|
| **Arducam IMX219 USB (w/ IR filter)** | Amazon, Arducam | 1-3 days (US), 1-2 weeks (intl) | In stock |
| **ELP IMX179 (w/ IR filter)** | Amazon, SVPRO.cc | 1-5 days (US), 1-2 weeks (intl) | In stock |
| **Arducam 2MP Day/Night USB** | Amazon, Arducam | 1-3 days (US), 1-2 weeks (intl) | In stock |
| **Arducam Pi CSI NoIR** | Amazon, Arducam | 1-3 days (US), 1-2 weeks (intl) | In stock |
| **e-con See3CAM_CU83** | e-con Systems direct | Contact for quote | Sample orders available |

### Custom Order Lead Times

| Product | Vendor | MOQ | Lead Time | Notes |
|---------|--------|-----|-----------|-------|
| **IMX179 NoIR (custom)** | ELP, SVPRO | TBD | 2-6 weeks | Contact sales for quote |
| **IMX219 USB NoIR (custom)** | Arducam | TBD | 2-4 weeks | May require engineering |
| **IMX317 NoIR (custom)** | ELP, e-con | TBD | 2-6 weeks | Contact for feasibility |

**Recommendation:** If custom order needed, contact manufacturers NOW (January 2026) for March/April deployment.

---

## Gaps and Limitations

### Critical Gaps

1. **No confirmed 8MP USB NoIR camera under $100:** Off-shelf options don't exist. Custom order required.

2. **IR filter removal uncertainty:** Manufacturers may not offer NoIR versions, or may have high MOQ.

3. **Wide angle + NoIR combination:** Most wide-angle USB cameras have IR filters. Custom order needed.

4. **ORC software 8MP requirement:** If software requires 8MP, 2MP day/night camera not viable.

### Alternative Approaches

**If 8MP NoIR USB camera not available:**

1. **Use CSI NoIR camera:** Relaxes USB requirement, proven solution, cheapest option
   - Limitation: Short cable length (camera near Pi)

2. **Use 2MP USB day/night camera:** Turnkey solution, automatic IR-cut switching
   - Limitation: Requires ORC software modification for 1080p

3. **Use 8MP camera with IR filter + visible light only:** No night vision
   - Limitation: No night monitoring capability

4. **Use RGB-IR camera (See3CAM_CU83):** Premium solution, exceeds budget
   - Limitation: 2.5× over budget

---

## Next Steps

### Immediate Actions (January 2026)

1. **Contact ELP for custom quote:**
   - Email: sales@elpcctv.com
   - Request: 8MP IMX179 USB camera, NoIR version, 115° wide angle lens
   - Quantities: 2 units (test), 5 units (Sukabumi + Jakarta + spares)
   - Confirm: Lead time, MOQ, V4L2 compatibility, operating temp

2. **Contact SVPRO for custom quote:**
   - Similar request as ELP (compare options)

3. **Contact Arducam:**
   - Request: 8MP IMX219 USB camera in NoIR version (if available)
   - Alternative: Confirm Pi CSI NoIR camera compatibility with Raspberry Pi 5

4. **Contact e-con Systems:**
   - Request: Quote for See3CAM_CU83 (RGB-IR camera)
   - Quantity discount for 2-5 units?
   - Confirm RGB-IR separation works with V4L2/ffmpeg

5. **Test ORC software with 1080p:**
   - If Arducam 2MP day/night camera is fallback option
   - Verify ORC can process 1080p video (not just 4K/8MP)

### Decision Points

**By January 15, 2026:**
- Confirm whether custom 8MP NoIR USB camera is feasible (pricing, MOQ, lead time)
- Decide: Custom order vs. alternative approach

**By January 20, 2026:**
- Finalize camera selection for Sukabumi BOM
- Order cameras (allow 2-6 weeks for custom, or 1-2 weeks for off-shelf)

**By February 1, 2026:**
- Test cameras with Raspberry Pi 5 + ORC software
- Verify night vision with 850nm IR illuminator
- Confirm V4L2 compatibility

---

## Research Sources

### Product Documentation
- [e-con Systems See3CAM_CU83 Product Page](https://www.e-consystems.com/usb-cameras/8mp-4k-rgb-ir-usb3-camera.asp)
- [ELP 8MP IMX179 USB Camera Category](https://www.svpro.cc/product-category/elp-products/8mp-sony-imx179-usb-cameras/)
- [Arducam 8MP IMX219 USB Camera](https://www.arducam.com/product/arducam-usb-autofocus-imx219-b0292/)
- [Arducam 8MP IMX219 NoIR for Raspberry Pi](https://www.arducam.com/8mp-imx219-noir-for-raspberry-pi-b0395.html)
- [Arducam Day/Night Vision USB Camera](https://www.arducam.com/arducam-1080p-day-night-vision-usb-camera-2mp-infrared-webcam-with-automatic-ir-cut-switching-and-ir-leds.html)
- [e-con Systems See3CAM_CU27 IMX462](https://www.e-consystems.com/usb-cameras/sony-starvis-imx462-ultra-low-light-camera.asp)

### Technical Resources
- [Sony IMX179 Sensor Datasheet](https://www.sony-semicon.com/en/products/is/industry/product/imx179.html)
- [Sony IMX219 Sensor Datasheet](https://www.sony-semicon.com/en/products/is/industry/product/imx219.html)
- [Sony IMX317 Sensor Datasheet](https://www.sony-semicon.com/en/products/is/industry/product/imx317.html)
- [Arducam Wiki - 8MP IMX219](https://docs.arducam.com/Raspberry-Pi-Camera/Native-camera/8MP-IMX219/)
- [Raspberry Pi Camera Documentation](https://www.raspberrypi.com/documentation/accessories/camera.html)

### Vendor Contact Information
- **ELP (Ailipu Technology):** sales@elpcctv.com, www.elpcctv.com
- **SVPRO:** www.svpro.cc
- **Arducam:** support@arducam.com, www.arducam.com
- **e-con Systems:** camerasales@e-consystems.com, www.e-consystems.com

### Related Research
- [IR Night Vision Technology Overview](https://reolink.com/blog/night-vision-security-camera/)
- [Best Night Vision Security Cameras 2026](https://www.security.org/security-cameras/best/infrared/)
- [IR Illuminator Technology](https://lensviewing.com/best-digital-camera-module-for-night-vision/)

---

## Conclusion

**Finding an 8MP USB camera with IR sensitivity (NoIR) under $100 is challenging** because:
1. Most USB cameras include IR-cut filters for accurate color reproduction
2. NoIR versions are rare in the USB market (common for Raspberry Pi CSI cameras)
3. Wide-angle + NoIR combination further limits options

**Best Path Forward:**

1. **Contact ELP/SVPRO immediately** for custom 8MP IMX179 NoIR USB camera quote
   - This is the most likely solution to meet all requirements
   - Pricing expected $70-100, may require MOQ

2. **Consider fallback options:**
   - **Option A:** e-con See3CAM_CU83 RGB-IR camera for Jakarta site (premium, $249)
   - **Option B:** Arducam 2MP Day/Night USB camera if ORC accepts 1080p
   - **Option C:** Raspberry Pi CSI NoIR camera if USB requirement can be relaxed

3. **Test ORC software** with 1080p to determine if 8MP is hard requirement

**Timeline:** Order custom cameras by mid-January 2026 to allow 2-6 weeks lead time for March/April deployment.

---

**Document Version:** 1.0
**Last Updated:** January 8, 2026
**Next Review:** After manufacturer responses (January 15, 2026)
