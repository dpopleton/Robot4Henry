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


# Intensity follows brain/limbic/mood.py: 1 "a little", 2 "quite", 3
# "very". Every render accepts it; ones with no intensity variants (e.g.
# "dead") just ignore it.
DEFAULT_INTENSITY = 2


class ExpressionSpec:
    def __init__(self, render=None, trackable=True, blinks=True, animates=False,
                 status="implemented", source="", notes=""):
        self.render = render
        self.trackable = trackable
        self.blinks = blinks
        # True/False, or a tuple of the intensities that animate — e.g.
        # tears only drip once sad is strong enough to have tears.
        self.animates = animates
        self.status = status  # "implemented" | "placeholder" | "needs_redraw" | "planned" | "not_an_expression"
        self.source = source
        self.notes = notes

    def animates_at(self, intensity):
        if isinstance(self.animates, bool):
            return self.animates
        return intensity in self.animates


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


def render_neutral(driver, dx=0.0, dy=0.0, mirror=False, t=0, intensity=2):
    ox, oy = _offset(dx, dy, MAX_PUPIL_OFFSET)
    driver.fill(SCLERA_COLOR)
    driver.fill_circle(CX + ox, CY + oy, 42, PUPIL_COLOR)


def render_happy(driver, dx=0.0, dy=0.0, mirror=False, t=0, intensity=2):
    """The ^ crescent gets thicker the happier it is; at 3 it bounces."""
    ox, oy = _offset(dx, dy, 20)
    if intensity >= 3:
        oy += 4 * math.sin(t * 0.5)
    carve_dy = (24, 42, 60)[intensity - 1]
    _crescent(driver, CX + ox, CY - 8 + oy, carve_dy=carve_dy)


# TODO: unused — disabled in REGISTRY until reworked (see the note there).
def render_singing(driver, dx=0.0, dy=0.0, mirror=False, t=0, intensity=2):
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


def _teardrop(driver, x, y, r, color):
    """A drop hanging from its point: circle with a triangle on top."""
    driver.fill_circle(x, y, r, color)
    driver.fill_polygon([(x - r * 0.95, y - r * 0.3), (x, y - r * 2.6), (x + r * 0.95, y - r * 0.3)], color)


def render_sad(driver, dx=0.0, dy=0.0, mirror=False, t=0, intensity=2):
    """Puppy-dog sad: the upper lid droops towards the *outer* corner
    (the opposite slant to angry), over a big glossy pupil gazing a
    little downward.
    Intensity steepens the droop; a tear wells up at 2 and runs down,
    looping, at 3."""
    driver.fill(SCLERA_COLOR)
    ox, oy = _offset(dx, dy, 22)
    cx, cy = CX + ox, CY + 22 + oy
    r = 46
    driver.fill_circle(cx, cy, r, PUPIL_COLOR)
    driver.fill_circle(cx - r * 0.35, cy - r * 0.35, r * 0.22, SCLERA_COLOR)

    # mirror=False: inner corner is the right edge (same as render_mad)
    inner, outer = ((50, 80), (55, 105), (60, 125))[intensity - 1]
    left_y, right_y = (inner, outer) if mirror else (outer, inner)
    driver.fill_polygon([(0, 0), (WIDTH, 0), (WIDTH, right_y), (0, left_y)], PUPIL_COLOR)

    if intensity >= 2:
        tear_x = (WIDTH - 50) if mirror else 50  # outer corner, clear of the pupil
        if intensity == 2:
            _teardrop(driver, tear_x, 168, 11, PUPIL_COLOR)
        else:
            _teardrop(driver, tear_x, 160 + (t * 4) % 48, 12, PUPIL_COLOR)


def render_mad(driver, dx=0.0, dy=0.0, mirror=False, t=0, intensity=2):
    """Eyebrow droops towards the inner corner (the side facing the
    other eye) on *both* eyes, so they converge into a scowl instead of
    both tilting the same way — mirror flips which side is "inner" for
    the right eye. It also twitches slightly (t), rather than sitting
    frozen mid-scowl. Intensity deepens the scowl and the twitch."""
    driver.fill(SCLERA_COLOR)
    twitch = int((2, 4, 6)[intensity - 1] * math.sin(t * 0.15))
    outer_depth, inner_depth = ((40, 80), (55, 110), (65, 128))[intensity - 1]
    outer_depth, inner_depth = outer_depth + twitch, inner_depth + twitch
    left_depth, right_depth = (inner_depth, outer_depth) if mirror else (outer_depth, inner_depth)
    driver.fill_polygon([(0, 0), (WIDTH, 0), (WIDTH, right_depth), (0, left_depth)], PUPIL_COLOR)
    ox, oy = _offset(dx, dy, 20)
    driver.fill_circle(CX + ox, CY + 30 + oy, 34, PUPIL_COLOR)


