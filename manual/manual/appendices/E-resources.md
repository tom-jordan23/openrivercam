# Appendix E: Resources and References

This appendix provides links to additional learning materials, software downloads, technical support contacts, community forums, and relevant standards and guidelines. All resources are organized by category for easy reference.

---

## 1. OpenRiverCam Software and Documentation

### 1.1 Core Software

**pyOpenRiverCam (pyorc) - Main Processing Library**
- GitHub Repository: https://github.com/localdevices/pyorc
- Documentation: https://localdevices.github.io/pyorc/
- PyPI Package: https://pypi.org/project/pyopenrivercam/
- License: AGPLv3 (open source)
- Latest Release: [Check GitHub for current version]
- Requirements: Python 3.8 or later

**What it does:**
- Large-Scale Particle Image Velocimetry (LSPIV)
- Particle Tracking Velocimetry (PTV)
- Dense Optical Flow analysis
- Rating curve establishment
- Discharge calculation

**Installation:**
```bash
pip install pyopenrivercam
```

**Key Dependencies:**
- OpenPIV (particle image velocimetry library)
- OpenCV (computer vision library)
- NumPy, SciPy (scientific computing)
- Matplotlib (visualization)

### 1.2 Official Documentation

**pyOpenRiverCam Documentation:**
- Main documentation: https://localdevices.github.io/pyorc/
- Tutorials and examples included
- API reference
- Contribution guidelines

**GitHub Wiki and Issues:**
- Community discussions: GitHub Issues tab
- Feature requests: GitHub Issues with enhancement label
- Bug reports: GitHub Issues with bug label

### 1.3 Training Videos and Tutorials

**[INFO NEEDED: Video Tutorial Library]**

Planned video content (placeholders):
- Introduction to OpenRiverCam (10 minutes)
- Site Selection Walkthrough (15 minutes)
- RTK Survey Training (30 minutes)
- Camera Installation and Setup (20 minutes)
- Software Configuration Tutorial (25 minutes)
- Processing Your First Video (20 minutes)
- Troubleshooting Common Issues (15 minutes)

**YouTube Channel:** [INFO NEEDED: Official OpenRiverCam YouTube channel if available]

**Online Training Platform:** [INFO NEEDED: Any e-learning platform with OpenRiverCam courses]

---

## 2. Survey and Geospatial Resources

### 2.1 RTK GPS Software

**RTKLIB - GNSS Processing Tools**
- Website: https://www.rtklib.com/
- GitHub: https://github.com/tomojitakasu/RTKLIB
- License: BSD 2-Clause (open source)
- Tools included:
  - RTKCONV: UBX to RINEX conversion
  - CONVBIN: Command-line conversion tool
  - RTKPOST: Post-processing
  - RTKPLOT: Visualization

**Download:**
- Windows: https://www.rtklib.com/prog/rtklib_2.4.3_b34.zip
- Source code: GitHub repository

**u-center (u-blox Configuration Software)**
- Website: https://www.u-blox.com/en/product/u-center
- Platform: Windows only
- Purpose: Configure u-blox receivers (ArduSimple, etc.)
- Required for base station setup
- Free download (registration required)

**GNSS Master (Android App)**
- Google Play Store: Search "GNSS Master"
- Developer: Androidkosmos
- Purpose: Provide RTK position as mock location to Android apps
- Required for SW Maps integration
- Free app

**SW Maps (Field Data Collection)**
- Website: https://www.swmaps.com/
- Platforms: Android, iOS
- Free version available (limited features)
- Pro version: $50/year (additional features, layers)
- Purpose: Collect RTK survey points with attributes
- Alternative: QField (free, open-source)

### 2.2 PPP Processing Services

**AUSPOS (Recommended for Indonesia/Asia-Pacific)**
- Website: https://www.ga.gov.au/auspos
- Provider: Geoscience Australia
- Coverage: Global
- Cost: Free
- Processing time: 2-24 hours
- Accuracy: 2-10 cm
- Input: RINEX observation files
- Output: Coordinates in various formats (WGS84, UTM, etc.)

**How to use:**
1. Convert UBX to RINEX using CONVBIN
2. Upload RINEX file to AUSPOS website
3. Enter email and antenna information
4. Wait for results email (usually within 4 hours)
5. Apply corrections to survey data

**GAPS (Alternative PPP Service)**
- Website: https://webapp.csrs-scrs.nrcan-rncan.gc.ca/geod/tools-outils/ppp.php
- Provider: Natural Resources Canada
- Coverage: Global
- Cost: Free
- Similar process to AUSPOS

