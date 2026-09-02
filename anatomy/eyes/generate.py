"""Generates a mounting plate for the two eye displays from measurements.yaml.

This is intentionally a simple flat plate with two socket pockets — it
exists to prove the measurements.yaml -> STEP/STL pipeline end to end,
not as a finished design. Once anatomy/head/ settles on the real head
shape, this is the place to swap the flat plate for a curved one, add
snap-fit tabs, etc. Change numbers in measurements.yaml, not here —
this script should only need edits when the *shape* changes.

For a printable dimensioned drawing instead of a 3D solid, see
drawing.py — both read the same numbers via eyes_layout.compute().

Run from the repo root:
    python anatomy/eyes/generate.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import cadquery as cq
from _lib import load_measurements, export_all
from eyes_layout import compute

m = load_measurements(__file__)
L = compute(m)

plate_width = L["plate_width"]
plate_height = L["plate_height"]
plate_thickness = L["plate_thickness"]

# All cuts are built as solids spanning (at least) the plate's full
# height/depth and subtracted in one boolean pass at the end — chaining
# face-selection between successive .cut() calls is fragile in
# cadquery once a cut has reshaped the solid's faces.
cutters = []

for cx, cy in L["socket_centers"]:
    # Socket pocket: a blind hole from the top face down socket_depth.
    cutters.append(
        cq.Workplane("XY")
        .workplane(offset=plate_thickness / 2 - L["socket_depth"])
        .center(cx, cy)
        .circle(L["socket_diameter"] / 2)
        .extrude(L["socket_depth"] + 1)  # +1 so it cleanly breaks through the top face
    )

    # Wire channel: full-thickness slot from the socket out the bottom edge.
    cutters.append(
        cq.Workplane("XY")
        .workplane(offset=-plate_thickness / 2)
        .center(cx, -plate_height / 2)
        .rect(L["channel_width"], L["rim"] * 2)
        .extrude(plate_thickness)
    )

# Corner mounting holes, full thickness.
for x, y in L["corner_xy"]:
    cutters.append(
        cq.Workplane("XY")
        .workplane(offset=-plate_thickness / 2)
        .center(x, y)
        .circle(L["mounting_hole_diameter"] / 2)
        .extrude(plate_thickness + 2)
    )

plate = cq.Workplane("XY").box(plate_width, plate_height, plate_thickness)
for cutter in cutters:
    plate = plate.cut(cutter)

export_all(plate, __file__, "eye_mount_plate")
