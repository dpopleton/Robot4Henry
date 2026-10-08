---
id: D-007
title: Recording/video indicator LEDs are driven by the hardware they report on
status: accepted
date: 2026-10-08
area: head
---
## Context
The head has "recording on" and "video on" lights. If they were driven by
the lights Pico on the brain's say-so, a software bug could leave the mics
or camera running with the light off.

## Decision
The **crown Pico** drives the recording LED, lit whenever it's actually
streaming audio. The video LED is driven by the camera's own power or its
Pico. The Q and antenna lights are separate and fed by the router.

## Consequences
- The lights can't lie: on if and only if audio/video is leaving the device.
- Each indicator needs a pin on its own organ's Pico — plan for it when
  wiring the crown and camera.
