#!/usr/bin/env python3
"""
Normalize Sukabumi incoming inspection photos.

- Resize to consistent 800px long edge (preserving aspect ratio)
- Rename with descriptive part names
- Keep originals in originals/ subfolder
"""

import os
import shutil
from PIL import Image

PHOTOS_DIR = os.path.dirname(os.path.abspath(__file__))
ORIGINALS_DIR = os.path.join(PHOTOS_DIR, "originals")
LONG_EDGE = 800

# Mapping: original filename -> (new_name, part_description)
PHOTO_MAP = {
    "IMG_1281.png": "raspberry_pi_5.png",
    "IMG_1282.png": "witty_pi_5_hat.png",
    "IMG_1283.png": "stacking_headers.png",
    "IMG_1284.png": "gpio_breakout_g469.png",
    "IMG_1285.png": "usb_flash_256gb.png",
    "IMG_1286.png": "sd_cards.png",
    "IMG_1287.png": "active_cooler.png",
    "IMG_1288.png": "quectel_eg25g.png",
    "IMG_1289.png": "wwan_usb_adapter.png",
    "IMG_1290.png": "proxicast_antenna.png",
    "IMG_1291.png": "annke_c1200_camera.png",
    "IMG_1292.png": "poe_switch_12v.png",
    "IMG_1293.png": "vertical_mount.png",
    "IMG_1294.png": "hydreon_rg15.png",
    "IMG_1295.png": "nema_4x_enclosure.png",
    "IMG_1297.png": "din_rail.png",
    "IMG_1298.png": "din_clip_pi.png",
    "IMG_1299.png": "din_terminal_blocks.png",
    "IMG_1300.png": "gore_vent_m12.png",
    "IMG_1301.png": "status_leds.png",
    "IMG_1302.png": "ip67_pushbutton.png",
    "IMG_1303.png": "cable_glands.png",
    "IMG_1304.png": "12v_power_couplers.png",
    "IMG_1305.png": "dielectric_grease.png",
    "IMG_1306.png": "conformal_coating.png",
}


def normalize_image(src_path, dst_path, long_edge=LONG_EDGE):
    """Resize image so longest edge = long_edge, save as PNG."""
    img = Image.open(src_path)

    w, h = img.size
    if max(w, h) <= long_edge:
        scale = 1.0
    else:
        scale = long_edge / max(w, h)

    new_w = int(w * scale)
    new_h = int(h * scale)

    if scale != 1.0:
        img = img.resize((new_w, new_h), Image.LANCZOS)

    # Strip metadata by saving clean
    clean = Image.new(img.mode, img.size)
    clean.putdata(list(img.getdata()))
    clean.save(dst_path, "PNG", optimize=True)
    return new_w, new_h


def main():
    # Create originals backup dir
    os.makedirs(ORIGINALS_DIR, exist_ok=True)

    results = []

    for orig_name, new_name in sorted(PHOTO_MAP.items()):
        src = os.path.join(PHOTOS_DIR, orig_name)
        if not os.path.exists(src):
            print(f"  SKIP (not found): {orig_name}")
            continue

        # Backup original
        backup = os.path.join(ORIGINALS_DIR, orig_name)
        if not os.path.exists(backup):
            shutil.copy2(src, backup)

        # Normalize
        dst = os.path.join(PHOTOS_DIR, new_name)
        new_w, new_h = normalize_image(src, dst)

        orig_size = os.path.getsize(src)
        new_size = os.path.getsize(dst)
        orientation = "landscape" if new_w > new_h else "portrait"

        results.append((orig_name, new_name, new_w, new_h, orientation,
                         orig_size, new_size))
        print(f"  {orig_name} -> {new_name}  ({new_w}x{new_h} {orientation})"
              f"  {orig_size//1024}KB -> {new_size//1024}KB")

    # Remove originals from photos dir (now backed up)
    for orig_name in PHOTO_MAP:
        orig_path = os.path.join(PHOTOS_DIR, orig_name)
        if os.path.exists(orig_path):
            os.remove(orig_path)

    print(f"\nDone: {len(results)} photos normalized.")
    print(f"Originals backed up to: {ORIGINALS_DIR}/")


if __name__ == "__main__":
    main()
