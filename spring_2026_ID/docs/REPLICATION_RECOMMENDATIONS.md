# OpenRiverCam in Indonesia: What the Pilot Taught Us, and the Path Forward

**Version:** 2026-08-31 (draft for internal review — not yet circulated)

**Partners:** Palang Merah Indonesia · Institut Pertanian Bogor · Balai Hidrologi
dan Lingkungan Keairan · American Red Cross

**Prepared for:** IPB and BHLK, following the PMI / IPB / BHLK meeting at
Sukabumi, 21 August 2026.

**Reading time:** about twelve minutes.

**Companion document:** *Appendix — Recommendations for Replication of the
OpenRiverCam Station Design*, written for the engineers who will build, procure
and operate the units. Every measurement, interface specification and procedure
referred to below is held there.

---

## The pilot, and what we think comes next

The pilot has been a good experience. It put a station in the water, gave us four
months of behaviour to learn from, and produced something more valuable than
either: a working relationship between PMI, IPB and BHLK that did not exist
before. Colleagues who had not worked together now share a problem, a site and a
vocabulary for both. We would do it again.

**Our recommendation is that the next step is yours.** Not because the partnership
has run its course, but because of what the pilot actually produced. It produced
knowledge rather than a body of measurements, and knowledge is worth more to you
as an input to your own approach than as a set of parts to copy. We would rather
help you start your own design than hand you ours to maintain.

This document is that knowledge, offered in full and including the parts that
reflect badly on choices we made. It is written to give an accurate basis for your
decision rather than an encouraging one.

At Sukabumi on 21 August, BHLK offered to build one to three stations as a pilot,
offered server capacity for the data, and recommended moving the present site to
open ground. We welcome all three offers, and this document responds to them and
to the request to study the current design.

**The scope is the technology only.** We describe the station as built, what four
months in the field revealed about it, and what we would do differently. We do not assess what the resulting data is fit to
support, or what accuracy any particular application requires. Those judgements
belong with IPB, BHLK and their federal partners. Where a measurement requirement
appears below, it is one recorded from you rather than proposed by us.

**The evidence is thin, and we ask you to treat it as thin.** One station, on one
river, observed across part of one season. A second station was built but never
installed. The calibration the station runs on today was recovered from a survey
that failed. What the deployment has produced so far is knowledge about the
design, not a body of measurements.

## Why a low-cost station is worth studying

A river gauge is only useful if there are enough of them. How many stations an
agency can afford determines how much of a catchment it can observe, and that is
a different question from how good any single station is.

The station described here came to **USD 1,340 in materials**. That figure is the
electronics and enclosure only: Sukabumi already had a 200 W panel and a 50 Ah
battery on site, so no solar array is included in it, and a new solar site would
have to add one. A mains site does not. The lowest-cost automatic water-level
station we could confirm on the Indonesian government e-catalogue is the
domestically assembled IDDATA RL03 with GSM telemetry, at **Rp 58,000,000,
approximately USD 3,600 before VAT**, and it measures stage only. The comparison
is not like for like: the RL03 is a supported commercial instrument, and this is a
pilot-stage assembly. The reason it is worth stating is that at this price a basin
authority can consider a network where it might otherwise consider a single
gauge.

That possibility is the whole of the argument for studying the design. Everything
else in this document is about whether the thing can be made reliable enough to
deserve it.

## What is being offered for study

A camera on a pole watches the river. A small computer in a weatherproof box
turns the video into a water level and a discharge figure, and a mobile data link
sends both, with the video, to a server. At Sukabumi the station runs on solar
power and wakes on a thirty-minute cycle: it starts, captures, processes, uploads,
and shuts down again.

![The camera on its pole sends video to the station computer, which derives water
level and discharge; both travel over the mobile network to the server. The three
things the computer depends on are shown beneath it. The whole sequence happens
inside a waking period of about two minutes, of which the first thirty to sixty
seconds is spent waiting for the camera to start.](figures/fig1_system.svg)

