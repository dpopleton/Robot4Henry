from types import SimpleNamespace

from serial.tools import list_ports

from nervous_system.serial_transport import list_pico_ports


def test_picos_first_then_other_usb_ports(monkeypatch):
    ports = [
        SimpleNamespace(device="/dev/ttyUSB0", vid=0x1A86),   # some other USB serial adapter
        SimpleNamespace(device="/dev/ttyS0", vid=None),       # built-in serial, never a Pico
        SimpleNamespace(device="/dev/ttyACM1", vid=0x2E8A),   # a Pico
    ]
    monkeypatch.setattr(list_ports, "comports", lambda: ports)
    assert list_pico_ports() == ["/dev/ttyACM1", "/dev/ttyUSB0"]
