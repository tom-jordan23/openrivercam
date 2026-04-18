# ANNKE C1200 → Genuine Hikvision Firmware Cross-Flash (Backup Plan)

**Research Date:** 2026-04-18
**Status:** Not executed. Documented as a contingency in case the RTSP-live capture path cannot meet PIV pass-rate requirements.
**Trigger:** Only pursue if Profile A/B RTSP-live capture fails to deliver an acceptable PIV pass rate, i.e. the ORC algorithm cannot reliably extract surface velocities from the delivered video.

---

## Executive Summary

The ANNKE C1200 is a Hikvision OEM camera built on the Hikvision G6 platform, running ANNKE-branded firmware. ANNKE's firmware strips a subset of the Hikvision ISAPI surface — notably the HTTP `ContentMgmt/download` endpoint used to pull finished recordings off the camera's SD card. This broke Profile C (camera-local SD recording, then file-based fetch), forcing us to fall back to RTSP-live capture for all production deployments.

Cross-flashing the camera with genuine Hikvision firmware is reported by the IP Cam Talk community to restore the full ISAPI surface, which would make Profile C viable again. Profile C is attractive because it eliminates RTSP transport overhead (10–20% of the configured bitrate) and lets the encoder run at the full CBR budget with zero real-time delivery constraints.

This document captures the motivation, the procedure outline, the risks, and the go/no-go criteria so we can execute quickly if the RTSP path proves inadequate for PIV.

---

## 1. Why This Matters

### The Profile C gap

Profile C (`camera/profiles/profile-c/CAPTURE_NOTES.md`) was designed to bypass RTSP transport losses by recording locally on the camera SD card and then pulling the finished file via HTTP:

1. `PUT /ISAPI/ContentMgmt/record/control/manual/start/tracks/101`
2. Wait N seconds
3. `PUT /ISAPI/ContentMgmt/record/control/manual/stop/tracks/101`
4. `POST /ISAPI/ContentMgmt/search`
5. `GET /ISAPI/ContentMgmt/download?playbackURI=<uri>`   ← **missing on ANNKE firmware**

Step 5 is the blocker. On genuine Hikvision firmware this endpoint returns the recorded file over HTTP at wire speed. ANNKE's firmware returns the endpoint for still images only — recorded video files are not downloadable over HTTP ContentMgmt.

### Current fallback in code

`camera/camtool.py:720-765` (function `_download_recording`) implements the HikLoad `--ffmpeg` workaround: after `ContentMgmt/search` returns a `playbackURI`, the tool uses `ffmpeg -rtsp_transport tcp -c copy` to pull the clip via RTSP playback with codec-copy (remux only, no re-encode). Byte quality is preserved, but **the whole point of Profile C was to avoid RTSP**, so this workaround gives up the quality budget advantage. Profile C was therefore not selected for production; deployment uses an RTSP-live profile.

### What cross-flash would restore

Genuine Hikvision firmware on the same G6 hardware is reported to expose the full `ContentMgmt/download` HTTP endpoint, making Profile C viable as originally designed:

- Encoder runs at full configured CBR (e.g. 20 Mbps) with no real-time transport coupling
- File pulled over the PoE Ethernet link at ~100 Mbps, faster than real-time
- No RTSP packet loss, no transport jitter, no buffering artifacts

Expected quality gain vs. Profile A: 15–25% higher effective bitrate delivered to disk, with cleaner motion under fast-flowing water. Whether that translates to a meaningful PIV pass-rate improvement is the empirical question.

---

## 2. Risks

### Bricking

G6-platform cross-flash is not guaranteed. IP Cam Talk threads document:

- Some ANNKE firmware revisions reject the Hikvision `digicap.dav` installer at the web UI uploader.
- A failed flash can brick the camera; recovery requires TFTP boot from the internal bootloader, which in turn requires opening the housing and wiring to the UART pads on some models.
- Hardware revision matters. The "recipe" on IP Cam Talk applies to specific ANNKE C1200 hardware revisions — ours must be confirmed before flashing.

### Warranty

