"""
Host-side driver for the mouth organ (a 2" screen on its own Pico).
Translates calls into the mouth's line format
(organs/mouth/firmware/mouth_protocol.py — the same module the Pico parses
with) and writes it to a transport: a real Pico (SerialTransport), the
virtual panel (organs/mouth/virtual.py), or the virtual robot's switch
between the two.

  - talking on/off: the line becomes a seismograph, then settles flat;
  - level: how loud the voice is right now, 0.0-1.0, sent about 25 times
    a second while talking (D-024). Without levels the mouth wiggles by itself.
"""

from organs.base import Organ
from organs.mouth.firmware.mouth_protocol import MAX_LEVEL, encode


class MouthOrgan(Organ):
    def __init__(self, transport):
        """transport: anything with connect()/write(bytes)/close()."""
        self.transport = transport

    def connect(self):
        self.transport.connect()

    def close(self):
        self.transport.close()

    def update(self, talking: bool = None, level: float = None):
        """Send either or both in one line. level: 0.0-1.0 (clamped)."""
        self.transport.write(encode(
            talking=talking,
            level=None if level is None else level * MAX_LEVEL,
        ))

    def start_talking(self):
        self.update(talking=True)

    def stop_talking(self):
        self.update(talking=False)

    def level(self, level: float):
        self.update(level=level)

    def send_command(self, cmd: str, payload: dict):
        """Bus entry point (nervous_system.NervousSystem.send)."""
        if cmd == "talking":
            self.update(talking=bool(payload["on"]))
        elif cmd == "level":
            self.level(payload["level"])
        elif cmd == "update":
            self.update(**payload)
        else:
            raise ValueError(f"Unknown mouth command {cmd!r}")