**OPUS (US-Based Service)**
- Website: https://geodesy.noaa.gov/OPUS/
- Provider: NOAA National Geodetic Survey
- Coverage: Best for USA, works globally
- Cost: Free
- Shorter session times acceptable

### 2.3 GIS Software

**QGIS (Recommended)**
- Website: https://qgis.org/
- Download: https://qgis.org/en/site/forusers/download.html
- License: GNU General Public License (free, open source)
- Platforms: Windows, Mac, Linux
- Purpose: View, edit, and process survey data
- Required for PPP corrections workflow

**Key QGIS Plugins for OpenRiverCam:**
- Field Calculator (built-in): Apply PPP corrections
- Point sampling tool: Extract elevations
- Profile tool: Visualize cross-sections
- QuickMapServices: Add background imagery

**Alternatives:**
- ArcGIS (commercial, expensive, powerful)
- GRASS GIS (free, open source, steeper learning curve)
- SAGA GIS (free, open source, good for terrain analysis)

### 2.4 Coordinate System Resources

**EPSG Geodetic Parameter Dataset**
- Website: https://epsg.org/
- Search tool: https://epsg.io/
- Purpose: Look up coordinate system codes
- Example: Search "UTM Zone 48 South" → EPSG:32748

**Coordinate System Converters:**
- PROJ: https://proj.org/ (command-line tool, widely used)
- Online converter: https://mygeodata.cloud/cs2cs/
- QGIS built-in reprojection tools

---

## 3. Humanitarian and Technical Standards

### 3.1 Hydrological Standards

**World Meteorological Organization (WMO)**
- Guide to Hydrological Practices (WMO-No. 168)
  - https://library.wmo.int/index.php?lvl=notice_display&id=16793
  - Volume I: Hydrology – From Measurement to Hydrological Information
  - Volume II: Management of Water Resources and Application of Hydrological Practices
- Technical Regulations (WMO-No. 49)
- Standards for river flow measurement

**ISO Standards for Hydrometry:**
- ISO 748: Measurement of liquid flow in open channels - Velocity-area methods
- ISO 1100 series: Liquid flow measurement in open channels
- Available through: https://www.iso.org/ (purchase required)

**US Geological Survey (USGS) Techniques and Methods:**
- USGS Techniques and Methods 3-A8: Discharge Measurements at Gaging Stations
- Available free: https://pubs.usgs.gov/tm/tm3-a8/
- Best practices for traditional flow measurement
- Useful context for camera-based methods

### 3.2 GNSS/Survey Standards

**Federal Geographic Data Committee (US)**
- Geospatial Positioning Accuracy Standards
- https://www.fgdc.gov/standards/projects/accuracy/
- Part 2: Standards for Geodetic Networks
- Relevant for RTK survey quality requirements

**International Federation of Surveyors (FIG)**
- Publications: https://www.fig.net/resources/publications/
- Best practices for GPS/GNSS surveying
- Many freely available publications

### 3.3 Humanitarian Standards

**Sphere Standards (WASH)**
- Sphere Handbook: https://spherestandards.org/handbook/
- Water Supply Standard 1.1: Access and water quantity
  - Minimum 15 liters per person per day (survival)
  - Target 20 liters per person per day (minimum)
- Relevant for understanding water resource monitoring in humanitarian contexts

**Global WASH Cluster**
- Website: https://www.washcluster.net/
- Resources: https://www.washcluster.net/resources
- Monitoring and accountability frameworks
- Data standards for WASH reporting

**UNHCR WASH Manual**
- UNHCR Water Manual for Refugee Situations
- https://www.unhcr.org/media/unhcr-water-manual-refugee-situations
- Comprehensive guidance on water supply in refugee contexts
- Chapter on water resource assessment and monitoring

---

## 4. Training and Capacity Building

### 4.1 Hydrology Training

**HydroLearn - CUAHSI**
- Website: https://www.hydrolearn.org/
- Free online hydrology teaching resources
- Modules on streamflow measurement, rating curves, hydrographs
- Suitable for self-study

**UNESCO-IHP Training Resources**
- International Hydrological Programme: https://www.unesco.org/en/ihp
- Free educational materials
- Focus on water resource management

**USGS Water Science School**
- Website: https://www.usgs.gov/special-topics/water-science-school
- Simple explanations of hydrological concepts
- Good for non-specialists learning basics

### 4.2 GNSS/RTK Training

**UNAVCO Education and Training**
- Website: https://www.unavco.org/education/education.html
- Short courses on GNSS
- Focus on geodetic applications
- Some online materials freely available

