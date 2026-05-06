# Lessons Learned — Indonesia Spring 2026 Deployment

Observations and recommendations for future ORC deployments. Updated during
the April 2026 field trip.

---

## 1. Procurement: Source all major components before travel

**What happened:** The Jakarta station was designed around a 12V LiFePO4
100Ah battery with a matched charger, providing ~20-25 hours of backup
power. This was to be sourced locally in Jakarta to avoid airline lithium
battery restrictions (1,280 Wh exceeds all carry-on and checked limits).

On arrival, procurement of the battery, charger, shielded Cat6 cable,
and other local items consumed most of Day 1-2. Finding the right
LiFePO4 battery with a compatible charger in Jakarta's electronics
markets (Glodok, Mangga Dua) proved harder than expected — most shops
stock AGM/lead-acid, and LiFePO4 options required cross-checking charger
chemistry compatibility. The time pressure led to a pivot: we purchased
a commercial APC 900VA AC UPS instead.

**Impact:** The commercial AC UPS is significantly less runtime than
the original LiFePO4 design would have delivered. The UPS is simpler
(standalone appliance, no DC integration, no charger wiring) but the
runtime tradeoff was driven by schedule pressure, not engineering
preference.

**Recommendation for next time:**
- Order the LiFePO4 battery and charger online (Tokopedia/Shopee) at
  least 1 week before arrival, with delivery to the PMI office or
  accommodation. Same-day/next-day delivery in Jakarta is reliable for
  items under ~$400.
- Alternatively, ship the battery separately via sea freight or courier
  if the project timeline allows (2-4 weeks lead time).
- Do not plan to walk into Glodok and buy a LiFePO4 battery same-day.
  The shops that carry them are specialist solar suppliers with limited
  stock and inconsistent hours.
- Budget a full day for local procurement regardless — even "simple"
  items (shielded Cat6, specific cable glands, stainless hardware) may
  require visiting 3-4 shops across Jakarta.

---

## 2. Procurement: Document specifications, not just product names

**What happened:** Many components that are commodity items in the US are
hard to find or come in different forms in Indonesia. Shielded Cat6 cable,
specific cable gland sizes, stainless steel fasteners, LiFePO4 batteries
with matched chargers — all required visiting multiple shops across
Jakarta. Products vary greatly between markets: an "outdoor Cat6 cable"
in Glodok may not be shielded, a "12V battery" defaults to lead-acid,
and wood dimensions follow metric conventions not imperial.

The local PMI team was willing to help source parts but didn't know
where to look for specialized items. They know where to buy general
hardware, but not where an electrician buys shielded structured cabling
or where a solar installer buys LiFePO4 batteries.

**Impact:** Procurement consumed most of Days 1-2 in Jakarta. We visited
Azko (hardware), Mangga Dua (cabling distributors), Glodok (electronics
and solar), and street-level hardware stalls — all spread across the
city. Items we expected to grab in an hour took a full day.

**Recommendation for next time:**
- Document **specifications**, not just product names. "Shielded Cat6
  outdoor cable, F/UTP, UV-resistant PE jacket, 305m box" is sourceable.
  "Cat6 cable" is ambiguous.
- For each item that must be sourced locally, identify the **trade** that
  would normally buy it, then ask the local team: "Where would an
  electrician go for structured cabling supplies?" or "Where would a
  solar installer buy LiFePO4 batteries?" This gets you to the right
  district/market faster than browsing general hardware stores.
- Prepare a **bilingual spec sheet** (English + Bahasa Indonesia) with
  the local term for each item. Include photos. Hand this to the local
  team in advance so they can pre-scout availability.
- For critical or unusual items, **order online** (Tokopedia/Shopee)
  with delivery to the PMI office 1-2 weeks before arrival. Same-day
  GoSend delivery in Jakarta is also reliable for items under ~$400.
- Accept that a full day of in-person procurement is unavoidable for
  bulky items (poles, lumber, concrete) and items that need physical
  inspection (cable quality, battery condition). Plan for it.

