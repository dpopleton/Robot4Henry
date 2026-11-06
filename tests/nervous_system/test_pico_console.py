from nervous_system.pico_console import PicoConsole, describe_crash


# What the real Pico 2 printed when main.py hit math.hypot (2026-11-05).
PICO_CRASH = (
    "Traceback (most recent call last):\r\n"
    '  File "main.py", line 81, in <module>\r\n'
    '  File "expressions.py", line 318, in render_scared\r\n'
    '  File "expressions.py", line 74, in _thick_line\r\n'
    "AttributeError: 'module' object has no attribute 'hypot'\r\n"
    "MicroPython v1.29.0 on 2026-08-24; Raspberry Pi Pico2 with RP2350\r\n"
    'Type "help()" for more information.\r\n'
    ">>> "
)


class ConsoleTransport:
    def __init__(self, chunks):
        self.chunks = list(chunks)

    def read_available(self):
        return self.chunks.pop(0) if self.chunks else b""


def test_describe_crash_gives_the_error_and_where():
    assert describe_crash(PICO_CRASH) == (
        "AttributeError: 'module' object has no attribute 'hypot' "
        '(File "expressions.py", line 74, in _thick_line)'
    )


def test_describe_crash_without_a_traceback_means_already_at_the_prompt():
    assert ">>> prompt" in describe_crash("Ehappy:2\r\n>>> ")


def test_poll_crash_is_none_while_the_pico_is_quiet():
    console = PicoConsole(ConsoleTransport([]))
    assert console.poll_crash() is None


def test_poll_crash_waits_for_the_prompt_across_reads():
    data = PICO_CRASH.encode()
    console = PicoConsole(ConsoleTransport([data[:60], data[60:]]))
    assert console.poll_crash() is None
    summary, text = console.poll_crash()
    assert "hypot" in summary
    assert text == PICO_CRASH
    assert console.poll_crash() is None  # reported once
