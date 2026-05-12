# profile-night — image pipeline for IR night captures

ANNKE C1200 image parameters tuned for nighttime ORC processing. Replaces
the daytime `common/image.xml` while the camera is in IR mode. Push via
`camtool.py push <camera> --config profiles/profile-night/image.xml`,
ideally on a time-based schedule (see deployment section).

## Why this profile exists

The 2026-05-11 night captures (5 videos sampled 13:01–15:01 UTC) processed
through pyorc all hit the optical water-level SNR floor — the worst at
SNR 1.17 against a 3.0 threshold. Inspecting frames showed three structural
problems caused by the default day profile being used at night:

1. **IR over-illumination** of the near-bank cobblestone wall (the LB side
   of the cross-section). At `irLightBrightness=100` the cobblestone-mortar
   transitions clip near-white. The CSL water-level detector latches onto
   those bright mortar gradients and returns a false water-level at
   h ≈ 619 m (the true surface is at z_0 = 617.065 m, ~2 m below).
2. **Far-bank invisibility.** IR LEDs are co-located with the camera; light
   falls off into noise before reaching the RB GCPs (13, 14). The
   cross-section polyline samples darkness on that half.
3. **Default image processing pipeline tuned for color/daylight.**
   `Sharpness=50` and `NoiseReduce=50` together amplify cobblestone edges
   and smooth away the dim water-surface texture PIV needs to track.

## What this profile changes (relative to `common/image.xml`)

Only the image-pipeline endpoint is overridden. Streaming (`streaming_101.xml`),
NTP, OSD, motion detection, etc. stay on the common defaults.

| Element | Day (current) | Night | Rationale |
|---------|---------------|-------|-----------|
| `SupplementLight.irLightBrightness` | 100 | **50** | Single biggest expected win — stops the near-bank from clipping, may also let the AGC find a useful operating point. Sweep 40/50/60 across nights and pick the best. |
| `SupplementLight.mixedLightBrightnessRegulatMode` | `auto` | **`manual`** | Pin the IR level. `auto` would let the camera's AGC fight whatever we set here. |
| `SupplementLight.whiteLightBrightness` | 100 | **0** | Defensive — `supplementLightMode=irLight` already gates this, but zero the channel anyway. |
| `Sharpness.SharpnessLevel` | 50 | **25** | Reduce edge enhancement that turns mortar lines into false gradients. |
| `NoiseReduce.GeneralMode.generalLevel` | 50 | **20** | Preserve water-surface micro-texture for PIV. Some noise is acceptable here — the PIV correlation window averages across many pixels. |
| `Color.contrastLevel` | 50 | **70** | Stretch histogram to pull the dim far-bank up out of the noise floor. The output is already grayscale at night (IR cut filter out), so this acts as luminance contrast. |
| `IrcutFilter.nightToDayFilterLevel` | 4 | **5** | Stays in night mode longer through dawn — avoids mode-flipping captures with transitional light getting mistuned. |
| `Shutter.ShutterLevel` | 1/25 | 1/25 (unchanged) | See "shutter tradeoff" below. |
| Everything else | — | unchanged | WDR off, BLC off, Dehaze off, HLC off, Exposure=manual all kept from day profile. |

## What this profile does NOT change

- **Streaming params** (`streaming_101.xml`): bitrate, codec, GOP, resolution.
  Night uses the same encode as day so processed videos are consistent.
- **NTP / time** — no reason to change clock behavior at night.
- **OSD overlays** — same.
- **Motion detection** — not relied on for capture (orc-capture pulls RTSP
  on a schedule), no need to retune.

## The shutter tradeoff

`Shutter=1/25` gives 40 ms exposure. Going to `1/12` (~80 ms) doubles the
light gathered, which would help the far bank significantly. But:

- 80 ms exposure on flowing water blurs the surface features PIV tracks
  between consecutive frames. PIV correlation degrades as blur length
  exceeds the typical particle displacement between frames.
- At 12.5 fps stream, frame-to-frame interval is 80 ms anyway, so 80 ms
  shutter ≈ continuous integration with no dark interval — the worst case
  for distinguishing one frame from the next.

**Decision:** start the first night profile attempt with the shutter
unchanged at 1/25. If after a sweep on `irLightBrightness` we still can't
get far-bank visibility, fork a `profile-night-long-shutter` variant with
`Shutter=1/16` (62.5 ms) and a/b them against each other on the same nights.

## Deployment

The profile switch is **integrated into `orc-capture`** rather than a
standalone systemd timer. This sidesteps the duty-cycle race condition
(the Pi is asleep when fixed wallclock times fire on Sukabumi) and keeps
camera-state management in a single place.

### Flow

`orc-capture` runs every wake cycle (Sukabumi: ~15 min; Jakarta: per
ORC-OS managed timer). Its workflow is now:

1. Power on PoE relay
2. Wait for camera to boot
3. **`orc-camera-profile-switch auto`** — decides day or night from local
   clock; pushes the matching profile only if it differs from the last
   push (state file at `/var/lib/orc-camera/active-profile`)
4. `enforce_camera_config` — re-fixes specific fields that must always be
   right (supplement-light mode, OSD overlays)
5. Capture, validate, deliver

Because Hikvision/ANNKE image config persists in NVRAM across power
cycles, the switch is normally a no-op (active=desired, exits early).
Real pushes happen twice a day at the day↔night threshold.

### Configuration

