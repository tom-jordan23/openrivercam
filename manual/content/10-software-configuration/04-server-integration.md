# 10.4 Configuring the PtBox - Server Integration

This section configures connectivity between the PtBox field device and the LiveORC server for remote data access. While the PtBox can operate standalone, server integration enables real-time monitoring, data visualization, alerting, and multi-site management from a central location.

Server integration connects field measurements to humanitarian decision-makers. Raw velocity and discharge data become accessible dashboards, automated alerts, and operational intelligence for flood preparedness, water resource management, and emergency response.

By the end of this section, you will be able to:
- Understand LiveORC server architecture and data flow
- Configure PtBox network connectivity (WiFi, cellular, Ethernet)
- Enter server connection parameters (URL, API credentials)
- Configure data transmission settings (frequency, retry logic)
- Test server connection and data upload
- Verify data appearing on server dashboard
- Troubleshoot connection and authentication issues
- Configure upload schedule for operational monitoring

**Reference:** Completes deployment workflow from Chapter 6 (Site Selection) through Chapter 9 (Survey) to operational system.

---

## Understanding Server Integration Architecture

### LiveORC Server Overview

**LiveORC provides centralized data management:**

**Server functions:**
- **Data storage:** Centralized database for velocity, discharge, and water level time series
- **Data processing:** Additional processing and quality control on server side
- **Visualization:** Web dashboards displaying hydrographs, maps, and site status
- **Alerting:** Automated notifications when thresholds exceeded (flood warnings)
- **API access:** Programmatic data access for integration with other systems
- **Multi-site management:** Monitor multiple OpenRiverCam installations from one interface

**Why server integration matters for humanitarian applications:**

**Real-time awareness:**
- Decision-makers monitor river conditions remotely without visiting field sites
- Early warning systems detect rising water levels and trigger alerts
- Operational staff assess multiple sites simultaneously

**Data accessibility:**
- Field data accessible from headquarters, regional offices, or mobile devices
- No need to physically download data from PtBox
- Historical data available for analysis and reporting

**Coordination:**
- Multiple organizations access same data stream (no data silos)
- Standardized data formats and APIs enable interoperability
- Integration with other humanitarian information systems (flood forecasting, evacuation planning)

### Data Flow: PtBox to Server

**Operational data pipeline:**

1. **PtBox captures video:** Camera records river at configured interval (e.g., every 5 minutes)
2. **PtBox processes video:** PIV analysis extracts velocity field from video
3. **PtBox calculates discharge:** Combine velocity with cross-section area (Q = v × A)
4. **PtBox packages data:** Create data packet with timestamp, velocity, discharge, water level, metadata
5. **PtBox transmits to server:** Upload data packet via internet connection (WiFi, cellular, or Ethernet)
6. **Server receives data:** Validate, process, and store in database
7. **Server updates dashboards:** Real-time display of latest measurements
8. **Server evaluates alerts:** Check if measurements exceed thresholds, send notifications if needed

**Transmission frequency:**
- Typically every 5-15 minutes (matches measurement frequency)
- Configurable based on application needs (more frequent for flood warning, less frequent for long-term monitoring)
- Bandwidth considerations for cellular connections

**Data security:**
- Encrypted transmission (HTTPS/TLS)
- API authentication (username/password or token-based)
- Access control on server (role-based permissions)

### Connection Requirements

**For PtBox to communicate with server:**

**Network connectivity:**
- Internet connection: WiFi, cellular (4G/LTE), or Ethernet
- Stable connection (occasional dropouts acceptable with retry logic)
- Sufficient bandwidth: ~1-10 MB per upload (depending on data payload size)

**Server accessibility:**
- Server must have public IP address or domain name
- Or PtBox must be on same network as server (for local installations)
- Firewall rules allow PtBox to connect to server (outbound HTTPS typically port 443)

**Authentication credentials:**
- Username and password, or API token
- Provided by server administrator during site registration

