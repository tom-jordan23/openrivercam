# Outsourced Survey — Team Briefing and Provider Options

*Brief for the deployment team. Describes the fully-outsourced survey option for the ORC camera stations, with providers in Sukabumi and Jakarta, and a decision checklist.*

## 1. Objective

Hire a licensed survey firm to produce the complete survey dataset required by each ORC station, so that the local team does not need to repeat or refine the existing survey work. The vendor handles: ground control points (GCPs), river cross-section, staff gauge datum tie, and a written report. The vendor brings their own geodetic equipment.

## 2. What the Vendor Will Deliver

For each site, the vendor must provide:

1. **Ground control points (GCPs):** 6–10 points visible from the camera view, coordinates in UTM Zone 48S (SRGI2013), horizontal RMSE ≤ 3 cm, vertical RMSE ≤ 7 cm, RTK Fixed observations only (no Float).
2. **River cross-section:** distance–elevation pairs from bank to bank through the camera view, with chainage from a defined datum stake. Spacing 0.5–1.0 m across the channel, with additional points at any break in slope. Include wetted and dry portions.
3. **Staff gauge datum tie:** elevation of the staff gauge zero, referenced to the same coordinate system as the GCPs, with at least two independent checks.
4. **Permanent benchmark:** one concrete or rebar monument per site, in a stable location outside the flood footprint, with recorded coordinates. This lets future teams re-establish the datum if a GCP is lost.
5. **Written report** (laporan survei) in PDF including: equipment model and serial number, CORS stations used, observation durations and fix status per point, processing software, computed RMSE, field sketches of GCP and benchmark positions with descriptions.
6. **Data files:** point list as CSV (ID, Easting, Northing, Elevation, RMSE-H, RMSE-V, duration, fix status), raw RINEX logs if static observations were used, cross-section as CSV.

## 3. Provider Shortlist

All providers below cover Sukabumi regency. Prices are indicative for one site, one day of field work, all deliverables above, including PPN. Expect Rp 5,000,000–Rp 15,000,000 per site.

### Sukabumi and West Java

