# Eyes firmware entry point: listens on USB serial for direction and
# expression commands from the host (organs/eyes/driver.py) and keeps
# the eyes idling naturally (glances, blinks, animation) in between.
#
# Wire format: see eye_protocol.py. Responsiveness comes from three things:
#   - polling stdin without blocking, so a command is picked up within
#     milliseconds, even between idle ticks;
#   - draining *everything* waiting before drawing and merging it into one
#     Update — if the host sends direction faster than the panels can
#     redraw, stale positions are skipped rather than queued up;
#   - drawing into a RAM framebuffer and pushing each eye in one SPI write
#     (framebuffer.py), instead of hundreds of small per-scanline writes.
#
# For the old standalone wiring test, see bringup.py.

import select
import sys
import time

from eye_protocol import Update, MAX_LINE
from eyes import Eye, Face
from framebuffer import BufferedPanel
from panels import init_panels

TICK_MS = 150           # idle animation step — see eyes.Face
MAX_DRAIN_BYTES = 512   # read at most this much per loop before drawing, so a flood can't starve redraws


class LineReader:
    def __init__(self, stream):
        self.stream = stream
        self.poller = select.poll()
        self.poller.register(stream, select.POLLIN)
        self.chars = []
        self.overflow = False

    def wait(self, timeout_ms):
        """Sleep until input arrives or timeout_ms passes."""
        self.poller.poll(timeout_ms)

    def drain_into(self, update):
        """Merge every complete line already waiting into update."""
        for _ in range(MAX_DRAIN_BYTES):
            if not self.poller.poll(0):
                return
            ch = self.stream.read(1)
            if ch == "\n":
                if not self.overflow:
                    update.merge_line("".join(self.chars))
                self.chars = []
                self.overflow = False
            elif ch == "\r":
                pass
            elif len(self.chars) < MAX_LINE:
                self.chars.append(ch)
            else:
                self.overflow = True  # garbage — drop until the next newline


left_panel, right_panel, backlight = init_panels()

# One 115KB buffer shared by both eyes (each renders + shows in turn).
frame = bytearray(left_panel.WIDTH * left_panel.HEIGHT * 2)
# mirror=True on the right eye points asymmetric shapes (brows) inward on
# both — it never touches look direction (see expressions.py).
face = Face(
    Eye(BufferedPanel(left_panel, frame), mirror=False),
    Eye(BufferedPanel(right_panel, frame), mirror=True),
)
reader = LineReader(sys.stdin)

next_tick = time.ticks_add(time.ticks_ms(), TICK_MS)
while True:
    remaining = time.ticks_diff(next_tick, time.ticks_ms())
    if remaining > 0:
        reader.wait(remaining)

    update = Update()
    reader.drain_into(update)
    if not update.is_empty():
        face.update(update.expression, update.intensity, update.direction)
        if update.blink:
            face.blink()
            next_tick = time.ticks_add(time.ticks_ms(), TICK_MS)  # hold it shut a full tick

    if time.ticks_diff(time.ticks_ms(), next_tick) >= 0:
        face.tick()
        next_tick = time.ticks_add(time.ticks_ms(), TICK_MS)
