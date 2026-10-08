# Compact host -> Pico wire format for the eyes. Shared by both sides:
# the Pico parses it (main.py), the host builds it (organs/eyes/driver.py)
# — so it must stay pure Python with no imports, runnable on MicroPython
# and CPython alike.
#
# One ASCII line per update, made of space-separated fields, each one
# optional — send direction alone, expression alone, or both at once:
#
#     D-40,25          look direction, dx,dy as integers in [-100, 100]
#     Ehappy:3         expression (a REGISTRY name) and intensity 1-3
#     Ehappy           expression at its default intensity
#     B                blink
#     Ehappy:3 D-40,25 both together — applied as one redraw, not two
#
# Why not the JSON nervous_system/protocol.py uses: a direction update is
# at most 11 bytes here vs ~70 as JSON, and parsing it on the Pico is a split and
# two int()s. Why not raw binary: MicroPython treats a 0x03 byte on stdin
# as Ctrl-C and would kill main.py mid-stream — plain ASCII never
# contains one, and you can still type commands straight into a serial
# terminal to test.
#
# Unknown or malformed fields are skipped, not fatal: a half-received
# line at power-up shouldn't crash the eyes.

DIRECTION_SCALE = 100
MIN_INTENSITY = 1   # kept in step with brain/limbic/mood.py (a test checks)
MAX_INTENSITY = 3
MAX_LINE = 64       # longer than this is line noise, not a command


def _clamp(value, lo, hi):
    return lo if value < lo else hi if value > hi else value


class Update:
    """Pending changes, merged from one or more lines. Later lines win,
    so a burst of queued direction updates collapses into just the newest
    one — the Pico only ever draws the latest state, never a backlog.
    Fields left as None mean "unchanged"."""

    def __init__(self):
        self.expression = None
        self.intensity = None   # None with an expression = its default intensity
        self.direction = None   # (dx, dy) floats in [-1, 1]
        self.blink = False

    def is_empty(self):
        return self.expression is None and self.direction is None and not self.blink

    def merge_line(self, line):
        for field in line.split():
            kind, body = field[0], field[1:]
            try:
                if kind == "E":
                    parts = body.split(":", 1)
                    if not parts[0]:
                        continue
                    self.expression = parts[0]
                    self.intensity = (
                        _clamp(int(parts[1]), MIN_INTENSITY, MAX_INTENSITY) if len(parts) > 1 else None
                    )
                elif kind == "D":
                    x, y = body.split(",")
                    self.direction = (
                        _clamp(int(x), -DIRECTION_SCALE, DIRECTION_SCALE) / DIRECTION_SCALE,
                        _clamp(int(y), -DIRECTION_SCALE, DIRECTION_SCALE) / DIRECTION_SCALE,
                    )
                elif kind == "B":
                    self.blink = True
            except ValueError:
                pass
        return self


def parse(line):
    return Update().merge_line(line)


def encode(expression=None, intensity=None, direction=None, blink=False):
    """Build one line. Any combination of fields; at least one required."""
    parts = []
    if expression is not None:
        if not expression or " " in expression or ":" in expression or "\n" in expression:
            raise ValueError("Bad expression name: %r" % (expression,))
        if intensity is None:
            parts.append("E" + expression)
        else:
            parts.append("E%s:%d" % (expression, _clamp(int(intensity), MIN_INTENSITY, MAX_INTENSITY)))
    if direction is not None:
        dx, dy = direction
        parts.append("D%d,%d" % (
            _clamp(round(dx * DIRECTION_SCALE), -DIRECTION_SCALE, DIRECTION_SCALE),
            _clamp(round(dy * DIRECTION_SCALE), -DIRECTION_SCALE, DIRECTION_SCALE),
        ))
    if blink:
        parts.append("B")
    if not parts:
        raise ValueError("Nothing to send")
    return (" ".join(parts) + "\n").encode()
