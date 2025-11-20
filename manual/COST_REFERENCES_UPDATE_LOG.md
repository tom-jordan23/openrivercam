# Cost References Update Log

**Purpose:** Track all cost mentions in the manual and ensure consistency with COST_FRAMEWORK.md

**Status:** In Progress
**Date Started:** November 20, 2025

---

## Standardized Framework Reference

**COST_FRAMEWORK.md establishes:**
- **Budget Tier:** $3,000-$5,000 (equipment only), $3,700-$6,700 (first year total)
- **Standard Tier:** $7,000-$10,000 (equipment only), $8,800-$14,500 (first year total)
- **Premium Tier:** $12,000-$15,000 (equipment only), $16,500-$25,500 (first year total)

**5-Year TCO:**
- Budget: $6,400-$13,000
- Standard: $14,000-$24,500
- Premium: $26,500-$45,500

---

## Files Requiring Updates

### 1. README.md

**Location:** /Users/tjordan/code/git/openrivercam/manual/README.md

**Current References:**
- Line 17: "$3,000-$15,000 total"
- Line 138: "Three price tiers ($3K, $7K, $15K)"

**Recommendation:**
- Line 17: Update to "$3,000-$15,000 (equipment costs, see COST_FRAMEWORK.md for complete TCO)"
- Line 138: Update to "Three price tiers: Budget ($3-5K), Standard ($7-10K), Premium ($12-15K) - see Appendix B and COST_FRAMEWORK.md"

**Status:** ⏳ Pending

---

### 2. content/01-background/01-orc-overview.md

**Location:** /Users/tjordan/code/git/openrivercam/manual/content/01-background/01-orc-overview.md

**Search for cost references in this file to determine what needs updating**

**Status:** ⏳ Pending - Need to read file and identify specific cost claims

---

### 3. content/01-background/04-advantages-and-use-cases.md

**Location:** /Users/tjordan/code/git/openrivercam/manual/content/01-background/04-advantages-and-use-cases.md

**Search for cost references and comparison tables**

**Status:** ⏳ Pending - Need to read file and identify cost comparison tables

---

### 4. content/02-humanitarian-applications/01-humanitarian-potential.md

**Location:** /Users/tjordan/code/git/openrivercam/manual/content/02-humanitarian-applications/01-humanitarian-potential.md

**Search for cost references in humanitarian context**

**Status:** ⏳ Pending

---

### 5. content/02-humanitarian-applications/02-specific-use-examples.md

**Location:** /Users/tjordan/code/git/openrivercam/manual/content/02-humanitarian-applications/02-specific-use-examples.md

**These are the hypothetical scenarios that need disclaimers**
- Nepal Melamchi River example
- Kenya Kakuma Camp example
- Mozambique Water Mission example
- Tanzania-Kenya Pangani River example

**Status:** ⏳ Pending - Needs both cost updates AND scenario disclaimers

---

### 6. content/02-humanitarian-applications/04-problems-orc-addresses.md

**Location:** /Users/tjordan/code/git/openrivercam/manual/content/02-humanitarian-applications/04-problems-orc-addresses.md

**Search for cost references in problem-solution framework**

**Status:** ⏳ Pending

---

### 7. content/03-hydrology-concepts/03-conventional-methods-comparison.md

**Location:** /Users/tjordan/code/git/openrivercam/manual/content/03-hydrology-concepts/03-conventional-methods-comparison.md

**Likely contains cost comparison with traditional methods**

**Status:** ⏳ Pending

---

### 8. content/03-hydrology-concepts/04-rating-curves.md

**Location:** /Users/tjordan/code/git/openrivercam/manual/content/03-hydrology-concepts/04-rating-curves.md

**Check for any cost references related to rating curve development**

**Status:** ⏳ Pending

---

### 9. content/05-geospatial-concepts/04-base-and-rover-stations.md

**Location:** /Users/tjordan/code/git/openrivercam/manual/content/05-geospatial-concepts/04-base-and-rover-stations.md

**Likely mentions RTK equipment costs**

**Status:** ⏳ Pending

---

### 10. content/05-geospatial-concepts/06-logging-rinex-ppp.md

**Location:** /Users/tjordan/code/git/openrivercam/manual/content/05-geospatial-concepts/06-logging-rinex-ppp.md

**Check for PPP service cost references**

**Status:** ⏳ Pending

---

### 11. appendices/B-equipment-specifications.md

