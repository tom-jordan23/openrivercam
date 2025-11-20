# 10.5 Configuring the PtBox - Automated Collection and Upload

This final configuration section establishes fully autonomous operation. With orientation, transformation, cross-sections, and server integration complete, the PtBox now operates independently - capturing video, processing velocity, calculating discharge, and uploading data without manual intervention.

Automated collection transforms OpenRiverCam from a field survey tool into an operational monitoring system. The deployment becomes self-sustaining, providing continuous data for humanitarian decision-making across seasons, years, and changing flow conditions.

By the end of this section, you will be able to:
- Configure automated video capture schedule
- Set processing triggers and frequency
- Enable continuous discharge calculation
- Configure system health monitoring
- Set up automated alerts for equipment issues
- Schedule data backup and maintenance tasks
- Verify autonomous operation
- Monitor system status remotely
- Plan for long-term operational support

**Reference:** Completes the deployment workflow from Chapters 6-10, producing operational river monitoring system.

---

## Understanding Automated Operation

### Operational Workflow

**In fully automated mode, PtBox executes this cycle continuously:**

**Capture cycle (every 5-15 minutes):**
1. **Capture video:** Camera records 5-30 second video clip of river
2. **Store video:** Save video file to local storage (with timestamp)
3. **Process video:** Run PIV analysis to extract velocity field
4. **Calculate discharge:** Combine velocity with current water level and cross-section area (Q = v × A)
5. **Upload to server:** Transmit velocity, discharge, water level, and metadata to LiveORC server
6. **Log results:** Record processing status, data quality flags, and any errors
7. **Wait for next cycle:** Sleep until next scheduled capture time
8. **Repeat indefinitely**

**No human intervention required** after initial configuration. System operates 24/7 across weeks, months, or years.

**System self-management:**
- Automatic error recovery (retry failed uploads, restart processing if crash)
- Storage management (delete old videos when storage fills, keep critical data)
- Power management (sleep between captures to conserve solar/battery power)
- Network management (reconnect if connection lost, switch to backup network if available)

### Why Automation Matters for Humanitarian Applications

**Operational continuity:**
- Monitoring continues during holidays, weekends, staff shortages
- No gaps in data during critical periods (rainy season, flood events)
- Reliable early warning requires consistent data flow

**Reduced operational costs:**
- No field visits for routine data download
- Minimal staff time after initial deployment
- One staff member can oversee multiple automated sites

**Scalability:**
- Deploy multiple sites across river basin or region
- Each site operates independently
- Central server aggregates data from all sites

**Rapid response:**
- Real-time data enables immediate decision-making
- Automated alerts trigger emergency response
- Hours or days gained for flood preparedness, evacuations, or aid deployment

---

## Configuring Video Capture Schedule

### Setting Capture Frequency

**How often PtBox captures video:**

**Configuration options:**

**Continuous monitoring (flood warning, emergency response):**
- **Capture interval:** Every 5 minutes
- **Video duration:** 10-15 seconds (sufficient for velocity calculation)
- **Daily videos:** 288 videos per day (24 hours × 12 per hour)
- **Storage requirement:** ~500 MB - 1 GB per day (depends on video resolution and compression)
- **Battery/power:** Higher power consumption (camera and processing active frequently)

**Standard monitoring (water resource management, seasonal trends):**
- **Capture interval:** Every 15 minutes
- **Video duration:** 15-20 seconds
- **Daily videos:** 96 videos per day
- **Storage requirement:** ~200-400 MB per day
- **Battery/power:** Moderate consumption (balance between data frequency and power conservation)

**Low-power monitoring (remote sites, solar-powered installations):**
- **Capture interval:** Every 1 hour or specific times of day (e.g., 6 AM, 12 PM, 6 PM)
- **Video duration:** 20-30 seconds (longer video for better averaging)
- **Daily videos:** 24 videos per day (hourly) or 3 videos per day (timed)
- **Storage requirement:** ~50-100 MB per day
- **Battery/power:** Minimal consumption (long sleep periods)

**Configuration in PtBox:**

