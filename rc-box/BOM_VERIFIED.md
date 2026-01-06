# RC-Box Bill of Materials (Verified)

**Target:** Complete dual-camera unit with PoE IP cameras
**Date:** 2026-01-06
**Revision:** 4 - PoE camera system with relay-controlled power management

---

## CRITICAL COMPATIBILITY NOTES

1. **Camera System:** Using factory-sealed IP67 PoE cameras (ANNKE C1200) instead of USB cameras. Eliminates DIY housing/anti-fog system. Requires RTSP capture via ffmpeg (not V4L2).

2. **Camera Power Management:** Cameras power-cycle with Pi using relay-controlled PoE. 15-minute duty cycle = ~35,000 cycles/year. Budget for camera replacement every 2-3 years.

3. **Global Modem:** Quectel EG25-G supports 15 LTE bands covering Americas, Europe, Asia-Pacific, and Africa. Regional variants (EC25-AF, EC25-E) do NOT provide global coverage.

4. **Power Management:** PiSugar 3 Plus is **NOT compatible** with Pi 5. Use Waveshare UPS HAT (B) or Witty Pi 4 instead.

5. **PoE Power:** Planet IPOE-260-12V has 12V boost technology - accepts 10.5-14.6V LiFePO4 battery range directly.

---

## DigiKey/Mouser Order

| Qty | Part Number | Manufacturer | Description | Unit Price | Ext Price | Source |
|-----|-------------|--------------|-------------|------------|-----------|--------|
| 1 | SC1111 | Raspberry Pi | Raspberry Pi 5 4GB | $60.00 | $60.00 | DigiKey |
| 1 | EG25GGB-MINIPCIE | Quectel | LTE Cat 4 Modem **GLOBAL** (15 LTE bands) | $78.93 | $78.93 | DigiKey |
| 1 | PU201 | Techship | Mini PCIe to USB3 Adapter (dual nano SIM) | $50.00 | $50.00 | DigiKey |
| 6 | CG-PG9-2-BK | Essentra | PG9 Cable Gland IP68 4-8mm | $1.17 | $7.02 | DigiKey |
| 3 | VENT-PS1NGY-N8002 | Amphenol LTW | M12 Breather Vent IP69K | $8.50 | $25.50 | DigiKey |
| 4 | M2012SS1W01 | NKK Switches | SPST Toggle Switch IP67 | $12.50 | $50.00 | DigiKey |
| 1 | 26295 | Universal Solder | 1.3" OLED 128x64 I2C SSD1306 | $15.00 | $15.00 | DigiKey |
| 3 | 559-QS103XXR12 | Apem | 10mm LED 12V Red Panel Mount | $3.50 | $10.50 | Mouser |

**DigiKey/Mouser Subtotal: ~$297**

---

## PoE Camera System (Factory Sealed IP67)

**NOTE:** Factory-sealed cameras eliminate DIY housing, anti-fog systems, and desiccant maintenance. RTSP capture via ffmpeg replaces V4L2/USB interface.

### Cameras

| Qty | Part Number | Manufacturer | Description | Unit Price | Ext Price | Source |
|-----|-------------|--------------|-------------|------------|-----------|--------|
| 2 | C1200 | ANNKE | 12MP PoE Camera, IP67, IR, -30 to +60C | $110.00 | $220.00 | Annke/Amazon |

**ANNKE C1200 Specifications:**
- Resolution: 4096x3072 (12MP)
- Sensor: 1/2.7" BSI CMOS
- Lens: 2.8mm F1.6, 113 horizontal FOV
- Night Vision: Dual-light (IR + 700lm spotlight), 100ft range
- IP Rating: IP67
- Temperature: -30C to +60C (exceeds requirements)
- WDR: 120dB (handles river reflections)
- Compression: H.265+/H.264
- ONVIF: v19.12 (S/T/G profiles)
- PoE: 802.3af (6.5W typical)
- RTSP URL: `rtsp://admin:password@IP:554/Streaming/channels/101`

### PoE Power System (12V Battery Input)