**Site registration:**
- Site must be registered on server before PtBox can upload data
- Server creates site ID and credentials
- Credentials configured in PtBox

---

## Configuring Network Connectivity

### Network Connection Options

**PtBox supports multiple network types:**

**Option 1: WiFi connection**
- Connect PtBox to local WiFi network (office, field station, community center)
- Requires WiFi network with internet access
- Configuration: SSID (network name) and password

**Option 2: Cellular connection (4G/LTE)**
- Install SIM card in PtBox cellular modem
- PtBox connects via mobile network
- Requires cellular coverage at site and active data plan
- Configuration: APN settings (provided by cellular carrier)

**Option 3: Ethernet connection**
- Connect PtBox to wired network via Ethernet cable
- Typically used for permanent installations near infrastructure
- Configuration: DHCP (automatic) or static IP address

**Option 4: Satellite connection (specialized)**
- For remote sites without terrestrial connectivity
- Requires satellite modem and service subscription
- Higher latency and cost but enables connectivity anywhere

**Most humanitarian deployments use WiFi or cellular.** Choose based on site conditions and available infrastructure.

### WiFi Configuration

**If using WiFi connection:**

1. **Access PtBox network configuration interface:**
   - Configuration menu → Network → WiFi Settings
   - Or System → Connectivity → WiFi

2. **Scan for available networks:**
   - Click "Scan Networks" or "Search"
   - PtBox displays list of detected WiFi networks (SSIDs)

3. **Select target network:**
   - Choose network with internet access
   - Example: "FieldOffice_Guest" or "NGO_Operations"

4. **Enter network credentials:**
   - **SSID:** Network name (auto-filled if selected from scan)
   - **Security type:** WPA2 (most common), WPA3, or Open (not recommended)
   - **Password:** Network password (case-sensitive)

5. **Connect:**
   - Click "Connect" or "Apply"
   - PtBox attempts connection
   - Wait 10-30 seconds for connection to establish

6. **Verify connection:**
   - Interface displays "Connected" status
   - IP address assigned to PtBox (e.g., 192.168.1.150)
   - Internet connectivity indicator (green checkmark or "Online")

**Test internet connectivity:**
- Some interfaces provide "Test Connection" button
- Pings external server to verify internet access
- Or manually browse to external website (e.g., google.com) to confirm

**If connection fails:**
- Verify password correct (check for typos, case sensitivity)
- Ensure network has internet access (not isolated local network)
- Check WiFi signal strength (may need to relocate PtBox or use external antenna)
- Verify network allows new device connections (some networks restrict DHCP)

### Cellular Configuration

**If using cellular connection:**

1. **Install SIM card in PtBox:**
   - Power off PtBox
   - Open cellular modem slot (location varies by hardware)
   - Insert SIM card (ensure correct orientation)
   - Close slot and power on PtBox

2. **Access cellular configuration interface:**
   - Configuration menu → Network → Cellular Settings
   - Or System → Connectivity → Mobile Data

3. **Enter APN settings:**
   - **APN (Access Point Name):** Provided by cellular carrier
   - Example: "internet.carrier.com" or "web.carrier.net"
   - **Username:** May be required (carrier-specific)
   - **Password:** May be required (carrier-specific)
   - Obtain APN settings from carrier documentation or support

4. **Enable cellular connection:**
   - Toggle "Enable Cellular" or "Mobile Data"
   - PtBox attempts connection to cellular network
   - Wait 30-60 seconds for registration and connection

5. **Verify connection:**
   - Interface displays signal strength (bars or dBm value)
   - Connection status: "Connected" or "Registered"
   - IP address assigned by carrier
   - Data usage counter may display (useful for monitoring data plan usage)

**Test internet connectivity** as with WiFi (ping external server or browse to website).

**Cellular troubleshooting:**
- **No signal:** Verify SIM card installed correctly, check cellular coverage at site
- **No data connection:** Verify APN settings correct, ensure data plan active
- **Slow connection:** Check signal strength, consider external antenna if weak

