from brain.limbic.mood import Mood
from nervous_system.bus import NervousSystem
from nervous_system.router import RobotRouter, RouterSettings, bearing_to_eye_direction
from organs.base import MockOrgan


class Clock:
    def __init__(self):
        self.now = 0.0

    def __call__(self):
        return self.now

    def advance(self, seconds):
        self.now += seconds


def make_router(**settings):
    clock = Clock()
    bus = NervousSystem()
    eyes = MockOrgan("eyes")
    bus.register("eyes", eyes)
    router = RobotRouter(bus, RouterSettings(smoothing=1, resend_seconds=10, **settings), clock=clock)
    return router, eyes, clock


def test_bearing_maps_full_circle_and_clamps_behind():
    assert bearing_to_eye_direction(0) == (0.0, 0.0)
    assert bearing_to_eye_direction(45) == (0.5, 0.0)
    assert bearing_to_eye_direction(90) == (1.0, 0.0)
    assert bearing_to_eye_direction(180) == (1.0, 0.0)
    assert bearing_to_eye_direction(270) == (-1.0, 0.0)


def test_direction_is_independent_of_mood_and_is_sent_as_one_eye_update():
    router, eyes, _ = make_router()
    router.set_mood(Mood("scared", 2))
    router.hear_direction(45, confidence=0.9)
    router.tick()
    assert eyes.calls == [("update", {"expression": "scared", "intensity": 2, "direction": (0.5, 0.0)})]


def test_direction_moves_smoothly_towards_the_voice():
    clock = Clock()
    bus = NervousSystem()
    eyes = MockOrgan("eyes")
    bus.register("eyes", eyes)
    router = RobotRouter(bus, RouterSettings(smoothing=0.5), clock=clock)
    router.hear_direction(90)

    router.tick()
    router.tick()

    assert [call[1]["direction"] for call in eyes.calls] == [(0.5, 0.0), (0.75, 0.0)]


def test_low_confidence_is_ignored_but_confident_bearing_is_available_to_brain():
    router, eyes, _ = make_router(confidence_threshold=0.7)
    router.hear_direction(90, confidence=0.69)
    router.tick()
    assert router.last_voice_bearing is None
    assert eyes.calls[0][1]["direction"] == (0.0, 0.0)
    router.hear_direction(270, confidence=0.7)
    assert router.last_voice_bearing == 270


def test_hysteresis_extends_hold_without_jittering_target():
    router, eyes, clock = make_router(bearing_hysteresis_degrees=10)
    router.hear_direction(50)
    router.tick()
    clock.advance(0.7)
    router.hear_direction(56)  # Same speaker, but refreshes the hold.
    clock.advance(0.2)
    router.tick()
    assert eyes.calls[-1][1]["direction"] == (50 / 90, 0.0)


def test_direction_holds_then_returns_to_centre_and_is_muted_while_speaking():
    router, eyes, clock = make_router(hold_seconds=1)
    router.hear_direction(90)
    router.tick()
    clock.advance(1.01)
    router.tick()
    assert eyes.calls[-1][1]["direction"] == (0.0, 0.0)
    router.hear_direction(270)
    router.set_speaking(True)
    router.tick()
    assert eyes.calls[-1][1]["direction"] == (0.0, 0.0)


def test_own_voice_while_speaking_does_not_replace_last_voice_bearing():
    router, _, _ = make_router()
    router.hear_direction(30, confidence=0.9)
    router.set_speaking(True)
    router.hear_direction(0, confidence=0.95)  # Qbot's own speaker.
    assert router.last_voice_bearing == 30


def test_state_is_resent_periodically_and_an_unplugged_organ_does_not_crash_router():
    router, eyes, clock = make_router()
    router.tick()
    clock.advance(10)
    router.tick()
    assert len(eyes.calls) == 2

    class BrokenBus:
        def has_organ(self, name):
            return True

        def send(self, *args, **kwargs):
            raise OSError("Pico unplugged")

    RobotRouter(BrokenBus()).tick()