---

## 3. Design philosophy: Rigid reproducibility vs. field adaptability

**What happened:** The Indonesia deployment was designed as a specific,
reproducible BOM — exact part numbers, exact suppliers, exact wiring
diagrams. This works well when building in a home workshop with access
to DigiKey and Amazon. It breaks down in the field: the specified UPS
wasn't available, cable specs didn't match local stock, mounting
hardware had to be improvised from what the local hardware store
carried, and the APC 900VA UPS replaced a carefully designed 12V
LiFePO4 system because procurement time ran out.

Every substitution required re-evaluating compatibility, updating
documentation, and accepting tradeoffs (like reduced UPS runtime).
Some substitutions were straightforward (equivalent cable gland), others
changed the architecture (AC UPS vs. DC battery backup).

**Impact:** This tension will grow as ORC deployments scale to new
countries and contexts. A rigid BOM is great for the first build but
becomes a liability when the next team is in a different country with
different suppliers, different power standards, different climate, and
different local expertise. On the other hand, a fully flexible "use
whatever you can find" approach makes documentation, troubleshooting,
and remote support much harder.

**Recommendation — things to figure out:**
- Separate the design into **fixed interfaces** and **flexible
  implementations**. The interface (e.g. "12V DC bus at terminal block
  TB1, 10A capacity") is rigid. The implementation (which PSU, which
  battery, which UPS) is flexible as long as it meets the interface
  spec. Document the interface specs, not just the product choices.
- Define **substitution rules** for each component class: what
  parameters matter (voltage, current, IP rating, operating temp) and
  what don't (brand, form factor, mounting style). This lets a local
  team make informed substitutions without re-engineering the system.
- Create a **site adaptation checklist** — a structured process for
  walking through the design with local conditions in mind: What power
  is available? What's the climate? What can be sourced locally? What
  must be shipped? This replaces the current approach of discovering
  mismatches on arrival.
- Accept that **documentation will always lag field reality**. Build the
  docs to be updatable by the installing team (as-built markups, photo
  documentation of substitutions) rather than treating them as frozen
  specs.
- Consider a **tiered design**: a core platform (Pi + Witty Pi + G469 +
  camera + relay + software) that is the same everywhere, plus a
  site-specific power/enclosure/mounting layer that adapts to local
  conditions. The core ships from a central source; the site layer is
  sourced locally.

---

## 4. Architecture: Support camera-only deployments with remote compute

**What happened:** The current design co-locates the camera and compute
(Pi) in the same enclosure or on the same pole. This works when you
control the installation site end-to-end, but several real-world
situations push back on it:
- Sites where power is available for a camera but not for a full
  compute stack (e.g. a bridge pier with a single AC outlet)
- Sites where the camera must be far from any building (river bank)
  but compute could live indoors where it's cooler, drier, and easier
  to maintain
- Sites where a local partner already has IP cameras installed for
  other purposes and just wants ORC processing added
- Scaling: a camera + PoE injector is ~$150 and can be installed by
  anyone who can mount a security camera. Adding a Pi + Witty Pi +
  relay + modem + enclosure + solar triples the cost and complexity.

The split architecture design (`docs/SPLIT_ARCHITECTURE_DESIGN.md`)
was written during planning but hasn't been field-tested. The Jakarta
permission letter delay reinforced the value — if the camera were
already installed and streaming, we could have started processing from
a laptop at the PMI office on Day 1 instead of waiting for site access.

**Impact:** Co-located camera+compute is the simplest architecture for
a single site built by the design team. But for wide adoption — where
local partners install cameras and a central team provides processing —
a camera-only field node with remote compute is more practical. It
reduces what needs to happen at the river to mounting a camera and
running a cable.

**Recommendation — things to figure out:**
- Prioritize the split architecture as a first-class deployment mode,
  not just a future option. Field-test it at a convenient site.
- Define the minimum camera-only field node: PoE camera + PoE injector
  + power source + network backhaul. No Pi, no GPIO, no enclosure
  complexity.
