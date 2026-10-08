---
id: R-303
title: "Crown firmware: 4-channel USB microphone"
phase: 3
status: planned
area: crown
kind: code
depends_on: [R-301]
decisions: [D-004, D-005, D-007, D-010]
cost_gbp: null
updated: 2026-10-08
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
- [ ] Stop streaming when asleep (D-010)

## Done when
The laptop sees a 4-channel microphone and records clean audio from all four mics.

## Log
- 2026-10-08: created in the first full phase review (see journal 2026-W41).
