"""Dimensioned, print-ready orthographic drawing of the head shell.

Three views: front (overall width/height, window positions/sizes),
top (overall width/depth), side (overall depth/height, wall thickness,
where each window sits front-to-back). Reads the same numbers as
generate.py via head_layout.compute() — which itself reads
eyes/measurements.yaml and mouth/measurements.yaml, so the window
sizes shown here always match those parts.

Run from the repo root:
    python anatomy/head/drawing.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from _drawing import autoscale, dim_h, dim_v, new_sheet, note, outline_rect, save_pdf
from _lib import load_measurements, load_measurements_for
from head_layout import compute

m = load_measurements(__file__)
eyes_m = load_measurements_for("eyes")
mouth_m = load_measurements_for("mouth")
L = compute(m, eyes_m, mouth_m)

width, depth, height, wall = L["width"], L["depth"], L["height"], L["wall"]
eyes_w = L["eyes_window"]
mouth_w = L["mouth_window"]

fig, (front, top, side) = new_sheet("Head shell", ["Front", "Top", "Side"])

# --- Front view (X = width, Z = height, base at Z=0) ---
outline_rect(front, 0, height / 2, width, height)
outline_rect(front, 0, eyes_w["center_z"], eyes_w["width"], eyes_w["height"], style="--", color="#555555")
note(front, 0, eyes_w["center_z"], f"eyes window\n{eyes_w['width']:.1f} x {eyes_w['height']:.1f}")
outline_rect(front, 0, mouth_w["center_z"], mouth_w["width"], mouth_w["height"], style="--", color="#555555")
note(front, 0, mouth_w["center_z"], f"mouth window\n{mouth_w['width']:.1f} x {mouth_w['height']:.1f}")

dim_h(front, -width / 2, width / 2, 0, f"{width:.1f}", offset=20)
dim_v(front, 0, height, -width / 2, f"{height:.1f}", offset=20)
dim_v(front, 0, eyes_w["center_z"], width / 2, f"eyes center ht {eyes_w['center_z']:.1f}", offset=-20)
dim_v(front, 0, mouth_w["center_z"], width / 2, f"mouth center ht {mouth_w['center_z']:.1f}", offset=-40)
autoscale(front, [(-width / 2 - 40, -30), (width / 2 + 60, height + 20)])

# --- Top view (X = width, Y = depth); front edge is -depth/2 ---
outline_rect(top, 0, 0, width, depth)
note(top, 0, -depth / 2 - 10, "front edge")
dim_h(top, -width / 2, width / 2, depth / 2, f"{width:.1f}", offset=-20)
dim_v(top, -depth / 2, depth / 2, width / 2, f"{depth:.1f}", offset=-20)
autoscale(top, [(-width / 2 - 25, -depth / 2 - 25), (width / 2 + 25, depth / 2 + 25)])

# --- Side view (Y = depth, Z = height); front edge is -depth/2 ---
outline_rect(side, 0, height / 2, depth, height)
notch_x = -depth / 2 + (wall + 4) / 2
outline_rect(side, notch_x, eyes_w["center_z"], wall + 4, eyes_w["height"], style="--", color="#555555")
outline_rect(side, notch_x, mouth_w["center_z"], wall + 4, mouth_w["height"], style="--", color="#555555")

dim_h(side, -depth / 2, depth / 2, 0, f"{depth:.1f}", offset=20)
dim_v(side, 0, height, -depth / 2, f"{height:.1f}", offset=20)
dim_h(side, -depth / 2, -depth / 2 + wall, height, f"wall {wall:.1f}", offset=-14)
autoscale(side, [(-depth / 2 - 40, -30), (depth / 2 + 25, height + 20)])

save_pdf(fig, __file__, "head_shell_drawing")
