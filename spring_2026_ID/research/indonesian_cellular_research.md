# Indonesian Cellular Network Compatibility Research
## Quectel EG25-G LTE Modem

**Research Date:** January 9, 2026
**Purpose:** Verify compatibility of Quectel EG25-G LTE modem with Indonesian cellular carriers
**Prepared for:** OpenRiverCam Spring 2026 Indonesia Deployment

---

## Executive Summary

**Key Findings:**

1. **Full LTE Compatibility Confirmed:** The Quectel EG25-G supports all primary LTE bands used by major Indonesian carriers (Bands 1, 3, 8, and 40).

2. **Strong Multi-Carrier Support:** The modem is compatible with all five targeted Indonesian carriers: Telkomsel, Indosat Ooredoo, XL Axiata, Tri, and Smartfren.

3. **Fallback Coverage Available:** The EG25-G supports 3G WCDMA Band 1 (2100 MHz) for rural areas, though 3G networks are being phased out. 2G GSM support provides emergency fallback.

4. **Single SKU Solution:** The EG25-G is a "Global" variant with worldwide coverage, eliminating the need for region-specific models.

5. **Certification Consideration:** While the EG25-G has extensive international certifications (GCF, CE, FCC, PTCRB, RCM, IMDA, NBTC), Indonesian DJID/SDPPI certification should be verified for commercial deployment.

**Recommendation:** The Quectel EG25-G is suitable for deployment in Indonesia with excellent compatibility across all major carriers.

---

## 1. Quectel EG25-G Technical Specifications

### 1.1 Module Overview

The Quectel EG25-G is an LTE Cat 4 module optimized for M2M and IoT applications, adopting 3GPP Release 11 LTE technology. Key characteristics:

- **Form Factor:** LGA (29.0mm × 32.0mm × 2.4mm)
- **Weight:** Approx. 4.9g
- **Supply Voltage:** 3.3-4.3V (3.8V typical)
- **Global Variant:** Single SKU for worldwide deployment

### 1.2 Supported Frequency Bands

#### LTE-FDD Bands
**B1/B2/B3/B4/B5/B7/B8/B12/B13/B18/B19/B20/B25/B26/B28**

Breakdown:
- **B1:** 2100 MHz
- **B2:** 1900 MHz (PCS)
- **B3:** 1800 MHz (DCS)
- **B4:** 1700/2100 MHz (AWS-1)
- **B5:** 850 MHz
- **B7:** 2600 MHz
- **B8:** 900 MHz
- **B12:** 700 MHz (Lower SMH)
- **B13:** 700 MHz (Upper SMH)
- **B18:** 800 MHz (Lower)
- **B19:** 800 MHz (Upper)
- **B20:** 800 MHz (Digital Dividend)
- **B25:** 1900 MHz (Extended PCS)
- **B26:** 850 MHz (Extended Cellular)
- **B28:** 700 MHz (APT)

#### LTE-TDD Bands
**B38/B39/B40/B41**

Breakdown:
- **B38:** 2600 MHz
- **B39:** 1900 MHz
- **B40:** 2300 MHz
- **B41:** 2500 MHz

#### WCDMA/UMTS Bands (3G Fallback)
**B1/B2/B4/B5/B6/B8/B19**

Breakdown:
- **B1:** 2100 MHz (IMT)
- **B2:** 1900 MHz (PCS)
- **B4:** 1700/2100 MHz (AWS)
- **B5:** 850 MHz (Cellular)
- **B6:** 800 MHz (UMTS only)
- **B8:** 900 MHz (Extended GSM)
- **B19:** 800 MHz (Japan)

#### GSM Bands (2G Emergency Fallback)
**B2/B3/B5/B8**

Breakdown:
- **B2:** 1900 MHz (DCS 1900/PCS)
- **B3:** 1800 MHz (DCS 1800)
- **B5:** 850 MHz
- **B8:** 900 MHz (EGSM 900)

### 1.3 Performance Specifications

| Technology | Downlink Speed | Uplink Speed |
|------------|----------------|--------------|
| LTE-FDD | Max. 150 Mbps | Max. 50 Mbps |
| LTE-TDD | Max. 130 Mbps | Max. 30 Mbps |
| DC-HSDPA | Max. 42 Mbps | - |
| HSUPA | - | Max. 5.76 Mbps |
| WCDMA | Max. 384 kbps | Max. 384 kbps |
| EDGE | Max. 296 kbps | Max. 236.8 kbps |
| GPRS | Max. 107 kbps | Max. 85.6 kbps |

### 1.4 Additional Features

- **GNSS Support:** Qualcomm IZat location technology Gen8C Lite (GPS, GLONASS, BeiDou, Galileo, QZSS)
- **Backward Compatibility:** EDGE and GSM/GPRS networks for remote area connectivity
- **Carrier Certifications:** Verizon, AT&T, Sprint, U.S. Cellular, T-Mobile (US); Deutsche Telekom (Europe); Telus, Rogers (Canada)
- **Regulatory Certifications:** GCF, CE, FCC, PTCRB, IC, Anatel, IFETEL, SRRC, CCC, NAL, KC, NCC, JATE, TELEC, RCM, IMDA, ICASA

### 1.5 Regional Variants

**Important Note:** Unlike the Quectel EC25 series (which has 14 regional variants), the **EG25-G is a single "Global" SKU** with the "-G" suffix denoting global coverage. This eliminates the need for separate EMEA, APAC, or Americas variants and simplifies inventory management for international deployments.

---

## 2. Indonesian Cellular Market Overview

### 2.1 Market Structure