| Qty | Part Number | Manufacturer | Description | Unit Price | Ext Price | Source |
|-----|-------------|--------------|-------------|------------|-----------|--------|
| 1 | IPOE-260-12V | Planet Technology | 2-Port Industrial PoE+ Injector w/ 12V Boost | $164.00 | $164.00 | Planet/NetworkCameraStore |
| 1 | Relay HAT | Waveshare | RPi Relay Board (screw terminals, LED indicators) | $32.00 | $32.00 | Waveshare/Amazon |

**Planet IPOE-260-12V Specifications:**
- Input: 12-54V DC (handles LiFePO4 10.5-14.6V range)
- Output: 54V PoE+ (802.3at), up to 36W per port
- Ports: 2x Data In, 2x PoE Out (Gigabit)
- Temperature: -40C to +75C (industrial grade)
- Mounting: DIN rail or wall
- Connectors: Screw terminal for power, RJ45 for data/PoE

**Waveshare Relay HAT:**
- Plugs directly onto Pi 5 GPIO header (no wiring for control)
- Screw terminals for power connections
- LED indicators for relay state
- Audible click confirms switching
- Field-serviceable (no soldering)

### Camera Cabling & Mounting

| Qty | Part Number | Manufacturer | Description | Unit Price | Ext Price | Source |
|-----|-------------|--------------|-------------|------------|-----------|--------|
| 2 | - | Various | Cat6 Outdoor Shielded Cable 30m | $25.00 | $50.00 | Amazon |
| 2 | - | Various | IP68 RJ45 Feedthrough Connector | $8.00 | $16.00 | Amazon |
| 2 | B0D2VPL4L6 | WiTi | Stainless Steel Pole Mount Bracket | $25.00 | $50.00 | Amazon |

**PoE Camera System Subtotal: ~$532**

---

## Specialty Electronics

| Qty | Part Number | Manufacturer | Description | Unit Price | Ext Price | Source |
|-----|-------------|--------------|-------------|------------|-----------|--------|
| 1 | Witty Pi 4 | UUGear | RTC + Power Management for Pi 5 (5-26V input) | $30.00 | $30.00 | UUGear/Amazon |
| 1 | - | Various | M.2 SATA 512GB SSD | $40.00 | $40.00 | Amazon |
| 1 | - | StarTech/Sabrent | M.2 SATA to USB 3.0 Enclosure | $15.00 | $15.00 | Amazon |
| 2 | - | Various | LTE Antenna SMA 700-2700MHz (for EG25-G) | $8.00 | $16.00 | Amazon |

**Specialty Electronics Subtotal: ~$101**

---

## Power System (Solar Configuration)

| Qty | Part Number | Manufacturer | Description | Unit Price | Ext Price | Source |
|-----|-------------|--------------|-------------|------------|-----------|--------|
| 1 | - | Ampere Time/Redodo | LiFePO4 12V 50Ah Battery | $160.00 | $160.00 | Amazon |
| 1 | - | Renogy/Newpowa | 100W 12V Mono Solar Panel | $90.00 | $90.00 | Amazon |
| 1 | - | EPEVER/PowMr | MPPT 20A Solar Charge Controller | $35.00 | $35.00 | Amazon |
| 1 | - | Various | 10A Inline Fuse Holder + Fuses (5-pack) | $10.00 | $10.00 | Amazon |

**Power System Subtotal: ~$295**

**Note:** Upgraded to 50Ah battery and 100W panel to support PoE camera power cycling (~191 Wh/day).

---

## Enclosure & Mounting

| Qty | Part Number | Manufacturer | Description | Unit Price | Ext Price | Source |
|-----|-------------|--------------|-------------|------------|-----------|--------|
| 1 | WQ-57 | Polycase | IP67 Enclosure 11.8"x9.1"x5.5" | $45.00 | $45.00 | Polycase |
| 4 | - | Generic | SS Hose Clamp 3-6" | $3.00 | $12.00 | Amazon |
| 1 | - | Various | Wire, connectors, standoffs, terminal blocks | $25.00 | $25.00 | Various |
| 1 | - | Various | DIN Rail 35mm (for PoE injector mounting) | $8.00 | $8.00 | Amazon |

