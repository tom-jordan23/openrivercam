#!/usr/bin/env python3
"""Generate a 5x7 ChArUco calibration board for US Letter paper at 300 DPI.

Board parameters:
    - 5 columns x 7 rows
    - Square size: 39mm
    - Marker size: 29mm (ratio 0.74)
    - Dictionary: DICT_4X4_50
    - 17 ArUco markers, 24 checkerboard corners

Output: charuco_5x7_letter.png (2550 x 3300 px, 300 DPI)

Usage:
    python generate_charuco_board.py
    # or with uv:
    uv run --with opencv-contrib-python --with numpy python generate_charuco_board.py
"""

import os
import cv2
import numpy as np

# Board parameters
COLS = 5          # number of squares in X
ROWS = 7          # number of squares in Y
SQUARE_MM = 39    # square side length in mm
MARKER_MM = 29    # marker side length in mm

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


def generate_board():
    """Generate and save the ChArUco board image."""
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
    board = cv2.aruco.CharucoBoard((COLS, ROWS), SQUARE_MM, MARKER_MM, aruco_dict)

    # Generate board at exact pixel dimensions (margin=0, we'll add our own)
    board_img = board.generateImage((BOARD_W_PX, BOARD_H_PX), marginSize=0)

    # Create white letter-sized page and center the board
    page = np.ones((PAGE_H_PX, PAGE_W_PX), dtype=np.uint8) * 255
    x_off = (PAGE_W_PX - BOARD_W_PX) // 2
    y_off = (PAGE_H_PX - BOARD_H_PX) // 2
    page[y_off:y_off + BOARD_H_PX, x_off:x_off + BOARD_W_PX] = board_img

    # Convert to BGR for text rendering
    page_color = cv2.cvtColor(page, cv2.COLOR_GRAY2BGR)

    # Add parameter text below the board
    text_y = y_off + BOARD_H_PX + int(12 * PX_PER_MM)
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.9
    color = (0, 0, 0)
    thickness = 2
    line_height = int(5 * PX_PER_MM)

    lines = [
        f"ChArUco {COLS}x{ROWS}  |  Square: {SQUARE_MM}mm  |  Marker: {MARKER_MM}mm  |  DICT_4X4_50",
        "Print at 100% scale (no fit-to-page). Verify: one square = 39mm.",
    ]
    for i, line in enumerate(lines):
        cv2.putText(page_color, line, (x_off, text_y + i * line_height),
                    font, font_scale, color, thickness, cv2.LINE_AA)

    # Save
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(output_dir, "charuco_5x7_letter.png")
    cv2.imwrite(output_path, page_color)

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