Indonesia's telecommunications sector is dominated by four major network operators with a fifth specialized carrier:

1. **Telkomsel** - Market leader, ~40% market share, 98% population coverage
2. **Indosat Ooredoo Hutchison (IOH)** - ~21% market share (merged with Tri/Hutchison 3 in January 2022)
3. **XL Axiata** - Major carrier, extensive urban and rural coverage
4. **Tri (3)** - Now part of Indosat Ooredoo Hutchison
5. **Smartfren** - CDMA/LTE specialist using less common frequency bands

### 2.2 Network Technology Status

#### LTE (4G)
All major carriers have deployed extensive LTE networks using primarily:
- **Band 3 (1800 MHz)** - Primary band, all major carriers
- **Band 8 (900 MHz)** - Secondary band for coverage
- **Band 40 (2300 MHz TDD)** - Capacity band, Telkomsel and Smartfren
- **Band 1 (2100 MHz)** - Limited deployment, some carriers

#### WCDMA (3G)
**Status: Being Phased Out**
- Starting in 2022, Indonesian operators began shutting down 3G networks
- Spectrum is being reallocated to 4G LTE and 5G services
- **Band 1 (2100 MHz)** was the primary 3G band
- Limited ongoing 3G support; not recommended for primary connectivity

#### GSM (2G)
**Status: Legacy Emergency Fallback Only**
- **900 MHz and 1800 MHz** still available on some networks
- Gradually being decommissioned
- Should not be relied upon for primary connectivity

#### 5G
**Status: Early Deployment**
- **5G NR N1 (2100 MHz)** - Telkomsel, XL Axiata (since 2024)
- **5G NR N3 (1800 MHz)** - XL Axiata (since 2024)
- **5G NR N40 (2300 MHz)** - Telkomsel (first operator with Band 40 5G)
- Not relevant for EG25-G (LTE Cat 4 module)

---

## 3. Indonesian Carrier Band Analysis

### 3.1 Telkomsel (Indonesia's Largest Carrier)

**Market Position:**
- Largest carrier with ~40% market share
- Best coverage: 98% of Indonesia including outer islands
- Active in all provinces
- Strong urban and rural presence

**Frequency Bands:**

#### LTE (4G)
- **Band 3 (1800 MHz FDD-LTE):** 22.5 MHz bandwidth - PRIMARY BAND
- **Band 8 (900 MHz FDD-LTE):** 7.5 MHz bandwidth - COVERAGE BAND
- **Band 40 (2300 MHz TDD-LTE):** 30 MHz bandwidth - CAPACITY BAND

#### WCDMA (3G) - Being Phased Out
- **Band 1 (2100 MHz):** 15 MHz bandwidth - LEGACY

#### GSM (2G) - Mostly Decommissioned
- **900 MHz** - Limited legacy support
- **1800 MHz (DCS)** - Removed as of August 2024

#### 5G (Recent Deployment)
- **5G NR N1 (2100 MHz)** - Added August 2024
- **5G NR N40 (2300 MHz)** - First operator to deploy

**EG25-G Compatibility with Telkomsel:**
- ✅ **LTE Band 3 (1800 MHz)** - FULLY SUPPORTED
- ✅ **LTE Band 8 (900 MHz)** - FULLY SUPPORTED
- ✅ **LTE Band 40 (2300 MHz TDD)** - FULLY SUPPORTED
- ✅ **WCDMA Band 1 (2100 MHz)** - SUPPORTED (fallback)
- ✅ **GSM 900 MHz** - SUPPORTED (emergency fallback)

**Verdict: EXCELLENT COMPATIBILITY** - All primary LTE bands supported

---

### 3.2 Indosat Ooredoo Hutchison (IOH)

**Market Position:**
- ~21% market share
- Result of Indosat Ooredoo and Hutchison 3 Indonesia (Tri) merger (January 2022)
- Over 70% population coverage
- Strong in major cities: Jakarta, Bali, Sumatra
- Slightly less coverage in remote areas vs. Telkomsel

**Frequency Bands:**

#### LTE (4G)
- **Band 3 (1800 MHz FDD-LTE):** 20 MHz bandwidth - PRIMARY BAND
- **Band 8 (900 MHz FDD-LTE):** 10 MHz bandwidth - COVERAGE BAND
- **Band 1 (2100 MHz FDD-LTE):** 20 MHz bandwidth - ADDITIONAL (since 2017)

**Deployment Strategy:**
- Dual-carrier in major cities (Bandung, Jakarta, Denpasar, Yogyakarta): Band 8 + Band 3
- Single-carrier elsewhere (Surabaya, Surakarta, Semarang, Malang, Makassar): Band 3

#### WCDMA (3G) - Removed
- **Band 1 (2100 MHz)** - Removed as of August 2024
- **Band 8 (900 MHz GSM)** - Removed as of August 2024

#### GSM (2G) - Decommissioned
- **1800 MHz (DCS)** - Removed as of August 2024

#### Spectrum Holdings
- 850 MHz: 2.5 MHz
- 900 MHz: 10 MHz
- 1800 MHz: 20 MHz
- 2100 MHz: 20 MHz

**EG25-G Compatibility with Indosat Ooredoo Hutchison:**
- ✅ **LTE Band 3 (1800 MHz)** - FULLY SUPPORTED
- ✅ **LTE Band 8 (900 MHz)** - FULLY SUPPORTED
- ✅ **LTE Band 1 (2100 MHz)** - FULLY SUPPORTED
- ⚠️ **WCDMA** - No longer available (removed 2024)
- ⚠️ **GSM** - No longer available (removed 2024)

