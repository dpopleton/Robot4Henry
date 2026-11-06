import pytest

from virtual_robot.link import OrganLink


class FakePanel:
    def __init__(self):
        self.got = []

    def write(self, data):
        self.got.append(data)


class FakeSerial:
    def __init__(self, port, output=b""):
        self.port = port
        self.sent = []
        self.closed = False
        self.output = output
        self.unplugged = False

    def write(self, data):
        if self.unplugged:
            raise OSError("device disconnected")
        self.sent.append(data)

    def read_available(self):
        out, self.output = self.output, b""
        return out

    def close(self):
        self.closed = True


@pytest.fixture
def link():
    opened = []

    def open_serial(port):
        if port == "/dev/missing":
            raise OSError("no such port")
        opened.append(FakeSerial(port))
        return opened[-1]

    link = OrganLink(FakePanel(), open_serial)
    link.opened = opened
    return link


def test_starts_virtual_and_only_feeds_the_panel(link):
    link.write(b"S1\n")
    assert link.mode == "virtual"
    assert link.panel.got == [b"S1\n"]
    assert link.opened == []


@pytest.mark.parametrize("mode, to_panel, to_pico", [
    ("off", False, False),
    ("virtual", True, False),
    ("real", True, True),     # the panel follows out of sight, so switching back is right
    ("both", True, True),
])
def test_each_mode_routes_writes(link, mode, to_panel, to_pico):
    link.set_mode(mode, "/dev/ttyACM0")
    link.write(b"L50\n")
    assert (link.panel.got == [b"L50\n"]) == to_panel
    assert bool(link.opened and link.opened[-1].sent == [b"L50\n"]) == to_pico


def test_leaving_the_pico_closes_it(link):
    link.set_mode("both", "/dev/ttyACM0")
    link.set_mode("virtual")
    assert link.opened[0].closed
    assert link.port is None


def test_switching_between_real_and_both_keeps_one_connection(link):
    link.set_mode("real", "/dev/ttyACM0")
    link.set_mode("both", "/dev/ttyACM0")
    assert len(link.opened) == 1


def test_a_new_port_reopens(link):
    link.set_mode("real", "/dev/ttyACM0")
    link.set_mode("real", "/dev/ttyACM1")
    assert link.opened[0].closed and link.opened[1].port == "/dev/ttyACM1"


def test_failing_to_open_leaves_the_mode_alone(link):
    with pytest.raises(OSError):
        link.set_mode("both", "/dev/missing")
    assert link.mode == "virtual"
    link.write(b"S1\n")
    assert link.panel.got == [b"S1\n"]


def test_unknown_mode_raises(link):
    with pytest.raises(ValueError):
        link.set_mode("sideways")


def test_unplugged_pico_raises_after_the_panel_got_it(link):
    link.set_mode("both", "/dev/ttyACM0")
    link.opened[0].unplugged = True
    with pytest.raises(OSError):
        link.write(b"S1\n")
    assert link.panel.got == [b"S1\n"]
    link.drop_pico()
    assert link.mode == "virtual" and link.opened[0].closed


def test_crash_watch_only_while_on_the_pico(link):
    assert link.poll_crash() is None
    link.set_mode("real", "/dev/ttyACM0")
    link.opened[0].output = b"Traceback (most recent call last):\r\nValueError: boom\r\n>>> "
    summary, _ = link.poll_crash()
    assert summary == "ValueError: boom"
