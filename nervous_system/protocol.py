"""
Wire format shared by every organ, on both sides of the link (host driver
and Pico firmware). One message per line, so it stays readable straight
off a serial terminal:

    {"organ": "eyes", "cmd": "blink", "payload": {}}
"""

import json
from dataclasses import dataclass, field


@dataclass
class Message:
    organ: str
    cmd: str
    payload: dict = field(default_factory=dict)

    def encode(self) -> bytes:
        """Serialize to a single newline-terminated line."""
        line = json.dumps({
            "organ": self.organ,
            "cmd": self.cmd,
            "payload": self.payload,
        })
        return (line + "\n").encode("utf-8")

    @classmethod
    def decode(cls, line: bytes | str) -> "Message":
        if isinstance(line, bytes):
            line = line.decode("utf-8")
        data = json.loads(line.strip())
        return cls(
            organ=data["organ"],
            cmd=data["cmd"],
            payload=data.get("payload", {}),
        )
