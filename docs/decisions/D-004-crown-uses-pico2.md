---
id: D-004
title: The crown mic array is built on a Pico 2 with I2S MEMS mics
status: accepted
date: 2026-10-08
area: crown
---
## Context
Direction-finding needs four mics sampled at exactly the same instant,
plus maths at audio rates and USB audio out. Dan wants to build it rather
than buy a ready-made array (fun and cost). It has to be C, not
MicroPython.

## Decision
A Raspberry Pi Pico 2 (RP2350) reading four digital I2S MEMS mics
(INMP441-type) with PIO + DMA, on one shared clock.

## Alternatives considered
- **ESP32-S3.** Faster DSP, and Espressif's speech libraries include echo
  cancellation. Heavier tooling. **Plan B** if the Pico runs out of
  processing power or echo cancellation becomes a priority.
- **STM32F411.** No real gain over the Pico 2, and clunkier tooling.
- **Teensy 4.x.** Excellent audio support, but several times the price.
- **Analog mics into the Pico's ADC.** The ADC reads one pin at a time,
  which creates its own time gaps between mics, and the Pico 2 only brings
  out three ADC pins.
- **Buying a ready-made USB mic array.** Least work, but defeats the point.

## Consequences
- Same platform as the eyes: one flashing routine and one set of docs.
- Learning C with the Pico SDK + TinyUSB. A Raspberry Pi Debug Probe
  (~£12) is worth buying.