1. **Navigate to automation settings:**
   - Configuration menu → Automation → Capture Schedule
   - Or Monitoring → Collection Settings
   - Or System → Operational Mode

2. **Enable automated capture:**
   - Toggle "Enable Automated Capture" or "Start Autonomous Mode"

3. **Set capture interval:**
   - **Interval type:** Select from dropdown
     - Fixed interval: Every X minutes (5, 15, 30, 60 min)
     - Scheduled: Specific times of day (enter time list: 06:00, 12:00, 18:00)
     - Adaptive: Increase frequency when flow changing rapidly (advanced)
   - **Interval value:** Enter number if fixed interval (e.g., 15 minutes)

4. **Set video duration:**
   - **Capture length:** 10-30 seconds (typical: 15 seconds)
   - Longer video → more frames → better velocity averaging
   - Shorter video → faster processing → lower storage

5. **Configure capture window (optional):**
   - **Active hours:** Capture only during specified time window
   - Example: 6 AM to 10 PM (daylight only, saves power)
   - Or 24-hour operation (continuous monitoring)

6. **Save schedule:**
   - Click "Save Schedule" or "Apply and Start"
   - PtBox begins automated capture cycle

### Handling Special Conditions

**Adaptive capture during events:**

**Some systems support event-triggered capture:**
- **Threshold trigger:** If discharge exceeds threshold (e.g., 50 m³/s), increase capture frequency
  - Normal: Every 15 minutes
  - Event: Every 5 minutes
  - Return to normal when discharge drops below threshold
- **Rate-of-change trigger:** If water level rising rapidly (e.g., >10 cm/hour), increase frequency
- **External trigger:** Emergency management system sends signal to increase monitoring

**Configuration:**
- Enable event-triggered mode: Toggle "Adaptive Capture"
- Set thresholds: Discharge threshold 50 m³/s, rate-of-change 10 cm/hr
- Set event frequency: Increase to every 5 minutes during event
- Set cooldown period: Return to normal after 2 hours below threshold

**Backup capture strategy:**
- If primary capture fails (camera error, storage full), retry after 1 minute
- If multiple failures, log error and alert administrator
- Continue attempting capture (do not give up permanently)

---

## Configuring Processing and Calculation

### Automated PIV Processing

**After video captured, PtBox processes video to extract velocity:**

**Processing configuration:**

1. **Navigate to processing settings:**
   - Configuration menu → Processing → PIV Settings
   - Or Video Analysis → Parameters

2. **Enable automated processing:**
   - Toggle "Process Videos Automatically" (typically enabled by default in autonomous mode)

3. **Set processing trigger:**
   - **Immediate:** Process video as soon as captured (real-time operation)
   - **Batched:** Process multiple videos together (reduces processing overhead, acceptable for non-urgent monitoring)
   - **Scheduled:** Process videos at specific times (e.g., every hour, process all videos captured in last hour)

4. **Configure PIV parameters:**
   - **Search area size:** Typically 32×32 or 64×64 pixels (balance between accuracy and speed)
   - **Correlation method:** Cross-correlation (standard) or optical flow (faster but less robust)
   - **Velocity range:** Expected velocity range (0.1-3.0 m/s typical for rivers)
   - **Quality filters:** Discard velocity vectors with low correlation scores
   - These parameters typically set during commissioning and rarely changed

5. **Set processing priority:**
   - **Real-time mode:** Process immediately even if battery low (prioritize data over power conservation)
   - **Power-saving mode:** Delay processing if battery below threshold, process when power available

### Automated Discharge Calculation

**After velocity calculated, PtBox combines with cross-section to calculate discharge:**

**Discharge calculation configuration:**

1. **Enable automated discharge calculation:**
   - Toggle "Calculate Discharge Automatically"
   - Requires cross-section configured (Section 10.3)

2. **Configure water level input:**
   - **Stage sensor (recommended):** PtBox reads water level from connected sensor
     - Sensor type: Pressure transducer, ultrasonic, or radar
     - Read interval: Every 5 minutes (or match capture interval)
     - Sensor address: Serial port, analog input, or network address
   - **Manual input:** Operator enters water level (not suitable for autonomous operation)
   - **Camera-based detection:** Estimate water level from image (experimental, less accurate)

