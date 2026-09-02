"""Pure-geometry values for the head shell — no cadquery or matplotlib
here, just arithmetic. Unlike eyes_layout/mouth_layout, this one also
takes the eyes and mouth measurements dicts, since the shell's window
cutouts are sized to those parts' actual plate footprints (that's what
makes this an *assembly* layout rather than a per-part one).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "eyes"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "mouth"))

from eyes_layout import compute as compute_eyes
from mouth_layout import compute as compute_mouth


def compute(m: dict, eyes_m: dict, mouth_m: dict) -> dict:
    shell = m["shell"]
    layout = m["layout"]

    eyes = compute_eyes(eyes_m)
    mouth = compute_mouth(mouth_m)

    width = shell["width_mm"]
    depth = shell["depth_mm"]
    height = shell["height_mm"]
    wall = shell["wall_thickness_mm"]

    eyes_window = dict(
        width=eyes["plate_width"] + 2 * layout["eyes_plate_margin_mm"],
        height=eyes["plate_height"] + 2 * layout["eyes_plate_margin_mm"],
        center_z=layout["eyes_center_height_mm"],
    )
    mouth_window = dict(
        width=mouth["plate_width"] + 2 * layout["mouth_plate_margin_mm"],
        height=mouth["plate_height"] + 2 * layout["mouth_plate_margin_mm"],
        center_z=layout["mouth_center_height_mm"],
    )

    return dict(
        width=width,
        depth=depth,
        height=height,
        wall=wall,
        eyes_window=eyes_window,
        mouth_window=mouth_window,
    )
