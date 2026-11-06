# Compact host -> Pico wire format for the mouth. Shared by both sides:
# the Pico parses it (main.py), the host builds it (organs/mouth/driver.py),
# so it must stay pure Python with no imports — MicroPython and CPython alike.
# Same style as the eyes' (D-001): one ASCII line, space-separated fields,
# each optional.
#
#     S1      start talking: the line becomes a seismograph
#     S0      stop talking: it settles back to a flat line
#     L57     voice level 0-100, sent about 25 times a second while
#             talking (D-024). With no levels, the mouth wiggles by itself.
#     S1 L40  both together
#
# Reserved, not yet used: E<mood>:<intensity> like the eyes, if Henry
# decides mood should show on the mouth (R-210); V for the volume (R-306).
# Unknown or malformed fields are skipped, not fatal.

MIN_LEVEL = 0
MAX_LEVEL = 100
MAX_LINE = 64   # longer than this is line noise, not a command


def _clamp(value, lo, hi):
    return lo if value < lo else hi if value > hi else value


class Update:
    """Pending changes, merged from one or more lines. Later lines win,
    so a backlog of levels collapses into the newest one. None means
    "unchanged"."""

    def __init__(self):
        self.talking = None   # True / False
        self.level = None     # int 0-100

    def is_empty(self):
        return self.talking is None and self.level is None

    def merge_line(self, line):
        for field in line.split():
            kind, body = field[0], field[1:]
            try:
                if kind == "S":
                    if body in ("0", "1"):
                        self.talking = body == "1"
                elif kind == "L":
                    self.level = _clamp(int(body), MIN_LEVEL, MAX_LEVEL)
            except ValueError:
                pass
        return self


def parse(line):
    return Update().merge_line(line)


def encode(talking=None, level=None):
    """Build one line. Any combination of fields; at least one required."""
    parts = []
    if talking is not None:
        parts.append("S1" if talking else "S0")
    if level is not None:
        parts.append("L%d" % _clamp(round(level), MIN_LEVEL, MAX_LEVEL))
    if not parts:
        raise ValueError("Nothing to send")
    return (" ".join(parts) + "\n").encode()
