---
id: R-307
title: "Text-to-speech and Qbot's voice"
phase: 3
status: planned
area: organs/voice
kind: code
depends_on: []
decisions: [D-012]
cost_gbp: null
updated: 2026-10-22
---
## Goal
Local text-to-speech (e.g. Piper) on the brain computer, with a voice Henry picks.

## Why
Qbot talks back.

## Tasks
- [x] Shortlist voices (docs/henry/voices/)
- [ ] Check the chosen voice is fast enough on the robot laptop
- [x] Henry picks the voice: **`en_GB-northern_english_male-medium`**, Piper defaults, no effects (preset below)
- [ ] Tell the router while speaking (mute direction, mouth waves)
- [ ] Works in the virtual robot (D-012): speaks through the machine's own speakers, so it's built before the head's speakers exist (R-306)

## Voice preset
| Setting | Value |
|---|---|
| Model | `en_GB-northern_english_male-medium` (in `storage/voices/`) |
| Speaker | 0 (single-speaker model) |
| Length / noise / noise-w scale | Piper defaults |
| Filters | none |

## Done when
Qbot speaks its replies in Henry's chosen voice.

## Log
- 2026-10-08: created in the first full phase review (see journal 2026-W41).
- 2026-10-12: added the virtual-robot task (D-012).
- 2026-10-14: Phase 3 grill: no longer waits for the speakers — the virtual robot plays through the machine's own speakers.
- 2026-10-15: shortlist of 7 Piper voices plus 2 robot-effect variants in docs/henry/voices/ for Henry to pick on 21 Oct.
- 2026-10-15: Piper installed in .venv (voice extra); models incl. two multi-speaker ones in storage/voices/. Voice is chosen live with Henry on 21 Oct. ~0.7s per short line on the dev machine — robot laptop untested.
- 2026-10-22: Henry firmly chose voice 2, en_GB-northern_english_male-medium, as soon as he heard it. No tuning needed.
