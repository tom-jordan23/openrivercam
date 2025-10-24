# PPP_TRANSLATION.md
PPP Translation — UTM‑Everywhere Guide (EPSG:32748)

**Goal**  
Align your RTK survey (cm‑level relative) to a precise global position by applying a **UTM‑meter translation** from the PPP‑refined base. Expect ~0.25–0.5 m absolute alignment to imagery, while preserving internal geometry.

**Project CRS:** UTM Zone 48 South (**EPSG:32748**) • **Heights:** Ellipsoidal (m)

---

## 0) Inputs & assumptions
- **Survey points** are or will be saved as **EPSG:32748** layers (meters).  
- **Field base** coordinate from 5‑min survey‑in (`Lat_field, Lon_field, Z_field`) — may start as lat/lon.  
- **PPP base** coordinate from 6–12 h PPP (`Lat_ppp, Lon_ppp, Z_ppp` ellipsoidal).  
- Field attributes include `pole_h_m` (tip→ARP), optional `Z_ellipsoid` attribute (or Z is in geometry).

**Why UTM:** We compute and apply translations in **meters** to avoid degree/meter confusion. Only reproject lat/lon inputs *once* into EPSG:32748 before calculating deltas.

---

## 1) Build base points in UTM (What & Why)
**What:** Create two point layers: `FieldBase_UTM` and `PPPBase_UTM`, both in **EPSG:32748**.  
**Why:** You need both bases in the **same projected CRS** to compute a clean meter translation.

Steps
1. If your base coordinates are in lat/lon, **Add Delimited Text** (WGS84) then **Save As → EPSG:32748**.  
2. Name the layers: `FieldBase_UTM` and `PPPBase_UTM`.  
3. Use **Identify** (or `$x`, `$y`) to read **Easting (E)** and **Northing (N)**; note **Z**.

---

## 2) Compute the translation (ΔE, ΔN, ΔZ)
**What:** Compute **PPP − Field** in meters.  
**Why:** This 3‑value vector moves your entire survey into the precise PPP frame.

Formulas
- **ΔE = E_ppp − E_field**  
- **ΔN = N_ppp − N_field**  
- **ΔZ = Z_ppp − Z_field**

Record the three numbers.

---

## 3) Translate the survey (planar shift in meters)
**What:** Shift all survey points by ΔE/ΔN in **EPSG:32748** using **Translate (Move, shift)**.  
**Why:** Corrects absolute placement without changing shapes/slopes.

Steps
1. Ensure the survey layer is **EPSG:32748** (Save As if needed).  
2. **Vector ► Geoprocessing ► Translate (Move, shift)** → Input = survey layer → **Offset X = ΔE**, **Offset Y = ΔN** → Output `Survey_UTM_shifted`.

---

## 4) Apply vertical shift and compute bed_Z
**What:** Update altitude by ΔZ and subtract pole height to get **bed elevation**.  
**Why:** Antenna Z (ARP) must be reduced by **tip→ARP** to represent the **river bed**.

If Z is an attribute (e.g., `Z_ellipsoid`):  
```
Z_ellipsoid_shifted = "Z_ellipsoid" + <DeltaZ>
```

If Z is only in geometry:  
```
Z_ellipsoid_shifted = $z + <DeltaZ>
```

Then compute bed elevation:  
```
bed_Z = "Z_ellipsoid_shifted" - "pole_h_m"
```

*(If no PPP, skip ΔZ and use `"Z_ellipsoid" - "pole_h_m"` or `$z - "pole_h_m"`; vertical may be biased by a constant.)*

---

## 5) Validate & archive
- **Imagery overlay:** Expect **~0.25–0.5 m** visual agreement near hard edges.  
- **Relative precision:** CP START/NOON/END repeatability remains **≤ 2 cm H / ≤ 3–4 cm V**.  
- **Archive:** ΔE/ΔN/ΔZ, PPP report (frame/epoch), antenna ARP height, CRS (EPSG:32748), processing notes.

---

## Common pitfalls
- Translating in **degrees** instead of meters → always use **EPSG:32748**.  
- Using **Field − PPP** by mistake → must be **PPP − Field**.  
- Forgetting **ΔZ** → verticals off by a constant.  
- Mixing orthometric & ellipsoidal heights → keep ellipsoidal through translation; apply geoid later if needed.
