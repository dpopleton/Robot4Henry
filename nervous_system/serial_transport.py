"""
USB serial transport — one Pico per port. Requires pyserial
(install the "hardware" extra: pip install -e ".[hardware]").
"""

from nervous_system.protocol import Message

PICO_USB_VENDOR_ID = 0x2E8A  # Raspberry Pi — every Pico reports this over USB


def list_pico_ports() -> list[str]:
    """Serial ports that look like a Pico, best guess first: anything
    with the Raspberry Pi vendor ID, then other USB serial ports
    (ttyACM/ttyUSB on Linux, COM on Windows). Empty if pyserial is missing."""
    try:
        from serial.tools import list_ports
    except ImportError:
        return []
    picos, others = [], []
    for port in sorted(list_ports.comports(), key=lambda p: p.device):
        if port.vid == PICO_USB_VENDOR_ID:
            picos.append(port.device)
        elif port.vid is not None:
            others.append(port.device)
    return picos + others


class SerialTransport:
    def __init__(self, port: str, baudrate: int = 115200, timeout: float = 1.0):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self._serial = None

    def connect(self):
        import serial
        self._serial = serial.Serial(
            self.port, self.baudrate, timeout=self.timeout
        )

    def send(self, message: Message):
        if not self._serial:
            raise RuntimeError(f"Not connected to {self.port} — call connect() first.")
        self._serial.write(message.encode())

    def write(self, data: bytes):
        """Send pre-encoded bytes as-is — for organs with their own
        compact wire format (e.g. organs/eyes) instead of JSON Messages."""
        if not self._serial:
            raise RuntimeError(f"Not connected to {self.port} — call connect() first.")
        self._serial.write(data)

    def receive(self) -> Message | None:
        """Read one line and decode it. Returns None on timeout/empty read."""
        if not self._serial:
            raise RuntimeError(f"Not connected to {self.port} — call connect() first.")
        line = self._serial.readline()
        if not line:
            return None
        return Message.decode(line)

    def close(self):
        if self._serial:
            self._serial.close()
            self._serial = None