Five constraints governed every choice of part, and they are the reason the design
can be copied at all: commodity electronics with more than one supplier; no
soldering, with every connection made by screw terminal, plug or header; no
specialist assembly skills; common hand tools; and any part replaceable in five
minutes.

<figure class="photo-row">
<img src="../build_photos/sukabumi/IMG_0048.png" alt="Components laid out on a workbench before assembly: enclosure mounting plate, two lengths of DIN rail, three fuse holders, the camera, the rain gauge dome, a small computer with its screw-terminal riser, a power converter, terminal blocks, a relay board, the mobile data modem and its antenna.">
<img src="images/sukabumi/complete-system-before-power.png" alt="The same components assembled onto the mounting plate and wired, with a bench power supply alongside reading 12.08 volts.">
<figcaption>The parts for one station, and the same parts wired onto the mounting
plate under bench power. Nothing here is fabricated, and nothing is
single-source. A technician with a screwdriver can replace any of it.</figcaption>
</figure>

Those constraints are what make local repair possible, and local repair is what
keeps a station working in a place where the nearest specialist is a day away. We
would ask you to hold them even where they are inconvenient.

## What four months in the field taught us

Three design gaps matter more than the rest. Each is something the station should
have been able to do and could not, and for each we say what we would build
instead. The measurements behind them are in the appendix, recorded there as known
failure modes of this design rather than as a performance record.

**The station cannot report its own condition.** When it stopped, it stopped
quietly. Nothing in the design let an interruption announce itself, so periods
when it was not running had to be reconstructed afterwards by querying the server
database. A fault the system never reports cannot be found by watching for it, and
no amount of attention from the field makes up for a machine that cannot say what
is wrong. There is a related gap: a maintenance setting that suppresses recording
and holds the processor awake has no time limit and raises no alarm, so it can
stay on without anyone being told.

*What we would build instead:* the station reports its own state on every waking,
and any mode that suppresses data or raises energy use expires on its own and
raises an alert while it is set. Health reporting belongs in the requirements
alongside the measurement, not added afterwards when something has already gone
quiet. That is R4 and R5.

**Nothing reconciles what was recorded against what arrived.** The station knows
what it captured and the server knows what it received, and no part of the design
compares the two. Video and sensor readings also travel by separate paths and fail
separately, so neither confirms the other. Data can go missing without producing a
symptom at either end, which is the kind of loss that is found late or not at all.

*What we would build instead:* a scheduled comparison of the station's own record
against the server's, raising a difference as an alert. It is a small piece of
software and it should have been in the first version. That is R7.

**Water level is read from the image, and daylight defeats it.** Sukabumi has no
water-level sensor and derives the level from the video. In a sample of 200
captures every rejection fell between 06:00 and 19:00, and none at night. Because
the water level is worked out first, a daytime rejection costs the whole discharge
measurement and not only the level.

*What we would build instead:* an independent water-level reference — a sensor, or
a staff gauge inside the camera's view — so the measurement does not depend on a
single optical method succeeding. Deriving the level from the image is a good
capability to have and a poor one to rely on alone. That is R1, and it is the
change with the clearest benefit.

![Captures counted by hour of day, and the confidence score of all 200 captures
against the threshold at which a water level is accepted. Rejections peak in
mid-morning and again in mid-afternoon, with fewer in the early afternoon — the
pattern a sun-angle effect produces and a general brightness effect would
not.](figures/fig2_optical.svg)

The cause is most likely reflected sunlight, and that reading is well supported by
the shape of the day, but it is not settled. The recommendation below rests on the
failure, which is measured, and not on the explanation.

## Eleven things we would do differently

These are offered as input to your design rather than as corrections to ours. Some
will not apply to the approach you choose, and we would not expect them to be
adopted as a set. The appendix gives the observation behind each and the detail
needed to act on it. They fall into three groups, and the first two decide whether
a station produces information anyone can use.

