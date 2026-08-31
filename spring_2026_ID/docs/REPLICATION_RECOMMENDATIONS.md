# OpenRiverCam in Indonesia: What the Pilot Taught Us, and the Path Forward

**Version:** 2026-08-31 (draft for internal review — not yet circulated)

**Partners:** Palang Merah Indonesia · Institut Pertanian Bogor · Balai Hidrologi
dan Lingkungan Keairan · American Red Cross

**Prepared for:** IPB and BHLK, following the PMI / IPB / BHLK meeting at
Sukabumi, 21 August 2026.

**Reading time:** about eight minutes, plus the index at the back.

**Companion documents:** the *Appendix*, which holds the measurements, interface
specifications and procedures behind everything below; and
`docs/RECOMMENDATIONS.md`, the working list this report is drawn from.

---

## Thank you

None of this exists without the people who built it and looked after it. PMI
volunteers and staff at Sukabumi and Jakarta gave their time to a system that was
new to them and that did not always work. IPB re-surveyed the site with a total
station after our own survey failed twice, and that survey is what the station
runs on today. BHLK brought the standards knowledge, and the offer of server
capacity, that make a pilot possible at all.

What follows is largely a list of things we would do differently. Every one of
them was learned because someone did the work that made it visible.

## What we did

A camera on a pole watches the river. A small computer in a weatherproof box
turns the video into a water level and a discharge figure, and a mobile data link
sends both, with the video, to a server. Sukabumi runs on solar power and wakes
every thirty minutes: it starts, records, processes, uploads and shuts down.

![The camera on its pole sends video to the station computer, which derives water
level and discharge; both travel over the mobile network to the server. The three
things the computer depends on are shown beneath it. The whole sequence happens
inside a waking period of about two minutes, of which the first thirty to sixty
seconds is spent waiting for the camera to start.](figures/fig1_system.svg)

The station came to **USD 1,340 in materials** — electronics and enclosure only,
since Sukabumi already had a solar panel and battery on site. For comparison, the
lowest-cost automatic water-level station we could confirm on the Indonesian
government e-catalogue is about **USD 3,600 before VAT**, and it measures stage
only. That price difference is the whole argument for studying this design: how
many stations an agency can afford decides how much of a catchment it can
observe.

Five constraints governed every choice of part, and they are why the design can be
copied at all: commodity parts with more than one supplier; no soldering, every
connection a screw terminal, plug or header; no specialist assembly skills; common
hand tools; and any part replaceable in five minutes.

<figure class="photo photo-right">
<img src="../build_photos/sukabumi/IMG_0048.png" alt="Components laid out on a workbench before assembly: mounting plate, DIN rail, fuse holders, the camera, the rain gauge dome, a small computer with its screw-terminal riser, a power converter, terminal blocks, a relay board, the modem and its antenna.">
<figcaption>The parts for one station. Nothing is fabricated and nothing is
single-source.</figcaption>
</figure>

Two stations were built. Sukabumi was installed in April and has run since. The
Jakarta station was finished and tested, but permission for its intended site did
not arrive, and it is still at Wisma PMI, unpowered since April.

## What we learned

Sukabumi is a volunteer-supported pilot. It is visited rarely and looked after
remotely by people doing it alongside other work. It was never built to production
standards of availability, and measuring it against an industrial instrument would
be the wrong test. The useful question is narrower: what does this design make
hard?

**A twenty-five dollar decision caused most of the outages**, and no single step
in the chain looks like a mistake. The USB storage drive caused a driver fault at
boot, so it was removed rather than fixed. That left the SD card as the only
volume, small enough to sit permanently at the level where it deletes old
recordings. That caused processing to fail on 43% of videos. Because the station
shuts down *after processing finishes*, a failed run meant it never shut down: it
stayed awake to the scheduling board's 25-minute backstop instead of stopping
after two minutes, roughly twelve times the energy for that cycle. Repeated
across a night, that flattened the battery — and a missed wake left the
next-startup alarm in the past with nothing to reset it, so one missed cycle
became days.

Two lessons follow. **Shutdown and startup are controlled by two different
systems and neither owns the whole cycle**, so when processing fails they fail
together. And **cheap parts can carry expensive operating costs** — the camera is
the other example, bought for about USD 60 against an alternative near USD 1,268,
meeting its specification but running a reseller's firmware with capability
removed, so recorded video cannot be fetched and capture falls back to a lower
quality live stream.

