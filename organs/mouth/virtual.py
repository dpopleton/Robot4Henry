"""
The mouth's virtual panel (D-023): takes the same bytes the real mouth
Pico does and runs the mouth's firmware drawing code on them, unchanged,
onto any driver — a Tk canvas in the virtual robot, or a recording fake
in tests. It's also a transport, so MouthOrgan can write straight to it.

The Pico's main.py applies commands as they arrive and calls tick() every
TICK_MS; whoever hosts the panel does the same with tick().
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
for _path in (os.path.join(_HERE, "firmware"), os.path.join(_HERE, "..", "pico_common")):
    if _path not in sys.path:
        sys.path.insert(0, _path)

from line_reader import LineReader  # noqa: E402
from mouth import Mouth, TICK_MS  # noqa: E402
from mouth_geometry import WIDTH, HEIGHT  # noqa: E402
from mouth_protocol import MAX_LINE, parse  # noqa: E402


class MouthPanel:
    WIDTH = WIDTH
    HEIGHT = HEIGHT
    TICK_MS = TICK_MS

    def __init__(self, driver, rand=None):
        self.mouth = Mouth(driver) if rand is None else Mouth(driver, rand)
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
        if not update.is_empty():
            self.mouth.update(talking=update.talking, level=update.level)

    # Host side: the frame clock, and repainting after being covered.
    def tick(self):
        return self.mouth.tick()

    def redraw(self):
        self.mouth.redraw()


class MouthControls:
    """The mouth's own buttons for the virtual robot's bench (D-023).

    - Say it: speaks the text in Qbot's real voice (Piper, through this
      computer's speakers), sends the mouth levels worked out from that
      audio at the real rate (D-024), and shows each sentence as a subtitle.
      Without Piper or speakers it falls back to made-up levels, still
      showing the text.
    - Mouth delay: delays the mouth against the sound, to cover the
      speakers' lag. Tune it by eye here; the robot will need its own value
      (R-210).
    - Move the mouth by hand: Talking on its own makes the mouth wiggle by
      itself; Hold loudness sends the slider's level steadily.

    Everything goes out through send(**MouthOrgan.update kwargs), so it
    reaches the panel, the Pico or both, via the real driver."""

    LEVEL_MS = 40   # 25 levels a second, like the real voice (D-024)
    LINES = (
        "Hello Henry! I'm Qbot. Shall we build something amazing today?",
        "Did you know an octopus has three hearts? That's two more than me. I have none!",
        "Beep boop. Just kidding, robots don't really say that.",
        "Time for bed. Goodnight, see you tomorrow!",
    )

    def __init__(self, parent, send, root, voice=None):
        import tkinter as tk
        from tkinter import ttk

        from virtual_robot.fake_speech import RATE, sentence_levels
        from virtual_robot.voice import Utterance, VirtualVoice, split_sentences

        self._fake_levels, self._rate = sentence_levels, RATE  # levels per second
        self._Utterance, self._split = Utterance, split_sentences
        self.voice = voice or VirtualVoice()
        self.voice_problem = self.voice.unavailable_reason()
        self.send = send
        self.root = root
        self.frame = tk.Frame(parent)

        def hint(parent, text, row):
            tk.Label(parent, text=text, fg="gray30", justify="left", wraplength=420,
                     font=("", 9)).grid(row=row, column=0, columnspan=3, sticky="w")

        self.subtitle = tk.Label(self.frame, text="", font=("", 13), wraplength=440,
                                 justify="center", height=2)
        self.subtitle.pack(fill="x")

        # Speaking: the normal way to see the mouth.
        speak = tk.LabelFrame(self.frame, text="Make Qbot speak", padx=6, pady=4)
        speak.pack(fill="x")
        self.text = ttk.Combobox(speak, values=self.LINES, width=46)
        self.text.set(self.LINES[0])
        self.text.grid(row=0, column=0, columnspan=2, sticky="ew")
        self.text.bind("<Return>", lambda _e: self.say())
        self.say_button = tk.Button(speak, text="Say it", command=self.say)
        self.say_button.grid(row=0, column=2, padx=(6, 0))
        hint(speak, "Pick a line or type your own, then press Say it.", 1)

        self.sync_ms = tk.IntVar(value=100)
        tk.Label(speak, text="Mouth delay (ms)").grid(row=2, column=0, sticky="sw", pady=(4, 0))
        tk.Scale(speak, from_=-200, to=400, resolution=20, orient="horizontal", variable=self.sync_ms,
                 length=260).grid(row=2, column=1, columnspan=2, sticky="w")
        hint(speak, "Lip-sync. Speakers play sound a little late, so the mouth waits this long "
                    "to match. Mouth moves before the voice: slide right. After it: slide left.", 3)

        # By hand: for testing the mouth without speech.
        manual = tk.LabelFrame(self.frame, text="Move the mouth by hand", padx=6, pady=4)
        manual.pack(fill="x", pady=(6, 0))
        self.talking = tk.BooleanVar(value=False)
        self.send_levels = tk.BooleanVar(value=False)
        self.level = tk.IntVar(value=60)
        tk.Checkbutton(manual, text="Talking", variable=self.talking,
                       command=lambda: self.send(talking=self.talking.get())).grid(row=0, column=0, sticky="w")
        hint(manual, "On its own, the mouth makes up its own talking rhythm "
                     "(what the robot does if the laptop stops sending loudness).", 1)
        tk.Checkbutton(manual, text="Hold loudness at", variable=self.send_levels).grid(
            row=2, column=0, sticky="sw", pady=(4, 0))
        tk.Scale(manual, from_=0, to=100, orient="horizontal", variable=self.level,
                 length=220).grid(row=2, column=1, columnspan=2, sticky="w")
        hint(manual, "While Talking, sends this voice loudness (0 = quiet, 100 = loud) "
                     "instead, so you can see how tall the spikes get.", 3)

        self.note = tk.Label(self.frame, fg="gray30", justify="left", wraplength=440, text=(
            f"No voice, so Say it uses made-up levels: {self.voice_problem}" if self.voice_problem else ""
        ))
        self.note.pack(fill="x", pady=(4, 0))

        self._utterance = None   # playing now
        self._started = None     # time.monotonic() when the sound started
        self._ready = None       # set by the synthesis thread
        self._send_loop()

    def sync(self):
        """Bring a freshly connected Pico in line with the controls."""
        self.send(talking=self.talking.get() or self._utterance is not None)

    def say(self):
        import threading

        text = self.text.get().strip()
        if not text:
            return
        self.say_button.config(state="disabled")
        self.voice.stop()
        if self.voice_problem:
            self._ready = self._fake_utterance(text)
            return

        def work():
            try:
                self._ready = self.voice.prepare(text)
            except Exception as e:  # shown on the bench, then fall back
                self.voice_problem = f"the voice failed ({e})"
                self._ready = self._fake_utterance(text)

        self.subtitle.config(text="…")
        threading.Thread(target=work, daemon=True).start()

    def _fake_utterance(self, text):
        sentences = self._split(text)
        seconds = max(1.5, 0.07 * len(text))
        levels = self._fake_levels(seconds)
        share = seconds / max(1, len(sentences))
        return self._Utterance(b"", self._rate, levels, [(i * share, s) for i, s in enumerate(sentences)])

    def _send_loop(self):
        import time

        if self._ready is not None:
            self._utterance, self._ready = self._ready, None
            if self._utterance.audio:
                self.voice.play(self._utterance)
            self._started = time.monotonic()
            self.talking.set(True)
            self.send(talking=True)
            if self.voice_problem:
                self.note.config(text=f"No voice, so Say it uses made-up levels: {self.voice_problem}")

        failure = self.voice.failure()
        if failure:
            import sys
            print(f"--- aplay couldn't play the voice ---\n{failure}\n---", file=sys.stderr)
            self.note.config(fg="dark red", text=f"The sound didn't play: {failure.splitlines()[-1]}")

        if self._utterance is not None:
            elapsed = time.monotonic() - self._started
            mouth_time = elapsed - self.sync_ms.get() / 1000
            index = int(mouth_time * self._rate)
            if index >= len(self._utterance.levels):
                self._utterance = None
                self.subtitle.config(text="")
                self.say_button.config(state="normal")
                self.talking.set(False)
                self.send(talking=False)
            else:
                self.subtitle.config(text=self._utterance.sentence_at(elapsed))
                self.send(level=self._utterance.levels[index] if index >= 0 else 0.0)
        elif self.talking.get() and self.send_levels.get():
            self.send(level=self.level.get() / 100)
        self.root.after(self.LEVEL_MS, self._send_loop)
