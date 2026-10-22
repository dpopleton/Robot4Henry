---
id: D-013
title: The head has its own USB hub and sound card; one cable bundle leaves it
status: accepted
date: 2026-10-14
area: head
---
## Context
One Pico per organ (D-009) puts 4–6 USB devices in the head (eyes, mouth,
lights, crown, perhaps a camera), and the speakers need audio from the
brain computer. Until the body exists, the brain computer is a laptop
beside the head; later it moves into the body below a neck (R-401, R-504).

## Decision
A **powered USB hub lives inside the head**. Every Pico plugs into it, and so
does a **USB sound card** that feeds the speakers' amp. Only one USB lead and
one power lead leave the head, through the bottom panel.

## Alternatives considered
- **Hub beside the laptop.** One USB lead per Pico would run out of the head:
  a thick bundle that has to pass through a turning neck later.
- **3.5 mm headphone lead from the laptop to the amp.** One more cable out of
  the head, and laptop headphone outputs often hum when shared with USB grounds.
- **An I2S amp driven by a Pico.** Another piece of firmware just to play
  sound; worth revisiting only if the mouth needs exact speech levels.

## Consequences
- The head needs its own power supply sized for the hub, amp and LEDs (R-213).
- The neck only has to pass two leads.
- The mouth's sound waves can't read levels straight off an I2S stream; they
  come from the laptop or an ADC tap on the amp input (R-210).
