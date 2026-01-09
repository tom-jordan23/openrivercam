# Travel & Import Strategy - Indonesia Deployment

**Travel Method:** Personal carry (checked + carry-on luggage)
**Status:** Humanitarian papers expected - duty exemption likely
**Date:** January 9, 2026

---

## Quick Reference

| Category | Carry from US | Source in Indonesia |
|----------|--------------|---------------------|
| Electronics (Pi, cameras, modem) | Yes | No |
| Batteries (LiFePO4 100Ah) | **NO** | Yes (Jakarta) |
| Conformal coating | Yes (small bottle OK) | No |
| Enclosures | Maybe | Preferred locally |
| Mounting hardware | Some | Bulk locally |
| Cables (Cat6, USB) | Yes | Available locally |
| Grounding equipment | No | Yes |
| Tools | Basic set | Supplement locally |

---

## Air Travel Restrictions

### Lithium/LiFePO4 Batteries

**CRITICAL:** The 100Ah LiFePO4 battery for Jakarta site CANNOT fly.

| Battery Type | Wh Rating | Carry-On | Checked | Status |
|--------------|-----------|----------|---------|--------|
| LiFePO4 100Ah 12V | 1,280 Wh | **NO** | **NO** | Must source locally |
| Small Li-ion (laptop) | <100 Wh | Yes | No | Normal rules |
| Power banks | <100 Wh | Yes (2 max) | No | Normal rules |
| Pi 5 (no battery) | N/A | Yes | Yes | No issue |

**Airline limits (typical):**
- Carry-on: Up to 100Wh without approval, 100-160Wh with airline approval
- Checked: Lithium batteries prohibited
- 1,280Wh battery: Not allowed on passenger aircraft

**Solution:** Purchase LiFePO4 battery in Jakarta
- Tokopedia, Shopee, or local battery suppliers
- Brands available: LiTime, Ampere Time, local equivalents
- Allow 1-2 days for local delivery

### Other Restricted Items

| Item | Restriction | Action |
|------|-------------|--------|
| Silicone sealant | Flammable/liquid | Source locally |
| Large spray cans | Pressurized | Not applicable (brush coating) |
| Sharp tools | Security | Check luggage only |
| Dielectric grease | Gel/paste OK | Small tube carry-on OK |
| IPA (alcohol) | <100mL liquid | Small bottle or source locally |
| Conformal coating 55mL | Liquid <100mL | Carry-on OK in liquids bag |

---

## Packing Strategy

### Carry-On Luggage (Critical Items)

Keep these with you - irreplaceable or long lead time:

| Item | Qty | Weight (est) | Notes |
|------|-----|--------------|-------|
| Raspberry Pi 5 (×3: 2 sites + 1 spare) | 3 | 0.15 kg | Keep in anti-static bags |
| Witty Pi 5 HAT+ (×3) | 3 | 0.1 kg | |
| Pi-EzConnect HAT (×3) | 3 | 0.1 kg | |
| Quectel EG25-G modems (×3) | 3 | 0.2 kg | With PU201 adapters |
| MicroSD cards (×6) | 6 | 0.05 kg | Pre-imaged |
| M.2 SSDs (×3) | 3 | 0.1 kg | Without enclosures |
| Custom USB camera | 1 | 0.1 kg | Long lead time item |
| ANNKE C1200 cameras (×3) | 3 | 1.0 kg | Fragile |
| LTE antennas (×6) | 6 | 0.2 kg | |
| USB relay (Numato) | 2 | 0.1 kg | |
| Laptop | 1 | 2.0 kg | For configuration |
| Documentation folder | 1 | 0.5 kg | Customs papers, manuals |
| **Carry-on total** | | **~4.5 kg** | Well under 7-10kg limit |

### Checked Luggage #1 (Electronics & Components)

| Item | Qty | Weight (est) | Notes |
|------|-----|--------------|-------|
| PoE injector (Planet IPOE-260-12V) | 2 | 0.8 kg | With spare |
| Mean Well SDR-120-12 PSU | 2 | 1.0 kg | With spare |
| Phoenix Contact surge protector | 2 | 0.6 kg | With spare |
| Victron BatteryProtect | 1 | 0.3 kg | |
| LiFePO4 charger | 1 | 0.5 kg | |
| USB SSD enclosures | 3 | 0.3 kg | |
| DIN rail (×4 × 1m sections) | 4 | 2.0 kg | Cut to fit |
| Terminal blocks | - | 0.5 kg | Assorted |
| Cable glands | - | 0.3 kg | Assorted M12/M16/M20 |
| IP67 LEDs | 6 | 0.1 kg | |
| IP67 pushbuttons | 3 | 0.1 kg | |
| Gore M12 vents | 6 | 0.1 kg | |
| VA Imaging camera housing | 2 | 1.0 kg | With spare |
| Tendelux IR lights | 2 | 0.8 kg | |
| PTC heaters | 4 | 0.4 kg | |
| Bulgin USB cables | 3 | 0.5 kg | |
| USB cables (short) | 10 | 0.3 kg | Assorted |
| **Checked #1 total** | | **~9.6 kg** | |

