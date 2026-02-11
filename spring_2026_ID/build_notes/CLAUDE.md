# Sukabumi Build Phase - Guide for Claude

**Context:** Build and test phase for Sukabumi ORC station
**Prerequisite:** Parts procured (see `sukabumi_parts_procured.csv`)
**Reference:** Main project planning in `/spring_2026_ID/CLAUDE.md`

---

## Purpose

This directory contains build documentation, test results, and lessons learned for the Sukabumi deployment. The goal is a fully tested, deployable unit with documentation sufficient for:

1. **Repeatability** - Another person could build an identical unit from documentation
2. **Traceability** - Every component tracked, every decision documented
3. **Field service** - Troubleshooting and repair possible without original builder

---

## Guiding Principles

### Quality Over Speed

This is not a rush job. Take time to:
- Verify before proceeding (hold points)
- Document as you go (not after)
- Investigate anomalies (don't ignore)
- Photograph key stages

### No Assumptions

- Measure, don't estimate
- Test, don't assume
- Record actual values, not expected values
- Cross-reference specifications against datasheets

### Design Constraints (from DESIGN_SPECS.md)

| Constraint | Requirement |
|------------|-------------|
| No soldering | All connections via screw terminals, plugs, or headers |
| No fabrication | Use commodity parts only |
| Common tools | Phillips screwdriver, adjustable wrench, wire strippers |
| Field serviceable | Any component replaceable in <5 minutes |

**If a build step requires soldering or custom fabrication, stop and reconsider.**

### Software Ecosystem

This project operates within the **LiveORC/NodeORC ecosystem**. We are working closely with the OpenRiverCam team.

| Principle | Approach |
|-----------|----------|
| No forking | Do not fork OpenRiverCam or create incompatible versions |
| Contribute upstream | If software changes are needed, submit PRs to the project |
| Extend, don't replace | Build on existing functionality rather than reimplementing |
| Coordinate with team | Discuss significant changes with OpenRiverCam maintainers |

**If software modifications are needed during build/test:**

1. Document the need clearly (what's missing, why it's needed)
2. Check if the functionality already exists in LiveORC/NodeORC
3. Design changes to be general-purpose, not site-specific
4. Submit as PR to appropriate repository
5. Use temporary workarounds only if blocking, and document for later cleanup

**Do not create custom scripts or forks that diverge from the main project.**

### Remote Access & Configuration

The device will be on an Indonesian cellular network with no public IP. Remote access and configuration management are critical for field support.

**Remote Access: Pangolin**

The ORC team uses Pangolin for remote access to field devices. We will use the same approach for consistency and support.

| Requirement | Solution |
|-------------|----------|
| SSH access from abroad | Pangolin tunnel |
| No public IP needed | Pangolin handles NAT traversal |
| Secure connection | Pangolin provides encrypted tunnel |
| Consistent with ORC team | Same tooling, shared knowledge |

**Remote Configuration Management**

The ORC team uses a script that checks an FTP server for configuration updates at device startup. We will mirror this approach:

| Behavior | Implementation |
|----------|----------------|
| On boot | Device checks FTP server for config updates |
| Config changed | Download new config, apply, log change |
| Config unchanged | Continue with existing config |
| FTP unreachable | Continue with existing config, log warning |
| Rollback | Keep previous config as backup |

**Build implications:**

- Phase 5/6: Configure Pangolin client during Witty Pi / modem setup
- Phase 11: Configure FTP config-check script as part of ORC installation
- Phase 12: Test remote access via Pangolin before enclosure sealing
- Phase 14: Verify config-check works during scheduled wake cycles

**Document in `configuration_backup.md`:**
- Pangolin server details and device credentials
- FTP server location and credentials
- Config file format and location
- Rollback procedure if bad config pushed

---

## Build Sequence Overview

The build proceeds in phases. Each phase has verification criteria that must pass before proceeding.

| Phase | Description | Blocking Dependencies | Notes |
|-------|-------------|----------------------|-------|
| 0 | Incoming inspection | None | |
| 1 | Workspace preparation | Phase 0 | |
| 1B | **Complete dry fit** | Phase 1 | Verify ALL fits before any irreversible action |
| 2 | Conformal coating | Phase 1B; requires 24hr cure | Boards non-returnable after |
| 3 | Compute platform assembly | Phase 2 complete | |
| 4 | Initial boot test | Phase 3 | |
| 5 | Witty Pi configuration | Phase 4 | |
| 6 | Modem assembly & test | Phase 4 | Include Pangolin client setup |
| 7 | Camera configuration | Phase 4 | |
| 8 | Rain gauge setup | Phase 4 | |
| 9 | Status LEDs & button | Phase 4 | |
| 10 | Enclosure assembly | Phases 3-9 | |
| 11 | ORC software installation | Phase 10 | Include FTP config-check script |
| 12 | Integration testing | Phase 11 | **Test Pangolin remote access** |
| 13 | Power budget verification | Phase 12 | |
| 14 | Schedule testing | Phase 13 | Verify config-check on wake |
| 15 | Environmental testing | Phase 14 | |
| 16 | Final verification | Phase 15 | |

### Quality Hold Points

Do not proceed past these phases without explicit verification:

- **After Phase 0** - All components inspected and functional
- **After Phase 1B** - Complete dry fit verified (last chance to return/exchange components)
- **After Phase 2** - Coating cured, coverage verified (boards non-returnable)

### Point of No Return

Phase 1B is the last checkpoint before irreversible modifications:

| After Phase | What Becomes Non-Returnable |
|-------------|----------------------------|
| Phase 2 | Coated PCBs (Pi, Witty Pi, GPIO Breakout) |
| Phase 10 | Enclosure (drilled/cut) |

**Verify everything fits and works in Phase 1B before proceeding.**
- **After Phase 4** - System boots reliably with all devices detected
- **After Phase 10** - Enclosure sealed (difficult to rework)
- **After Phase 14** - Automated schedule working correctly
- **After Phase 16** - Final acceptance

---

## Documents to Create

### Required Artifacts

| Document | Purpose | When to Create |
|----------|---------|----------------|
| `component_registry.md` | Serial numbers, date codes, supplier info for all components | Phase 0 |
| `incoming_inspection.md` | Inspection results, photos of components as received | Phase 0 |
| `build_checklist.md` | Step-by-step checklist with verification criteria | Phase 1, update throughout |
| `environmental_log.md` | Temperature/humidity during build sessions | Ongoing |
| `test_results.md` | All test measurements and pass/fail outcomes | Phases 4-15 |
| `wiring_diagram.md` or `.svg` | Actual wiring as built | Phase 10 |
| `configuration_backup.md` | All software settings, credentials (secure storage) | Phase 11 |
| `known_issues.md` | Problems encountered and resolutions | As needed |
| `final_acceptance.md` | Sign-off that unit is ready for deployment | Phase 16 |

### Photo Requirements

Store in `photos/` subdirectory with naming convention: `YYYYMMDD_phase##_description.jpg`

| Phase | Required Photos |
|-------|-----------------|
| 0 | Each component as received (labels visible) |
| 2 | Each board before and after coating |
| 3 | HAT stack assembled (side and top views) |
| 6 | Modem in adapter, antenna connections |
| 8-9 | Wiring at GPIO breakout |
| 10 | Enclosure interior, cable routing, exterior |
| 16 | Final unit from all sides |

---

## Specialized Agents

Use these agents for specific tasks:

| Agent | When to Use |
|-------|-------------|
| `documentation-expert` | Creating checklists, wiring diagrams, field documentation |
| `comprehensive-researcher` | Researching datasheets, troubleshooting unfamiliar issues |
| `test-engineer` | Developing test procedures, acceptance criteria |
| `error-detective` | Debugging boot failures, connection issues, log analysis |
| `backend-architect` | Power budget calculations, timing analysis |
| `Explore` | Finding existing research or specs in the codebase |

### Example Prompts

**Creating the build checklist:**
> Use documentation-expert to create a detailed build checklist for Phase 3 (compute platform assembly). Include step-by-step instructions, verification criteria with specific pass/fail thresholds, and a notes section for recording actual observations. Reference the stacking headers, Witty Pi 5, and GPIO breakout from the parts list.

**Developing test criteria:**
> Use test-engineer to develop acceptance criteria for camera configuration (Phase 7). Include specific thresholds for video resolution, duration, codec, and streaming reliability. Format as a table with requirement, minimum acceptable, and actual value columns.

**Troubleshooting:**
> Use error-detective to investigate why the Pi won't boot with the Witty Pi HAT installed. It boots fine without the HAT. Check for I2C conflicts, power issues, or GPIO pin conflicts.

---

## Acceptance Criteria Framework

When creating checklists and test procedures, use this framework:

### For Each Build Step

1. **Preconditions** - What must be true before starting
2. **Actions** - Specific steps to perform
3. **Verification** - How to confirm success
4. **Acceptance criteria** - Specific pass/fail thresholds
5. **Notes field** - Space to record actual values and observations

### For Measurements

| Element | Include |
|---------|---------|
| Expected value | From datasheet or design |
| Minimum acceptable | Lower bound for pass |
| Maximum acceptable | Upper bound for pass |
| Actual measured | Filled in during build |
| Pass/Fail | Based on actual vs. acceptable range |

### Example

```markdown
#### 4.3 CPU Temperature Check

**Precondition:** System booted and idle for 2+ minutes

**Action:** Run `vcgencmd measure_temp`

**Acceptance Criteria:**

| Metric | Min | Max | Actual | Pass |
|--------|-----|-----|--------|------|
| CPU temp at idle | - | 50°C | ___°C | [ ] |
| Ambient temp | 18°C | 30°C | ___°C | [ ] |

**Notes:**
```
(Record any thermal concerns, fan behavior)
```
```

---

## Key Technical References

### From Main CLAUDE.md

- **Power budget target:** <94 Wh/day
- **Duty cycle:** 2.5 min on, 12.5 min off (15 min cycle)
- **Camera boot time:** ~45-60 seconds
- **Humidity protection:** Conformal coating (MG 422C) + Gore vent, no heaters

### Parts Reference

See `sukabumi_parts_procured.csv` for:
- Exact components ordered
- Supplier and order numbers
- Pricing and links

### Research Documents

| Topic | Location |
|-------|----------|
| Conformal coating procedure | `/spring_2026_ID/research/conformal_coating_procedure.md` |
| GPIO stacking analysis | `/spring_2026_ID/research/GPIO_STACKING_ANALYSIS.md` |
| Witty Pi 5 research | `/spring_2026_ID/research/witty_pi_5_research.md` |
| Camera options | `/rc-box/research/camera_options_summary.md` |
| Design specifications | `/rc-box/DESIGN_SPECS.md` |

### Software Ecosystem

| Component | Repository / Resource | Purpose |
|-----------|----------------------|---------|
| LiveORC | https://github.com/localdevices/LiveORC | Cloud platform |
| NodeORC | https://github.com/localdevices/nodeorc | Edge device software |
| pyorc | https://github.com/localdevices/pyorc | Python processing library |
| Pangolin | https://github.com/fossorern/pangolin (or ORC team resource) | Remote access tunneling |

**Note:** Phase 11 (ORC software installation) should use existing LiveORC/NodeORC packages. If modifications are needed, coordinate with the OpenRiverCam team and submit PRs rather than creating local forks.

**Remote access:** Pangolin is used by the ORC team for secure remote access to field devices behind NAT/cellular. Configure during Phase 6, test during Phase 12.

---

## Issue Tracking

When problems arise during build:

1. **Document immediately** - Don't wait until later
2. **Include context** - What phase, what was happening, what was expected vs. actual
3. **Investigate root cause** - Use error-detective agent if needed
4. **Record resolution** - What fixed it
5. **Update procedures** - If the checklist needs correction, note it

### Issue Template

```markdown
## Issue: [Brief description]

**Phase:** [Number]
**Date:** YYYY-MM-DD
**Severity:** [Blocking / Major / Minor]

### Symptoms
[What was observed]

### Expected Behavior
[What should have happened]

### Investigation
[Steps taken to diagnose]

### Root Cause
[Why it happened]

### Resolution
[How it was fixed]

### Prevention
[How to avoid in future builds]

### Checklist Updates Needed
[Any changes to build procedures]
```

---

## Recovery Procedures

If major issues occur, document recovery approach for:

- **Bad conformal coating** - Coating on connectors, incomplete coverage
- **Boot failure after assembly** - HAT conflicts, damaged components
- **Component damage** - Bent pins, broken connectors
- **Enclosure seal failure** - Water ingress, failed seal test
- **Corrupted SD card** - Filesystem errors, boot failure
- **Modem connection issues** - SIM problems, network registration failure

Use comprehensive-researcher or error-detective agents to develop recovery procedures as needed.

---

## Success Criteria

The build phase is complete when:

- [ ] All 16 build phases documented with results
- [ ] All quality hold points passed
- [ ] All acceptance criteria met (no failures)
- [ ] Component registry complete with serial numbers
- [ ] All required photos taken
- [ ] Test results documented with actual measurements
- [ ] Known issues documented with resolutions
- [ ] Configuration backed up and verified
- [ ] System runs 4+ consecutive duty cycles without error
- [ ] Power consumption verified within budget
- [ ] Final acceptance signed off
- [ ] Documentation sufficient for another builder to replicate

---

## Workflow

### Starting a Build Session

1. Record environmental conditions (temp, humidity)
2. Review where previous session ended
3. Identify next phase to work on
4. Gather required tools and components
5. Review checklist for that phase

### During Build

1. Follow checklist step by step
2. Record actual values, not just pass/fail
3. Take required photos
4. Note any deviations or issues immediately
5. Don't skip verification steps

### Ending a Build Session

1. Update checklist with progress
2. Document any open issues
3. Secure components appropriately
4. Back up any new documentation
5. Note stopping point for next session

### Asking for Help

When requesting Claude assistance:
- Specify which phase you're in
- Describe what you're trying to accomplish
- Include any error messages or symptoms
- Reference relevant documentation
- Ask for specific deliverables (checklist, test procedure, troubleshooting steps)