# TODO: unused — disabled in REGISTRY until reworked (see the note there).
def render_serious(driver, dx=0.0, dy=0.0, mirror=False, t=0, intensity=2):
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


def render_sleepy(driver, dx=0.0, dy=0.0, mirror=False, t=0, intensity=2):
    """Drowsy but still awake — distinct from fully-closed "sleeping".
    A heavy upper lid with a rounded, drooping edge and a lower lid
    pushing up, leaving a narrow almond-shaped gap with the pupil
    resting low in it. From 2 it nods off: the lid creeps down over a
    few seconds, then snaps back open, looping."""
    driver.fill(SCLERA_COLOR)
    ox, oy = _offset(dx, dy, 18)
    oy = max(-6, min(6, oy))
    driver.fill_circle(CX + ox, CY + 30 + oy, 40, PUPIL_COLOR)

    lid = (114, 126, 136)[intensity - 1]   # where the upper lid's edge sits mid-eye
    if intensity >= 2:
        cycle = t % 30                     # ~4.5s at 150ms ticks
        lid += (cycle * (1 if intensity == 2 else 1.4)) if cycle < 24 else 0
    lid = min(lid, 168)
    # Upper lid: a big circle whose bottom edge is a drooping curve —
    # reads as a heavy lid, not a flat shutter. A white band just below
    # it slices the top off the pupil, so the lid visibly sits *over*
    # the eye instead of merging into the pupil.
    big = 170
    driver.fill_circle(CX, lid + 8 - big, big, SCLERA_COLOR)
    driver.fill_circle(CX, lid - big, big, PUPIL_COLOR)
    # Lower lid: same trick from below.
    driver.fill_circle(CX, 196 + big, big, PUPIL_COLOR)


def render_sleeping(driver, dx=0.0, dy=0.0, mirror=False, t=0, intensity=2):
    """Fully closed — a flat line, no pupil. Deliberately static: no
    look direction, no blink (see REGISTRY — trackable=False)."""
    driver.fill(SCLERA_COLOR)
    driver.fill_polygon([(40, 114), (200, 114), (200, 126), (40, 126)], PUPIL_COLOR)


def render_dead(driver, dx=0.0, dy=0.0, mirror=False, t=0, intensity=2):
    """Deliberately static: no look direction, no blink (see
    REGISTRY — trackable=False)."""
    driver.fill(SCLERA_COLOR)
    _thick_line(driver, 70, 70, 170, 170, 16, PUPIL_COLOR)
    _thick_line(driver, 170, 70, 70, 170, 16, PUPIL_COLOR)


# TODO: unused — disabled in REGISTRY until reworked (see the note there).
def render_zombie(driver, dx=0.0, dy=0.0, mirror=False, t=0, intensity=2):
    """A vacant stare: an off-center pupil under a heavy, half-drooped
    lid. The off-center skew is deliberate and stays put regardless of
    mirror — both eyes drift the same absolute way, which is what
    reads as "not quite tracking together" rather than a normal gaze.
    Unblinking on purpose (see REGISTRY — blinks=False)."""
    driver.fill(SCLERA_COLOR)
    driver.fill_polygon([(0, 0), (WIDTH, 0), (WIDTH, 60), (0, 60)], PUPIL_COLOR)
    ox, oy = _offset(dx, dy, 20)
    driver.fill_circle(CX + 20 + ox, CY + 5 + oy, 30, PUPIL_COLOR)


def render_spy(driver, dx=0.0, dy=0.0, mirror=False, t=0, intensity=2):
    """Narrowed to a squint, like sunglasses/a suspicious sideways look.
    The slit is wide but short, so horizontal movement reads much more
    than vertical."""
    driver.fill(SCLERA_COLOR)
    driver.fill_polygon([(0, 0), (WIDTH, 0), (WIDTH, 96), (0, 96)], PUPIL_COLOR)
    driver.fill_polygon([(0, 144), (WIDTH, 144), (WIDTH, HEIGHT), (0, HEIGHT)], PUPIL_COLOR)
    ox, oy = dx * 40, dy * 8
    driver.fill_circle(CX + ox, CY + oy, 16, PUPIL_COLOR)


