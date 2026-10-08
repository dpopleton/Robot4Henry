# Limbic (mood)

## Purpose

Qbot's emotional state. A mood is a category (calm, happy, curious,
excited, sleepy, sad, scared, angry) plus an intensity of 1–3 ("a little",
"quite", "very"). The mood colours Qbot's tone in the prompt, and will drive
the face (eyes, mouth, Q colour) through the router.

## How it works

- **`mood.py`** — `Mood(category, intensity)`, a frozen dataclass that
  rejects unknown categories or out-of-range intensities. `describe()`
  turns it into prompt text ("quite curious"). `random_wake_mood()` picks a
  weighted random starting mood: mostly calm/happy/curious, mostly low
  intensity, rarely angry.
- **`state.py`** — `LimbicSystem` holds the current mood:
  - `wake()` — a fresh random mood at the start of each session.
  - `react(category, intensity)` — called once per turn with how the
    exchange felt:
    - **Same feeling** → intensity drifts one step towards the new value.
    - **Different feeling at intensity 3** → takes over outright.
    - **Different, milder feeling** → the current mood fades a notch. Once
      it's below 1, the new feeling takes over at intensity 1.

Where the per-turn signal comes from: `RobotBrain.chat()` asks the model
for JSON shaped like `{"reply": ..., "mood": {"category", "intensity"}}`
(`brain/cognition/response_schema.py`). A malformed mood just means no
change this turn — the reply is never lost.

## Why it's built this way

- **Moods drift, they don't snap.** One mildly sad message shouldn't flip
  a happy robot to sad — only a strong feeling takes over at once. That
  makes the face steady rather than flickering every turn.
- **Random wake mood** gives Qbot a bit of personality from the first
  message, weighted so it rarely wakes up grumpy.
- **Structured output, not a text tag.** Small models were unreliable at
  appending `MOOD: …` lines. A JSON schema constrains them at decode time.
- **Intensity 1–3 is shared with the eyes.** `organs/eyes/firmware/eye_protocol.py`
  has the same range, and a test checks they match.

## Interfaces

```python
from brain.limbic import LimbicSystem, Mood, CATEGORIES

limbic = LimbicSystem()
limbic.wake()                  # -> Mood
limbic.react("scared", 3)      # -> Mood (new current mood)
limbic.current.describe()      # "very scared"
```

- **Consumers:** `RobotBrain._mood_context()` (prompt) and
  `_response_format()` (category list). The router will consume it later.
- **Every category must have eye art:** `tests/organs/test_eyes_firmware.py`
  fails if a category here has no expression in `organs/eyes`.

## Running and testing

- `tests/brain/test_mood.py`, `test_limbic_state.py`,
  `test_response_schema.py` — fast unit tests.
- `python run_scenario.py mood_shifts_when_angered` — watch a mood change
  against the real model (needs `ollama serve`). Mood scenarios start from
  `SetMood(...)` rather than the random wake mood.

## Status and known gaps

- Mood isn't sent to the face yet ([R-208](../../docs/roadmap/items/R-208-brain-sends-its-mood-to-the-router.md)).
- No "activity" state yet (listening/thinking/talking/asleep) — needed for
  the antenna light and the thinking look ([R-206](../../docs/roadmap/items/R-206-thinking-look-and-backlight-dimming.md)).
- Moods don't decay over time on their own — only from conversation turns.
