#!/usr/bin/env python3
"""
Generate a PDF circuit diagram for the Sukabumi ORC station.
Uses matplotlib to draw a block-level system wiring diagram.

Usage: python3 generate_circuit_pdf.py
Output: circuit_diagram.pdf (in same directory)
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import os

# ── Configuration ──────────────────────────────────────────────────

FIG_W, FIG_H = 22, 17  # inches (landscape A3-ish)
DPI = 150
BG_COLOR = '#FAFAFA'
TITLE_COLOR = '#1a1a2e'
WIRE_12V = '#CC0000'     # red
WIRE_GND = '#333333'     # dark grey
WIRE_5V = '#FF6600'      # orange
WIRE_48V = '#0066CC'     # blue
WIRE_ETH = '#006633'     # green
WIRE_USB = '#6600CC'     # purple
WIRE_GPIO = '#999900'    # olive
BOX_POWER = '#FFE0E0'
BOX_COMPUTE = '#E0E8FF'
BOX_CAMERA = '#E0FFE8'
BOX_NETWORK = '#FFF5E0'
BOX_UI = '#F0E0FF'
BOX_SENSOR = '#E8F8FF'


def draw_box(ax, xy, w, h, label, sublabel='', color='#E8E8E8',
             fontsize=9, sublabel_size=7, bold=True):
    """Draw a rounded component box with label."""
    x, y = xy
    box = FancyBboxPatch((x, y), w, h,
                         boxstyle="round,pad=0.15",
                         facecolor=color, edgecolor='#444444',
                         linewidth=1.2, zorder=2)
    ax.add_patch(box)
    weight = 'bold' if bold else 'normal'
    ax.text(x + w/2, y + h/2 + (0.15 if sublabel else 0),
            label, ha='center', va='center',
            fontsize=fontsize, fontweight=weight, zorder=3)
    if sublabel:
        ax.text(x + w/2, y + h/2 - 0.25,
                sublabel, ha='center', va='center',
                fontsize=sublabel_size, color='#555555', zorder=3,
                style='italic')


def draw_wire(ax, points, color='#CC0000', lw=1.5, style='-', zorder=1):
    """Draw a wire path through a list of (x,y) points."""
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    ax.plot(xs, ys, color=color, linewidth=lw, linestyle=style,
            solid_capstyle='round', zorder=zorder)


def draw_arrow(ax, start, end, color='#CC0000', lw=1.5):
    """Draw a wire with arrowhead."""
    ax.annotate('', xy=end, xytext=start,
                arrowprops=dict(arrowstyle='->', color=color, lw=lw),
                zorder=2)


def draw_label(ax, xy, text, fontsize=7, color='#444444', ha='center',
               rotation=0, va='center'):
    """Draw a text label."""
    ax.text(xy[0], xy[1], text, ha=ha, va=va, fontsize=fontsize,
            color=color, rotation=rotation, zorder=4)


def draw_fuse(ax, xy, label='5A', color=WIRE_12V):
    """Draw a small fuse symbol."""
    x, y = xy
    # fuse body
    ax.plot([x-0.3, x+0.3], [y, y], color=color, lw=2, zorder=2)
    box = FancyBboxPatch((x-0.2, y-0.12), 0.4, 0.24,
                         boxstyle="round,pad=0.03",
                         facecolor='white', edgecolor=color,
                         linewidth=1.5, zorder=3)
    ax.add_patch(box)
    ax.text(x, y, label, ha='center', va='center', fontsize=6,
            color=color, fontweight='bold', zorder=4)


def main():
    fig, ax = plt.subplots(1, 1, figsize=(FIG_W, FIG_H), dpi=DPI)
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 22)
    ax.set_ylim(0, 17)
    ax.set_aspect('equal')
    ax.axis('off')

    # ── Title Block ────────────────────────────────────────────────
    ax.text(11, 16.5, 'SUKABUMI ORC STATION — SYSTEM WIRING DIAGRAM',
            ha='center', va='center', fontsize=16, fontweight='bold',
            color=TITLE_COLOR)
    ax.text(11, 16.1, 'OpenRiverCam  |  Rev B  |  2026-02-16  |  Solar-Powered PoE Camera System',
            ha='center', va='center', fontsize=9, color='#666666')
    ax.plot([1, 21], [15.85, 15.85], color='#AAAAAA', lw=0.8)

    # ── Enclosure boundary ─────────────────────────────────────────
    encl = FancyBboxPatch((3.5, 2.5), 15, 11.5,
                          boxstyle="round,pad=0.3",
                          facecolor='#F5F5F5', edgecolor='#888888',
                          linewidth=2, linestyle='--', zorder=0)
    ax.add_patch(encl)
    ax.text(11, 14.2, 'IP67 COMPUTE ENCLOSURE',
            ha='center', va='center', fontsize=10, fontweight='bold',
            color='#888888', style='italic')

    # ================================================================
    # EXTERNAL POWER (left of enclosure)
    # ================================================================
    draw_box(ax, (0.3, 12.5), 2.5, 1.2,
             '200W Solar Panel', color=BOX_POWER, fontsize=9)
    draw_box(ax, (0.3, 10.5), 2.5, 1.2,
             'Charge Controller', '(site-provided)', color=BOX_POWER)
    draw_box(ax, (0.3, 8.5), 2.5, 1.2,
             '12V 50Ah Battery', 'LiFePO4 / Lead-Acid', color=BOX_POWER)

    # Solar → CC → Battery wires
    draw_wire(ax, [(1.55, 12.5), (1.55, 11.7)], WIRE_12V, lw=2)
    draw_wire(ax, [(1.55, 10.5), (1.55, 9.7)], WIRE_12V, lw=2)

    # Battery → enclosure
    draw_wire(ax, [(2.8, 9.1), (4.2, 9.1)], WIRE_12V, lw=2.5)
    draw_label(ax, (3.5, 9.4), '12V DC\n18AWG', fontsize=6, color=WIRE_12V)

    # Cable gland symbol
    ax.plot([3.8, 3.8], [8.8, 9.4], color='#888888', lw=3, zorder=1)
    draw_label(ax, (3.8, 8.55), 'M12\ngland', fontsize=5, color='#888888')

    # ================================================================
    # TERMINAL BLOCK TB1
    # ================================================================
    draw_box(ax, (4.2, 8.3), 2.2, 1.6,
             'Terminal Block', 'TB1 (Power Dist.)', color='#FFD0D0',
             fontsize=8)

    # ================================================================
    # WITTY PI 5
    # ================================================================
    draw_box(ax, (4.2, 11.0), 2.8, 2.0,
             'Witty Pi 5 HAT+', 'RTC / Sleep-Wake\n5-26V in → 5V USB-C out',
             color=BOX_COMPUTE, fontsize=8, sublabel_size=6)

    # TB1 → Witty Pi (12V)
    draw_wire(ax, [(5.3, 9.9), (5.3, 11.0)], WIRE_12V, lw=2)
    draw_label(ax, (5.6, 10.45), '12V', fontsize=6, color=WIRE_12V)

    # ================================================================
    # RASPBERRY PI 5
    # ================================================================
    draw_box(ax, (8.0, 10.0), 3.5, 3.0,
             'Raspberry Pi 5', '8GB • NodeORC\n5V USB-C powered',
             color=BOX_COMPUTE, fontsize=10, sublabel_size=7)

    # Witty Pi → Pi 5 (5V USB-C)
    draw_wire(ax, [(7.0, 12.0), (8.0, 12.0)], WIRE_5V, lw=2)
    draw_label(ax, (7.5, 12.3), '5V\nUSB-C', fontsize=6, color=WIRE_5V)

    # Witty Pi switched 12V rail
    draw_wire(ax, [(7.0, 11.5), (7.5, 11.5), (7.5, 8.0), (7.5, 7.2)],
              WIRE_12V, lw=1.5, style='--')
    draw_label(ax, (7.1, 7.6), 'Switched\n12V rail', fontsize=5.5,
               color=WIRE_12V, ha='left')

    # ================================================================
    # POE INJECTOR + FUSE
    # ================================================================
    # Fuse
    draw_fuse(ax, (7.5, 6.5), '5A', WIRE_12V)

    draw_box(ax, (6.5, 5.0), 2.8, 1.2,
             'Planet IPOE-260', '12V PoE Injector\n12V→48V PoE',
             color=BOX_CAMERA, fontsize=8, sublabel_size=6)

    # Fuse → PoE injector
    draw_wire(ax, [(7.5, 6.38), (7.5, 6.2)], WIRE_12V, lw=1.5)

    # Switched rail → fuse
    draw_wire(ax, [(7.5, 7.2), (7.5, 6.62)], WIRE_12V, lw=1.5, style='--')

    # PoE injector DATA → Pi Ethernet
    draw_wire(ax, [(9.3, 6.2), (9.3, 7.5), (9.5, 7.5),
                    (9.5, 10.0)], WIRE_ETH, lw=1.5)
    draw_label(ax, (9.8, 8.5), 'DATA\n(Ethernet)', fontsize=5.5,
               color=WIRE_ETH, ha='left')

    # PoE injector DATA+POWER → Camera (goes outside enclosure)
    draw_wire(ax, [(7.9, 5.0), (7.9, 4.2), (7.9, 3.5)], WIRE_48V, lw=2)
    draw_label(ax, (8.3, 4.2), 'Cat6 PoE\n48V + Data', fontsize=5.5,
               color=WIRE_48V, ha='left')

    # Cable gland for Cat6
    ax.plot([7.6, 8.2], [3.3, 3.3], color='#888888', lw=3, zorder=1)
    draw_label(ax, (7.9, 3.0), 'M12 gland\n+ IP68 RJ45', fontsize=5,
               color='#888888')

    # ================================================================
    # CAMERA (external)
    # ================================================================
    draw_box(ax, (6.0, 0.8), 3.8, 1.8,
             'ANNKE C1200', 'PoE Camera (IP67)\n12MP • Built-in IR\n48V PoE powered',
             color=BOX_CAMERA, fontsize=9, sublabel_size=6)

    draw_wire(ax, [(7.9, 3.0), (7.9, 2.6)], WIRE_48V, lw=2)

    # ================================================================
    # LTE MODEM (inside enclosure)
    # ================================================================
    draw_box(ax, (12.5, 12.0), 2.8, 1.5,
             'Quectel EG25-G', 'LTE Cat-4 Modem\nPU201 USB adapter',
             color=BOX_NETWORK, fontsize=8, sublabel_size=6)

    # Pi USB 2.0 → Modem
    draw_wire(ax, [(11.5, 12.5), (12.5, 12.5)], WIRE_USB, lw=1.5)
    draw_label(ax, (12.0, 12.8), 'USB 2.0', fontsize=6, color=WIRE_USB)

    # ================================================================
    # LTE ANTENNAS (external via bulkheads)
    # ================================================================
    draw_box(ax, (12.5, 14.5), 3.2, 0.8,
             'Proxicast ANT-122-S02', 'MIMO LTE Puck (IP67)',
             color=BOX_NETWORK, fontsize=7, sublabel_size=6)

    draw_wire(ax, [(13.5, 13.5), (13.5, 14.5)], '#CC8800', lw=1.2)
    draw_wire(ax, [(14.3, 13.5), (14.3, 14.5)], '#CC8800', lw=1.2)
    draw_label(ax, (13.0, 14.0), 'SMA\nbulkhead', fontsize=5, color='#888888')

    # ================================================================
    # USB STORAGE
    # ================================================================
    draw_box(ax, (12.5, 10.0), 2.8, 1.2,
             'Samsung FIT Plus', '256GB USB 3.1 (IP67)',
             color=BOX_COMPUTE, fontsize=8, sublabel_size=6)

    # Pi USB 3.0 → SSD
    draw_wire(ax, [(11.5, 11.0), (12.0, 11.0), (12.0, 10.6),
                    (12.5, 10.6)], WIRE_USB, lw=1.5)
    draw_label(ax, (12.0, 11.3), 'USB 3.0', fontsize=6, color=WIRE_USB)

    # ================================================================
    # GPIO Section: LEDs
    # ================================================================
    # Pi-EzConnect
    draw_box(ax, (16.0, 10.0), 2.5, 3.0,
             'Pi-EzConnect', 'GPIO Terminal\nBlock (Adafruit\n2711)',
             color=BOX_UI, fontsize=8, sublabel_size=6)

    # Pi GPIO → EzConnect
    draw_wire(ax, [(11.5, 11.5), (16.0, 11.5)], WIRE_GPIO, lw=1.2)
    draw_label(ax, (13.8, 11.7), '40-pin GPIO header', fontsize=5.5,
               color=WIRE_GPIO)

    # LED section
    led_y_base = 8.0
    led_colors_map = [('#00AA00', 'Green LED', 'GPIO 17\nSystem OK'),
                      ('#CCAA00', 'Yellow LED', 'GPIO 27\nWorking'),
                      ('#CC0000', 'Red LED', 'GPIO 22\nError')]

    for i, (lc, lname, ldesc) in enumerate(led_colors_map):
        y = led_y_base - i * 1.2
        # wire from EzConnect
        draw_wire(ax, [(18.5, 10.5 - i * 0.5), (19.0, y + 0.3)],
                  WIRE_GPIO, lw=1.0)
        # resistor symbol
        ax.plot([19.0, 19.3], [y + 0.3, y + 0.3], color='#555', lw=1.5)
        rect = FancyBboxPatch((19.3, y + 0.15), 0.4, 0.3,
                              boxstyle="square,pad=0",
                              facecolor='#E8E8E8', edgecolor='#555',
                              linewidth=1, zorder=3)
        ax.add_patch(rect)
        draw_label(ax, (19.5, y + 0.55), '330\u03A9', fontsize=5)

        # LED symbol (circle)
        circle = plt.Circle((20.2, y + 0.3), 0.18, facecolor=lc,
                             edgecolor='#333', linewidth=1, zorder=3)
        ax.add_patch(circle)
        ax.plot([19.7, 20.02], [y + 0.3, y + 0.3], color='#555', lw=1.5)

        draw_label(ax, (20.8, y + 0.3), ldesc, fontsize=5.5,
                   color='#444', ha='left')

    # LED label
    draw_label(ax, (20.2, led_y_base + 0.8), 'STATUS LEDs', fontsize=7,
               color='#555', ha='center')

    # ================================================================
    # Maintenance Button
    # ================================================================
    btn_y = 4.5
    draw_wire(ax, [(18.5, 10.0), (19.0, btn_y + 0.3)], WIRE_GPIO, lw=1.0)

    # Button symbol
    ax.plot([19.0, 19.5], [btn_y + 0.3, btn_y + 0.3], color='#555', lw=1.5)
    ax.plot([19.5, 19.5], [btn_y + 0.3, btn_y + 0.6], color='#555', lw=1.5)
    ax.plot([19.5, 20.0], [btn_y + 0.6, btn_y + 0.6], color='#555', lw=1.5)
    ax.plot([20.0, 20.0], [btn_y + 0.6, btn_y + 0.3], color='#555', lw=1.5)
    ax.plot([20.0, 20.5], [btn_y + 0.3, btn_y + 0.3], color='#555', lw=1.5)
    draw_label(ax, (19.75, btn_y + 0.95), 'IP67 Pushbutton', fontsize=6)
    draw_label(ax, (19.75, btn_y - 0.1), 'GPIO 23 (pull-up)\nLong press 3s\n= Maintenance',
               fontsize=5.5, color='#555')

    # Cable gland for button
    draw_label(ax, (19.75, btn_y - 0.7), 'M16 gland', fontsize=5,
               color='#888888')

    # ================================================================
    # Rain Gauge (external, optional)
    # ================================================================
    draw_box(ax, (16.0, 6.5), 2.5, 1.5,
             'Hydreon RG-15', 'Rain Gauge\nUART Serial 3.3V',
             color=BOX_SENSOR, fontsize=7, sublabel_size=6)

    # EzConnect → Rain Gauge
    draw_wire(ax, [(17.25, 10.0), (17.25, 8.0)], WIRE_GPIO, lw=1.0)
    draw_label(ax, (17.6, 9.0), 'GPIO 14/15\nUART TX/RX', fontsize=5.5,
               color=WIRE_GPIO, ha='left')
    # Power for rain gauge
    draw_wire(ax, [(16.5, 8.0), (16.5, 8.0)], WIRE_12V, lw=1.0)
    draw_label(ax, (16.0, 8.2), '12V from\nTB1', fontsize=5,
               color=WIRE_12V, ha='left')
    draw_label(ax, (17.25, 6.2), 'PG9 gland', fontsize=5, color='#888888')

    # ================================================================
    # LEGEND
    # ================================================================
    leg_x, leg_y = 0.5, 5.5
    ax.text(leg_x, leg_y, 'WIRE LEGEND', fontsize=8, fontweight='bold',
            color='#333')
    legends = [
        (WIRE_12V, '12V DC Power (18 AWG)'),
        (WIRE_5V,  '5V USB-C (to Pi)'),
        (WIRE_48V, '48V PoE (Cat6)'),
        (WIRE_ETH, 'Ethernet Data'),
        (WIRE_USB, 'USB Data'),
        (WIRE_GPIO, 'GPIO / Signal (22 AWG)'),
    ]
    for i, (c, t) in enumerate(legends):
        y = leg_y - 0.45 * (i + 1)
        ax.plot([leg_x, leg_x + 0.8], [y, y], color=c, lw=2)
        ax.text(leg_x + 1.0, y, t, fontsize=6.5, va='center', color='#444')

    # ================================================================
    # NOTES
    # ================================================================
    notes_x, notes_y = 0.5, 2.8
    ax.text(notes_x, notes_y, 'NOTES', fontsize=8, fontweight='bold',
            color='#333')
    notes = [
        '1. PoE injector on Witty Pi switched 12V rail — camera power-cycles with Pi.',
        '2. No heaters (Sukabumi tropical climate, solar power budget).',
        '3. Conformal coating MG 422C on all exposed PCBs.',
        '4. Dielectric grease on all outdoor electrical connections.',
        '5. Gore vent on enclosure for pressure equalization.',
        '6. Carrier: Telkomsel (Indonesia).  Peak draw: ~42W (3.5A @ 12V).',
        '7. Cycle: 2.5 min ON / 12.5 min SLEEP (96 cycles/day).',
    ]
    for i, n in enumerate(notes):
        ax.text(notes_x, notes_y - 0.35 * (i + 1), n,
                fontsize=6, color='#555')

    # ================================================================
    # VOLTAGE / PROTECTION TABLE
    # ================================================================
    tbl_x, tbl_y = 0.5, 7.5
    ax.text(tbl_x, tbl_y, 'VOLTAGE / PROTECTION', fontsize=8,
            fontweight='bold', color='#333')
    tbl_data = [
        ('Solar system', '12V nom', '—'),
        ('Witty Pi in', '12V (5-26V)', 'Internal OCP'),
        ('Pi 5 (USB-C)', '5V', 'From Witty Pi'),
        ('PoE injector', '12V→48V', '5A inline fuse'),
        ('Camera (PoE)', '48V', '802.3af/at'),
        ('LTE modem', '5V USB', 'Pi USB OCP'),
        ('GPIO signals', '3.3V', '330\u03A9 series R'),
    ]
    for i, (comp, volt, prot) in enumerate(tbl_data):
        y = tbl_y - 0.35 * (i + 1)
        ax.text(tbl_x, y, comp, fontsize=6, color='#444')
        ax.text(tbl_x + 1.8, y, volt, fontsize=6, color='#444')
        ax.text(tbl_x + 3.0, y, prot, fontsize=6, color='#444')

    # ── Save ───────────────────────────────────────────────────────
    out_dir = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(out_dir, 'circuit_diagram.pdf')
    fig.savefig(out_path, dpi=DPI, bbox_inches='tight',
                facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f'Saved: {out_path}')

    # Also save a PNG for quick preview
    fig2, ax2 = plt.subplots(1, 1, figsize=(FIG_W, FIG_H), dpi=100)
    fig2.patch.set_facecolor(BG_COLOR)
    ax2.set_facecolor(BG_COLOR)
    # Re-run all drawing on fig2... or just save PDF and note it
    plt.close(fig2)


if __name__ == '__main__':
    main()
