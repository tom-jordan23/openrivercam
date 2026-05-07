# Sukabumi station — manual bringup checklist

Pasteable, single-pane session guide for configuring the deployed
Sukabumi ORC-OS station entirely through the dashboard UI. Designed
to fit a sub-1-hour station window.

> **Why manual?** The dashboard form's `{action:'save'}` websocket
> overwrites the camera_config `data` blob from the form's
> in-memory copy on every save (ISS-FIELD-003). API-import-then-UI-bbox
> clobbers the imported values. The only durable path is **populate
> every field in the form before the first save** — meaning we set
> GCPs, intrinsics, h_ref, z_0, *and* bbox in one in-form pass.

---

## Before you connect (pre-flight on the laptop)

Open these on a second monitor / phone / split panes — you'll need them visible during the session:

| Pane | What to open | What it gives you |
|------|--------------|-------------------|
| 1 | `survey_data/sukabumi_handoff/annotated.png` | Calibration frame with each GCP marked + labelled at its pixel position. **The click reference for step 5.** |
| 2 | `survey_data/sukabumi_handoff/gcp_photos.pdf` | Field photos of each physical GCP marker, in case the annotated frame is ambiguous |
| 3 | `survey_data/sukabumi_handoff/gcps_salvage_subset_6.csv` | The 6 winning GCPs (UTM coords) — paste source for step 4 |
| 4 | `survey_data/sukabumi_handoff/camera_position.csv` | Camera UTM coords (one row) |
| 5 | `survey_data/sukabumi_handoff/water_level.csv` | z_0 / h_ref value (one row) |
| 6 | `survey_data/sukabumi_handoff/cross_section.geojson` | What you'll upload in step 3 |
| 7 | This file (`MANUAL_BRINGUP.md`) | The flow you're following |

**Static values you'll reference repeatedly** (memorize or keep at the top of a scratchpad):

```
CRS:           32748               (EPSG code, no prefix)
Frame size:    1920 × 1080
z_0:           617.065 m
h_ref:         617.065 m           (set equal to z_0; no staff gauge at this site)
GCP set:       6 GCPs              (GCP7, GCP8, GCP10, GCP13, GCP14, GCP3.2)
```

---

## Session flow

```
0. Maintenance mode ON       (GitHub Actions in orc-pmi-stations)
1. SSH + tunnel              (laptop)
2. Cross-section upload      (dashboard)
3. CameraConfig — single-save (dashboard, all fields + bbox + GCP clicks)
4. Wire video_config         (dashboard)
5. Process a real video      (dashboard)
6. Verify time_series + LiveORC upload  (CLI)
7. Maintenance mode OFF      (GitHub Actions)
```

---

## Step 0 — Maintenance mode ON

Toggle via the `orc-pmi-stations` GitHub Actions workflow before opening any UI. The Pi must stay awake the whole session; mid-session sleep mid-form means the form state is gone.

Verify on the station:
```bash
sudo /usr/local/bin/orc-maintenance-check
# expect output containing 'maintenance' / 'paused' / 'disabled'
```

## Step 1 — Connect

```bash
# From laptop
ssh -L 3000:localhost:3000 -L 3001:localhost:3001 pi@<sukabumi-tailscale>

# In another terminal pane on laptop, open dashboard:
open http://localhost:3000   # or paste in browser
```

