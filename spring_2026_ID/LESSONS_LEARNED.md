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

**Impact:** The APC 900VA UPS provides ~3-5 hours of backup at our
measured 12-15W system load, compared to the ~20-25 hours the original
LiFePO4 100Ah design would have delivered. That's a significant
reduction in outage tolerance for a site in Jakarta where grid power is
unreliable. The UPS is simpler (standalone appliance, no DC integration,
no charger wiring) but the runtime tradeoff was driven by schedule
pressure, not engineering preference.

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

## 6. (Template for future entries)

**What happened:**

**Impact:**

**Recommendation for next time:**

---

*Last updated: 2026-04-16*
