# InaCORS NTRIP HOWTO

This companion guide provides step-by-step instructions for registering with the InaCORS (Indonesia Continuously Operating Reference Station) service and configuring NTRIP corrections in GNSS Master and SW Maps. InaCORS provides a free alternative to operating your own RTK base station, streaming real-time corrections over a mobile data connection.

This guide is relevant when surveying at sites within Indonesia where InaCORS coverage is available. For sites outside Indonesia, or where mobile data coverage is insufficient, refer to the base station procedures in Section 9.4 and 9.5.

---

## What is InaCORS?

InaCORS is Indonesia's national network of Continuously Operating Reference Stations, operated by **Badan Informasi Geospasial (BIG)** — the national geospatial information agency. The network consists of approximately 397 permanent GNSS stations distributed throughout Indonesia, forming the physical infrastructure of the **Sistem Referensi Geospasial Indonesia (SRGI)**.

InaCORS provides three services:

| Service | Description |
|---|---|
| **RTK-NTRIP** | Real-time corrections streamed over internet (this guide) |
| **RINEX Data** | Raw observation data for post-processing download |
| **Online Post-Processing** | Upload raw GNSS data to BIG's server for computed coordinates |

When using the RTK-NTRIP service, your rover receiver connects to the InaCORS caster via mobile data and receives RTCM3 correction streams. This eliminates the need to set up a local base station, provided you are within reasonable distance of an InaCORS reference station.

### Coverage

- **Java and Bali:** Fully covered. Fast RTK Fix times, excellent accuracy.
- **Sumatra:** Near-complete coverage.
- **Kalimantan, Sulawesi, Papua, Maluku:** Coverage is sparser with greater inter-station distances. RTK Fix may be difficult to achieve in remote areas.

Average inter-station spacing is approximately 50 km, though this varies significantly by region. Use the SRGI service check page (`https://srgi.big.go.id/page/service-check`) or the Mobile InaCORS app (Google Play: `bignrtk.bignrtk`) to verify station availability near your survey site before field deployment.

### When to Use InaCORS vs. Your Own Base Station

Use InaCORS when:
- You are surveying in Java, Bali, or Sumatra where station density is high
- You have reliable mobile data coverage at the survey site
- You want to reduce equipment logistics (no base station tripod, no base receiver)

Use your own base station when:
- The nearest InaCORS station is more than 30-50 km away
- Mobile data coverage is unreliable at the survey site
- You need guaranteed correction availability independent of external services

---

## Step 1: Register for an InaCORS Account

### 1.1 Create Your Account

1. Open a browser and navigate to the registration page:
   `http://nrtk.big.go.id/sbc/Account/Register`

   > **Note:** The portal uses HTTP, not HTTPS. Some browsers may warn about this. Allow the connection to proceed.

2. Complete the registration form. Typical fields include:
   - Username
   - Email address
   - Password
   - Full name
   - Organization / company name
   - Country

   > **Note:** The interface is in Bahasa Indonesia. The service does not appear to restrict registration to Indonesian citizens, but expect the entire portal to be in Indonesian.

3. Submit the form.

### 1.2 Activate Your Account

1. Check the email address you registered with for an activation email from BIG.
2. Click the activation link in the email. Without activation, you cannot log in.

### 1.3 Subscribe to the NTRIP Service

This step is critical. Your username and password will not work for NTRIP connections until you complete this subscription.

1. Log in to the SBC portal: `http://nrtk.big.go.id/sbc/`
2. Navigate to the **Shop** menu.
3. Find the product **"Network RTK -- Unlimited"**.
4. Click **"Buy Now"** (the service is free of charge).
5. Tick the Terms of Use checkbox.
6. Click **"Subscribe Now"**.

### 1.4 Verify Your Connection Details

1. In the SBC portal, navigate to **Account Detail -> User Profile -> Preferences**.
2. Note the NTRIP caster IP address and port displayed. These should match the values in the quick reference below but always verify against what the portal shows.

---

## Step 2: NTRIP Connection Details

After registration and subscription, use these connection parameters:

| Parameter | Value |
|---|---|
| **Host** | `103.22.171.6` |
| **Port** | `2001` |
| **Username** | Your SBC username |
| **Password** | Your SBC password |
| **Format** | RTCM3 |
| **Send NMEA GGA** | Yes (required for VRS/network mountpoints) |

### Mountpoint Selection

InaCORS offers four mountpoint types:

| Mountpoint | Type | Use Where |
|---|---|---|
| `VRS` | Virtual Reference Station | Java, Bali, Sumatra (recommended) |
| `max` | Master-Auxiliary Corrections | Java, Bali, Sumatra |
| `imax` | Individual Master-Auxiliary | Java, Bali, Sumatra |
| `nearest` | Single nearest station | Kalimantan, Sulawesi, Papua, or sparse coverage areas |

**Selection guidance:**

- In **Java, Bali, and Sumatra** (dense station coverage), use `VRS`. This network RTK method combines data from multiple nearby stations, providing better accuracy than any single station.
- In **other islands** where stations are more sparse, use `nearest`. This connects to the single geographically closest active station.
- `VRS`, `max`, and `imax` mountpoints all require your NTRIP client to transmit your current position (NMEA GGA sentence) back to the caster. Both GNSS Master and SW Maps support this.

> **Important:** Always verify the server address and port against the SBC portal's Account Preferences page. The values above are confirmed from InaCORS official sources but BIG may update them.

---

## Step 3: Configure GNSS Master

GNSS Master acts as a bridge between your Bluetooth GNSS receiver and Android apps. It includes a built-in NTRIP client that receives corrections and forwards them to your connected receiver.

### Prerequisites

- Your GNSS/RTK receiver is paired over Bluetooth and GNSS Master is receiving positions from it.
- Your Android device has a working mobile data connection.
- You have completed InaCORS registration including the subscription step.

### Configuration Procedure

1. **Open the Corrections page** in GNSS Master's main interface.

2. **Set the Mode** to **NTRIP Client** from the Mode dropdown.

3. **Add a new NTRIP connection** by tapping the **+** (plus) button. This opens the NTRIP Client dialog.

4. **Enter the connection parameters:**

   | Field | Value |
   |---|---|
   | NTRIP Version | V2 (try V1 if V2 fails) |
   | Address / Host | `103.22.171.6` |
   | Port | `2001` |
   | Mountpoint | `VRS` or `nearest` (see selection guidance above) |
   | Username | Your InaCORS/SBC username |
   | Password | Your InaCORS/SBC password |

5. **Fetch mountpoint list** (recommended): Tap the button next to the mountpoint field to pull the live source table from the caster. This lets you select from available mountpoints rather than typing manually.

6. **Enable GGA transmission**: Confirm that GNSS Master is configured to send NMEA GGA sentences back to the caster. This is required for VRS and network mountpoints.

7. **Save and connect**: Tap Save, select the new profile from the connections list, and press Connect.

### Verify Corrections

Once connected, GNSS Master should show the NTRIP data stream as active with data bytes being received. Your receiver should progress through fix states:

- **Autonomous** -> **RTK Float** -> **RTK Fix**

RTK Fix typically takes 30-120 seconds with good sky visibility. In heavy ionospheric conditions (common near the equator), allow up to 3-5 minutes.

---

## Step 4: Configure SW Maps

SW Maps is the survey data collection app. If using GNSS Master as a bridge, corrections are already being forwarded to your receiver and SW Maps receives the corrected position. However, SW Maps also has its own built-in NTRIP client that you can use directly.

### Using SW Maps Built-in NTRIP Client

If you prefer to use SW Maps' own NTRIP client instead of GNSS Master's:

1. **Connect to your GNSS receiver** in SW Maps first:
   - Open the left navigation drawer (hamburger menu).
   - Tap **Bluetooth GNSS** (or **External GNSS**).
   - Select your paired receiver and set the instrument height.
   - Tap **CONNECT** and verify you are receiving positions.

2. **Open the NTRIP Client**:
   - From the left navigation drawer, select **NTRIP Client**.
   - The NTRIP Client menu may only appear after connecting to an external receiver.

3. **Enter the connection parameters:**

   | Field | Value |
   |---|---|
   | Host / Caster Address | `103.22.171.6` |
   | Port | `2001` |
   | Username | Your InaCORS/SBC username |
   | Password | Your InaCORS/SBC password |
   | Mountpoint | `VRS` or `nearest` |
   | Send NMEA GGA to Caster | **ON** |

4. **Connect**: Tap CONNECT. SW Maps will forward corrections to your receiver.

5. **Verify RTK Fix**: Open the **Skyplot** screen from the main menu. Watch for the fix status to progress from Autonomous to RTK Float to RTK Fix.

### Which NTRIP Client to Use?