### Checked Luggage #2 (Cables, Hardware, Consumables)

| Item | Qty | Weight (est) | Notes |
|------|-----|--------------|-------|
| Cat6 outdoor cable spool | 1 | 5.0 kg | 100m (~300ft) - heavy |
| RJ45 connectors + boots | 50 | 0.2 kg | |
| RJ45 crimp tool | 1 | 0.3 kg | |
| Wire (18AWG, various) | - | 1.0 kg | Red/black spools |
| Fuse holders + fuses | - | 0.3 kg | |
| Heat shrink kit | 1 | 0.2 kg | |
| SS hardware kit | 2 | 1.0 kg | |
| Velcro/Dual-Lock | 2 | 0.2 kg | |
| Ferrule crimper kit | 1 | 0.5 kg | |
| Basic tool kit | 1 | 2.0 kg | Screwdrivers, wrenches, etc |
| Multimeter | 1 | 0.3 kg | |
| Ethernet tester | 1 | 0.2 kg | |
| Rain gauges (DFRobot) | 2 | 0.6 kg | With spare |
| Conformal coating (55mL) | 3 | 0.3 kg | |
| Kapton tape | 2 | 0.1 kg | |
| Cable ties (bags) | 2 | 0.4 kg | |
| **Checked #2 total** | | **~12.6 kg** | |

### Total Luggage Estimate

| Bag | Weight | Airline Limit (typical) |
|-----|--------|------------------------|
| Carry-on | ~4.5 kg | 7-10 kg |
| Checked #1 | ~9.6 kg | 23 kg |
| Checked #2 | ~12.6 kg | 23 kg |
| **Total** | **~26.7 kg** | **53-56 kg** |

**Status:** Well within typical airline limits. Room for personal items.

---

## Source Locally in Indonesia

### Jakarta - Required Local Purchases

| Item | Est. Cost (USD) | Where to Buy |
|------|-----------------|--------------|
| **LiFePO4 100Ah battery** | $300-400 | Tokopedia, Shopee, local battery shops |
| Grounding rod (1.5m copper) | $13 | Electrical supply stores |
| Ground cable (6 AWG, 10m) | $10 | Electrical supply |
| Ground lugs + clamps | $6 | Electrical supply |
| Mounting pole (4m galvanized) | $32 | Hardware stores, metal shops |
| Pole base flange | $13 | Hardware stores |
| U-bolts (stainless) | $6 | Hardware stores |
| Concrete + anchors | $6 | Hardware stores |
| Silicone sealant | $5 | Hardware stores |
| Electrical tape | $3 | Any store |
| **Jakarta local total** | **~$394-494** | |

### Sukabumi - Optional Local Purchases

| Item | Est. Cost (USD) | Where to Buy |
|------|-----------------|--------------|
| Enclosure (if not carrying) | $45 | Industrial supply |
| Cable conduit | $15 | Hardware stores |
| Stainless hardware (backup) | $10 | Hardware stores |
| **Sukabumi local total** | **~$70** | |

### Recommended Local Suppliers (Jakarta)

**Electronics:**
- Glodok Electronics Market (largest in Jakarta)
- Tokopedia.com (online marketplace)
- Shopee.co.id (online marketplace)

**Batteries:**
- Tokopedia: Search "LiFePO4 100Ah 12V"
- Local brands: Kijo, Aki Kering Jakarta
- Or specify LiTime/Ampere Time for known quality

**Hardware:**
- ACE Hardware (multiple Jakarta locations)
- Informa (similar to Home Depot)
- Local toko bangunan (hardware stores)

**Electrical Supply:**
- Glodok market
- Mega Elektrik (Jakarta)

---

## Customs & Import Documentation

### Required Documents

Prepare these before travel:

| Document | Purpose | Format |
|----------|---------|--------|
| **Humanitarian letter** | Establish non-commercial purpose | Original on letterhead |
| **Equipment manifest** | Detailed list with values | Printed spreadsheet |
| **Commercial invoice** | Shows purchase prices | From suppliers |
| **Packing list** | Box contents | Printed list |
| **Serial number list** | Pi, modem IMEI, cameras | Spreadsheet |
| **Project description** | Explain installation purpose | 1-page summary |
| **Passport** | Personal identification | Valid 6+ months |
| **Return ticket** | Prove temporary visit | E-ticket printout |

### Humanitarian Letter Template

Request from sponsoring organization (PMI or equivalent):

```
[Organization Letterhead]

To Whom It May Concern:

This letter confirms that [Your Name] is traveling to Indonesia on behalf of
[Organization] to install river monitoring equipment for flood early warning
purposes at humanitarian project sites.

The equipment being transported is:
- Computing equipment (Raspberry Pi computers)
- Cameras and sensors
- Power management equipment
- Mounting hardware and cables

This equipment is for permanent installation at project sites operated by
Palang Merah Indonesia (Indonesian Red Cross) and will not be resold or
used for commercial purposes.

Total estimated value: USD $3,000

Contact: [Organization contact info]

Sincerely,
[Signature]
[Name, Title]
```

