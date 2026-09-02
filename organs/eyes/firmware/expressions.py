# Named mood/activity expressions — full-eye artwork drawn straight onto
# a driver. Every expression can still look around (dx, dy, each in
# [-1, 1], same convention as Eye.look()) — only genuinely fixed parts
# (an eyelid, an eyebrow, an X) stay put; whatever stands in for the
# pupil moves under them, same as a real eye. These are stylised
# interpretations of Henry's drawings (see the .jpg in this folder), not
# literal reproductions — redraw/adjust the numbers below as his designs
# get clearer, or add new ones the same way.
#
# `mirror` is for shapes that should point inward on both eyes (e.g. a
# scowling eyebrow angled down towards the nose on both sides) rather
# than identically on both panels, which would read as both eyebrows
# tilting the same way instead of converging. It only ever affects which
# side of a static, asymmetric shape is which — never dx/dy — precisely
# so it can't reintroduce the cross-eyed look-direction bug fixed
# earlier (see README's "What the bring-up test does").
#
# A driver only needs fill(color), fill_circle(cx, cy, r, color), and
# fill_polygon(points, color) to render every expression here — that's
# the whole contract, satisfied by both the real GC9A01 driver and the
# desktop SimDriver (organs/eyes/simulate.py). Kept in black-on-white
# throughout, same as the pencil-on-paper drawings they're based on.
#
# Not implemented yet:
# - "gaming": Henry wants the eyes to show video-game characters
#   (he drew Fortnite-style figures) when the robot is playing a game.
#   Full character art is a lot more than these primitives draw well —
#   worth a dedicated design once it's actually needed.
# - Two of his drawings weren't legible enough to transcribe (a
#   half-circle/wink shape, and one labelled roughly "cyees") — he's
#   redrawing those in a later iteration.
# - "pointing" isn't a static expression at all — it's just `Eye.look()`
#   aimed at whatever the robot is pointing at, using the existing
#   look-direction machinery, not new artwork.

import math

from eye_geometry import SCLERA_COLOR, PUPIL_COLOR, EYE_CENTER, MAX_PUPIL_OFFSET, WIDTH, HEIGHT

CX, CY = EYE_CENTER


def _offset(dx, dy, max_offset):
    return dx * max_offset, dy * max_offset


def _thick_line(driver, x0, y0, x1, y1, thickness, color):
    dx, dy = x1 - x0, y1 - y0
    length = math.hypot(dx, dy) or 1
    px, py = -dy / length * thickness / 2, dx / length * thickness / 2
    driver.fill_polygon([
        (x0 - px, y0 - py), (x0 + px, y0 + py),
        (x1 + px, y1 + py), (x1 - px, y1 - py),
    ], color)


def _crescent(driver, cx, cy, r=60, carve_dy=48, carve_r=60):
    """An upward-smiling closed-eye crescent: a filled circle with a
    second, lower circle carved out of it in the background color,
    leaving a thin arc — the ^ shape from the "happy"/"singing" drawings."""
    driver.fill(SCLERA_COLOR)
    driver.fill_circle(cx, cy, r, PUPIL_COLOR)
    driver.fill_circle(cx, cy + carve_dy, carve_r, SCLERA_COLOR)


def render_neutral(driver, dx=0.0, dy=0.0, mirror=False):
    ox, oy = _offset(dx, dy, MAX_PUPIL_OFFSET)
    driver.fill(SCLERA_COLOR)
    driver.fill_circle(CX + ox, CY + oy, 42, PUPIL_COLOR)


def render_happy(driver, dx=0.0, dy=0.0, mirror=False):
    ox, oy = _offset(dx, dy, 20)
    _crescent(driver, CX + ox, CY - 8 + oy)


def render_singing(driver, dx=0.0, dy=0.0, mirror=False):
    """Like "happy", but with eyelashes fanning up from the crescent."""
    ox, oy = _offset(dx, dy, 20)
    cx, cy = CX + ox, CY - 8 + oy
    _crescent(driver, cx, cy)
    base_x, base_y = cx, cy - 40
    for angle_deg in (-50, -90, -130):
        a = math.radians(angle_deg)
        adx, ady = math.cos(a), math.sin(a)
        length, thickness = 26, 7
        _thick_line(driver, base_x, base_y, base_x + adx * length, base_y + ady * length, thickness, PUPIL_COLOR)


def render_sad(driver, dx=0.0, dy=0.0, mirror=False):
    driver.fill(SCLERA_COLOR)
    # droopy eyelid over most of the eye — fixed, doesn't track
    driver.fill_polygon([(0, 0), (WIDTH, 0), (WIDTH, 128), (0, 128)], PUPIL_COLOR)
    # downward-curving sliver showing at the bottom, like a frown — this
    # part tracks, along with the tears
    ox, oy = _offset(dx, dy, 15)
    driver.fill_circle(CX + ox, CY + 78 + oy, 70, PUPIL_COLOR)
    driver.fill_circle(CX + ox, CY + 35 + oy, 65, SCLERA_COLOR)
    driver.fill_polygon([(96 + ox, 200 + oy), (108 + ox, 200 + oy), (108 + ox, 232 + oy), (96 + ox, 232 + oy)], PUPIL_COLOR)
    driver.fill_polygon([(132 + ox, 200 + oy), (144 + ox, 200 + oy), (144 + ox, 232 + oy), (132 + ox, 232 + oy)], PUPIL_COLOR)


