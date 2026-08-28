# A very basic "eye": a white sclera with a black pupil that can look
# around and blink. No brain/nervous_system integration yet — this is
# purely for the two-display hardware bring-up test in main.py.

import time

SCLERA_COLOR = 0xFFFF  # white, RGB565
PUPIL_COLOR = 0x0000   # black
BACKGROUND_COLOR = 0x0000

EYE_CENTER = (120, 120)
PUPIL_RADIUS = 42
MAX_PUPIL_OFFSET = 34


class Eye:
    def __init__(self, driver):
        self.driver = driver
        self.pos = EYE_CENTER
        self._redraw()

    def _redraw(self):
        self.driver.fill(SCLERA_COLOR)
        self.driver.fill_circle(self.pos[0], self.pos[1], PUPIL_RADIUS, PUPIL_COLOR)

    def look(self, dx: float, dy: float):
        """dx, dy each in [-1, 1] — direction to look."""
        x = EYE_CENTER[0] + int(dx * MAX_PUPIL_OFFSET)
        y = EYE_CENTER[1] + int(dy * MAX_PUPIL_OFFSET)
        self.pos = (x, y)
        self._redraw()

    def center(self):
        self.look(0, 0)

    def blink(self):
        self.driver.fill(BACKGROUND_COLOR)
        time.sleep_ms(180)
        self._redraw()
