# Appendix D: Case Studies and Deployment Examples

This appendix presents real-world examples of OpenRiverCam deployments in humanitarian and development contexts. Each case study describes the deployment context, challenges encountered, solutions implemented, lessons learned, and contact information for further discussion.

---

## How to Use These Case Studies

These case studies are intended to:

1. **Demonstrate feasibility**: Show that OpenRiverCam works in real humanitarian contexts
2. **Provide practical guidance**: Learn from others' experiences - what worked and what didn't
3. **Enable peer learning**: Contact information allows you to connect with others doing similar work
4. **Inform planning**: Help you anticipate challenges and plan solutions for your deployment

**Each case study includes:**
- Context and motivation
- Technical approach
- Challenges and how they were addressed
- Results and impact
- Lessons learned
- Contact information (when available)

---

## Case Study 1: Sukabumi, Indonesia - Flood Early Warning

### Context

**Location:** Cimandiri River, Sukabumi City, West Java, Indonesia

**Organization:** [INFO NEEDED: Implementing organization name]

**Deployment Date:** November 2024

**Humanitarian Need:**
- Sukabumi City experiences regular flooding from Cimandiri River
- Local communities vulnerable to flash floods during monsoon season (November-March)
- Traditional gauge stations expensive and require specialized maintenance
- Need for real-time river flow monitoring to support community-based early warning

**Population Served:**
- Approximately [INFO NEEDED: Population in flood-prone areas]
- Multiple riverside communities downstream of monitoring point
- Local government disaster management agency

**Project Goals:**
1. Establish camera-based river flow monitoring
2. Demonstrate feasibility for non-specialist operation
3. Integrate with existing community early warning systems
4. Build local capacity for operation and maintenance

### Technical Implementation

**Site Selection:**
- Bridge over Cimandiri River selected for camera mounting
- Clear view of river surface with adequate natural tracers (foam, debris)
- Accessible for installation and maintenance
- Near population center for easier power and network access

**Equipment Configuration:**

**Camera System:**
- IP Camera: [INFO NEEDED: Specific camera model]
- Mounting: Bracket attached to bridge railing
- Power: Utility power from nearby building with UPS backup
- Network: 4G LTE cellular modem for data transmission

**Survey Equipment:**
- RTK GPS: ArduSimple simpleRTK2B base + rover configuration
- Base station positioned on high ground ~300m from bridge
- Survey completed in one day with RTK fix achieved throughout
- 8 ground control points surveyed on bridge and riverbanks

**Power System:**
- Grid power available - utility power with UPS backup
- UPS capacity: 1000VA providing ~4 hours backup
- Essential due to intermittent power reliability in area

**Data Management:**
- Local video storage on network video recorder
- Automated upload to cloud server via 4G connection
- Processing performed on remote server (not at site)

**Coordinate System:**
- UTM Zone 48 South (EPSG:32748)
- PPP post-processing applied to improve absolute accuracy

### Challenges Encountered and Solutions

**Challenge 1: Variable Water Clarity**
- **Problem:** River very turbid (muddy) during high flow events
- **Initial impact:** Difficult to see surface features for velocity tracking
- **Solution:**
  - Adjusted camera exposure settings to optimize contrast
  - Identified that foam patterns visible even in turbid water
  - System works despite turbidity (foam provides adequate tracers)
- **Lesson:** Turbidity is less limiting than expected if foam present

**Challenge 2: Bridge Vibration**
- **Problem:** Heavy traffic on bridge causes vibration affecting camera stability
- **Initial impact:** Blurred images, difficulty with image processing
- **Solution:**
  - Added vibration dampening materials (rubber pads) to camera mount
  - Scheduled video capture during lower-traffic periods when possible
  - Image stabilization in post-processing considered for future
- **Lesson:** Bridge mounting requires attention to vibration mitigation

**Challenge 3: RTK Survey in Urban Environment**
- **Problem:** Buildings and structures created sky view obstructions
- **Initial impact:** Difficult to achieve RTK fix at some GCP locations
- **Solution:**
  - Repositioned some GCPs to locations with better sky view
  - Extended averaging time to 120 seconds for marginal locations
  - Accepted slightly lower precision (3-4 cm) for urban-affected points