3. **Set velocity-to-discharge parameters:**
   - **Velocity correction factor:** k = 0.85-0.90 (converts surface velocity to mean velocity)
   - **Measurement region:** Use mean velocity from entire field of view or specific region
   - **Cross-section selection:** Which cross-section to use (if multiple configured)

4. **Configure output:**
   - **Units:** m³/s (standard), L/s, or cfs (cubic feet per second)
   - **Precision:** Number of decimal places (typically 2: 4.35 m³/s)
   - **Quality flags:** Annotate data with quality indicators (good, marginal, poor)

### Data Quality Control

**Automated quality checks during processing:**

**Configuration:**

1. **Enable quality control:**
   - Toggle "Automatic Quality Control"

2. **Define quality criteria:**
   - **Minimum correlation:** PIV correlation score threshold (e.g., >0.6 for good quality)
   - **Velocity range:** Flag velocities outside expected range (e.g., <0 or >5 m/s likely errors)
   - **Discharge range:** Flag discharge outside reasonable range for site
   - **Temporal consistency:** Flag sudden jumps (e.g., discharge changes by >50% between measurements)

3. **Set actions for quality issues:**
   - **Flag data:** Mark as "Poor quality" but upload to server (users interpret with caution)
   - **Discard data:** Do not upload poor-quality measurements
   - **Alert administrator:** Send notification if repeated quality issues (indicates equipment problem)
   - **Retry capture:** If quality poor, capture additional video and reprocess

---

## Configuring System Health Monitoring

### Hardware Status Checks

**PtBox monitors hardware health automatically:**

**Monitored parameters:**

**Camera status:**
- Camera responding? (can capture images)
- Image quality adequate? (not completely dark, not overexposed)
- Lens clean? (not obstructed by dirt, spider webs, or water droplets)

**Storage status:**
- Available storage space (GB remaining)
- Storage health (solid-state drive or SD card not failing)
- Alert threshold: Warning when <20% storage free, critical when <10%

**Power status:**
- Battery voltage (if battery-powered)
- Solar panel output (if solar-powered)
- External power connection (if AC or DC mains)
- Alert threshold: Warning when battery <30%, critical when <20%

**Network status:**
- Internet connectivity active? (can reach server)
- Signal strength (if cellular or WiFi)
- Data usage (if cellular with limited plan)

**Temperature and environment:**
- Internal temperature (overheating risk in hot climates)
- Humidity (moisture intrusion risk)
- Alert threshold: Warning when temperature >60°C or <-10°C

**Configuration:**

1. **Navigate to health monitoring:**
   - Configuration menu → System → Health Monitoring
   - Or Diagnostics → Status Checks

2. **Enable automatic health checks:**
   - Toggle "Enable System Monitoring"

3. **Set check frequency:**
   - **Status check interval:** Every 15 minutes (typical)
   - Or every hour for less critical parameters

4. **Configure alerts:**
   - **Warning thresholds:** Generate warning when parameter marginal
   - **Critical thresholds:** Generate critical alert when parameter problematic
   - **Alert destinations:** Email, SMS, or server notification

**Example alert configuration:**
```
Storage space <20%: Warning (email to admin)
Storage space <10%: Critical (email + SMS to admin)
Battery <30%: Warning
Battery <20%: Critical (reduce capture frequency automatically)
Temperature >60°C: Warning (consider ventilation)
Network offline >1 hour: Critical (investigate connectivity)
```

### Software Status and Error Logging

**PtBox logs software events and errors:**

**Logged events:**
- Video capture success/failure
- Processing completion/errors
- Server upload success/failure
- Configuration changes
- System restarts or crashes

**Log configuration:**

1. **Enable logging:**
   - Toggle "Enable System Logging" (typically always enabled)

2. **Set log level:**
   - **Debug:** Very verbose (every operation logged, large log files)
   - **Info:** Standard operations logged (recommended for production)
   - **Warning:** Only warnings and errors logged (minimal logs)
   - **Error:** Only errors logged (troubleshooting mode)