**Verdict: EXCELLENT LTE COMPATIBILITY** - All LTE bands supported, though no 3G/2G fallback

---

### 3.3 XL Axiata

**Market Position:**
- Major carrier with significant market share
- First to commercially launch 4.5G Ready on 1800 MHz spectrum
- Good urban and suburban coverage

**Frequency Bands:**

#### LTE (4G)
- **Band 3 (1800 MHz FDD-LTE):** 22.5 MHz bandwidth - PRIMARY BAND
- **Band 8 (900 MHz FDD-LTE):** 7.5 MHz bandwidth - COVERAGE BAND

#### WCDMA (3G) - Removed
- **Band 1 (2100 MHz)** - Removed as of August 2024

#### GSM (2G) - Decommissioned
- **1800 MHz (DCS)** - Removed as of August 2024

#### 5G (Recent Deployment)
- **5G NR N1 (2100 MHz)** - Added August 2024
- **5G NR N3 (1800 MHz)** - Added August 2024

#### Spectrum Holdings
- 900 MHz: 7.5 MHz
- 1800 MHz: 22.5 MHz
- 2100 MHz: 15 MHz
- Total: 45 MHz

**EG25-G Compatibility with XL Axiata:**
- ✅ **LTE Band 3 (1800 MHz)** - FULLY SUPPORTED
- ✅ **LTE Band 8 (900 MHz)** - FULLY SUPPORTED
- ⚠️ **WCDMA** - No longer available (removed 2024)
- ⚠️ **GSM** - No longer available (removed 2024)

**Verdict: EXCELLENT LTE COMPATIBILITY** - Primary LTE bands supported, though no 3G/2G fallback

---

### 3.4 Tri (3) - Now Part of Indosat Ooredoo Hutchison

**Market Position:**
- Merged with Indosat Ooredoo in January 2022
- Network now operates under Indosat Ooredoo Hutchison (IOH) brand
- Previous coverage: 227 cities in 25 provinces

**Frequency Bands (Historical):**

#### LTE (4G)
- **Band 3 (1800 MHz FDD-LTE):** 10 MHz bandwidth - PRIMARY BAND (started 2015)
- **Band 1 (2100 MHz FDD-LTE):** 15 MHz bandwidth - ADDITIONAL (auctioned 2017)

#### GSM (2G)
- **900 MHz and 1800 MHz** - Legacy support

**EG25-G Compatibility with Tri/IOH Network:**
- ✅ **LTE Band 3 (1800 MHz)** - FULLY SUPPORTED
- ✅ **LTE Band 1 (2100 MHz)** - FULLY SUPPORTED
- ✅ **GSM 900/1800 MHz** - SUPPORTED (emergency fallback if still active)

**Verdict: EXCELLENT COMPATIBILITY** - Now operates on IOH infrastructure with full band support

---

### 3.5 Smartfren

**Market Position:**
- Specialized LTE carrier
- Uses less common frequency bands
- Good coverage in major cities
- May have limited rural coverage

**Frequency Bands:**

#### LTE (4G) - SPECIALIZED BANDS
- **Band 5 (850 MHz FDD-LTE):** 10 MHz bandwidth - COVERAGE BAND (RARE)
- **Band 40 (2300 MHz TDD-LTE):** 30 MHz bandwidth - CAPACITY BAND

**Note:** Smartfren primarily uses **Band 5 (850 MHz)** and **Band 40 (2300 MHz TDD)**, which are less common in Indonesia.

#### Former Bands
- **Band 3 (1800 MHz)** - Removed as of August 2024

#### Technology
- LTE Advanced with carrier aggregation
- Higher speeds through CA technology

**EG25-G Compatibility with Smartfren:**
- ✅ **LTE Band 5 (850 MHz)** - FULLY SUPPORTED
- ✅ **LTE Band 40 (2300 MHz TDD)** - FULLY SUPPORTED
- ❌ **No 3G/2G Fallback** - Smartfren is LTE-only network

**Verdict: EXCELLENT COMPATIBILITY** - All active LTE bands supported despite unusual band selection

---

## 4. Band Compatibility Matrix

### 4.1 Complete Compatibility Table

| Band | Frequency | Type | EG25-G Support | Telkomsel | Indosat IOH | XL Axiata | Tri (IOH) | Smartfren |
|------|-----------|------|----------------|-----------|-------------|-----------|-----------|-----------|
| **B1** | 2100 MHz | LTE-FDD | ✅ YES | ❌ No | ✅ YES | ❌ No | ✅ YES | ❌ No |
| **B3** | 1800 MHz | LTE-FDD | ✅ YES | ✅ PRIMARY | ✅ PRIMARY | ✅ PRIMARY | ✅ PRIMARY | ❌ Removed |
| **B5** | 850 MHz | LTE-FDD | ✅ YES | ❌ No | ❌ No | ❌ No | ❌ No | ✅ PRIMARY |
| **B7** | 2600 MHz | LTE-FDD | ✅ YES | ❌ No | ❌ No | ❌ No | ❌ No | ❌ No |
| **B8** | 900 MHz | LTE-FDD | ✅ YES | ✅ COVERAGE | ✅ COVERAGE | ✅ COVERAGE | Via IOH | ❌ No |
| **B28** | 700 MHz | LTE-FDD | ✅ YES | ❌ No | ❌ No | ❌ No | ❌ No | ❌ No |
| **B40** | 2300 MHz | LTE-TDD | ✅ YES | ✅ CAPACITY | ❌ No | ❌ No | ❌ No | ✅ CAPACITY |
| **B41** | 2500 MHz | LTE-TDD | ✅ YES | ❌ No | ❌ No | ❌ No | ❌ No | ❌ No |

