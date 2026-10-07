"""
Host-side driver for the eyes organ (LCD screens on a Raspberry Pi
Pico). Translates high-level calls into the eyes' compact line format
(organs/eyes/firmware/eye_protocol.py — the same module the Pico parses
with) and writes it to a serial transport.

The eyes run on two inputs, sendable independently or together:
  - direction: (dx, dy), each in [-1, 1], as seen by someone facing the
    robot — +dx is screen-right, +dy is down;
  - expression: a name from firmware/expressions.py's REGISTRY (every
    brain/limbic/mood.py category is one) plus intensity 1-3.
"""

from organs.base import Organ
from organs.eyes.firmware.eye_protocol import encode

NAMED_DIRECTIONS = {
    "center": (0.0, 0.0),
    "left": (-1.0, 0.0),
    "right": (1.0, 0.0),
    "up": (0.0, -1.0),
    "down": (0.0, 1.0),
    "up_left": (-0.7, -0.7),
    "up_right": (0.7, -0.7),
    "down_left": (-0.7, 0.7),
    "down_right": (0.7, 0.7),
}


def _direction(direction):
    if isinstance(direction, str):
        try:
            return NAMED_DIRECTIONS[direction]
        except KeyError:
            raise ValueError(f"Unknown direction {direction!r} — use one of {sorted(NAMED_DIRECTIONS)} or (dx, dy)")
    dx, dy = direction
    return float(dx), float(dy)


class EyesOrgan(Organ):
    def __init__(self, transport):
        """transport: anything with connect()/write(bytes)/close(), e.g.
        nervous_system.serial_transport.SerialTransport."""
        self.transport = transport

    def connect(self):
        self.transport.connect()

    def close(self):
        self.transport.close()

    def update(self, expression: str = None, intensity: int = None, direction=None, blink: bool = False):
        """Send any combination in one line — the Pico applies it as a
        single redraw. direction: (dx, dy) or a NAMED_DIRECTIONS key."""
        self.transport.write(encode(
            expression=expression,
            intensity=intensity,
            direction=None if direction is None else _direction(direction),
            blink=blink,
        ))

    def send_command(self, cmd: str, payload: dict):
        """Bus entry point (nervous_system.NervousSystem.send)."""
        if cmd == "blink":
            self.blink()
        elif cmd == "look":
            self.look(payload["direction"])
        elif cmd == "set_expression":
            self.set_expression(payload.get("expression", payload.get("mood")), payload.get("intensity"))
        elif cmd == "update":
            self.update(**payload)
        else:
            raise ValueError(f"Unknown eyes command {cmd!r}")

    # Convenience methods the brain actually calls.
    def blink(self):
        self.update(blink=True)

    def look(self, direction):
        self.update(direction=direction)

    def set_expression(self, expression: str, intensity: int = None):
        self.update(expression=expression or "neutral", intensity=intensity)

    def show_mood(self, mood, direction=None):
        """mood: a brain.limbic.mood.Mood — its category is the
        expression name, its intensity the intensity."""
        self.update(expression=mood.category, intensity=mood.intensity, direction=direction)