**Enclosure/Mounting Subtotal: ~$90**

---

## TOTAL COST SUMMARY

| Category | Cost |
|----------|------|
| DigiKey/Mouser | $297 |
| PoE Camera System | $532 |
| Specialty Electronics | $101 |
| Power System (Solar) | $295 |
| Enclosure/Mounting | $90 |
| **TOTAL (Solar)** | **$1,315** |
| **TOTAL (Grid)** | **~$1,030** |

**Note:** Grid power configuration saves ~$285 (no solar panel/controller, smaller battery).

**Cost Comparison vs Previous USB Camera Approach:**
- Previous (Arducam USB + DIY housing): ~$906
- Current (PoE cameras + power management): ~$1,315
- Difference: +$409 for factory-sealed cameras, integrated IR, no DIY assembly

---

## Cost Reduction Options

| Change | Savings | Notes |
|--------|---------|-------|
| Use Pi 5 2GB instead of 4GB | -$15 | Minimal impact for this application |
| Smaller battery (12V 30Ah) | -$60 | ~1.5 day autonomy |
| 50W panel instead of 100W | -$35 | Marginal in cloudy weather |
| 256GB SSD instead of 512GB | -$15 | Still ~2 weeks storage |
| Single camera initially | -$110 | Add second camera later |
| Reolink RLC-1212A instead of ANNKE | -$20 | Narrower temp range (-10 to +55C) |

**Realistic reduced total: ~$1,100-1,200**

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           RC-BOX ENCLOSURE                               │
│                                                                          │
│  [12V LiFePO4 Battery]                                                  │
│         │                                                                │
│         ├────[Fuse]────┬──────────────────────────────────┐             │
│         │              │                                   │             │
│         ▼              ▼                                   ▼             │
│  [Witty Pi 4]    [Relay HAT]                     [Planet IPOE-260-12V]  │
│         │              │                          (DIN rail mounted)     │
│         ▼              │                                   │             │
│  [Raspberry Pi 5]─GPIO─┘                                   │             │
│         │                                                  │             │
│         │◄──────────── Ethernet ───────────────────────────┤             │
│         │                                                  │             │
│    [EG25-G Modem]                              PoE Out 1───┼──► Camera 1 │
│         │                                      PoE Out 2───┼──► Camera 2 │
│    [LTE Antenna]                                           │             │
│                                                            │             │
└────────────────────────────────────────────────────────────┼─────────────┘
                                                             │
                                        (via IP68 cable glands + outdoor Cat6)
```

---

## Duty Cycle Timing (15-Minute Interval)

| Phase | Duration | Cumulative |
|-------|----------|------------|
| Witty Pi 4 wakes Pi 5 | 0s | 0:00 |
| Pi boot complete | 15-20s | 0:20 |
| GPIO activates relay | <1s | 0:21 |
| PoE injector stabilizes | 2-3s | 0:24 |
| Camera boot + PoE negotiation | 60-90s | **1:54** |
| RTSP stream ready | - | **~2:00** |
| ffmpeg capture (2 cameras) | 120-180s | 4:00-5:00 |
| GPIO deactivates relay | <1s | 5:01 |
| Pi shutdown | 5s | **~5:05** |
| Sleep until next cycle | 9:55 | 15:00 |

**Active time:** ~5 minutes per cycle
**Sleep time:** ~10 minutes per cycle

---

## Power Budget (Daily)

| Component | Active Power | Daily Runtime | Daily Energy |
|-----------|-------------|---------------|--------------|
| Pi 5 + Witty Pi | 5W | 8 hr | 40 Wh |
| Relay HAT | 1W | 8 hr | 8 Wh |
| IPOE-260-12V (idle + boost) | 3W | 5.3 hr | 16 Wh |
| Cameras (2x 12W) | 24W | 5.3 hr | 127 Wh |
| **Daily Total** | | | **~191 Wh** |

**Solar Production (100W panel, 4 sun-hours):** ~400 Wh/day
**Margin:** ~50% (adequate for cloudy days)
**Battery Autonomy:** 50Ah x 12V x 0.8 DoD = 480 Wh = ~2.5 days

---

## Notes

### Verified DigiKey Part Numbers
- SC1111 - Raspberry Pi 5 4GB
- EG25GGB-MINIPCIE - Quectel LTE modem (GLOBAL, 15 LTE bands)
- PU201 - Techship Mini PCIe to USB3 Adapter (dual nano SIM, industrial)
- CG-PG9-2-BK - Essentra cable gland
- VENT-PS1NGY-N8002 - Amphenol breather vent
- M2012SS1W01 - NKK IP67 toggle switch

### Cellular Modem Details (EG25-G + PU201)
**EG25-G Global LTE Bands:**
- LTE-FDD: B1/2/3/4/5/7/8/12/13/18/19/20/25/26/28
- LTE-TDD: B38/39/40/41
- 3G WCDMA: B1/2/4/5/6/8/19
- 2G GSM: B2/3/5/8

**Techship PU201 Adapter Features:**
- USB 3.0 Type-A connection
- Dual 4FF nano SIM slots (push-pull)
- Industrial DC-DC power circuit with ceramic capacitors
- Thermal pads for heat dissipation
- Tested with Quectel EC2x/EG2x, Sierra MC74xx, Telit LE910
- Made in Sweden, RoHS/REACH compliant

### PoE Camera Details (ANNKE C1200)
**RTSP Configuration:**
- Main stream: `rtsp://admin:password@IP:554/Streaming/channels/101`
- Sub stream: `rtsp://admin:password@IP:554/Streaming/channels/102`
- Enable RTSP in camera web interface (disabled by default)
- Use static IP addresses (faster boot, no DHCP delay)