**Let the station account for itself.** A station that cannot report its own
condition cannot be looked after from a distance, and travelling to a river to
learn whether a computer is running is an expensive way to find out. Nothing in
this group is difficult or costly. The maintenance setting described above was
readable remotely the whole time, and no software ever asked. **R4, R5, R6,
R7.**

**Make the measurement trustworthy.** Two changes carry most of the weight here.
The station needs an independent water-level reference (**R1**) — a sensor, or a
staff gauge inside the camera's view tied to the same *papan duga air* zero BBWS
uses — because without one it measures dependably only at night.

And the survey should be planned as professional work from the start (**R2**),
because the surveyed shape of the riverbed is an input the processing cannot
recover. We learned this the hard way, and IPB fixed it. Two RTK surveys at
Sukabumi on consecutive days, with the same equipment and the same crew, disagreed
with themselves by about **99 cm horizontally and 139 cm vertically**, and nothing
in our workflow caught it on site. **IPB's total-station survey replaced that
approach and is what the station runs on today** — a camera configuration built
from IPB data alone, fitted at **3.7 cm RMSE** against a 5 cm target. The lesson
for a new site is to plan for that standard of survey from the beginning rather
than arriving at it after two failures, and to carry an independent field check of
a different kind so a survey problem is caught before people go home.

**Make the units buildable and maintainable in Indonesia.** BHLK will buy in
Indonesia under Indonesian procurement rules, so substitution is the expected
case rather than a risk to be managed. Documenting which properties bind and
which do not (**R3**) is what allows that without every substitution becoming a
question referred back to us. **R8** and **R11** change where the equipment lives
and how it is powered, and both make the station easier to keep running; **R9**
and **R10** are about how parts are chosen and one board fewer.

| | Change | What it buys | Cost |
|---|---|---|---|
| **R1** | Fit an independent water-level reference | Measurement through the day, not only at night | A level sensor, or a staff gauge in view |
| **R2** | Commission a professional survey first | The one input the processing cannot recover | Rp 5–15 million per site |
| **R3** | Specify interfaces, not part numbers | Local procurement without referring back to us | Documentation only |
| **R4** | Health reporting and mode alarms as requirements | The station reports its own condition | Negligible |
| **R5** | Station sends diagnostics; no login required | Support that works inside a short waking period | Small |
| **R6** | Record voltage and current together | Separates a failing battery from a heavy load | A current-sensing module |
| **R7** | Compare recorded against received, automatically | Loss is noticed rather than discovered later | Negligible |
| **R8** | Put the computer indoors | Removes it from heat, humidity, dust and travel | Designed, not yet field tested |
| **R9** | Budget per station; check the interface before buying | Keeps a network affordable without hidden costs | Screening effort |
| **R10** | Use the computer's own clock where the site allows | One less board to fail | Saves about USD 50 per station |
| **R11** | Build on mains and leave it running, where continuous reporting is wanted | Removes most of the gaps above | No solar array to buy; constrains siting |

**R8 deserves a note, because it is the least proven and possibly the most
useful.** Camera and sensors stay at the river; the computer runs at a BHLK or IPB
facility over a network link. That reduces the work at the riverbank to mounting a
camera, puts the computer where temperature, humidity, dust and access are
controlled, and lowers what has to be asked of a landowner. Where the field unit
is a standard security camera, installation and support also fall within a supply
chain that already exists across Indonesia. Stated plainly: this arrangement is
designed and **not yet field tested**. We offer it as the pilot's first
experiment, not as a proven alternative.

![As built, the camera, computer, modem and power system all sit in one enclosure
at the riverbank, and all of it is in the weather. As proposed for the pilot units,
only the camera stays at the river. The right-hand arrangement is designed and not
yet field tested.](figures/fig3_configurations.svg)

### One lesson about method

<figure class="photo photo-right">
<img src="images/components/annke_c1200_camera.png" alt="The camera as delivered, on a workbench mat with its mounting hardware, waterproof cable boot and printed manual.">
<figcaption>Capable hardware, running a reseller's version of the manufacturer's
software. Every limitation we met came from that software rather than from the
optics or the sensor.</figcaption>
</figure>

