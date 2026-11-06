"""The mouth's drawing/behaviour code is plain Python (no machine
imports), so it runs here against a recording fake panel."""

import os
import random
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "organs", "mouth", "firmware"))

import mouth  # noqa: E402
from mouth import Mouth, seismograph_points, LEVEL_TIMEOUT_TICKS  # noqa: E402
from mouth_geometry import (  # noqa: E402
    WIDTH, HEIGHT, CENTER_Y, LEFT, RIGHT, LINE_THICKNESS, MAX_AMPLITUDE, BACKGROUND_COLOR,
)


class RecordingDriver:
    def __init__(self):
        self.calls = []
        self.shows = 0

    def fill(self, color):
        self.calls = [("fill", color)]

    def fill_circle(self, cx, cy, r, color):
        self.calls.append(("circle", cx, cy, r, color))

    def fill_polygon(self, points, color):
        self.calls.append(("poly", tuple(points), color))

    def show(self):
        self.shows += 1

    def dots(self):
        return [(c[1], c[2]) for c in self.calls if c[0] == "circle"]


def _mouth(seed=1):
    driver = RecordingDriver()
    return Mouth(driver, random.Random(seed).random), driver


def _height(points):
    return max(abs(y - CENTER_Y) for _, y in points)


def test_starts_as_a_flat_line():
    m, driver = _mouth()
    assert driver.shows == 1
    assert driver.calls[0] == ("fill", BACKGROUND_COLOR)
    assert {y for _, y in driver.dots()} == {CENTER_Y}


def test_quiet_ticks_dont_redraw():
    m, driver = _mouth()
    assert not any(m.tick() for _ in range(20))
    assert driver.shows == 1


def test_talking_redraws_every_tick_and_flickers():
    m, driver = _mouth()
    m.update(talking=True)
    frames = []
    for _ in range(10):
        m.update(level=60)
        assert m.tick()
        frames.append(tuple(driver.dots()))
    assert driver.shows == 11
    assert len(set(frames)) == 10  # never the same frame twice


@pytest.mark.parametrize("level", [0.0, 0.3, 1.0])
def test_seismograph_is_mouth_shaped_and_stays_on_screen(level):
    rng = random.Random(2).random
    for _ in range(50):
        points = seismograph_points(level, rng)
        assert points[0] == (LEFT, CENTER_Y) and points[-1] == (RIGHT, CENTER_Y)  # corners on the line
        assert [x for x, _ in points] == sorted(x for x, _ in points)
        assert _height(points) <= MAX_AMPLITUDE * level + 1e-9
        half = LINE_THICKNESS / 2
        assert all(half <= x <= WIDTH - half and half <= y <= HEIGHT - half for x, y in points)


def test_spikes_alternate_up_and_down():
    points = seismograph_points(1.0, random.Random(3).random)[1:-1]
    signs = [y < CENTER_Y for _, y in points]
    assert all(a != b for a, b in zip(signs, signs[1:]))


def test_tallest_in_the_middle():
    points = seismograph_points(1.0, lambda: 1.0)  # no randomness: pure envelope
    middle = len(points) // 2
    assert _height(points[middle - 1:middle + 2]) > 3 * _height(points[1:3])


def test_louder_means_taller():
    def height_at(level):
        m, driver = _mouth()
        m.update(talking=True)
        for _ in range(10):
            m.update(level=level)
            m.tick()
        return m.shown
    assert height_at(20) < height_at(50) < height_at(90)


def test_levels_are_ignored_when_not_talking():
    m, driver = _mouth()
    m.update(level=80)
    assert not m.tick()
    assert m.shown == 0


def test_wiggles_by_itself_with_no_levels():
    m, driver = _mouth()
    m.update(talking=True)
    shown = []
    for _ in range(40):
        assert m.tick()
        shown.append(m.shown)
    assert max(shown) > 0.3


def test_falls_back_to_wiggling_when_levels_stop():
    m, driver = _mouth(seed=5)
    m.update(talking=True)
    m.update(level=0)  # silence, freshly sent: stays near flat
    for _ in range(LEVEL_TIMEOUT_TICKS - 1):
        m.tick()
    assert m.shown < 0.01
    for _ in range(30):  # host went quiet without sending S0
        m.tick()
    assert m.shown > 0.1


def test_stopping_settles_to_flat_then_stops_redrawing():
    m, driver = _mouth()
    m.update(talking=True)
    for _ in range(5):
        m.update(level=100)
        m.tick()
    m.update(talking=False)
    ticks = 0
    while m.tick():
        ticks += 1
        assert ticks < 30
    assert ticks > 1  # eases down, not snapped flat
    assert {y for _, y in driver.dots()} == {CENTER_Y}
    assert not m.tick()


def test_firmware_imports_nothing_pico_only():
    for name in ("mouth", "mouth_geometry", "mouth_protocol"):
        with open(os.path.join(os.path.dirname(mouth.__file__), name + ".py")) as f:
            source = f.read()
        assert "import machine" not in source and "from machine" not in source