# --- Mood categories Henry hasn't drawn yet. These are placeholder
# interpretations so every brain/limbic/mood.py category shows
# *something* distinct at each intensity — swap in Henry's versions
# when he draws them (REGISTRY marks them status="placeholder").

def render_calm(driver, dx=0.0, dy=0.0, mirror=False, t=0, intensity=2):
    """Relaxed: a plain eye under a softly lowered lid. 1 is "calm",
    2-3 "deeply relaxed" (mood.py), so the lid comes down further."""
    driver.fill(SCLERA_COLOR)
    ox, oy = _offset(dx, dy, MAX_PUPIL_OFFSET)
    driver.fill_circle(CX + ox, CY + 8 + oy, 42, PUPIL_COLOR)
    lid = (44, 62, 76)[intensity - 1]
    driver.fill_polygon([(0, 0), (WIDTH, 0), (WIDTH, lid), (0, lid)], PUPIL_COLOR)


def render_curious(driver, dx=0.0, dy=0.0, mirror=False, t=0, intensity=2):
    """Interested and wide open: big, slightly upward-looking pupils
    with a catch-light, and raised, arched brows. Stronger curiosity =
    bigger pupil, higher brow. Symmetric on purpose — a one-eyed squint
    read as a mistake rather than a raised eyebrow."""
    driver.fill(SCLERA_COLOR)
    ox, oy = _offset(dx, dy, 26)
    r = (44, 50, 56)[intensity - 1]
    cx, cy = CX + ox, CY + 18 + oy
    # arched brow: a thick ring segment — big black circle with a white
    # one carved just below it, above the eye
    brow_y = (62, 52, 42)[intensity - 1]   # top of the arch, mid-eye
    driver.fill_circle(CX, brow_y + 150, 150, PUPIL_COLOR)
    driver.fill_circle(CX, brow_y + 168, 150, SCLERA_COLOR)
    # the carve also erased the pupil — redraw it on top
    driver.fill_circle(cx, cy, r, PUPIL_COLOR)
    driver.fill_circle(cx - r * 0.35, cy - r * 0.35, r * 0.22, SCLERA_COLOR)


def _sparkle(driver, cx, cy, r, intensity):
    """White catch-lights on a big pupil — the "anime excited" look.
    Not mirrored: light comes from the same direction for both eyes."""
    driver.fill_circle(cx - r * 0.35, cy - r * 0.35, r * 0.26, SCLERA_COLOR)
    if intensity >= 2:
        driver.fill_circle(cx + r * 0.32, cy + r * 0.30, r * 0.12, SCLERA_COLOR)


def render_excited(driver, dx=0.0, dy=0.0, mirror=False, t=0, intensity=2):
    """Wide, sparkly pupil that grows with intensity; at 3 it pulses."""
    driver.fill(SCLERA_COLOR)
    ox, oy = _offset(dx, dy, 24)
    r = (48, 56, 62)[intensity - 1]
    if intensity >= 3:
        r += 4 * math.sin(t * 0.6)
    cx, cy = CX + ox, CY + oy
    driver.fill_circle(cx, cy, r, PUPIL_COLOR)
    _sparkle(driver, cx, cy, r, intensity)


