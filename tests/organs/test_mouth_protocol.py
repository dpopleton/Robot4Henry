import pytest

from organs.mouth.firmware.mouth_protocol import encode, parse


@pytest.mark.parametrize("kwargs", [
    {"talking": True},
    {"talking": False},
    {"level": 57},
    {"talking": True, "level": 0},
    {"level": 100},
])
def test_round_trip(kwargs):
    update = parse(encode(**kwargs).decode())
    assert update.talking == kwargs.get("talking")
    assert update.level == kwargs.get("level")


def test_level_line_is_tiny():
    assert len(encode(level=100)) <= 5  # "L100\n" — sent ~25 times a second


def test_encode_clamps_and_rounds():
    assert encode(level=150) == b"L100\n"
    assert encode(level=-3) == b"L0\n"
    assert encode(level=41.6) == b"L42\n"


def test_encode_needs_something():
    with pytest.raises(ValueError):
        encode()


def test_later_lines_win():
    update = parse("S1 L10")
    update.merge_line("L80")
    update.merge_line("S0")
    assert (update.talking, update.level) == (False, 80)


@pytest.mark.parametrize("line", ["", "S2", "Lloud", "L", "S", "X1", "Ehappy:2", "V"])
def test_unknown_or_malformed_fields_are_skipped(line):
    assert parse(line).is_empty()


def test_one_bad_field_doesnt_spoil_the_rest():
    update = parse("Lloud S1 L30")
    assert (update.talking, update.level) == (True, 30)
