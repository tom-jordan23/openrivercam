# Profile C: Camera-Local Recording — Implementation Notes

## Concept

Instead of pulling video over RTSP in real-time (where network buffering
limits effective bitrate), the camera records to its own SD card at full
encoder quality. The Pi then copies the finished file.

## Why This Matters

RTSP transport overhead consumes 10-20% of the configured bitrate. With
CBR at 16 Mbps, actual delivered bitrate is 12-15.5 Mbps. By recording
locally, the camera encoder gets the full bitrate budget with zero
transport loss. VBR can even peak above the target for complex scenes
(water surface texture with variable motion).

## Implementation Options

### Option 1: ISAPI Manual Recording + File Download

1. Pi triggers manual recording via ISAPI:
   ```
   PUT /ISAPI/ContentMgmt/record/control/manual/start/tracks/101
   ```
2. Wait 5 seconds
3. Stop recording:
   ```
   PUT /ISAPI/ContentMgmt/record/control/manual/stop/tracks/101
   ```
4. Search for the recorded file:
   ```
   POST /ISAPI/ContentMgmt/search
   ```
   (with XML body specifying time range)
5. Download the file:
   ```
   GET /ISAPI/ContentMgmt/download?playbackURI=<uri-from-search>
   ```

**Pros:** Pure ISAPI, no additional services needed
**Cons:** Multiple HTTP round-trips, search/download adds latency

### Option 2: FTP Push from Camera

1. Configure camera to FTP captured files to the Pi
2. Pi runs a lightweight FTP server (vsftpd)
3. Camera records on event/schedule, pushes to Pi

**Pros:** Camera handles the file transfer
**Cons:** Requires FTP server on Pi, less control over timing

### Option 3: NFS Mount

1. Pi exports a directory via NFS
2. Camera mounts the NFS share
3. Camera records directly to the NFS mount

**Pros:** Appears as local storage to camera
**Cons:** NFS adds network dependency during recording (defeats the purpose
if network is the bottleneck)

## Recommended: Option 1

ISAPI manual recording gives us the most control. The flow in orc-capture
would be:

```bash
# Instead of ffmpeg RTSP pull:
# 1. Start recording
curl --digest -u $USER:$PASS -X PUT \
  "http://$CAMERA_IP/ISAPI/ContentMgmt/record/control/manual/start/tracks/101"

# 2. Wait capture duration
sleep $CAPTURE_DURATION

# 3. Stop recording
curl --digest -u $USER:$PASS -X PUT \
  "http://$CAMERA_IP/ISAPI/ContentMgmt/record/control/manual/stop/tracks/101"

# 4. Search for the file (POST with time range XML)
# 5. Download the file to INCOMING_DIR
# 6. Run quality gate on downloaded file
```

## Prerequisites

- Camera must have an SD card inserted and formatted
- Camera storage must be configured (ISAPI ContentMgmt/Storage)
- orc-capture needs a new capture mode (e.g., CAPTURE_METHOD=isapi-local)

## Testing Plan

1. Manually test the ISAPI recording endpoints from the Pi
2. Verify file appears in search results
3. Download and check bitrate with ffprobe
4. Compare against RTSP capture from same scene
5. If bitrate is consistently above 20 Mbps, this is the winner

## Risks

- ISAPI recording endpoints may differ between firmware versions
- File search/download adds 5-10 seconds to each capture cycle
- SD card wear (continuous write cycles) — use industrial-grade card
- Sukabumi duty cycle needs to account for the extra copy time
