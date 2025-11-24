# 7.3 Network and Internet Connectivity

Network connectivity enables remote data transmission, system monitoring, and configuration updates. This section guides you through connectivity options, requirements, and implementation strategies for OpenRiverCam deployments.

## Understanding Connectivity Requirements

OpenRiverCam can operate in various connectivity modes, from continuous internet connection to fully offline operation with periodic data collection.

### Data Transmission Needs

OpenRiverCam data transmission requirements vary substantially based on the type of data transmitted and measurement frequency. Typical data volumes include raw video frames (1-5 MB per measurement), processed results including velocities and discharge estimates (10-50 KB per measurement), system status and diagnostic information (5-10 KB per transmission), and configuration updates (100-500 KB per update). Measurement frequency substantially impacts total data volumes, with hourly measurements requiring 50-150 MB per day when images are transmitted, daily measurements consuming 2-5 MB per day with images, and results-only transmission (without images) requiring only 500 KB to 2 MB daily. The critical consideration in network planning is that bandwidth and cost requirements depend heavily on whether raw video frames are transmitted to the cloud for processing, or only processed results are sent after local computation (Le Coz et al., 2016).

### Real-Time vs. Batch Transmission

**Real-time transmission** (recommended where bandwidth available):
- Measurements processed and transmitted immediately
- Enables real-time monitoring dashboards
- Allows prompt detection of issues
- Higher bandwidth and reliability requirements

**Batch transmission** (suitable for limited connectivity):
- Measurements stored locally
- Transmitted periodically (hourly, daily, or on-demand)
- Reduces connectivity requirements
- Introduces delay in data availability

**Offline operation** (fallback mode):
- Measurements stored locally only
- Data retrieved during maintenance visits
- No connectivity required
- Maximum delay in data availability

### Remote Access Requirements

Remote system access enables:
- Configuration changes without site visits
- Troubleshooting and diagnostics
- Software updates
- Camera view adjustments

**Access options**:
- VPN connection to system (most secure)
- SSH access via public IP or dynamic DNS
- Cloud-based management platform
- No remote access (site visits only)

## Cellular Network Connectivity

Cellular (mobile network) connectivity is the most common solution for OpenRiverCam deployments, offering good balance of coverage, cost, and reliability.

### Cellular Technology Options

**4G LTE** (preferred):
- Widely available in most regions
- Sufficient bandwidth for all transmission modes
- Typical speeds: 5-50 Mbps download, 2-10 Mbps upload
- Suitable for: Real-time transmission including images

**3G HSPA** (acceptable):
- Available in areas without 4G coverage
- Sufficient for results-only or batch transmission
- Typical speeds: 1-5 Mbps download, 0.5-2 Mbps upload
- Suitable for: Batch transmission, results-only mode

**2G GPRS/EDGE** (minimal):
- Legacy networks being phased out in many regions
- Sufficient only for results-only transmission
- Typical speeds: 50-200 Kbps
- Suitable for: Emergency fallback, results-only transmission

### Signal Strength Assessment

Signal strength at the installation site critically affects reliability:

**Measurement method**:
1. Visit site with mobile phone using intended network carrier
2. Test at proposed camera mounting height (signal improves with elevation)
3. Use network testing apps to measure signal strength
4. Test at different times of day (networks can be congested)

**Signal quality indicators**:
- Excellent (>-70 dBm): Reliable 4G, real-time transmission feasible
- Good (-70 to -85 dBm): Adequate 4G, suitable for most applications
- Fair (-85 to -100 dBm): Marginal 4G, may drop to 3G, batch transmission recommended
- Poor (<-100 dBm): Unreliable, consider alternative connectivity or offline operation

**Improvement options for weak signal**:
- External antenna mounted at camera height or higher
- Use carrier with best coverage in area
- Higher-gain directional antenna pointed at nearest tower
- Consider cellular repeater/booster (200-500 USD additional cost)

### Cellular Hardware Selection

**USB cellular modems** (most common):
- Advantages: Simple installation, low power consumption, widely available
- Typical cost: 50-150 USD
- Recommended for: Standard installations with good signal
- Example models: Huawei E3372, ZTE MF823, Quectel EC25

**Cellular routers**:
- Advantages: Better antenna options, more robust, advanced features
- Typical cost: 100-300 USD
- Recommended for: Challenging signal environments, multiple devices
- Example models: Teltonika RUT240, Digi TransPort, Sierra Wireless