**The station cannot say what is wrong with it.** No interruption announced
itself. The record had to be reconstructed afterwards from the server database,
and a fault the system never reports cannot be found by watching for it. Related:
nothing compares what the station recorded against what the server received, so
data can go missing with no symptom at either end.

**Water level is the weakest measurement, and it fails in daylight.** The station
reads the level from the video. In a 200-capture sample, every rejection fell
between 06:00 and 19:00 and none at night. It matters more than a missing level
because level is computed first — when it fails the whole measurement is
discarded, including the surface velocity that succeeded — and because level feeds
the cross-sectional area, so an error in it scales the discharge figure directly.

![Captures counted by hour of day, and how confident each reading was against the
threshold at which a water level is accepted. Rejections peak in mid-morning and
again in mid-afternoon, with fewer in the early afternoon — the pattern a
sun-angle effect produces.](figures/fig2_optical.svg)

**The survey is unforgiving, and IPB fixed it.** Two RTK surveys on consecutive
days, with the same equipment and crew, disagreed with themselves by about 99 cm
horizontally and 139 cm vertically. Repeating a method that has failed reproduces
the same noise. IPB's total-station survey replaced the approach and is what the
station runs on today, at 3.7 cm RMSE.

**We had no station we could break.** Everything above was diagnosed on a solar
station, on a river, awake for tens of seconds at a time, that we could not touch.
We could not reproduce a fault, test a fix before committing it to a remote
machine, or tell the difference between a change working and the fault simply not
happening that week. Several of these diagnoses took months for that reason alone.
The Jakarta station was meant to be that test station and never became one.

## What we recommend

The full set is indexed at the back and detailed in the working list. The
headlines:

**Build the test station first.** A working station, mains-powered, always on,
somewhere someone can watch it, open it and break it deliberately. It is where a
fault is reproduced before it is diagnosed remotely, where a software change is
tried before it goes to a river, and where a server upgrade is rehearsed before it
obliges every station to follow. We would treat it as the first station a pilot
builds, not the last. **R36**

**Build monitoring for a fleet, not for one station.** What ORC-OS reports is
enough for a single station watched by the people who built it. An agency running
ten or fifty will need more: whether each station woke and shut down, time awake
per cycle, voltage and current together, free disk space against its deletion
threshold, captured against delivered, processing outcome per video, and last
contact per station. This is the highest-value work on the list. **R4–R7**

**Fit an independent water-level reference, and plan the survey as skilled work
from the start.** A level sensor or a staff gauge in the camera's view removes the
dependence on one optical method. And carry an independent field check of a
different kind, so a survey problem is found before the team leaves site. **R1,
R2, R19, R20**

**Give one process control of the whole sleep and wake cycle**, set the next wake
as part of shutting down, and make shutdown happen on a timer regardless of what
processing does. **R10, R12**

**Make mains power the default, and use solar only where mains is not
available.** An always-on station removes the wake cycle and, with it, most of
what is described above. **R11**

**Choose the site before anything else, and confirm permission in writing before
building for it.** The site fixes limits nothing later can undo: satellite
positioning for the survey, sun angle for the water level, and how much of the
flow the camera resolves. **R16–R18**

**Keep what works.** The five constraints above all. And **keep the spare
switched outputs** — the relay module has four channels, one drives the camera and
three are deliberately left free, wired and ready. That is what lets a station
drive a siren, a beacon or an alerting relay without reopening the design, and it
is what turns a measurement station into something a community can act on. We
would ask that any replication keeps that spare capacity rather than removing it
to save a few dollars. **R30–R35**

## The path forward

Our recommendation is that the next step is yours. The pilot produced knowledge
rather than a body of measurements, and knowledge is worth more as an input to
your own design than as a set of parts to copy. We would rather help you start
your own approach than hand you ours to maintain.

The Jakarta station is available and we would suggest a particular use for it: a
study and test unit. Open it, trace it, power it up, take it apart, and install it
locally if that is useful. What we would not recommend is putting it into service
as an operational station with expectations of availability, because it carries
the design this report recommends changing.

