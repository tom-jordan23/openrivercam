# InaCORS / NTRIP Research for Indonesia RTK Surveys

**Purpose:** Document the InaCORS (Indonesian CORS) NTRIP service for use with ArduSimple RTK rover in Indonesia deployments.
**Last Updated:** 2026-03-03

---

## What is InaCORS?

InaCORS (Indonesian Continuously Operating Reference Station) is a national GNSS CORS network operated by BIG (Badan Informasi Geospasial — the Indonesian Geospatial Information Agency). The network provides real-time GNSS corrections via NTRIP (Networked Transport of RTCM via Internet Protocol), enabling RTK positioning without deploying your own base station.

### Key Facts

- **Operator:** BIG (Badan Informasi Geospasial)
- **Network Size:** 200+ permanent reference stations across Indonesia (as of 2024)
- **Service:** Free for registered users
- **Coverage:** Nationwide, with denser coverage on Java
- **Coordinate Reference:** SRGI2013 (Sistem Referensi Geospasial Indonesia 2013), which is aligned with ITRF2008 epoch 2012.0 — practically equivalent to WGS84 for centimeter-level work
- **Corrections:** VRS (Virtual Reference Station) and nearest-station modes

---

## NTRIP Connection Parameters

These are the confirmed connection parameters for InaCORS:

| Parameter | Value | Notes |
|-----------|-------|-------|
| **NTRIP Caster Host** | `nrtk.big.go.id` | Primary hostname |
| **IP Address (fallback)** | `103.22.171.6` | Use if DNS resolution fails |
| **Port** | `2001` | **Non-standard** — most NTRIP casters use 2101 |
| **Mountpoint (primary)** | `VRS` | Virtual Reference Station — interpolates corrections for your position |
| **Mountpoint (fallback)** | `nearest` | Connects to the single nearest physical station |
| **NTRIP Version** | `1.0` | Some clients may also work with v2.0 |
| **Send NMEA GGA** | **YES** | Required for VRS — the caster needs your position to generate virtual corrections |
| **Username** | From registration | Free account |
| **Password** | From registration | Free account |

### Important Notes on Port

The standard NTRIP port is 2101. InaCORS uses port **2001**. This is a common source of connection failures — if you use the default port in your NTRIP client, it will not connect. Always explicitly set port 2001.

### VRS vs Nearest Mountpoint

- **VRS (Virtual Reference Station):** The caster receives your rover's approximate position (via NMEA GGA messages), then interpolates corrections from surrounding physical stations to create a "virtual" reference station near you. This provides the best accuracy because corrections are tailored to your location. Requires the rover to send its position back to the caster.

- **nearest:** Connects you to the single closest physical reference station. Simpler (no position feedback needed), but accuracy degrades with distance from that station. Useful as a fallback if VRS is not available or if the rover's NTRIP client doesn't support sending GGA.

---

## Registration

### How to Register

1. Navigate to: **http://nrtk.big.go.id/sbc/Account/Register**
2. Fill in the registration form:
   - Name, email, phone number
   - Institution/organization
   - Purpose of use
3. Receive credentials via email
4. Log in at: http://nrtk.big.go.id/sbc/

### Registration Notes

- Registration is free and open to anyone
- Accounts may take 1-2 business days to activate (register well before your field day)
- Indonesian phone number may be required — a local Telkomsel SIM works
- The registration portal is in Indonesian (Bahasa Indonesia) — use browser translation if needed

---

## Coverage

### Coverage Check

Use the BIG SRGI service checker to verify coverage at your survey site:

- **URL:** https://srgi.big.go.id/page/service-check
- Enter your site coordinates or browse the map
- Green zones indicate good CORS coverage; red/blank indicates gaps

### Coverage by Region

- **Java:** Excellent coverage — dense station network, most stations within 30-50km of each other
- **Sumatra:** Good coverage along major corridors
- **Kalimantan:** Moderate coverage, concentrated around cities
- **Sulawesi:** Moderate coverage
- **Papua:** Limited coverage — base station fallback recommended

### For Sukabumi and Jakarta Sites

Both Sukabumi (West Java) and Jakarta are in areas with excellent InaCORS coverage. Multiple CORS stations are within 30-50km, providing strong VRS geometry. Cell data coverage (Telkomsel 4G) is reliable at both locations.

---

## Cell Data Requirements

NTRIP requires a mobile data connection between the rover's NTRIP client and the InaCORS caster. The bandwidth requirements are minimal:

- **Upstream (rover → caster):** ~50 bytes/second (NMEA GGA messages)
- **Downstream (caster → rover):** ~500 bytes/second (RTCM3 corrections)
- **Total:** ~1-2 KB/second, or roughly 3-7 MB/hour
- **A full survey day (8 hours):** ~25-60 MB of data

### Recommended Provider

- **Telkomsel:** Best 4G coverage across Indonesia, including rural areas near rivers
- **Indosat Ooredoo:** Good alternative in urban areas
- Prepaid SIM with data package is sufficient — even 1GB lasts multiple survey days

### Connection Method

