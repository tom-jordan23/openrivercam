# Documentation Conversion Guide

## Conversion Standards for Sections 06-10 and Appendices

This guide documents the systematic approach for converting all remaining manual sections from conversational to formal academic prose with proper APA citations.

## Conversion Principles

### 1. Remove Conversational Language

**Before:**
```markdown
By the end of this section, you will be able to:
- Understand the concept
- Apply the method
- Recognize problems
```

**After:**
```markdown
Upon completion of this section, practitioners will possess the competencies necessary to comprehend the fundamental concepts, apply appropriate methodological frameworks, and identify problematic conditions requiring alternative approaches.
```

### 2. Convert Bullet Lists to Prose Paragraphs

**Before:**
```markdown
Good tracers have:
- Sufficient contrast against water surface
- Distribution across the river width
- Persistence for 2-5 seconds
- Movement representative of water flow
```

**After:**
```markdown
Effective surface tracers exhibit four essential characteristics that enable reliable velocity measurement. First, tracers must demonstrate sufficient contrast against the water surface to facilitate optical detection (Fujita et al., 1998). Second, spatial distribution across the full river width ensures representative velocity sampling throughout the cross-section. Third, temporal persistence of individual features for approximately 2-5 seconds allows tracking across multiple video frames (Le Coz et al., 2010). Fourth, tracer movement must accurately represent surface water motion without significant influence from wind or obstacle interference.
```

### 3. Replace Second-Person with Third-Person Academic Voice

**Before:**
```markdown
When you assess a site, observe the water surface carefully. You should look for features moving downstream consistently.
```

**After:**
```markdown
Site assessment requires careful observation of water surface characteristics. Evaluators should identify features exhibiting consistent downstream movement patterns (Muste et al., 2008).
```

### 4. Add Appropriate APA Citations

Key citation opportunities:
- Methodological statements → cite foundational papers
- Technical specifications → cite standards or research
- Empirical observations → cite field studies
- Conceptual frameworks → cite theoretical work

**Example Citations to Use:**
- Surface velocity methods: Fujita et al. (1998), Muste et al. (2008)
- LSPIV techniques: Hauet et al. (2008), Le Coz et al. (2010)
- Rating curves: Rantz et al. (1982), ISO (2007)
- Discharge measurement: ISO (2007), WMO (2010)
- Image velocimetry: Tauro et al. (2016), Pearce et al. (2020)
- Humanitarian applications: Dolcetti et al. (2022)

### 5. Maintain Technical Accuracy

While formalizing language:
- Preserve all technical specifications exactly
- Retain numerical values and units precisely
- Keep procedural steps accurate
- Maintain safety warnings clearly

## Section-by-Section Conversion Status

### Section 06: Site Selection (6 files)
- [x] 01-visible-tracers.md - IN PROGRESS
- [ ] 02-lighting-shadows.md
- [ ] 03-uniform-flow.md
- [ ] 04-survey-accessibility.md
- [ ] 05-hydrologic-study-factors.md
- [ ] 06-event-types-placement.md

### Section 07: Site Planning (4 files)
- [ ] 01-camera-location-planning.md
- [ ] 02-power-requirements.md
- [ ] 03-network-connectivity.md
- [ ] 04-security-considerations.md

### Section 08: Equipment Installation (4 files)
- [ ] 01-power-installation-solar.md
- [ ] 02-power-installation-utility.md
- [ ] 03-camera-installation.md
- [ ] 04-fov-assessment.md

### Section 09: Site Survey (15 files)
- [ ] 01-survey-concepts-overview.md through 15-ppp-corrections.md

### Section 10: Software Configuration (5 files)
- [ ] 01-orienting-image.md through 05-automated-collection.md

### Appendices (5 files)
- [ ] A-glossary.md through E-resources.md

## Key Reference List (to be expanded)

Dolcetti, G., Hortobágyi, B., Perks, M., Tait, S. J., & Dervilis, N. (2022). Using noncontact measurement of water surface dynamics to estimate river discharge. Water Resources Research, 58(9), e2022WR032829.

Fujita, I., Muste, M., & Kruger, A. (1998). Large-scale particle image velocimetry for flow analysis in hydraulic engineering applications. Journal of Hydraulic Research, 36(3), 397-414.

Hauet, A., Kruger, A., Krajewski, W. F., Bradley, A., Muste, M., Creutin, J. D., & Wilson, M. (2008). Experimental system for real-time discharge estimation using an image-based method. Journal of Hydrologic Engineering, 13(2), 105-110.

ISO. (2007). Hydrometry—Measurement of liquid flow in open channels using current-meters or floats (ISO 748:2007). International Organization for Standardization.

Le Coz, J., Hauet, A., Pierrefeu, G., Dramais, G., & Camenen, B. (2010). Performance of image-based velocimetry (LSPIV) applied to flash-flood discharge measurements in Mediterranean rivers. Journal of Hydrology, 394(1-2), 42-52.

Muste, M., Fujita, I., & Hauet, A. (2008). Large-scale particle image velocimetry for measurements in riverine environments. Water Resources Research, 44(4), W00D19.

Pearce, S., Ljubičić, R., Peña-Haro, S., Perks, M., Tauro, F., Pizarro, A., ... & Manfreda, S. (2020). An evaluation of image velocimetry techniques under low flow conditions and high seeding densities using unmanned aerial systems. Remote Sensing, 12(2), 232.

Rantz, S. E., & others. (1982). Measurement and computation of streamflow: Volume 1. Measurement of stage and discharge (USGS Water Supply Paper 2175). United States Geological Survey.

Tauro, F., Porfiri, M., & Grimaldi, S. (2016). Surface flow measurements from drones. Journal of Hydrology, 540, 240-245.

WMO. (2010). Manual on stream gauging (WMO-No. 1044). World Meteorological Organization.

## Common Phrase Conversions

| Conversational | Formal Academic |
|----------------|-----------------|
| "you will be able to" | "practitioners will possess the competency to" |
| "As you learned" | "As established in the preceding section" |
| "let's examine" | "examination of... reveals" |
| "this is important because" | "this consideration proves significant due to" |
| "you should" | "evaluators should" or "the methodology requires" |
| "Real-world example" | "Field implementation demonstrates" or "Empirical evidence from" |
| "helps you" | "facilitates" or "enables practitioners to" |
| "Key point" | "Critical consideration" or "Essential principle" |

## Quality Checklist

For each converted file, verify:
- [ ] All bullet points converted to complete prose paragraphs
- [ ] No second-person pronouns (you, your) remain
- [ ] Third-person academic voice throughout
- [ ] Minimum 5-10 citations added per major section
- [ ] Technical specifications preserved exactly
- [ ] Procedural accuracy maintained
- [ ] Professional academic tone consistent
- [ ] Headers and structure retained
- [ ] Visual placeholders maintained

## Next Steps

1. Complete Section 06 conversions (6 files)
2. Proceed through Sections 07-10 systematically
3. Convert Appendices
4. Compile comprehensive REFERENCES.md with all citations in APA format
5. Final review for consistency and academic standards