---

## Configuring Server Connection Parameters

### Obtaining Server Credentials

**Before configuring PtBox, register site with LiveORC server:**

**Server administrator provides:**
- **Server URL:** Example: `https://liveorc.rainriver.org` or `http://192.168.1.10:8000` (local server)
- **Site ID:** Unique identifier for this monitoring site: `Site_01` or `RiverX_Bridge`
- **API endpoint:** Full API URL for data upload: `https://liveorc.rainriver.org/api/v1/upload`
- **Authentication credentials:**
  - Option A: Username and password
  - Option B: API token or key
- **Additional parameters:**
  - Upload frequency (how often to send data)
  - Data format specifications (JSON, CSV, or proprietary format)
  - Retry settings (how to handle failed uploads)

**Document credentials securely:**
- Record in configuration log or secure password manager
- Do not share publicly (API credentials provide data write access)

### Entering Server Configuration in PtBox

**In PtBox interface:**

1. **Navigate to server configuration section:**
   - Configuration menu → Server → LiveORC Connection
   - Or Data Upload → Server Settings
   - Or Cloud → Integration

2. **Enable server integration:**
   - Toggle "Enable Server Upload" or "Activate Cloud Connection"

3. **Enter server URL:**
   - **Server address:** `https://liveorc.rainriver.org`
   - Ensure correct protocol: HTTPS (secure) vs. HTTP (not secure, use only for local servers)
   - Include port if non-standard: `https://server.org:8443`

4. **Enter API endpoint (if separate from base URL):**
   - **Upload endpoint:** `/api/v1/upload` or `/data/push`
   - Or full URL: `https://liveorc.rainriver.org/api/v1/upload`

5. **Enter authentication credentials:**
   - **Authentication method:** Select Username/Password or API Token
   - If Username/Password:
     - **Username:** `site01_user`
     - **Password:** `***********` (hidden, case-sensitive)
   - If API Token:
     - **Token:** `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` (long alphanumeric string)

6. **Enter site identification:**
   - **Site ID:** `Site_01` (must match server site registration)
   - **Site name:** "River X Bridge Monitoring" (descriptive, optional)
   - **Location:** May include coordinates or description

7. **Save configuration:**
   - Click "Save" or "Apply Settings"
   - PtBox stores server connection parameters
   - Confirmation: "Server configuration saved"

---

## Configuring Data Transmission Settings

### Upload Frequency and Scheduling

**How often PtBox uploads data to server:**

**Typical configurations:**

**Real-time monitoring (flood warning applications):**
- Upload frequency: Every 5 minutes
- Enables rapid response to changing conditions
- Higher cellular data usage (~250-300 MB/month)

**Standard monitoring (water resource management):**
- Upload frequency: Every 15 minutes
- Balance between data timeliness and bandwidth
- Moderate data usage (~100-150 MB/month)

**Low-bandwidth monitoring (remote sites with limited connectivity):**
- Upload frequency: Every 1 hour or once per day
- Minimize cellular data costs
- Acceptable for long-term trends but not real-time alerting
- Low data usage (~20-50 MB/month)

**Configuration in PtBox:**

1. **Set upload interval:**
   - **Upload frequency:** Select from dropdown or enter value
   - Options: Every 5 min, 15 min, 30 min, 1 hour, 4 hours, 1 day
   - Or custom: Enter interval in minutes

2. **Set upload schedule (optional):**
   - Upload only during specific time windows (e.g., 6 AM to 10 PM)
   - Useful for minimizing nighttime cellular usage
   - Or continuous upload (default)

3. **Configure batch uploads (optional):**
   - Accumulate multiple measurements, upload in batches
   - Reduces number of connections (saves cellular overhead)
   - Example: Measure every 5 minutes, upload batch of 3 measurements every 15 minutes

### Retry Logic and Error Handling

**What happens if upload fails:**

**Retry configuration:**

1. **Enable automatic retry:**
   - Toggle "Enable Retry on Failure" (typically enabled by default)

