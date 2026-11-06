import json
import pytest
import warnings

from nervous_system.protocol import Message
from nervous_system.serial_transport import SerialTransport
from config.settings import _serial_by_id_setting


def test_message_encode_newline_terminated_json():
    msg = Message(organ="eyes", cmd="blink", payload={"speed": 1})
    encoded = msg.encode()
    assert encoded.endswith(b"\n")
    decoded_dict = json.loads(encoded.decode("utf-8").strip())
    assert decoded_dict == {"organ": "eyes", "cmd": "blink", "payload": {"speed": 1}}


def test_message_decode_from_bytes():
    line = b'{"organ": "mouth", "cmd": "talk", "payload": {"viseme": "O"}}\n'
    msg = Message.decode(line)
    assert msg.organ == "mouth"
    assert msg.cmd == "talk"
    assert msg.payload == {"viseme": "O"}


def test_message_decode_from_str():
    line = '{"organ": "lights", "cmd": "set_color", "payload": {"rgb": [255, 0, 0]}}'
    msg = Message.decode(line)
    assert msg.organ == "lights"
    assert msg.cmd == "set_color"
    assert msg.payload == {"rgb": [255, 0, 0]}


def test_message_decode_default_payload():
    line = '{"organ": "eyes", "cmd": "blink"}'
    msg = Message.decode(line)
    assert msg.payload == {}


def test_message_decode_invalid_json_raises():
    with pytest.raises(json.JSONDecodeError):
        Message.decode(b"not json\n")


def test_serial_transport_operations_with_fake_serial():
    class FakeSerial:
        def __init__(self):
            self.written = []
            self.read_queue = []
            self.closed = False

        def write(self, data):
            self.written.append(data)

        def readline(self):
            return self.read_queue.pop(0) if self.read_queue else b""

        @property
        def in_waiting(self):
            return len(self.read_queue[0]) if self.read_queue else 0

        def read(self, size):
            assert size == len(self.read_queue[0])
            return self.read_queue.pop(0)

        def close(self):
            self.closed = True

    transport = SerialTransport(port="/dev/test", baudrate=115200)
    fake = FakeSerial()
    transport._serial = fake

    # send() Message
    msg = Message(organ="eyes", cmd="look", payload={"dx": 1.0})
    transport.send(msg)
    assert len(fake.written) == 1
    assert b'"look"' in fake.written[0]

    # write() raw bytes
    transport.write(b"D50,50\n")
    assert fake.written[-1] == b"D50,50\n"

    # receive() valid message
    fake.read_queue.append(b'{"organ": "eyes", "cmd": "ack", "payload": {}}\n')
    rec = transport.receive()
    assert rec is not None
    assert rec.organ == "eyes"
    assert rec.cmd == "ack"

    # receive() timeout/empty line
    assert transport.receive() is None

    # receive() line noise (corrupt JSON)
    fake.read_queue.append(b"\xff\xfe garbage line noise\n")
    assert transport.receive() is None

    # read_available(): never blocks
    assert transport.read_available() == b""
    fake.read_queue.append(b"Traceback ...\r\n>>> ")
    assert transport.read_available() == b"Traceback ...\r\n>>> "

    # close()
    transport.close()
    assert fake.closed
    assert transport._serial is None


def test_serial_transport_not_connected_raises():
    transport = SerialTransport(port="/dev/unconnected")
    with pytest.raises(RuntimeError):
        transport.send(Message("eyes", "blink"))
    with pytest.raises(RuntimeError):
        transport.write(b"data")
    with pytest.raises(RuntimeError):
        transport.read_available()
    with pytest.raises(RuntimeError):
        transport.receive()


def test_serial_by_id_setting_warns_and_returns_none_on_invalid_path(monkeypatch):
    monkeypatch.setenv("TEST_QBOT_PORT", "/dev/ttyACM0")
    with warnings.catch_warnings(record=True) as recorded:
        warnings.simplefilter("always")
        port = _serial_by_id_setting("TEST_QBOT_PORT")
        assert port is None
        assert len(recorded) == 1
        assert "TEST_QBOT_PORT should be a /dev/serial/by-id/... path" in str(recorded[0].message)


def test_serial_by_id_setting_accepts_valid_path(monkeypatch):
    valid_path = "/dev/serial/by-id/usb-Raspberry_Pi_Pico_12345"
    monkeypatch.setenv("TEST_QBOT_PORT", valid_path)
    assert _serial_by_id_setting("TEST_QBOT_PORT") == valid_path
