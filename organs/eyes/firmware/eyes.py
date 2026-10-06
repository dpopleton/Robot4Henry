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
        self.t = 0
        self._render()

    def _render(self):
        expressions.render(self.expression, self.driver, dx=self.dx, dy=self.dy, mirror=self.mirror, t=self.t)

    def look(self, dx: float, dy: float):
        """dx, dy each in [-1, 1] — direction to look. A no-op for
        expressions whose spec marks them non-trackable (e.g. "dead"),
        since their render functions ignore dx/dy entirely — stored
        anyway so it takes effect if the expression changes later."""
        self.dx, self.dy = dx, dy
        self._render()

    def center(self):
        self.look(0.0, 0.0)

    def set_expression(self, name: str):
        """Switch to a named mood/activity expression (see
        expressions.py), keeping the current look direction."""
        self.expression = name
        self._render()

    def advance(self, t: int):
        """Bump the animation clock and redraw — used for idle
        flourishes (e.g. an eyebrow twitch, dripping tears) that keep
        moving even when look direction isn't changing. Only worth
        calling for expressions whose spec marks animates=True."""
        self.t = t
        self._render()

    def blink(self):
        self.driver.fill(BACKGROUND_COLOR)
        sleep_ms(180)
        self._render()


class Face:
    """Coordinates a left/right Eye pair: syncs look direction so both
    eyes track together, and drives natural-feeling idle behaviour —
    mostly holding attention on one spot with brief glances away, plus
    occasional blinks, rather than a continuous random drift. Call
    tick() regularly (e.g. every ~150ms) from whatever loop is running:
    a plain while-loop on the Pico, or a Tkinter .after() callback in
    the simulator.

    Whether idle movement/blinking/animation happens at all depends on
    the current expression's spec in expressions.REGISTRY — "dead" and
    "sleeping", for instance, are fully static by design.
    """

    GLANCE_CHANCE = 0.02   # per tick, chance to start a brief glance away
    GLANCE_TICKS = (2, 4)  # how many ticks a glance lasts (~300-600ms at 150ms/tick)
    BLINK_CHANCE = 0.02    # per tick

    def __init__(self, left: Eye, right: Eye):
        self.left = left
        self.right = right
        self.attention = (0.0, 0.0)
        self._glance_until = 0
        self._t = 0

    def set_expression(self, name: str):
        self.left.set_expression(name)
        self.right.set_expression(name)

    def look_at(self, dx: float, dy: float):
        """Where to rest the gaze when not mid-glance — this is what a
        future "look at whoever's talking" would call. Takes effect
        immediately unless a glance-away is currently mid-flight, and
        is a no-op for non-trackable expressions."""
        self.attention = (dx, dy)
        spec = expressions.REGISTRY.get(self.left.expression, expressions.NEUTRAL_SPEC)
        if spec.trackable and self._t >= self._glance_until:
            self._apply_look(dx, dy)

    def _apply_look(self, dx, dy):
        self.left.look(dx, dy)
        self.right.look(dx, dy)

    def blink(self):
        self.left.blink()
        self.right.blink()

    def tick(self):
        """Advance idle animation by one step. Cheap to call often —
        expressions that don't animate/track/blink just skip straight
        through with no redraw at all."""
        self._t += 1
        spec = expressions.REGISTRY.get(self.left.expression, expressions.NEUTRAL_SPEC)

        if spec.trackable:
            if self._t < self._glance_until:
                pass  # mid-glance — hold until it's over
            elif self._glance_until:
                self._apply_look(*self.attention)  # glance just ended — return to attention
                self._glance_until = 0
            elif random.random() < self.GLANCE_CHANCE:
                gx = max(-1.0, min(1.0, self.attention[0] + random.uniform(-1, 1)))
                gy = max(-1.0, min(1.0, self.attention[1] + random.uniform(-0.5, 0.5)))
                self._apply_look(gx, gy)
                self._glance_until = self._t + random.randint(*self.GLANCE_TICKS)

        if spec.blinks and random.random() < self.BLINK_CHANCE:
            self.blink()

        if spec.animates:
            self.left.advance(self._t)
            self.right.advance(self._t)