**External antennas**:
- Omnidirectional (5-8 dBi gain): 30-60 USD, suitable for moderate signal
- Directional (10-20 dBi gain): 60-150 USD, suitable for weak signal areas
- MIMO (multiple antenna): Best performance for 4G, 80-200 USD

### Data Plans and Costs

Cellular connectivity requires a data plan from a mobile network operator:

**Plan selection considerations**:
- Data volume requirements (calculated above)
- Prepaid vs. postpaid options
- Contract length and flexibility
- Coverage in deployment area
- Roaming if applicable

**Typical costs** (vary significantly by region):
- Prepaid data (1-5 GB/month): 5-20 USD/month
- Postpaid unlimited: 20-50 USD/month
- IoT-specific plans (lower data volumes): 3-15 USD/month
- Machine-to-machine (M2M) plans: 5-25 USD/month

**Cost optimization strategies**:
- Transmit results only (not images) to minimize data
- Use batch transmission to reduce overhead
- Select plan matching actual data volume requirements
- Consider IoT/M2M plans if available (often cheaper than consumer plans)
- Evaluate multi-SIM plans if deploying multiple stations

### SIM Card Management

**Procurement**:
- Purchase locally to avoid roaming charges
- Verify network coverage in deployment area before purchasing
- Register SIM card as required by local regulations
- Test connectivity before site installation

**Configuration**:
- Record SIM card phone number and ICCID
- Configure correct APN (Access Point Name) settings for carrier
- Disable unnecessary services (voicemail, SMS notifications)
- Set up data alerts if available

**Ongoing management**:
- Monitor data usage to avoid overage charges
- Maintain SIM card balance (prepaid plans)
- Renew contracts before expiration
- Keep backup SIM card available for troubleshooting

## WiFi Connectivity

WiFi connectivity is suitable when reliable internet access is available nearby, such as at research stations, offices, or community facilities.

### WiFi Implementation Requirements

**Access point proximity**:
- Standard WiFi range: 50-100 meters outdoors (line of sight)
- Extended with directional antennas: 200-500 meters
- Physical obstacles (buildings, vegetation) significantly reduce range

**Network configuration**:
- Stable internet connection at access point
- Static IP or dynamic DNS for remote access
- Port forwarding configured if needed
- Network security (WPA2/WPA3 encryption)

**Hardware requirements**:
- WiFi adapter compatible with OpenRiverCam system (typically USB)
- External antenna for extended range (if needed)
- Weatherproof cable glands for antenna cables

**Cost estimate**:
- Standard USB WiFi adapter: 15-40 USD
- Long-range WiFi bridge: 80-200 USD per pair
- Directional antennas: 50-150 USD

### Long-Range WiFi Solutions

For distances beyond standard WiFi range:

**WiFi bridge systems**:
- Point-to-point wireless links
- Distances: 500 meters to 5+ kilometers (line of sight required)
- Examples: Ubiquiti NanoStation, TP-Link CPE series
- Cost: 100-300 USD per pair

**Implementation**:
1. One unit at internet access point (AP mode)
2. Second unit at camera location (Station/Client mode)
3. Both units require power and mounting
4. Alignment critical for maximum performance

**Advantages**:
- No ongoing service costs
- High bandwidth available
- Full network access for remote management

**Limitations**:
- Requires line of sight
- Weather sensitivity (rain, fog attenuate signal)
- Both ends require power and maintenance
- Permission needed for equipment at access point

## Satellite Connectivity

Satellite connectivity provides coverage in extremely remote locations where terrestrial options are unavailable, though at significantly higher cost.

### Satellite Technology Options

**Low Earth Orbit (LEO) constellations** (Starlink, OneWeb):
- Advantages: Lower latency, higher bandwidth, improving coverage
- Typical speeds: 50-200 Mbps
- Cost: 100-150 USD/month service + 500-600 USD equipment
- Availability: Expanding globally, check coverage maps

**Geostationary satellite** (traditional satellite internet):
- Advantages: Established coverage, various service tiers available
- Typical speeds: 1-25 Mbps
- Cost: 50-200 USD/month service + 300-1,000 USD equipment
- Availability: Near-global coverage

**Satellite M2M/IoT services** (Iridium, Globalstar, Orbcomm):
- Advantages: Lower cost for low data volumes, true global coverage
- Typical speeds: Very limited (2-10 Kbps)
- Cost: 20-100 USD/month service + 200-500 USD equipment
- Suitable for: Results-only transmission, emergency backup

