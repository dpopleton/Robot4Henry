---
id: D-021
title: Wire colours still mean a job, but with ten colours 5V gets orange and each pair gets a look-alike second colour
status: accepted
date: 2026-11-04
area: anatomy
supersedes: D-019
---
## Context
D-019 gave each wire colour a job, using the six colours Dan had then.
That needed tape or marker on shared colours, and 3.3V and 5V were both
red, which D-019 itself flagged as the risky part. The wire Dan bought
turned out too thick for the eyes' connectors, so he used thinner wire
he already had. It comes in ten colours: white, grey, purple, blue,
green, yellow, orange, red, black and brown.

## Decision
Colours still mean a job, the same on every organ. The extra colours do
three things: 5V gets its own colour, each job that often comes in twos
gets a second colour that looks like it belongs with the first, and
brown is kept spare.

| Colour | Job | Examples |
|---|---|---|
| Red | 3.3V power | VCC, 3V3(OUT) |
| Orange | 5V power (only 5V) | VBUS, the LED chain's 5V (D-018) |
| Black | Ground | GND |
| Yellow | Clock | SPI SCK, I²C SCL, I2S BCLK |
| Blue | Data | SPI MOSI, I²C SDA, LED DIN |
| Green | Control | DC |
| Purple | Control (second) | RST |
| White | Chip select / enable | CS (first, e.g. left eye) |
| Grey | Chip select / enable (second) | CS (second, e.g. right eye) |
| Brown | Spare | Kept for whatever the crown's four I2S mics need (R-301) |

Rule for Henry: light colours (white, grey) pick which one; red is
power, orange is strong power; black is ground.

If an organ still needs more wires of one job than there are colours,
mark the extra ones (tape or marker) at both ends and say which in that
part's `build.md`, as before.

## Alternatives considered
- **Keep D-019 unchanged.** It works, but keeps 5V and 3.3V both red,
  and keeps the marked wires.
- **One colour per signal.** Ten colours is enough for the eyes, but not
  for the whole robot, and the colours would stop meaning anything.
- **Use orange for something else and keep 5V as marked red.** That
  leaves the one swap that can damage a board relying on a marking.

## Consequences
- 5V on a 3.3V pin is the only colour swap that could do damage, and it
  now needs two clearly different colours to be confused.
- The eyes need no marked wires. Swapping white and grey swaps the left
  and right eyes; swapping green and purple gives a blank screen.
  Neither does any damage.
- Brown is spare. If the crown needs it, decide its job then.
- Each part's `build.md` wiring table lists the colour of every wire.