2. **Set retry parameters:**
   - **Maximum retry attempts:** 3-5 (try failed upload multiple times before giving up)
   - **Retry delay:** 1-5 minutes between attempts (exponential backoff recommended)
   - Example: First retry after 1 min, second retry after 2 min, third retry after 4 min

3. **Configure data buffering:**
   - **Buffer failed uploads:** Store data locally if upload fails
   - **Buffer size:** Maximum number of measurements to store (e.g., 1000 measurements = ~3 days at 5-min intervals)
   - When connectivity restored, upload buffered data

4. **Set data priority:**
   - **Upload recent data first:** Latest measurements uploaded before buffered data (prioritize real-time)
   - Or **upload oldest data first:** Historical gaps filled chronologically (prioritize completeness)

**Handling persistent connection failures:**

**If connection fails repeatedly:**
- PtBox logs errors for later review
- Continues measuring and processing (data not lost, just not uploaded)
- Buffered data uploaded when connectivity restored
- May trigger local alert (email, SMS, or dashboard notification if configured)

### Data Format and Compression

**Configure data payload format:**

**Format options:**

**JSON format (common for REST APIs):**
```json
{
  "site_id": "Site_01",
  "timestamp": "2024-11-15T14:30:00Z",
  "velocity_mean": 0.65,
  "velocity_max": 1.15,
  "discharge": 4.35,
  "water_level": 140.25,
  "quality_flag": "good"
}
```

**CSV format (simpler, smaller payload):**
```
site_id,timestamp,velocity_mean,discharge,water_level
Site_01,2024-11-15T14:30:00Z,0.65,4.35,140.25
```

**Configuration:**
- **Data format:** Select JSON, CSV, or XML
- **Include metadata:** Toggle additional fields (camera ID, software version, processing parameters)
- **Compression:** Enable gzip compression to reduce upload size (typically reduces by 50-70%)

---

## Testing Server Connection

### Initial Connection Test

**Before operational use, test server integration:**

**Test procedure:**

1. **Navigate to test interface:**
   - Server configuration → Test Connection
   - Or click "Test Upload" button

2. **Initiate test:**
   - PtBox attempts connection to server
   - Uploads test data packet (or current measurements if available)

3. **Monitor test progress:**
   - Interface displays status messages:
     - "Connecting to server..."
     - "Authenticating..."
     - "Uploading data..."
     - "Upload successful" or "Upload failed"

4. **Review test results:**
   - **Success:** Server responded with confirmation (typically HTTP 200 OK)
   - **Failure:** Error message indicates problem (authentication failed, network timeout, server unavailable)

**Interpreting test results:**

**Success indicators:**
- Status: "Upload successful" or "Connection OK"
- HTTP response code: 200 (OK) or 201 (Created)
- Server response message: "Data received and stored"

**Failure indicators:**
- Status: "Upload failed" or "Connection error"
- HTTP response code:
  - 401 Unauthorized: Authentication credentials incorrect
  - 403 Forbidden: Credentials correct but insufficient permissions
  - 404 Not Found: API endpoint URL incorrect or site not registered
  - 500 Server Error: Server-side problem (contact server administrator)
  - Timeout: Network connectivity issue or server not responding

### Verifying Data on Server Dashboard

**After successful test upload:**

1. **Access LiveORC server web interface:**
   - Open browser, navigate to server URL: `https://liveorc.rainriver.org`
   - Log in with server account credentials (separate from PtBox API credentials)

2. **Navigate to site dashboard:**
   - Select site from list: "Site_01 - River X Bridge"
   - Or use map to locate site geographically

3. **Check latest data:**
   - Dashboard displays most recent measurements
   - Timestamp should match test upload time
   - Velocity, discharge, water level values should match PtBox readings

4. **Verify data time series:**
   - View hydrograph (discharge vs. time plot)
   - Verify test data point appears on graph
   - Check that historical data (if any) displays correctly

