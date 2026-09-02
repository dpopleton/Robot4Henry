"""Pure-geometry values derived from measurements.yaml — no cadquery or
matplotlib here, just arithmetic. Both generate.py (3D solid) and
drawing.py (2D dimensioned print sheet) call compute() so they can
never disagree about a number.
"""


def compute(m: dict) -> dict:
    mechanism = m["mechanism"]
    mount = m["mount"]

    plate_width = mount["plate_width_mm"]
    plate_height = mount["plate_height_mm"]
    plate_thickness = mount["plate_thickness_mm"]
    opening_width = mount["opening_width_mm"]
    opening_height = mount["opening_height_mm"]
    inset = mount["hole_inset_mm"]
    mounting_hole_diameter = mount["mounting_hole_diameter_mm"]

    corner_xy = [
        (sx * (plate_width / 2 - inset), sy * (plate_height / 2 - inset))
        for sx in (-1, 1)
        for sy in (-1, 1)
    ]

    servo_w = mechanism["servo_body_width_mm"]
    servo_h = mechanism["servo_body_height_mm"]
    # Reserved pocket sits above the opening, against the top edge —
    # see generate.py; kept here so drawing.py positions it identically.
    servo_pocket_center = (0.0, plate_height / 2 - servo_h / 2 - 2)

    return dict(
        plate_width=plate_width,
        plate_height=plate_height,
        plate_thickness=plate_thickness,
        opening_width=opening_width,
        opening_height=opening_height,
        corner_xy=corner_xy,
        mounting_hole_diameter=mounting_hole_diameter,
        servo_pocket_width=servo_w,
        servo_pocket_height=servo_h,
        servo_pocket_depth=plate_thickness / 2,
        servo_pocket_center=servo_pocket_center,
    )
