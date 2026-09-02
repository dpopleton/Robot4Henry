"""Dimensioned, print-ready orthographic drawing of the eyes mount plate.

Two views: front (looking at the plate face-on — socket positions,
spacing, corner holes) and side (a cross-section — plate thickness,
socket depth). Reads the same numbers as generate.py via
eyes_layout.compute(), so the drawing never drifts from the 3D model.

Run from the repo root:
    python anatomy/eyes/drawing.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from _drawing import autoscale, dim_diameter, dim_h, dim_v, hidden_line, new_sheet, outline_circle, outline_rect, save_pdf
from _lib import load_measurements
from eyes_layout import compute

m = load_measurements(__file__)
L = compute(m)

fig, (front, side) = new_sheet("Eyes mount plate", ["Front", "Side (cross-section)"])

# --- Front view ---
w, h = L["plate_width"], L["plate_height"]
outline_rect(front, 0, 0, w, h)
for cx, cy in L["socket_centers"]:
    outline_circle(front, cx, cy, L["socket_diameter"] / 2)
for x, y in L["corner_xy"]:
    outline_circle(front, x, y, L["mounting_hole_diameter"] / 2)

dim_h(front, -w / 2, w / 2, -h / 2, f"{w:.1f}", offset=16)
dim_v(front, -h / 2, h / 2, -w / 2, f"{h:.1f}", offset=16)
dim_h(
    front, L["socket_centers"][0][0], L["socket_centers"][1][0], 0,
    f"eye spacing {L['eye_spacing']:.1f}", offset=-12,
)
dim_diameter(front, *L["socket_centers"][1], L["socket_diameter"] / 2, f"socket ⌀{L['socket_diameter']:.1f}")
dim_diameter(
    front, *L["corner_xy"][-1], L["mounting_hole_diameter"] / 2,
    f"⌀{L['mounting_hole_diameter']:.1f} (x4)", angle_deg=45, leader=18,
)
autoscale(front, [(-w / 2 - 25, -h / 2 - 25), (w / 2 + 25, h / 2 + 25)])

# --- Side view (cross-section through one socket) ---
t = L["plate_thickness"]
sd = L["socket_depth"]
outline_rect(side, 0, 0, w, t)
hidden_line(side, -w / 2, t / 2 - sd, w / 2, t / 2 - sd)
dim_v(side, -t / 2, t / 2, -w / 2, f"{t:.1f}", offset=16)
dim_v(side, t / 2 - sd, t / 2, w / 2, f"socket depth {sd:.1f}", offset=16)
autoscale(side, [(-w / 2 - 25, -t / 2 - 20), (w / 2 + 25, t / 2 + 20)])

save_pdf(fig, __file__, "eye_mount_plate_drawing")