**If data does not appear on server:**
- Wait 1-2 minutes (server may have processing delay)
- Refresh dashboard page
- Check server logs (if access available) for upload errors
- Verify site ID in PtBox matches site ID on server (case-sensitive)

### Testing Upload Reliability

**Beyond initial test, verify consistent uploads:**

**24-hour reliability test:**

1. **Configure PtBox for frequent uploads:** Set to every 5 minutes
2. **Monitor for 24 hours:** Check server dashboard periodically
3. **Review upload success rate:**
   - Expected measurements: 24 hours × 12 per hour = 288 measurements
   - Received measurements: Check count on server
   - Success rate: (received / expected) × 100%
   - Acceptable: >95% success rate (occasional dropouts OK)
   - Problematic: <90% success rate (investigate connectivity or configuration)

**Check data gaps:**
- Review time series on server for missing periods
- If gaps appear, check PtBox logs for upload errors during those times
- Common causes: Temporary network outage, server maintenance, configuration error

---

## Troubleshooting Connection Issues

### Issue: Authentication Failed (401 Unauthorized)

**Symptoms:**
- Test upload fails with "Authentication failed" error
- HTTP 401 response code
- Data does not appear on server

**Solutions:**
- **Verify credentials:** Double-check username/password or API token
  - Check for typos, extra spaces, incorrect case
  - Copy-paste credentials to avoid manual entry errors
- **Verify site registered on server:** Contact server administrator to confirm site exists and credentials active
- **Check authentication method:** Ensure using correct method (username/password vs. API token)
- **Token expiration:** Some API tokens expire after period (e.g., 90 days) - request new token if expired

### Issue: Network Timeout or Connection Refused

**Symptoms:**
- Test upload fails with "Connection timeout" or "Cannot reach server"
- No HTTP response code (timeout before response received)

**Solutions:**
- **Verify network connectivity:** Confirm PtBox has internet access
  - Ping external server: `ping 8.8.8.8` (Google DNS)
  - Browse to website (google.com) to test internet
- **Check server URL:** Verify URL correct (typo in domain name or port?)
- **Check firewall rules:** Outbound HTTPS (port 443) may be blocked
  - Contact network administrator to allow PtBox IP address
- **Verify server operational:** Server may be down for maintenance
  - Contact server administrator or check server status page

### Issue: Server Error (500 Internal Server Error)

**Symptoms:**
- Test upload fails with "Server error" message
- HTTP 500, 502, or 503 response code
- Server receives request but cannot process

**Solutions:**
- **Contact server administrator:** Server-side issue (database error, processing bug, storage full)
- **Check server logs:** Administrator can review logs for specific error details
- **Wait and retry:** Temporary server issue may resolve itself
- **Verify data format:** Malformed data packet may cause server processing error
  - Check that PtBox data format matches server expectations

### Issue: Data Appears on Server but Incorrect Values

**Symptoms:**
- Upload successful, data visible on server dashboard
- But velocity, discharge, or water level values incorrect or unrealistic

**Solutions:**
- **Check unit conversion:** Server may expect different units than PtBox sends
  - Example: PtBox sends discharge in m³/s, server expects L/s
  - Configure unit conversion in PtBox or server settings
- **Verify coordinate transformation:** Velocity errors may stem from GCP calibration issues (Section 10.2)
- **Check cross-section configuration:** Discharge errors may stem from cross-section or water level datum issues (Section 10.3)
- **Review server processing:** Server may apply additional processing (averaging, filtering) that alters values

---

## Configuring Additional Server Features

### Alert and Notification Configuration

**Many servers support automated alerting:**

**Alert configuration (typically on server side, not PtBox):**

1. **Access server alert settings:**
   - Server dashboard → Site Settings → Alerts
   - Or Notifications → Configure Thresholds

2. **Define alert thresholds:**
   - **Discharge threshold:** Alert if discharge exceeds 50 m³/s (flood warning)
   - **Water level threshold:** Alert if water level exceeds 141.5 m (overbank flow)
   - **Velocity threshold:** Alert if velocity exceeds 2.0 m/s (hazardous conditions)