Cross-flashing voids ANNKE warranty and departs from the supported firmware image. If an unrelated hardware failure occurs later, RMA is off the table.

### Field service

The deployed ANNKE firmware is something the PMI office can recover from via factory reset + `camtool.py push`. A cross-flashed camera adds an extra dimension to troubleshooting: any replacement unit (spare) must also be cross-flashed to match, or the deployed config profile (Profile C) won't work on the replacement.

### Boot self-check LED

Cross-flash does not solve ISS-004 (white-LED boot self-check). That's a pre-OS hardware behavior; firmware cannot suppress it. Evaluate this independently.

---

## 3. Prerequisites

Before attempting a cross-flash:

- [ ] At least one uncommitted spare ANNKE C1200 available as a test victim. We have one in-country (from the 2-pack purchase per `BOM_Sukabumi.md`). **Never flash an installed production camera first.**
- [ ] Web UI access to the spare — admin credentials, reachable on `192.168.50.0/24`.
- [ ] Full ANNKE config backup pulled via `camtool.py pull <cam>` and committed to git.
- [ ] ANNKE firmware file backed up (download from ANNKE web UI's "current firmware" or manufacturer site) so we can roll back if cross-flash fails in a recoverable way.
- [ ] Hikvision firmware image matching the G6 platform, sourced from either:
  - Hikvision region-appropriate support site (`digicap.dav` binary), or
  - A known-good community mirror referenced in the IP Cam Talk thread.
- [ ] Hardware revision of the test unit confirmed against the cross-flash recipe's supported revisions (check the sticker on the camera body and the ANNKE firmware version string before flashing).
- [ ] TFTP server prepared on a laptop in case recovery is needed (tftpd on macOS or `tftpd-hpa` on Linux, serving the Hikvision recovery image from `192.168.1.64` — the Hikvision bootloader default).
- [ ] Physical access to the camera body for worst-case UART recovery (screwdriver set, USB-TTL adapter).

---

## 4. Procedure Outline

This is an outline, not a step-by-step. The authoritative recipe is the IP Cam Talk thread, which may have been updated since this doc was written. Re-read it before flashing.

### Phase 1 — Non-destructive reconnaissance

1. Pull and commit the spare camera's current ANNKE config: `python3 camtool.py pull <spare-name>`.
2. From web UI, record: hardware version, current firmware version, model suffix.
3. Cross-reference hardware version against the IP Cam Talk thread's known-working revisions.
4. Hit the missing endpoint directly to confirm failure mode (not just a URL typo):
   ```
   curl -v --digest -u admin:PASSWORD \
     'http://192.168.50.100/ISAPI/ContentMgmt/download?playbackURI=...'
   ```
5. Download a copy of the shipping ANNKE firmware (for rollback).

### Phase 2 — Flash

1. Put laptop on the same subnet as the spare camera. Disconnect the camera from the production network.
2. Upload Hikvision `digicap.dav` through the ANNKE web UI's firmware update page.
   - If it rejects the file ("incompatible"), do not force. Fall back to the TFTP recovery method documented in the IP Cam Talk thread.
3. Wait for the camera to reboot. First boot after cross-flash can take 5–10 minutes while the new firmware initializes NAND partitions.
4. If the camera comes back on a different IP (Hikvision default is `192.168.1.64`), locate it with SADP or a ping sweep.

### Phase 3 — Verification

Run these checks in order. Stop and roll back at any failure.

1. **Basic health:** Web UI login works with Hikvision default credentials (or activation flow runs).
2. **ISAPI basics unchanged:** `GET /ISAPI/System/deviceInfo` returns 200 with sensible XML.
3. **Streaming still works:** Pull an RTSP clip with `orc-capture` — confirms encoder, sensor, PoE, and network path are fine.
4. **ContentMgmt surface restored:** The make-or-break test —
   ```bash
   python3 camtool.py record <spare-name> --duration 5 --output test.mp4
   ```
   On success, `test.mp4` should be present and playable. Inspect the `_download_recording` path in `camtool.py`: the code should be switched to use HTTP `ContentMgmt/download` instead of RTSP playback. (See §6.)
5. **Bitrate improvement:** Run the profile test harness with Profile C enabled, compare against Profile A baseline. Look for delivered bitrate at/above the configured CBR target and an improved PIV pass rate on the resulting clips.

### Phase 4 — Rollback if needed

- If verification fails at any step, re-flash the ANNKE firmware (preserved in Phase 1).
- If the camera is unresponsive, attempt TFTP recovery per the IP Cam Talk thread.
- If TFTP recovery fails, treat the unit as dead; use the remaining spare as a replacement and continue with the RTSP-live path.

---

## 5. Decision Triggers

Execute this plan only if one of the following is true:

- Profile A/B RTSP-live capture delivers acceptable bitrate but PIV pass rate is below the acceptance threshold on the Jakarta or Sukabumi reference clips.
- Post-deployment, the site's observed water conditions (faster flow, lower visual texture) push PIV pass rates below acceptable during routine processing, and the root cause is traced to encoder bitrate starvation rather than lighting/angle/GCPs.

Do **not** execute speculatively. The RTSP-live path is working in production; the cost of cross-flash (bricking risk, service complexity) is real.

---

## 6. Code Change Required On Success

If cross-flash works and we adopt Profile C in production, `_download_recording()` in `camera/camtool.py:720-765` should be updated:

- Current implementation: RTSP playback via ffmpeg codec-copy (HikLoad `--ffmpeg` mode).
- After cross-flash: switch to HTTP `GET /ISAPI/ContentMgmt/download?playbackURI=<uri>` as originally designed in `profile-c/CAPTURE_NOTES.md:39`.

Keep the RTSP fallback available for any camera that happens to be running unflashed ANNKE firmware (e.g. an emergency replacement unit before it can be cross-flashed). Detect which path to use based on a successful `HEAD /ISAPI/ContentMgmt/download` probe at tool startup, or via a per-camera flag in `cameras.json`.

---

## 7. Open Questions

- Does the G6 hardware in our specific ANNKE C1200 batch match the cross-flash recipes on IP Cam Talk, or is our batch too new? **Needs a hardware-version check on the spare before any attempt.**
- Does cross-flashed firmware interact with the PoE camera auto-activation flow used by the Hikvision SADP tool? If so, factory-reset recovery at PMI office gets more complicated.
- If we cross-flash one camera (e.g. Jakarta cam1), do we need to cross-flash all of them, or is Profile C per-camera selectable so we can run Profile C on some and Profile A on others? **Profile is per-camera in `cameras.json`, so mixed operation should work.**
- Does cross-flashed firmware affect the SD card write cycle count Profile C was already flagged as a wear risk for?

---

## 8. References

### In-repo

- `camera/profiles/profile-c/CAPTURE_NOTES.md` — original Profile C design, including the 5-step ISAPI sequence.
- `camera/camtool.py:720-765` (`_download_recording`) — the RTSP-playback workaround currently in use.
- `camera/camtool.py:568-720` — full Profile C recording implementation (`cmd_record`, `_build_search_xml`, `_parse_search_results`).
- `research/camera_isapi_config_management.md` — overall ISAPI protocol context and the camtool.py design rationale.
- `ISSUE_LOG.md` ISS-004 — separate motivation (boot-flash LED) that also considered cross-flash; conclusion there was "unlikely to help per community reports." That conclusion is specific to ISS-004; it does **not** apply to the ContentMgmt/download issue, which is a userspace ISAPI gap and is the kind of thing firmware can genuinely fix.

### External

- [Annke Firmware to Hikvision Firmware: HOW TO — IP Cam Talk](https://ipcamtalk.com/threads/annke-firmware-to-hikvision-firmware-how-to.56888/) — primary community recipe. Re-read before any flash attempt; content and supported revisions evolve.
- [How to Activate Hikvision IP Camera Using SADP Tool](https://sadptool.net/activate-hikvision-ip-camera/) — post-flash activation flow, if the cross-flashed camera comes up requiring Hikvision activation.
