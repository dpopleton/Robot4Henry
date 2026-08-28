# Minimal MicroPython driver for the GC9A01 1.28" round SPI TFT.
# Write-only (no MISO needed). Two displays can share one SPI bus,
# SCK/MOSI/DC/RST — each just needs its own CS pin.

import math
import time
from machine import Pin

_CASET = 0x2A
_RASET = 0x2B
_RAMWR = 0x2C
_MADCTL = 0x36
_COLMOD = 0x3A

_MADCTL_MX = 0x40   # mirror column order
_MADCTL_BGR = 0x08  # panel is wired BGR, not RGB

# Reference init sequence for this panel: (command, data bytes or None, delay_ms after).
_INIT_SEQUENCE = (
    (0xEF, None, 0),
    (0xEB, b"\x14", 0),
    (0xFE, None, 0),
    (0xEF, None, 0),
    (0xEB, b"\x14", 0),
    (0x84, b"\x40", 0),
    (0x85, b"\xFF", 0),
    (0x86, b"\xFF", 0),
    (0x87, b"\xFF", 0),
    (0x88, b"\x0A", 0),
    (0x89, b"\x21", 0),
    (0x8A, b"\x00", 0),
    (0x8B, b"\x80", 0),
    (0x8C, b"\x01", 0),
    (0x8D, b"\x01", 0),
    (0x8E, b"\xFF", 0),
    (0x8F, b"\xFF", 0),
    (0xB6, b"\x00\x20", 0),
    (_COLMOD, b"\x05", 0),  # 16 bits/pixel
    (0x90, b"\x08\x08\x08\x08", 0),
    (0xBD, b"\x06", 0),
    (0xBC, b"\x00", 0),
    (0xFF, b"\x60\x01\x04", 0),
    (0xC3, b"\x13", 0),
    (0xC4, b"\x13", 0),
    (0xC9, b"\x22", 0),
    (0xBE, b"\x11", 0),
    (0xE1, b"\x10\x0E", 0),
    (0xDF, b"\x21\x0C\x02", 0),
    (0xF0, b"\x45\x09\x08\x08\x26\x2A", 0),
    (0xF1, b"\x43\x70\x72\x36\x37\x6F", 0),
    (0xF2, b"\x45\x09\x08\x08\x26\x2A", 0),
    (0xF3, b"\x43\x70\x72\x36\x37\x6F", 0),
    (0xED, b"\x1B\x0B", 0),
    (0xAE, b"\x77", 0),
    (0xCD, b"\x63", 0),
    (0x70, b"\x07\x07\x04\x0E\x0F\x09\x07\x08\x03", 0),
    (0xE8, b"\x34", 0),
    (0x62, b"\x18\x0D\x71\xED\x70\x70\x18\x0F\x71\xEF\x70\x70", 0),
    (0x63, b"\x18\x11\x71\xF1\x70\x70\x18\x13\x71\xF3\x70\x70", 0),
    (0x64, b"\x28\x29\xF1\x01\xF1\x00\x07", 0),
    (0x66, b"\x3C\x00\xCD\x67\x45\x45\x10\x00\x00\x00", 0),
    (0x67, b"\x00\x3C\x00\x00\x00\x01\x54\x10\x32\x98", 0),
    (0x74, b"\x10\x85\x80\x00\x00\x4E\x00", 0),
    (0x98, b"\x3E\x07", 0),
    (0x35, None, 0),
    (0x21, None, 0),
    (0x11, None, 120),  # sleep out
    (0x29, None, 20),   # display on
)


class GC9A01:
    WIDTH = 240
    HEIGHT = 240

    def __init__(self, spi, cs: Pin, dc: Pin, rst: Pin, mirror_x: bool = False):
        self.spi = spi
        self.cs = cs
        self.dc = dc
        self.rst = rst
        self.mirror_x = mirror_x

        self.cs.value(1)
        self._reset()
        self._init_display()

    def _reset(self):
        self.rst.value(1)
        time.sleep_ms(10)
        self.rst.value(0)
        time.sleep_ms(10)
        self.rst.value(1)
        time.sleep_ms(120)

    def _cmd(self, cmd: int, data: bytes = None):
        self.cs.value(0)
        self.dc.value(0)
        self.spi.write(bytes([cmd]))
        if data is not None:
            self.dc.value(1)
            self.spi.write(data)
        self.cs.value(1)

    def _init_display(self):
        for cmd, data, delay in _INIT_SEQUENCE:
            self._cmd(cmd, data)
            if delay:
                time.sleep_ms(delay)

        madctl = _MADCTL_BGR
        if self.mirror_x:
            madctl |= _MADCTL_MX
        self._cmd(_MADCTL, bytes([madctl]))

    def set_window(self, x0: int, y0: int, x1: int, y1: int):
        self._cmd(_CASET, bytes([x0 >> 8, x0 & 0xFF, x1 >> 8, x1 & 0xFF]))
        self._cmd(_RASET, bytes([y0 >> 8, y0 & 0xFF, y1 >> 8, y1 & 0xFF]))
        self._cmd(_RAMWR)

    def _write_pixels(self, color: int, count: int):
        hi, lo = color >> 8, color & 0xFF
        chunk_len = min(count, 512)
        buf = bytearray(chunk_len * 2)
        for i in range(chunk_len):
            buf[i * 2] = hi
            buf[i * 2 + 1] = lo

        self.cs.value(0)
        self.dc.value(1)
        remaining = count
        while remaining > 0:
            n = min(remaining, chunk_len)
            self.spi.write(buf if n == chunk_len else buf[: n * 2])
            remaining -= n
        self.cs.value(1)

    def fill(self, color: int):
        self.set_window(0, 0, self.WIDTH - 1, self.HEIGHT - 1)
        self._write_pixels(color, self.WIDTH * self.HEIGHT)

    def fill_circle(self, cx: int, cy: int, r: int, color: int):
        for y in range(max(0, cy - r), min(self.HEIGHT, cy + r + 1)):
            dy = y - cy
            span = r * r - dy * dy
            if span < 0:
                continue
            half_w = int(math.sqrt(span))
            x0 = max(0, cx - half_w)
            x1 = min(self.WIDTH - 1, cx + half_w)
            if x1 < x0:
                continue
            self.set_window(x0, y, x1, y)
            self._write_pixels(color, x1 - x0 + 1)