**Trimble/Leica Training (Commercial)**
- Professional training courses
- Usually tied to equipment purchase
- Comprehensive but expensive

**YouTube Channels:**
- ArduSimple RTK tutorials: https://www.youtube.com/c/ArduSimple
- Emlid tutorials: https://www.youtube.com/c/EMLIDtech
- Community tutorials (search "RTK GPS tutorial")

### 4.3 GIS Training

**QGIS Training Materials**
- Official training manual: https://docs.qgis.org/3.28/en/docs/training_manual/
- Free, comprehensive
- Step-by-step tutorials

**OpenGeoLab YouTube Channel**
- Practical QGIS tutorials
- Beginner to advanced
- Free

### 4.4 Humanitarian IM Training

**MapAction Training**
- Website: https://mapaction.org/training/
- GIS for emergency response
- Field-focused practical skills

**UNOSAT Training**
- Geospatial training for humanitarian sector
- https://unosat.org/training/
- Includes satellite analysis, GIS, field data collection

---

## 5. Community and Support

### 5.1 OpenRiverCam Community

**GitHub Discussions:**
- Repository: https://github.com/localdevices/pyorc
- Issues tab: For bug reports and technical questions
- Discussions: [INFO NEEDED: If GitHub Discussions enabled]

**Community Forum:**
- [INFO NEEDED: Is there a dedicated forum or mailing list?]
- [INFO NEEDED: Slack, Discord, or other community platform?]

**Contributing:**
- Contributions welcome: Code, documentation, case studies
- Contribution guide: https://github.com/localdevices/pyorc/blob/main/CONTRIBUTING.md
- Issue tracker for feature requests and bugs

### 5.2 Related Communities

**OpenPIV Community:**
- Website: http://www.openpiv.net/
- Forum: https://github.com/OpenPIV/openpiv-python/discussions
- Particle Image Velocimetry techniques

**RTKLIB Community:**
- Forum: https://github.com/tomojitakasu/RTKLIB/discussions
- RTK GPS processing discussions

**QGIS Community:**
- Main site: https://qgis.org/en/site/getinvolved/index.html
- Mailing lists, user groups, IRC chat
- Very active and helpful community

### 5.3 Humanitarian Technology Communities

**Humanitarian OpenStreetMap Team (HOT)**
- Website: https://www.hotosm.org/
- Community mapping for humanitarian response
- Training, tools, and community

**Humanitarian Innovation Network**
- Website: https://www.humanitarianinnovation.org/
- Network of practitioners and researchers
- Webinars, publications, community

**CDAC Network (Communicating with Disaster-Affected Communities)**
- Website: https://www.cdacnetwork.org/
- Focus on communication and information management
- Resources and training

---

## 6. Technical Support Contacts

### 6.1 OpenRiverCam Project Support

**Primary Project Contact:**
- [INFO NEEDED: Official project email or contact form]
- [INFO NEEDED: Response time expectations]
- [INFO NEEDED: Languages supported]

**Technical Support:**
- GitHub Issues: https://github.com/localdevices/pyorc/issues
- Expected response: Community-driven, varies
- For bugs: Include minimal reproducible example

**Training and Capacity Building:**
- [INFO NEEDED: Training request contact]
- [INFO NEEDED: On-site training availability]
- [INFO NEEDED: Remote training/webinar schedule]

### 6.2 Equipment Vendor Support

**RTK GPS Equipment:**
- ArduSimple: support@ardusimple.com | https://www.ardusimple.com/question/
- Emlid: support@emlid.com | https://community.emlid.com/
- CHC Nav: Contact local distributor
- Trimble, Leica, Topcon: Contact authorized dealer

**Camera Equipment:**
- Hikvision: https://www.hikvision.com/en/support/
- Dahua: https://www.dahuasecurity.com/support
- Axis: https://www.axis.com/support
- Bosch: https://commerce.boschsecurity.com/us/en/Support

**Solar Power Equipment:**
- Renogy: support@renogy.com | https://www.renogy.com/
- Victron Energy: https://www.victronenergy.com/support-and-downloads/

### 6.3 Software Support

**QGIS:**
- Documentation: https://docs.qgis.org/
- User manual: https://docs.qgis.org/3.28/en/docs/user_manual/
- Community support: Mailing list, StackExchange

**RTKLIB:**
- GitHub: https://github.com/tomojitakasu/RTKLIB
- Community forum (discussions tab)
- Documentation in repository

**SW Maps:**
- Email: support@swmaps.app
- Documentation: https://www.swmaps.com/support/
- In-app help and tutorials

---

## 7. Data and Research

### 7.1 Academic Publications on Camera-Based Streamflow

