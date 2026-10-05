# Source Notes 5 — October 2025 PTBox and the April 2026 Design Transition

## Scope and chronology

**Reported by Tom, September 23, 2026:** October 2025 installation with the PTBox; April 2026 installation with devices he built. **Documented connection:** the [Sukabumi site record](../../spring_2026_ID/SITES.md), “Sukabumi Site,” describes an existing combined compute/video unit affected by trapped humidity and an April 2026 redeployment. Read together, these establish the earlier Sukabumi phase and its relationship to the later build. Jakarta was a separate April build and remained undeployed.

The root [README](../../README.md) currently summarizes April 2026. Its repository map leads to `prior_work/`, `rc-box/`, and `survey/` for the earlier work. Its April-focused opening must not be treated as the start of the full project.

## Preparation and field workflow

- [Initial planning questions](../../prior_work/utilities/questions.md) cover access, mounting, solar power, ground control, calibration, cellular service, software access, and local support. These are planning questions, not proof every proposed activity occurred.
- [Pre-installation discussion](../../prior_work/deployment_guides/ORC_pre_install_meeting.txt) records Tom and Hessel discussing camera orientation, fixing the view before survey, remote access, and field support. Salvador was to be included for hardware guidance. The surviving transcript is partial and does not establish an on-site participant list.
- [PTBox survey procedure](../../survey/SURVEY_PROCESS_v2.md), “Export for PtBox” and “Connect to PtBox,” documents XYZ survey exports, maintenance mode, camera-view selection, and numbered control-point imagery. It warns that starting a malfunctioning camera can lock up the unit.
- [Archived configuration variants](../../prior_work/legacy_hardware/) identify PTBox 00031 and contain capture-cycle, recording-duration, maintenance, and infrared settings. Several variants exist; none should be treated as the final as-installed configuration without reconciliation. Files use JSON-like syntax that is not always valid JSON.

## Observations and design responses

| Evidence from earlier work | Design response | Claim boundary |
|---|---|---|
| Site record attributes interruption of the combined unit to trapped humidity; camera-options notes describe condensation after the camera bay was opened in very humid air | Separate factory-sealed camera from computing enclosure | Documented rationale, not an independently tested root-cause report or lifetime comparison |
| PTBox procedure warns that starting the malfunctioning camera can lock up the unit | Design emphasis on replaceable modules, accessible diagnostics, and field service | Supports the serviceability discussion; does not prove this one observation caused every design choice |
| Existing Sukabumi pole, 200 W solar panels, charge controller, and 50 Ah LiFePO4 battery recorded in the April site plan | Reuse site infrastructure for the April redeployment | Equipment specifications in the plan; not measured remaining capacity or autonomy |
| Earlier design requirements specify widely available parts, no soldering, common tools, and rapid component replacement | April build uses commodity modules and documented assembly/maintenance | Requirements and implemented approach; five-minute replacement is a design target, not a demonstrated service metric |

**Sources:** [SITES.md](../../spring_2026_ID/SITES.md); [camera-options summary](../../rc-box/research/camera_options_summary.md), opening rationale, updated January 6, 2026; [RC-Box specification](../../rc-box/DESIGN_SPECS.md), design principles; [earlier design record](../../prior_work/hardware_design_evolution/CLAUDE.md), camera rationale and field serviceability; [April build overview](../../spring_2026_ID/README.md).

The older design records also discuss ant ingress and several alternative camera/power approaches. Treat these as design history and research, not as a complete installed bill of materials. Some document headings use 2024 dates while related research and Git history are from late 2025; do not derive installation dates from those headings. The October 30, 2025 repository snapshot (`4f0646b`) already contains PTBox configurations and survey work; its root README describes a lab setup, not a full deployment narrative.

## Interpretation for the paper

The two phases form a constructive account of learning: establish field experience with the PTBox, translate observations into packaging and service requirements, build and install revised devices, and use the later operating record to refine measurement and delivery. Preserve the environmental observations without characterizing the installation as a failure. Do not claim the April design resolved every concern or improved reliability by a measured amount without comparable data.

## Remaining publication checks

Confirm individual credits and photograph permissions; reconcile configuration variants before publishing exact PTBox settings; identify dated PTBox outputs if available. The present source packet supports a substantive qualitative account but not a numerical comparison of the two installations.