3. **Configure log rotation:**
   - **Maximum log size:** 100 MB (typical)
   - When limit reached, archive old logs and start new log file
   - **Log retention:** Keep logs for 30 days, then delete (or upload to server)

4. **Enable remote log access:**
   - Upload logs to server periodically (weekly or monthly)
   - Enables remote troubleshooting without site visit
   - Or access logs via PtBox web interface remotely

---

## Configuring Alerts and Notifications

### Equipment Failure Alerts

**Notify administrators of system issues:**

**Alert configuration:**

1. **Navigate to alert settings:**
   - Configuration menu → Alerts → Equipment Alerts
   - Or Notifications → System Status

2. **Enable equipment alerts:**
   - Toggle "Enable Equipment Alerts"

3. **Configure alert channels:**
   - **Email alerts:**
     - SMTP server settings (mail server address, port, credentials)
     - Recipients: admin@organization.org, technician@organization.org
   - **SMS alerts:**
     - SMS gateway or API settings
     - Phone numbers: +123456789, +987654321
   - **Server-based alerts:**
     - Alert via LiveORC server notification system (if available)

4. **Set alert triggers:**
   - Camera failure: 3 consecutive capture failures
   - Processing failure: 5 consecutive processing errors
   - Upload failure: 10 consecutive upload failures (indicates prolonged connectivity loss)
   - Battery critical: Battery <20% and decreasing
   - Storage critical: Storage <10% free space

5. **Configure alert frequency:**
   - **Immediate:** Send alert as soon as trigger condition met
   - **Daily summary:** Send one alert per day summarizing all issues
   - **Suppress repeats:** Do not send duplicate alerts for same issue within 24 hours

**Example alert message:**
```
Subject: [OpenRiverCam Alert] Equipment Issue at Site_01

Site: Site_01 - River X Bridge
Issue: Camera failure (3 consecutive capture failures)
Time: 2024-11-15 14:30 UTC
Status: Camera not responding to capture commands
Action: Site visit required for camera inspection

Battery: 45% (OK)
Storage: 35% free (OK)
Network: Connected (OK)

Last successful capture: 2024-11-15 14:00 UTC
Next automatic retry: 2024-11-15 14:35 UTC
```

### Data Quality Alerts

**Notify users of poor data quality:**

**Alert configuration:**

1. **Enable data quality alerts:**
   - Toggle "Enable Data Quality Alerts"

2. **Set quality thresholds:**
   - **Low correlation:** >20% of velocity vectors have correlation <0.5
   - **Unrealistic values:** Discharge <0 or >200 m³/s (site-specific thresholds)
   - **Repeated failures:** Quality issues for >6 consecutive measurements

3. **Configure alert recipients:**
   - Data users (decision-makers who use discharge data)
   - System administrators (can investigate root cause)

**Data quality alerts indicate:**
- Camera image quality degraded (dirty lens, obstructions)
- Water surface conditions poor for PIV (no visible features, glare)
- Configuration error (incorrect transformation or cross-section)
- Equipment malfunction (camera, processor, or storage)

---

## Configuring Data Management

### Storage Management

**PtBox local storage limited (typically 32-128 GB):**

**Storage policy configuration:**

1. **Navigate to storage settings:**
   - Configuration menu → System → Storage Management
   - Or Data → Local Storage

2. **Set storage limits:**
   - **Maximum storage used:** 80% (leave headroom for system operation)
   - **Alert threshold:** Warning when 70% full

3. **Configure data retention:**
   - **Video retention:** Keep videos for 7 days, then delete
     - Videos uploaded to server (if enabled) so local deletion acceptable
     - Or keep indefinitely if critical or server not available
   - **Processed data retention:** Keep velocity/discharge results indefinitely (small file size)
   - **Log retention:** Keep logs for 30 days

4. **Enable automatic deletion:**
   - Toggle "Auto-Delete Old Videos"
   - Oldest videos deleted first when storage threshold exceeded
   - Critical data (flagged measurements, event videos) protected from deletion

### Data Backup

**Backup strategy for operational data:**

**Configuration:**