**Key Research Papers:**

**OpenRiverCam Specific:**
- Pearce, S., et al. (2021). "OpenRiverCam, open-source operational discharge monitoring with low-cost cameras." EGU General Assembly 2021.
  - https://meetingorganizer.copernicus.org/EGU21/EGU21-5880.html

**LSPIV and Image Velocimetry:**
- Fujita, I., et al. (1998). "Large-scale particle image velocimetry for flow analysis in hydraulic engineering applications." Journal of Hydraulic Research.
  - Foundational paper on LSPIV technique

- Perks, M.T., et al. (2020). "Towards harmonization of image velocimetry techniques for river surface velocity observations." Earth System Science Data.
  - https://essd.copernicus.org/articles/12/1545/2020/

**Humanitarian Applications:**
- Tauro, F., et al. (2021). "Measurements and Observations in the XXI century (MOXXI): innovation and multi-disciplinarity to sense the hydrological cycle." Hydrological Sciences Journal.
  - Discusses emerging technologies including camera-based methods

### 7.2 Datasets and Benchmarks

**[INFO NEEDED: Sample Datasets]**

Planned publicly available datasets:
- Example videos from various river conditions
- Ground truth velocity measurements
- Sample GCP coordinate files
- Example cross-section surveys
- Processed discharge time series

**Purpose:** Allow users to test software and processing without conducting their own survey first.

### 7.3 Related Research Projects

**HydroHub (WMO)**
- Website: [INFO NEEDED: HydroHub project website if available]
- Global collaboration on hydrological innovation
- OpenRiverCam is supported by HydroHub program

**Horizon Europe Projects:**
- OpenRiverCam received funding from EU Horizon Europe
- Related projects in water monitoring and innovation

---

## 8. Funding and Grant Opportunities

### 8.1 Humanitarian Innovation Funding

**UNHCR Innovation Fund**
- Website: https://www.unhcr.org/innovation/innovation-fund/
- Supports innovative solutions for refugee contexts
- Rolling application process
- Typical grant: $50,000-200,000

**UNICEF Innovation Fund**
- Website: https://www.unicef.org/innovation/venture-fund
- Focus on open-source solutions
- Technology for vulnerable populations
- Funding: Up to $100,000

**WFP Innovation Accelerator**
- Website: https://innovation.wfp.org/
- Accelerator program and funding
- Focus on food security, resilience, climate
- Water resource monitoring relevant

**Start Network Innovation Lab**
- Website: https://startnetwork.org/learn-change/innovation-lab
- Support for humanitarian innovation
- Funding and technical assistance

### 8.2 Climate and Water Funding

**Green Climate Fund**
- Website: https://www.greenclimate.fund/
- Climate change adaptation projects
- Large-scale funding (>$1M typical)
- Requires country nomination

**Adaptation Fund**
- Website: https://www.adaptation-fund.org/
- Projects up to $10M
- Focus on vulnerable communities
- Climate adaptation and resilience

**Global Water Partnership**
- Website: https://www.gwp.org/
- Water resources management
- Regional programs and funding

### 8.3 Research and Development

**National Science Foundation (US)**
- Program: Science, Engineering and Education for Sustainability (SEES)
- Supports research on sustainable water resources

**European Commission Research Programs**
- Horizon Europe: https://research-and-innovation.ec.europa.eu/funding/funding-opportunities/funding-programmes-and-open-calls/horizon-europe_en
- Water-related calls under Cluster 6 (Food, Bioeconomy, Natural Resources, Agriculture and Environment)

**[INFO NEEDED: Other relevant funding programs by region]**

---

## 9. Equipment Procurement Resources

### 9.1 Major Suppliers

**RTK GPS Equipment:**
- ArduSimple: https://www.ardusimple.com/ (global shipping)
- Emlid: https://emlid.com/ (global shipping)
- CHC Nav: https://chcnav.com/ (find local distributor)
- Trimble: https://www.trimble.com/ (authorized dealers)

**IP Cameras:**
- B&H Photo (US): https://www.bhphotovideo.com/
- Adorama (US): https://www.adorama.com/
- Local security equipment suppliers (recommended for warranty/support)

**Solar Power Equipment:**
- Renogy: https://www.renogy.com/ (global shipping)
- Victron Energy: https://www.victronenergy.com/ (find distributor)
- Local solar equipment suppliers (often better pricing)

### 9.2 Humanitarian Procurement Programs

**UNHCR Supply Management Service**
- Catalogue: https://www.unhcr.org/supply-management
- Vetted suppliers for humanitarian organizations
- Bulk purchasing programs

