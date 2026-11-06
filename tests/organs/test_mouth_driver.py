import random

import pytest

from organs.mouth.driver import MouthOrgan
from organs.mouth.virtual import MouthPanel


class FakeTransport:
    def __init__(self):
        self.sent = []

    def connect(self):
        pass

    def write(self, data):
        self.sent.append(data)

    def close(self):
        pass


class RecordingDriver:
    def __init__(self):
        self.shows = 0

    def fill(self, color):
        pass

    def fill_circle(self, cx, cy, r, color):
        pass

    def fill_polygon(self, points, color):
        pass

    def show(self):
        self.shows += 1


@pytest.fixture
def mouth():
    return MouthOrgan(FakeTransport())


def test_talking_on_and_off(mouth):
    mouth.start_talking()
    mouth.stop_talking()
    assert mouth.transport.sent == [b"S1\n", b"S0\n"]


def test_level_is_0_to_1_on_the_host_and_0_to_100_on_the_wire(mouth):
    mouth.level(0.57)
    mouth.level(1.7)
    assert mouth.transport.sent == [b"L57\n", b"L100\n"]


def test_both_in_one_line(mouth):
    mouth.update(talking=True, level=0.4)
    assert mouth.transport.sent == [b"S1 L40\n"]


def test_bus_commands(mouth):
    mouth.send_command("talking", {"on": True})
    mouth.send_command("level", {"level": 0.2})
    mouth.send_command("update", {"talking": False})
    assert mouth.transport.sent == [b"S1\n", b"L20\n", b"S0\n"]
    with pytest.raises(ValueError):
        mouth.send_command("smile", {})


def test_driver_into_the_virtual_panel_end_to_end():
    driver = RecordingDriver()
    panel = MouthPanel(driver, rand=random.Random(1).random)
    mouth = MouthOrgan(panel)
    assert not panel.tick()                    # quiet: no redraw
    mouth.update(talking=True, level=0.8)
    assert panel.tick() and panel.tick()       # talking: every frame
    assert panel.mouth.shown > 0.5
    mouth.stop_talking()
    while panel.tick():
        pass
    assert panel.mouth.shown == 0


def test_panel_takes_bytes_in_any_chunks():
    panel = MouthPanel(RecordingDriver())
    for chunk in (b"S", b"1 L4", b"0\r", b"\n"):
        panel.write(chunk)
    assert panel.mouth.talking and panel.mouth.level == 0.4


def test_panel_redraw_repaints_without_changing_state():
    driver = RecordingDriver()
    panel = MouthPanel(driver)
    shows = driver.shows
    panel.redraw()
    assert driver.shows == shows + 1
    assert not panel.mouth.talking
