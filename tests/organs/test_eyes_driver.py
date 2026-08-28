from organs.eyes.driver import EyesOrgan


class FakeTransport:
    def __init__(self):
        self.sent = []
        self.connected = False

    def connect(self):
        self.connected = True

    def send(self, message):
        self.sent.append(message)

    def close(self):
        self.connected = False


def test_blink_sends_eyes_blink_message():
    transport = FakeTransport()
    eyes = EyesOrgan(transport)

    eyes.blink()

    assert len(transport.sent) == 1
    msg = transport.sent[0]
    assert msg.organ == "eyes"
    assert msg.cmd == "blink"


def test_set_expression_includes_mood_payload():
    transport = FakeTransport()
    eyes = EyesOrgan(transport)

    eyes.set_expression("curious")

    msg = transport.sent[0]
    assert msg.cmd == "set_expression"
    assert msg.payload == {"mood": "curious"}
