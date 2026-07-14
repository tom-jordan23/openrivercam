# Finding: daytime optical water-level failure at Sukabumi (candidate cause: specular sun glint)

**Status:** Hypothesis — strongly supported by log statistics; **direct visual proof pending** (see §7).
**Site:** Sukabumi (IPB), optical water-level only, no water-level sensor.
**Software:** pyorc 0.9.4 via ORC-OS; recipe id 3 (`ipb_recipe.json`), video_config id 3.
**Data window:** 2026-07-08 → 2026-07-14.
**Author:** Tom Jordan (analysis assisted by Claude).
**Last updated:** 2026-07-14.

> Why this is written down: it is an early, load-bearing finding in evaluating whether
> **image-based optical water-level detection** is fit for purpose at this site. It also
> **inverts a prior working assumption** — night was thought to be the weak case; the data
> show night is the *reliable* case and **daylight** is where the technique currently fails.

---

## 1. Headline

Over 2026-07-08→14, a large fraction of **daytime** captures error out because pyorc cannot
estimate the optical water level: it locates a plausible waterline but the detection's
signal-to-noise (S/N) falls below the recipe gate (`s2n_thres: 2.0`). **Night captures pass
reliably** with high S/N. The failure window coincides exactly with the daylight window,
pointing to a **solar-illumination-driven** mechanism, of which **specular sun glint** (a
mirror reflection of the sun off the water surface, washing out the water-line edge) is the
leading candidate.

Because water-level estimation aborts the entire run, **each daytime failure loses the whole
discharge measurement**, not just the water level.

---

## 2. How the data was collected

- Tool: `spring_2026_ID/pi/tools/orc_gather_logs.py` (read-only; pulls each video's record +
  pyorc log + the config that produced it). Run on-station against the ORC-OS API via nginx
  (`BASE=http://localhost/api`).
- Two bundles, each the **100 most-recent** videos of a status:
  - ERROR set — `--status error` — 100 videos, 2026-07-08→14.
  - DONE set — `--status done` — 100 videos, 2026-07-11→14.
- Derived, coordinate-free dataset: [`ipb_optical_wl_s2n_2026-07-08_to_14.csv`](ipb_optical_wl_s2n_2026-07-08_to_14.csv)
  (video_id, timestamp, local hour, status, S/N, pass flag, detected h). Raw bundles are **not**
  committed — they contain `cross_section_*.json` with real UTM survey coordinates (private per
  the survey-data rule).

