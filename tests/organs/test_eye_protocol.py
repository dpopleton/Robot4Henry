import pytest

from brain.limbic import mood
from organs.eyes.firmware.eye_protocol import (
    MAX_INTENSITY, MIN_INTENSITY, Update, encode, parse,
)


def test_intensity_range_matches_mood():
    assert (MIN_INTENSITY, MAX_INTENSITY) == (mood.MIN_INTENSITY, mood.MAX_INTENSITY)


@pytest.mark.parametrize("kwargs", [
    {"direction": (-0.4, 0.25)},
    {"expression": "happy", "intensity": 3},
    {"expression": "happy"},
    {"expression": "angry", "intensity": 1, "direction": (1.0, -1.0), "blink": True},
    {"blink": True},
])
def test_round_trip(kwargs):
    update = parse(encode(**kwargs).decode())
    assert update.expression == kwargs.get("expression")
    assert update.intensity == kwargs.get("intensity")
    assert update.direction == kwargs.get("direction")
    assert update.blink == kwargs.get("blink", False)


def test_direction_line_is_tiny():
    assert len(encode(direction=(-1, -1))) <= 11  # worst case: "D-100,-100\n"


def test_encode_clamps():
    assert encode(direction=(5, -5), expression="sad", intensity=9) == b"Esad:3 D100,-100\n"


def test_encode_rejects_empty_and_bad_names():
    with pytest.raises(ValueError):
        encode()
    with pytest.raises(ValueError):
        encode(expression="two words")


def test_later_lines_win_when_merged():
    update = Update()
    for line in ("D10,10", "Ehappy:1", "D-20,30", "Esad:3"):
        update.merge_line(line)
    assert update.direction == (-0.2, 0.3)
    assert (update.expression, update.intensity) == ("sad", 3)


def test_direction_only_line_leaves_expression_unchanged():
    update = parse("D0,0")
    assert update.expression is None and update.intensity is None


@pytest.mark.parametrize("line", ["", "   ", "Dxx", "D1", "E", "E:3", "Zfoo", "Ehappy:x"])
def test_garbage_is_ignored_not_fatal(line):
    parse(line)  # must not raise


def test_garbage_field_does_not_spoil_good_ones():
    update = parse("Dnope Ehappy:2")
    assert update.direction is None
    assert update.expression == "happy"