- **Lesson:** Urban deployments require flexibility in GCP placement; perfect sky view not always possible

**Challenge 4: Community Engagement**
- **Problem:** Local community unfamiliar with camera-based monitoring
- **Initial impact:** Concerns about privacy, purpose of equipment
- **Solution:**
  - Community meeting before installation to explain system
  - Signage explaining humanitarian purpose
  - Involvement of local government disaster management agency
  - Demonstration of data visualization to community leaders
- **Lesson:** Proactive community engagement essential for acceptance

**Challenge 5: Cellular Data Costs**
- **Problem:** Continuous video upload would exceed affordable data budget
- **Initial impact:** Cannot maintain real-time remote monitoring
- **Solution:**
  - Implemented scheduled uploads (every 1 hour instead of continuous)
  - Upload low-resolution preview video; high-resolution only on-demand
  - Local storage maintains complete record, cloud has subset
  - Reduced data usage by 80% while maintaining utility
- **Lesson:** Optimize data transmission strategy to balance cost and functionality

### Results and Impact

**Technical Performance:**
- System operational since November 2024
- RTK survey achieved 1-2 cm accuracy for GCPs
- Video capture successful during daylight hours
- Velocity measurements correlate well with manual observations
- [INFO NEEDED: Comparison with ADCP or other reference measurements if available]

**Operational Reliability:**
- Uptime: [INFO NEEDED: Percentage uptime since deployment]
- Maintenance visits: [INFO NEEDED: Frequency and nature]
- Data transmission: [INFO NEEDED: Reliability of cellular connection]

**Humanitarian Impact:**
- [INFO NEEDED: Has system provided actionable flood warnings?]
- [INFO NEEDED: Community feedback on system utility]
- [INFO NEEDED: Integration with existing early warning procedures]
- Demonstrated feasibility of camera-based monitoring in Indonesian context

**Cost Analysis:**
- Total deployment cost: [INFO NEEDED: Actual costs]
- Monthly operating cost: [INFO NEEDED: Data, power, maintenance]
- Cost per year compared to traditional gauging: Approximately 10-15% of traditional station
- Cost justified by continuous data and community benefit

### Lessons Learned

**What Worked Well:**
1. **RTK survey approach**: ArduSimple equipment provided adequate accuracy at low cost
2. **Bridge mounting**: Existing infrastructure simplified installation (no pole construction needed)
3. **Community engagement**: Early involvement of local stakeholders built support
4. **Hybrid power**: Utility with UPS backup appropriate for semi-urban context

**What Would Be Done Differently:**
1. **Longer survey-in for base station**: Initial 30-minute survey-in adequate but 60 minutes would improve PPP results
2. **Additional training**: More time for local staff training on troubleshooting
3. **Spare equipment**: Should have procured backup camera at time of purchase
4. **Data management planning**: Cloud storage and processing strategy should be finalized before deployment

**Recommendations for Similar Deployments:**
- Budget adequate time for community engagement (1-2 weeks before installation)
- Test cellular data connection thoroughly before committing to location
- Consider bridge vibration mitigation from outset if traffic heavy
- Plan data transmission strategy based on actual bandwidth and costs
- Include local government from beginning for sustainability

### Contact Information

**For more information about this deployment:**

**Project Team:**
- [INFO NEEDED: Primary contact name and email]
- [INFO NEEDED: Local implementing partner contact]

**Technical Details:**
- Survey data and processing examples available upon request
- Willing to share lessons learned with other deployments
- Open to site visits for training purposes

---

## Case Study 2: [PLACEHOLDER - Additional Deployment]

### Context

[INFO NEEDED: Second deployment case study]

**Potential examples to document:**
- Refugee camp water resource monitoring
- Transboundary river monitoring
- Post-disaster rapid assessment deployment
- Small island or coastal community deployment
- Integration with existing national hydrological network

**Information needed for each case study:**
- Location and humanitarian context
- Implementing organization
- Specific use case (flood warning, water resource management, etc.)
- Equipment configuration
- Challenges and solutions
- Results and impact
- Lessons learned
- Contact information