We are not proposing to build your stations. What we can offer is the record —
this report, the appendix, the operator and assembly documentation in English and
Bahasa Indonesia, the software, and the built station to take apart — along with
whatever else is useful: reviewing a design, answering a question about something
that surprised us, looking at data that does not behave. Sukabumi will keep
running and we will keep reporting what it does, including the parts that go
wrong.

## Questions for consideration

- Who should hold the Jakarta station as a study and test unit, IPB or BHLK?
- Can a staff gauge be read from the camera image accurately enough? If it can,
  R1 needs no separate sensor.
- Two interruptions remain unexplained, with the energy signature of the
  maintenance setting without that setting being on.
- How does the velocity measurement perform across the surface conditions the
  pilot sites present? This has not been characterised.
- Absolute discharge accuracy at Sukabumi, unresolved pending further survey work.

We expect your work to change some of what is written here.

## Index of recommendations

The full text of each is in `docs/RECOMMENDATIONS.md`. Measurements and
procedures are in the companion appendix.

<!-- INDEX:BEGIN -->

**What is worth keeping**

| | Recommendation |
|---|---|
| **R30** | Keep the five constraints |
| **R31** | Keep spare switched outputs, and design for community alerting |
| **R32** | Keep the camera factory-sealed |
| **R33** | Keep the recovery kit with the station |
| **R34** | Keep aligning with existing practice |
| **R35** | Keep the software stack open |

**Keep a station you can break**

| | Recommendation |
|---|---|
| **R36** | Put a test station on a bench, online, and keep it there |

**Choose the site before anything else**

| | Recommendation |
|---|---|
| **R16** | Treat site selection as a measurement decision, not a logistics one |
| **R17** | Confirm site permission in writing before any hardware is built for that site |
| **R18** | Engage local academic and basin partners in site selection |

**Improve measurement accuracy**

| | Recommendation |
|---|---|
| **R1** | Fit an independent water-level reference |
| **R2** | Plan the survey as skilled work from the start, and budget for it |
| **R19** | If a survey method fails once at a site, change the method |
| **R20** | Carry an independent check of a different kind, and use it before leaving site |

**Improve monitoring**

| | Recommendation |
|---|---|
| **R4** | Build a monitoring regime for a fleet, not a station |
| **R5** | Have the station send diagnostics; do not require a login |
| **R6** | Record voltage and current together |
| **R21** | Remove the rain gauge from the camera station |
| **R7** | Compare what was recorded against what arrived, automatically |

**Give one process control of the sleep and wake cycle**

| | Recommendation |
|---|---|
| **R10** | One process should control both shutdown and startup |
| **R12** | A processing failure must not prevent shutdown |

**Improve the server and the processing chain**

| | Recommendation |
|---|---|
| **R13** | Manage disk space before it stops the station working |
| **R14** | A failed water level should not discard the whole measurement |
| **R15** | Monitor the server as well as the station |
| **R22** | Plan video storage before the fleet grows |
| **R23** | Configuration edits must go through one interface |
| **R24** | Do not move bulk media through the API |

**Choose parts for operating cost, not just purchase price**

| | Recommendation |
|---|---|
| **R9** | These stations were built with low unit cost as the primary goal, and some of those choices raise operating cost at volume |
| **R25** | Three specific parts cost more than they saved |
| **R26** | Check the control interface before buying anything under software control |

**Choose the architecture to suit the site**

| | Recommendation |
|---|---|
| **R11** | Mains power should be the default. Use solar only where mains is not an option |
| **R8** | Consider putting the computer indoors, and decide deliberately where the processing happens |
| **R27** | A camera-only field node is the most deployable version of this system |

**Support local construction and maintenance**

| | Recommendation |
|---|---|
| **R3** | Specify interfaces, not part numbers |
| **R28** | Order locally-sourced parts weeks in advance, not on arrival |

**Divide responsibilities**

| | Recommendation |
|---|---|
| **R29** | Write the division of responsibility into the agreement |

<!-- INDEX:END -->

## Supporting documentation

Appendix sections: camera firmware limitations and the capture path (A1);
firmware replacement risks (A2); survey scope of work and acceptance checks (A3);
the availability record (A4); the water-level dataset (A5); data delivery
measurements (A6); and the power, scheduling and always-on comparisons (A7).

Operator and assembly documentation, in English and Bahasa Indonesia, is
available on request.
