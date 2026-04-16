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

## 2. (Template for future entries)

**What happened:**

**Impact:**

**Recommendation for next time:**

---

*Last updated: 2026-04-16*
