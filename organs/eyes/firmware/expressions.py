# Named mood/activity expressions — full-eye artwork drawn straight onto
# a driver. These are stylised interpretations of Henry's drawings (see
# the .jpg in this folder), not literal reproductions.
#
# REGISTRY below is the single source of truth for both what an
# expression looks like AND how it behaves, so behavior can never drift
# out of sync with the artwork:
#   - trackable: can Face nudge this expression's look direction (idle
#     glances, or eventually "look at whoever's talking")? False for
#     "dead"/"sleeping" — those are fully static by design, not just
#     idle-still; their render functions ignore dx/dy entirely.
#   - blinks: does idle blinking apply? False for anything already
#     closed (blinking a closed eye is meaningless) or deliberately
#     unblinking (zombie's vacant stare).
#   - animates: does this expression have its own idle flourish
#     independent of look direction (e.g. a twitching eyebrow, dripping
#     tears)? Driven by `t`, a tick counter Face.tick() advances.
#   - status/source/notes: for organs/eyes/expression_status.py, which
#     regenerates organs/eyes/EXPRESSIONS.md from this registry — that's
#     the file to check for "what does Henry need to draw."
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

import math

from eye_geometry import SCLERA_COLOR, PUPIL_COLOR, EYE_CENTER, MAX_PUPIL_OFFSET, WIDTH, HEIGHT

CX, CY = EYE_CENTER


class ExpressionSpec:
    def __init__(self, render=None, trackable=True, blinks=True, animates=False,
                 status="implemented", source="", notes=""):
        self.render = render
        self.trackable = trackable
        self.blinks = blinks
        self.animates = animates
        self.status = status  # "implemented" | "needs_redraw" | "planned" | "not_an_expression"
        self.source = source
        self.notes = notes


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


def render_neutral(driver, dx=0.0, dy=0.0, mirror=False, t=0):
    ox, oy = _offset(dx, dy, MAX_PUPIL_OFFSET)
    driver.fill(SCLERA_COLOR)
    driver.fill_circle(CX + ox, CY + oy, 42, PUPIL_COLOR)


def render_happy(driver, dx=0.0, dy=0.0, mirror=False, t=0):
    ox, oy = _offset(dx, dy, 20)
    _crescent(driver, CX + ox, CY - 8 + oy)


def render_singing(driver, dx=0.0, dy=0.0, mirror=False, t=0):
    """Like "happy", but with eyelashes fanning up from the crescent —
    which flutter (length pulses with t) instead of sitting frozen."""
    ox, oy = _offset(dx, dy, 20)
    cx, cy = CX + ox, CY - 8 + oy
    _crescent(driver, cx, cy)
    flutter = math.sin(t * 0.3) * 4
    base_x, base_y = cx, cy - 40
    for angle_deg in (-50, -90, -130):
        a = math.radians(angle_deg)
        adx, ady = math.cos(a), math.sin(a)
        length, thickness = 26 + flutter, 7
        _thick_line(driver, base_x, base_y, base_x + adx * length, base_y + ady * length, thickness, PUPIL_COLOR)


def render_sad(driver, dx=0.0, dy=0.0, mirror=False, t=0):
    """Tears drip: they slide down and reset, looping, instead of
    sitting frozen mid-drop."""
    driver.fill(SCLERA_COLOR)
    # droopy eyelid over most of the eye — fixed, doesn't track
    driver.fill_polygon([(0, 0), (WIDTH, 0), (WIDTH, 128), (0, 128)], PUPIL_COLOR)
    # downward-curving sliver showing at the bottom, like a frown — this
    # part tracks, along with the tears
    ox, oy = _offset(dx, dy, 15)
    driver.fill_circle(CX + ox, CY + 78 + oy, 70, PUPIL_COLOR)
    driver.fill_circle(CX + ox, CY + 35 + oy, 65, SCLERA_COLOR)
    drip = (t * 3) % 40
    for tear_x in (94, 130):
        driver.fill_polygon([
            (tear_x + ox, 196 + oy + drip), (tear_x + 12 + ox, 196 + oy + drip),
            (tear_x + 12 + ox, 216 + oy + drip), (tear_x + ox, 216 + oy + drip),
        ], PUPIL_COLOR)


