#!/usr/bin/env python3
"""Generate a 5x7 ChArUco calibration board for US Letter paper at 300 DPI.

Board parameters:
    - 5 columns x 7 rows
    - Square size: 38mm
    - Marker size: 28mm (ratio 0.74)
    - Dictionary: DICT_4X4_50
    - 17 ArUco markers, 24 checkerboard corners

Output: charuco_5x7_letter.png (2550 x 3300 px, 300 DPI)

Usage:
    python generate_charuco_board.py
    # or with uv:
    uv run --with opencv-contrib-python --with numpy python generate_charuco_board.py
"""

import os
import struct
import zlib
import cv2
import numpy as np

# Board parameters
COLS = 5          # number of squares in X
ROWS = 7          # number of squares in Y
SQUARE_MM = 38    # square side length in mm
MARKER_MM = 28    # marker side length in mm (0.74 ratio)

# US Letter at 300 DPI
DPI = 300
PAGE_W_PX = 2550  # 8.5" x 300
PAGE_H_PX = 3300  # 11" x 300

# Pixel-exact square size: round to nearest integer pixel
MM_PER_INCH = 25.4
PX_PER_MM = DPI / MM_PER_INCH  # ~11.811 px/mm
SQUARE_PX = round(SQUARE_MM * PX_PER_MM)  # 461 px

# Board dimensions in pixels (from integer square size)
BOARD_W_PX = COLS * SQUARE_PX
BOARD_H_PX = ROWS * SQUARE_PX

# Actual printed size (may differ from nominal by <0.1mm due to rounding)
ACTUAL_SQUARE_MM = SQUARE_PX / PX_PER_MM


def _set_png_dpi(filepath, dpi):
    """Inject a pHYs chunk into a PNG file to set DPI metadata.

    macOS Preview (and most image viewers) read the pHYs chunk to determine
    print size. Without it, the image defaults to 72 DPI and prints enormous.
    """
    ppm = int(round(dpi / MM_PER_INCH * 1000))  # pixels per meter
    # pHYs chunk: 4 bytes X ppm + 4 bytes Y ppm + 1 byte unit (1 = meter)
    phys_data = struct.pack(">IIB", ppm, ppm, 1)
    phys_crc = struct.pack(">I", zlib.crc32(b"pHYs" + phys_data) & 0xFFFFFFFF)
    phys_chunk = struct.pack(">I", 9) + b"pHYs" + phys_data + phys_crc

    with open(filepath, "rb") as f:
        data = f.read()

    # Insert pHYs right after the IHDR chunk (first chunk after 8-byte PNG signature)
    # IHDR is always first: 8 (sig) + 4 (len) + 4 (type) + 13 (data) + 4 (crc) = 33 bytes
    ihdr_end = 33
    with open(filepath, "wb") as f:
        f.write(data[:ihdr_end] + phys_chunk + data[ihdr_end:])


def generate_board():
    """Generate and save the ChArUco board image."""
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
    board = cv2.aruco.CharucoBoard((COLS, ROWS), SQUARE_MM, MARKER_MM, aruco_dict)

    # Generate board at exact pixel dimensions (margin=0, we'll add our own)
    board_img = board.generateImage((BOARD_W_PX, BOARD_H_PX), marginSize=0)

    # Create white letter-sized page.
    # Push the board to the top (small top margin) to leave room for text below.
    page = np.ones((PAGE_H_PX, PAGE_W_PX), dtype=np.uint8) * 255
    x_off = (PAGE_W_PX - BOARD_W_PX) // 2
    top_margin = int(3 * PX_PER_MM)  # ~3mm from top edge
    y_off = top_margin
    page[y_off:y_off + BOARD_H_PX, x_off:x_off + BOARD_W_PX] = board_img

    # Convert to BGR for text rendering
    page_color = cv2.cvtColor(page, cv2.COLOR_GRAY2BGR)

    # Add verification text below the board
    font = cv2.FONT_HERSHEY_SIMPLEX
    below_board = y_off + BOARD_H_PX

    # Verification line
    verify_y = below_board + int(5 * PX_PER_MM)
    cv2.putText(page_color,
                f"VERIFY: measure one square with a ruler -- must be {SQUARE_MM}mm",
                (x_off, verify_y), font, 0.75, (0, 0, 0), 2, cv2.LINE_AA)

    # Parameter reference line
    params_y = verify_y + int(4.5 * PX_PER_MM)
    cv2.putText(page_color,
                f"ChArUco {COLS}x{ROWS} | Square: {SQUARE_MM}mm | "
                f"Marker: {MARKER_MM}mm | DICT_4X4_50",
                (x_off, params_y), font, 0.6, (100, 100, 100), 1, cv2.LINE_AA)

    # Save with 300 DPI metadata (OpenCV doesn't write PNG pHYs chunk)
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(output_dir, "charuco_5x7_letter.png")
    cv2.imwrite(output_path, page_color)
    _set_png_dpi(output_path, DPI)

    # Print summary
    print(f"ChArUco board generated: {output_path}")
    print(f"  Layout: {COLS} cols x {ROWS} rows")
    print(f"  Square size: {SQUARE_MM}mm (actual: {ACTUAL_SQUARE_MM:.2f}mm)")
    print(f"  Marker size: {MARKER_MM}mm")
    print(f"  Square pixels: {SQUARE_PX} px")
    print(f"  Board area: {BOARD_W_PX} x {BOARD_H_PX} px")
    print(f"  Page: {PAGE_W_PX} x {PAGE_H_PX} px @ {DPI} DPI (US Letter)")
    margin_h = (PAGE_W_PX - BOARD_W_PX) / 2 / PX_PER_MM
    margin_v = (PAGE_H_PX - BOARD_H_PX) / 2 / PX_PER_MM
    print(f"  Margins: {margin_h:.1f}mm horizontal, {margin_v:.1f}mm vertical")
    print(f"  Dictionary: DICT_4X4_50")
    print(f"  Markers: 17 ArUco markers, 24 checkerboard corners")


if __name__ == "__main__":
    generate_board()
