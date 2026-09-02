"""Pure-geometry values derived from measurements.yaml — no cadquery or
matplotlib here, just arithmetic. Both generate.py (3D solid) and
drawing.py (2D dimensioned print sheet) call compute() so they can
never disagree about a number.
"""


def compute(m: dict) -> dict:
    display = m["display"]
    mount = m["mount"]

    socket_diameter = display["outer_diameter_mm"] + 2 * mount["socket_clearance_mm"]
    eye_spacing = mount["eye_spacing_mm"]
    rim = mount["rim_width_mm"]
    plate_thickness = mount["plate_thickness_mm"]
    socket_depth = min(mount["socket_depth_mm"], plate_thickness)
    channel_width = mount["wire_channel_width_mm"]
    inset = mount["hole_inset_mm"]
    mounting_hole_diameter = mount["mounting_hole_diameter_mm"]

    plate_width = eye_spacing + socket_diameter + 2 * rim
    plate_height = socket_diameter + 2 * rim

    socket_centers = [(-eye_spacing / 2, 0.0), (eye_spacing / 2, 0.0)]
    corner_xy = [
        (sx * (plate_width / 2 - inset), sy * (plate_height / 2 - inset))
        for sx in (-1, 1)
        for sy in (-1, 1)
    ]

    return dict(
        plate_width=plate_width,
        plate_height=plate_height,
        plate_thickness=plate_thickness,
        socket_diameter=socket_diameter,
        socket_depth=socket_depth,
        socket_centers=socket_centers,
        eye_spacing=eye_spacing,
        rim=rim,
        channel_width=channel_width,
        corner_xy=corner_xy,
        mounting_hole_diameter=mounting_hole_diameter,
    )
