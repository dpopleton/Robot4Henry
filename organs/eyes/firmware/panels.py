# Pico pin setup for the two GC9A01 panels, shared by main.py and
# bringup.py so the wiring lives in one place (wiring table in
# anatomy/eyes/build.md).
#
# Each eye has its own wires: its own SPI bus, DC, RST and CS, so nothing
# is spliced except VCC (D-026). They still move together because the
# firmware draws them one after the other each frame, not because of
# shared wires.

from machine import Pin, SPI

from gc9a01 import GC9A01
from backlight import Backlight


def init_panels(baudrate=40_000_000):
    """Returns (left_panel, right_panel, backlight). If the picture is
    garbled/noisy, try baudrate=20_000_000 or 10_000_000."""
    left_spi = SPI(0, baudrate=baudrate, polarity=0, phase=0, sck=Pin(18), mosi=Pin(19))
    right_spi = SPI(1, baudrate=baudrate, polarity=0, phase=0, sck=Pin(10), mosi=Pin(11))
    backlight = Backlight(16)  # BLK not wired yet (R-206); GP22 is now left CS

    # The panels are mounted turned a quarter-turn opposite ways, so each
    # picture is turned back to upright: left 90° anticlockwise (270°
    # clockwise), right 90° clockwise.
    # Separate RST lines, so each panel can reset itself on construction.
    left = GC9A01(left_spi, cs=Pin(22, Pin.OUT), dc=Pin(20, Pin.OUT), rst=Pin(21, Pin.OUT), rotation=270)
    right = GC9A01(right_spi, cs=Pin(14, Pin.OUT), dc=Pin(12, Pin.OUT), rst=Pin(13, Pin.OUT), rotation=90)
    return left, right, backlight