All in `/etc/orc-capture.conf` (site-specific copies under `pi/sukabumi/`
and `pi/jakarta/`):

```
NIGHT_START=18:00               # local time when night profile takes over
NIGHT_END=06:00                 # local time when day profile resumes
DAY_PROFILE_PATH=/home/pi/camera_profiles/common/image.xml
NIGHT_PROFILE_PATH=/home/pi/camera_profiles/profiles/profile-night/image.xml
CAMERA_NAME=sukabumi-cam1       # cameras.json key for camtool push
```

Wraparound across midnight is handled (NIGHT_START > NIGHT_END means
night spans midnight, which is the usual case).

### Files involved

| Path | Role |
|------|------|
| `camera/profiles/profile-night/image.xml` | The night profile (this directory) |
| `camera/camtool.py` | Push tool; `--config FILE` derives endpoint from filename stem so `image.xml` → `/ISAPI/Image/channels/1` |
| `pi/shared/usr/local/bin/orc-camera-profile-switch` | Idempotent day/night decision + push script. Invokable directly for manual override: `orc-camera-profile-switch night --force` |
| `pi/shared/usr/local/bin/orc-capture` | Step 3 calls the switch script |
| `pi/shared/etc/orc-capture.conf` | Shared defaults |
| `pi/{sukabumi,jakarta}/etc/orc-capture.conf` | Site-specific values (CAMERA_NAME, etc.) |
| `/var/lib/orc-camera/active-profile` | Runtime state (single line: `day` or `night`); created by `deploy.sh` |

### Manual operator override

For testing, an operator on the Pi can force a profile:

```bash
orc-camera-profile-switch night --force   # push night profile now
orc-camera-profile-switch day --force     # push day profile now
orc-camera-profile-switch status          # print what's active + desired
```

The state file gets updated so subsequent automatic invocations stay in
sync with what was forced — but at the next day↔night threshold the
automatic logic will switch back. Force is for *testing*, not for
overriding the schedule long-term; change `NIGHT_START` / `NIGHT_END`
in the config for that.

### Time choice for Sukabumi (~7°S)

Annual sunset variation is roughly 17:35–18:15 local. A fixed 18:00 switch
wastes at most ~25 min of suboptimal captures per side per day, and dusk
captures are usually bad data anyway (transitional light, IR cut filter
actively switching). If the diagnostic logging (below) shows we're
consistently mistuned during transitions, narrow the threshold or pick a
seasonal schedule.

### Diagnostic logging (future iteration)

Not implemented yet, but worth tracking: extend `orc-capture` to query the
camera's `IrcutFilterType` runtime state immediately after each capture and
log it alongside what profile the Pi pushed. Mismatches uploaded with the
sensor CSVs let us validate the time-based threshold against the camera's
own ambient-light decision. If mismatches stay <5%, the schedule is fine;
if >5%, revisit threshold values or move to state-based switching.

## Sweep & iteration plan

This is iteration 1. Future iterations should change **one variable at a
time** so we know what helped:

| Iteration | Hypothesis | Variable | Test |
|-----------|-----------|----------|------|
| 1 (this) | IR clipping + processing smear are the dominant issues | irLight=50, sharp=25, NR=20, contrast=70 | One night of captures, compare SNR distribution against the 2026-05-11 baseline |
| 2a | IR brightness sweet spot | irLight ∈ {40, 50, 60} | Three nights, one per value; same other params |
| 2b | Far bank needs more exposure | Shutter ∈ {1/25, 1/16}; profile-night-long-shutter fork | Two nights, A/B |
| 3 | Contrast pull is helping | Color.contrastLevel ∈ {60, 70, 80} | If iteration 1 looks promising on the histogram, sweep this |

Each iteration's results, profile diff, and decision logged in
`ISSUE_LOG.md` or a dedicated `NIGHT_TUNING.md`.

## Validation

After deploying, before declaring success:

1. Pull 10+ night captures over 2 evenings (one with the new profile,
   one baseline for comparison if not already covered).
2. Run the validation analysis script (TODO: build under `survey_data/night_videos/`
   or as a one-shot in `survey/`) measuring per-frame:
   - Brightness histogram clipping % at 0 and 255
   - CSL-band intensity profile + gradient peak location
   - Water-region local variance (Laplacian)
3. Run pyorc water-level detection. Success criteria:
   - SNR > 3.0 on ≥ 50% of night-profile frames (currently failing 100%)
   - Detected water level within ±50 cm of z_0 = 617.065 m (currently
     detecting at ~619 m, 200 cm off)
4. If SNR passes but the detected h is still wrong: that's a CSL-band
   problem we can address with pyorc-side preprocessing (Layer 1 of the
   original three-layer plan), not more camera tuning.

## Known unknowns

- **Whether `irLightBrightness=50` is the actual sweet spot.** The choice
  is informed by visual inspection of the 5 sample frames; it may need
  to be much lower (e.g., 20) or there may not be a useful operating
  point at all for this camera + this geometry.
- **Whether the AGC behavior is reasonable with our values.** Hikvision
  AGC interacts with the exposure / gain / IR settings in firmware-internal
  ways. Setting `mixedLightBrightnessRegulatMode=manual` *should* lock IR,
  but the firmware may still adjust exposure based on what it sees.
- **Whether rain frames are filtered out separately.** The 2026-05-11 13:31
  frame failed for rain-in-IR reasons, not night-tuning ones. No image
  profile fixes that — needs a separate rain quality gate that's outside
  the scope of this profile.
