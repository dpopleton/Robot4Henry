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
from backlight import Backlight

spi = SPI(0, baudrate=40_000_000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(19))
dc = Pin(20, Pin.OUT)
rst = Pin(21, Pin.OUT)
backlight = Backlight(22)

# RST is one physical line shared by both panels — reset it once here rather
# than letting each GC9A01 reset on construction, which would re-reset (and
# un-initialize) whichever panel was already set up.
rst.value(1)
time.sleep_ms(10)
rst.value(0)
time.sleep_ms(10)
rst.value(1)
time.sleep_ms(120)

left_driver = GC9A01(spi, cs=Pin(17, Pin.OUT), dc=dc, rst=rst, reset=False)
right_driver = GC9A01(spi, cs=Pin(16, Pin.OUT), dc=dc, rst=rst, reset=False)

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