**Location:** /Users/tjordan/code/git/openrivercam/manual/appendices/B-equipment-specifications.md

**CRITICAL:** This appendix contains detailed equipment pricing and should align exactly with COST_FRAMEWORK.md

**Status:** ⏳ Pending - High priority, contains detailed cost breakdowns

---

### 12. appendices/C-troubleshooting.md

**Location:** /Users/tjordan/code/git/openrivercam/manual/appendices/C-troubleshooting.md

**Check for any cost references in troubleshooting guidance**

**Status:** ⏳ Pending - Likely minimal cost references

---

### 13. appendices/E-resources.md

**Location:** /Users/tjordan/code/git/openrivercam/manual/appendices/E-resources.md

**Check for equipment supplier pricing information**

**Status:** ⏳ Pending

---

## Update Strategy

### Phase 1: Assessment (Current)
1. ✅ Create COST_FRAMEWORK.md (completed)
2. ✅ Identify all files with cost references (completed)
3. ⏳ Read each file and document specific cost claims (in progress)

### Phase 2: Prioritized Updates
**Order by impact:**

1. **HIGH PRIORITY - Core Reference Documents:**
   - appendices/B-equipment-specifications.md (must match COST_FRAMEWORK.md exactly)
   - README.md (first thing users see)
   - content/01-background/04-advantages-and-use-cases.md (comparison tables)