### 4.2 3G/WCDMA Fallback Compatibility

| Band | Frequency | EG25-G Support | Telkomsel | Indosat IOH | XL Axiata | Tri (IOH) | Smartfren |
|------|-----------|----------------|-----------|-------------|-----------|-----------|-----------|
| **B1** | 2100 MHz | ✅ YES | ⚠️ Phasing Out | ❌ Removed 2024 | ❌ Removed 2024 | ❌ Removed | ❌ N/A |
| **B8** | 900 MHz | ✅ YES | ⚠️ Phasing Out | ❌ Removed 2024 | ❌ N/A | ❌ N/A | ❌ N/A |

**Note:** 3G networks across Indonesia are being shut down (started 2022) to reallocate spectrum for 4G/5G. Do not rely on 3G for primary connectivity.

### 4.3 2G/GSM Emergency Fallback Compatibility

| Band | Frequency | EG25-G Support | Telkomsel | Indosat IOH | XL Axiata | Tri (IOH) | Smartfren |
|------|-----------|----------------|-----------|-------------|-----------|-----------|-----------|
| **GSM 900** | 900 MHz | ✅ YES | ⚠️ Limited | ❌ Removed | ❌ Removed | ⚠️ Legacy | ❌ N/A |
| **GSM 1800** | 1800 MHz | ✅ YES | ❌ Removed 2024 | ❌ Removed 2024 | ❌ Removed 2024 | ⚠️ Legacy | ❌ N/A |

**Note:** 2G/GSM is being decommissioned across Indonesia. Should only be considered for emergency fallback, not primary connectivity.

---

## 5. Coverage and Performance Analysis

### 5.1 Primary LTE Band Performance

#### Band 3 (1800 MHz) - Universal Primary Band
- **Coverage:** Good urban and suburban coverage
- **Penetration:** Moderate building penetration
- **Capacity:** High capacity, wide bandwidth allocations
- **Carriers Using:** Telkomsel (22.5 MHz), Indosat IOH (20 MHz), XL Axiata (22.5 MHz), Tri
- **EG25-G Support:** ✅ FULL
- **Data Rates:** Up to 150 Mbps downlink, 50 Mbps uplink
- **Recommendation:** This is the most important band for Indonesian deployment

#### Band 8 (900 MHz) - Coverage Band
- **Coverage:** Excellent rural and wide-area coverage
- **Penetration:** Excellent building and vegetation penetration
- **Capacity:** Lower capacity, narrower bandwidth (7.5 MHz typical)
- **Carriers Using:** Telkomsel, Indosat IOH (10 MHz), XL Axiata
- **EG25-G Support:** ✅ FULL
- **Use Case:** Rural areas, indoor coverage, long-range connectivity
- **Recommendation:** Critical for rural/remote deployments

#### Band 40 (2300 MHz TDD) - Capacity Band
- **Coverage:** Urban/high-density areas
- **Penetration:** Lower penetration, limited indoor reach
- **Capacity:** Very high capacity, 30 MHz bandwidth
- **Carriers Using:** Telkomsel, Smartfren
- **EG25-G Support:** ✅ FULL
- **Data Rates:** Up to 130 Mbps downlink, 30 Mbps uplink (TDD)
- **Use Case:** High-data-rate applications in urban areas
- **Recommendation:** Excellent for urban deployments with high bandwidth needs

#### Band 1 (2100 MHz) - Supplementary Band
- **Coverage:** Moderate urban coverage
- **Penetration:** Moderate building penetration
- **Capacity:** Medium to high capacity
- **Carriers Using:** Indosat IOH (20 MHz), Tri (15 MHz)
- **EG25-G Support:** ✅ FULL
- **Use Case:** Additional capacity in specific networks
- **Recommendation:** Useful for Indosat/Tri networks

#### Band 5 (850 MHz) - Smartfren Specific
- **Coverage:** Excellent wide-area and rural coverage
- **Penetration:** Excellent building penetration (lower frequency)
- **Capacity:** Lower capacity, 10 MHz bandwidth
- **Carriers Using:** Smartfren only
- **EG25-G Support:** ✅ FULL
- **Use Case:** Smartfren network connectivity
- **Recommendation:** Only relevant if using Smartfren

### 5.2 Carrier-Specific Recommendations

#### Best Overall Coverage: Telkomsel
- **Strengths:** 98% population coverage, all provinces, best rural reach
- **Key Bands:** B3 (1800 MHz), B8 (900 MHz), B40 (2300 MHz)
- **EG25-G Match:** Perfect - all bands supported
- **Recommended For:** Maximum reliability, rural deployments, nationwide coverage
- **Expected Performance:** Excellent in urban and rural areas

#### Best Urban Performance: Telkomsel or Smartfren
- **Telkomsel:** B40 (2300 MHz TDD) provides high capacity in cities
- **Smartfren:** B40 (2300 MHz TDD) with B5 (850 MHz) fallback
- **EG25-G Match:** Perfect - both carrier bands supported
- **Recommended For:** High-bandwidth urban applications
- **Expected Performance:** 50-130 Mbps depending on band and conditions

#### Good Alternative: Indosat IOH or XL Axiata
- **Strengths:** Good urban coverage, competitive pricing, 70%+ population coverage
- **Key Bands:** B3 (1800 MHz), B8 (900 MHz)
- **EG25-G Match:** Perfect - all bands supported
- **Recommended For:** Cost-effective deployments in populated areas
- **Expected Performance:** Very good in urban areas, moderate in rural areas

