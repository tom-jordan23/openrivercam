# ORC Software Compatibility Check

**Date:** January 8, 2026
**Context:** Sukabumi (1 USB camera + IR) and Jakarta (2 PoE cameras)

## Summary

| Component | Status | Risk | Notes |
|-----------|--------|------|-------|
| Single-camera (Sukabumi) | ⚠️ Conditional | Medium | Validate dynamic IR switching |
| USB camera capture | ⚠️ Not confirmed | Medium | May need opencv/ffmpeg driver code |
| PoE camera (RTSP) | ✅ Likely works | Low | Validate with real cameras |
| Dual camera (Jakarta) | ⚠️ Unclear | Medium | Clarify multi-camera intent |
| Time-based scheduling | ✅ Works | Low | Config supports start_time/night_time |
| Hardware IR relay | ✅ Good approach | Low | Bypasses need for software changes |

## Key Findings

### 1. Single-Camera + IR Mode
The codebase explicitly flags this as needing validation:
> "With a single camera, ORC software may require modification to dynamically switch between day and night capture settings on the same camera."

**Mitigation:** Your hardware relay approach (Tendelux + Numato) handles IR control independently of ORC software. This is the right approach.

### 2. USB Camera Support
Current scripts use `picamera2` (Pi CSI cameras only). USB/UVC cameras will need:
- `opencv-python` with V4L2 capture, OR
- Direct `ffmpeg` with v4l2 device

**Effort:** ~4-8 hours to adapt capture code

### 3. PoE/RTSP Cameras
RTSP integration code not visible in the repo (may be in main ORC software). Should work with standard OpenCV RTSP capture.

## Recommendations

1. **Keep hardware IR relay approach** - avoids software complexity
2. **Test USB camera capture early** - before deployment
3. **Validate RTSP with actual cameras** before shipping
4. **Plan 1-2 weeks buffer** for any software integration work

## Action Items

- [ ] Test USB camera with ORC on a Pi 5
- [ ] Test RTSP stream from PoE camera candidate
- [ ] Confirm single-camera mode works with scheduled captures
- [ ] Document any code changes needed