**Optimization Settings:**
- Disable cloud services
- Disable audio (if not needed)
- Disable motion detection
- Use H.264 (faster encoder startup than H.265)
- Disable automatic firmware updates

### Items NOT on DigiKey/Mouser
- ANNKE C1200 cameras - Annke.com or Amazon
- Planet IPOE-260-12V - NetworkCameraStore.com or Planet dealers
- Waveshare Relay HAT - Waveshare.com or Amazon
- Witty Pi 4 - UUGear.com or Amazon
- WiTi pole mounts - Amazon (ASIN: B0D2VPL4L6)
- LiFePO4 batteries - Amazon (Ampere Time, Redodo)
- Solar panels/controllers - Amazon/Renogy
- Polycase enclosures - Polycase.com direct

---

## Assembly Notes

### Pre-Deployment Prep (Do Before Shipping)

1. **Main enclosure assembly:**
   - Mount DIN rail for PoE injector
   - Mount Pi 5 + Witty Pi 4 on standoffs
   - Plug Waveshare Relay HAT onto Pi GPIO header
   - Mount Planet IPOE-260-12V on DIN rail
   - Install switches, LEDs, display on panel
   - Install IP68 RJ45 feedthrough connectors in enclosure wall
   - Install SMA bulkhead connectors for LTE antennas

2. **Internal wiring (all screw terminals, no soldering):**
   ```
   Battery 12V+ ──► Fuse 10A ──► Terminal Block

   From Terminal Block:
   ├── 12V+ ──► Witty Pi 4 power input
   ├── 12V+ ──► Relay HAT VCC
   ├── 12V+ ──► Relay COM (input to be switched)
   └── GND  ──► Common ground bus

   Relay NO ──► IPOE-260-12V 12V+ input
   Ground   ──► IPOE-260-12V GND input

   IPOE-260-12V Data IN Port 1 ◄── Pi 5 Ethernet
   ```

3. **Camera pre-configuration:**
   - Power cameras temporarily via standard PoE switch
   - Access web interface, set static IP addresses (192.168.1.100, 192.168.1.101)
   - Enable RTSP, set username/password
   - Disable cloud, audio, motion detection, auto-update
   - Set H.264 encoding
   - Note: Camera boot time ~60-90 seconds

4. **Software installation:**
   - Install ffmpeg on Pi 5
   - Configure Witty Pi 4 schedule (wake every 15 minutes)
   - Install camera control script (GPIO relay + ffmpeg capture)
   - Test complete duty cycle before shipping

