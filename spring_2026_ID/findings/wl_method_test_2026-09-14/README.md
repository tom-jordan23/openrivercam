# Optical water-level test: transect arrangement and colour method (2026-09-14)

**Status:** Local test, two days of mirrored Sukabumi video. Not yet applied to
the station. No independent water-level reference.
**Software:** ORC-OS 0.6.0 image (`orc-os-v060-orcapi`), pyorc 0.9.9, the same
`velocity_flow_subprocess` call the station makes (`orc_api/schemas/video.py:277`).
**Inputs:** recipe 4, camera config 3 and cross-sections 4 and 5 of VideoConfig 3
("Sukabumi IPB"), taken from the 2026-06-29 LiveORC dump. Video from the TODO-114
mirror (`data/liveorc-mirror/4/media`).
**Related:** TODO-113 (transect swap), TODO-120 (lessons learned),
`optical_wl_daytime_glint.md` (the July daytime failure finding).

## Summary

1. **The transect is not the main lever.** Swapping the discharge and
   water-level transects lifted failing daytime S/N from about 1.6 to about
   2.2, and moved part of the discharge transect out of the camera frame
   (velocity coverage fell from about 95% to about 72%).
2. **The colour method is.** The deployed recipe uses `grayscale` for both
   water-level passes. Trying `hue` first and falling back to `grayscale`
   passed nearly every clip on both test days, with the fewest outlying water
   levels.
3. **Passing the S/N gate does not make a water level right.** Deployed
   `grayscale` accepted daytime readings 1.14 m above that day's night level
   at S/N 2.02 and 2.32.

## Harness check

Under the deployed configuration the harness reproduces the station's water
level: errored clip 2421 fails the gate as the server recorded, and night clip
2417 reproduces its published h of 614.7733 m exactly. Discharge does **not**
reproduce (2417: q_50 0.274 against a published 0.192), so discharge values
here are comparable between runs, not against published figures.

## Results

### Transect arrangement (16 clips: 8 errored daytime, 6 finished daytime, 2 night)

| Arrangement | Clips passing | Median velocity coverage |
|---|---|---|
| Deployed: discharge upstream, water level downstream | 8/16 | 95% |
| Swapped: discharge downstream, water level upstream | 15/16 | 73% |
| Upstream transect for both | 15/16 | 96% |

With the colour methods below, the upstream transect performs poorly (daytime
`hue` 3/19, `sat` 5/19 on 07-03). The deployed downstream water-level transect
is the better line once the method changes.

### Colour method, deployed transects

Reference level is each day's median night `grayscale` reading: 614.794 m on
07-03, 614.773 m on 08-11.

| Day | Recipe | Day | Night | Total | Readings >10 cm off | Accepted S/N < 2.3 |
|---|---|---|---|---|---|---|
| 07-03 | `grayscale` (deployed) | 10/19 | 23/24 | 33/43 | 6 | 5 |
| 07-03 | `sat`, then `grayscale` | 18/19 | 24/24 | 42/43 | 2 | 6 |
| 07-03 | `hue`, then `grayscale` | 19/19 | 24/24 | 43/43 | 0 | 7 |
| 08-11 | `grayscale` (deployed) | 10/23 | 24/24 | 34/47 | 9 | 12 |
| 08-11 | `sat`, then `grayscale` | 21/23 | 24/24 | 45/47 | 4 | 12 |
| 08-11 | `hue`, then `grayscale` | 22/23 | 24/24 | 46/47 | 2 | 11 |

Single-method results on 07-03 (both passes the same method):

| Method | Day passing | Median day S/N | Night passing |
|---|---|---|---|
| `grayscale` | 10/19 | 2.01 | 23/24 |
| `hue` | 19/19 | 2.72 | 1/24 |
| `sat` | 17/19 | 4.25 | 1/24 |
| `val` | 16/19 | 2.70 | 23/24 |

`hue` and `sat` return S/N of about 1.00 on the monochrome IR night image, so in
a combined recipe they fail cleanly at night and `grayscale` takes over.

### Observations

- `hue` gives the most consistent daytime level (about 614.75 m on nearly every
  clip) but with thin margins: roughly a quarter of accepted readings are below
  S/N 2.3.
- `sat` gives stronger S/N in the morning (3.4–4.5 on 08-11) but accepted one
  reading 28 cm high at S/N 3.68 (clip 3618, 14:31 WIB).
- Daytime `grayscale` passes are the least reliable readings in the set, not
  only the most frequent failures.
- Lighting metrics in a fixed near-bank region (clipped pixels, sun/shade
  split) did **not** correlate with daytime `grayscale` S/N on 07-03 (Spearman
  +0.01 and +0.08, n=19). An earlier reading from a single frame suggested
  otherwise; it did not hold. The region may not match where the transect
  reads.
- Night clips alternate wake to wake between about 0% and about 6% clipped
  pixels in that region. Not investigated.

## Caveats

- Two dry-season days (2026-07-03, 2026-08-11). Wet-season and overcast
  behaviour is untested.
- No independent water-level reference. Agreement with the night reading is
  support, not proof.
- The day camera profile on the station is a March placeholder
  (TODO-120). These clips were captured under it; results may change once the
  day profile is tuned.
- Recipe, camera config and cross-sections are **not** included: they carry
  real survey coordinates. Regenerate them from the dump (below).

## Reproducing

```bash
# 1. Extract inputs from the 2026-06-29 dump into ./work/prod
cd spring_2026_ID/liveorc_server/reprocess/liveorc-backups/20260629-141301
for t in api_recipe api_cameraconfig api_profile; do
  pg_restore -a -t $t -f - liveorc_full.dump > <work>/prod/$t.copy
done
#    then write api_recipe_4.json, api_cameraconfig_3.json (the `data` column)
#    and xs_4_ipb_discharge.geojson, xs_5_ipb_wl_optical.geojson (`features`)

# 2. Copy the scripts and a jobs file from results/ into <work>, then run
docker run --rm --user $(id -u):$(id -g) -e HOME=/tmp -e MPLCONFIGDIR=/tmp \
  -v <work>:/work -v data/liveorc-mirror/4/media:/media:ro \
  --entrypoint python3 orc-os-v060-orcapi:latest \
  /work/run_swap.py /work/<jobs>.json /work/<out> 5

# 3. Extract results serially (libhdf5 is not thread-safe)
docker run ... /work/extract_serial.py /work/<out>
```

Job `method` values: `grayscale`, `hue`, `sat`, `val`, or `<method>_then_gray`.
Job `arr` values: `live`, `swap`, `up_both`.

## Files

| File | What |
|---|---|
| `run_swap.py` | Harness: one pyorc run per job, results to `results.jsonl` |
| `extract_serial.py` | Re-reads outputs one at a time; records accepted and rejected S/N |
| `frame_metrics.py` | Per-clip lighting metrics |
| `analyse_day.py` | Joins lighting metrics with method results |
| `diff_camera.py` | Diffs the station camera-settings grab against `camera/` |
| `results/*.jsonl` | Per-clip results and metrics (no coordinates) |
| `results/jobs_*.json`, `results/day*.json` | Job lists and clip lists |