3. **Configure notification channels:**
   - **Email:** Send alert to recipients@organization.org
   - **SMS:** Send text message to phone numbers
   - **Webhook:** POST alert to external system (emergency management platform)

4. **Set alert frequency:**
   - Immediate: Alert sent as soon as threshold exceeded
   - Delayed: Alert sent if threshold exceeded for sustained period (e.g., 15 minutes)
   - Daily summary: Alert sent once per day with status update

**Alert configuration beyond scope of PtBox setup,** but essential for operational monitoring. Coordinate with server administrator and decision-makers to define appropriate thresholds and notification procedures.

### API Access for Third-Party Integration

**Server may provide API for programmatic data access:**

**Use cases:**
- Export data to GIS platforms (ArcGIS, QGIS)
- Integrate with flood forecasting models
- Feed data to humanitarian information systems (HDX, ReliefWeb)
- Custom dashboards and visualization tools

**API documentation:**
- Request from server administrator
- Typically includes endpoints for:
  - Query latest data: `GET /api/v1/sites/Site_01/latest`
  - Query time series: `GET /api/v1/sites/Site_01/data?start=2024-11-01&end=2024-11-15`
  - Site metadata: `GET /api/v1/sites/Site_01/info`

**Authentication for API access:**
- Similar to PtBox upload credentials (username/password or API token)
- Different permission levels (read-only vs. read-write)

---

## Time Estimates

**Server integration configuration time:**

**First-time configuration:**
- Configure network connectivity (WiFi or cellular): 10-20 minutes
- Enter server connection parameters: 5-10 minutes
- Configure data transmission settings: 5-10 minutes
- Test connection and upload: 5-10 minutes
- Verify data on server dashboard: 5 minutes
- Troubleshoot (if needed): 10-30 minutes
- **Total: 40-85 minutes**

**Experienced user:**
- Network and server configuration: 10-15 minutes
- Test and verify: 5 minutes
- **Total: 15-20 minutes**

**Troubleshooting adds significant time if connection issues arise.** Budget extra time for first deployment or sites with challenging connectivity.

---

## Summary: Server Integration

**Purpose:**
- Enable remote access to river monitoring data
- Centralize data storage and visualization
- Support real-time alerting and decision-making
- Integrate with humanitarian information systems

**Key steps:**
1. Configure network connectivity (WiFi, cellular, or Ethernet)
2. Obtain server credentials and API endpoint (from server administrator)
3. Enter server connection parameters in PtBox (URL, authentication, site ID)
4. Configure data transmission settings (frequency, retry logic, format)
5. Test connection and verify data upload
6. Confirm data appearing on server dashboard
7. Troubleshoot connection issues (authentication, network, server errors)
8. Configure upload schedule for operational monitoring

**Quality criteria:**
- Network connectivity stable (>95% uptime)
- Server uploads successful (>95% success rate)
- Data appearing on server in real-time or near-real-time
- Credentials secure and documented

**Common issues and resolutions:**
- Authentication failed: Verify credentials, check site registration
- Network timeout: Check internet connectivity, verify server URL
- Server error: Contact server administrator, review data format
- Incorrect values on server: Check unit conversion, verify transformation and cross-section configuration

**Integration with operational workflow:**
- PtBox now autonomous: Measures, processes, and uploads data without manual intervention
- Server provides access for decision-makers (no field visits required for data)
- Alerts notify stakeholders of critical conditions (flood warnings, equipment failures)
- Historical data supports analysis, reporting, and planning

**Next step:**
With server integration complete, proceed to Section 10.5: Automated Collection and Upload to configure fully autonomous operational monitoring.

---

**References:**
- Section 8: Equipment Installation (network infrastructure setup)
- Section 10.5: Automated Collection and Upload (final configuration step)
- LiveORC Server documentation (provided by server administrator)
