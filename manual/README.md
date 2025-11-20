# OpenRiverCam Manual

**A Comprehensive Guide for Humanitarian River Monitoring**

**Version:** 1.0
**Date:** November 2025
**Target Audience:** Humanitarian IM Officers and Program Managers

---

## About This Manual

This manual provides complete guidance for deploying and operating OpenRiverCam systems in humanitarian contexts. OpenRiverCam is a camera-based river monitoring system that provides real-time discharge measurements for flood early warning, water resource management, and emergency response.

**Key Features:**
- Non-contact, safe measurement during floods
- Low-cost deployment ($3,000-$15,000 equipment; see COST_FRAMEWORK.md for complete TCO)
- Operates autonomously with minimal maintenance
- Designed for non-technical staff
- Open-source and community-driven

---

## How to Use This Manual

### For Different Audiences

**Program Managers:**
- Start with Chapters 1-2 (Background and Humanitarian Applications)
- Review Chapter 6 (Site Selection) for strategic placement
- Use Appendix B (Equipment Specifications) for budgeting
- Reference Appendix D (Case Studies) for implementation examples

**IM Officers / Technical Coordinators:**
- Read Chapters 3-5 (Technical Concepts) for system understanding
- Follow Chapters 6-10 sequentially for deployment
- Use Appendix C (Troubleshooting) as operational reference
- Consult Appendix E (Resources) for software and support

**Field Technicians:**
- Focus on Chapters 8-9 (Installation and Survey procedures)
- Keep Appendix C (Troubleshooting) accessible during fieldwork
- Reference Chapter 10 (Software Configuration) for system setup

**All Users:**
- Use Appendix A (Glossary) for technical terms
- Review ROADMAP.md for manual structure and progress

---

## Manual Structure

### Part I: Foundation (Chapters 1-2)

**Chapter 1: OpenRiverCam Background**
- What is OpenRiverCam and how it works
- Development history and partnerships
- Current deployments worldwide
- Advantages and ideal use cases

**Chapter 2: Humanitarian Applications**
- Potential in humanitarian spaces
- Specific use examples (flood warning, refugee camps, etc.)
- Prior humanitarian deployments
- Problem-solution framework

### Part II: Technical Concepts (Chapters 3-5)

**Chapter 3: Hydrology Concepts**
- Fundamental relationships (Q = v × A)
- Tracers and flow measurement
- Comparison with conventional methods
- Rating curves (stage-discharge relationships)

**Chapter 4: Computer Imaging Concepts**
- Pixel-to-physical transformation
- Lens distortion
- Perspective distortion
- Atmospheric effects
- PIV/PTV overview (how the camera measures velocity)

**Chapter 5: Geospatial Survey Concepts**
- Centimeter-level survey strategies
- GNSS vs Total Station
- RTK fundamentals (Real-Time Kinematic positioning)
- Base and rover stations
- RTK fix status
- RINEX logging and PPP corrections
- Coordinate systems (UTM, local, global)
- Environmental factors affecting survey quality

### Part III: Site Work (Chapters 6-9)

**Chapter 6: Site Selection**
- Visible tracers requirement
- Lighting and shadow considerations
- Uniform flow requirement
- Survey accessibility at all water levels
- Hydrologic study factors
- Event types and placement strategy

**Chapter 7: Site Planning and Preparation**
- Camera location and installation planning
- Power requirements and options
- Network and internet connectivity
- Site security considerations

**Chapter 8: Equipment Installation**
- Power equipment installation (solar, utility, hybrid)
- Camera installation and mounting
- Assessing camera scene and marking field of view

**Chapter 9: Site Survey** (15 detailed sections)
- Survey concepts overview
- Day-before preparation
- Ground control point selection and placement
- Survey setup (hardware and software)
- Survey execution (camera, GCPs, water level, check points, cross-sections)
- Data processing (pole height, water level, UTM conversion, PPP corrections)

### Part IV: Operations (Chapter 10)

**Chapter 10: Software Configuration**
- Orienting the image
- Adding control points
- Adding cross-sections
- Server integration
- Automated collection and upload

