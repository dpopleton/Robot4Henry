# Pico common

## Purpose

Firmware code shared by every organ's Pico: drawing into a RAM framebuffer
and reading command lines from USB serial. Written once here, used by the
eyes now and the mouth next (R-210), rather than copied into each organ.

## How it works

- **`framebuffer.py`** — `BufferedPanel(panel, buf=None)`: draws shapes
  (`fill`, `fill_circle`, `fill_polygon`) into a RAM frame with MicroPython's
  built-in `framebuf`, and `show()` pushes the whole frame to the panel in
  one SPI write (`panel.blit(buf)`). Two panels can share one buffer if each
  renders and shows in turn, as the eyes do. Pico-only (needs `framebuf`).
- **`line_reader.py`** — `LineReader(stream, max_line)`: `wait(ms)` sleeps
  until input arrives; `drain(on_line)` calls `on_line(line)` for every
  complete line already waiting, reading at most 512 characters per call so
  a flood can't starve redraws. Lines over `max_line` are dropped whole.
  `feed(ch, on_line)` is the line-splitting on its own, for tests.

On the Pico these files sit flat in the root next to the organ's own
firmware and are imported by bare name (`from line_reader import LineReader`).
`organs/deploy.py <organ>` copies both folders and refuses if a file name
is in both.

## Why it's built this way

- **Shared, not copied:** the mouth needs exactly the same pieces as the
  eyes (D-023). Copies would drift apart, and a fix in one would miss the other.
- **Flat on the Pico:** MicroPython imports from the root, and the organ
  code already imports its own files by bare name, so the shared files
  join them there rather than in a package.
- Framebuffer rendering: [D-002](../../docs/decisions/D-002-eyes-framebuffer-rendering.md).

## Interfaces

```python
from framebuffer import BufferedPanel
from line_reader import LineReader

panel = BufferedPanel(gc9a01_or_st7789_panel)   # needs WIDTH, HEIGHT, blit(buf)
reader = LineReader(sys.stdin, max_line=64)
reader.wait(150)
reader.drain(update.merge_line)
```

## Running and testing

- `tests/organs/test_line_reader.py` — line splitting, overlong lines, and
  `drain` against a real pipe.
- `tests/organs/test_micropython_compat.py` — no CPython-only `math` here or
  in any organ's firmware.
- `framebuffer.py` only runs on a Pico; check it there with the organ's
  side-by-side simulator.

## Status and known gaps

- Used by the eyes (tested on the real Pico 2 on 2026-11-05); the mouth is next.
- `BufferedPanel` has no line or text drawing yet. The mouth's seismograph
  may need lines (`framebuf.line` is one pixel wide).