### On-Site Assembly

5. **Camera mounting:**
   - Attach WiTi pole mount brackets to pole using SS hose clamps
   - Mount cameras to brackets, aim toward river
   - Route outdoor Cat6 cables from cameras to enclosure
   - Connect cables through IP68 feedthrough connectors
   - Connect to IPOE-260-12V PoE output ports

6. **Final connections:**
   - Connect solar panel to charge controller
   - Connect battery to charge controller
   - Connect 12V from battery to main terminal block
   - Connect LTE antennas to EG25-G module
   - Insert SIM card into PU201 adapter

7. **Testing:**
   - Power on system
   - Verify relay clicks when Pi boots
   - Verify cameras power up and become pingable (~90s)
   - Test RTSP capture: `ffmpeg -i rtsp://admin:password@192.168.1.100:554/... -vframes 1 test.jpg`
   - Monitor one complete duty cycle
   - Verify cameras power down when Pi shuts down

---

## Field Service Quick Reference

```
┌─────────────────────────────────────────────────────────────┐
│              CAMERA POWER TROUBLESHOOTING                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. CHECK RELAY HAT                                          │
│     ├─ LED ON when cameras should be powered? Y/N           │
│     ├─ Hear relay "click" when Pi boots? Y/N                │
│     └─ If NO: Check Pi GPIO connection or replace HAT       │
│                                                              │
│  2. CHECK POE INJECTOR (Planet IPOE-260-12V)                │
│     ├─ Power LED lit? Y/N                                   │
│     ├─ Check 12V at input terminals with multimeter         │
│     └─ If no 12V: Check relay output, fuse, battery         │
│                                                              │
│  3. CHECK CAMERAS                                            │
│     ├─ PoE LED on injector port lit? Y/N                    │
│     ├─ Camera IR LEDs glow at night? Y/N                    │
│     ├─ Can ping camera IP? Y/N                              │
│     └─ If NO: Check Ethernet cable or replace camera        │
│                                                              │
│  REPLACEMENT PROCEDURE:                                      │
│     1. Power OFF entire system (main switch)                │
│     2. Photo document all wire connections                  │
│     3. Loosen screw terminals (turn counter-clockwise)      │
│     4. Remove failed component                               │
│     5. Install replacement                                   │
│     6. Reconnect wires matching photo                       │
│     7. Power ON and test                                     │
│                                                              │
│  CAMERA BOOT TIME: Wait 90 seconds after power-on           │
│  before testing RTSP or ping                                 │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Spare Parts Kit (Ship with Each Unit)

| Qty | Item | Notes |
|-----|------|-------|
| 1 | ANNKE C1200 camera | Complete spare camera |
| 1 | Waveshare Relay HAT | GPIO control module |
| 3 | 10A fuses | For inline fuse holder |
| 2 | Cat6 patch cable 1m | For troubleshooting |
| 2 | RJ45 connectors + boots | Field cable repair |
| 1 | RJ45 crimp tool | For cable repair |
| 1 | Multimeter | For voltage checks |
| 1 | Laminated wiring diagram | Reference during service |
| 1 | Laminated troubleshooting guide | Quick reference |

---

## Research Documentation

Detailed research reports available in `/rc-box/research/`:
- `ip_cameras_12mp_ip67.md` - Camera selection analysis
- `usb_cameras_12mp_ip67.md` - USB camera limitations
- `poe_power_12v.md` - 12V to PoE conversion options
- `poe_power_control.md` - Relay control solutions
- `ip_camera_boot_times.md` - Boot timing analysis

---

## Camera Lifespan Notice

**WARNING:** 15-minute power cycling = 96 cycles/day = ~35,000 cycles/year

| Operation Mode | Expected Lifespan |
|----------------|-------------------|
| Continuous (normal) | 6-10 years |
| Daily reboot | 5-8 years |
| 15-minute power cycle | **2-4 years** |

**Recommendations:**
1. Budget for camera replacement every 2-3 years
2. Keep 1 spare camera per station (included in spare parts kit)
3. Consider extending interval to 30 minutes if data requirements allow
4. Monitor for boot failures in logs

