"""
Watches a Pico's console for a crash. Every organ's main.py prints
nothing while it runs, so any output means it stopped: MicroPython
prints a traceback and then its >>> prompt. Used by anything holding a
real organ's transport (the virtual robot app, simulate.py) so a crash
shows up instead of the organ silently freezing.
"""

MAX_CONSOLE_CHARS = 4096  # keep only the tail of what the Pico prints


def describe_crash(text: str) -> str:
    """One line saying why the Pico's main.py stopped, from what it
    printed: the error and the line it happened on. Uses the first
    traceback — any later ones are just the REPL complaining about
    commands that arrived after the crash."""
    if "Traceback" not in text:
        return "the organ's program isn't running (the Pico is at its >>> prompt)"
    lines = [line.strip() for line in text[text.index("Traceback"):].splitlines()[1:]]
    where = [line for line in lines if line.startswith("File ")]
    error = next((line for line in lines if line and not line.startswith("File ")), "unknown error")
    return error + (f" ({where[-1]})" if where else "")


class PicoConsole:
    def __init__(self, transport):
        """transport: anything with read_available() -> bytes that never
        blocks, e.g. nervous_system.serial_transport.SerialTransport."""
        self.transport = transport
        self._text = ""

    def poll_crash(self):
        """Read anything the Pico has printed. Returns (summary,
        everything_printed) once the >>> prompt shows up, else None.
        Until then, partial output is kept for the next call."""
        data = self.transport.read_available()
        if not data:
            return None
        self._text = (self._text + data.decode(errors="replace"))[-MAX_CONSOLE_CHARS:]
        if ">>>" not in self._text:
            return None
        text, self._text = self._text, ""
        return describe_crash(text), text