**Timezone (verified, not assumed):** the station system clock is **UTC**, confirmed by the
tracked `spring_2026_ID/pi/sukabumi/etc/orc-capture.conf` ("Times are UTC … WIB sunset 18:00 =
11:00 UTC, WIB sunrise 06:00 = 23:00 UTC"). Video timestamps are therefore UTC; local WIB =
UTC+7. This mapping is load-bearing for the day/night result in §4, so it was checked directly.

---

## 3. The failure mode (measured)

Every ERROR video ends identically:

```
Found water level at h: 614.795 m with too low signal-to-noise: 1.306 < 2.000
Water level could not be estimated from video. Please set a water level with --h_a.
Could not estimate water level from video.
```

100/100 ERROR videos share this exact mode. It is **not a crash** — the video reads fine and a
waterline candidate is found; it is rejected by the S/N gate.

Recipe water-level config (`recipe_3`, YAML):

```yaml
water_level_options: { bank: near, length: 3.0, padding: 0.5, min_z: 614.3, max_z: 618.5 }
frames_options:
  - { method: grayscale, range: {}, s2n_thres: 2.0 }   # pass 1
  - { method: grayscale,            s2n_thres: 2.0 }   # pass 2
```

---

## 4. Evidence

### E1 — The S/N gate is well-placed, not too strict (bimodal separation)

| set | n | S/N min | median | max |
|-----|---|--------|--------|-----|
| DONE (passes) | 100 | **2.004** | **4.009** | 5.561 |
| ERROR (fails) | 100 | 1.185 | **1.630** | **1.983** |

Passing captures cluster at S/N ≈ 3–5 (half above 4); failing captures cluster at ≈ 1.3–1.8;
**almost nothing lives between 1.98 and 2.00**. The `s2n_thres: 2.0` gate sits in the valley of
a genuinely bimodal distribution — it is separating "good capture" from "bad capture," which is
what a threshold should do. **Lowering it would admit unreliable estimates, not recover good
ones.**

ERROR best-S/N histogram: `1.0–1.3: 6 | 1.3–1.5: 16 | 1.5–1.7: 44 | 1.7–1.9: 27 | 1.9–2.0: 7`.

### E2 — The failures find the *right* waterline (river is stable)

Detected h is essentially identical across both sets — DONE median **614.794 m**, ERROR median
**614.794 m** (band is 614.3–618.5). Only 15/100 failures pin near the `min_z` floor. So the
failures are **not** finding the wrong line or hitting the search-band edge; they find the
correct, stable level (~614.8 m all week) but without enough confidence to pass. This rules out
"search band wrong" and "water dropped below band" as the primary cause.

### E3 — Failures are bounded exactly by daylight; nights pass

Hour-of-day counts (local WIB = UTC+7):

```
WIB hour   FAIL  DONE          WIB hour   FAIL  DONE
00–05        0    36  (night)  12           8     1
06           3     3           13           4     3   <- solar noon
07           4     4           14           3     4
08           9     0           15          10     2
09          11     0           16          12     1
10          11     1           17          11     2
11           9     3           18           5     4
                               19–23        0    44  (night)
```

- **Zero** failures occur at night (19:00–06:00 WIB = 12:00–22:00 UTC); night captures pass with
  high S/N (IR-illuminated, glint-free).
- All failures fall inside the **daylight** window (06:00–18:00 WIB), whose edges match sunrise
  (23:00 UTC) and sunset (11:00 UTC) per the capture config.
- Within daylight the failures show a **double peak (08–12 and 15–17 WIB) with a dip at solar
  noon (13–14)**.

The daylight-bounded failure implicates **direct sunlight**. The morning/afternoon-peak,
midday-dip sub-structure is the geometric signature of **specular glint** (the sun–surface–camera
mirror alignment is met at low/mid sun angles and broken when the sun is overhead) rather than a
uniform daytime effect.

---

## 5. Interpretation and terminology

**Glint vs glare (used precisely here):**
- **Glint** = specular reflection — light bouncing off the water at the mirror angle into the
  camera. Directional, geometry-dependent; appears as a bright hotspot / sparkle field that
  saturates pixels to near-white. This is the hypothesised cause.
- **Glare** = the general effect of excessive brightness degrading a sensor's contrast (includes
  veiling/haze). Glint is *one source* of glare; not all glare is glint.

The day/night shape (§E3) is diagnostic of **glint specifically**, because a haze/veiling glare
tracks sky brightness, not sun *angle*, and would not produce the midday dip.

**Leading hypothesis:** specular sun glint on the water surface raises luminance where the
water-line edge sits, collapsing the S/N of the optical water-level detection during daylight.

---

## 6. Alternatives / confounders considered

| Alternative | Argues against it |
|-------------|-------------------|
| S/N threshold simply too strict | E1: bimodal, threshold in the valley; passes sit far above 2.0 |
| Wrong search band / water below band | E2: same h (614.79) in pass and fail; only 15% near floor |
| General daytime underexposure/dimness | Fails would peak at dawn/dusk and be monotonic; instead peaks mid-morning/mid-afternoon with a **midday dip** |
| Afternoon wind ripple | Could explain the 15–17 peak, but **not** the 08–12 morning peak; ripple roughens/darkens (no saturation) — separable by the pixel test in §7 |
| Weather/turbidity | Random, not locked to sun angle; would not respect the daylight boundary |

None of these fit the daylight-bounded, twin-peaked, midday-dip shape as cleanly as glint. They
are not yet *excluded* — that requires §7.

---

## 7. What would prove it (proof protocol) — PENDING

Glint is falsifiable. Confirm by testing its unique predictions, strongest/easiest first.

