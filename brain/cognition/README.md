# Cognition (thinking)

## Purpose

Qbot's conversation turn: take what Henry said, build a prompt from
Qbot's personality, mood and memories, ask the local LLM (Ollama), and
return the spoken reply plus how the exchange made Qbot feel. This is
where the other parts of the brain (memory, limbic, the session and rest
machinery) are wired together.

## How it works

```
main.py ──"text"──▶ RobotBrain.chat()
                      ├─ RawLogger.log("user", …)          (brain/raw_logger.py)
                      ├─ system prompt = personality + mood + response format
                      │                 + key facts + long-term memories + medium-term summary
                      ├─ LLMClient.chat(…, format=CHAT_RESPONSE_SCHEMA) ──▶ Ollama
                      ├─ parse_chat_response() → (reply, mood signal)
                      ├─ LimbicSystem.react(mood)            (brain/limbic/)
                      ├─ RawLogger.log("assistant", reply)
                      └─ short-term add → evicted exchange → medium-term summary
```

- **`robot_brain.py`** — `RobotBrain`:
  - `chat(text)` runs one turn. The first turn of a session starts a new
    log session and wakes the mood with a fresh random mood.
  - The **system prompt** is built every turn from: the personality, the
    current mood ("you are feeling quite curious"), the JSON response
    format, key facts, the 3 long-term memories closest to what was just
    said, and the medium-term summary. Empty sections are left out.
  - If Ollama fails, Qbot says "I'm having trouble thinking right now…",
    and that exchange is logged like any other.
  - Sessions end after 5 minutes of silence (`SessionManager`), or by
    `end_session()`. Ending one runs the **rest process** in the
    background and clears short- and medium-term memory (see
    `brain/memory/README.md`).
  - A lock (`_turn_lock`) stops the timeout ending a session in the middle
    of a turn.
  - `shutdown()` rests the last session and waits for any rest still
    running, so quitting never loses a conversation.
- **`llm_client.py`** — `LLMClient`: a thin wrapper over the Ollama
  client. `chat(system, messages, format=…)` for turns (`format` takes a
  JSON schema that constrains the model's output), `complete(prompt,
  options=…)` for one-off prompts (summaries, fact extraction).
- **`response_schema.py`** — `CHAT_RESPONSE_SCHEMA`
  (`{"reply": …, "mood": {"category", "intensity"}}`) and
  `parse_chat_response()`. A broken or missing mood just means no mood
  change this turn; a broken reply falls back to the model's raw text, so
  Henry always gets an answer.

## Why it's built this way

- **Mood comes back as structured JSON, constrained by Ollama**, not as a
  free-text "MOOD:" tag the model was asked to append: small models forget
  tags, but a schema is enforced while the model writes. More fields can
  be added to the schema later.
- **The brain only sends a mood**; what the face shows is the router's job
  ([D-008](../../docs/decisions/D-008-brain-sends-mood-router-composes-face.md)).
- **Key facts and long-term memories are built at rest, not during the
  turn**, so they cost no reply time.
- **Everything is logged before and after the LLM call**, so a crash or
  timeout never loses what Henry said.

## Interfaces

```python
from brain.cognition.robot_brain import RobotBrain

with RobotBrain() as brain:          # db_path=, chroma_path= for disposable storage in tests
    reply = brain.chat("Hello Qbot!")
    brain.limbic.current             # the mood after this turn
    brain.end_session()              # rest now (blocking=True waits for it)
```

Settings (`config/settings.py`): `PRIMARY_MODEL` (`llama3.2:1b`),
`OLLAMA_HOST`, `SESSION_TIMEOUT_SECONDS` (300), `SHORT_TERM_MAX_EXCHANGES`
(10), `LONG_TERM_RETRIEVE_COUNT` (3), `DB_PATH`, `CHROMA_PATH`.

## Running and testing

```bash
ollama serve                 # in another terminal, with the model pulled
python main.py               # chat in the terminal
python -m pytest tests/brain # fast tests, no Ollama (a fake LLM)
python -m pytest -m llm      # scenario tests against the real model (tests/scenarios/)
```

`tests/brain/test_robot_brain.py` covers the turn, logging, the LLM-failure
reply and session endings; `test_response_schema.py` the parsing.

## Status and known gaps

- Works end to end in the terminal on the dev machine.
- `_personality()` is still the old generic text. The approved character
  sheet is `brain/personality.md`; building the prompt from it is R-106.
- Reply speed on the robot laptop isn't measured yet; the target and the
  model choice come from R-105 and the model shoot-out (R-104), at the end
  of Phase 1.
- The mood isn't sent anywhere yet: that needs the router (R-207, R-208).
- Logs hold only the words, not errors, moods or timings (R-901).
