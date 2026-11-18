# Minimal MicroPython driver for the mouth's ST7789 2" IPS panel
# (SEENGREAT, 240x320 portrait, used sideways as 320x240). Write-only
# (no MISO). Only what main.py needs: set up the panel and push whole
# frames from a RAM framebuffer (organs/pico_common/framebuffer.py) —
# the drawing itself happens there, in framebuf's C code.

import time

_SWRESET = 0x01
_SLPOUT = 0x11
_NORON = 0x13
_INVOFF = 0x20
_INVON = 0x21
_DISPON = 0x29
_CASET = 0x2A
_RASET = 0x2B
_RAMWR = 0x2C
_MADCTL = 0x36
_COLMOD = 0x3A

_MADCTL_MY = 0x80   # mirror row order
_MADCTL_MX = 0x40   # mirror column order
_MADCTL_MV = 0x20   # swap rows and columns

# Turning the picture clockwise from portrait by this many degrees, done
# by the panel itself (MADCTL), so drawing doesn't change or slow down.
# 90 and 270 are the landscape ones.
_ROTATION_BITS = {
    0: 0,
    90: _MADCTL_MV | _MADCTL_MX,
    180: _MADCTL_MX | _MADCTL_MY,
    270: _MADCTL_MV | _MADCTL_MY,
}

_NATIVE_WIDTH = 240
_NATIVE_HEIGHT = 320


class ST7789:
    def __init__(self, spi, cs, dc, rst, rotation=90, invert=True):
        """rotation: 0/90/180/270 degrees clockwise from portrait; 90 and
        270 give 320x240. If the mouth is upside down, swap 90 for 270.
        invert: IPS panels like this one usually need colour inversion on;
        if the line shows black on white, pass invert=False."""
        if rotation not in _ROTATION_BITS:
            raise ValueError("rotation must be 0, 90, 180 or 270")
        self.spi, self.cs, self.dc, self.rst = spi, cs, dc, rst
        if rotation in (90, 270):
            self.WIDTH, self.HEIGHT = _NATIVE_HEIGHT, _NATIVE_WIDTH
        else:
            self.WIDTH, self.HEIGHT = _NATIVE_WIDTH, _NATIVE_HEIGHT
        self.cs.value(1)
        self._reset()
        self._cmd(_SWRESET)
        time.sleep_ms(150)
        self._cmd(_SLPOUT)
        time.sleep_ms(120)
        self._cmd(_COLMOD, b"\x55")   # 16 bits/pixel
        self._cmd(_MADCTL, bytes([_ROTATION_BITS[rotation]]))
        self._cmd(_INVON if invert else _INVOFF)
        self._cmd(_NORON)
        time.sleep_ms(10)
        self._cmd(_DISPON)
        time.sleep_ms(20)

    def _reset(self):
        self.rst.value(1)
        time.sleep_ms(10)
        self.rst.value(0)
        time.sleep_ms(10)
        self.rst.value(1)
        time.sleep_ms(120)

    def _cmd(self, cmd, data=None):
        self.cs.value(0)
        self.dc.value(0)
        self.spi.write(bytes([cmd]))
        if data is not None:
            self.dc.value(1)
            self.spi.write(data)
        self.cs.value(1)

    def blit(self, buf):
        """Send a whole frame (WIDTH*HEIGHT big-endian RGB565 pixels) in
        one SPI write."""
        x1, y1 = self.WIDTH - 1, self.HEIGHT - 1
        self._cmd(_CASET, bytes([0, 0, x1 >> 8, x1 & 0xFF]))
        self._cmd(_RASET, bytes([0, 0, y1 >> 8, y1 & 0xFF]))
        self._cmd(_RAMWR)
        self.cs.value(0)
        self.dc.value(1)
        self.spi.write(buf)
        self.cs.value(1)
