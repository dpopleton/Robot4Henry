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
updated: 2026-10-08
---
## Goal
A "thinking" look while the LLM is working, and dimmer backlight for sleepy/sleeping.

## Why
chat() takes seconds — the eyes should show Qbot is thinking rather than freeze. The backlight is already PWM-controlled.

## Tasks
- [ ] Design the thinking look (glance up-and-aside? animated?)
- [ ] Backlight level per expression in REGISTRY
- [ ] Activity 'thinking' sent by the router

## Done when
The eyes visibly think during a reply and dim when sleepy.

## Log
- 2026-10-08: created in the first full phase review (see journal 2026-W41).
