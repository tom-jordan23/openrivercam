# Sukabumi station — manual bringup

UI-driven configuration of the deployed Sukabumi ORC-OS station. No
scripts. No CLI verification. Everything happens in the dashboard
form.

> **The session cheat sheet — with all UTM coordinates, paste blocks,
> and step-by-step UI clicks — is in `data/SESSION.md`** (gitignored,
> travels with the data files). Open that during the session and
> follow it top-to-bottom.

This file is just the high-level shape of the workflow for repo
readers; `data/SESSION.md` is the operational doc.

---

## Why manual

The dashboard form's save event overwrites the camera_config `data`
blob from the form's in-memory copy. API-import-then-UI-bbox loses
the imported values on the first save, and the bbox is a UI-only
field. The only durable path is **fill every field in the form
before the first save** — done entirely in the UI.

## Workflow shape

1. **Maintenance mode ON** (GitHub Actions in `orc-pmi-stations`)
2. **Cross-section upload** — dashboard sidebar, GeoJSON upload (not CSV)
3. **CameraConfig creation** — single form, populate everything (CRS,
   frame dims, z_0, h_ref, camera position, 6 GCPs, click each on
   calibration frame, draw bbox), then save once
4. **Wire video_config** — point at the new camera_config and
   cross_section ids
5. **Process a video** — Videos sidebar → click Process
6. **Verify in LiveORC** — browser
7. **Maintenance mode OFF**

Exact field values, paste blocks, and visual references are in
`data/SESSION.md`.

## Before the session

The bringup folder must contain (after `cp` from the salvage handoff):

- `data/camera_config.json` — pyorc CameraConfig (reference only for the manual flow; not imported)
- `data/cross_section.geojson` — uploaded in step 2
- `data/SESSION.md` — the cheat sheet you'll follow during the session
- `.env` — API password (used only if you fall back to the script flow)

`scp -r .` the whole `sukabumi_bringup/` folder to the station before
the session. Open the dashboard from your laptop browser through
Tailscale or Pangolin.

## What's also in this folder (not used in the manual flow)

`preflight.sh`, `bringup.sh`, `lib.sh` are an alternative API-driven
flow that hits the bbox-clobber problem mentioned above. They're
retained for one-off diagnostic / rollback use and for future sites
where the bbox issue is fixed upstream. Ignore them for the Sukabumi
session — follow `data/SESSION.md`.
