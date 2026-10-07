# An "eye" that can look around, blink, and show a named expression
# (expressions.py) at an intensity — look direction and expression
# combine, so an expression's pupil/tracking element moves rather than
# sitting frozen.

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
        same way when told to.

        driver may optionally have show(): drivers that draw into an
        off-screen buffer (firmware/framebuffer.py) push the finished
        frame to the panel there, once per redraw."""
        self.driver = driver
        self.mirror = mirror
        self.expression = None
        self.intensity = expressions.DEFAULT_INTENSITY
        self.dx = 0.0
        self.dy = 0.0
        self.t = 0
        self._show = getattr(driver, "show", None)
        self.render()

    def render(self):
        expressions.render(self.expression, self.driver, dx=self.dx, dy=self.dy,
                           mirror=self.mirror, t=self.t, intensity=self.intensity)
        if self._show:
            self._show()

    def close(self):
        """Draw the eye shut (first half of a blink) without waiting."""
        self.driver.fill(BACKGROUND_COLOR)
        if self._show:
            self._show()

    def look(self, dx: float, dy: float):
        """dx, dy each in [-1, 1] — direction to look. A no-op for
        expressions whose spec marks them non-trackable (e.g. "dead"),
        since their render functions ignore dx/dy entirely — stored
        anyway so it takes effect if the expression changes later."""
        self.dx, self.dy = dx, dy
        self.render()

    def center(self):
        self.look(0.0, 0.0)

    def set_expression(self, name: str, intensity: int = None):
        """Switch to a named mood/activity expression (see
        expressions.py), keeping the current look direction. intensity
        None = the expression's default."""
        self.expression = name
        self.intensity = expressions.DEFAULT_INTENSITY if intensity is None else intensity
        self.render()

    def advance(self, t: int):
        """Bump the animation clock and redraw — used for idle
        flourishes (e.g. an eyebrow twitch, dripping tears) that keep
        moving even when look direction isn't changing. Only worth
        calling for expressions whose spec says they animate."""
        self.t = t
        self.render()

    def blink(self):
        """Blocking blink — fine for the bring-up test, but Face.blink()
        is what anything that also has to stay responsive should use."""
        self.close()
        sleep_ms(180)
        self.render()


class Face:
    """Coordinates a left/right Eye pair: syncs look direction so both
    eyes track together, and drives natural-feeling idle behaviour —
    mostly holding attention on one spot with brief glances away, plus
    occasional blinks, rather than a continuous random drift. Call
    tick() regularly (e.g. every ~150ms) from whatever loop is running:
    a plain while-loop on the Pico, or a Tkinter .after() callback in
    the simulator.

    update() is the one entry point for outside commands (direction,
    expression, or both) — it redraws at most once however many fields
    change, and not at all if nothing did.

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
        self.eyes = (left, right)
        self.attention = (0.0, 0.0)
        self._glance_until = 0
        self._blinking = False
        self._t = 0

    def _spec(self):
        return expressions.spec_for(self.left.expression)

    def _render(self):
        self._blinking = False
        for eye in self.eyes:
            eye.render()

    def update(self, expression=None, intensity=None, direction=None):
        """Apply any combination of a new expression (+ intensity, None =
        default) and a new attention direction (dx, dy). None means
        "leave as is". Returns True if it redrew."""
        changed = False
        if expression is not None:
            if intensity is None:
                intensity = expressions.DEFAULT_INTENSITY
            if expression != self.left.expression or intensity != self.left.intensity:
                for eye in self.eyes:
                    eye.expression, eye.intensity = expression, intensity
                changed = True

        if direction is not None:
            # An explicit command beats an idle glance — cut it short.
            self.attention = direction
            self._glance_until = 0
        # Re-aim even when only the expression changed: switching from a
        # non-trackable expression (e.g. "sleeping") must pick up wherever
        # attention moved meanwhile.
        if self._spec().trackable and self._t >= self._glance_until:
            dx, dy = self.attention
            if (dx, dy) != (self.left.dx, self.left.dy):
                for eye in self.eyes:
                    eye.dx, eye.dy = dx, dy
                changed = True

        if changed or self._blinking:
            self._render()
        return changed

    def set_expression(self, name: str, intensity: int = None):
        self.update(expression=name, intensity=intensity)

    def look_at(self, dx: float, dy: float):
        """Where to rest the gaze when not mid-glance — this is what a
        future "look at whoever's talking" would call. Takes effect
        immediately (cutting short any idle glance), and is a no-op for
        non-trackable expressions."""
        self.update(direction=(dx, dy))

    def blink(self):
        """Close both eyes now; the next tick() (or update()) reopens
        them. Non-blocking, so commands keep flowing mid-blink."""
        for eye in self.eyes:
            eye.close()
        self._blinking = True

    def tick(self):
        """Advance idle animation by one step. Cheap to call often —
        expressions that don't animate/track/blink just skip straight
        through with no redraw at all."""
        self._t += 1
        if self._blinking:
            self._render()  # second half of the blink
            return

        spec = self._spec()
        redraw = False

        if spec.trackable:
            if self._t < self._glance_until:
                pass  # mid-glance — hold until it's over
            elif self._glance_until:
                for eye in self.eyes:  # glance just ended — return to attention
                    eye.dx, eye.dy = self.attention
                self._glance_until = 0
                redraw = True
            elif random.random() < self.GLANCE_CHANCE:
                gx = max(-1.0, min(1.0, self.attention[0] + random.uniform(-1, 1)))
                gy = max(-1.0, min(1.0, self.attention[1] + random.uniform(-0.5, 0.5)))
                for eye in self.eyes:
                    eye.dx, eye.dy = gx, gy
                self._glance_until = self._t + random.randint(*self.GLANCE_TICKS)
                redraw = True

        if spec.animates_at(self.left.intensity):
            for eye in self.eyes:
                eye.t = self._t
            redraw = True

        if spec.blinks and random.random() < self.BLINK_CHANCE:
            self.blink()
        elif redraw:
            self._render()
