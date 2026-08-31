# Recommended improvements — working list

**This is the source.** Adjust it here — reorder, reword, cut, add — and the
report (`REPLICATION_RECOMMENDATIONS.md`) and the deck (`build_deck.py`) get
rewritten to match. Do not edit those two for content changes; they will be
regenerated from this.

Numbering is R1–R11 as currently published. If you renumber, say so and I will
carry it through both documents and the appendix cross-references.

---

## Let the station account for itself

- **R4 — Health reporting and mode alarms are requirements, not extras.** Any
  mode that suppresses data or raises energy use must be visible remotely, raise
  an alert if it persists, and expire on its own. *Cost: negligible.*

- **R5 — The station sends its own diagnostics; no login required.** A station
  awake for tens of seconds cannot hold an interactive session. *Cost: small.*

- **R6 — Record voltage and current together.** Voltage alone cannot separate a
  failing battery from a heavy load. *Cost: a current-sensing module and its
  logging.*

- **R7 — Compare what was recorded against what arrived, automatically.** The
  station knows what it captured; the server knows what it received; nothing
  compares them. *Cost: negligible.*

## Make the measurement trustworthy

- **R1 — Fit an independent water-level reference.** A level sensor, or a staff
  gauge in the camera's view tied to the *papan duga air* zero. Without one the
  station measures dependably only at night. *Cost: sensor, or gauge plus the
  survey tie.*

- **R2 — Plan the survey as professional work from the start.** The surveyed bed
  geometry is an input the processing cannot recover. Carry an independent field
  check of a different kind so a problem is caught before people leave site.
  *Cost: Rp 5–15 million per site.*

## Make the units buildable and maintainable in Indonesia

- **R3 — Specify interfaces, not part numbers.** Publish which properties bind —
  voltage, current, ingress protection, temperature — and which do not, so
  substitution under Indonesian procurement does not come back to us as a
  question. *Cost: documentation only.*

- **R8 — Consider putting the computer indoors.** Camera and sensors at the
  river, computer at a BHLK or IPB facility over a network link. *Designed, not
  yet field tested.*

- **R9 — Budget per station, and check the control interface before buying.**
  Apply the ceiling to the station rather than to each part in isolation, and
  confirm the interface you need exists in the firmware the unit actually ships
  with. *Cost: screening effort.*

- **R10 — Use the computer's own clock rather than a separate scheduling board,
  where the site allows.** Keep the separate board on solar sites, where its
  low-voltage and temperature cut-offs do real work. *Cost: saves about USD 50
  per station.*

- **R11 — Build on mains and leave it running, where continuous reporting is
  wanted.** *Cost: no solar array to buy; constrains siting to mains power.*

---

## Notes on the current set

Things worth deciding while you edit:

- **Grouping.** Three groups now, and the report says the first two decide
  whether a station produces usable information. Change the grouping or the
  claim if you disagree.
- **R8 and R11 overlap.** Both move the station away from a solar, duty-cycled
  box at the riverbank. They could be one recommendation.
- **R6 and R10 are the smallest.** If the list should be shorter, these are the
  two that could fold into others or drop.
- **Nothing here covers the server or the processing chain.** Every
  recommendation is about the station. If that is a gap, it is a real one.
- **R2 is the only one with a real price attached.** The others are effort, and
  the report does not estimate that effort. Say if it should.