### 5.3 Rural vs Urban Deployment Considerations

#### Urban/Suburban Deployments
**Primary Band:** Band 3 (1800 MHz)
- Available on all major carriers (Telkomsel, Indosat IOH, XL Axiata)
- High capacity, good coverage
- EG25-G fully compatible

**Capacity Enhancement:** Band 40 (2300 MHz TDD)
- Available on Telkomsel and Smartfren
- Very high data rates
- EG25-G fully compatible

**Recommendation:** Any major carrier will work well. Telkomsel recommended for maximum reliability.

#### Rural/Remote Deployments
**Primary Band:** Band 8 (900 MHz)
- Best propagation characteristics
- Excellent penetration through vegetation and buildings
- Available on Telkomsel, Indosat IOH, XL Axiata
- EG25-G fully compatible

**Alternative:** Band 5 (850 MHz) - Smartfren only
- Similar propagation to Band 8
- Only available on Smartfren
- EG25-G fully compatible

**Fallback:** Band 1 (2100 MHz) WCDMA (3G)
- Being phased out, not recommended for primary
- Limited availability
- EG25-G supports for temporary fallback

**Recommendation:** Telkomsel strongly recommended due to 98% coverage and Band 8 deployment.

---

## 6. Certification and Regulatory Compliance

### 6.1 EG25-G Global Certifications

The Quectel EG25-G has obtained extensive international certifications:

#### Global Standards
- **GCF** (Global Certification Forum) - Global carrier interoperability
- **PTCRB** (PCS Type Certification Review Board) - North American carrier certification

#### Regional Certifications

**Europe:**
- **CE** (Conformité Européenne) - European Union

**North America:**
- **FCC** (Federal Communications Commission) - United States
- **IC** (Innovation, Science and Economic Development Canada) - Canada

**Latin America:**
- **Anatel** - Brazil
- **IFETEL** - Mexico

**Asia-Pacific:**
- **SRRC** (State Radio Regulation of China) - China
- **NAL** (Network Access License) - China
- **CCC** (China Compulsory Certificate) - China
- **KC** (Korea Certification) - South Korea
- **NCC** (National Communications Commission) - Taiwan
- **JATE/TELEC** - Japan
- **RCM** (Regulatory Compliance Mark) - Australia/New Zealand
- **NBTC** - Thailand
- **IMDA** (Info-communications Media Development Authority) - Singapore

**Africa:**
- **ICASA** (Independent Communications Authority of South Africa) - South Africa

### 6.2 Indonesian Certification Requirements

#### DJID (Directorate General of Digital Infrastructure) Certification
Formerly known as SDPPI (Directorate General of Post and Telecommunications Resources and Equipment).

**Mandatory For:**
- All wireless and telecommunications products entering Indonesian market
- Devices using: Bluetooth, WLAN, NFC/SRD, GSM, WCDMA, LTE, 5G, etc.
- IoT devices, smartphones, laptops, wireless routers, modems

**Purpose:**
- Ensure device compatibility with Indonesian networks
- Prevent interference with other wireless systems
- Consumer protection and safety

**Recent Changes:**
- As of January 20, 2025, all certification logos and codes were updated
- Testing requirements include:
  - **RF Testing:** For all transmitting devices (LTE, GSM, WLAN, Bluetooth)
  - **EMC Testing:** Electromagnetic Compatibility mandatory for all devices

**EG25-G Status:**
- No specific Indonesian DJID/SDPPI certification found in documentation
- Regional certifications include Thailand (NBTC), Singapore (IMDA), but not Indonesia specifically

**Recommendation:**
1. **For Commercial Deployment:** Verify DJID/SDPPI certification status directly with Quectel
2. **If Not Certified:** May need to obtain certification through local testing laboratory
3. **For Pilot/Research:** May be acceptable without certification depending on use case
4. **Consult:** Local regulatory expert or Indonesian distributor for specific requirements

### 6.3 Carrier Certifications

The EG25-G has carrier approvals from:

**North America:**
- Verizon
- AT&T
- T-Mobile
- Sprint
- U.S. Cellular
- Telus (Canada)
- Rogers (Canada)

**Europe:**
- Deutsche Telekom

**Indonesia:**
- No specific Indonesian carrier certifications documented
- Global variant should work on GSM/LTE networks without carrier-specific approval
- Carrier testing recommended before large-scale deployment

---

## 7. Deployment Recommendations

### 7.1 Recommended Configuration for Indonesia

#### Primary Carrier: Telkomsel
**Rationale:**
- Best coverage: 98% of Indonesia including outer islands
- Supports all three key LTE bands (B3, B8, B40)
- Active in all provinces
- Most reliable for rural deployments

**Expected Performance:**
- Urban areas: 50-100 Mbps typical, up to 150 Mbps peak
- Suburban areas: 20-50 Mbps typical
- Rural areas: 5-20 Mbps typical (via Band 8)
- Remote areas: 1-5 Mbps (Band 8 or 3G fallback if available)

#### Alternative Carriers (in priority order):

**2. Indosat Ooredoo Hutchison (IOH)**
- Good urban coverage (70%+ population)
- Supports B1, B3, B8
- Cost-effective alternative
- Acceptable for urban/suburban deployments
- Limited rural coverage

**3. XL Axiata**
- Good urban and suburban coverage
- Supports B3, B8
- Similar to Indosat for urban deployments
- Moderate rural coverage

**4. Smartfren**
- Specialized carrier with unique bands (B5, B40)
- Good urban coverage
- High data rates in coverage areas
- Limited rural coverage
- Consider for urban-only or high-bandwidth applications

