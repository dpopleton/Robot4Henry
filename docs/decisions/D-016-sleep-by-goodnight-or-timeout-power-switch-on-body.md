---
id: D-016
title: The button only wakes Qbot; he sleeps on "goodnight" or a timeout, and the body has an on/off switch
status: accepted
date: 2026-10-22
area: brain
supersedes: D-010
---
## Context
D-010 had one button both waking Qbot and putting him to sleep. Since then
the big button on top of the head has become the wake button (D-015), and a
press while awake is also meant to be a pat on the head (R-313). One button
with three meanings needs press-length rules that a 3-year-old won't follow.

## Decision
Everything in D-010 still holds except how Qbot goes to sleep:

- The **big button on top of the head wakes Qbot** (D-015). While awake, a
  press is a **pat**; it never puts him to sleep.
- He **goes to sleep on "goodnight" or a silence timeout** — no sleep button.
- While awake he listens to (and, for now, answers) everything.
- **While asleep, the mics and cameras are off**: the crown stops streaming
  and the recording LED goes out.
- Transcripts are kept. Audio recordings are kept only when a debug setting
  is switched on.
- To switch Qbot off completely, the **body gets an on/off switch** (R-502).
  Until the body exists, that means quitting or unplugging.

## Alternatives considered
- **Short press = pat, long press = sleep.** Works, but it's a hidden rule,
  and an accidental long press puts him to sleep mid-conversation.
- **A separate sleep button.** One more part, when "goodnight" and the
  timeout already cover it.
- From D-010: a wake word (always half-listening), push-to-talk (not how
  Henry wants to use it), deciding whether to reply (too much for the
  current models, R-310).

## Consequences
- "Listens to everything" is still limited to times someone deliberately woke him.
- If "goodnight" isn't recognised, he stays awake until the timeout. Speech
  recognition has to catch it reliably (R-304).
- Log review (R-901) covers transcripts only by default.