- Remote compute can be a Pi indoors, a Docker container on an office
  machine, or a cloud VM. The software (`orc-capture` fetching RTSP
  over the network, `sensors_logger.py` reading an ESP32 HTTP bridge)
  already supports this with minor config changes.
- For sensors (rain gauge, temp), the ESP32 bridge concept in the split
  architecture doc is the right approach — keeps sensor reading local,
  exposes data over HTTP, compute fetches it.
- Camera-side SD recording + periodic clip fetch (also in the split
  architecture doc) decouples capture from network reliability and
  eliminates the real-time RTSP dependency.
- This aligns with lesson #3 (rigid vs. flexible): the camera-only
  field node is the "site layer" that adapts to local conditions, while
  remote compute is the "core platform" that stays standardized.
- **Piggyback on the security camera industry.** Every country has a
  local ecosystem for IP-based security camera deployment — installers,
  distributors, PoE switches, weatherproof housings, cable runs, pole
  mounts, and power solutions designed for the local environment. This
  supply chain already solves the hard problems (outdoor power,
  weatherproofing, cable routing, mounting) at commodity prices with
  local support. If ORC's field node is just a standard PoE IP camera,
  a local security camera installer can deploy it using their normal
  tools and suppliers. We don't need to ship enclosures, source
  LiFePO4 batteries, or explain DIN rail mounting — we just need to
  specify "install an IP camera here, pointed at the river, with
  network access." The ORC-specific value (processing, calibration,
  discharge calculation) lives entirely in the remote compute layer.

---

## 5. Sensors: Co-located rain gauges may not answer the right question

**What happened:** Both stations include a Hydreon RG-15 rain gauge
mounted on the same pole as the camera, measuring rainfall at the flow
measurement site. The assumption was that local rainfall is a useful
companion to flow data. But hydrologically, rainfall at the flow
measurement point primarily affects discharge *downstream* of that
point. What we actually want to understand is how rainfall *upstream*
in the catchment contributes to the flow we're measuring. A rain gauge
at the measurement site tells us about downstream impact, not upstream
cause.

**Impact:** The co-located rain gauge isn't useless — it provides local
weather context and helps interpret data quality (e.g. rain on the
camera lens, visibility). But it doesn't answer the key hydrological
question. Meanwhile, co-locating sensors with the camera adds wiring
complexity, more cable gland penetrations in the enclosure, UART/GPIO
dependencies, and more things to break in the field.

