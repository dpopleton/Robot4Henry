# Draws into a RAM framebuffer and pushes each finished frame to the
# panel in one SPI write — the fast path for main.py.
#
# Drawing straight to the GC9A01 (gc9a01.py's fill_circle etc.) does a
# window-set + write per scanline, from Python, while the panel shows
# every half-drawn step — slow, and it flickers. Here the shapes are
# filled by framebuf's C code into RAM, then show() sends the whole
# 240x240 frame at once: no flicker, and the cost per redraw is
# basically fixed at one 115KB SPI transfer (~23ms at 40MHz).
#
# Same driver contract as gc9a01.GC9A01 and simulate.py's SimDriver
# (fill/fill_circle/fill_polygon), plus show(), which eyes.Eye calls
# after every render.

from array import array

import framebuf


def _swap(color):
    # framebuf stores RGB565 little-endian; the panel reads big-endian.
    return ((color & 0xFF) << 8) | (color >> 8)


class BufferedPanel:
    def __init__(self, panel, buf=None):
        """buf: pass the same bytearray to both eyes' BufferedPanels to
        share one 115KB buffer between them — safe because eyes.Eye
        renders and shows one eye fully before starting the next."""
        self.panel = panel
        self.WIDTH, self.HEIGHT = panel.WIDTH, panel.HEIGHT
        self.buf = buf if buf is not None else bytearray(self.WIDTH * self.HEIGHT * 2)
        self.fb = framebuf.FrameBuffer(self.buf, self.WIDTH, self.HEIGHT, framebuf.RGB565)

    def fill(self, color):
        self.fb.fill(_swap(color))

    def fill_circle(self, cx, cy, r, color):
        r = int(r)
        self.fb.ellipse(int(cx), int(cy), r, r, _swap(color), True)

    def fill_polygon(self, points, color):
        coords = array("h")
        for x, y in points:
            coords.append(int(x))
            coords.append(int(y))
        self.fb.poly(0, 0, coords, _swap(color), True)

    def show(self):
        self.panel.blit(self.buf)