### Appendices

**Appendix A: Glossary of Terms**
- Comprehensive definitions of 80+ technical terms
- Cross-references to detailed explanations

**Appendix B: Equipment Specifications**
- Complete system specifications
- Three price tiers: Budget ($3-5K), Standard ($7-10K), Premium ($12-15K)
- Procurement guidance
- Equipment comparison tables
- See COST_FRAMEWORK.md for detailed cost breakdowns and TCO analysis

**Appendix C: Troubleshooting Guide**
- Organized by system category
- Diagnostic procedures
- Solutions and escalation

**Appendix D: Case Studies**
- Sukabumi, Indonesia (detailed)
- Nepal CBFEWS context
- UNHCR refugee camp applications
- Lessons learned

**Appendix E: Resources and References**
- Software downloads
- Training materials
- Technical support
- Community forums
- Standards and research

---

## Quick Start Paths

### Path 1: Understanding OpenRiverCam (1-2 hours)
1. Chapter 1: OpenRiverCam Background
2. Chapter 2: Humanitarian Applications
3. Appendix D: Case Studies

### Path 2: Feasibility Assessment (2-4 hours)
1. Chapter 1.4: Advantages and Use Cases
2. Chapter 2.4: Problems ORC Can Address
3. Chapter 6: Site Selection
4. Appendix B: Equipment Specifications

### Path 3: Technical Understanding (1-2 days)
1. Chapter 3: Hydrology Concepts
2. Chapter 4: Computer Imaging Concepts
3. Chapter 5: Geospatial Survey Concepts

### Path 4: Deployment Execution (Follow sequentially)
1. Chapter 6: Site Selection
2. Chapter 7: Site Planning
3. Chapter 8: Equipment Installation
4. Chapter 9: Site Survey
5. Chapter 10: Software Configuration

---

## Key Documents

- **ROADMAP.md** - Development roadmap and progress tracking
- **OUTLINE.md** - Original manual outline and resource links
- **SURVEY_PROCESS.md** - Detailed survey field procedures (integrated into Chapter 9)

---

## Manual Statistics

- **Total Sections:** 64 (59 main chapters + 5 appendices)
- **Total Word Count:** ~280,000 words
- **Page Equivalent:** ~240-260 pages
- **Visual Aid Placeholders:** 400+
- **Development Time:** Phases 1-4 complete

---

## Getting Help

**Technical Questions:**
- Consult Appendix A (Glossary) for term definitions
- Check Appendix C (Troubleshooting) for common problems
- Review Appendix E (Resources) for support contacts

**Operational Questions:**
- Review relevant chapter based on deployment phase
- Consult case studies in Appendix D for real-world examples
- Connect with community through forums (see Appendix E)

**Equipment Questions:**
- See Appendix B for specifications and procurement
- Compare options across three price tiers
- Review 5-year total cost of ownership

---

## Contributing

This manual is a living document. Contributions are welcome:

- Case studies from new deployments
- Lessons learned and best practices
- Equipment recommendations and reviews
- Translations into other languages
- Corrections and clarifications

Contact the OpenRiverCam team through channels listed in Appendix E.

---

## License and Attribution

**Recommended Citation:**
OpenRiverCam Development Team (2025). *OpenRiverCam Manual: A Comprehensive Guide for Humanitarian River Monitoring*. Version 1.0.

**Acknowledgments:**
- Waterboard Limburg (Netherlands)
- Royal Netherlands Meteorological Institute (KNMI)
- Tanzania Water Practitioners
- Rainbow Sensing
- EU Horizon Europe
- World Meteorological Organization HydroHub
- All field deployment partners

---

## Version History

**Version 1.0 (November 2025)**
- Complete manual with all 10 chapters and 5 appendices
- Comprehensive coverage from concept through deployment
- Integrated SURVEY_PROCESS.md procedures
- 400+ visual aid placeholders documented
- Tailored for humanitarian audiences

---

**Ready to get started? Begin with [Chapter 1: OpenRiverCam Background](content/01-background/01-orc-overview.md)**
