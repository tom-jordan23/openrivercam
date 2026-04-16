# Profile C: Camera-Local SD Recording — Implementation Notes

## Concept

Instead of pulling video over RTSP in real-time (where network buffering
limits effective bitrate), the camera records to its own SD card at full
encoder quality. The Pi then downloads the finished file via ISAPI.

## Why This Matters

RTSP transport overhead consumes 10-20% of the configured bitrate. With
CBR at 16-20 Mbps, actual RTSP-delivered bitrate is typically 12-17 Mbps.
By recording locally, the camera encoder gets the full bitrate budget with
zero transport loss. The Pi downloads the finished file over the PoE
Ethernet link (100 Mbps), far faster than real-time.

## Encoding

Profile C uses **identical encoding settings to Profile A** (CBR 20 Mbps,
H.264, GovLength 13, smoothing 1). The only variable being tested is the
capture method: SD card vs RTSP. This makes the A-vs-C comparison a clean
single-variable test.

## Implementation: camtool record

Recording is handled by the `record` command in `camtool.py`:

```bash
python3 camtool.py --profile-dir ../camera record sukabumi-cam1 \
    --duration 5 --output capture.mp4
```

The command performs:

1. **Start recording** — `PUT /ISAPI/ContentMgmt/record/control/manual/start/tracks/101`
2. **Wait** for the specified duration
3. **Stop recording** — `PUT /ISAPI/ContentMgmt/record/control/manual/stop/tracks/101`
4. **Search** for the file — `POST /ISAPI/ContentMgmt/search` (time range with 5s clock-skew buffer)
5. **Download** the file — `GET /ISAPI/ContentMgmt/download?playbackURI=<uri>`

### Check SD card status

```bash
python3 camtool.py --profile-dir ../camera storage sukabumi-cam1
```

## Test Harness Integration

In `run_profile_test.sh`, Profile C uses a different capture method:

```bash
./run_profile_test.sh --profiles a,c --captures 5
```

The harness automatically routes Profile C through `camtool record` instead
of `orc-capture` RTSP pull. Output files land in the same profile directory,
so quality analysis and cross-profile comparison work identically.

## Prerequisites

- Camera must have an SD card inserted and formatted
- Camera storage must be accessible via ISAPI ContentMgmt endpoints
- Camera clock must be synced (NTP) — search uses UTC time ranges

## Risks

- ISAPI recording endpoints may differ between firmware versions
- File search/download adds 5-10 seconds to each capture cycle
- SD card wear (continuous write cycles) — use industrial-grade card
- Sukabumi duty cycle needs to account for the extra download time
