import pytest

from brain.limbic.mood import Mood
from organs.eyes.driver import EyesOrgan


class FakeTransport:
    def __init__(self):
        self.sent = []
        self.connected = False

    def connect(self):
        self.connected = True

    def write(self, data):
        self.sent.append(data)

    def close(self):
        self.connected = False


@pytest.fixture
def eyes():
    return EyesOrgan(FakeTransport())


def test_blink(eyes):
    eyes.blink()
    assert eyes.transport.sent == [b"B\n"]


def test_look_with_vector(eyes):
    eyes.look((-0.4, 0.25))
    assert eyes.transport.sent == [b"D-40,25\n"]


def test_look_with_named_direction(eyes):
    eyes.look("left")
    assert eyes.transport.sent == [b"D-100,0\n"]


def test_unknown_named_direction_raises(eyes):
    with pytest.raises(ValueError):
        eyes.look("sideways")


def test_set_expression_with_intensity(eyes):
    eyes.set_expression("curious", 3)
    assert eyes.transport.sent == [b"Ecurious:3\n"]


def test_set_expression_none_is_neutral(eyes):
    eyes.set_expression(None)
    assert eyes.transport.sent == [b"Eneutral\n"]


def test_show_mood_sends_category_and_intensity_with_direction_in_one_line(eyes):
    eyes.show_mood(Mood("scared", 2), direction=(1, 0))
    assert eyes.transport.sent == [b"Escared:2 D100,0\n"]


def test_bus_commands_map_onto_the_compact_format(eyes):
    eyes.send_command("set_expression", {"mood": "happy", "intensity": 1})
    eyes.send_command("look", {"direction": "up"})
    eyes.send_command("update", {"expression": "sad", "direction": (0, 0.5)})
    assert eyes.transport.sent == [b"Ehappy:1\n", b"D0,-100\n", b"Esad D0,50\n"]


def test_unknown_bus_command_raises(eyes):
    with pytest.raises(ValueError):
        eyes.send_command("wiggle", {})
