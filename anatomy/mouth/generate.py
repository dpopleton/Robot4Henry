"""Generates a placeholder mounting plate for the mouth from measurements.yaml.

Like anatomy/eyes/generate.py, this proves the pipeline rather than
being a finished design — the mechanism (servo jaw vs. LEDs vs.
static shape) isn't decided yet, so this just cuts the visible
opening and reserves a footprint-sized pocket for whatever mechanism
sits behind it. Revisit this once mechanism.type in measurements.yaml
is no longer a placeholder.

For a printable dimensioned drawing instead of a 3D solid, see
drawing.py — both read the same numbers via mouth_layout.compute().

Run from the repo root:
    python anatomy/mouth/generate.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import cadquery as cq
from _lib import load_measurements, export_all
from mouth_layout import compute

m = load_measurements(__file__)
L = compute(m)

plate = cq.Workplane("XY").box(L["plate_width"], L["plate_height"], L["plate_thickness"])

# Visible mouth opening, cut all the way through.
opening = cq.Workplane("XY").box(L["opening_width"], L["opening_height"], L["plate_thickness"] + 2)
plate = plate.cut(opening)

# Reserved pocket for the mechanism's body — a footprint placeholder,
# not a real fit, until mechanism.type in measurements.yaml is settled.
sx, sy = L["servo_pocket_center"]
servo_pocket = (
    cq.Workplane("XY")
    .box(L["servo_pocket_width"], L["servo_pocket_height"], L["servo_pocket_depth"])
    .translate((sx, sy, L["plate_thickness"] / 2 - L["servo_pocket_depth"] / 2))
)
plate = plate.cut(servo_pocket)

# Corner mounting holes, full thickness.
for x, y in L["corner_xy"]:
    hole = (
        cq.Workplane("XY")
        .circle(L["mounting_hole_diameter"] / 2)
        .extrude(L["plate_thickness"] + 2)
        .translate((x, y, -L["plate_thickness"] / 2 - 1))
    )
    plate = plate.cut(hole)

export_all(plate, __file__, "mouth_plate")