**Recommendation — things to figure out:**
- **Decouple the sensor package from the flow measurement package.**
  Treat them as two independent deployable units that work together but
  don't need to be co-located. The flow package is a camera + compute
  (or camera-only per lesson #4). The sensor package is a standalone
  weather/hydro station that can be placed anywhere in the catchment —
  upstream, at the site, at multiple points — wherever the data is most
  valuable.
- The sensor package maps naturally to the ESP32 bridge concept from
  the split architecture doc: a small, low-power, weatherproof unit
  that reads sensors locally and reports over HTTP/MQTT/cellular. No
  camera, no Pi, no ORC software. Just a telemetry node.
- This separation also simplifies the camera station. If the rain gauge
  and temp probes are removed, the camera station loses the SD16
  bulkhead, PG9 gland, UART wiring, 1-Wire wiring, and the
  `orc-sensors` service. It becomes closer to the "just a camera"
  deployment from lesson #4.
- For future deployments, ask: where in the catchment would sensor
  data be most valuable? Deploy sensor nodes there. Don't default to
  co-locating with the camera just because it's convenient.

---

## 6. Site permission must be confirmed before the build begins

**What happened:** Jakarta was built around a specific intended
installation site whose permission was understood to be pending but
expected. During the trip, that permission did not come through —
ultimately we returned to the US without deploying the Jakarta
station. The work was not wasted (the station is built and tested),
but the assumption that "we will sort the permission while we build"
turned out to be load-bearing in a way it shouldn't have been.

**Impact:** A built-but-not-deployed station is the worst outcome on
the procurement axis: the kit is paid for, packed, flown, and back —
without producing any data. The station now has to either be deployed
to a different site (with whatever site-specific design constraints
that brings) or warehoused until a site is identified. We are
re-engaging IPB (Bogor University) for site selection — which is the
right partner to find a viable location, but is a delay that should
not have been necessary.

**Recommendation for next time:**
- **Site permission is a P0 prerequisite, not a parallel workstream.**
  Build only against sites whose installation permission is in writing.
  If the partner organization can't get a written permission letter
  before the build begins, design to not need permission at that site
  (e.g. install on the partner's own premises or a public bridge with
  a clear regulatory path) — or pick a different site.
- **Engage local academic / domain partners for site selection.** PMI
  has the deployment relationships but not necessarily the
  hydrological judgment for "which urban canal would actually be
  useful to monitor." A domain partner like IPB or another local
  university adds the rigour and reduces the chance that a politically-
  available site is chosen over a hydrologically-useful one.
- **Treat the bench-built station as a soak rig.** Once it's clear a
  station won't deploy on the planned trip, rotate it to "extended
  bench / long-term burn-in" mode rather than packing and flying it.
  Months of thermal cycling and software soak time on a bench is more
  valuable than a round-trip flight.
- This pairs with lesson #4: a camera-only field node lowers the
  permission ask from "build out an enclosure with a battery and a
  modem" to "mount an IP camera." Many sites that won't approve a
  full kit will approve a camera. Designing for camera-only deployment
  expands the set of permission-feasible sites.

---

## 7. Repeat surveys with the same equipment / methods will reproduce the same noise

**What happened:** The Sukabumi RTK survey on day 1 produced a check-
point spread of ~99 cm horizontal / ~139 cm vertical between repeat
occupations of the same physical markers — well outside the 3 cm / 4 cm
RTK gate. We re-occupied the next day, with the same Emlid Reach RS+
rover, the same temporary base setup, and the same field crew. The
day-2 survey produced exactly the same noise level. The day-1 → day-2
drifts on individual same-marker re-occupations were even worse:
GCP3 drifted 89 cm, GCP4 drifted 75 cm, GCP2 drifted 29 cm. The data
is salvageable for a 6-GCP subset calibration via subset search
(4.6 cm RMSE), but is unfit for certified discharge measurement.

**Impact:** Two field days of surveyor time produced one survey of
borderline-usable quality. The salvage calibration is sufficient to
demonstrate the pipeline end-to-end at the site, but the absolute
discharge numbers it produces inherit a multiplicative scaling error
of similar magnitude to the geometric noise. We are now arranging an
IPB-led total station survey as the recovery path — at the cost of
several weeks of additional schedule slip and a separate budget line.

**Recommendation for next time:**
- **If RTK fails once at a site, switch methodology — do not re-try
  RTK with the same equipment.** The most likely failure modes
  (poor base-station coordinate quality, multipath at the receiver,
  ionospheric activity, ambient RF interference, sky obstruction)
  all reproduce day-to-day at the same site with the same gear.
  Doing the same thing twice is not "verification"; it is gathering
  the same evidence twice. If the methodology has produced unusable
  results once, the next attempt must change something material:
  different equipment (dual-frequency rover, longer base-station
  occupation), different correction source (network NTRIP instead of
  temporary base), or a different methodology entirely (total station,
  conventional levelling).
- **Carry an independent check-method.** If RTK is the primary, the
  check-method should be something orthogonal — a tape-measured
  cross-section between two GCPs, a clinometer-and-rod elevation
  check, a known-elevation reference benchmark within the camera
  view. The check needs to fail-fast on bad RTK data while still in
  the field, not weeks later in post-processing.
- **The auto-fit salvage pipeline buys us time, but is not a substitute
  for a clean survey.** The pipeline finds the subset of GCPs that
  agree, but every flow number it produces still inherits the survey's
  underlying noise floor. Treat salvage outputs as "this site is
  alive and producing relative data" rather than "this site is
  certified for discharge publication."
- For the next site: budget for a professional surveyor up front
  (see `survey/outsourced_survey_brief.md` for the SOW template). The
  cost of a vendor survey (Rp 5–15 M / ~$300–950 USD per site) is
  small compared to the cost of an unusable in-house survey plus
  the recovery survey afterward.

---

## 8. Investigate a self-contained, networked, solar-powered rain gauge

**What happened:** The Hydreon RG-15 is co-located with the camera station
at Sukabumi because it's convenient — the Pi is already there, the UART is
already wired, it shares the solar budget. But the rainfall regime that
matters for a river-gauging station is the *catchment*, not the point
where the camera happens to be. A single rain gauge bolted to the camera
pole tells you about rainfall at the camera, which may be many kilometers
downstream of where the water actually fell.

**Impact:** Rainfall data from the station is a point measurement with
limited hydrologic value. For discharge modelling, event attribution, or
flood-warning applications, we'd want distributed rainfall across the
catchment — which the current architecture doesn't support.

**Recommendation for next time:**
- Investigate a self-contained networked rain gauge node: solar panel,
  small battery, RG-15 (or similar optical gauge), a low-power MCU, and a
  LoRa / LTE-M / NB-IoT radio. Target BOM in the $200–$400 range.
- Design as part of a **store-and-forward mesh**: gauges that can't reach
  the internet hop through neighbors until one node does, so a single
  cellular / WiFi gateway covers the whole catchment. LoRaWAN is the
  obvious starting point; Meshtastic is worth a look for ad-hoc meshes
  without a LoRaWAN gateway.
- Keep the protocol plain and idempotent (retry-safe timestamped
  rainfall totals) so packets dropped or duplicated in the mesh don't
  corrupt the time series.
- Treat the camera station as one consumer of rainfall data, not its
  host. The gauge network and the camera station are independent
  subsystems that happen to feed the same pipeline.
- Related: this also addresses lesson #5 — decoupling sensing location
  from camera location is the same architectural move applied to the
  catchment scale instead of just a few meters of cable.
- **Match the existing station style and footprint.** The catchment
  gauge nodes should look like smaller siblings of the camera station:
  same enclosure family, same pole-mount hardware, same cable-gland
  conventions, same visual identity. Same physical footprint or
  smaller. Benefits: spare parts and tools overlap, PMI staff can
  service both without re-training, and the network reads as one system
  instead of a grab-bag of third-party boxes. Design the gauge node
  within that constraint rather than optimising each node in isolation.
- **Match the ombrometer standard for manual gauges.** PMI and the
  Indonesian meteorological agencies (BMKG) use the ombrometer as their
  standard manual rain gauge; daily totals across the country are
  reported in those units and against that resolution. The automated
  node should be able to reproduce an ombrometer reading at the same
  site within the ombrometer's tolerance, so that its output is
  directly interchangeable with the existing manual-reading record
  and so historical time series stitch cleanly. That means: match the
  typical 0.1–0.2 mm resolution and the 24-hour totalling convention,
  and log in a form that an operator comparing to a manual ombrometer
  reading can reconcile without a conversion step.
- Note: **BMKG owns rainfall, not river stage or discharge.** Rain
  gauge networks fall under BMKG; river-level and flow monitoring is
  a separate agency (Kementerian PUPR / Ditjen SDA / BBWS) — see
  lesson #9. Any rainfall node in this design should target BMKG
  ingest pipelines and ombrometer-equivalence; level/flow nodes
  target PUPR/BBWS pipelines.

---

## 9. Explore a cheaper river-level / stage sensor with public-alert relays

**What happened:** Operators in the region currently run German diver-style
pressure-transducer gauges (Schlumberger/van Essen, OTT, Seba and
similar) for water level and derived flow, at roughly **USD ~$1,000 per
station**. That includes the vented transducer, cable, barometric
reference, and usually a logger/telemetry unit. It's reliable, accurate,
and well-understood — but it's also the dominant cost of a gauging
station and puts density at a price ceiling. If a watershed wants 20
stations, that's $20k just in level sensors.

**Impact:** Price pressure directly limits how dense a hydrometric
network can be. Every station that a community can't afford is a
catchment where floods aren't measured or warned on.

**Indonesian standards context** (research summary — full report at
`spring_2026_ID/research/indonesia_hydrometric_standards.md`):

- **Responsible agency is PUPR, not BMKG.** Water-level and discharge
  monitoring in Indonesia is owned by Kementerian PUPR / Ditjen SDA,
  executed through 34 **BBWS/BWS** river-basin offices, with
  **PUSAIR** (Bandung) running calibration and standards. BMKG is
  atmospheric/rainfall only (see lesson #8). No public evidence of
  BMKG-operated rated river discharge stations.
- **Automatic water level (AWLR / pos duga air telemetri).**
  International dominant brand: **OTT HydroMet** — PLS/PLS 500
  pressure probe, RLS radar, CBS bubbler, Thalimedes shaft encoder,
  netDL 500/1000 data logger. Domestic alternatives: **IDDATA RL03**
  radar + GSM, catalogued on INAPROC at **~Rp 58 M (~USD 3,600) ex-VAT**;
  **Mertani** (radar/ultrasonic); **PT. Tatonas** (ultrasonic and
  float/encoder, projects at BBWS Pemali Juana). Campbell Scientific
  CR300/CR1000 loggers present but secondary to OTT netDL.
- **Manual staff gauge.** Called **papan duga air** (or *peilschaal*).
  Enameled-steel or fiberglass board, centimeter resolution, zero
  referenced to a local benchmark. Read three times daily (07:00,
  12:00, 17:00) by a contracted community observer (**juru pengamat
  hidrologi**). Data recorded on printed PUPR forms.
- **Discharge is rating-curve derived.** BBWS does *not* operate
  continuous-discharge sensors at most stations. Standard cycle: (1)
  continuous stage record, (2) 3–5 current-meter gaugings per year,
  (3) fit **lengkung debit** (rating curve) from ≥30 Q-H pairs,
  (4) apply curve to stage record to produce Q. Gauging instruments:
  **OTT C31 propeller**, **OTT MF Pro electromagnetic**, **SonTek
  FlowTracker 2** (handheld ADV, wading/bridge), **SonTek RiverSurveyor
  M9 ADCP** (boat-mounted, for flood stages).
- **Binding standards.** **SNI 8066:2015** — current binding standard
  for current-meter discharge. **SNI 03-2414-1991** — foundational.
  **WMO-No. 168** (Guide to Hydrological Practices) — international
  baseline referenced in PUSAIR materials.
- **Telemetry pipelines.** National portals: **SIHLSDA** / **SIH3** /
  **SIHKA**. Typical ingest: CSV or HTTP POST with timestamp, station
  ID, TMA (tinggi muka air) in cm or m. GSM/GPRS transmission is the
  Java/Sumatra norm.
- **The $1k diver-style price point referenced above is the informal
  regional market price**, not confirmed in Indonesian government
  tenders in this research. The cheapest confirmed government-catalog
  entry is the IDDATA RL03 radar at ~USD 3,600. So "undercut the
  diver" and "undercut the government catalog entry" are two different
  targets, both worth pursuing.

**Recommendation for next time:**
- Investigate a level-sensor station with a BOM target **well under
  $1,000**. Candidate technologies: non-contact ultrasonic (MaxBotix,
  Senix), radar (Acconeer A121, Seeed / Tl. mmWave modules), low-cost
  vented pressure transducers (Keller 26Y / 36X lines), or a
  camera-based staff-gauge read (re-using the ORC camera hardware we
  already deploy).
- **Interoperability, not sensor principle, is the acceptance test.**
  To be additive to BBWS time-series: output in meters above the
  local peilschaal zero; timestep 15-min minimum (5-min preferred for
  flood-warning ingest); CSV or HTTP POST in SIH3/SIHLSDA format;
  paired daily reading against a manual papan duga air during
  commissioning. Calibration verifiable against PUSAIR's KAN-accredited
  lab (0–300 cm pressure range). Any sensor principle — pressure,
  radar, ultrasonic, camera-based staff-gauge read — is acceptable if
  it meets those interop requirements.
- **Discharge is supplementary, not replacement.** Our ORC-derived
  surface velocity feeds Q via an index-velocity or rating relationship;
  it supplements the BBWS rating curve, not replaces it. Uncertainty
  should be documented per SNI 8066:2015 / WMO-No. 168 Ch. 5 for the
  output to be accepted alongside BBWS data.
- **Expose open relay outputs for public alerting.** The station should
  have 1–2 dry-contact relay outputs (or optoisolated GPIO) wired to
  screw terminals, triggerable by local threshold rules without a
  round-trip to a central server. Typical wired loads: siren driver,
  strobe, SMS modem, public-address trigger, downstream-gate SCADA
  input. Local thresholds survive WAN outages — which is exactly when
  public alerting matters most.
- Keep the alert rule engine local and simple — e.g. "relay 1 closes if
  stage > X for > Y minutes" — and make the thresholds configurable
  without a firmware rebuild. The central server should be able to
  *push* threshold updates but the relay logic must keep running when
  it's unreachable.
- Document the safety boundary clearly: this is a *gauging* relay, not
  a certified safety-of-life alarm. Publicly-facing alerts need a human
  in the loop or a redundant certified path. The relays lower the
  latency for that human, they don't replace them.

---

## 10. Split responsibilities: university owns the technology, Red Cross owns deployment and operations

**What happened:** Technology development and field deployment are two
very different disciplines, and one organisation rarely excels at both.
Through this trip it's become clear which side each partner is best
positioned to own: the university is where sensor design, software
engineering, calibration methodology and research iteration happen;
the Red Cross (PMI in-country, and the broader IFRC network) is where
local language, community trust, long-term site presence, volunteer
networks, and operational continuity live.

**Impact:** When responsibilities overlap or shift ad-hoc, things fall
between the cracks — field diagnostics land in research inboxes where
they wait for a PhD schedule, or the research team gets pulled into
running day-to-day station support they're not set up for. Both sides
move slower than they should.

**Recommendation for next time:**
- **University role — technology.** Hardware and software design, BOM
  definition, firmware, ORC pipeline and calibration methodology,
  training materials, and the R&D pipeline for future sensors
  (lessons #8 and #9 sit squarely here). Produces reproducible
  station designs and documented procedures the operator can rely on.
- **Red Cross role — deployment, support, and operations.** Site
  selection within the Red Cross mission scope, stakeholder
  engagement, on-site installation and maintenance, spares inventory
  at the local chapter, staff training, incident response when a
  station misbehaves, and the data-to-decision loop when the station
  output feeds a humanitarian action. PMI is the primary point of
  contact for in-country questions.
- **Scope the Red Cross role to mission-aligned use cases.** Flood
  warning, disaster preparedness, community-health-adjacent water
  monitoring — yes. General-purpose hydrometric networks for
  research-only or commercial purposes — no; those need a different
  operator (or a layered agreement where the Red Cross gets value in
  exchange). This boundary keeps the Red Cross's scarce operational
  capacity pointed at humanitarian outcomes.
- Write this split into MoUs and deployment plans explicitly — don't
  leave it as tribal knowledge between the individual collaborators
  who happen to know each other today. The point is the model
  survives staff turnover on either side.
- Keep a lightweight joint forum (monthly call, shared issue tracker)
  where edge cases get adjudicated. Not every incident sorts cleanly;
  the forum handles the grey zone and updates the written split as
  patterns emerge.

---

## 11. (Template for future entries)

**What happened:**

**Impact:**

**Recommendation for next time:**

---

*Last updated: 2026-05-06*
