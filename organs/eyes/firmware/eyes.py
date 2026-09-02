# An "eye" that can look around, blink, and show a named expression
# (expressions.py) — look direction and expression combine, so an
# expression's pupil/tracking element moves rather than sitting frozen.

import random
import time

from eye_geometry import BACKGROUND_COLOR
import expressions

try:
    from time import sleep_ms
except ImportError:
    # CPython (desktop simulator) has no time.sleep_ms — MicroPython does.
    def sleep_ms(ms):
        time.sleep(ms / 1000)


class Eye:
    def __init__(self, driver, mirror: bool = False):
        """mirror: flips asymmetric decorative shapes (e.g. a scowling
        eyebrow) so they point inward on this eye — see expressions.py.
        Never affects look direction itself, so both eyes still look the
        same way when told to."""
        self.driver = driver
        self.mirror = mirror
        self.expression = None
        self.dx = 0.0
        self.dy = 0.0
        self._render()

    def _render(self):
        expressions.render(self.expression, self.driver, dx=self.dx, dy=self.dy, mirror=self.mirror)

    def look(self, dx: float, dy: float):
        """dx, dy each in [-1, 1] — direction to look."""
        self.dx, self.dy = dx, dy
        self._render()

    def center(self):
        self.look(0.0, 0.0)

    def set_expression(self, name: str):
        """Switch to a named mood/activity expression (see
        expressions.py), keeping the current look direction."""
        self.expression = name
        self._render()

    def blink(self):
        self.driver.fill(BACKGROUND_COLOR)
        sleep_ms(180)
        self._render()


class Face:
    """Coordinates a left/right Eye pair so idle movement — look drift,
    occasional blinks — happens in sync rather than each eye wandering
    independently, which would look wall-eyed. Call tick() regularly
    (e.g. every ~150ms) from whatever loop is running: a plain while-loop
    on the Pico, or a Tkinter .after() callback in the simulator."""

    IDLE_MOVE_CHANCE = 0.06
    BLINK_CHANCE = 0.03

    def __init__(self, left: Eye, right: Eye):
        self.left = left
        self.right = right

    def set_expression(self, name: str):
        self.left.set_expression(name)
        self.right.set_expression(name)

    def look(self, dx: float, dy: float):
        self.left.look(dx, dy)
        self.right.look(dx, dy)

    def blink(self):
        self.left.blink()
        self.right.blink()

    def tick(self):
        if random.random() < self.IDLE_MOVE_CHANCE:
            self.look(random.uniform(-1, 1), random.uniform(-1, 1))
        if random.random() < self.BLINK_CHANCE:
            self.blink()