You only need **one** NTRIP client active at a time. Do not run both GNSS Master's and SW Maps' NTRIP clients simultaneously.

- **GNSS Master NTRIP client**: Use when GNSS Master is your primary receiver bridge and you want corrections managed there.
- **SW Maps NTRIP client**: Use when connecting to the receiver directly through SW Maps without GNSS Master as an intermediary.

---

## Step 5: Verification and Validation

Before beginning survey data collection, perform these checks to confirm InaCORS corrections are working correctly and your position solution is trustworthy.

### 5.1 Confirm NTRIP Connection is Active

1. **Check data flow:** In whichever NTRIP client you are using (GNSS Master or SW Maps), verify that the connection status shows "Connected" and that data bytes received are incrementing. A connected status with zero or static byte count indicates the caster accepted your credentials but is not sending correction data — check your mountpoint selection and GGA transmission setting.

2. **Check correction age:** If your app displays correction age (also called "differential age"), confirm it is updating and stays below 10 seconds. A correction age that climbs steadily or exceeds 30 seconds indicates the data stream has stalled.

### 5.2 Confirm RTK Fix

1. **Check fix type:** In SW Maps, open the Skyplot screen. In GNSS Master, check the position status display. The fix type must read **RTK Fix** (not "Autonomous", "DGPS", or "RTK Float") before you begin collecting survey points.

2. **Check reported accuracy:** With RTK Fix, the horizontal accuracy estimate (HRMS or CEP) should be below 5 cm. If the display shows RTK Fix but reports accuracy worse than 10 cm, something is wrong — investigate before proceeding.

3. **Allow sufficient convergence time:** After first connecting, wait for RTK Fix to stabilise. Do not collect points during the first 30-60 seconds after achieving Fix, as the solution may still be converging. A stable Fix will show consistent coordinates with variations of only 1-2 cm.

### 5.3 Known Point Check

If you have access to a known control point, benchmark, or previously surveyed point at or near the site:

1. Place the rover on the known point.
2. Record the position reported by InaCORS-corrected RTK Fix.
3. Compare against the known coordinates. Agreement within 3-5 cm horizontally confirms the correction chain is functioning correctly.

If you do not have a known point available, at minimum:

1. Stand in one position with clear sky for 2 minutes after achieving RTK Fix.
2. Observe the coordinate stability. Easting and Northing should not wander by more than 2-3 cm. Elevation should not wander by more than 5 cm.
3. If coordinates are jumping by 10+ cm or the fix type is flickering between Float and Fix, do not proceed with survey data collection until the issue is resolved.

### 5.4 Cross-Check: Compare InaCORS vs. Base Station (Optional)

If this is your first time using InaCORS at a site and you want to build confidence in the service, you can run a comparison:

1. Set up your local base station and collect a few points using radio-link RTK corrections as normal (with NTRIP disconnected — see the warning in Step 6 below).
2. Disconnect the radio corrections, connect to InaCORS NTRIP, and re-measure the same points.
3. Compare the two sets of coordinates. Differences of 1-3 cm are expected and acceptable. Differences larger than 10 cm suggest a problem with either the base station survey-in position or the InaCORS connection.

> **Important:** Do not run both correction sources simultaneously during this comparison. Measure with one source, then switch to the other. See Step 6.

---

## Step 6: Do NOT Run the Local Base Station and InaCORS Simultaneously

**This is critical. If you are using InaCORS NTRIP corrections, your local RTK base station must be turned off or its radio link to the rover must be disabled.**

### Why This Matters

The u-blox ZED-F9P rover receiver accepts RTCM3 correction data from all enabled input ports simultaneously. It does not have a priority mechanism to choose between competing correction streams. When corrections arrive from two independent sources — the local radio base on one UART and NTRIP via Bluetooth on another — both streams are fed into the same internal correction engine.

This creates a documented failure mode:

- **Correction mixing:** The rover can associate the base station position (RTCM message 1005/1006) from one source with the satellite observation corrections (MSM messages) from the other source. The resulting position solution is silently wrong by up to the physical distance between the two base positions.
- **No error flag is raised.** The receiver may report RTK Fix with good accuracy estimates while the actual position is offset by meters. This error is invisible to the operator.
- **Coordinate jumps:** If the rover intermittently locks to corrections from the local base vs. InaCORS, your survey points will jump between two reference frames. With an auto-surveyed local base (which has 1-3 m absolute position error), these jumps can be 1-3 m — far exceeding acceptable survey tolerances.

