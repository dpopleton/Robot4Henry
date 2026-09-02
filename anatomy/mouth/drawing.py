"""Dimensioned, print-ready orthographic drawing of the mouth plate.

Two views: front (opening size/position, corner holes, reserved
mechanism footprint) and side (plate thickness, pocket depth). Reads
the same numbers as generate.py via mouth_layout.compute().

Run from the repo root:
    python anatomy/mouth/drawing.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from _drawing import autoscale, dim_h, dim_v, hidden_line, new_sheet, outline_circle, outline_rect, save_pdf
from _lib import load_measurements
from mouth_layout import compute

m = load_measurements(__file__)
L = compute(m)

fig, (front, side) = new_sheet("Mouth plate", ["Front", "Side (cross-section)"])

# --- Front view ---
w, h = L["plate_width"], L["plate_height"]
ow, oh = L["opening_width"], L["opening_height"]
sw, sh = L["servo_pocket_width"], L["servo_pocket_height"]
sx, sy = L["servo_pocket_center"]

outline_rect(front, 0, 0, w, h)
outline_rect(front, 0, 0, ow, oh)
outline_rect(front, sx, sy, sw, sh, style="--", color="#555555")
leader_x0, leader_y0 = sx + sw / 2, sy
leader_x1, leader_y1 = w / 2 + 16, sy
front.plot([leader_x0, leader_x1], [leader_y0, leader_y1], color="#555555", linewidth=0.6)
front.text(leader_x1 + 2, leader_y1, "mechanism footprint\n(placeholder)", fontsize=7.5, color="#555555", va="center")
for x, y in L["corner_xy"]:
    outline_circle(front, x, y, L["mounting_hole_diameter"] / 2)

dim_h(front, -w / 2, w / 2, -h / 2, f"{w:.1f}", offset=16)
dim_v(front, -h / 2, h / 2, -w / 2, f"{h:.1f}", offset=16)
dim_h(front, -ow / 2, ow / 2, -oh / 2, f"opening {ow:.1f}", offset=-12)
dim_v(front, -oh / 2, oh / 2, ow / 2, f"{oh:.1f}", offset=-12)
autoscale(front, [(-w / 2 - 25, -h / 2 - 25), (w / 2 + 60, h / 2 + 25)])

# --- Side view (cross-section) ---
t = L["plate_thickness"]
pd = L["servo_pocket_depth"]
outline_rect(side, 0, 0, w, t)
hidden_line(side, sx - sw / 2, t / 2 - pd, sx + sw / 2, t / 2 - pd)
dim_v(side, -t / 2, t / 2, -w / 2, f"{t:.1f}", offset=16)
dim_v(side, t / 2 - pd, t / 2, w / 2, f"pocket depth {pd:.1f}", offset=16)
autoscale(side, [(-w / 2 - 25, -t / 2 - 20), (w / 2 + 25, t / 2 + 20)])

save_pdf(fig, __file__, "mouth_plate_drawing")
