# Screen size, colours and mouth proportions — used by the drawing code
# (mouth.py) and by whatever shows it: the real ST7789 panel, the virtual
# panel, or the tests. Change the size here once the display is confirmed.

# The SEENGREAT 2" module is 240x320 portrait; the mouth uses it sideways.
WIDTH = 320
HEIGHT = 240

BACKGROUND_COLOR = 0x0000   # black, RGB565
LINE_COLOR = 0xFFFF         # white

CENTER_Y = HEIGHT // 2
LEFT = 30                   # mouth corners
RIGHT = WIDTH - 30
LINE_THICKNESS = 8
MAX_AMPLITUDE = 90          # tallest spike, up or down from the line, at full level
SPIKES = 25                 # zig-zag points between the corners
