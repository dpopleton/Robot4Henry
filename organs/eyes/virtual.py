"""
The eyes' virtual panel (D-023): takes the same bytes the real eyes Pico
does and runs the eyes' firmware drawing code on them, unchanged, onto
two drivers (left and right screen) — Tk canvases in the virtual robot,
or recording fakes in tests. It's also a transport, so EyesOrgan can
write straight to it.

As the Pico's main.py: commands apply as they arrive, Face.tick() runs
every TICK_MS for idle glances, blinks and animation, and a commanded
blink stays shut for a full tick.
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
for _path in (os.path.join(_HERE, "firmware"), os.path.join(_HERE, "..", "pico_common")):
    if _path not in sys.path:
        sys.path.insert(0, _path)

from eye_geometry import WIDTH, HEIGHT  # noqa: E402
from eye_protocol import MAX_LINE, MAX_INTENSITY, MIN_INTENSITY, parse  # noqa: E402
from eyes import Eye, Face  # noqa: E402
from expressions import DEFAULT_INTENSITY, EXPRESSIONS  # noqa: E402
from line_reader import LineReader  # noqa: E402

GAP = 20   # panel pixels between the two eyes on screen


class EyesPanel:
    TICK_MS = 150   # as firmware/main.py
    # Left eye drawn on the left, as the old simulator did.
    SCREENS = ((0, 0, WIDTH, HEIGHT), (WIDTH + GAP, 0, WIDTH, HEIGHT))

    def __init__(self, left_driver, right_driver):
        # mirror=True on the right eye points asymmetric shapes (brows)
        # inward on both; it never touches look direction (expressions.py).
        self.face = Face(Eye(left_driver, mirror=False), Eye(right_driver, mirror=True))
        self.idle = True          # off: no glances, blinks or animation (window only)
        self._hold_blink = False
        self._reader = LineReader(None, MAX_LINE)

    # Transport side: bytes in, like the Pico's USB serial.
    def connect(self):
        pass

    def close(self):
        pass

    def write(self, data: bytes):
        for ch in data.decode(errors="replace"):
            self._reader.feed(ch, self._on_line)

    def _on_line(self, line):
        update = parse(line)
        if update.is_empty():
            return
        self.face.update(update.expression, update.intensity, update.direction)
        if update.blink:
            self.face.blink()
            self._hold_blink = True   # main.py restarts its tick clock here

    # Host side: the frame clock, and repainting after being covered.
    def tick(self):
        if self._hold_blink:
            self._hold_blink = False
        elif self.idle:
            self.face.tick()
        else:
            self.face.update()   # still reopens a blink, nothing else moves

    def redraw(self):
        for eye in self.face.eyes:
            eye.render()


LOOK_BUTTONS = (
    ("↖", -1, -1), ("↑", 0, -1), ("↗", 1, -1),
    ("←", -1, 0), ("●", 0, 0), ("→", 1, 0),
    ("↙", -1, 1), ("↓", 0, 1), ("↘", 1, 1),
)


class EyesControls:
    """The eyes' buttons for the virtual robot's bench (D-023): a button
    per expression, intensity 1–3, look arrows, Blink, Neutral, and Idle
    movement. Everything except Idle movement goes out through
    send(**EyesOrgan.update kwargs), so it reaches the panel, the Pico or
    both, via the real driver. Idle movement only pauses the window: the
    wire format has no command for it, so the real eyes keep glancing and
    blinking on their own."""

    def __init__(self, parent, send, root, panel=None):
        import tkinter as tk

        self.send = send
        self.panel = panel
        self.frame = tk.Frame(parent)
        self.expression = None
        self.direction = (0.0, 0.0)
        self.intensity = tk.IntVar(value=DEFAULT_INTENSITY)

        tk.Label(self.frame, text="Expressions", font=("", 10, "bold")).grid(
            row=0, column=0, columnspan=6, sticky="w")
        names = sorted(EXPRESSIONS)
        per_row = 6
        for i, name in enumerate(names):
            tk.Button(self.frame, text=name, width=9, command=lambda n=name: self.set_expression(n)).grid(
                row=1 + i // per_row, column=i % per_row, padx=1, pady=1, sticky="ew")
        row = 1 + (len(names) + per_row - 1) // per_row

        intensity = tk.Frame(self.frame)
        intensity.grid(row=row, column=0, columnspan=6, sticky="w", pady=(6, 0))
        tk.Label(intensity, text="Intensity", font=("", 10, "bold")).pack(side="left")
        for level in range(MIN_INTENSITY, MAX_INTENSITY + 1):
            tk.Radiobutton(intensity, text=str(level), value=level, variable=self.intensity,
                           command=self._on_intensity).pack(side="left")

        tk.Label(self.frame, text="Look", font=("", 10, "bold")).grid(
            row=row + 1, column=0, columnspan=6, sticky="w", pady=(6, 0))
        look = tk.Frame(self.frame)
        look.grid(row=row + 2, column=0, columnspan=3, sticky="w")
        for i, (label, dx, dy) in enumerate(LOOK_BUTTONS):
            tk.Button(look, text=label, width=3, command=lambda d=(dx, dy): self.look(d)).grid(
                row=i // 3, column=i % 3)

        actions = tk.Frame(self.frame)
        actions.grid(row=row + 2, column=3, columnspan=3, sticky="nw")
        tk.Button(actions, text="Blink", width=10, command=lambda: self.send(blink=True)).pack(pady=2)
        tk.Button(actions, text="Neutral", width=10, command=lambda: self.set_expression("neutral")).pack(pady=2)
        self.idle = tk.BooleanVar(value=True)
        tk.Checkbutton(actions, text="Idle movement (window only)", variable=self.idle,
                       command=self._on_idle).pack(pady=2)

    def set_expression(self, name):
        self.expression = name
        self.send(expression=name, intensity=self.intensity.get())

    def _on_intensity(self):
        if self.expression is not None:
            self.send(expression=self.expression, intensity=self.intensity.get())

    def look(self, direction):
        self.direction = direction
        self.send(direction=direction)

    def _on_idle(self):
        if self.panel is not None:
            self.panel.idle = self.idle.get()

    def sync(self):
        """Bring a freshly connected Pico in line with the controls."""
        self.send(expression=self.expression or "neutral", intensity=self.intensity.get(),
                  direction=self.direction)