1. **Matched-frame pixel test (direct).** Pull the actual video from a failing ~09:00 and
   ~16:00, a passing ~13:00, and a passing night capture. In the water-surface band, measure the
   fraction of saturated / near-white (high-value, low-saturation) pixels.
   - *Confirms* if failing frames show a bright specular patch on the water and a much higher
     saturated-pixel fraction than passes; *refutes* if failing water is darker/rougher (ripple)
     or the whole frame is dim (exposure), with no hotspot.
   - Requires fetching pixels — `orc_gather_logs.py` pulls logs+config only; add a
     `--fetch-video`/frame-grab mode.
2. **Overcast vs sunny natural experiment (causal).** On a known-overcast day, did the
   08–12 / 15–17 captures pass? Direct sun is required for glint; ripple and shadows are not. If
   daytime failures vanish under cloud and return under sun, that is causal. In-image proxy for
   "direct sun": presence of hard shadows / bright sky region.
3. **Solar-geometry overlay (confirmatory).** Compute sun azimuth/elevation for the site at each
   failing timestamp, predict the specular point, and verify the observed hotspot sits there and
   migrates across the day as predicted.

**Refutation conditions (any one):** failing daytime water surfaces are not brighter/more
saturated than passing ones; failures persist at the same rate on overcast days; or the S/N
collapse is uniform along the whole cross-section rather than localized at a bright patch.

---

## 8. Implications

- **Do not lower `s2n_thres`.** E1 shows the gate is correctly placed; lowering it trades honest
  failures for silently-wrong water levels feeding discharge.
- **Cost is real:** on fully-sampled days, a large share of *daytime* discharge measurements are
  lost (see caveat in §9). Night discharge is unaffected by this issue (velocimetry at night is a
  separate, parked question).
- The river level is stable (~614.8 m all week), so bracketing good reads exist around every
  glint window — a **fallback water level** (e.g. last good optical h, or `--h_a`) could recover
  daytime *discharge* even while the optical read is untrustworthy, if ORC-OS/pyorc supports it.

### Candidate mitigations (untested; ordered)
1. Prove the mechanism (§7) before investing.
2. **Glint-robust water-level preprocessing** — both recipe passes are plain `grayscale`
   (maximally glint-sensitive). A hue/saturation-based or normalized method can suppress specular
   highlights. This addresses the cause without touching the threshold.
3. **Fallback h on optical failure** to preserve discharge continuity in daylight.
4. Physical: a polarizing filter kills glint at the source, but the ANNKE C1200 is a sealed PoE
   camera — impractical.

---

## 9. Reproducibility & caveats

- Dataset: [`ipb_optical_wl_s2n_2026-07-08_to_14.csv`](ipb_optical_wl_s2n_2026-07-08_to_14.csv)
  (200 rows). S/N per video = the accepted `signal-to-noise: X > 2.000` (DONE) or the best
  (max) `too low signal-to-noise: X` (ERROR). h = last detected `at h:` value.
- **Sampling caveat:** each set is the 100 most-recent of its status. DONE only reaches back to
  2026-07-11, so a naïve per-day ERROR-vs-DONE ratio for 07-08→10 is a sampling artifact, **not**
  a real "zero successes" cliff. Day/night and S/N-distribution results (§4) are unaffected.
- The `.json` extension on `recipe_*` / `cross_section_*` from the gather tool is misleading —
  those endpoints return YAML / GeoJSON respectively.

## 10. Related
- **Validation plan:** [`optical_wl_validation_plan.md`](optical_wl_validation_plan.md) — the
  multi-phase plan to confirm mechanism, seasonality, and mitigation. Supersedes the proof
  protocol sketched in §7.
- Memory: `project_ipb_optical_wl_recipe_tuning`, `project_night_snr_tuning_findings`,
  `project_night_profile_rebaseline` (this finding refines the last: night optical WL confirmed
  reliable; the open gap is **daytime**, not night).
- Recipe under test: `spring_2026_ID/survey_data/ipb_survey_1/handoff_station/ipb_recipe.json`.