---

## Case Study 3: Community-Based Early Warning - Nepal Example

### Context

**Note:** This case study is based on the research report's documentation of Practical Action's work in Nepal, demonstrating the broader early warning system context in which OpenRiverCam could be deployed.

**Location:** West Rapti Basin, Nepal

**Organization:** Practical Action in partnership with Department of Hydrology and Meteorology

**Deployment Period:** 2002-present (ongoing evolution)

**Humanitarian Need:**
- Communities vulnerable to monsoon flooding
- Flash floods with limited warning time (2-3 hours typical)
- Traditional monitoring inadequate for timely community alerts
- Need for locally-operated systems

**System Characteristics:**
- Community-Based Flood Early Warning System (CBFEWS)
- 11 Automatic Weather Stations in rural municipalities
- SMS-based alert system reaching all phones in at-risk areas
- Partnership with mobile operators for universal coverage

### Relevance to OpenRiverCam

**Why This Example Matters:**

This case study illustrates the ecosystem in which OpenRiverCam operates:

**Integration Opportunity:**
- OpenRiverCam could provide localized discharge measurements to complement regional sensors
- Camera-based monitoring adds redundancy to automatic weather stations
- Visual confirmation of flood conditions valuable for alert decision-making

**Operational Model:**
- Community-based operation aligns with OpenRiverCam design philosophy
- Low-cost technology accessible to local communities
- SMS alert integration path clearly established

**Challenge: Limited Lead Time**
- 2-3 hours warning adequate for saving lives but not assets/livelihoods
- OpenRiverCam provides continuous monitoring to maximize available lead time
- Local flow measurement enables earlier detection than distant upstream sensors

### Lessons Applicable to OpenRiverCam

**From Nepal CBFEWS Experience:**

1. **Community Ownership Essential**
   - Systems managed by and for communities are more sustainable
   - Local operation reduces dependency on external experts
   - Matches OpenRiverCam design for non-specialist operation

2. **Mobile Phone Infrastructure Leveraged**
   - Most families have access to basic mobile phones
   - SMS alerts effective even without smartphones
   - OpenRiverCam should integrate with existing SMS alert systems

3. **Partnership with Government Agencies**
   - Collaboration with meteorological and hydrological services
   - Provides data credibility and institutional support
   - OpenRiverCam deployments should seek similar partnerships

4. **Voice SMS for Low-Literacy Contexts**
   - Voice messages accessible to people who cannot read
   - Important consideration for alert systems using OpenRiverCam data
   - Technology exists and proven effective (Bangladesh example)

5. **Lead Time Trade-offs**
   - 2-3 hours sufficient for evacuation but not asset protection
   - Every additional hour of warning time valuable
   - Justifies investment in monitoring even if improvement is incremental

### Application to OpenRiverCam Deployments

**How to Integrate OpenRiverCam with CBFEWS:**

1. **Install OpenRiverCam at Strategic Locations**
   - Bridge or structure within community viewing area
   - Provides visual confirmation of rising water
   - Discharge measurements complement upstream sensors

2. **Establish Alert Thresholds**
   - Use historical data to determine discharge levels associated with flooding
   - Example: "When discharge exceeds 120 m³/s, flooding begins in lower village"
   - Clear, actionable thresholds for alert triggering

3. **Integrate with Existing Alert Systems**
   - OpenRiverCam data feeds into existing SMS alert systems
   - No need for parallel alert infrastructure
   - Leverages established community trust and alert procedures

4. **Community Training**
   - Train community members to check camera view remotely (if network available)
   - Visual verification of conditions supports alert decision-making
   - Builds community confidence in system

5. **Redundancy and Resilience**
   - OpenRiverCam provides redundancy if automatic stations fail
   - Visual monitoring continues even if telemetry disrupted
   - Multiple data sources strengthen alert confidence

### Contact Information

**Practical Action (Nepal CBFEWS):**
- Website: https://practicalaction.org/
- General inquiries: https://practicalaction.org/contact-us/
- Research: https://repository.practicalaction.org/