**UNICEF Supply Division**
- Website: https://www.unicef.org/supply
- Products for children and families
- WASH equipment catalogue

**IOM Procurement**
- Contact through IOM country offices
- Equipment for displacement contexts

### 9.3 Procurement Guides

**Humanitarian Procurement Centres:**
- UNHCR Supply Hub (Copenhagen)
- UNICEF Supply Division (Copenhagen)
- WFP Global Logistics Cluster

**Tips for Humanitarian Procurement:**
1. Check duty exemptions for humanitarian imports
2. Coordinate with country office on import procedures
3. Consider local procurement for common items
4. Budget 15-30% additional for import duties/taxes
5. Build relationships with local suppliers for support

---

## 10. Updates and Changelog

**This Appendix Last Updated:** [Current Date]

**How to Suggest Updates:**
- [INFO NEEDED: Process for suggesting resource additions]
- [INFO NEEDED: Email or form for submitting new resources]

**Planned Additions:**
- Video tutorial library (in development)
- Additional case studies as deployments expand
- Sample datasets for testing and training
- Regional procurement guides
- Translated resources (French, Spanish, Arabic)

**Stay Informed:**
- [INFO NEEDED: Mailing list signup for updates]
- [INFO NEEDED: Social media accounts]
- GitHub: Watch repository for updates

---

## Quick Reference: Essential Links

**Software:**
- pyOpenRiverCam: https://github.com/localdevices/pyorc
- QGIS: https://qgis.org/
- RTKLIB: https://www.rtklib.com/

**Documentation:**
- pyorc docs: https://localdevices.github.io/pyorc/
- This manual: [INFO NEEDED: Link to online manual]

**Support:**
- GitHub Issues: https://github.com/localdevices/pyorc/issues
- [INFO NEEDED: Community forum or mailing list]

**PPP Processing:**
- AUSPOS: https://www.ga.gov.au/auspos

**Standards:**
- Sphere Handbook: https://spherestandards.org/handbook/
- WMO Hydrology: https://community.wmo.int/activity-areas/hydrology-and-water-resources

**Training:**
- QGIS Training: https://docs.qgis.org/3.28/en/docs/training_manual/
- HydroLearn: https://www.hydrolearn.org/

**Equipment:**
- ArduSimple RTK: https://www.ardusimple.com/
- Renogy Solar: https://www.renogy.com/

---

## References Cited in Manual

### Books and Manuals

1. UNHCR. (2024). UNHCR Water Manual for Refugee Situations. https://www.unhcr.org/media/unhcr-water-manual-refugee-situations

2. Sphere Association. (2018). The Sphere Handbook: Humanitarian Charter and Minimum Standards in Humanitarian Response. https://spherestandards.org/handbook/

3. World Meteorological Organization. (2009). Guide to Hydrological Practices, Volume I: Hydrology - From Measurement to Hydrological Information (WMO-No. 168). https://library.wmo.int/

### Journal Articles

4. Tauro, F., et al. (2018). "Measurements and Observations in the XXI century (MOXXI): innovation and multi-disciplinarity to sense the hydrological cycle." Hydrological Sciences Journal, 63(2), 169-196.

5. Perks, M.T., et al. (2020). "Towards harmonization of image velocimetry techniques for river surface velocity observations." Earth System Science Data, 12(3), 1545-1568.

6. Pearce, S., et al. (2021). "An Evaluation of Image Velocimetry Techniques under Low Flow Conditions and High Seeding Densities Using Unmanned Aerial Systems." Remote Sensing, 12(2), 232.

### Technical Reports and Grey Literature

7. ICIMOD. (2024). Community Based Flood Early Warning Systems. https://www.icimod.org/mountain/cbfews/

8. Practical Action. (2024). Preventing monsoon flood disasters: our work in climate resilience. https://practicalaction.org/

9. UNHCR. (2023). Global Report 2023 - Clean Water, Sanitation and Hygiene. https://reporting.unhcr.org/

### Online Resources

10. OpenRiverCam. (2024). pyOpenRiverCam Documentation. https://localdevices.github.io/pyorc/

11. World Meteorological Organization. (2024). HydroHub. https://wmo.int/

12. USGS. (2019). Discharge Measurements at Gaging Stations (Techniques and Methods 3-A8). https://pubs.usgs.gov/tm/tm3-a8/

---

**This appendix provides comprehensive resources for OpenRiverCam deployment, operation, and ongoing learning. Resources will be updated as the project and community evolve.**

**Contributions welcome:** Please submit additional resources, corrections, or updates to [INFO NEEDED: Contact for resource submissions].