def render_mad(driver, dx=0.0, dy=0.0, mirror=False, t=0):
    """Eyebrow droops towards the inner corner (the side facing the
    other eye) on *both* eyes, so they converge into a scowl instead of
    both tilting the same way — mirror flips which side is "inner" for
    the right eye. It also twitches slightly (t), rather than sitting
    frozen mid-scowl."""
    driver.fill(SCLERA_COLOR)
    twitch = int(4 * math.sin(t * 0.15))
    outer_depth, inner_depth = 55 + twitch, 110 + twitch
    left_depth, right_depth = (inner_depth, outer_depth) if mirror else (outer_depth, inner_depth)
    driver.fill_polygon([(0, 0), (WIDTH, 0), (WIDTH, right_depth), (0, left_depth)], PUPIL_COLOR)
    ox, oy = _offset(dx, dy, 20)
    driver.fill_circle(CX + ox, CY + 30 + oy, 34, PUPIL_COLOR)


def render_serious(driver, dx=0.0, dy=0.0, mirror=False, t=0):
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


def render_sleepy(driver, dx=0.0, dy=0.0, mirror=False, t=0):
    """Drowsy but still open — half-lidded, distinct from fully-closed
    "sleeping". Lid is fixed; the pupil tracks in the narrow gap left
    under it."""
    driver.fill(SCLERA_COLOR)
    ox, oy = _offset(dx, dy, 15)
    oy = max(-8, min(8, oy))  # keep the pupil clear of the lid either way
    driver.fill_circle(CX + ox, CY + 15 + oy, 34, PUPIL_COLOR)
    driver.fill_polygon([(0, 0), (WIDTH, 0), (WIDTH, 88), (0, 88)], PUPIL_COLOR)


def render_sleeping(driver, dx=0.0, dy=0.0, mirror=False, t=0):
    """Fully closed — a flat line, no pupil. Deliberately static: no
    look direction, no blink (see REGISTRY — trackable=False)."""
    driver.fill(SCLERA_COLOR)
    driver.fill_polygon([(40, 114), (200, 114), (200, 126), (40, 126)], PUPIL_COLOR)


def render_dead(driver, dx=0.0, dy=0.0, mirror=False, t=0):
    """Deliberately static: no look direction, no blink (see
    REGISTRY — trackable=False)."""
    driver.fill(SCLERA_COLOR)
    _thick_line(driver, 70, 70, 170, 170, 16, PUPIL_COLOR)
    _thick_line(driver, 170, 70, 70, 170, 16, PUPIL_COLOR)


def render_zombie(driver, dx=0.0, dy=0.0, mirror=False, t=0):
    """A vacant stare: an off-center pupil under a heavy, half-drooped
    lid. The off-center skew is deliberate and stays put regardless of
    mirror — both eyes drift the same absolute way, which is what
    reads as "not quite tracking together" rather than a normal gaze.
    Unblinking on purpose (see REGISTRY — blinks=False)."""
    driver.fill(SCLERA_COLOR)
    driver.fill_polygon([(0, 0), (WIDTH, 0), (WIDTH, 60), (0, 60)], PUPIL_COLOR)
    ox, oy = _offset(dx, dy, 20)
    driver.fill_circle(CX + 20 + ox, CY + 5 + oy, 30, PUPIL_COLOR)


def render_spy(driver, dx=0.0, dy=0.0, mirror=False, t=0):
    """Narrowed to a squint, like sunglasses/a suspicious sideways look.
    The slit is wide but short, so horizontal movement reads much more
    than vertical."""
    driver.fill(SCLERA_COLOR)
    driver.fill_polygon([(0, 0), (WIDTH, 0), (WIDTH, 96), (0, 96)], PUPIL_COLOR)
    driver.fill_polygon([(0, 144), (WIDTH, 144), (WIDTH, HEIGHT), (0, HEIGHT)], PUPIL_COLOR)
    ox, oy = dx * 40, dy * 8
    driver.fill_circle(CX + ox, CY + oy, 16, PUPIL_COLOR)


NEUTRAL_SPEC = ExpressionSpec(
    render=render_neutral,
    source="default — no mood/activity set",
    notes="Plain open eye; also the fallback for any name not in this registry.",
)

