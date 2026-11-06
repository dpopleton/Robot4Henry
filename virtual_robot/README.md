# Virtual robot

## Purpose

Qbot's organs as on-screen panels, so organ code can be tried, compared
with the real hardware, and eventually run as a whole robot without the
hardware built or plugged in (D-012, R-209). Each panel runs the organ's
own firmware drawing code, fed the same bytes the real Pico gets.

Today it has the **mouth**. The eyes move over from
`organs/eyes/simulate.py` next; the router/brain hookup comes with R-209.

## How it works

```
controls ──▶ OrganDriver (e.g. MouthOrgan) ──▶ OrganLink ──┬──▶ panel (organs/<organ>/virtual.py) ──▶ CanvasDriver ──▶ Tk canvas
command box ─────────────────────────────────▶            └──▶ SerialTransport ──▶ real Pico
                                                                     └── PicoConsole: crash watch
```

- **`organs.py`** — `ORGANS`: per organ, an `OrganKit` naming its panel,
  host driver and bench controls (all from the organ's own folder).
- **`app.py`** — the window. One `OrganBench` per organ: the panel's canvas,
  the organ's controls, a **Command** box for raw wire lines, and the
  **Off / Virtual / Real Pico / Both** switch with a port picker. It ticks
  each panel at its `TICK_MS` (as the Pico's `main.py` does) and checks a
  real Pico for crashes every 200ms.
- **`link.py`** — `OrganLink`, the switch itself, and the transport the
  organ's driver writes to. Off sends nowhere; Virtual feeds the panel;
  Real feeds the Pico (and the panel out of sight, so switching back shows
  the right state); Both feeds both. No Tk, so it's tested on its own.
- **`canvas_driver.py`** — `CanvasDriver`: `fill`/`fill_circle`/
  `fill_polygon` onto a Tk canvas, scaled; `cover(note)` greys the panel
  out for Off and Real.
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

- a **panel** class `(driver)` with `WIDTH`, `HEIGHT`, `TICK_MS`,
  `write(bytes)`, `tick()` and `redraw()`;
- a **controls** class `(parent, send, root)` with `.frame` and `sync()`
  (resend its state to a freshly connected Pico); `send(**kwargs)` calls
  the driver's `update(**kwargs)`;

then add an `OrganKit` to `ORGANS`. Its firmware file names must not clash
with another organ's (a test checks), since every firmware folder ends up
on `sys.path`.

## Running and testing

```bash
python -m virtual_robot --only mouth     # one organ's bench
python -m virtual_robot                  # every organ (just the mouth so far)
python -m virtual_robot --scale 1.0      # smaller panels
```

For **Real Pico** or **Both**, pick the port (↻ rescans; the first Pico
found is chosen) and close anything else holding it. Needs pyserial
(`pip install -e ".[hardware]"`). If the Pico crashes, the error shows on
the bench, the full traceback goes to the terminal, and the switch drops
back to Virtual.

Tests: `tests/virtual_robot/` (the switch, fake speech) and the organs'
own tests (`tests/organs/test_mouth_driver.py` drives the panel through the
driver).

## Status and known gaps

- Mouth bench done and checked on 2026-11-05: the window, "Say a sentence",
  every switch position, and the crash watch (against the eyes' Pico,
  which ignores mouth lines, since the mouth Pico isn't built).
- The eyes still use `organs/eyes/simulate.py` (R-209).
- The port picker doesn't know which Pico is which organ, so with two
  plugged in, check the port. Fix with `/dev/serial/by-id/` names or a Pico
  that says what it is.
- No router or brain yet: the whole-robot mode shows the benches side by side (R-209).
