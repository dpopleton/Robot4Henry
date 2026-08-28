"""
Every organ driver — real or mock — implements this so the nervous
system (and the brain, through it) can treat all organs the same way.
"""

from abc import ABC, abstractmethod


class Organ(ABC):
    @abstractmethod
    def connect(self):
        """Open the transport (e.g. the serial port) to the physical organ."""

    @abstractmethod
    def send_command(self, cmd: str, payload: dict):
        """Send one command to the organ."""

    @abstractmethod
    def close(self):
        """Release the transport."""


class MockOrgan(Organ):
    """Stand-in for hardware that isn't built yet, or isn't plugged in.
    Records every command it receives so tests/dev runs can assert on it."""

    def __init__(self, name: str):
        self.name = name
        self.calls = []
        self.connected = False

    def connect(self):
        self.connected = True

    def send_command(self, cmd: str, payload: dict):
        self.calls.append((cmd, payload))
        return {"organ": self.name, "cmd": cmd, "status": "mocked"}

    def close(self):
        self.connected = False