### Equipment Manifest Format

| # | Description | Qty | Unit Value | Total | Serial/IMEI |
|---|-------------|-----|------------|-------|-------------|
| 1 | Raspberry Pi 5 8GB | 3 | $80 | $240 | N/A |
| 2 | Quectel EG25-G modem | 3 | $35 | $105 | IMEI: xxx |
| 3 | ANNKE C1200 camera | 3 | $60 | $180 | SN: xxx |
| ... | ... | ... | ... | ... | ... |

**Include:** All items with individual value >$50

### HS Codes (If Asked)

| Category | HS Code | Description |
|----------|---------|-------------|
| Computers | 8471.50.00 | Processing units |
| Modems | 8517.62.90 | Transmission apparatus |
| Cameras | 8525.80.30 | Television cameras |
| Power supplies | 8504.40.90 | Static converters |
| Batteries | 8507.60.00 | Lithium-ion (if any small ones) |
| Cables | 8544.42.00 | Electric conductors |
| Connectors | 8536.69.90 | Electrical connectors |

### Indonesian Customs Notes

**What to Expect:**
- Green channel (nothing to declare) usually works for humanitarian equipment
- If questioned, show humanitarian letter and equipment manifest
- Customs officers may inspect bags - keep equipment organized
- Declare honestly if asked about value

**Potential Issues:**
- Multiple identical items may raise "commercial goods" suspicion
  - Counter: Show humanitarian letter, explain two separate sites
- High-value electronics
  - Counter: Show receipts, emphasize non-commercial installation
- LTE modem IMEI
  - May need registration with POSTEL (see below)

**Duty Rates (If Applied):**
- Electronics: 0-10%
- Cameras: 0-5%
- Most goods: 7.5% average
- VAT: 11% on CIF value
- **With humanitarian papers:** Likely 0%

---

## IMEI Registration

### Quectel EG25-G Modem

Indonesian regulations require IMEI registration for cellular devices.

**Process:**
1. Record IMEI numbers before travel (printed on modem or via AT command)
2. Register at: https://imei.kemenperin.go.id/
3. Fee: ~IDR 300,000 ($20) per device
4. Timeline: 1-2 business days
5. Can be done after arrival in Indonesia

**Required for Registration:**
- Passport copy
- Device IMEI number
- Purchase receipt
- Device photo

**Alternative:**
- Use local SIM and register within 60 days of arrival
- Most tourists/short-term visitors skip this
- For permanent installation, registration recommended

---

## Pre-Travel Checklist

### 2 Weeks Before

- [ ] Confirm all components received and tested
- [ ] Apply conformal coating to all PCBs (24hr cure)
- [ ] Pre-configure cameras (static IP, RTSP enabled)
- [ ] Load OS images on all SD cards
- [ ] Record all serial numbers and IMEI numbers
- [ ] Request humanitarian letter from organization
- [ ] Prepare equipment manifest spreadsheet
- [ ] Print all customs documentation

### 1 Week Before

- [ ] Pack carry-on with critical electronics (use anti-static bags)
- [ ] Pack checked luggage #1 and #2
- [ ] Weigh all bags (confirm under limits)
- [ ] Confirm flight allows 2 checked bags
- [ ] Research Jakarta battery suppliers (have backup options)
- [ ] Confirm local contact will receive you / assist with procurement

### Day of Travel

- [ ] Carry-on: All critical electronics, laptop, documentation folder
- [ ] Checked: All other components
- [ ] Keep customs documentation easily accessible
- [ ] Have organization contact number ready (if questioned)

### Upon Arrival

- [ ] Clear customs (green channel, show papers if asked)
- [ ] Purchase LiFePO4 battery within 1-2 days
- [ ] Purchase local hardware items (grounding, pole, etc.)
- [ ] Begin IMEI registration if staying >60 days

---

## Emergency Contacts

**In Indonesia:**
- PMI Jakarta: [Add contact]
- Local fixer/translator: [Add contact]

**Suppliers (Jakarta):**
- Glodok market is in West Jakarta, open daily
- ACE Hardware: Multiple locations, check Google Maps

**US-Based Support:**
- Equipment supplier contacts (if warranty issues)
- Organization HQ contact

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Customs delays | Have all documentation ready, arrive with time buffer |
| Equipment damaged in transit | Use hard cases, pack fragile items in carry-on |
| Battery not available locally | Research multiple suppliers, have backup plan |
| IMEI registration required | Start process immediately on arrival |
| Lost luggage | Critical items in carry-on, have spares in second checked bag |
| Component DOA | Test everything before departure, carry spares |

---

**Document Version:** 1.0
**Last Updated:** January 9, 2026
