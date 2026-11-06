# Reads command lines from USB serial (stdin) without blocking — shared by
# every organ's main.py. Copied to the Pico next to the organ's own files
# (organs/deploy.py), so it's imported flat: `from line_reader import LineReader`.
#
# Plain Python plus select.poll, which MicroPython and CPython both have.
# The line-splitting (feed) is separate from the polling (drain) so tests
# can run it without a real stream.

import select

MAX_DRAIN_CHARS = 512  # read at most this much per drain, so a flood can't starve redraws


class LineReader:
    def __init__(self, stream, max_line):
        """max_line: longer lines are line noise, not commands — dropped
        whole, up to the next newline. stream None: feed() only, for
        bytes that arrive some other way (the virtual robot's panels)."""
        self.stream = stream
        self.max_line = max_line
        if stream is not None:
            self.poller = select.poll()
            self.poller.register(stream, select.POLLIN)
        self.chars = []
        self.overflow = False

    def wait(self, timeout_ms):
        """Sleep until input arrives or timeout_ms passes."""
        self.poller.poll(timeout_ms)

    def drain(self, on_line):
        """Call on_line(line) for every complete line already waiting."""
        for _ in range(MAX_DRAIN_CHARS):
            if not self.poller.poll(0):
                return
            self.feed(self.stream.read(1), on_line)

    def feed(self, ch, on_line):
        """Take one character; call on_line(line) when it ends a line."""
        if ch == "\n":
            if not self.overflow:
                on_line("".join(self.chars))
            self.chars = []
            self.overflow = False
        elif ch == "\r":
            pass
        elif len(self.chars) < self.max_line:
            self.chars.append(ch)
        else:
            self.overflow = True  # garbage — drop until the next newline
