"""The firmware's drawing/behaviour code is plain Python (no machine
imports), so it runs here against a recording fake panel."""

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "organs", "eyes", "firmware"))

import expressions  # noqa: E402
from eyes import Eye, Face  # noqa: E402
from brain.limbic.mood import CATEGORIES  # noqa: E402


class RecordingDriver:
    def __init__(self):
        self.calls = []
        self.shows = 0

    def fill(self, color):
        self.calls = [("fill", color)]

    def fill_circle(self, cx, cy, r, color):
        self.calls.append(("circle", round(cx), round(cy), round(r), color))

    def fill_polygon(self, points, color):
        self.calls.append(("poly", tuple((round(x), round(y)) for x, y in points), color))

    def show(self):
        self.shows += 1


def _draw(name, intensity, mirror=False, t=0):
    driver = RecordingDriver()
    expressions.render(name, driver, mirror=mirror, t=t, intensity=intensity)
    return driver.calls


@pytest.mark.parametrize("category", CATEGORIES)
def test_every_mood_has_art(category):
    assert expressions.REGISTRY[category].render is not None


@pytest.mark.parametrize("category", CATEGORIES)
def test_each_intensity_looks_different(category):
    frames = [tuple(_draw(category, i)) for i in (1, 2, 3)]
    assert len(set(frames)) == 3


@pytest.mark.parametrize("name", sorted(expressions.EXPRESSIONS))
@pytest.mark.parametrize("intensity", (1, 2, 3))
def test_every_expression_renders_at_every_intensity(name, intensity):
    for mirror in (False, True):
        assert _draw(name, intensity, mirror=mirror)


def _face():
    left, right = RecordingDriver(), RecordingDriver()
    face = Face(Eye(left), Eye(right, mirror=True))
    return face, left, right


def test_combined_update_redraws_once():
    face, left, right = _face()
    before = left.shows
    assert face.update(expression="happy", intensity=3, direction=(0.5, -0.5))
    assert left.shows - before == 1 and right.shows - before == 1
    assert (face.left.expression, face.left.intensity) == ("happy", 3)
    assert (face.right.dx, face.right.dy) == (0.5, -0.5)


def test_repeated_identical_update_does_not_redraw():
    face, left, _ = _face()
    face.update(expression="sad", intensity=1, direction=(0.1, 0.1))
    before = left.shows
    assert not face.update(expression="sad", intensity=1, direction=(0.1, 0.1))
    assert left.shows == before


def test_direction_alone_keeps_expression():
    face, _, _ = _face()
    face.update(expression="angry", intensity=2)
    face.update(direction=(-1, 0))
    assert (face.left.expression, face.left.intensity, face.left.dx) == ("angry", 2, -1)


def test_direction_cuts_short_an_idle_glance():
    face, _, _ = _face()
    face._t, face._glance_until = 5, 50
    face.update(direction=(0.3, 0.3))
    assert (face.left.dx, face.left.dy) == (0.3, 0.3)


def test_non_trackable_expression_ignores_direction_until_it_changes():
    face, _, _ = _face()
    face.update(expression="sleeping")
    face.update(direction=(1, 1))
    assert (face.left.dx, face.left.dy) == (0.0, 0.0)
    face.update(expression="calm", intensity=1)
    assert (face.left.dx, face.left.dy) == (1, 1)


def test_blink_is_non_blocking_and_tick_reopens():
    face, left, _ = _face()
    face.update(expression="calm")
    face.blink()
    assert left.calls == [("fill", 0x0000)]
    face.tick()
    assert len(left.calls) > 1
