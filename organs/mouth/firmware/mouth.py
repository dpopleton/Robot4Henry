# Qbot's mouth: white lines on black. A flat line while quiet; while
# talking, a seismograph in a mouth shape — a zig-zag of spikes up and
# down from the line, tallest in the middle and fading to nothing at the
# corners, re-randomised every frame so it flickers constantly. How tall
# the spikes get follows the voice level the laptop sends (D-024); with no
# levels arriving, it makes up its own speech-like rhythm.
#
# Plain Python (no machine imports), so it runs unchanged on the Pico, in
# the virtual robot and in the tests. A driver needs fill(color),
# fill_circle(cx, cy, r, color) and fill_polygon(points, color) — the same
# contract as the eyes — and optionally show(), called once per redraw.

import math
import random

from mouth_geometry import (
    BACKGROUND_COLOR, LINE_COLOR, CENTER_Y, LEFT, RIGHT,
    LINE_THICKNESS, MAX_AMPLITUDE, SPIKES,
)

# One frame; main.py and the virtual panel call tick() this often. Measured on
# a Pico 2 (2026-11-05): drawing a talking frame takes ~25ms (worst ~36ms),
# and pushing 320x240 to the panel ~31ms at 40MHz SPI, so 50ms frames didn't fit.
TICK_MS = 80
LEVEL_TIMEOUT_TICKS = 4      # ~320ms without a level while talking: wiggle by itself instead
ATTACK = 0.6                 # how fast the shown level rises towards the target, per tick
RELEASE = 0.3                # ...and falls (slower, so it doesn't look jumpy)
FLAT = 0.02                  # below this, after talking stops, it's drawn flat again
MIN_SPIKE = 0.35             # each spike is this-to-1 of the envelope height, at random

# Self-wiggle: a new syllable every few ticks, with the odd gap between words.
SYLLABLE_TICKS = (2, 5)
SYLLABLE_LEVELS = (0.35, 0.9)
GAP_CHANCE = 0.15
GAP_LEVEL = 0.05


def envelope(u):
    """The mouth shape: 0 at the corners (u=0, u=1), 1 in the middle."""
    return math.sin(math.pi * u)


def seismograph_points(level, rand=random.random):
    """The zig-zag for a level 0-1: from corner to corner, alternating up
    and down, each spike a random share of the envelope at that point."""
    points = [(LEFT, CENTER_Y)]
    step = (RIGHT - LEFT) / (SPIKES + 1)
    for i in range(1, SPIKES + 1):
        height = MAX_AMPLITUDE * level * envelope(i / (SPIKES + 1)) * (MIN_SPIKE + (1 - MIN_SPIKE) * rand())
        points.append((LEFT + i * step, CENTER_Y - height if i % 2 else CENTER_Y + height))
    points.append((RIGHT, CENTER_Y))
    return points


def draw_line(driver, points, thickness=LINE_THICKNESS, color=LINE_COLOR):
    """A thick polyline with round joins and ends: a filled quad along
    each segment, and a dot at every point."""
    half = thickness / 2
    for (x0, y0), (x1, y1) in zip(points, points[1:]):
        dx, dy = x1 - x0, y1 - y0
        length = math.sqrt(dx * dx + dy * dy) or 1
        px, py = -dy / length * half, dx / length * half
        driver.fill_polygon([(x0 - px, y0 - py), (x0 + px, y0 + py),
                             (x1 + px, y1 + py), (x1 - px, y1 - py)], color)
    for x, y in points:
        driver.fill_circle(x, y, half, color)


class Mouth:
    def __init__(self, driver, rand=random.random):
        """rand: a 0-1 random source — pass a seeded one for repeatable tests."""
        self.driver = driver
        self.rand = rand
        self._show = getattr(driver, "show", None)
        self.talking = False
        self.level = 0.0                 # newest level from the host, 0-1
        self._ticks_since_level = None   # None = no levels since talking started
        self._wiggle = 0.0
        self._wiggle_ticks = 0
        self.shown = 0.0                 # smoothed level actually drawn
        self._flat_drawn = False
        self._draw([(LEFT, CENTER_Y), (RIGHT, CENTER_Y)])
        self._flat_drawn = True

    def update(self, talking=None, level=None):
        """Apply a command: talking True/False, level 0-100. None means
        "unchanged". Levels only count while talking. Nothing is drawn
        here — the next tick() does, as it does every frame anyway."""
        if talking is not None and talking != self.talking:
            self.talking = talking
            self._ticks_since_level = None
        if level is not None and self.talking:
            self.level = level / 100
            self._ticks_since_level = 0

    def tick(self):
        """Advance one frame. Returns True if it redrew — every frame while
        talking or settling, never while quietly flat."""
        target = self._target()
        rate = ATTACK if target > self.shown else RELEASE
        self.shown += (target - self.shown) * rate

        if not self.talking and self.shown < FLAT:
            self.shown = 0.0
            if self._flat_drawn:
                return False
            self._draw([(LEFT, CENTER_Y), (RIGHT, CENTER_Y)])
            self._flat_drawn = True
            return True

        self._draw(seismograph_points(self.shown, self.rand))
        self._flat_drawn = False
        return True

    def redraw(self):
        """Draw the current state now — for when whatever shows it was
        covered or cleared (a quiet mouth doesn't otherwise redraw)."""
        if self.shown > 0:
            self._draw(seismograph_points(self.shown, self.rand))
            self._flat_drawn = False
        else:
            self._draw([(LEFT, CENTER_Y), (RIGHT, CENTER_Y)])
            self._flat_drawn = True

    def _target(self):
        if not self.talking:
            return 0.0
        if self._ticks_since_level is not None and self._ticks_since_level < LEVEL_TIMEOUT_TICKS:
            self._ticks_since_level += 1
            return self.level
        return self._self_wiggle()

    def _self_wiggle(self):
        """Made-up speech rhythm for when no levels are arriving."""
        if self._wiggle_ticks <= 0:
            lo, hi = SYLLABLE_LEVELS
            self._wiggle = GAP_LEVEL if self.rand() < GAP_CHANCE else lo + (hi - lo) * self.rand()
            ticks_lo, ticks_hi = SYLLABLE_TICKS
            self._wiggle_ticks = ticks_lo + int(self.rand() * (ticks_hi - ticks_lo + 1))
        self._wiggle_ticks -= 1
        return self._wiggle

    def _draw(self, points):
        self.driver.fill(BACKGROUND_COLOR)
        draw_line(self.driver, points)
        if self._show:
            self._show()