def render_scared(driver, dx=0.0, dy=0.0, mirror=False, t=0, intensity=2):
    """Wide-open eye with a shrinking pinprick pupil. From 2 a worried
    brow slants up towards the inner corner; at 3 the pupil trembles."""
    driver.fill(SCLERA_COLOR)
    ox, oy = _offset(dx, dy, MAX_PUPIL_OFFSET + 10)
    if intensity >= 3:
        ox += 3 * math.sin(t * 2.3)
        oy += 2 * math.sin(t * 1.7)
    r = (26, 19, 13)[intensity - 1]
    driver.fill_circle(CX + ox, CY + oy, r, PUPIL_COLOR)
    if intensity >= 2:
        outer_y, inner_y = 44, 18
        left_y, right_y = (inner_y, outer_y) if mirror else (outer_y, inner_y)
        _thick_line(driver, 40, left_y, 200, right_y, 12, PUPIL_COLOR)


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
        render=render_happy, blinks=False, animates=(3,),
        source="Row 3, the '^ ^' crescents labelled roughly \"happy\"",
        notes="Already closed, so blinking is a no-op — disabled rather than doing nothing. "
              "Intensity thickens the crescent; 3 bounces.",
    ),
    # TODO: not a mood — disabled until reworked: lashes need another look before it's used.
    # "singing": ExpressionSpec(
    #     render=render_singing, blinks=False, animates=True,
    #     source="Labelled 'singing'; a squiggle we couldn't otherwise parse",
    #     notes='Dan: "like happy, except with eyelashes" — implemented as happy + fluttering lashes.',
    # ),
    "sad": ExpressionSpec(
        render=render_sad, animates=(2, 3),
        source="Row 1 'sad' cluster: eyelid + tear lines + downward crescent",
        notes="Reworked: lid droops to the outer corner over a glossy downcast pupil. Steeper with intensity; "
              "tear wells at 2, runs at 3.",
    ),
    "mad": ExpressionSpec(
        render=render_mad, animates=True,
        source="'Mad' cluster, angled eyebrow shape",
        notes="Brow now droops towards the inner corner on both eyes (fixed from an earlier version where both eyes slanted the same way). "
              "Intensity deepens the scowl and twitch.",
    ),
    "angry": ExpressionSpec(
        render=render_mad, animates=True,
        source="Alias of 'mad' — brain/limbic/mood.py's category name for the same feeling",
        notes="Intensity deepens the scowl and twitch.",
    ),
    # TODO: not a mood — disabled until reworked: the pupil overlaps the scribble brow.
    # "serious": ExpressionSpec(
    #     render=render_serious,
    #     source="'Seeris' scribble/crosshatch over the eye",
    #     notes='Confirmed by Dan: furrowed brow.',
    # ),
    "sleepy": ExpressionSpec(
        render=render_sleepy, animates=(2, 3),
        source="Drowsy circle+scribble cluster near 'dead'",
        notes="Distinct from 'sleeping' — still awake, can still track/blink. Reworked: heavy curved lid over "
              "the pupil + lower lid; lower with intensity, nodding off (lid creeps shut, snaps open) at 2-3.",
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
    # TODO: not a mood — disabled until reworked: needs another look before it's used.
    # "zombie": ExpressionSpec(
    #     render=render_zombie, blinks=False,
    #     source="'zomb' circle with an off-center pupil",
    #     notes="Unblinking/vacant is intentional for the theme — revisit if it should blink after all.",
    # ),
    "spy": ExpressionSpec(
        render=render_spy,
        source="'Spy' narrow visor/slit shapes",
    ),
    # Mood categories brain/limbic/mood.py defines that Henry hasn't
    # drawn yet — placeholder art so every mood shows something.
    "calm": ExpressionSpec(
        render=render_calm, status="placeholder", source="brain/limbic/mood.py category",
        notes="No drawing yet — placeholder: relaxed lid, lower at 2-3 (\"deeply relaxed\").",
    ),
    "curious": ExpressionSpec(
        render=render_curious, status="placeholder", source="brain/limbic/mood.py category",
        notes="No drawing yet — placeholder: wide eyes, big pupils, raised arched brows; bigger/higher with intensity.",
    ),
    "excited": ExpressionSpec(
        render=render_excited, animates=(3,), status="placeholder", source="brain/limbic/mood.py category",
        notes="No drawing yet — placeholder: big sparkly pupil, bigger with intensity, pulsing at 3.",
    ),
    "scared": ExpressionSpec(
        render=render_scared, animates=(3,), status="placeholder", source="brain/limbic/mood.py category",
        notes="No drawing yet — placeholder: pinprick pupil, worried brow from 2, trembling at 3.",
    ),
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


def spec_for(name):
    return REGISTRY.get(name, NEUTRAL_SPEC)


def render(name, driver, dx=0.0, dy=0.0, mirror=False, t=0, intensity=DEFAULT_INTENSITY):
    """Render a named expression at intensity 1-3, looking in direction
    (dx, dy) at animation tick t, falling back to the plain neutral eye
    for anything not drawn yet (including "neutral" itself)."""
    EXPRESSIONS.get(name, render_neutral)(driver, dx=dx, dy=dy, mirror=mirror, t=t, intensity=intensity)