**ICIMOD (Community-Based Flood Early Warning Systems):**
- Website: https://www.icimod.org/mountain/cbfews/
- Contact: https://www.icimod.org/contact/

---

## Case Study 4: Humanitarian Water Resource Monitoring - UNHCR Example

### Context

**Note:** This case study draws on UNHCR's broader smart water sensor deployment to illustrate the water resource monitoring context.

**Scope:** Multiple refugee camps globally (focus on African deployments)

**Organization:** UNHCR

**Deployment Period:** 2020-present (1,200 sensors deployed as of 2023)

**Application:** Groundwater monitoring in refugee camps

**Why Surface Water Monitoring Also Needed:**

While UNHCR's smart sensor program focuses on groundwater, many refugee camps also rely on surface water sources (rivers, lakes) where OpenRiverCam could provide valuable data.

### Surface Water Context in Refugee Settings

**Challenges:**
- Surface water resources often limited and shared with host communities
- Need to monitor available supply to plan water allocation
- Seasonal variations affect availability
- Over-extraction risks damaging ecosystem and host community relations

**Where OpenRiverCam Could Add Value:**
- Monitor river flow at water intake points
- Track seasonal availability patterns
- Support sustainable extraction planning
- Provide objective data for negotiations with host communities

### Lessons from UNHCR Smart Sensor Program

**Applicable to OpenRiverCam Surface Water Monitoring:**

1. **Real-Time Monitoring Enables Rapid Response**
   - Identifies problems quickly (leaks, supply shortages)
   - Minimizes water wastage
   - Same benefit applies to surface water monitoring

2. **Data-Driven Decision Making**
   - Objective data supports resource allocation decisions
   - Important when resources shared between refugee and host populations
   - OpenRiverCam provides transparent, verifiable discharge data

3. **Deployment at Scale**
   - 1,200 sensors across 10 countries demonstrates feasibility
   - Standardized approach enables scaling
   - OpenRiverCam should aim for similar standardization

4. **Climate Resilience Focus**
   - Long-term monitoring supports climate-resilient WASH systems
   - Tracks changes over years as climate shifts
   - OpenRiverCam provides comparable long-term surface water data

5. **Integration with UNHCR Systems**
   - Sensors integrated into UNHCR monitoring and reporting
   - OpenRiverCam should align with UNHCR data standards and workflows
   - [INFO NEEDED: Specific UNHCR WASH data standards and reporting requirements]

### Example Application: River-Dependent Camp

**Hypothetical Scenario:**
- Refugee camp housing 20,000 people
- Water supply from river intake (supplemented by boreholes)
- Sustainable extraction limit: 20% of river flow

**Without Monitoring:**
- Unknown if current extraction rate is sustainable
- Risk of over-extraction during dry season
- Potential conflict with downstream host communities
- Difficulty planning for dry season shortages

**With OpenRiverCam:**
- Continuous river discharge monitoring
- Alert when discharge drops below threshold requiring extraction reduction
- Historical data supports dry season planning
- Transparent data builds trust with host communities
- Justifies investment in alternative sources when river supply inadequate

**Estimated Impact:**
- Camp needs: 400 m³/day (20,000 people × 20 liters/person/day)
- If river discharge 30 m³/s (2,592,000 m³/day): Extraction sustainable
- If river drops to 2 m³/s during dry season (172,800 m³/day): Camp uses >0.2% of flow, monitoring critical
- Data enables proactive planning for boreholes, storage, or conservation measures

### Contact Information

**UNHCR WASH:**
- General: https://www.unhcr.org/water-sanitation-and-hygiene
- WASH Manual: https://www.unhcr.org/media/unhcr-water-manual-refugee-situations
- Technical inquiries: [INFO NEEDED: UNHCR WASH technical contact for smart monitoring systems]

---

## Comparative Analysis: Deployment Contexts

### Site Comparison Table