This is not a theoretical concern. It is a protocol-level problem with how RTCM3 messages are associated inside the receiver, documented by NovAtel for their OEM7 receivers and applicable to any receiver that accepts corrections on multiple ports without explicit source arbitration. The ZED-F9P has no equivalent of NovAtel's `RTKSOURCE` command to select a preferred correction source.

### What To Do

**When using InaCORS NTRIP:**
- Power off the local base station entirely, OR
- Turn off the base station's radio transmitter, OR
- On the rover, physically disconnect or power off the radio receiver module

**When using the local radio base station:**
- Disconnect the NTRIP client in GNSS Master or SW Maps before beginning survey work
- Ensure no NTRIP connection is active on any app forwarding data to the rover

**Never** leave both active and assume the receiver will sort it out. It will not.

### Switching Between Sources in the Field

If you need to switch from one correction source to the other during a survey session:

1. **Stop collecting survey points.**
2. **Disconnect the current correction source** (close NTRIP client, or power off base station radio).
3. **Wait for the rover to lose RTK Fix** (it will drop to Autonomous or Float).
4. **Enable the new correction source** (connect NTRIP, or power on base station radio).
5. **Wait for RTK Fix** to re-establish on the new source (30-120 seconds).
6. **Verify the solution** per Step 5 before resuming data collection.

Do not collect any survey points during the transition. The position solution during switchover is unreliable.

---

## Troubleshooting

### Authentication Fails / Connection Refused

- **Most common cause:** You did not complete the subscription step (Step 1.3). Log in to `http://nrtk.big.go.id/sbc/` and verify the "Network RTK -- Unlimited" subscription is active.
- Check username and password for typos. Credentials are case-sensitive.
- Try NTRIP Version V1 if V2 fails, or vice versa.

### Connected but Stuck at RTK Float (No Fix)

- **Baseline too long:** You may be more than 30-50 km from the nearest station. Try the `nearest` mountpoint to confirm which station you are connecting to.
- **GGA not being sent:** Ensure "Send NMEA GGA" is enabled. Without GGA, VRS mountpoints cannot generate corrections for your location.
- **Poor sky visibility:** Move to a more open location. Multipath from buildings and tree canopy prevents ambiguity resolution.
- **Ionospheric conditions:** Near the equator, ionospheric activity can delay RTK Fix. Allow up to 5 minutes in challenging conditions.
- **Cold start issue:** If your receiver has no initial position (fresh cold start), the GGA sentence may be invalid. Wait for an autonomous fix before connecting NTRIP.

### App Shows Connected but Receiver Shows No Corrections

- In **GNSS Master**: Check that both the NTRIP client and the receiver connection are active simultaneously. The NTRIP client must have a receiver connection to forward corrections to.
- In **SW Maps**: Connect to the external GNSS receiver before opening the NTRIP client. Some versions require this order.

### Cannot Reach the Portal in Browser

- The portal at `nrtk.big.go.id` uses HTTP (not HTTPS). Some browsers block plain HTTP by default. Use Chrome and allow the HTTP connection.
- Check service status at `https://srgi.big.go.id/page/service-check`.

---

## Accuracy Reference

| Scenario | Typical Horizontal Accuracy |
|---|---|
| Autonomous GNSS (no corrections) | 3-5 m |
| RTK Float (corrections received, no fix) | 0.3-1 m |
| RTK Fix, `nearest`, baseline < 20 km | 2-3 cm |
| RTK Fix, `VRS`/`max` in Java/Sumatra | 1-3 cm |
| RTK Fix, `nearest`, baseline 20-50 km | 5-10 cm |

Accuracy degrades approximately 1 mm per additional kilometer of baseline distance when using the `nearest` (single-base) mountpoint. For baselines exceeding 50 km, RTK Fix becomes unreliable. In such cases, consider using InaCORS RINEX data for post-processing instead.

---

## Useful Resources

- **InaCORS portal:** `http://nrtk.big.go.id/sbc/`
- **Registration:** `http://nrtk.big.go.id/sbc/Account/Register`
- **SRGI service check:** `https://srgi.big.go.id/page/service-check`
- **SRGI nRTK info:** `https://srgi.big.go.id/page/nrtk`
- **Mobile InaCORS app** (station status/proximity): Google Play, package `bignrtk.bignrtk`
- **InaCORS on X/Twitter:** `@InaCORS` (operational notices and maintenance warnings)