The budget was applied part by part: for each function, the cheapest item meeting
the requirement. That produced a working station at USD 1,340, and it has one
failure this deployment demonstrated. **It prices each part against its
specification sheet, not against what that part's limits cost the rest of the
system.**

The camera is the clear case. At about USD 60 against a professional alternative
near USD 1,268, it was not really a choice. The unit meets every line of its
specification and still costs the system a fifth of its video quality, a slower
measurement cycle, and thirty to sixty seconds of battery on every waking — none
of which appeared in the comparison that selected it. Its light also fires at full
brightness whenever it starts and cannot be turned off, which at the present site
is forty-eight flashes a day. That is a reason to weigh siting and cycle length,
and not only the power budget.

## Building and looking after the units in Indonesia

The design was made to be built by people who are not electronics specialists,
with tools they already own. That intent only becomes real if the parts can be
bought locally and the documentation supports substitution, which is what R3
addresses.

For maintenance, the pattern that has worked is a small stock of spares held at
the local PMI chapter, so a failure is a part swap rather than a shipment. Where
the field unit is a standard security camera (R8), installation and support fall
within a supply chain that already exists across Indonesia, with a deeper set of
suppliers than specialist hydrometric equipment.

We would rather help build the capacity to maintain these stations than remain the
place they are sent when they break.

## Hosting the data in Indonesia

BHLK's offer of server capacity suits the pilot well, and holding the data in
Indonesia carries a clear benefit for a government-partnered deployment. The
server software is packaged for straightforward installation. Two constraints are
worth designing for rather than discovering: the video store and the database must
share one filesystem, so plan storage as a single volume; and the server and
station software versions are tied together, so a server upgrade obliges the
stations to follow, which a remote station cannot do on demand.

We would suggest running the BHLK instance alongside the existing one, receiving
the same data, until it has completed a full operating cycle including an upgrade.
It would also be worth agreeing in writing, in advance, where the authoritative
copy sits, who administers it, who has access, and what the retention policy is.

## Choosing the sites

BHLK's recommendation to move to open ground free of obstruction is supported, and
the field record adds independent evidence for it. An open site helps with three
separate problems at once: satellite positioning is degraded by nearby buildings,
which is among the leading candidate causes of the survey trouble at the present
site; the angle between sun, water and camera can be chosen to avoid the daytime
failure through more of the day; and the view across the section determines how
much of the flow the camera can resolve.

Two things to plan for. A move costs a fresh survey and a fresh calibration, not
only a physical relocation, and the survey is the expensive part. And site
permission should be settled before a unit is built for a particular site: a
complete station was built and tested for an intended Jakarta site whose
permission was expected and fell through during the April visit. We would not
build to a specific site again before being told the permission is in place.

**That station is still available, and we would suggest a particular use for it.**
It is complete and software-ready, held at Wisma PMI in Jakarta, and has not been
powered on since April. The plan had been to transfer it to IPB to install at a
river.

We would suggest it serves you best as a study and test unit: a complete working
example to open, trace, power up, take apart and rebuild while your own units are
built — and, if that is useful, installed somewhere convenient and local so it can
be exercised against real water. That answers the request recorded at the meeting,
access to the current design in order to study it, with hardware rather than only
with documents.

What we would not recommend is putting it into service as an operational station
with expectations of availability and consistent data. It was built to the design
this document recommends changing, so it carries the problems described above.
Those are acceptable in something you are learning from, and a poor foundation for
a record anyone depends on.

## Working together

The division recorded at the meeting matches what this project's experience
supports. Technology development and field operations are different disciplines,
and where the responsibilities blur, field problems land in research inboxes and
wait.

- **BHLK** — data processing, conformance with standards, and the route to
  acceptance within PUPR data systems. Offers server capacity.
- **IPB** — design, calibration methodology, training material, and the
  development path for future sensor types.