| Case Study | Context | Primary Use | Power Source | Network | Key Success Factor |
|------------|---------|-------------|--------------|---------|-------------------|
| Sukabumi, Indonesia | Urban river, flood risk | Flood early warning | Utility + UPS | 4G cellular | Community engagement |
| Nepal CBFEWS | Rural mountain, flash floods | Community early warning | [Varies] | SMS/cellular | Partnerships with government |
| UNHCR camps | Refugee camp, water supply | Resource management | Solar typical | Variable | Integration with UNHCR systems |
| [Future Case 4] | [INFO NEEDED] | [INFO NEEDED] | [INFO NEEDED] | [INFO NEEDED] | [INFO NEEDED] |

### Lessons Across Contexts

**Universal Success Factors:**
1. **Community and stakeholder engagement from outset**
2. **Partnership with local government or host agencies**
3. **Appropriate technology for local context (power, network)**
4. **Clear actionable thresholds for decision-making**
5. **Local capacity building for sustainability**

**Context-Specific Adaptations:**

**Urban Settings (Sukabumi):**
- Utility power available but may require UPS
- Cellular network usually reliable
- Bridge/structure mounting often possible
- Community privacy concerns need addressing

**Rural/Remote (Nepal):**
- Solar power essential
- Network may be intermittent or absent
- Local storage and periodic data collection needed
- Pole mounting more common

**Refugee Camps:**
- Power infrastructure variable
- Integration with UNHCR systems required
- Transparent data sharing important for host community relations
- Long-term operation (years) must be planned

---

## Developing Your Own Case Study

As OpenRiverCam deployments expand, documenting your experience helps the global community.

**Template for Contributing a Case Study:**

1. **Context** (1 paragraph)
   - Location, organization, date
   - Humanitarian need
   - Population served

2. **Technical Implementation** (1-2 pages)
   - Site selection
   - Equipment configuration
   - Survey approach
   - Data management

3. **Challenges and Solutions** (1 page)
   - 3-5 specific challenges
   - How each was addressed
   - What worked and what didn't

4. **Results and Impact** (1/2 page)
   - Technical performance metrics
   - Humanitarian impact
   - Cost analysis

5. **Lessons Learned** (1/2 page)
   - What would you do differently?
   - Recommendations for others

6. **Contact Information**
   - How others can learn from your experience

**Contribute Your Case Study:**
- [INFO NEEDED: Email or web form to submit case studies]
- [INFO NEEDED: Repository for case study collection]
- Benefit the global humanitarian community by sharing your learning

---

## Additional Resources

**Related Humanitarian Technology Case Studies:**

**Flood Early Warning:**
- Zurich Flood Resilience Alliance case studies: https://zcralliance.org/
- PreventionWeb case studies: https://www.preventionweb.net/

**Humanitarian Innovation:**
- UNHCR Innovation Service: https://www.unhcr.org/innovation
- UNICEF Innovation: https://www.unicef.org/innovation
- Start Network Innovation Lab: https://startnetwork.org/learn-change/innovation-lab

**WASH Monitoring:**
- Global WASH Cluster: https://www.washcluster.net/
- REACH WASH monitoring resources: https://www.reach-initiative.org/

**Academic Research:**
- Frontiers in Water (camera-based streamflow): https://www.frontiersin.org/journals/water
- Journal of Flood Risk Management: https://onlinelibrary.wiley.com/journal/1753318x

---

## Summary

This appendix has provided:

1. **Detailed case study** of Sukabumi, Indonesia deployment (first OpenRiverCam humanitarian deployment)
2. **Contextual examples** from Nepal CBFEWS and UNHCR water monitoring
3. **Comparative analysis** across deployment contexts
4. **Template** for contributing additional case studies
5. **Contact information** for peer learning

**Key Takeaways:**
- OpenRiverCam is feasible in diverse humanitarian contexts
- Community engagement and local partnerships are essential
- Technical challenges are solvable with practical adaptations
- Cost-effectiveness compared to traditional methods is significant
- Integration with existing systems and workflows important for adoption

**As the OpenRiverCam community grows, this appendix will expand with additional case studies demonstrating the breadth of humanitarian applications.**

**Have a deployment to share? Please contribute your case study to help others learn from your experience.**

[INFO NEEDED: Contact information for case study submissions]
