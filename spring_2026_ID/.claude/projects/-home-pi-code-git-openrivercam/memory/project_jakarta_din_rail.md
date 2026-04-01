---
name: Jakarta DIN rail full
description: Jakarta enclosure has no empty DIN rail space — affects LED and any future component mounting
type: project
---

Jakarta enclosure has no remaining DIN rail space. The Sukabumi LED 5V splice uses a Wago 221 lever-nut (no rail needed), but any future components that need DIN mounting will require rearranging the Jakarta layout.

**Why:** The Jakarta box is more densely packed (AC power supply, surge suppressor, additional terminal blocks).

**How to apply:** When planning Jakarta LED wiring or any new component, don't assume DIN rail availability. The Wago splice approach for 5V works without rail space. Flag this constraint early in Jakarta build planning.
