---
id: R-206
title: "Thinking look and backlight dimming"
phase: 2
status: planned
area: organs/eyes
kind: code
depends_on: [R-207]
decisions: []
cost_gbp: null
updated: 2026-10-28
---
## Goal
A "thinking" look while the LLM is working, and dimmer backlight for sleepy/sleeping.

## Why
chat() takes seconds — the eyes should show Qbot is thinking rather than freeze. The firmware already drives a PWM backlight on GP22, but the eyes are being wired without a backlight wire (BLK unconnected, so always full brightness). Dimming needs that wire added.

## Tasks
- [ ] Design the thinking look (glance up-and-aside? animated?)
- [ ] Wire BLK to GP22 (check the boards have an onboard backlight driver first)
- [ ] Backlight level per expression in REGISTRY
- [ ] Activity 'thinking' sent by the router

## Done when
The eyes visibly think during a reply and dim when sleepy.

## Log
- 2026-10-08: created in the first full phase review (see journal 2026-W41).
- 2026-10-28: eyes wired without the backlight wire (anatomy/eyes/build.md), so dimming now needs BLK wired first.
