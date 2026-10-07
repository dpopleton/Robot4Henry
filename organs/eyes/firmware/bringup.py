# Hardware bring-up test for two GC9A01 eyes on one Pico — not main.py
# (that listens for commands from the host; see main.py). Run it on its
# own with `mpremote run organs/eyes/firmware/bringup.py`: it proves the
# wiring is right by moving both eyes together, with occasional
# independent blinks so a miswired CS pin shows up immediately.
#
# See organs/eyes/README.md for the wiring table.

import random
import time

from eyes import Eye
from panels import init_panels

left_driver, right_driver, backlight = init_panels()

left_eye = Eye(left_driver)
right_eye = Eye(right_driver)

LOOK_DIRECTIONS = [
    (0, 0), (-1, 0), (1, 0), (0, -1), (0, 1),
    (-0.6, -0.6), (0.6, -0.6), (-0.6, 0.6), (0.6, 0.6),
]

cycle = 0
while True:
    dx, dy = random.choice(LOOK_DIRECTIONS)
    left_eye.look(dx, dy)
    right_eye.look(dx, dy)
    time.sleep(1.5)

    cycle += 1
    if cycle % 5 == 0:
        # Independent movement, on purpose: if the CS wiring is
        # crossed, this is where you'll see the wrong eye blink.
        target = random.choice(["left", "right", "both"])
        if target in ("left", "both"):
            left_eye.blink()
        if target in ("right", "both"):
            right_eye.blink()
