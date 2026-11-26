# Memory

## Purpose

What Qbot remembers, at four time scales: the last few exchanges word for
word, a summary of earlier in this conversation, facts about Henry, and
memories from past conversations. Together they let Qbot keep track of a
conversation and remember Henry between them.

## How it works

| Layer | File | Lives | Holds | Fed by |
|---|---|---|---|---|
| Short-term | `short_term.py` | this session, in RAM | the last 10 exchanges, word for word | every turn |
| Medium-term | `medium_term.py` | this session, in RAM | a rolling summary (under 150 words) of exchanges older than that | each exchange pushed out of short-term |
| Key facts | `key_facts.py` | forever, SQLite (`storage/robot.db`) | `key: value` facts about Henry (name, likes, pets…) | the rest process |
| Long-term | `long_term.py` | forever, ChromaDB (`storage/chroma_db/`) | sentences about past conversations, searched by meaning | the rest process |

All four go into the system prompt each turn (see
`brain/cognition/README.md`); long-term only the 3 closest to what was
just said.

**A session's life:**

1. Each message is written to `raw_conversations` straight away
   (`brain/raw_logger.py`).
2. Short-term keeps the last 10 exchanges. When an 11th arrives, the
   oldest is pushed out and folded into the medium-term summary by the LLM.
3. After 5 minutes of silence (`brain/session_manager.py`), on "quit", or
   on shutdown, the session ends. Short- and medium-term are wiped.
4. **Rest** (`brain/rest_process.py`) runs in the background over every
   unprocessed session:
   - **Key facts:** the LLM lists facts from Henry's lines only, at
     temperature 0. A fact is kept only if every word of its value appears
     in what Henry actually said (D-011).
   - **Long-term:** the LLM lists up to 5 memorable sentences, stored in
     ChromaDB with the session id. They *replace* whatever that session
     stored before (ids `<session_id>-<n>`), so re-resting a session never
     leaves two sets.
   - **Archive:** a 2–3 sentence summary is saved on the session and it's
     marked processed.
5. A session interrupted part-way (a crash, a kill) is picked up by the
   next start (`recover_interrupted_sessions`), so its memories still get
   made.

## Why it's built this way

- **Short-term is exact, medium-term is cheap:** a 1B model on an old
  laptop can't take a long transcript, so older parts are squeezed into a
  summary rather than dropped.
- **Facts and memories are made at rest, not during a turn**, so they
  cost no reply time, and they work from the full, saved transcript.
- **Key facts are checked against Henry's own words**, not by asking the
  model whether they're true: the model invented favourites and a yes/no
  check was close to a coin flip
  ([D-011](../../docs/decisions/D-011-key-facts-grounded-by-word-match.md)).
- **ChromaDB for long-term**, so memories are found by meaning ("dinosaurs"
  finds "Henry loves the T. rex"), not by matching words.
- **Medium-term is wiped at session end:** what mattered has gone into key
  facts and long-term by then.

## Interfaces

```python
from brain.memory.short_term import ShortTermMemory
from brain.memory.medium_term import MediumTermMemory
from brain.memory.key_facts import KeyFactsStore
from brain.memory.long_term import LongTermMemory

short = ShortTermMemory()                  # add(role, text) returns an evicted exchange or None
medium = MediumTermMemory(llm)             # update(evicted), format_for_prompt(), clear()
facts = KeyFactsStore(db_path)             # set/get/delete/get_all, format_for_prompt()
memories = LongTermMemory(chroma_path)     # replace_session(id, texts, metadata), store(text, metadata), retrieve(query, n)
```

`DB_PATH` and `CHROMA_PATH` (`config/settings.py`) can be overridden with
`QBOT_DB_PATH` / `QBOT_CHROMA_PATH`, so tests and tools use disposable
storage.

## Running and testing

```bash
python -m pytest tests/brain     # each layer, rest, the raw logger and sessions (fake LLM)
python -m pytest -m llm          # scenario tests: does Qbot remember across sessions with the real model
```

`tests/test_storage_isolation.py` checks tests never touch the real
`storage/`; `tests/test_wipe_memory.py` covers wiping Qbot's memory.

## Status and known gaps

- All four layers and rest work on the dev machine.
- Rest is safe alongside a conversation: an `RLock` guards each shared
  SQLite connection, and `tests/brain/test_rest_concurrency.py` runs rest
  in the background during a conversation, two rests at once, and a
  re-rest after a crash, against real SQLite and ChromaDB (R-110).
- Long-term memories have stable ids per session and a re-rest replaces
  them. Memories stored before this (2026-11-23) keep their random ids;
  their sessions are already processed, so they're never re-rested.
- `LongTermMemory` takes an `embedding_function`; tests pass a fake
  (`tests/brain/fake_embedding.py`) so they need no embedding model.
- Nothing is backed up: `storage/` is gitignored and lives only on the
  laptop (R-906).
- Rest uses the same small model as conversation; a bigger rest model is
  a question for the model shoot-out (R-104).