1. **Primary backup: Server upload**
   - Velocity, discharge, water level uploaded to LiveORC server (Section 10.4)
   - Server provides persistent storage and redundancy

2. **Secondary backup: Local storage**
   - Processed data stored on PtBox (redundancy if server unavailable)
   - Or external USB drive connected to PtBox for backup

3. **Tertiary backup: Periodic site visit**
   - During maintenance visits, download all data from PtBox to laptop
   - Archive data to organization's secure storage (cloud or local server)

**Backup frequency:**
- Server upload: Real-time or every 5-15 minutes (continuous backup)
- External drive backup: Weekly or monthly (if configured)
- Manual download: During quarterly or annual maintenance visits

---

## Verifying Autonomous Operation

### Initial Verification (24-48 Hours)

**After configuration complete, verify system operates autonomously:**

**Verification procedure:**

**Day 1: Initial operation**
1. **Start autonomous mode:**
   - Enable automated capture, processing, and upload
   - Verify first video captured successfully
   - Check first data point appears on server

2. **Monitor first few cycles (2-3 hours):**
   - Check data uploads every 15 minutes (or configured interval)
   - Review logs for errors
   - Verify data quality acceptable (velocity and discharge reasonable)

3. **Leave site:**
   - Do not intervene (test autonomous operation)
   - Monitor remotely via server dashboard

**Day 2: Review 24-hour operation**
4. **Check server dashboard:**
   - Verify data continuity (no large gaps)
   - Count data points: Should match expected (e.g., 96 measurements if 15-min intervals)

5. **Review upload success rate:**
   - Expected: 96 uploads in 24 hours
   - Actual: Check count on server
   - Success rate: (actual / expected) × 100%
   - Target: >95% success rate

6. **Check system health:**
   - Battery level stable or charging? (if solar/battery)
   - Storage usage reasonable? (not filling too quickly)
   - No critical alerts sent?

**If verification successful:** System ready for long-term operation.

**If issues detected:** Investigate logs, review configuration, make corrections, repeat verification.

### Long-Term Monitoring

**After initial verification, monitor system periodically:**

**Daily monitoring (first week):**
- Check server dashboard once per day
- Verify data still flowing
- Review any alerts received

**Weekly monitoring (after first week):**
- Review weekly data summary
- Check data quality trends
- Verify system health metrics stable

**Monthly monitoring (long-term):**
- Review monthly hydrograph
- Check storage and battery trends
- Plan maintenance visits if needed

**Quarterly maintenance visits (recommended):**
- Site visit to inspect hardware
- Clean camera lens, check mounting security
- Download data backup from PtBox
- Verify GCP markers still visible and stable
- Update configuration if needed

---

## Operational Best Practices

### Power Management

**For solar-battery installations:**

**Optimize power consumption:**
- Reduce capture frequency during cloudy periods (if battery low)
- Disable non-essential features during low power (e.g., high-resolution video)
- Implement sleep mode between captures (minimize power draw)

**Monitor power trends:**
- Battery voltage should increase during day (solar charging)
- Battery voltage should be stable or slow decrease at night
- If battery continuously decreasing, solar capacity insufficient (add panel or reduce load)

**Power budget example:**
```
Daily power consumption:
- Camera capture: 96 captures × 0.5 Wh = 48 Wh
- Video processing: 96 processes × 0.3 Wh = 29 Wh
- Cellular upload: 96 uploads × 0.1 Wh = 10 Wh
- System idle: 23 hours × 1 W = 23 Wh
Total daily consumption: ~110 Wh

Solar generation (50W panel, 5 peak sun hours):
50W × 5 hours × 0.7 efficiency = 175 Wh/day

Power surplus: 175 - 110 = 65 Wh/day (adequate margin)
```

### Network and Connectivity

**For cellular connections:**

**Monitor data usage:**
- Typical data usage: 100-300 MB/month (15-minute intervals)
- Check usage against data plan limits
- Adjust upload frequency if approaching limits

**Optimize cellular costs:**
- Compress data before upload (reduce payload size)
- Batch uploads (reduce connection overhead)
- Use WiFi when available (cheaper than cellular)

