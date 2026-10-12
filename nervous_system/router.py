"""The real-time bridge between Qbot's inputs and face organs.

``RobotRouter`` owns the small, fast-changing bit of robot behaviour: where
the eyes look and which expression they show.  It deliberately has no LLM
dependency.  A direction finder can call :meth:`hear_direction` as often as
it likes while a separate chat thread is waiting for a reply.

``RouterProcess`` is the long-lived thread used by the application.  Keeping
the state machine separately tickable makes its timing behaviour testable and
also leaves open moving it into a separate OS process later.
"""

from __future__ import annotations

import math
import threading
import time
from dataclasses import dataclass
from typing import Callable

from brain.limbic.mood import Mood


@dataclass(frozen=True)
class RouterSettings:
    """Tuning values for direction reflexes.

    Bearings are clockwise degrees from straight ahead: 90 is Qbot's right,
    270 is Qbot's left.  An exactly-behind source (180) is deliberately sent
    to the right-hand limit; callers which can distinguish sides should emit
    a bearing just below or above 180.
    """

    confidence_threshold: float = 0.60
    bearing_hysteresis_degrees: float = 4.0
    hold_seconds: float = 0.75
    smoothing: float = 0.35
    resend_seconds: float = 3.0


def bearing_to_eye_direction(bearing: float) -> tuple[float, float]:
    """Map a 360-degree compass bearing to the eyes' +/- 90-degree range."""
    if not math.isfinite(bearing):
        raise ValueError("bearing must be finite")
    bearing = bearing % 360
    signed = bearing if bearing <= 180 else bearing - 360
    return (max(-1.0, min(1.0, signed / 90.0)), 0.0)


def _angular_distance(first: float, second: float) -> float:
    return abs((first - second + 180) % 360 - 180)


class RobotRouter:
    """State machine that maps moods and voice direction onto organ commands.

    The nervous system is intentionally injected.  Missing organs and failed
    sends are ignored: the next tick retries the complete current state, so a
    Pico can be unplugged or rebooted without taking the conversation down.
    """

    def __init__(
        self,
        nervous_system,
        settings: RouterSettings | None = None,
        *,
        clock: Callable[[], float] = time.monotonic,
    ):
        self.nervous_system = nervous_system
        self.settings = settings or RouterSettings()
        if not 0 < self.settings.smoothing <= 1:
            raise ValueError("smoothing must be in (0, 1]")
        self._clock = clock
        self._lock = threading.RLock()
        self._mood = Mood()
        self._speaking = False
        self._accepted_bearing: float | None = None
        self._accepted_at: float | None = None
        self._last_voice_bearing: float | None = None
        self._direction = (0.0, 0.0)
        self._last_sent: tuple[str, int, tuple[float, float]] | None = None
        self._last_sent_at: float | None = None

    @property
    def last_voice_bearing(self) -> float | None:
        """Most recent confident voice bearing, for cognition to ask about."""
        with self._lock:
            return self._last_voice_bearing

    def set_mood(self, mood: Mood | str, intensity: int | None = None) -> None:
        """Accept a brain mood without sending hardware commands inline."""
        if not isinstance(mood, Mood):
            mood = Mood(mood, 1 if intensity is None else intensity)
        with self._lock:
            self._mood = mood

    def set_speaking(self, speaking: bool) -> None:
        """Mute direction reflexes while Qbot's own voice is playing."""
        with self._lock:
            self._speaking = bool(speaking)
            if speaking:
                # Do not snap the screen, but ensure the next tick heads home.
                self._accepted_bearing = None
                self._accepted_at = None

    def hear_direction(self, bearing: float, confidence: float = 1.0) -> None:
        """Offer one crown direction estimate (clockwise degrees from front)."""
        if not math.isfinite(bearing) or not math.isfinite(confidence):
            return
        bearing %= 360
        if confidence < self.settings.confidence_threshold:
            return
        now = self._clock()
        with self._lock:
            if self._speaking:
                # Probably Qbot's own voice: don't look at it or remember it.
                return
            self._last_voice_bearing = bearing
            if (self._accepted_bearing is not None and
                    _angular_distance(bearing, self._accepted_bearing) < self.settings.bearing_hysteresis_degrees):
                # It still counts as hearing the same speaker: extend the hold.
                self._accepted_at = now
                return
            self._accepted_bearing = bearing
            self._accepted_at = now

    def tick(self) -> None:
        """Advance the reflex once and send an eye update when needed."""
        with self._lock:
            now = self._clock()
            target = (0.0, 0.0)
            if (not self._speaking and self._accepted_bearing is not None and
                    self._accepted_at is not None and
                    now - self._accepted_at <= self.settings.hold_seconds):
                target = bearing_to_eye_direction(self._accepted_bearing)
            self._direction = tuple(
                current + (wanted - current) * self.settings.smoothing
                for current, wanted in zip(self._direction, target)
            )
            # Avoid a never-ending tail of tiny floating-point changes.
            self._direction = tuple(0.0 if abs(value) < 0.001 else value for value in self._direction)
            state = (self._mood.category, self._mood.intensity, self._direction)
            due = self._last_sent_at is None or now - self._last_sent_at >= self.settings.resend_seconds
            changed = self._last_sent is None or state != self._last_sent
            if not changed and not due:
                return

        # Never hold the state lock while a serial driver may block.
        try:
            if not self.nervous_system.has_organ("eyes"):
                return
            self.nervous_system.send(
                "eyes", "update", expression=state[0], intensity=state[1], direction=state[2]
            )
        except Exception:
            # Hardware failures are expected operational events.  Leave
            # _last_sent untouched so a later tick reconnects/re-synchronises.
            return

        with self._lock:
            self._last_sent = state
            self._last_sent_at = now


class RouterProcess:
    """Runs a :class:`RobotRouter` regularly, independently of ``chat()``."""

    def __init__(self, router: RobotRouter, tick_seconds: float = 0.05):
        if tick_seconds <= 0:
            raise ValueError("tick_seconds must be positive")
        self.router = router
        self.tick_seconds = tick_seconds
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None

    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            return
        self._stop.clear()
        self._thread = threading.Thread(target=self._run, name="qbot-router", daemon=True)
        self._thread.start()

    def close(self, timeout: float | None = 1.0) -> None:
        self._stop.set()
        if self._thread:
            self._thread.join(timeout)

    def _run(self) -> None:
        while not self._stop.is_set():
            self.router.tick()
            self._stop.wait(self.tick_seconds)
