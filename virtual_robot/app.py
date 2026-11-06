"""
The virtual robot window (D-012, D-023). One bench per organ: its panel
drawn by the organ's own firmware code, its controls, a switch between
off / virtual / real Pico / both, and a command box for raw wire lines.
If the real Pico crashes, the error shows on its bench and the switch
drops back to virtual.

    python -m virtual_robot --only mouth    # one organ: the bench
    python -m virtual_robot                 # every organ (the router and
                                            # brain hook up later, R-209)
"""

import argparse
import sys
import tkinter as tk
from tkinter import ttk

from nervous_system.serial_transport import SerialTransport, list_pico_ports
from virtual_robot.canvas_driver import CanvasDriver
from virtual_robot.link import USES_PICO, OrganLink
from virtual_robot.organs import ORGANS

WATCH_MS = 200   # how often to check a real Pico for a crash
MODE_LABELS = (("Off", "off"), ("Virtual", "virtual"), ("Real Pico", "real"), ("Both", "both"))


def open_serial(port):
    transport = SerialTransport(port)
    transport.connect()
    return transport


class OrganBench:
    def __init__(self, parent, root, kit, scale):
        self.root = root
        self.name = kit.name
        self.frame = tk.LabelFrame(parent, text=kit.name.capitalize(), padx=8, pady=6)

        width, height = kit.panel_class.WIDTH, kit.panel_class.HEIGHT
        canvas = tk.Canvas(self.frame, width=width * scale, height=height * scale,
                           bg="black", highlightthickness=0)
        canvas.pack()
        self.canvas_driver = CanvasDriver(canvas, width, height, scale)
        self.panel = kit.panel_class(self.canvas_driver)
        self.link = OrganLink(self.panel, open_serial)
        self.driver = kit.driver_class(self.link)

        self.controls = kit.controls_class(self.frame, self.send, root)
        self.controls.frame.pack(fill="x", pady=(8, 0))

        command = tk.Frame(self.frame)
        command.pack(fill="x", pady=(8, 0))
        tk.Label(command, text="Command").pack(side="left")
        self.command = tk.Entry(command, width=24)
        self.command.pack(side="left", padx=4)
        self.command.insert(0, kit.example_command)
        self.command.bind("<Return>", lambda _e: self.send_command())
        tk.Button(command, text="Send", command=self.send_command).pack(side="left")

        switch = tk.Frame(self.frame)
        switch.pack(fill="x", pady=(8, 0))
        self.mode = tk.StringVar(value=self.link.mode)
        for label, mode in MODE_LABELS:
            tk.Radiobutton(switch, text=label, value=mode, variable=self.mode,
                           command=self._on_mode).pack(side="left")
        self.port = ttk.Combobox(switch, width=16)
        self.port.pack(side="left", padx=4)
        tk.Button(switch, text="↻", command=self.refresh_ports).pack(side="left")
        self.status = tk.Label(self.frame, text="", anchor="w", justify="left",
                               wraplength=width * scale)
        self.status.pack(fill="x")

        self.refresh_ports()
        self._tick()
        self._watch()

    # Sending — every control ends up here or in send_command.
    def send(self, **kwargs):
        try:
            self.driver.update(**kwargs)
        except OSError as e:
            self._lose_pico(f"Lost the {self.name} Pico: {e}")

    def send_command(self):
        line = self.command.get().strip()
        if line:
            try:
                self.link.write((line + "\n").encode())
            except OSError as e:
                self._lose_pico(f"Lost the {self.name} Pico: {e}")

    # The switch.
    def refresh_ports(self):
        ports = list_pico_ports()
        self.port["values"] = ports
        if ports and self.port.get() not in ports:
            self.port.set(ports[0])
        if self.link.mode not in USES_PICO:
            self._say("" if ports else "No Pico found — plug one in and press ↻.")

    def _on_mode(self):
        mode = self.mode.get()
        port = self.port.get().strip() or None
        if mode in USES_PICO and not port:
            self.mode.set(self.link.mode)
            self._say("Pick a port first (plug the Pico in and press ↻).", error=True)
            return
        try:
            self.link.set_mode(mode, port)
        except ImportError:
            self.mode.set(self.link.mode)
            self._say('pyserial isn\'t installed: pip install -e ".[hardware]"', error=True)
            return
        except OSError as e:
            self.mode.set(self.link.mode)
            hint = " (add yourself to the dialout group, then log out and in)" if "ermission" in str(e) else ""
            self._say(f"Couldn't open {port}: {e}{hint}", error=True)
            return
        self._show_mode()
        if mode in USES_PICO:
            self.controls.sync()  # bring the Pico in line with the controls
            self._say(f"Sending to the Pico on {port}.", ok=True)
        else:
            self._say("Off: nothing shown or sent." if mode == "off" else "")

    def _show_mode(self):
        mode = self.link.mode
        if mode == "off":
            self.canvas_driver.cover("Off")
        elif mode == "real":
            self.canvas_driver.cover(f"Showing on the real Pico only\n({self.link.port})")
        elif self.canvas_driver.covered:
            self.canvas_driver.uncover()
            self.panel.redraw()

    def _lose_pico(self, message):
        self.link.drop_pico()
        self.mode.set(self.link.mode)
        self._show_mode()
        self._say(message, error=True)

    def _say(self, text, error=False, ok=False):
        self.status.config(text=text, fg="dark red" if error else "dark green" if ok else "black")

    # Clocks.
    def _tick(self):
        self.panel.tick()
        self.root.after(self.panel.TICK_MS, self._tick)

    def _watch(self):
        try:
            crash = self.link.poll_crash()
        except OSError as e:
            self._lose_pico(f"Lost the {self.name} Pico: {e}")
        else:
            if crash:
                summary, text = crash
                print(f"--- the {self.name} Pico printed ---\n{text.strip()}\n---", file=sys.stderr)
                self._lose_pico(f"The {self.name} Pico crashed: {summary}\n"
                                "Unplug and replug it to restart, then switch to it again.")
        self.root.after(WATCH_MS, self._watch)

    def close(self):
        self.link.close()


def main(argv=None):
    parser = argparse.ArgumentParser(prog="python -m virtual_robot", description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--only", choices=sorted(ORGANS), help="show just this organ's bench")
    parser.add_argument("--scale", type=float, default=1.5, help="screen size multiplier (default 1.5)")
    args = parser.parse_args(argv)

    root = tk.Tk()
    root.title("Virtual Qbot" + (f": {args.only}" if args.only else ""))
    names = [args.only] if args.only else list(ORGANS)
    benches = []
    for name in names:
        bench = OrganBench(root, root, ORGANS[name](), args.scale)
        bench.frame.pack(side="left", padx=10, pady=10, anchor="n")
        benches.append(bench)

    def quit_():
        for bench in benches:
            bench.close()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", quit_)
    root.mainloop()
