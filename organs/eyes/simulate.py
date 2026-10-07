#!/usr/bin/env python3
"""
Desktop preview of the eyes — draws whatever expressions.py would draw
onto the real GC9A01 panels, but onto a Tkinter window instead, so you
can see how an expression looks before flashing the Pico.

Reuses organs/eyes/firmware/eyes.py and expressions.py completely
unchanged — SimDriver below just satisfies the same driver contract
(fill/fill_circle/fill_polygon) that gc9a01.py does, standing in for
the SPI panel.

The "Command" box takes the exact lines the host sends the Pico (e.g.
`Ehappy:3 D-40,25` — see firmware/eye_protocol.py), parsed by the same
code main.py uses, so you can try the wire format without hardware.

Usage:
    python organs/eyes/simulate.py
"""

import os
import sys
import tkinter as tk

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "firmware"))

from eye_geometry import WIDTH, HEIGHT  # noqa: E402
from eyes import Eye, Face  # noqa: E402
from expressions import EXPRESSIONS  # noqa: E402
from eye_protocol import parse, MIN_INTENSITY, MAX_INTENSITY  # noqa: E402

SCALE = 1.5       # canvas is bigger than the real 240x240 panel, for visibility
IDLE_TICK_MS = 150  # how often Face.tick() runs — see eyes.py for what it does per tick
BLINK_MS = 150     # how long a Blink-button blink stays shut (main.py holds it one tick)


def _rgb565_to_hex(color: int) -> str:
    r5, g6, b5 = (color >> 11) & 0x1F, (color >> 5) & 0x3F, color & 0x1F
    r, g, b = r5 * 255 // 31, g6 * 255 // 63, b5 * 255 // 31
    return f"#{r:02x}{g:02x}{b:02x}"


class SimDriver:
    """Same contract as GC9A01: fill(), fill_circle(), fill_polygon().
    Draws straight onto a Tkinter Canvas, scaled up for visibility."""

    WIDTH = WIDTH
    HEIGHT = HEIGHT

    def __init__(self, canvas: tk.Canvas):
        self.canvas = canvas

    def fill(self, color: int):
        self.canvas.delete("all")
        self.canvas.create_rectangle(
            0, 0, self.WIDTH * SCALE, self.HEIGHT * SCALE,
            fill=_rgb565_to_hex(color), outline="",
        )

    def fill_circle(self, cx: int, cy: int, r: int, color: int):
        self.canvas.create_oval(
            (cx - r) * SCALE, (cy - r) * SCALE, (cx + r) * SCALE, (cy + r) * SCALE,
            fill=_rgb565_to_hex(color), outline="",
        )

    def fill_polygon(self, points, color: int):
        flat = [coord * SCALE for p in points for coord in p]
        self.canvas.create_polygon(flat, fill=_rgb565_to_hex(color), outline="")


LOOK_BUTTONS = [
    ("↖", -1, -1), ("↑", 0, -1), ("↗", 1, -1),
    ("←", -1, 0), ("●", 0, 0), ("→", 1, 0),
    ("↙", -1, 1), ("↓", 0, 1), ("↘", 1, 1),
]


class SimulatorApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title("Eyes simulator")

        eyes_frame = tk.Frame(root)
        eyes_frame.pack(padx=10, pady=10)

        self.left_canvas = tk.Canvas(eyes_frame, width=WIDTH * SCALE, height=HEIGHT * SCALE, bg="black")
        self.left_canvas.grid(row=0, column=0, padx=5)
        self.right_canvas = tk.Canvas(eyes_frame, width=WIDTH * SCALE, height=HEIGHT * SCALE, bg="black")
        self.right_canvas.grid(row=0, column=1, padx=5)

        # mirror=True on the right eye only — see expressions.py: this
        # points asymmetric shapes (like a scowling eyebrow) inward on
        # both eyes instead of both tilting the same way. It never
        # touches look direction, so both eyes still look the same way.
        self.left_eye = Eye(SimDriver(self.left_canvas), mirror=False)
        self.right_eye = Eye(SimDriver(self.right_canvas), mirror=True)
        self.face = Face(self.left_eye, self.right_eye)

        controls = tk.Frame(root)
        controls.pack(padx=10, pady=(0, 10), fill="x")

        tk.Label(controls, text="Expressions", font=("", 10, "bold")).grid(row=0, column=0, columnspan=4, sticky="w")
        names = sorted(EXPRESSIONS)
        for i, name in enumerate(names):
            tk.Button(
                controls, text=name, width=10,
                command=lambda n=name: self.face.set_expression(n, self.intensity.get()),
            ).grid(row=1 + i // 4, column=i % 4, padx=2, pady=2, sticky="ew")

        row_after_expr = 1 + (len(names) + 3) // 4

        intensity_frame = tk.Frame(controls)
        intensity_frame.grid(row=row_after_expr, column=0, columnspan=4, sticky="w", pady=(6, 0))
        tk.Label(intensity_frame, text="Intensity", font=("", 10, "bold")).pack(side="left")
        self.intensity = tk.IntVar(value=2)
        for level in range(MIN_INTENSITY, MAX_INTENSITY + 1):
            tk.Radiobutton(
                intensity_frame, text=str(level), value=level, variable=self.intensity,
                command=self._apply_intensity,
            ).pack(side="left")
        row_after_expr += 1

        tk.Label(controls, text="Look direction", font=("", 10, "bold")).grid(
            row=row_after_expr, column=0, columnspan=4, sticky="w", pady=(10, 0)
        )
        look_frame = tk.Frame(controls)
        look_frame.grid(row=row_after_expr + 1, column=0, columnspan=2, sticky="w")
        for i, (label, dx, dy) in enumerate(LOOK_BUTTONS):
            tk.Button(look_frame, text=label, width=3, command=lambda dx=dx, dy=dy: self.face.look_at(dx, dy)).grid(
                row=i // 3, column=i % 3
            )

        actions = tk.Frame(controls)
        actions.grid(row=row_after_expr + 1, column=2, columnspan=2, sticky="n")
        tk.Button(actions, text="Blink", width=10, command=self._blink).pack(pady=2)
        tk.Button(actions, text="Neutral", width=10, command=lambda: self.face.set_expression("neutral")).pack(pady=2)
        self.idle_enabled = tk.BooleanVar(value=True)
        tk.Checkbutton(actions, text="Idle movement", variable=self.idle_enabled).pack(pady=2)

        command_frame = tk.Frame(controls)
        command_frame.grid(row=row_after_expr + 2, column=0, columnspan=4, sticky="ew", pady=(10, 0))
        tk.Label(command_frame, text="Command", font=("", 10, "bold")).pack(side="left")
        self.command = tk.Entry(command_frame, width=28)
        self.command.pack(side="left", padx=4)
        self.command.insert(0, "Ehappy:3 D-40,25")
        self.command.bind("<Return>", lambda _e: self._send_command())
        tk.Button(command_frame, text="Send", command=self._send_command).pack(side="left")

        self._schedule_tick()

    def _apply_intensity(self):
        if self.face.left.expression is not None:
            self.face.set_expression(self.face.left.expression, self.intensity.get())

    def _blink(self):
        self.face.blink()
        self.root.after(BLINK_MS, self.face.update)  # reopen, even with idle movement off

    def _send_command(self):
        update = parse(self.command.get())
        self.face.update(update.expression, update.intensity, update.direction)
        if update.intensity is not None:
            self.intensity.set(update.intensity)
        if update.blink:
            self._blink()

    def _schedule_tick(self):
        if self.idle_enabled.get():
            self.face.tick()
        self.root.after(IDLE_TICK_MS, self._schedule_tick)


if __name__ == "__main__":
    root = tk.Tk()
    SimulatorApp(root)
    root.mainloop()