Login with the API password (same as the `.env` value if you've used the bringup scripts before).

## Step 2 — Cross-section upload

Cross-section is independent of camera_config — upload it first so it has a stable ID before the camera_config flow. **Use `from_geojson/`, not `from_csv/`** (CSV upload has no CRS parameter and the record ends up CRS-less, which later breaks linking to the CRS-tagged camera_config).

In the dashboard:
1. Navigate to **Cross-sections** (or whatever the sidebar calls it)
2. **Upload from GeoJSON** → select `survey_data/sukabumi_handoff/cross_section.geojson`
3. Name: `sukabumi_XS_main_line`
4. Submit

Verify (CLI on the station):
```bash
curl -sS -b ~/.orc_cookie http://localhost:3001/api/cross_section/ \
  | python3 -m json.tool | grep -E 'id|name|crs|features' | head -20
```
Expect the new record with CRS `urn:ogc:def:crs:EPSG::32748` and 19 features. **Note its `id`** — you'll need it for step 4.

If you don't have the cookie file from a prior session, get a fresh one:
```bash
curl -sS -c ~/.orc_cookie -X POST \
  "http://localhost:3001/api/auth/login/?password=$(cat ~/sukabumi_bringup/.env)" \
  -o /dev/null
```

## Step 3 — CameraConfig (the big one — single-save)

**This is the step where order matters.** Open the camera_config form,
populate **every** field, and don't save until everything — including
the bbox — is in place.

1. Navigate to **CameraConfigs** → **New** (don't edit an existing one;
   start clean to avoid stale form state)
2. Set **Name**: `Sukabumi_salvage_v1` (or similar — use a name you'll
   recognize)
3. Set **CRS**: `32748`
4. Set **Frame size**: `width=1920`, `height=1080`
5. Set **z_0**: `617.065`
6. Set **h_ref**: `617.065`
7. Set **Camera position** from `camera_position.csv` (the one row;
   x=easting, y=northing, z=elevation)
8. **Add 6 GCPs** — paste rows from `gcps_salvage_subset_6.csv`. The
   form should accept either bulk paste or one-at-a-time entry. Order:

   ```
   GCP7    (river bed mid-channel near camera)
   GCP8
   GCP10
   GCP13
   GCP14   (far bank, opposite from camera)
   GCP3.2  (re-shoot of GCP3, near camera, day 2)
   ```

9. **Click each GCP's pixel position on the calibration frame.** Use
   `annotated.png` as the visual reference — every GCP is labelled at
   its expected pixel position. Cross-reference with `gcp_photos.pdf`
   if you can't pick a marker out of the dome / cobble background.

   **Click order doesn't matter** as long as each click is on the
   correct GCP. The form binds the click to the GCP row you have
   selected, not to position in the list.

10. **Draw the bounding box.** No automated guidance for this — see
    "Bbox drawing" section below for what to enclose.

11. **Now save once.** This is the only save in the form. After this,
    do not re-open the form. If you need to fix something, delete the
    record via the API and start over.

Verify after save (CLI):
```bash
sqlite3 ~/.ORC-OS/orc-os.db \
  "SELECT id, name,
          json_extract(data, '\$.gcps.h_ref'),
          json_extract(data, '\$.bbox')
   FROM camera_config ORDER BY id DESC LIMIT 1;"
```
Expect: `h_ref=617.065`, `bbox=<non-null>`.  **Note the new `id`.**

## Step 4 — Wire video_config

Find the video_config you'll process against (likely `id=1`). Update it to point at your new camera_config and cross_section.

Easiest path: dashboard → **Video configs** → `id=1` → set:
- `camera_config_id` → ID from step 3
- `cross_section_id` → ID from step 2
- `cross_section_wl_id` → same as `cross_section_id` (enables optical
  water-level fallback — backstop in case h_ref doesn't take for any
  reason)

Save.

CLI verify:
```bash
curl -sS -b ~/.orc_cookie http://localhost:3001/api/video_config/1/ \
  | python3 -m json.tool \
  | grep -E 'camera_config_id|cross_section|ready_to_run'
```
Expect: both IDs are your new ones, `ready_to_run=True`.

## Step 5 — Process a video

In the dashboard:
1. Navigate to **Videos**
2. Pick the most recent capture (real video, not the calibration video
   if a fresher one exists)
3. Click **Process**

Watch logs from the station (separate SSH session or tmux pane):
```bash
docker compose logs orcapi -f 2>&1 \
  | grep -E 'water level|Process|transect|Error|ERROR|liveorc|upload'
```

What to look for:
- `Water level set to 617.065 m.` → ✓ h_ref took
- `Running without water level, will estimate optically if possible.` →
  ⚠ h_ref didn't take. Optical fallback will still produce a result
  because of `cross_section_wl_id`, but the salvage-doc convention
  isn't being honored. See troubleshooting below.
- `Error processing transect` / `pyorc.api.velocimetry` traceback → the
  xarray<2026 pin in the local Dockerfile may be missing on the
  station. Check `pip show xarray` inside the orcapi container.

Process should complete in 5–10 min.

## Step 6 — Verify

```bash
# time_series row was created and has reasonable numbers
sqlite3 ~/.ORC-OS/orc-os.db "
  SELECT id, video_id, q_50, v_av, fraction_velocimetry, h
  FROM time_series ORDER BY id DESC LIMIT 3;"
```
Expect a fresh row with `q_50` populated (calibration-video reference
was 0.51 m³/s; real-video numbers will differ but should be in the
same order of magnitude).

```bash
# LiveORC upload fired
docker compose logs orcapi --since 15m \
  | grep -iE 'liveorc|institutionproject|upload.*video|upload.*POST'
```
Expect at least one POST to the LiveORC server with a 2xx response.

From your laptop browser, open the LiveORC site and confirm the new
video is listed for the Sukabumi project with velocity overlays.

## Step 7 — Maintenance mode OFF

Toggle off via the same `orc-pmi-stations` GitHub Actions workflow.

Confirm the duty cycle resumes:
```bash
journalctl -u orc-capture -f
# expect a wake → capture → sleep cycle on the next 15-min boundary
```

---

## Bbox drawing guidance

The bbox is a quadrilateral on the calibration frame in **pixel
space**, not UTM. It bounds the region where ORC-OS runs PIV. There's
no auto-fit output for it — you draw it visually.

What to enclose:
- The **water surface** within and around the cross-section line
- A few meters of channel **upstream** (into the flow) of the XS
- A few meters of channel **downstream** (away from the flow) of the XS
- Width: roughly the wetted channel width, plus a small margin to
  cover bank-to-bank surface

What to avoid:
- Dry banks, walls, vegetation — anything that isn't water motion will
  generate spurious PIV vectors
- The far horizon / sky if visible
- Strong reflections from sun / lights if you can crop them out

At Sukabumi the cross-section is a ~3 m wide concrete-walled urban
canal:
- One bank (the near-camera side, "LB") is a single-GCP wall, very
  close to the camera
- Opposite bank ("RB") is ~3 m across the channel
- Flow is roughly N→S in UTM (the XS line is east-west in the survey)
- Frame: 1920×1080, camera looks down + slightly across at the channel

Use `annotated.png` to identify:
- The XS endpoints (markers at each anchor)
- GCP13 + GCP14 cluster on the far bank → that's the RB side
- GCP3.2 + GCP7/8/10 are nearer the camera

Draw the bbox roughly centered on the XS line, oriented along the
channel (long axis vertical-ish in the frame, short axis tracking the
banks). Err on the side of slightly **smaller** rather than larger —
ORC's PIV cost scales with bbox area, and bank pixels poison the
velocity field.

You can iterate after the first Process run if results look wrong;
the bbox is part of camera_config but a save-only-bbox edit is safer
than re-pasting GCPs.

---

## Troubleshooting

**Symptom:** Process log says `Running without water level, will estimate optically if possible.`

→ `h_ref` didn't take in the camera_config save. Either the form
default of 0.0 was sent, or the record didn't include the `h_ref`
field at all. Check:
```bash
sqlite3 ~/.ORC-OS/orc-os.db \
  "SELECT json_extract(data,'\$.gcps.h_ref') FROM camera_config WHERE id=<NEW_ID>;"
```

If it's 0 or NULL: the camera_config form lost the value during entry.
Don't try to SQL-patch (that gets clobbered on the next form save).
Delete the record via API and redo Step 3 — making sure h_ref is set
**before** drawing the bbox or doing any other interaction that might
trigger a partial save.

```bash
# delete and redo
curl -sS -b ~/.orc_cookie -X DELETE \
  http://localhost:3001/api/camera_config/<NEW_ID>/
```

**Symptom:** Process completes but `q_50` is wildly off (e.g. orders of magnitude different from 0.51 m³/s on the calibration video, or NaN).

→ Likely a bbox / GCP-click problem. Inspect `plot_quiver.jpg` in
`~/.ORC-OS/uploads/videos/<date>/<id>/output/` — if the quiver vectors
are clearly outside the channel or pointing every which way, the bbox
or the calibration is off. Re-evaluate clicks against `annotated.png`.

**Symptom:** `Error processing transect` / `xr.Dataset(Dataset)` traceback.

→ The xarray<2026 pin isn't applied on this station's image. Check:
```bash
docker compose exec orcapi python -c "import xarray; print(xarray.__version__)"
```
If it's `2026.x.x` or higher, the local Dockerfile rebuild didn't land
here. See `survey/NEXT_SESSION_PLAN.md` "RESUME" section for the
constraint snippet (`setuptools<70`, `xarray<2026` in `/tmp/pip-constraints.txt`
during build).

**Symptom:** LiveORC upload didn't fire (no POST in `docker compose logs orcapi`).

→ LiveORC credentials may not be configured. In dashboard → Settings,
look for `liveSiteUrl`, `institutionId`, `projectId`, and an upload
token. If missing, configure now (this is one of the legitimate
dashboard-form interactions; it's a separate record from camera_config
so it can't clobber your salvage calibration).

After fixing, re-trigger Process — the upload should fire on the next
completed run.

---

## Rollback

If after Step 6 you decide the bringup is bad and want to revert to
the previous config:

```bash
# Back to whatever was on video_config.id=1 before today
# (you'll need to remember/look up the prior camera_config_id and cross_section_id)

curl -sS -b ~/.orc_cookie -X PATCH \
  http://localhost:3001/api/video_config/1/ \
  -H 'Content-Type: application/json' \
  -d '{"camera_config_id": <PRIOR>, "cross_section_id": <PRIOR>, "cross_section_wl_id": <PRIOR>}'

# Then DELETE the new records to keep the DB clean
curl -sS -b ~/.orc_cookie -X DELETE \
  http://localhost:3001/api/camera_config/<NEW_ID>/
curl -sS -b ~/.orc_cookie -X DELETE \
  http://localhost:3001/api/cross_section/<NEW_ID>/
```

Capture the prior IDs **before** Step 4 if you think rollback is
likely:
```bash
curl -sS -b ~/.orc_cookie http://localhost:3001/api/video_config/1/ \
  | python3 -m json.tool > ~/video_config_1_prebringup.json
```

---

## What this manual flow does NOT cover

- Maintenance-mode toggling (use the GitHub Actions workflow)
- Standing up Grafana on the LiveORC server (TODO-102 — separate session)
- LiveORC upload backfill if uploads were broken for a long time
  (TODO-103 has the verification path; backfill needs a different tool)
- The flow-direction question on `plot_quiver.jpg` (TODO-101 has it as
  an open inspection task)