**Handle connectivity interruptions:**
- Buffer data locally during outages (upload when restored)
- Retry failed uploads with exponential backoff
- Alert if connectivity lost for extended period (>24 hours)

### Seasonal Adjustments

**Configuration may need seasonal adjustments:**

**Rainy season (flood monitoring):**
- Increase capture frequency (every 5 minutes)
- Lower discharge alert thresholds (earlier warnings)
- More frequent server dashboard checks

**Dry season (low flow monitoring):**
- Decrease capture frequency (every 30-60 minutes)
- Adjust velocity range (lower velocities expected)
- Less frequent monitoring (stable conditions)

**Vegetation growth:**
- Trim vegetation near GCP markers (maintain visibility)
- Clean camera lens more frequently (pollen, leaves)
- Resurvey GCPs if markers obscured permanently

---

## Common Issues and Solutions

### Issue: System stops capturing videos

**Symptoms:**
- No new data on server for several hours
- Last capture timestamp significantly in past

**Solutions:**
- **Check power:** Battery drained? Solar panel disconnected? External power failed?
  - Solution: Recharge battery, reconnect power, replace failed component
- **Check camera:** Camera malfunctioning? Cable disconnected?
  - Solution: Reconnect cable, restart camera, replace camera if failed
- **Check storage:** Storage full?
  - Solution: Enable auto-delete old videos, increase storage, manually delete files
- **Check software:** PtBox software crashed?
  - Solution: Restart PtBox, check logs for crash cause, update software if bug

### Issue: Data uploads but quality poor

**Symptoms:**
- Velocity measurements erratic or unrealistic
- Discharge values do not match expected patterns
- Quality flags indicate poor data

**Solutions:**
- **Check camera lens:** Dirty or obstructed?
  - Solution: Clean lens (site visit), schedule more frequent cleaning
- **Check water surface:** No visible features for PIV? (glare, stagnant water)
  - Solution: Accept lower quality during these conditions, or adjust camera angle
- **Check transformation:** GCPs moved or camera shifted?
  - Solution: Verify GCP markers stable, recalibrate transformation if needed
- **Check lighting:** Videos too dark or overexposed?
  - Solution: Adjust camera exposure settings, restrict capture to daylight hours

### Issue: Battery drains faster than expected

**Symptoms:**
- Battery voltage decreasing over days
- Battery critical alerts frequent
- System shutting down due to low power

**Solutions:**
- **Increase solar capacity:** Add panel or larger panel
- **Reduce power consumption:** Decrease capture frequency, reduce processing load
- **Check battery health:** Old battery capacity degraded?
  - Solution: Replace battery (typically every 2-5 years)
- **Check connections:** Loose solar panel connection reducing charge?
  - Solution: Tighten connections, check for corrosion

### Issue: Cellular data usage exceeds plan

**Symptoms:**
- Data plan exhausted mid-month
- Cellular carrier throttles speed or stops service
- Unexpected overage charges

**Solutions:**
- **Reduce upload frequency:** Every 30 minutes instead of 15 minutes
- **Enable compression:** Compress data payloads (reduce size by 50-70%)
- **Reduce payload size:** Upload only essential fields (omit metadata)
- **Upgrade data plan:** If data valuable, invest in larger plan

---

## Time Estimates

**Automated collection configuration time:**

**First-time configuration:**
- Configure capture schedule: 10-15 minutes
- Configure processing and calculation: 10-15 minutes
- Configure system health monitoring: 10-15 minutes
- Configure alerts and notifications: 15-20 minutes
- Configure data management: 5-10 minutes
- Initial verification (24-48 hours): Ongoing monitoring
- **Total active configuration time: 50-75 minutes**
- **Plus 24-48 hour verification period**

**Experienced user:**
- Configure all automation settings: 20-30 minutes
- Initial verification: 24-48 hours
- **Total: 30 minutes + verification**

**Verification critical for operational success.** Do not leave site before confirming first few capture cycles successful.

---

## Summary: Automated Collection and Upload

**Purpose:**
- Enable fully autonomous operation (no manual intervention)
- Continuous data collection for operational monitoring
- Reliable early warning and long-term data series
- Scalable multi-site deployment

