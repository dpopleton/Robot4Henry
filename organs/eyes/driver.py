"""
Host-side driver for the eyes organ (LCD screens on a Raspberry Pi
Pico). Translates high-level expression calls into nervous_system
protocol messages and sends them over a serial transport.
"""

from nervous_system.protocol import Message
from organs.base import Organ


class EyesOrgan(Organ):
    def __init__(self, transport):
        """transport: anything with connect()/send()/close(), e.g.
        nervous_system.serial_transport.SerialTransport."""
        self.transport = transport

    def connect(self):
        self.transport.connect()

    def send_command(self, cmd: str, payload: dict):
        self.transport.send(Message(organ="eyes", cmd=cmd, payload=payload))

    def close(self):
        self.transport.close()

    # Convenience methods the brain actually calls.
    def blink(self):
        self.send_command("blink", {})

    def look(self, direction: str):
        self.send_command("look", {"direction": direction})

    def set_expression(self, mood: str):
        self.send_command("set_expression", {"mood": mood})
