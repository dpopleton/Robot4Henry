# Hardware bring-up test for two GC9A01 eyes on one Pico.
# No nervous_system/serial integration yet — this just proves the
# wiring is right by moving both eyes together, with occasional
# independent blinks so a miswired CS pin shows up immediately.
#
# See organs/eyes/README.md for the wiring table.

import random
import time
from machine import Pin, SPI

from gc9a01 import GC9A01
from eyes import Eye

spi = SPI(0, baudrate=40_000_000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(19))
dc = Pin(20, Pin.OUT)
rst = Pin(21, Pin.OUT)

left_driver = GC9A01(spi, cs=Pin(17, Pin.OUT), dc=dc, rst=rst)
right_driver = GC9A01(spi, cs=Pin(16, Pin.OUT), dc=dc, rst=rst, mirror_x=True)

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
