# Mouth firmware entry point: listens on USB serial for S/L commands from
# the host (organs/mouth/driver.py, wire format in mouth_protocol.py) and
# draws a fresh frame every TICK_MS while talking. Same shape as the
# eyes' main.py: poll stdin without blocking, merge everything waiting
# into one Update (newest wins), draw into RAM, push in one SPI write.

import sys
import time

from framebuffer import BufferedPanel      # organs/pico_common/
from line_reader import LineReader         # organs/pico_common/
from mouth import Mouth, TICK_MS
from mouth_geometry import WIDTH, HEIGHT
from mouth_panel import init_panel
from mouth_protocol import Update, MAX_LINE

panel, backlight = init_panel()
if (panel.WIDTH, panel.HEIGHT) != (WIDTH, HEIGHT):
    raise RuntimeError("panel is %dx%d, mouth_geometry expects %dx%d" % (panel.WIDTH, panel.HEIGHT, WIDTH, HEIGHT))

mouth = Mouth(BufferedPanel(panel))        # draws the flat line straight away
reader = LineReader(sys.stdin, MAX_LINE)

next_tick = time.ticks_add(time.ticks_ms(), TICK_MS)
while True:
    remaining = time.ticks_diff(next_tick, time.ticks_ms())
    if remaining > 0:
        reader.wait(remaining)

    update = Update()
    reader.drain(update.merge_line)
    if not update.is_empty():
        mouth.update(talking=update.talking, level=update.level)

    if time.ticks_diff(time.ticks_ms(), next_tick) >= 0:
        mouth.tick()
        next_tick = time.ticks_add(time.ticks_ms(), TICK_MS)