### 7.2 Band Priority Configuration

Configure the EG25-G with the following band priority for Indonesian deployment:

#### For Maximum Coverage (Telkomsel):
1. **Band 8 (900 MHz)** - Best coverage and penetration
2. **Band 3 (1800 MHz)** - Primary capacity band
3. **Band 40 (2300 MHz)** - Urban high-capacity
4. **Band 1 (2100 MHz)** - WCDMA fallback (if 3G still available)

#### For Urban High-Performance (Telkomsel or Smartfren):
1. **Band 40 (2300 MHz)** - Maximum throughput
2. **Band 3 (1800 MHz)** - Primary band
3. **Band 8/5 (900/850 MHz)** - Coverage fallback

#### For Multi-Carrier Compatibility:
1. **Band 3 (1800 MHz)** - Universal across all carriers
2. **Band 8 (900 MHz)** - Coverage on Telkomsel, Indosat, XL
3. **Band 1 (2100 MHz)** - Indosat/Tri support
4. **Band 40 (2300 MHz)** - Telkomsel/Smartfren capacity
5. **Band 5 (850 MHz)** - Smartfren compatibility

### 7.3 Testing and Validation Plan

Before full deployment, conduct testing in the following phases:

#### Phase 1: Laboratory Testing
- Verify EG25-G firmware version and band support
- Configure APN settings for target carrier(s)
- Test basic connectivity and data transfer
- Verify GNSS functionality

#### Phase 2: Field Testing - Urban
- Test in major cities (Jakarta, Surabaya, Bandung, Medan)
- Measure data rates on each supported band
- Test handoff between bands
- Verify stability over 24-48 hours

#### Phase 3: Field Testing - Rural
- Test in rural deployment areas
- Verify Band 8 (900 MHz) connectivity
- Test edge-of-coverage scenarios
- Measure signal strength (RSRP, RSRQ, SINR)

#### Phase 4: Extended Reliability Testing
- 7-day continuous operation test
- Monitor reconnection after signal loss
- Test power cycling and recovery
- Verify data integrity and throughput stability

#### Phase 5: Multi-Site Validation
- Deploy to 3-5 representative sites
- Monitor for 30 days
- Collect performance metrics
- Validate against requirements

### 7.4 Troubleshooting and Optimization

#### Signal Strength Targets
- **RSRP** (Reference Signal Received Power):
  - Excellent: > -80 dBm
  - Good: -80 to -90 dBm
  - Fair: -90 to -100 dBm
  - Poor: < -100 dBm

- **RSRQ** (Reference Signal Received Quality):
  - Excellent: > -10 dB
  - Good: -10 to -15 dB
  - Fair: -15 to -20 dB
  - Poor: < -20 dB

- **SINR** (Signal to Interference plus Noise Ratio):
  - Excellent: > 20 dB
  - Good: 13 to 20 dB
  - Fair: 0 to 13 dB
  - Poor: < 0 dB

#### Common Issues and Solutions

**Issue: Poor rural coverage**
- **Solution:** Ensure Band 8 (900 MHz) is enabled and prioritized
- **Carrier:** Switch to Telkomsel if using other carrier
- **Antenna:** Consider external antenna for improved gain

**Issue: Slow data rates**
- **Solution:** Check if device is on Band 40 (TDD) in urban areas for maximum speed
- **Band:** Verify Band 3 (1800 MHz) connectivity for good throughput
- **Carrier:** Telkomsel provides best balance of coverage and speed

**Issue: Frequent disconnections**
- **Solution:** Check for band reselection thrashing
- **Configuration:** Set appropriate band priorities
- **Signal:** Ensure RSRP > -100 dBm for stable connection

**Issue: No connectivity**
- **Solution:** Verify APN settings for chosen carrier
- **SIM:** Ensure SIM is activated and has data plan
- **Bands:** Check that required bands are enabled in firmware

---

## 8. Conclusions and Final Recommendations

### 8.1 Summary of Findings

The Quectel EG25-G LTE modem demonstrates **excellent compatibility** with Indonesian cellular networks:

1. **Band Support:** The EG25-G supports all primary LTE bands used in Indonesia:
   - Band 1 (2100 MHz) - ✅ Supported
   - Band 3 (1800 MHz) - ✅ Supported
   - Band 5 (850 MHz) - ✅ Supported
   - Band 8 (900 MHz) - ✅ Supported
   - Band 40 (2300 MHz TDD) - ✅ Supported

2. **Carrier Compatibility:** Full compatibility with all five target carriers:
   - ✅ Telkomsel - All bands (B3, B8, B40)
   - ✅ Indosat Ooredoo Hutchison - All bands (B1, B3, B8)
   - ✅ XL Axiata - All bands (B3, B8)
   - ✅ Tri (now IOH) - All bands (B1, B3)
   - ✅ Smartfren - All bands (B5, B40)

3. **Coverage Scenarios:**
   - ✅ Urban deployments - Excellent (Band 3, 40 support)
   - ✅ Suburban deployments - Excellent (Band 3, 8 support)
   - ✅ Rural deployments - Very Good (Band 8 support)
   - ⚠️ Remote areas - Good with Telkomsel (Band 8 + legacy 3G)

4. **Fallback Options:**
   - ✅ 3G/WCDMA Band 1 supported (though being phased out)
   - ✅ 2G/GSM supported (emergency only, being decommissioned)

5. **Global Variant Benefits:**
   - Single SKU for worldwide deployment
   - No need for region-specific models
   - Simplified inventory and logistics

