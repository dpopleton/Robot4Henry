---
id: D-010
title: Asleep means mics and cameras off; awake means it listens to everything
status: accepted
date: 2026-10-08
area: brain
---
## Context
Qbot won't run 24/7. It's for a 7-year-old and a 3-year-old, and is used
under supervision.

## Decision
A button on top of the head wakes Qbot. While awake it listens to (and,
for now, answers) everything. It goes back to sleep on the button,
"goodnight", or a silence timeout. **While asleep, the mics and cameras are
off** — the crown stops streaming and the recording LED goes out.
Transcripts are kept. Audio recordings are kept only when a debug setting
is switched on.

## Alternatives considered
- **A wake word.** Means it's always half-listening.
- **Push-to-talk.** Doesn't match how Henry wants to use it.
- **Deciding whether to reply at all.** A good later goal, but too much
  for the current small models and hardware (R-310).

## Consequences
- "Listens to everything" is limited to times someone deliberately woke it.
- Log review (R-901) covers transcripts only by default.