The NTRIP client runs on the Android phone that's already connected to the ArduSimple rover via USB. The phone uses its cellular data connection to reach the InaCORS caster. No additional hardware is needed.

Two software options for NTRIP client:
1. **SW Maps** — has built-in NTRIP client support (simplest setup)
2. **GNSS Master** — can act as NTRIP client and feed corrections to the rover

---

## Accuracy Expectations

### With NTRIP (InaCORS VRS)

- **Horizontal:** 2-3 cm (with RTK FIX)
- **Vertical:** 3-5 cm (with RTK FIX)
- **Absolute accuracy:** These are absolute positions in SRGI2013/WGS84 — no PPP post-processing needed
- **Time to FIX:** Typically 10-60 seconds after NTRIP connection established

### Comparison: NTRIP vs Base Station + PPP

| Aspect | NTRIP (InaCORS) | Base Station + PPP |
|--------|------------------|--------------------|
| **Absolute accuracy** | 2-5 cm (real-time) | 2-5 cm (after 6-8hr PPP processing) |
| **Field setup** | Connect phone to NTRIP — no base station needed | Deploy base, survey-in, start RINEX logging |
| **Post-processing** | None required | Convert UBX → RINEX → submit to AUSPOS → wait → apply translation |
| **Equipment** | Rover + phone + SIM | Rover + phone + base station + tripod + radio |
| **Dependencies** | Cell data coverage | None (self-contained) |
| **Time to accuracy** | Immediate (with RTK FIX) | 1-2 days (waiting for PPP results) |

### Cross-Validation Approach

For maximum confidence, especially on first deployments, you can use **both methods simultaneously**:

1. Connect rover to InaCORS NTRIP for real-time absolute positions
2. Also deploy the base station logging RINEX data
3. Post-process base station data with AUSPOS/CSRS-PPP
4. Compare NTRIP-derived positions against PPP-corrected positions
5. Agreement within 3-5 cm confirms both methods are working correctly

This "belt and suspenders" approach validates the NTRIP workflow against the established PPP workflow.

---

## Coordinate Reference System

### SRGI2013

InaCORS corrections are referenced to SRGI2013 (Sistem Referensi Geospasial Indonesia 2013):

- Based on ITRF2008, epoch 2012.0
- Practically equivalent to WGS84 for centimeter-level work
- The difference between SRGI2013 and WGS84 (ITRF2014) is sub-centimeter in Indonesia — negligible for our purposes
- Your rover will output coordinates in WGS84 by default, and the NTRIP corrections will place them in the SRGI2013/WGS84 frame

### Practical Implication

For OpenRiverCam deployments, you can treat SRGI2013 coordinates as WGS84 without transformation. The sub-centimeter difference is well within survey accuracy requirements. Continue using your UTM zone (e.g., EPSG:32748 for UTM 48S) for projected coordinates.

---

## Troubleshooting

### Connection Fails

1. **Check port number** — must be 2001, not 2101
2. **Check cell data** — open a webpage to verify internet connectivity
3. **Check credentials** — log into the web portal to verify account is active
4. **Try IP address** — use `103.22.171.6` instead of hostname if DNS fails
5. **Try "nearest" mountpoint** — VRS may be temporarily unavailable

### No RTK FIX After NTRIP Connected

1. **Verify corrections flowing** — GNSS Master or SW Maps should show correction age updating
2. **Wait longer** — initial convergence can take 1-2 minutes
3. **Check satellite count** — need ≥8 common satellites between rover and CORS station
4. **Move to open sky** — same requirements as local base station RTK

### NTRIP Disconnects During Survey

1. **Check cell signal** — move to higher ground or clearer area
2. **SW Maps/GNSS Master auto-reconnect** — most clients reconnect automatically
3. **Correction age** — if correction age exceeds 30 seconds, pause survey and wait for reconnection
4. **Fallback:** If cell coverage is unreliable at the site, switch to local base station method

### VRS Not Available

1. **Try "nearest" mountpoint** — individual station corrections still work
2. **Check coverage map** — your site may be outside VRS coverage
3. **Fall back to base station** — InaCORS may have maintenance or outages

---

## References and Sources

- BIG InaCORS Portal: http://nrtk.big.go.id/sbc/
- BIG SRGI Service Check: https://srgi.big.go.id/page/service-check
- InaCORS Registration: http://nrtk.big.go.id/sbc/Account/Register
- NTRIP Protocol: RTCM Standard 10410.1 (Networked Transport of RTCM via Internet Protocol)
- SRGI2013 Documentation: BIG Regulation No. 15/2013

---

## Quick Reference Card

```
NTRIP Caster Host:  nrtk.big.go.id
IP (fallback):      103.22.171.6
Port:               2001
Mountpoint:         VRS  (Java); nearest (fallback)
NTRIP Version:      1.0
Send NMEA GGA:      YES
Registration:       http://nrtk.big.go.id/sbc/Account/Register
Coverage check:     https://srgi.big.go.id/page/service-check
Coordinate system:  SRGI2013 (≈ WGS84/ITRF2014 for practical purposes)
```
