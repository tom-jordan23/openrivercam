# Profile F: Digital Crop / Reduced FOV

## Concept

The ANNKE C1200 has a 134-degree horizontal field of view. For most river
cross sections, we only need the center portion of the frame — the edges
capture sky, banks, and vegetation that ORC ignores.

If the camera supports a digital crop or Region of Interest (ROI) via ISAPI,
we can reduce the encoded frame to just the useful portion. Fewer pixels to
encode = more bits per pixel = better texture preservation at the same bitrate.

## Status: NEEDS INVESTIGATION

Before creating the XML config, we need to determine:

1. Does the ANNKE C1200 / Hikvision G6 platform support digital crop via ISAPI?
   - Check: `GET /ISAPI/Image/channels/1/crop`
   - Check: `GET /ISAPI/Streaming/channels/101/capabilities` for crop options
   - Check: `GET /ISAPI/Image/channels/1/regionEnhance`

2. If so, what are the crop parameters? (x, y, width, height as percentages or pixels)

3. Does cropping happen at the sensor level (before encoding) or as a post-encode crop?
   - Sensor-level crop: encoder gets fewer pixels, quality improves
   - Post-encode crop: no quality benefit, just smaller file

## Test in the field

```bash
# Check if crop endpoint exists
curl --digest -u admin:PASSWORD http://192.168.50.100/ISAPI/Image/channels/1/crop

# Check streaming capabilities for ROI
curl --digest -u admin:PASSWORD http://192.168.50.100/ISAPI/Streaming/channels/101/capabilities
```

If the camera supports sensor-level crop, create a streaming_101.xml config
with the crop parameters set to frame the cross section tightly.

## Fallback

If digital crop is not available via ISAPI, the alternative is to use
Profile B (720p) which achieves a similar effect — fewer pixels, more
bits per pixel — but through resolution reduction rather than FOV reduction.
