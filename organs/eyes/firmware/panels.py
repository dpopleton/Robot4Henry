# Pico pin setup for the two GC9A01 panels, shared by main.py and
# bringup.py so the wiring lives in one place (README wiring table).

import time
from machine import Pin, SPI

from gc9a01 import GC9A01
from backlight import Backlight


def init_panels(baudrate=40_000_000):
    """Returns (left_panel, right_panel, backlight). If the picture is
    garbled/noisy, try baudrate=20_000_000 or 10_000_000."""
    spi = SPI(0, baudrate=baudrate, polarity=0, phase=0, sck=Pin(18), mosi=Pin(19))
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

    left = GC9A01(spi, cs=Pin(17, Pin.OUT), dc=dc, rst=rst, reset=False)
    right = GC9A01(spi, cs=Pin(16, Pin.OUT), dc=dc, rst=rst, reset=False)
    return left, right, backlight
