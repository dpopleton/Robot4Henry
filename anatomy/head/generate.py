"""Generates a placeholder head shell from measurements.yaml, with front
windows cut for the eyes and mouth plates.

This is an assembly script: head_layout.compute() loads
anatomy/eyes/measurements.yaml and anatomy/mouth/measurements.yaml
directly, so the window sizes always match those parts' actual plate
footprints — change a number in eyes/measurements.yaml and re-run this
to get a correctly resized window, no copy-pasting dimensions between
files.

The shell itself is a plain hollow box for now — swap the box() calls
for whatever shape (dome, organic shell, etc.) once shell.shape_notes
in measurements.yaml stops being a TODO.

For a printable dimensioned drawing instead of a 3D solid, see
drawing.py.

Run from the repo root:
    python anatomy/head/generate.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import cadquery as cq
from _lib import load_measurements, load_measurements_for, export_all
from head_layout import compute

m = load_measurements(__file__)
eyes_m = load_measurements_for("eyes")
mouth_m = load_measurements_for("mouth")
L = compute(m, eyes_m, mouth_m)

width, depth, height, wall = L["width"], L["depth"], L["height"], L["wall"]

# Box centered in X/Y, base sitting at Z=0 (so layout heights read as
# "above the base", matching measurements.yaml).
outer = cq.Workplane("XY").box(width, depth, height).translate((0, 0, height / 2))
inner = (
    cq.Workplane("XY")
    .box(width - 2 * wall, depth - 2 * wall, height - 2 * wall)
    .translate((0, 0, height / 2))
)
head_shell = outer.cut(inner)


def front_window(win_width: float, win_height: float, center_z: float) -> cq.Workplane:
    """A cutter box spanning the front wall (Y = -depth/2)."""
    return (
        cq.Workplane("XY")
        .box(win_width, wall + 4, win_height)
        .translate((0, -depth / 2, center_z))
    )


head_shell = head_shell.cut(
    front_window(L["eyes_window"]["width"], L["eyes_window"]["height"], L["eyes_window"]["center_z"])
)
head_shell = head_shell.cut(
    front_window(L["mouth_window"]["width"], L["mouth_window"]["height"], L["mouth_window"]["center_z"])
)

export_all(head_shell, __file__, "head_shell")