**Key steps:**
1. Configure automated video capture schedule (frequency, duration, active hours)
2. Enable automated processing (PIV velocity extraction)
3. Enable automated discharge calculation (Q = v × A)
4. Configure system health monitoring (hardware and software status checks)
5. Set up equipment and data quality alerts (notify administrators of issues)
6. Configure data management (storage limits, retention, backup)
7. Verify autonomous operation (24-48 hour test)
8. Establish long-term monitoring routine (daily, weekly, monthly checks)

**Quality criteria:**
- Capture success rate >95% (occasional failures acceptable)
- Upload success rate >95% (reliable data transmission)
- Data quality acceptable (realistic velocity and discharge values)
- System health stable (battery charging, storage not full, network connected)
- Alerts functional (receive notifications when issues occur)

**Operational workflow established:**
- **PtBox:** Autonomous capture, processing, upload (no staff intervention)
- **Server:** Centralized data storage, visualization, alerting
- **Staff:** Remote monitoring via dashboard, respond to alerts, periodic maintenance visits

**Long-term sustainability:**
- Quarterly maintenance visits (clean lens, check hardware, download backup)
- Annual system review (verify GCPs stable, recalibrate if needed, update software)
- Multi-year operation (system designed for 5-10 year deployment with maintenance)

**Deployment complete:**
With automated collection configured, OpenRiverCam deployment is operational. The system now provides continuous river monitoring data for humanitarian decision-making - from flood early warning to water resource management to long-term climate adaptation planning.

---

## Final Deployment Checklist

**Before leaving site, verify:**

**Hardware:**
- [ ] Camera operational and capturing clear images
- [ ] Camera mounting secure (withstands wind, vibration)
- [ ] Solar panel oriented correctly (maximum sun exposure)
- [ ] Battery charged and connections secure
- [ ] Enclosure sealed (weather-resistant)
- [ ] GCP markers visible and stable

**Configuration:**
- [ ] Image orientation correct (Section 10.1)
- [ ] GCP transformation established with acceptable reprojection errors (Section 10.2)
- [ ] Cross-section loaded and discharge calculation working (Section 10.3)
- [ ] Server connection established and data uploading (Section 10.4)
- [ ] Automated capture and processing enabled (Section 10.5)

**Verification:**
- [ ] Multiple video captures successful (3-5 cycles observed)
- [ ] Data appearing on server dashboard in real-time
- [ ] Velocity and discharge values reasonable for site conditions
- [ ] No critical alerts or errors in logs
- [ ] Battery charging (if solar) or power stable (if mains)
- [ ] Storage usage reasonable (not filling too quickly)

**Documentation:**
- [ ] Configuration log completed (all settings documented)
- [ ] Site photos taken (hardware installation, GCP markers, river conditions)
- [ ] Survey data backed up (GCPs, cross-section, camera position)
- [ ] Contact information recorded (server administrator, local contacts, emergency contacts)
- [ ] Maintenance schedule planned (quarterly visits, annual review)

**Communication:**
- [ ] Server administrator notified of new site operational
- [ ] Data users informed of data availability (dashboard URL, access credentials)
- [ ] Local authorities informed of installation (security, coordination)
- [ ] Maintenance team briefed on site location and access

**Congratulations: Your OpenRiverCam system is now operational and providing valuable river monitoring data for humanitarian decision-making.**

---

**References:**
- Section 10.1: Orienting the Image (prerequisite configuration)
- Section 10.2: Adding Control Points (prerequisite configuration)
- Section 10.3: Adding Cross-Sections (prerequisite configuration)
- Section 10.4: Server Integration (prerequisite configuration)
- Chapter 8: Equipment Installation (hardware setup)
- Chapter 9: Site Survey (data collection for configuration)

**Next Steps:**
- Monitor system remotely via server dashboard
- Respond to alerts promptly (equipment issues, data quality problems)
- Schedule quarterly maintenance visits
- Analyze data for decision-making (flood warnings, water resource planning)
- Share data with stakeholders (humanitarian organizations, government agencies, communities)