### 8.2 Final Recommendation

**The Quectel EG25-G is FULLY SUITABLE for deployment in Indonesia.**

**Primary Recommendation:**
- **Use Telkomsel as the primary carrier** for maximum coverage and reliability
- The EG25-G supports all Telkomsel bands (B3, B8, B40)
- Expect excellent performance in urban, suburban, and rural areas
- 98% population coverage ensures connectivity nationwide

**Alternative Options:**
- Indosat Ooredoo Hutchison or XL Axiata for urban/suburban deployments
- Smartfren for high-bandwidth urban applications
- All carriers fully supported by EG25-G hardware

**Critical Action Items:**

1. **Certification Verification:**
   - ✅ Verify DJID/SDPPI certification status with Quectel before commercial deployment
   - ✅ Contact Indonesian distributor or regulatory expert if certification is required
   - ✅ Consider certification process timeline (may take 2-4 months)

2. **Pre-Deployment Testing:**
   - ✅ Conduct field testing in target deployment areas
   - ✅ Test with Telkomsel SIM in urban and rural locations
   - ✅ Validate data rates and stability over extended period
   - ✅ Verify GNSS functionality for location services

3. **Procurement:**
   - ✅ Order EG25-G modules (confirm "-G" Global variant)
   - ✅ Obtain Telkomsel SIM cards with appropriate data plans
   - ✅ Consider external antennas for rural installations

4. **Configuration:**
   - ✅ Configure band priority: B8 > B3 > B40 > B1 for maximum coverage
   - ✅ Set Telkomsel APN settings
   - ✅ Enable all Indonesian LTE bands (B1, B3, B5, B8, B40)
   - ✅ Test automatic fallback to 3G if needed

### 8.3 Risk Assessment

**Low Risk:**
- ✅ Hardware compatibility - All required bands supported
- ✅ Carrier availability - Multiple carrier options
- ✅ Technology maturity - LTE Cat 4 proven, widely deployed
- ✅ Form factor - Compact LGA module suitable for embedded designs

**Medium Risk:**
- ⚠️ Indonesian certification - DJID/SDPPI status unclear, may need verification
- ⚠️ 3G sunset - Limited fallback in some areas as 3G is phased out
- ⚠️ Rural coverage - Dependent on carrier selection (Telkomsel recommended)

**Mitigation Strategies:**
1. **Certification:** Engage with Quectel or local distributor early to verify/obtain certification
2. **3G Sunset:** Rely primarily on LTE bands; 3G fallback should not be primary strategy
3. **Rural Coverage:** Use Telkomsel and ensure Band 8 support is enabled
4. **Testing:** Comprehensive field testing before mass deployment

### 8.4 Next Steps

**Immediate Actions:**
1. Contact Quectel to verify Indonesian DJID/SDPPI certification status
2. Procure 1-2 EG25-G modules for evaluation
3. Obtain Telkomsel test SIM cards with data plans
4. Conduct laboratory testing of connectivity

**Short-term (1-2 months):**
1. Field testing in target deployment areas (urban and rural)
2. Validate data rates and stability
3. Test GNSS functionality
4. Document performance metrics

**Medium-term (2-4 months):**
1. Complete any required certification processes
2. Pilot deployment at 3-5 representative sites
3. 30-day monitoring and validation
4. Finalize carrier selection and data plans

**Long-term (4+ months):**
1. Full-scale deployment
2. Ongoing monitoring and optimization
3. Document lessons learned
4. Consider redundancy/failover strategies if needed

---

## 9. Supporting Data and References

### 9.1 Indonesian Band Allocation Summary

| Frequency | Band | Type | Status | Primary Users |
|-----------|------|------|--------|---------------|
| 700 MHz | B28 | LTE-FDD | Allocated | Not actively used |
| 850 MHz | B5 | LTE-FDD | Active | Smartfren |
| 900 MHz | B8 | LTE-FDD / GSM | Active | Telkomsel, Indosat, XL |
| 1800 MHz | B3 | LTE-FDD / GSM | Active | All major carriers |
| 2100 MHz | B1 | LTE-FDD / WCDMA | Active/Phasing | Indosat, Tri, Some 3G |
| 2300 MHz | B40 | LTE-TDD | Active | Telkomsel, Smartfren |
| 2600 MHz | B7, B38 | LTE-FDD/TDD | Limited | Limited deployment |

### 9.2 Quectel EG25-G Specifications Summary

| Parameter | Specification |
|-----------|---------------|
| **Form Factor** | LGA 29.0mm × 32.0mm × 2.4mm |
| **Weight** | 4.9g |
| **Supply Voltage** | 3.3-4.3V (3.8V typical) |
| **LTE Category** | Cat 4 |
| **3GPP Release** | Release 11 |
| **Max DL/UL (FDD)** | 150 Mbps / 50 Mbps |
| **Max DL/UL (TDD)** | 130 Mbps / 30 Mbps |
| **LTE-FDD Bands** | B1/2/3/4/5/7/8/12/13/18/19/20/25/26/28 |
| **LTE-TDD Bands** | B38/39/40/41 |
| **WCDMA Bands** | B1/2/4/5/6/8/19 |
| **GSM Bands** | B2/3/5/8 |
| **GNSS** | GPS, GLONASS, BeiDou, Galileo, QZSS |

### 9.3 Key Technical Terms