| Firm | Base | Contact | Notes |
|---|---|---|---|
| **CV Tata Bumi Geosurvey** | Sukabumi / West Java corridor | [tatabumigeosurvey.com](https://tatabumigeosurvey.com/) | Local to the region. 8+ years experience. RTK geodetic GPS, drone, total station. Shortest mobilization distance. |
| **Geopasi Survey** | Bandung | [geopasi.com](https://geopasi.com/jasa-survey-gps/) | Bandung–Sukabumi corridor explicitly served. Offers RTK, topographic, hydrographic, drone. Site contact form and LinkedIn. |
| **Geoindo Survey Services** | Bandung | [geoindo.com](http://www.geoindo.com/) — Phone +62-22-751-3168; Jl. Batununggal Indah IV No. 83 | Established firm (since 1994). Terrestrial, hydrographic, topographic, GPS control. |
| **DND Survey** | Bandung | [dndsurvey.id](https://dndsurvey.id/) | Multi-brand RTK. Also rents equipment if needed as backup. |
| **PT LAPI Ganeshatama Consulting (LAPI GTC)** | Bandung (ITB campus) | [lapiganeshatama.co.id](https://www.lapiganeshatama.co.id/) — Phone +62-22-250-7463; Jl. Ganesha No. 15-B | ITB's commercial consulting unit. Higher technical quality, longer approval timeline (2–4 weeks). Use if budget and schedule allow. |

### Jakarta

| Firm | Base | Contact | Notes |
|---|---|---|---|
| **TechnoGIS Indonesia** | Jakarta (Kebon Jeruk) | [technogis.co.id](https://www.technogis.co.id/contact/) — Phone +62-813-2552-3979; marketing@technogis.co.id | National coverage. GPS geodetic, topographic, UAV. WhatsApp on site number. |
| **Geo Survey Persada Indonesia (GSPI)** | Jakarta | [geosurveypersada.com](https://geosurveypersada.com/contact-us) | National firm. Terrestrial, LiDAR, drone, hydrographic. Good for multi-site coordination. |
| **MSDI** | Jakarta | [msdi.co.id](https://www.msdi.co.id/) | Rents Emlid Reach RS2/RS2+ and Trimble. Also provides survey services. Useful backup. |
| **CV ADHIJASA** | Jakarta / Bandung | [adhijasa.com](https://adhijasa.com/rental-gps-rtk-gnss-geodetik/) | Sukabumi regency in their delivery area. Smaller firm, faster quote turnaround. |

## 4. Copy-Paste Scope of Work (Send via WhatsApp or Email)

Send to three firms at once. Ask for response within 48 hours. The Indonesian version is the one to send; the English version is for the team's internal reference.

### Indonesian (paste this to vendors)

> Selamat pagi. Kami membutuhkan jasa survei topografi untuk [jumlah] lokasi stasiun monitoring sungai di Kabupaten Sukabumi. Lingkup pekerjaan per lokasi:
>
> 1. Pengukuran 6–10 titik kontrol (GCP) menggunakan RTK GNSS multi-frekuensi dengan koreksi jaringan InaCORS BIG. Akurasi yang diminta: horizontal ≤ 3 cm RMSE, vertikal ≤ 7 cm RMSE, status Fixed (bukan Float).
> 2. Pengukuran penampang melintang sungai (cross-section) dari tebing ke tebing, jarak titik 0,5–1,0 m.
> 3. Pengikatan elevasi nol papan duga (staff gauge) ke sistem koordinat yang sama, dengan minimal dua verifikasi independen.
> 4. Pemasangan satu benchmark permanen (beton atau besi) per lokasi, di luar area banjir.
> 5. Output: daftar koordinat (CSV), data mentah RINEX, CSV cross-section, dan laporan survei PDF lengkap dengan model dan nomor seri alat, stasiun CORS yang digunakan, dan RMSE per titik.
>
> Sistem referensi: SRGI2013, koordinat output UTM Zone 48S.
>
> Mohon penawaran harga termasuk PPN, waktu mobilisasi tercepat, dan durasi total hingga pengiriman laporan. Kami membutuhkan respon dalam 48 jam. Terima kasih.

### English (team reference)

> We need topographic survey services for [number] river monitoring station sites in Sukabumi regency. Per-site scope:
>
> 1. 6–10 GCPs by multi-frequency RTK GNSS with InaCORS BIG network corrections. Required accuracy: ≤ 3 cm horizontal RMSE, ≤ 7 cm vertical RMSE, Fixed status only (no Float).
> 2. River cross-section from bank to bank, 0.5–1.0 m point spacing.
> 3. Staff gauge zero elevation tied to the same coordinate system, with at least two independent checks.
> 4. One permanent benchmark (concrete or rebar) per site, outside the flood footprint.
> 5. Deliverables: coordinate list (CSV), raw RINEX, cross-section CSV, and PDF survey report including equipment model and serial, CORS stations used, and per-point RMSE.
>
> Reference system: SRGI2013, output coordinates UTM Zone 48S.
>
> Please respond with total price including PPN, earliest mobilization date, and total duration to report delivery. 48-hour response requested.

## 5. Quote Evaluation Checklist

When comparing the three quotes, check each item below. A missing or vague answer is a red flag — ask for clarification before signing.

- [ ] Price is **inclusive of PPN 11%**, or the quote states clearly "belum termasuk PPN" with the PPN amount shown.
- [ ] Equipment **model and serial number** are named. Acceptable: Emlid Reach RS2/RS2+, Trimble R series, Leica GS series, Hi-Target V series, Topcon HiPer. Not acceptable: generic "GPS Geodetic" with no model.
- [ ] The quote states **RTK Fixed** observations, not generic "centimeter accuracy." Float observations must be excluded or re-measured.
- [ ] **InaCORS BIG** network corrections are named, or a post-processed baseline from an InaCORS station is specified.
- [ ] Output coordinate system is **UTM Zone 48S, SRGI2013**. Any deviation must be justified.
- [ ] **Raw RINEX files** are included in deliverables (not only processed coordinates).
- [ ] **Mobilization date** and **report delivery date** are both specified.
- [ ] Payment terms: typical is 30–50% DP on SPK, remainder on report delivery. Avoid quotes asking for 100% up front.
- [ ] Consider adding a **denda keterlambatan** clause (1% per working day past the deadline).

## 6. Red Flags to Watch For

- Quote under Rp 3,000,000 per day all-in — equipment is probably not multi-band geodetic grade.
- Vendor cannot name the RTK equipment they will use.
- Vendor says "tidak perlu CORS" (no CORS needed) without explaining how they will achieve centimeter accuracy.
- Vendor refuses to provide raw RINEX files.
- Vendor offers only handheld-GPS output (no RMSE values reported).
- Deliverable format is vague — no CSV, no report structure described.

## 7. What the Field Team Needs to Do on Survey Day

Surveyors will work faster and produce a better result if the local team prepares before the visit:

- **Confirm site access** with landowner and village head (kepala desa). Provide the surveyor with contact names.
- **Mark the camera view** with painted stakes or flagging tape at the approximate corners of what the camera sees, so the surveyor can place GCPs where they will be visible in the image.
- **Have the staff gauge already installed** at final location before the survey. The surveyor cannot tie the datum to a gauge that will later move.
- **Provide a preferred benchmark location:** stable ground, outside the flood footprint, visible from at least two GCPs.
- **Be on site** during the survey. The surveyor's RMSE numbers are only meaningful if the right points were measured — the team should confirm each GCP is a point the camera can actually see.

## 8. Acceptance Checklist (When the Report Arrives)

Before paying the final invoice, verify:

- [ ] Coordinate list CSV is present and opens in QGIS without errors.
- [ ] All GCPs have RMSE horizontal ≤ 3 cm, vertical ≤ 7 cm. Any that do not must be re-measured or removed.
- [ ] All GCPs have fix status **Fixed**. Any Float must be re-measured.
- [ ] Staff gauge zero elevation is stated and matches one of the GCP elevations within expected difference for the physical layout.
- [ ] Benchmark coordinates and physical description are provided.
- [ ] Raw RINEX files are present for at least the benchmark observation.
- [ ] Cross-section CSV plots as a plausible channel shape (use pyorc's cross-section viewer or QGIS profile tool).
- [ ] PDF report includes equipment serial numbers, CORS stations used, and processing software version.

If all items pass, authorize termin 2 (remaining payment). If any item fails, hold payment and request the specific correction in writing.

## 9. Budget Summary

| Scenario | Per-site cost (IDR, incl. PPN) | Notes |
|---|---|---|
| Sukabumi-local firm, single site | 5,000,000 – 8,000,000 | Shortest mobilization |
| Bandung firm, single site | 6,000,000 – 12,000,000 | Wider firm selection |
| Jakarta firm, single site | 8,000,000 – 15,000,000 | Higher mobilization cost; consider bundling multiple sites |
| Multi-site discount | –10% to –20% | Ask for this explicitly if more than one site is visited in one mobilization |
| ITB / LAPI GTC | 10,000,000 – 15,000,000 | Premium option; longer timeline |

## 10. Recommended Vendors

Send the SOW (Section 4) to the following three firms in parallel. Ask each for a 48-hour response. These three are chosen to give a range of price and speed while all being capable of meeting the Section 5 checklist.

**Primary: Geopasi Survey (Bandung).** This is the recommended first choice. Geopasi explicitly offers hydrographic survey as a core service, which matches the river-focused nature of the ORC work better than firms that only do topographic survey. Bandung base gives a short mobilization distance to Sukabumi (approximately 90 km). Mid-size firm, lower risk than a single-operator freelance.

**Backup: Geoindo Survey Services (Bandung).** Use as the fallback if Geopasi does not respond within 48 hours or quotes outside the budget range. Geoindo has been operating since 1994, has a published phone number (+62-22-751-3168) for immediate contact, and covers GPS control surveys as a standard service.

**Price comparator: CV Tata Bumi Geosurvey (Sukabumi-local).** Include this firm to test whether a Sukabumi-based vendor can produce a materially cheaper quote thanks to zero mobilization distance. If their quote passes the checklist in Section 5 and is significantly lower than Geopasi's, this becomes the practical choice.

**Final selection rule:** Choose whichever of the three quotes arrives first that (a) passes every item in the Section 5 checklist and (b) fits the Section 9 budget range. If two quotes both pass, choose the lower-priced one. Do not wait for the third quote if the first two both pass — time in-country is the binding constraint.

**Do not use for this job:**
- LAPI GTC (ITB) — highest technical quality but the 2–4 week approval timeline does not fit the current deployment window. Keep as a future option if a larger multi-site project is planned.
- Jakarta firms (TechnoGIS, GSPI) — mobilization cost to Sukabumi is materially higher than Bandung firms for the same quality. Only use if the Bandung shortlist all fail to respond.

## 11. Contact Summary for Quick Reference

| Firm | Phone / WhatsApp | Email or Web Form |
|---|---|---|
| CV Tata Bumi Geosurvey | Via [tatabumigeosurvey.com](https://tatabumigeosurvey.com/) | Site contact form |
| Geopasi Survey | Via [geopasi.com](https://geopasi.com/jasa-survey-gps/) | Site contact form |
| Geoindo Survey Services | +62-22-751-3168 | Via [geoindo.com](http://www.geoindo.com/) |
| DND Survey | Via [dndsurvey.id](https://dndsurvey.id/) | Site contact form |
| LAPI GTC | +62-22-250-7463 | Via [lapiganeshatama.co.id](https://www.lapiganeshatama.co.id/) |
| TechnoGIS Indonesia | +62-813-2552-3979 | marketing@technogis.co.id |
| GSPI | Via [geosurveypersada.com](https://geosurveypersada.com/contact-us) | Site contact form |
| MSDI | Via [msdi.co.id](https://www.msdi.co.id/) | Site contact form |
| CV ADHIJASA | Via [adhijasa.com](https://adhijasa.com/) | Site contact form |
