# ChArUco Calibration Board

A ChArUco (Charuco + ArUco) board for camera intrinsic calibration, sized for US Letter paper. Designed for the ANNKE C1200 (12MP, 134° FOV, ~2.7mm focal length) but works for any camera.

## Why ChArUco?

A ChArUco board combines a checkerboard with ArUco markers. Advantages over a plain checkerboard:
- **Partial visibility works** — the board doesn't need to be fully in frame. Each ArUco marker uniquely identifies its position, so corners are detected even when the board is partially occluded or extends beyond the frame edges.
- **More robust detection** — ArUco markers are detected first, then sub-pixel checkerboard corners are refined within the known structure.
- **Better for wide-angle lenses** — critical for the ANNKE's 134° FOV where board edges will be heavily distorted.

## Board Parameters

| Parameter | Value |
|-----------|-------|
| Layout | 5 columns x 7 rows |
| Square size | 38mm |
| Marker size | 28mm (0.74 ratio) |
| ArUco dictionary | `DICT_4X4_50` |
| ArUco markers | 17 |
| Checkerboard corners | 24 per image |
| Paper | US Letter (8.5" x 11") |
| Resolution | 300 DPI |

## Printing

1. Open `charuco_5x7_letter.png` and print it
2. **Set scale to 100%** — do NOT use "fit to page" or "shrink to fit"
3. Use a laser printer if possible (sharper edges, no ink bleed)
4. Print on rigid card stock or mount on a flat surface (foam board, clipboard)

### Verify Print Dimensions

Measure any square with a ruler — it should be **38mm +/- 0.5mm**. If it's off, your printer scaled the image. Re-print with scaling set to exactly 100%.

## Capturing Calibration Images

Capture **15-20 images** of the board with the target camera. Quality matters more than quantity.

### Guidelines

- **Vary the board angle** — tilt it left/right, up/down (15-45 degrees from camera axis)
- **Cover the full frame** — place the board in all regions: center, corners, edges
- **Keep it in focus** — the board should be sharp in each image
- **Distance:** 1-3m from the camera
- **Lighting:** even, avoid glare or shadows on the board
- **Hold steady** — no motion blur
- **Flat surface** — the board must be planar (no bending)

### What makes a good calibration set

- Board appears in all four quadrants and center of the frame
- Mix of orientations (not all straight-on)
- At least 3-4 images with strong tilt
- Each image detects at least 8-10 corners

## Intrinsic Calibration is Distance-Independent

Camera intrinsics (focal length, principal point, distortion coefficients) are properties of the lens, not the scene. Calibrating at 2-3m in an office is valid for 10-30m field deployment. The calibration captures how the lens maps 3D rays to 2D pixels, which doesn't change with subject distance.

## Where This Fits in the OpenRiverCam Workflow

Camera intrinsic calibration is the first step in establishing the measurement chain that converts pixel movements into real-world velocities. The full chain is:

1. **Intrinsic calibration** (this board) — measures lens distortion so it can be corrected
2. **Site survey** — RTK survey of ground control points to 2-3cm accuracy
3. **Image orientation** — correct for camera rotation/flip
4. **Coordinate transformation** — match GCPs in image to surveyed positions
5. **Velocity measurement** — track surface features and convert pixel movement to m/s
6. **Discharge calculation** — integrate velocity across channel cross-section

Without intrinsic calibration, lens distortion (especially barrel distortion from wide-angle lenses like the ANNKE C1200) causes pixel measurements to be inaccurate. The error is worst near image edges — exactly where river banks and GCPs often appear. Uncorrected distortion can introduce 5-10% velocity errors.

### PyORC Documentation References

The [PyORC documentation](https://localdevices.github.io/pyorc/) covers the full camera configuration workflow:

- **[Camera configurations](https://localdevices.github.io/pyorc/user-guide/camera_config/)** — Setting up intrinsic parameters (`camera_matrix`, `dist_coeffs`), ground control points, lens position, and area of interest. This is the main reference for how calibration results feed into PyORC.

- **[Camera intrinsic matrix and distortion coefficients](https://localdevices.github.io/pyorc/user-guide/camera_config/)** — Explains how the camera matrix and distortion coefficients relate pixel coordinates to the real world. PyORC can auto-optimize focal length from 4+ GCPs and radial distortion from 6+ GCPs with varying elevations, but for wide-angle lenses like the ANNKE C1200 (134° FOV), pre-calibrating with this ChArUco board is strongly recommended.

- **[Ground control points](https://localdevices.github.io/pyorc/user-guide/camera_config/)** — How to measure and enter GCPs (`src` pixel coordinates + `dst` real-world coordinates), water level references (`z_0`, `h_ref`), and CRS settings. GCPs should be well-distributed across the field of view.

- **[Velocimetry](https://localdevices.github.io/pyorc/user-guide/velocimetry/)** — How PyORC uses the calibrated camera configuration to track surface features and compute real-world velocities.

### Using Calibration Results with PyORC

After running ChArUco calibration (see code below), pass the resulting `camera_matrix` and `dist_coeffs` to PyORC:

**API approach:**
```python
import pyorc

cam_config = pyorc.CameraConfig(height=3072, width=4096)  # ANNKE C1200 resolution
# camera_matrix and dist_coeffs are set, then configure GCPs:
cam_config.set_gcps(src=src, dst=dst, z_0=z_0, crs=crs)
```

**CLI approach** (if you have the values from calibration):
```
pyorc camera-config --focal_length <fx_pixels> --k1 <k1> --k2 <k2> ...
```

PyORC's built-in lens calibration (`set_lens_calibration()`) uses a standard chessboard pattern via video. This ChArUco board offers a more robust alternative — especially for wide-angle lenses where partial board visibility and edge distortion make plain chessboard detection unreliable.

## Using in Calibration Code

Use these parameters to reconstruct the board and run calibration:

```python
import cv2
import numpy as np
import glob

# Reconstruct the board
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
board = cv2.aruco.CharucoBoard((5, 7), 0.038, 0.028, aruco_dict)  # meters
detector_params = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(aruco_dict, detector_params)

# Collect corners from calibration images
all_charuco_corners = []
all_charuco_ids = []

for image_path in sorted(glob.glob("calibration_images/*.jpg")):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect ArUco markers
    corners, ids, rejected = detector.detectMarkers(gray)
    if ids is None or len(ids) < 4:
        continue

    # Refine to ChArUco corners
    ret, charuco_corners, charuco_ids = cv2.aruco.interpolateCornersCharuco(
        corners, ids, gray, board
    )
    if ret >= 6:
        all_charuco_corners.append(charuco_corners)
        all_charuco_ids.append(charuco_ids)

# Calibrate
ret, camera_matrix, dist_coeffs, rvecs, tvecs = cv2.aruco.calibrateCameraCharuco(
    all_charuco_corners, all_charuco_ids, board, gray.shape[::-1], None, None
)

print(f"RMS reprojection error: {ret:.4f} pixels")
print(f"Camera matrix:\n{camera_matrix}")
print(f"Distortion coefficients: {dist_coeffs.ravel()}")

# Save for use with PyORC
np.savez("annke_c1200_intrinsics.npz",
         camera_matrix=camera_matrix,
         dist_coeffs=dist_coeffs)
```

## Regenerating the Board

```bash
# Requires opencv-contrib-python and numpy
python generate_charuco_board.py

# Or with uv (no install needed):
uv run --with opencv-contrib-python --with numpy python generate_charuco_board.py
```

## Files

- `generate_charuco_board.py` — generates the board PNG
- `charuco_5x7_letter.png` — the printable board (300 DPI, US Letter)
- `README.md` — this file