- **LTE-FDD (Frequency Division Duplex):** LTE mode using separate frequencies for uplink and downlink
- **LTE-TDD (Time Division Duplex):** LTE mode using same frequency, time-separated for uplink and downlink
- **WCDMA (Wideband Code Division Multiple Access):** 3G technology (UMTS/HSPA)
- **GSM (Global System for Mobile Communications):** 2G technology
- **Band:** Specific frequency range allocated for cellular communications
- **RSRP (Reference Signal Received Power):** LTE signal strength measurement
- **RSRQ (Reference Signal Received Quality):** LTE signal quality measurement
- **SINR (Signal to Interference plus Noise Ratio):** Signal quality metric
- **APN (Access Point Name):** Gateway between mobile network and internet
- **Cat 4 (Category 4):** LTE device category with 150 Mbps DL / 50 Mbps UL capability

### 9.4 Useful AT Commands for EG25-G

```
AT+QCFG="band"                    // Query available bands
AT+QCFG="nwscanmode",0            // Set to automatic mode (LTE/WCDMA/GSM)
AT+QCFG="nwscanseq",020301        // Set scan sequence (LTE > WCDMA > GSM)
AT+COPS?                          // Query network operator
AT+CSQ                            // Query signal strength
AT+QCSQ                           // Query detailed signal quality
AT+QENG="servingcell"             // Query serving cell information
AT+CGDCONT?                       // Query APN settings
```

---

## 10. Sources and References

### 10.1 Quectel EG25-G Documentation

1. [Quectel EG25-G Product Page](https://www.quectel.com/product/lte-eg25-g/)
2. [EG25-G Specifications - EverythingRF](https://www.everythingrf.com/products/cellular-modules/quectel/811-439-eg25-g)
3. [Quectel EG25-G Standard Specification V1.6 (PDF)](https://quectel.com/content/uploads/2024/03/Quectel_EG25-G_LTE_Standard_Specification_V1.6-1-1.pdf?wpId=114158)
4. [Quectel EG25-G Mini PCIe Specification (Sixfab)](https://sixfab.com/wp-content/uploads/2022/02/Quectel_EG25-G_Mini_PCIe_LTE_Standard_Specification_V1.4.pdf)
5. [M2M Support - EG25-G Bands and Technologies](https://m2msupport.net/m2msupport/quectel-wireless-eg25-g-supported-bands-and-technologies/)
6. [Quectel LTE Standard Module Product Overview](https://forums.quectel.com/uploads/short-url/oISfjXkd5Y4njqUrrfHd3WYpaol.pdf)
7. [Waveshare EG25-G mPCIe Module](https://www.waveshare.com/eg25-g-mpcie.htm)

### 10.2 Indonesian Cellular Network Information

8. [Indonesia Wireless Frequency Bands and Carriers - FrequencyCheck](https://www.frequencycheck.com/countries/indonesia)
9. [Telkomsel Frequency Bands - FrequencyCheck](https://www.frequencycheck.com/carriers/telkomsel-indonesia)
10. [Telkomsel Spectrum Information - Spectrum Tracker](https://www.spectrum-tracker.com/Indonesia/Telkomsel)
11. [Indonesia Spectrum Overview - Spectrum Tracker](https://www.spectrum-tracker.com/Indonesia)
12. [Indosat Frequency Bands - FrequencyCheck](https://www.frequencycheck.com/carriers/indosat-indonesia)
13. [XL Axiata Frequency Bands - FrequencyCheck](https://www.frequencycheck.com/carriers/xl-axiata-indonesia)
14. [XL Axiata Spectrum Information - Spectrum Tracker](https://www.spectrum-tracker.com/Indonesia/XL-Axiata)
15. [Tri (3) Frequency Bands - FrequencyCheck](https://www.frequencycheck.com/carriers/3-tri-indonesia)
16. [Smartfren Frequency Bands - FrequencyCheck](https://www.frequencycheck.com/carriers/smartfren-indonesia)
17. [Indonesia 4G Bands Overview - MidTeknologi](https://midteknologi.com/blog/band-4g-di-indonesia/)
18. [Operator Watch: Indonesia Consolidating 4G](https://www.operatorwatch.com/2020/06/indonesia-consolidating-4g.html)
19. [Indonesia Prepaid Data SIM Wiki](https://prepaid-data-sim-card.fandom.com/wiki/Indonesia)
20. [Telkomsel 4G LTE 2.3 GHz TDD Frequency Announcement](https://www.telkomsel.com/en/about-us/news/telkomsel-strengthens-4g-lte-service-using-23-ghz-tdd-frequency)
21. [Will My Phone Work in Indonesia - Kimovil Band Checker](https://www.kimovil.com/en/frequency-checker/ID)

### 10.3 Certification and Regulatory Information

22. [EG25-G Certifications Discussion - Quectel Forums](https://forums.quectel.com/t/eg25-g-certifications/44338)
23. [Compliance Testing for EG25-G - Quectel Forums](https://forums.quectel.com/t/compliance-test-for-eg25-g-mini-pcie-modules/4748)
24. [Indonesian Certification Guide - JJR Lab](https://www.jjrlab.com/news/indonesian-certification-guide-for-electrical-products.html)
25. [Ericsson Marketplace - Quectel EG25-G](https://www.ericsson.com/en/partners/marketplace/offering-catalog/quectel-eg25-g)

---

## Document Information

**Prepared by:** OpenRiverCam Research Team
**Date:** January 9, 2026
**Document Version:** 1.0
**Status:** Final
**Distribution:** Internal - Spring 2026 Indonesia Deployment Team

**Revision History:**
- v1.0 (2026-01-09): Initial comprehensive research report

**For Questions or Updates:**
Contact OpenRiverCam technical team or refer to latest documentation in project repository.

---

*End of Report*
