import pytest

from organs.eyes.driver import EyesOrgan
from organs.eyes.virtual import EyesPanel


class RecordingDriver:
    """Counts what one eye's screen was asked to draw."""

    WIDTH = HEIGHT = 240

    def __init__(self):
        self.fills = []
        self.shapes = 0

    def fill(self, color):
        self.fills.append(color)

    def fill_circle(self, cx, cy, r, color):
        self.shapes += 1

    def fill_polygon(self, points, color):
        self.shapes += 1


@pytest.fixture
def setup():
    left, right = RecordingDriver(), RecordingDriver()
    panel = EyesPanel(left, right)
    return panel, EyesOrgan(panel), left, right


def test_two_screens_side_by_side():
    (x0, y0, w0, h0), (x1, y1, w1, h1) = EyesPanel.SCREENS
    assert (w0, h0) == (w1, h1) == (240, 240)
    assert x1 >= x0 + w0 and y0 == y1


def test_driver_bytes_reach_the_face(setup):
    panel, eyes, left, right = setup
    eyes.update(expression="happy", intensity=3, direction=(-0.4, 0.25))
    for eye in panel.face.eyes:
        assert (eye.expression, eye.intensity) == ("happy", 3)
        assert (eye.dx, eye.dy) == pytest.approx((-0.4, 0.25))
    assert left.shapes and right.shapes


def test_right_eye_is_mirrored_left_is_not(setup):
    panel, *_ = setup
    assert [eye.mirror for eye in panel.face.eyes] == [False, True]


def test_a_command_split_across_writes_still_arrives(setup):
    panel, *_ = setup
    panel.write(b"Esad")
    assert panel.face.left.expression is None
    panel.write(b":2\n")
    assert panel.face.left.expression == "sad"


def test_junk_lines_are_ignored(setup):
    panel, *_ = setup
    panel.write(b"\x00\xff nonsense ### \n" + b"X" * 500 + b"\n")
    assert panel.face.left.expression is None


def test_blink_stays_shut_for_a_full_tick_then_reopens(setup):
    panel, eyes, left, _right = setup
    eyes.blink()
    assert panel.face._blinking
    panel.tick()             # held, as main.py restarts its tick clock
    assert panel.face._blinking
    panel.tick()
    assert not panel.face._blinking


def test_idle_off_freezes_but_still_reopens_a_blink(setup, monkeypatch):
    panel, eyes, *_ = setup
    panel.idle = False
    called = []
    monkeypatch.setattr(panel.face, "tick", lambda: called.append(1))
    eyes.blink()
    panel.tick()
    panel.tick()
    assert not called and not panel.face._blinking


def test_redraw_paints_both_eyes(setup):
    panel, _eyes, left, right = setup
    before = len(left.fills), len(right.fills)
    panel.redraw()
    assert len(left.fills) > before[0] and len(right.fills) > before[1]
