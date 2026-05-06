# Sukabumi station bringup scripts

Apply the salvage CameraConfig + cross-section to the deployed Sukabumi
ORC-OS station via API, with preflight validation and automatic
rollback on failure. Designed for a sub-1-hour station session.

## What's in here

| File | Purpose |
|------|---------|
| `preflight.sh` | Read-only checks: tooling, input files, API reachable, DB state, recent captures, maintenance mode, disk, LiveORC config |
| `bringup.sh` | Apply: POST camera_config, POST cross_section, PATCH video_config — with rollback on any failure |
| `lib.sh` | Shared bash functions sourced by both scripts |
| `data/` | (gitignored) place `camera_config.json` and `cross_section.geojson` here |
| `state/` | (gitignored) per-run rollback state files |
| `.env` | (gitignored) one-line API password |

## One-time setup (on your laptop, before the trip)

```bash
cd spring_2026_ID/sukabumi_bringup

# Stage the input files from the salvage handoff folder
cp ../survey_data/sukabumi_handoff/sukabumi_autofit_camera_calibration.json \
   data/camera_config.json
cp ../survey_data/sukabumi_handoff/cross_section.geojson \
   data/cross_section.geojson

# Drop the API password (one line, no KEY=VALUE)
echo 'YOUR_ORC_API_PASSWORD' > .env
chmod 600 .env

# Optional: dry-run preflight against your local Docker ORC-OS first
./preflight.sh http://localhost:3001/api
```

Then push to the station:

```bash
# From the laptop, with the station reachable on Tailscale:
scp -r . pi@<sukabumi-tailscale>:~/sukabumi_bringup
```

## Running it on the station

SSH in, then:

```bash
cd ~/sukabumi_bringup

# 1. Validate (read-only — runs in seconds, exits 1 if blockers)
./preflight.sh

# 2. If clean, apply
./bringup.sh

# If anything goes wrong:
./bringup.sh --rollback
```

`bringup.sh` automatically rolls back on any failure during apply.
Manual `--rollback` is only needed if you need to undo a successful
run (e.g. you decide to re-import with different inputs).

## Critical gotcha — read this before opening the dashboard

**Do not open the camera_config edit form in the dashboard between
running `bringup.sh` and clicking Process on a video.** This is
ISS-FIELD-003: the dashboard's `{action:'save'}` websocket rewrites
the camera_config `data` blob from the form's stale in-memory copy,
which silently reverts `h_ref` from 617.065 back to 0.0. The
`h_ref = 0.0` then poisons every subsequent Process run. Symptoms:
log shows `Running without water level, will estimate optically if
possible.` instead of `Water level set to 617.065 m.`.

**Safe interaction pattern post-bringup:**

1. Open the dashboard.
2. Navigate directly to **Videos** (not CameraConfigs / not GCPs).
3. Click Process on the most recent capture.
4. Watch logs.

If you accidentally open the camera_config form, exit without saving
and verify `h_ref` is still 617.065 with:
```bash
sqlite3 ~/.ORC-OS/orc-os.db \
  "select json_extract(data,'\$.gcps.h_ref') from camera_config where id=<NEW_ID>"
```

## Flags / options

```
./preflight.sh                  # default (localhost API)
./preflight.sh http://other/api # custom API base

./bringup.sh                    # apply with auto-rollback on failure
./bringup.sh --no-link          # skip the video_config PATCH (just import records)
./bringup.sh --video-config-id 2  # PATCH a different video_config
./bringup.sh --rollback         # undo most recent run
./bringup.sh --rollback state/20260505T...json  # undo specific run
./bringup.sh --keep-state       # do not delete state file on success
./bringup.sh http://other/api   # custom API base (positional)
```

Environment overrides (all optional):

```
API_BASE         (default http://localhost:3001/api)
DATA_DIR         (default ./data)
ENV_FILE         (default ./.env)
CC_FILE          (default $DATA_DIR/camera_config.json)
XS_FILE          (default $DATA_DIR/cross_section.geojson)
ORC_DB           (default $HOME/.ORC-OS/orc-os.db)
EXPECTED_H_REF   (default 617.065)
EXPECTED_CRS     (default EPSG:32748)
VIDEO_CONFIG_ID  (default 1)
```

## What `preflight.sh` actually checks

| Check | Behavior |
|-------|----------|
| Tooling: `curl`, `python3`, `sqlite3` | BLOCKER if missing |
| `data/camera_config.json` parseable, has `gcps.h_ref ≈ 617.065`, ≥4 GCPs | BLOCKER |
| `data/cross_section.geojson` parseable, FeatureCollection, contains EPSG:32748 in CRS | BLOCKER |
| `.env` exists and non-empty | BLOCKER |
| API reachable at `$API_BASE` | BLOCKER |
| Auth login succeeds | BLOCKER |
| ORC-OS DB readable | WARN if missing — script falls back to API-only |
| Existing camera_configs / cross_sections / video_config.id=1 | informational |
| `uploads/incoming/` has a recent capture | WARN if empty |
| `orc-maintenance-check` reports maintenance mode | WARN if production mode active |
| Disk space at `$HOME` and `~/.ORC-OS` | informational |
| LiveORC settings present in DB | WARN if missing |
| LiveORC server reachability (HTTP probe to configured URL) | WARN if unreachable / 5xx |
| LiveORC auth probe (if a token-like setting is present) | WARN if 401/403 (token rotted) |
| `docker compose logs orcapi` recent upload events | WARN if error / failure / 4xx / 5xx lines |

Exit code: 0 = OK or warnings only, 1 = blockers.

## What `bringup.sh` actually does

1. Re-validate input files (defensive)
2. Login (cookie-auth)
3. Read current `video_config.id=1` and save its bindings to a state file
4. **POST** `/camera_config/from_file/` with `data/camera_config.json` → new id
5. Verify the new camera_config's `gcps.h_ref` matches 617.065 (via API + DB)
6. **POST** `/cross_section/` with `{name, features}` body → new id
7. Verify CRS contains EPSG:32748 and ≥4 features
8. **PATCH** `/video_config/$VIDEO_CONFIG_ID/` to point `camera_config_id`,
   `cross_section_id`, and `cross_section_wl_id` (for optical fallback) at
   the new ids
9. Verify `ready_to_run=True` on the patched video_config
10. Print next-step commands (Process trigger via dashboard, log tail, etc.)

If any of steps 4–8 fail, the script automatically:
- Reverts step 8 (PATCH back to prior video_config bindings)
- DELETEs the new cross_section
- DELETEs the new camera_config
- Renames the state file to `*.rolled-back.json`

Step 9 failing does **not** trigger rollback (the state is good; that's
just an assertion).

## Manual rollback

If you've successfully run `bringup.sh`, decided you want to undo,
and the state file is still in `state/`:

```bash
./bringup.sh --rollback
```

If you need to roll back to a specific older run:

```bash
ls state/
./bringup.sh --rollback state/20260505T120000Z.json
```

`--rollback` does **not** read input files (no need — it only revisits
the state file's recorded ids).

## What this script does NOT do

- Does not enable / disable maintenance mode. Toggle that via the
  `orc-pmi-stations` GitHub Actions workflow before/after the session.
- Does not trigger Process. Click Process in the dashboard's Video page,
  or POST to the appropriate run endpoint manually.
- Does not configure LiveORC upload credentials. If `preflight.sh`
  flags missing `liveSiteUrl` / project / institution settings, fix
  those in the dashboard's Settings page before running this script
  (or accept that uploads won't fire and verify processing only).
- Does not verify uploads on the LiveORC server side. After Process
  completes, check the LiveORC web UI from your laptop.
