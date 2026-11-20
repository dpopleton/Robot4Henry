# Virtual robot

## Purpose

Qbot's organs as on-screen panels, so organ code can be tried, compared
with the real hardware, and eventually run as a whole robot without the
hardware built or plugged in (D-012, R-209). Each panel runs the organ's
own firmware drawing code, fed the same bytes the real Pico gets.

Today it has the **eyes** and the **mouth**, side by side, each with its
own switch: any mix can be virtual, on a real Pico, or both. Every new
body part adds itself the same way (see Interfaces). The router/brain
hookup comes with R-209.

## How it works

```
controls ──▶ OrganDriver (e.g. MouthOrgan) ──▶ OrganLink ──┬──▶ panel (organs/<organ>/virtual.py) ──▶ CanvasDriver per screen ──▶ Tk canvas
command box ─────────────────────────────────▶            └──▶ SerialTransport ──▶ real Pico
                                                                     └── PicoConsole: crash watch
```

- **`organs.py`** — `ORGANS`: per organ, an `OrganKit` naming its panel,
  host driver and bench controls (all from the organ's own folder). Its
  order is the order of the benches in the window.
- **`app.py`** — the window. One `OrganBench` per organ: the panel's canvas,
  the organ's controls, a **Command** box for raw wire lines, and the
  **Off / Virtual / Real Pico / Both** switch with a port picker. It ticks
  each panel at its `TICK_MS` (as the Pico's `main.py` does) and checks a
  real Pico for crashes every 200ms. Benches know which ports the others
  hold: the picker defaults to a free one, and two benches can't open the
  same Pico (it would otherwise succeed and garble both organs).
- **`link.py`** — `OrganLink`, the switch itself, and the transport the
  organ's driver writes to. Off sends nowhere; Virtual feeds the panel;
  Real feeds the Pico (and the panel out of sight, so switching back shows
  the right state); Both feeds both. No Tk, so it's tested on its own.
- **`canvas_driver.py`** — `CanvasDriver` is one screen: `fill`/
  `fill_circle`/`fill_polygon` at its spot on the canvas, scaled, under its
  own tag (so one eye's `fill` doesn't wipe the other). `CanvasScreens`
  makes one per entry in the panel's `SCREENS` and `cover(note)` greys the
  whole organ out for Off and Real.
- **`voice.py`** — `VirtualVoice`: speaks text in Henry's chosen Piper voice
  (`config.settings.VOICE_MODEL`) through this computer's speakers (`aplay`),
  and returns an `Utterance`: the audio, its mouth levels
  (`organs/mouth/levels.py`) and when each sentence starts (for subtitles).
  Sentences are synthesised one at a time, trimmed of silence and joined
  with a 0.2 s pause, because Piper sometimes adds over a second of silence
  before a sentence.
- **`fake_speech.py`** — `sentence_levels()`: made-up voice levels (words
  of syllables, gaps between words), 25 a second, used when Piper or the
  speakers aren't available.

## Why it's built this way

- **One app, a panel per organ, a bench mode** —
  [D-023](../docs/decisions/D-023-one-virtual-robot-app-with-per-organ-bench-mode.md):
  the switch, port picking and crash watch are written once for every organ.
- **The panel is a transport:** controls go through the organ's real host
  driver, so the bench tests the driver and the wire format too, and
  "Both" is just sending the same bytes twice.
- **Real mode keeps feeding the panel** (hidden), so flipping between Real
  and Both never shows a stale picture.

## Interfaces

Adding an organ: give it, in `organs/<organ>/virtual.py`,

- a **panel** class with `SCREENS` (`((x, y, width, height), ...)` in
  panel pixels: one per real screen, laid out as they should appear),
  `TICK_MS`, and `write(bytes)`, `tick()`, `redraw()`. It's constructed
  with one driver per screen (`MouthPanel(driver)`,
  `EyesPanel(left, right)`), and should run the firmware's own drawing and
  parsing code, as the Pico's `main.py` does;
- a **controls** class `(parent, send, root, panel=None)` with `.frame` and
  `sync()` (resend its state to a freshly connected Pico); `send(**kwargs)`
  calls the driver's `update(**kwargs)`. `panel` is for window-only
  settings (the eyes' Idle movement);
- tests driving the panel through the real host driver
  (`tests/organs/test_<organ>_virtual.py`);

then add an `OrganKit` to `ORGANS`. An organ without a screen (lights,
sound) still needs a panel; how it shows itself is decided per organ
(D-012). Its firmware file names must not clash
with another organ's (a test checks), since every firmware folder ends up
on `sys.path`.

## Running and testing

```bash
python -m virtual_robot                      # every organ (eyes and mouth)
python -m virtual_robot --only eyes          # one organ's bench
python -m virtual_robot --only eyes mouth    # a chosen few
python -m virtual_robot --scale 1.5          # bigger screens (default 1.5 for one organ, 1.0 for several)
```

For **Real Pico** or **Both**, pick the port (↻ rescans; the first Pico
found is chosen) and close anything else holding it. Needs pyserial
(`pip install -e ".[hardware]"`). If the Pico crashes, the error shows on
the bench, the full traceback goes to the terminal, and the switch drops
back to Virtual.

Tests: `tests/virtual_robot/` (the switch, port picking, fake speech) and
the organs' own tests (`tests/organs/test_mouth_driver.py`,
`test_eyes_virtual.py` drive the panels through the drivers).

## Status and known gaps

- Mouth bench done and checked on 2026-11-05: the window, "Say a sentence",
  every switch position, and the crash watch (against the eyes' Pico,
  which ignores mouth lines, since the mouth Pico isn't built).
- Eyes added 2026-11-20 (R-209), replacing `organs/eyes/simulate.py`.
  Checked in the real window with both benches: every eyes control, Off/
  Virtual, the mouth alongside, and a bench refusing a port another holds.
  Not yet checked against the real Picos with both plugged in.
- The port picker still doesn't know which Pico is which organ, only which
  ports the other benches hold, so with both plugged in, check the ports.
  Fixed by R-215 (stable names per Pico, once the hub is in).
- No router or brain yet: the whole-robot mode shows the benches side by side (R-209).