- **PMI** — user of the information, and the operational side: installation and
  maintenance, siting within its mission, response when something fails, and
  spares held at the local chapter.

Two suggestions offered for your consideration. Writing the split into the
collaboration agreement, rather than holding it as an understanding between the
people currently working together, so that it survives staff changes on any side.
And keeping a light joint forum — a regular call, or a shared issue list — for the
cases that do not sort cleanly into one of the three roles.

The commitments this implies for PMI have not been discussed with PMI National
Headquarters. They are recorded here as the meeting recorded them, not as an
agreed position.

## Meeting the conditions for the data to be accepted

We reproduce the conditions the BBWS record is kept to because they constrain the
design, the parts list and the installation: a unit lacking the necessary hardware
cannot meet them afterwards. Whether the output should be accepted, and on what
terms, is not ours to assess.

Stage in metres above local datum, referenced to the same *papan duga air* zero,
at 1 cm resolution or better. A time step of 15 minutes at minimum and 5 minutes
preferred for SIH3 and SIHLSDA ingest; the station as built reports every 30
minutes. Discharge in m³/s with uncertainty documented following **SNI 8066:2015**
principles, or WMO-No. 168 Chapter 5. A standard transfer format carrying value,
timestamp and station identifier. Paired daily manual readings against the
co-located staff gauge during commissioning. A site report recording coordinates,
local benchmark, gauge zero elevation, sensor height and the calibration record.

Documenting uncertainty is the condition that bears hardest on the equipment. A
steady offset can be corrected afterwards. Error that varies from point to point
across the section cannot: there is no single correction factor, and it enters the
uncertainty rather than being removed from it. That is why R2 and R1 are not
separable from these conditions, and why neither can be added cheaply once a unit
is installed.

## Questions for consideration

We offer these as open, because they are.

- Who should hold the Jakarta station as a study and test unit? It was to
  transfer to IPB for deployment. Whether IPB or BHLK is better placed to hold it
  is a question for the two of you, and we will support either.
- Can a staff gauge be read from the camera image accurately enough? If it can, R1
  needs no separate sensor and the station aligns directly with BBWS practice.
- Two interruptions remain unexplained. They carry the energy signature of the
  maintenance setting without that setting being on, which suggests something else
  can make capture fail in the same way.
- Whether the recovery-voltage threshold bounds how long an interruption lasts.
  One recovered unattended in 6.5 hours against a prior range of 21 hours to 9.3
  days. One observation is not a result, and a competing reading is that the
  threshold may hold the station off rather than bring it back.
- How the velocity measurement performs across the surface conditions the pilot
  sites present. Not characterised at Sukabumi; it should be measured rather than
  assumed.
- Absolute discharge accuracy at Sukabumi, unresolved pending the survey and not
  resolvable without it.

We would welcome your reading of these, and we expect your work to change some of
what is written above. That is the point of handing it over rather than handing it
down.

## What we can offer from here

We are not proposing to build your stations. What we can offer is the record: this
document, the appendix behind it, the operator and assembly documentation in
English and Bahasa Indonesia, the software, and the built station at Wisma PMI to
take apart. Beyond that, whatever is useful — reviewing a design, answering a
question about something that surprised us, looking at data that does not behave.

Sukabumi will keep running, and we will keep reporting what it does, including the
parts that go wrong. If that is useful to your design work, it is yours.

The pilot did what a pilot should do. It found the problems while they were still
cheap, and it introduced three organisations to one another. The next station in
this story should be one you designed.

## Supporting documentation

Measurements, interface specifications and procedures are in the companion
appendix: the camera firmware limitations and capture path (A1); firmware
replacement risks (A2); survey scope of work, acceptance checks and contract terms
(A3); the availability record and maintenance-mode statistics (A4); the
water-level dataset (A5); data delivery measurements (A6); and the power,
scheduling and always-on comparisons (A7).

Operator and assembly documentation, in English and Bahasa Indonesia, is available
on request.
