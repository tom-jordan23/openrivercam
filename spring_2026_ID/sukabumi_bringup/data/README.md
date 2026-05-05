# Bringup input files

Place the salvage handoff files here before running `preflight.sh` /
`bringup.sh`. The contents of this directory are gitignored — only this
README is tracked.

| Filename (expected)        | Source |
|----------------------------|--------|
| `camera_config.json`       | `../survey_data/sukabumi_handoff/sukabumi_autofit_camera_calibration.json` |
| `cross_section.geojson`    | `../survey_data/sukabumi_handoff/cross_section.geojson` |

```bash
cp ../../survey_data/sukabumi_handoff/sukabumi_autofit_camera_calibration.json \
   ./camera_config.json
cp ../../survey_data/sukabumi_handoff/cross_section.geojson \
   ./cross_section.geojson
```

The filenames here are the script defaults. If you need to use
different paths (e.g. for testing against alternate calibrations),
override via the `CC_FILE` and `XS_FILE` environment variables.
