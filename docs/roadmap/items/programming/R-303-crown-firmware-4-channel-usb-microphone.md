---
id: R-303
title: "Crown firmware: 4-channel USB microphone"
phase: 3
status: planned
area: crown
kind: code
depends_on: [R-301]
decisions: [D-004, D-005, D-007, D-010, D-012]
cost_gbp: null
updated: 2026-10-14
---
## Goal
C firmware (Pico SDK + TinyUSB) that makes the crown a 4-channel 16 kHz USB microphone, plus a serial port for status, and drives the recording LED whenever it's streaming.

## Why
The gate for all hearing (D-005). Starting from TinyUSB's mic examples.

## Tasks
- [ ] Toolchain + debug probe working
- [ ] PIO + DMA I2S capture of 4 mics
- [ ] USB audio class (adapt TinyUSB example)
- [ ] Composite with CDC serial
- [ ] Recording LED lit while streaming (D-007)
- [ ] Read the wake button and report it over serial, even while asleep (D-014, R-308)
- [ ] Stop streaming when asleep (D-010)
- [ ] Works in the virtual robot (D-012); decide what it fakes as input and what it only displays

## Done when
The laptop sees a 4-channel microphone and records clean audio from all four mics.

## Open questions
- Stepping stone? Raw samples over the serial port first (4 ch × 16 kHz × 16-bit
  = 128 KB/s fits easily) so direction-finding can start, then the proper USB
  audio device (D-005). Undecided.

## Log
- 2026-10-08: created in the first full phase review (see journal 2026-W41).
- 2026-10-12: added the virtual-robot task (D-012).
- 2026-10-14: Phase 3 grill: the crown Pico also reads the wake button (D-014).