### Satellite Implementation Considerations

**Physical requirements**:
- Clear view of sky (no obstructions)
- Precise antenna pointing (geostationary systems)
- Stable mounting platform
- Weatherproof installation

**Power requirements**:
- LEO systems: 50-100W (significant additional power system cost)
- Geostationary: 20-40W
- IoT services: 5-10W

**Cost-benefit analysis**:
- Only economical for truly remote locations
- Consider accessibility for maintenance vs. connectivity cost
- May be more cost-effective to deploy offline and retrieve data manually

**Recommendation**: Reserve satellite connectivity for high-priority monitoring in locations with no other options. For most humanitarian applications, cellular or offline operation is more practical.

## Offline Operation and Data Storage

OpenRiverCam systems can operate completely offline, storing data locally for periodic retrieval.

### Local Storage Configuration

**Storage capacity planning**:
- Processed results only: 500 MB - 2 GB per year
- Including video frames: 10-50 GB per year (depends on frequency)
- System logs and diagnostics: 100-500 MB per year

**Storage media options**:
- MicroSD card (built-in): Suitable for results-only or short-term storage
- USB flash drive: Easy data retrieval, 32-128 GB typical
- External hard drive: High capacity for image archiving, 500 GB - 2 TB
- Network-attached storage (if local network available)

**Storage management**:
- Automatic old file cleanup to prevent capacity exhaustion
- Data export in standard formats for easy retrieval
- Backup storage if long-term reliability critical

### Manual Data Retrieval Process

For offline deployments, plan regular data collection:

**Retrieval frequency options**:
- Weekly: Suitable for nearby sites, timely data availability
- Monthly: Common for remote sites, acceptable delay for most applications
- Quarterly: Minimal maintenance visits, significant data delay
- Event-based: Triggered by specific flow conditions or alerts

**Retrieval procedure**:
1. Visit site during scheduled maintenance
2. Connect laptop to system via local network or direct connection
3. Copy data files from storage to laptop
4. Verify data integrity (file sizes, date ranges)
5. Upload data to central database when internet available

**Offline operation advantages**:
- No connectivity costs
- No ongoing service dependencies
- Simple, reliable operation
- Suitable for budget-constrained deployments

**Offline operation limitations**:
- Delayed data availability
- Cannot detect issues remotely
- No remote system access
- Requires regular site visits

## Network Configuration and Security

Proper network configuration ensures reliable operation and protects systems from unauthorized access.

### Basic Network Setup

**IP address assignment**:
- DHCP (automatic): Simplest, suitable for most installations
- Static IP: Required for some remote access configurations
- Dynamic DNS: Maps changing IP address to fixed hostname

**Port configuration**:
- SSH access: Port 22 (or custom port for security)
- Web interface: Port 80/443 (HTTP/HTTPS)
- VPN: Port 1194 (OpenVPN) or others depending on solution
- Configure router/firewall port forwarding if needed

### Remote Access Security

Remote access introduces security risks that must be mitigated:

**Authentication**:
- Strong passwords (minimum 12 characters, mixed case, numbers, symbols)
- SSH key authentication (preferred over password)
- Disable default passwords on all equipment
- Change default usernames where possible

**Access restriction**:
- Limit access to specific IP addresses if possible
- Use VPN for remote access rather than direct internet exposure
- Disable unused services and ports
- Implement automatic blocking of repeated failed login attempts

**Regular security maintenance**:
- Update software regularly to patch vulnerabilities
- Review access logs for suspicious activity
- Rotate passwords periodically
- Disable accounts for departed personnel

### VPN Solutions

Virtual Private Networks (VPNs) provide secure remote access:

**Cloud-based VPN** (Zerotier, Tailscale):
- Advantages: Simple setup, no public IP required, manageable from dashboard
- Cost: Free for small deployments, 5-10 USD/month for larger
- Suitable for: Multiple remote sites, managed access

**Self-hosted VPN** (OpenVPN, WireGuard):
- Advantages: Full control, no third-party dependency, no ongoing cost
- Complexity: Requires technical configuration and maintenance
- Suitable for: Technical teams, high-security requirements

**Router-based VPN**:
- Advantages: Integrated with network hardware, professional features
- Cost: Included with some cellular routers
- Suitable for: Commercial-grade deployments

