import pytest
from nervous_system.bus import NervousSystem
from organs.base import MockOrgan


def test_send_routes_to_registered_organ():
    bus = NervousSystem()
    eyes = MockOrgan("eyes")
    bus.register("eyes", eyes)

    bus.send("eyes", "blink")

    assert eyes.calls == [("blink", {})]


def test_send_passes_payload():
    bus = NervousSystem()
    eyes = MockOrgan("eyes")
    bus.register("eyes", eyes)

    bus.send("eyes", "look", direction="left")

    assert eyes.calls == [("look", {"direction": "left"})]


def test_send_to_unregistered_organ_raises():
    bus = NervousSystem()

    with pytest.raises(KeyError):
        bus.send("ears", "listen")
