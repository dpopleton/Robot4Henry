# Mouth

## Purpose

Qbot's mouth: a 2" screen under the eyes showing white lines on black. A
flat line while he's quiet; while he talks, a **seismograph in a mouth
shape**: spikes up and down from the line, tallest in the middle and fading
to nothing at the corners, flickering constantly, their height following
his voice. The firmware will run on its own Pico 2 (D-009).

Whether mood shows on the mouth too is Henry's call (R-210); the wire format
keeps room for it.

Hardware (display, wiring, mounting) lives in
[`anatomy/mouth/build.md`](../../anatomy/mouth/build.md).

## How it works

```
host: MouthOrgan (driver.py) ──"S1\n", "L57\n" …──▶ USB serial ──▶ Pico (later: main.py) → LineReader → Mouth → BufferedPanel → ST7789
                             └──────────────────▶ MouthPanel (virtual.py) → LineReader → Mouth → Tk canvas
                                       every 80ms: Mouth.tick()
```

- **`firmware/mouth_geometry.py`** — screen size (320×240: the 240×320
  panel used sideways), colours, mouth corners, line thickness, tallest
  spike, number of spikes. The one file to change if the display turns out
  different.
- **`firmware/mouth_protocol.py`** — the wire format, parsed on the Pico and
  built on the host by the same code (see Interfaces).
- **`firmware/mouth.py`** — `Mouth` holds the state and draws:
  - `update(talking, level)` takes a command and draws nothing; the next
    `tick()` does.
  - `tick()` runs every frame (`TICK_MS`, 80ms). It eases the shown level
    towards the target (fast up, slower down) and draws a fresh, randomised
    zig-zag (`seismograph_points`): alternating up and down, each spike a
    random 35–100% of the `envelope` (a sine hump: 0 at the corners, 1 in
    the middle) times the level.
  - **Levels from the laptop** (D-024) set the target while they keep
    arriving. With none for ~320ms while talking (none sent yet, or the host
    went quiet without `S0`), it **wiggles by itself**: made-up syllables of
    2–5 frames, with the odd gap between words.
  - After `S0` it eases down to flat over a few frames, draws the flat line
    once, then stops redrawing until it talks again.
  - `draw_line` draws a thick polyline as a quad per segment plus a dot at
    every point (round joins and ends).

- **`driver.py`** — `MouthOrgan(transport)`: `start_talking()`,
  `stop_talking()`, `level(0.0–1.0)`, `update(talking, level)` in one line,
  and the bus commands `talking`, `level`, `update`.
- **`levels.py`** — `levels_from_audio(samples, sample_rate)`: speech audio
  to mouth levels, one per 1/25 s: loudness (RMS) scaled to the utterance's
  own loud parts, lifted a little for soft syllables, and 0 in gaps. Used by
  the virtual voice now and by text-to-speech later (R-307).
- **`virtual.py`** — `MouthPanel`: the same bytes in, the firmware's `Mouth`
  drawing onto any driver; also a transport, so `MouthOrgan(MouthPanel(...))`
  works. `MouthControls`: the bench's buttons (below).

Like the eyes, the drawing only needs a driver with `fill`, `fill_circle`
and `fill_polygon` (plus optional `show`), so the same code runs on the Pico
(through `organs/pico_common/framebuffer.py`), in the virtual robot and in
the tests.

## Why it's built this way

- **Seismograph, not mouth shapes:** Dan's design, 2026-11-05: it reads as
  "talking" at a glance, and it's driven by one number.
- **Levels from the laptop, not a mic on the Pico** —
  [D-024](../../docs/decisions/D-024-mouth-levels-come-from-the-laptop.md):
  the speech audio exists before it plays, and the virtual robot gets the
  same bytes.
- **Self-wiggle fallback:** the mouth moves while talking even before text-to-speech
  sends levels (R-307), or if they stop arriving.
- **80ms frames:** measured on a Pico 2, drawing a talking frame takes ~25ms
  (worst ~36ms) and pushing a full 320×240 frame takes ~31ms at 40MHz SPI.
  50ms frames didn't fit; 12.5 frames a second still follows syllables (~200ms).
- **Same patterns as the eyes:** an ASCII line protocol (D-001, newest wins),
  framebuffer + one SPI write (D-002), shared code in `organs/pico_common/`
  (D-023).

## Interfaces

**Wire format** (host → Pico, one line per update, every field optional):

| line    | meaning |
|---------|---------|
| `S1`    | start talking |
| `S0`    | stop talking: settle back to a flat line |
| `L57`   | voice level 0–100, ~25 a second while talking; ignored when not talking |
| `S1 L40`| both at once |

Reserved: `E<mood>:<intensity>` (if mood shows on the mouth) and `V`
(volume, R-306). Malformed fields are skipped; lines over 64 characters
are dropped. Nothing comes back from the Pico.

## Running and testing

- `tests/organs/test_mouth_protocol.py`: round trips, clamping, newest wins,
  malformed fields skipped.
- `tests/organs/test_mouth_firmware.py`: flat when quiet with no redraws,
  flickers every frame while talking, mouth-shaped and on screen, louder
  is taller, self-wiggle, settles back to flat.
- `tests/organs/test_micropython_compat.py` covers this firmware too.
- `tests/organs/test_mouth_levels.py`: one level per 1/25 s, loud opens and
  gaps close, scaled per utterance.
- `tests/organs/test_mouth_driver.py`: the driver's lines, bus commands,
  and the driver into the virtual panel end to end.

**See it:** `python -m virtual_robot --only mouth`. **Say it** speaks the
text box (pick a line or type one) in Qbot's real voice through the
computer's speakers, drives the mouth from that audio, and shows each
sentence as a subtitle. Without Piper it uses made-up levels and still shows
the text. **Mouth delay** delays the mouth against the sound, to tune lip-sync by
eye. **Talking** on its own makes the mouth wiggle by itself; **Hold loudness at**
sends the slider's level 25 times a second; **Command** takes raw lines
(`S1 L80`). The switch sends to the real Pico
too (see `virtual_robot/README.md`).

## Status and known gaps

- Drawing, protocol, host driver and virtual bench done and tested; frame
  time measured on a Pico 2 without a screen. **Not built yet:** ST7789
  driver, `main.py`, backlight (step 4).
- Display assumed 240×320 ST7789V(W) from listings; confirm on a breadboard.
- Polygons are most of the drawing time (~20ms). If frames need to be faster,
  try a faster SPI clock first, then cheaper line drawing.
- Mood on the mouth: waiting for Henry.