## Bandwidth Optimization Strategies

Limited or costly connectivity requires optimizing data transmission:

### Reduce Transmitted Data Volume

**Transmit results only**:
- Send discharge values, velocities, and metadata only
- Store video frames locally for later retrieval if needed
- Reduces bandwidth by 90-95% compared to full transmission

**Image compression**:
- Reduce image resolution before transmission
- Use efficient compression (JPEG quality 70-85)
- Transmit keyframes only (not all captured frames)

**Scheduled transmission**:
- Batch multiple measurements before transmission
- Transmit during off-peak hours if rates vary by time
- Reduce transmission frequency for stable flow conditions

### Transmission Reliability

**Retry mechanisms**:
- Automatically retry failed transmissions
- Queue data locally if connectivity unavailable
- Prioritize recent data over backfill

**Compression**:
- Compress data files before transmission
- Use efficient protocols (MQTT more efficient than HTTP for IoT)

**Progressive transmission**:
- Send critical data first (current discharge value)
- Send detailed data (images, diagnostics) as bandwidth available
- Ensures essential information transmitted even with interruptions

## Troubleshooting Connectivity Issues

Common network problems and resolution steps:

**Cannot establish connection**:
1. Verify physical connectivity (cables, antenna connections)
2. Check signal strength (cellular) or link quality (WiFi)
3. Verify SIM card active and data plan valid
4. Check APN settings (cellular) or WiFi credentials
5. Restart modem/router and system

**Connection established but no data transmission**:
1. Verify internet connectivity (can system reach external servers?)
2. Check firewall rules and port configurations
3. Verify data transmission service running
4. Review system logs for error messages
5. Test with manual data transmission

**Intermittent connectivity**:
1. Monitor signal strength over time (may vary with weather, network load)
2. Check for overheating in cellular modem
3. Verify power supply adequate (modems can consume significant power)
4. Consider external antenna if signal marginal
5. Evaluate alternative carriers or connectivity methods

**High data usage**:
1. Review transmitted data volume by type
2. Verify image compression settings appropriate
3. Check for unnecessary service activity (updates, logs)
4. Confirm transmission frequency matches requirements
5. Consider switching to results-only transmission

## Connectivity Planning Checklist

Before finalizing connectivity approach:

- [ ] Determine required data transmission frequency and volume
- [ ] Decide whether to transmit images or results-only
- [ ] Assess cellular signal strength at installation site and height
- [ ] Select appropriate cellular carrier and data plan
- [ ] Procure and test cellular modem or alternative hardware
- [ ] Configure network settings (APN, IP addressing)
- [ ] Plan remote access method (VPN, direct SSH, none)
- [ ] Implement security measures (strong passwords, key authentication)
- [ ] Test connectivity before site deployment
- [ ] Document configuration for troubleshooting
- [ ] Plan fallback to offline operation if connectivity unreliable
- [ ] Budget for ongoing connectivity costs
- [ ] Determine data retrieval procedure if offline operation
- [ ] Plan connectivity monitoring and troubleshooting procedures

## Cost Comparison Summary

Typical costs for different connectivity approaches:

**Cellular (4G)**:
- Initial: 100-300 USD (modem, antenna, SIM)
- Ongoing: 10-30 USD/month (data plan)
- Best for: Most remote deployments with cellular coverage

**WiFi (existing access point)**:
- Initial: 15-40 USD (WiFi adapter)
- Ongoing: 0 USD (using existing internet)
- Best for: Installations near facilities with internet

**Long-range WiFi**:
- Initial: 200-500 USD (bridge equipment, mounting)
- Ongoing: 0 USD (one-time investment)
- Best for: Medium-distance from internet access point

**Satellite (LEO)**:
- Initial: 500-700 USD (terminal, mounting)
- Ongoing: 100-150 USD/month (service)
- Best for: Extremely remote locations, high priority

**Offline operation**:
- Initial: 20-100 USD (storage media)
- Ongoing: 0 USD (no connectivity costs)
- Best for: Budget-constrained, accessible locations

## Next Steps

With connectivity planning complete, proceed to:

- **Section 7.4**: Assess security requirements and protective measures
- **Chapter 8**: Execute physical installation and system configuration

Appropriate connectivity selection ensures your OpenRiverCam deployment delivers data with the frequency and reliability required for your application, while remaining within budget constraints.