# Keyed by both Henry's word for it and, where one exists, the matching
# brain/limbic/mood.py category name — "mad" the drawing says, "angry"
# the mood system says, same artwork either way.
REGISTRY = {
    "happy": ExpressionSpec(
        render=render_happy, blinks=False,
        source="Row 3, the '^ ^' crescents labelled roughly \"happy\"",
        notes="Already closed, so blinking is a no-op — disabled rather than doing nothing.",
    ),
    "singing": ExpressionSpec(
        render=render_singing, blinks=False, animates=True,
        source="Labelled 'singing'; a squiggle we couldn't otherwise parse",
        notes='Dan: "like happy, except with eyelashes" — implemented as happy + fluttering lashes.',
    ),
    "sad": ExpressionSpec(
        render=render_sad, animates=True,
        source="Row 1 'sad' cluster: eyelid + tear lines + downward crescent",
    ),
    "mad": ExpressionSpec(
        render=render_mad, animates=True,
        source="'Mad' cluster, angled eyebrow shape",
        notes="Brow now droops towards the inner corner on both eyes (fixed from an earlier version where both eyes slanted the same way).",
    ),
    "angry": ExpressionSpec(
        render=render_mad, animates=True,
        source="Alias of 'mad' — brain/limbic/mood.py's category name for the same feeling",
    ),
    "serious": ExpressionSpec(
        render=render_serious,
        source="'Seeris' scribble/crosshatch over the eye",
        notes='Confirmed by Dan: furrowed brow.',
    ),
    "sleepy": ExpressionSpec(
        render=render_sleepy,
        source="Drowsy circle+scribble cluster near 'dead'",
        notes="Distinct from 'sleeping' — still awake, half-lidded, can still track/blink.",
    ),
    "sleeping": ExpressionSpec(
        render=render_sleeping, trackable=False, blinks=False,
        source="'sleeping' flat-line pair",
        notes="Fully static per Dan: no look direction, no blinking.",
    ),
    "dead": ExpressionSpec(
        render=render_dead, trackable=False, blinks=False,
        source="'dead' circle with an X",
        notes="Fully static per Dan: no look direction, no blinking.",
    ),
    "zombie": ExpressionSpec(
        render=render_zombie, blinks=False,
        source="'zomb' circle with an off-center pupil",
        notes="Unblinking/vacant is intentional for the theme — revisit if it should blink after all.",
    ),
    "spy": ExpressionSpec(
        render=render_spy,
        source="'Spy' narrow visor/slit shapes",
    ),
    # Mood categories brain/limbic/mood.py already defines, with no
    # drawing yet — falls back to the neutral eye until Henry draws them.
    "calm": ExpressionSpec(render=None, trackable=None, blinks=None, status="planned",
                            source="brain/limbic/mood.py category", notes="No drawing yet."),
    "curious": ExpressionSpec(render=None, trackable=None, blinks=None, status="planned",
                               source="brain/limbic/mood.py category", notes="No drawing yet."),
    "excited": ExpressionSpec(render=None, trackable=None, blinks=None, status="planned",
                               source="brain/limbic/mood.py category", notes="No drawing yet."),
    "scared": ExpressionSpec(render=None, trackable=None, blinks=None, status="planned",
                              source="brain/limbic/mood.py category", notes="No drawing yet."),
    # Henry's ideas that aren't drawable/legible yet.
    "gaming": ExpressionSpec(
        render=None, trackable=None, blinks=None, status="planned",
        source="'Fortnite' character sketches (two framed figures)",
        notes="Henry wants eyes to show game characters during gameplay. Full character art is well beyond "
              "these circle/polygon primitives — needs a dedicated design once it's actually needed. Low priority.",
    ),
    "unclear_wink": ExpressionSpec(
        render=None, trackable=None, blinks=None, status="needs_redraw",
        source="Half-circle/wink shape next to illegible label (maybe \"quiet time\"?)",
        notes="Handwriting not legible enough to transcribe. Henry to redraw with a clearer label.",
    ),
    "unclear_cyees": ExpressionSpec(
        render=None, trackable=None, blinks=None, status="needs_redraw",
        source="'D'-shaped eye labelled roughly \"Cyees\"",
        notes="Meaning unknown (cyclops? cutie?). Henry to redraw with a clearer label.",
    ),
    "pointing": ExpressionSpec(
        render=None, trackable=None, blinks=None, status="not_an_expression",
        source="'pointing' cluster: circle + arrow/pointer shape",
        notes="Not a static expression — just Eye.look()/Face.look_at() aimed wherever the robot is "
              "pointing, using the existing look-direction machinery. No new artwork needed.",
    ),
}

EXPRESSIONS = {name: spec.render for name, spec in REGISTRY.items() if spec.render is not None}


def render(name: str, driver, dx: float = 0.0, dy: float = 0.0, mirror: bool = False, t: int = 0):
    """Render a named expression looking in direction (dx, dy) at
    animation tick t, falling back to the plain neutral eye for
    anything not drawn yet."""
    EXPRESSIONS.get(name, render_neutral)(driver, dx=dx, dy=dy, mirror=mirror, t=t)
