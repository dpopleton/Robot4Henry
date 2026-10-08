---
id: D-005
title: The crown is one USB device with separate audio and serial functions
status: accepted
date: 2026-10-08
area: crown
---
## Context
The crown has two jobs: telling the robot *where* a voice is (a few bytes,
10–30× a second) and giving speech-to-text *what* was said (continuous raw
audio). Both come from the same mics.

## Decision
The crown presents itself as a USB **composite device**: a USB microphone
(UAC, 4 channels at 16 kHz) plus a serial port (CDC) for direction and
status. Only send direction over serial if the direction maths moves onto
the Pico (see D-006).

## Alternatives considered
- **Mixing audio and direction in one serial stream.** You'd invent your
  own framing, direction would queue behind audio bytes, and the OS
  wouldn't see a microphone.
- **A separate mic for speech-to-text.** Two sets of mics hearing the same
  room, and they'd never line up.

## Consequences
- The brain computer sees an ordinary sound card — Whisper and
  `sounddevice` work with no special driver.
- Direction and audio come from one clock, so they line up exactly.
- Firmware has to be C with TinyUSB. Clock drift may cause the odd tiny
  click, which is harmless for speech-to-text.