2. **MEDIUM PRIORITY - Humanitarian Context:**
   - content/02-humanitarian-applications/*.md (4 files)
   - content/03-hydrology-concepts/03-conventional-methods-comparison.md

3. **LOW PRIORITY - Technical Sections:**
   - content/05-geospatial-concepts/*.md (2 files)
   - appendices/C-troubleshooting.md
   - appendices/E-resources.md

### Phase 3: Verification
1. Search entire manual for any remaining inconsistent cost figures
2. Verify all cost references point to COST_FRAMEWORK.md
3. Update ROADMAP.md to reflect completed cost standardization

---

## Scenario Disclaimer Additions

**File:** content/02-humanitarian-applications/02-specific-use-examples.md

**Four scenarios requiring disclaimers:**

### Scenario 1: Nepal Melamchi River
**Add at beginning:**
> **Note:** This is an illustrative scenario demonstrating how OpenRiverCam could support community-based flood early warning systems. While based on real challenges in Nepal's flood-prone regions, this specific deployment is hypothetical and represents potential application of the technology.

### Scenario 2: Kenya Kakuma Camp
**Add at beginning:**
> **Note:** This scenario illustrates how OpenRiverCam could address water resource management challenges in displacement settings. While informed by real conditions at Kakuma refugee complex, this specific deployment example is illustrative and demonstrates potential humanitarian application.

### Scenario 3: Mozambique Water Mission
**Add at beginning:**
> **Note:** This scenario demonstrates how OpenRiverCam could support rapid post-disaster water assessment. While based on realistic disaster response challenges, this specific deployment is hypothetical and illustrates emergency application potential.

### Scenario 4: Tanzania-Kenya Pangani River
**Add at beginning:**
> **Note:** This scenario illustrates how OpenRiverCam could support transboundary water resource monitoring and conflict reduction. While based on real transboundary challenges, this specific deployment is hypothetical and demonstrates potential peace-building application.

**Add at end of chapter:**
> ## From Scenarios to Reality
>
> The use cases presented in this chapter are illustrative scenarios designed to demonstrate OpenRiverCam's potential applications in humanitarian contexts. While these specific deployments are hypothetical, they are based on:
>
> - Real technical capabilities demonstrated in operational deployments (Netherlands, Indonesia)
> - Documented humanitarian challenges and needs
> - Established early warning and water management best practices
> - Feasibility assessments conducted during system development
>
> **Actual humanitarian deployments:**
> - Sukabumi, Indonesia (2024) - Urban flood monitoring (see Appendix D for detailed case study)
> - [Additional deployments will be documented as they occur]
>
> Organizations interested in implementing similar systems should refer to:
> - **Appendix D:** Detailed case studies from real deployments
> - **Chapter 6:** Site selection criteria for assessing feasibility
> - **Chapter 2.4:** Decision framework for determining ORC appropriateness
> - **COST_FRAMEWORK.md:** Detailed budget planning guidance

**Status:** ⏳ Pending

---

## Camera Mounting Height Specifications

**Issue:** Inconsistency between manual and SURVEY_PROCESS.md

**SURVEY_PROCESS.md (authoritative):**
- Height: 5-10m
- Viewing angle: 15-45°

**Manual inconsistencies found:**
- Some sections cite: 8-12m height, 20-45° angle

**Files to check and update:**
- content/04-imaging-concepts/03-perspective-distortion.md
- content/07-site-planning/01-camera-location.md
- Any other references to camera mounting specifications

**Standardized language to use:**
> Camera should be mounted **5-10 meters above the water surface** (typically 8-10m for optimal coverage) with a **viewing angle of 15-45° looking downstream**. Lower heights (5-7m) may be acceptable for narrow channels, while higher positions (9-10m) provide better coverage for wide rivers. The viewing angle should balance perspective distortion (minimized with steeper angles) against velocity measurement accuracy (requires seeing surface features).

**Status:** ⏳ Pending - Need to identify all instances

---

## Emerging Technology Disclaimer

**File:** content/02-humanitarian-applications/03-prior-humanitarian-work.md

**Location:** Beginning of chapter, after title

**Add disclaimer:**
> ## Technology Maturity Status
>
> **OpenRiverCam is an emerging technology in humanitarian contexts.** While the system has demonstrated reliable performance in professional water management settings (Netherlands, Indonesia), humanitarian deployments are limited and the technology is still being validated for aid organization use.
>
> **Current deployment status:**
> - **Proven:** Professional water management (Netherlands water boards, operational since [INFO NEEDED: year])
> - **Demonstrated:** Urban flood monitoring (Sukabumi, Indonesia, 2024)
> - **Emerging:** Humanitarian aid organization use (limited deployments, technology transfer in progress)
>
> This manual is designed to support the **transition from research/professional use to humanitarian deployment** by providing accessible guidance for non-technical IM officers and program managers. Organizations considering OpenRiverCam should:
>
> 1. **Start with pilot deployments** (Budget tier, single site, 6-12 month evaluation)
> 2. **Validate in local context** (test with site-specific conditions)
> 3. **Build local capacity** (ensure sustainability before scaling)
> 4. **Document and share** (contribute lessons learned to growing knowledge base)
>
> **What "emerging" means for your organization:**
> - ✅ Technology is proven functional (not experimental)
> - ✅ Technical support available (pyOpenRiverCam community, documentation)
> - ⚠️ Limited field experience in humanitarian contexts (fewer case studies than traditional methods)
> - ⚠️ May require troubleshooting and adaptation (not "plug and play" initially)
> - ⚠️ Best suited for organizations with some technical capacity (IM officers, WASH engineers)
>
> As more humanitarian organizations deploy OpenRiverCam, this status will evolve. Check [INFO NEEDED: project website] for updates on humanitarian deployments and case studies.

**Status:** ⏳ Pending

---

## Progress Tracking

**Started:** November 20, 2025

**Completed Actions:**
- ✅ Created COST_FRAMEWORK.md with authoritative three-tier system
- ✅ Identified 13 files requiring cost updates
- ✅ Documented standardized disclaimer text for scenarios
- ✅ Documented camera height standardization requirements
- ✅ Documented emerging technology disclaimer

**In Progress:**
- ⏳ Reading individual files to identify specific cost claims
- ⏳ Preparing file-by-file update instructions

**Next Actions:**
1. Read high-priority files (Appendix B, README, Chapter 1.4)
2. Document exact line numbers and current text for each cost reference
3. Begin systematic updates starting with highest priority
4. Test cross-references and ensure all links to COST_FRAMEWORK.md work
5. Update ROADMAP.md with completion status

---

## Verification Checklist

After all updates complete, verify:

- [ ] COST_FRAMEWORK.md referenced in README.md
- [ ] Appendix B matches COST_FRAMEWORK.md exactly
- [ ] All scenario disclaimers added to Chapter 2.2
- [ ] Camera mounting specs consistent (5-10m, 15-45°)
- [ ] Emerging technology disclaimer added to Chapter 2.3
- [ ] No remaining inconsistent cost figures (search manual for $[0-9])
- [ ] All cost ranges use Budget/Standard/Premium tier labels
- [ ] ROADMAP.md updated with completion date
- [ ] FACT_CHECK_REPORT.md marked as "Priority 1 issues addressed"

---

**Last Updated:** November 20, 2025
**Updated By:** Cost standardization project
**Status:** Phase 1 complete, Phase 2 in progress
