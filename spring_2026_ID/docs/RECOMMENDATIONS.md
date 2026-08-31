# Recommended improvements — working list

**This is the source.** Adjust it here — reorder, reword, cut, add — and the
report (`REPLICATION_RECOMMENDATIONS.md`) and the deck (`build_deck.py`) get
rewritten to match. Do not edit those two for content changes; they will be
regenerated from this.

Numbering is R1–R15. R12–R15 are new and cover the server and the processing
chain. If you renumber, say so and I will carry it through both documents and the
appendix cross-references.

---

## Improve monitoring

- **R4 — Report station health, and alarm on any mode that stops data.** The
  station should send its state on every wake. Any mode that suppresses recording
  or raises energy use should be visible remotely, should raise an alert if it
  stays set, and should expire on its own after a set time. *Cost: negligible.*

- **R5 — Have the station send diagnostics; do not require a login.** The station
  is awake for tens of seconds, which is not long enough to open an interactive
  session. Diagnostics have to be pushed by the station on its own schedule.
  *Cost: small.*

- **R6 — Record voltage and current together.** The station currently logs
  temperature, rainfall and humidity, and nothing electrical. Voltage on its own
  cannot separate a failing battery from a heavy load, so power problems could
  not be diagnosed remotely. The Witty Pi already reports voltage and current
  over the I2C link the sensor software uses. *Cost: a current-sensing module and
  its logging.*

- **R7 — Compare what was recorded against what arrived, automatically.** The
  station knows what it captured and the server knows what it received. Nothing
  compares the two, so data can go missing without any symptom at either end.
  *Cost: negligible.*

## Improve measurement accuracy

- **R1 — Fit an independent water-level reference.** A level sensor, or a staff
  gauge in the camera's view tied to the *papan duga air* zero. Without one, the
  station measures dependably only at night. *Cost: sensor, or gauge plus the
  survey tie.*

- **R2 — Plan the survey as professional work from the start.** The surveyed bed
  geometry is an input the processing cannot recover. Carry an independent field
  check of a different kind, so a problem is found before the survey team leaves
  the site. *Cost: Rp 5–15 million per site.*

## Support local construction and maintenance

- **R3 — Specify interfaces, not part numbers.** Publish which properties must be
  matched — voltage, current, ingress protection, operating temperature — and
  which are free to vary, such as brand and mounting style. Parts will be bought
  in Indonesia under Indonesian procurement rules, so substitution is normal and
  should not require asking us. *Cost: documentation only.*

- **R8 — Consider putting the computer indoors.** Camera and sensors at the
  river, computer at a BHLK or IPB facility, connected over a network link.
  *Designed, not yet field tested.*

- **R9 — Set the budget per station, and check the control interface before
  buying.** Apply the cost limit to the whole station rather than to each part
  separately, and confirm that the interface you need is present in the firmware
  the unit actually ships with. *Cost: screening effort.*

- **R11 — Build on mains power and leave the station running, where continuous
  reporting is wanted.** *Cost: no solar array to buy; restricts siting to places
  with mains power.*

## Give one process control of the sleep and wake cycle

- **R10 — One process should control both shutdown and startup.** At Sukabumi
  these are split between two systems, and that split caused a large share of the
  outages.

  How it currently works: the station software (ORC-OS) decides when to shut
  down, using a setting that shuts the station down after its processing task
  finishes. The scheduling board (Witty Pi) decides when to start up, using an
  alarm set for the next wake time. Neither one controls the whole cycle.

  This produces two failures that combine:

  - **The station does not shut down.** When processing does not finish, the
    shutdown never happens. Processing failed on 43% of videos, because the disk
    stayed full at the level where it deletes old files. The station then stayed
    awake until the scheduling board's 25-minute backstop, instead of shutting
    down after about two minutes — roughly twelve times the energy for that
    cycle. Repeated across a night, this is what flattened the battery. This was
    the root cause found in August.

  - **The station does not start up again.** When a wake is missed, the
    scheduling board's next-startup alarm is left in the past and nothing sets a
    new one. One missed cycle then becomes days off, until someone intervenes.

  Whichever way the design goes — the computer's own clock, or the scheduling
  board — one of them should own the whole cycle, and the next wake should be
  set as part of shutting down. The Raspberry Pi's own clock does this: the
  operating system writes the next alarm at shutdown, so the two halves cannot
  disagree.

  Two things to keep in mind. The Pi's own clock was the original design and was
  replaced late in the build because a small battery connector failed on both
  boards — treat that connector as fragile and keep a scheduling board in spares.
  And on a solar site the scheduling board is doing real work that the Pi's clock
  does not do: cutting power completely rather than leaving the Pi in standby,
  accepting 6–30 V straight from the battery, and providing low-voltage and
  temperature cut-offs. *Cost: saves about USD 50 per station where the board is
  removed; otherwise software only.*

## Improve the server and the processing chain

- **R12 — A processing failure must not prevent the station from shutting down.**
  Shutdown should be driven by a timer that runs regardless of what the
  processing task does, so that a bad video costs one measurement rather than a
  night of battery. See R10 for the mechanism.

- **R13 — Manage disk space before it stops the station working.** The station
  disk stayed full at the level where it automatically deletes old files, which
  caused processing failures and deleted recordings before they could be sent
  again. Free space should be reported with station health (R4), should raise an
  alert before the deletion threshold is reached, and recordings that have not
  yet reached the server should be the last to be deleted. *Cost: small.*

- **R14 — A failed water level should not discard the whole measurement.** Water
  level is worked out first, and when it fails the entire processing run is
  abandoned, including the surface velocity work that had already succeeded.
  Storing the partial result would keep the velocity data and make the failure
  visible as a missing level rather than as a missing measurement. *Cost:
  software only.*

- **R15 — Monitor the server as well as the station.** Video stopped arriving for
  twelve days while the station was healthy and logging normally throughout, and
  this was not noticed at the time. The reconciliation in R7 would catch it, but
  it needs to run against the server and alarm on the server side as well. Two
  server constraints found in practice also belong in the design: the video store
  and the database must share one filesystem, and server and station software
  versions are tied together, so a server upgrade obliges the stations to follow.
  *Cost: small.*

---

## Notes on the current set

Things worth deciding while you edit:

- **R10 has grown into the largest item** because it explains the outages. It
  could split into "one process owns the cycle" and "keep the scheduling board on
  solar sites", which are separate decisions.
- **R10 and R12 overlap.** R12 is the software half of R10. They could be one.
- **R8 and R11 overlap.** Both move the station away from a solar, duty-cycled
  box at the riverbank.
- **R2 is the only item with a real price.** The rest are effort, and this list
  does not estimate that effort. Say if it should.
- **Ordering.** The groups are currently monitoring, accuracy, local
  construction, sleep and wake, server and processing. The report leads with
  whichever comes first, so this order is an argument about priority.