def render_mad(driver, dx=0.0, dy=0.0, mirror=False):
    driver.fill(SCLERA_COLOR)
    # slanted, lowered eyebrow — droops down towards the inner corner
    # (the side facing the other eye) on *both* eyes, so they converge
    # into a scowl instead of both tilting the same way. mirror flips
    # which side is "inner" for the right eye.
    outer_depth, inner_depth = 55, 110
    left_depth, right_depth = (inner_depth, outer_depth) if mirror else (outer_depth, inner_depth)
    driver.fill_polygon([(0, 0), (WIDTH, 0), (WIDTH, right_depth), (0, left_depth)], PUPIL_COLOR)
    ox, oy = _offset(dx, dy, 20)
    driver.fill_circle(CX + ox, CY + 30 + oy, 34, PUPIL_COLOR)


def render_serious(driver, dx=0.0, dy=0.0, mirror=False):
    """Furrowed brow: a scribble of short crossing strokes pressing down
    on the pupil, like the crosshatching in the drawing. The scribble is
    fixed (it's the brow); the pupil underneath tracks."""
    driver.fill(SCLERA_COLOR)
    ox, oy = _offset(dx, dy, 20)
    driver.fill_circle(CX + ox, CY + oy, 42, PUPIL_COLOR)
    for x0, y0, x1, y1 in (
        (60, 70, 150, 100), (150, 70, 60, 100),
        (70, 60, 160, 90), (160, 95, 70, 65),
    ):
        _thick_line(driver, x0, y0, x1, y1, 7, PUPIL_COLOR)


def render_sleepy(driver, dx=0.0, dy=0.0, mirror=False):
    """Drowsy but still open — half-lidded, distinct from fully-closed
    "sleeping". Lid is fixed; the pupil tracks in the narrow gap left
    under it."""
    driver.fill(SCLERA_COLOR)
    ox, oy = _offset(dx, dy, 15)
    oy = max(-8, min(8, oy))  # keep the pupil clear of the lid either way
    driver.fill_circle(CX + ox, CY + 15 + oy, 34, PUPIL_COLOR)
    driver.fill_polygon([(0, 0), (WIDTH, 0), (WIDTH, 88), (0, 88)], PUPIL_COLOR)


def render_sleeping(driver, dx=0.0, dy=0.0, mirror=False):
    """Fully closed — a flat line, no pupil. Still allowed to drift a
    little so it doesn't look like a dead pixel."""
    driver.fill(SCLERA_COLOR)
    ox, oy = _offset(dx, dy, 20)
    oy = max(-6, min(6, oy))
    driver.fill_polygon([
        (40 + ox, 114 + oy), (200 + ox, 114 + oy),
        (200 + ox, 126 + oy), (40 + ox, 126 + oy),
    ], PUPIL_COLOR)


def render_dead(driver, dx=0.0, dy=0.0, mirror=False):
    ox, oy = _offset(dx, dy, 20)
    driver.fill(SCLERA_COLOR)
    _thick_line(driver, 70 + ox, 70 + oy, 170 + ox, 170 + oy, 16, PUPIL_COLOR)
    _thick_line(driver, 170 + ox, 70 + oy, 70 + ox, 170 + oy, 16, PUPIL_COLOR)


def render_zombie(driver, dx=0.0, dy=0.0, mirror=False):
    """A vacant stare: an off-center pupil under a heavy, half-drooped
    lid. The off-center skew is deliberate and stays put regardless of
    mirror — both eyes drift the same absolute way, which is what
    reads as "not quite tracking together" rather than a normal gaze."""
    driver.fill(SCLERA_COLOR)
    driver.fill_polygon([(0, 0), (WIDTH, 0), (WIDTH, 60), (0, 60)], PUPIL_COLOR)
    ox, oy = _offset(dx, dy, 20)
    driver.fill_circle(CX + 20 + ox, CY + 5 + oy, 30, PUPIL_COLOR)


def render_spy(driver, dx=0.0, dy=0.0, mirror=False):
    """Narrowed to a squint, like sunglasses/a suspicious sideways look.
    The slit is wide but short, so horizontal movement reads much more
    than vertical."""
    driver.fill(SCLERA_COLOR)
    driver.fill_polygon([(0, 0), (WIDTH, 0), (WIDTH, 96), (0, 96)], PUPIL_COLOR)
    driver.fill_polygon([(0, 144), (WIDTH, 144), (WIDTH, HEIGHT), (0, HEIGHT)], PUPIL_COLOR)
    ox, oy = dx * 40, dy * 8
    driver.fill_circle(CX + ox, CY + oy, 16, PUPIL_COLOR)


# Keyed by both Henry's word for it and, where one exists, the matching
# brain/limbic/mood.py category name — "mad" the drawing says, "angry"
# the mood system says, same artwork either way.
EXPRESSIONS = {
    "happy": render_happy,
    "singing": render_singing,
    "sad": render_sad,
    "mad": render_mad,
    "angry": render_mad,
    "serious": render_serious,
    "sleepy": render_sleepy,
    "sleeping": render_sleeping,
    "dead": render_dead,
    "zombie": render_zombie,
    "spy": render_spy,
}


def render(name: str, driver, dx: float = 0.0, dy: float = 0.0, mirror: bool = False):
    """Render a named expression looking in direction (dx, dy), falling
    back to the plain neutral eye for anything not drawn yet (e.g.
    "calm", "curious", "excited", "scared" — mood categories with no
    artwork from Henry yet)."""
    EXPRESSIONS.get(name, render_neutral)(driver, dx=dx, dy=dy, mirror=mirror)
