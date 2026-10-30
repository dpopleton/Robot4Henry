---
id: D-019
title: Wire colours mean a job (power, ground, clock, data, control, select), the same on every organ
status: accepted
date: 2026-10-28
area: anatomy
---
## Context
Dan wanted the same wire colours across the whole robot, and he has six:
blue, yellow, red, black, green and white. The eyes alone need eight
wires (3V3, GND, SCK, MOSI, DC, RST and two CS lines), so a colour for
each signal can't work even for one organ.

## Decision
Each colour stands for a type of job, not one signal:

| Colour | Job | Examples |
|---|---|---|
| Red | 3.3V power | VCC |
| Red, marked or striped | 5V power | VBUS, the LED chain's 5V (D-018) |
| Black | Ground | GND |
| Yellow | Clock | SPI SCK, I²C SCL, I2S BCLK |
| Blue | Data | SPI MOSI, I²C SDA, LED DIN |
| Green | Control lines | DC, RST |
| White | Chip select / enable | CS |

If two wires on one organ share a colour, mark one of them (tape or
marker) at both ends, and say which in that part's `build.md`.

## Alternatives considered
- **One colour per signal.** Six colours run out on the eyes alone.
- **Buy more colours.** It's more to keep track of, and it still runs out
  once the crown, mouth and lights are wired.
- **No scheme.** Nothing to keep track of, but harder to trace a wire
  later, and Henry can't learn what the colours mean.

## Consequences
- Colours that share a job are picked so a swap can't hurt anything. Two
  white CS lines swapped just trade the left and right eyes. Two green
  control lines swapped just give a blank screen.
- 3.3V and 5V are both red, so the 5V marking matters: 5V on a 3.3V pin
  can damage a board.
- Each part's `build.md` wiring table lists the colour of every wire.
