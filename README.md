# Robot4Henry 🤖

A locally-run AI brain for a child's companion robot. Built as a father-son project, 
Qbot is designed to be a friendly, safe, and memory-aware conversational robot companion 
for young children. Everything runs on your own hardware — no cloud, no subscriptions, 
no data leaving your home.

---

## What is this?

Qbot is the software brain for a physical robot companion. At its core it is a 
conversational AI with a multi-layered memory system that lets the robot remember 
your child across sessions — their name, their pets, their interests, and the 
conversations you have had together.

This repository contains Phase 1 of the project: the conversational brain and 
memory system. Future phases will add voice, emotional expression, vision, and 
physical movement.

### Current features
- Friendly, child-appropriate conversational AI
- Short term memory (current conversation, verbatim)
- Medium term memory (older exchanges compressed within a session)
- Long term memory (built during rest periods, persists across sessions)
- Mood (`brain/limbic`) — a randomised wake-up mood that drifts turn to turn based on the conversation, colouring Qbot's tone
- Session management with automatic reset after inactivity
- Full conversation logging for debugging and memory review
- Memory wipe utility for testing and reset

---

## Hardware requirements

**Minimum:**
- 8GB RAM
- Modern CPU (Intel i5 / AMD Ryzen 5 or better)
- 10GB free disk space (for OS, code, and models)
- Ubuntu 22.04 LTS (recommended) or any Linux distribution

**Recommended:**
- 16GB RAM
- AMD Ryzen 7 / Intel i7 or better
- SSD storage

**Note:** No GPU required. Everything runs on CPU via Ollama. 
A dedicated GPU will significantly improve response speed if available.

---

## Software requirements

- Python 3.10 or higher
- [Ollama](https://ollama.com) (local LLM runtime)
- Git

---

## Installation

### Step 1 — Install system dependencies

```bash
sudo apt update && sudo apt upgrade -y

sudo apt install -y \
  python3 python3-pip python3-venv \
  git build-essential cmake \
  ffmpeg portaudio19-dev \
  sqlite3 curl
```

### Step 2 — Install Ollama

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Verify it is running:

```bash
ollama --version
systemctl status ollama
```

### Step 3 — Pull the language model

```bash
ollama pull llama3.2:1b
```

This downloads approximately 1.3GB. On a slower connection this may take a few minutes.

You can verify the model is available:

```bash
ollama list
```

### Step 4 — Clone the repository

```bash
git clone https://github.com/dpopleton/Robot4Henry.git
cd Robot4Henry
```

### Step 5 — Create Python environment

```bash
python3.10 -m venv .venv
source .venv/bin/activate
```

### Step 6 — Install Python dependencies

```bash
pip install --upgrade pip
pip install -e ".[dev]"
```

### Step 7 — Create storage directories

```bash
mkdir -p storage/chroma_db
```

### Step 8 — Verify installation

```bash
python -m pytest tests/ -v
```

All tests should pass. You are ready to run Qbot.

---

## Running Qbot

```bash
source .venv/bin/activate
python main.py
```

You should see:

```
Qbot is ready. Type 'quit' to exit.

You: 
```

Start talking. Type `quit` or `exit` to stop, or press `Ctrl+C`.

---

## How the memory system works

Qbot has three layers of memory:

**Short term** — the current conversation, kept verbatim. Qbot remembers 
everything said in the current session exactly. After 10 exchanges older 
messages are compressed into medium term memory.

**Medium term** — a rolling summary of older exchanges within the current 
session. Keeps the context of a long conversation without overwhelming the 
model. Wiped at session end.

**Long term** — built during rest periods after a session ends. Memorable 
facts and moments are extracted from the raw conversation log and stored 
in a vector database. Retrieved semantically when relevant in future sessions.

**Session reset** — after 5 minutes of inactivity Qbot considers the 
conversation over, clears short and medium term memory, and processes 
the session into long term memory. The next conversation starts fresh 
while still having access to long term memories from previous sessions.

---

## Memory management

A utility script is included for wiping memory during testing or resetting Qbot:

```bash
# Wipe everything (recommended for a clean start)
python wipe_memory.py

# See what would be wiped without doing it
python wipe_memory.py --dry-run

# Wipe long term memory only
python wipe_memory.py --long-term-only

# Wipe key facts only
python wipe_memory.py --facts-only
```

---

## Testing

There are two tiers:

**Fast unit tests** — pure logic, no LLM calls, run in a few seconds:

```bash
python -m pytest tests/ -v
```

**Scenario tests** — full multi-turn conversations against the real model
(needs `ollama serve` running), checking internal state (mood, long term
memory) rather than parsing the reply text, since the model's exact
wording changes between runs but whether a fact got stored/recalled or a
mood actually shifted does not. Excluded from the default run above via
the `llm` pytest marker:

```bash
python -m pytest -m llm -v
```

Or run one interactively and watch it play out turn by turn:

```bash
python run_scenario.py --list
python run_scenario.py remembers_name_across_sessions
python run_scenario.py mood_shifts_when_angered
python run_scenario.py mood_shifts_when_angered --real-storage  # uses storage/ instead of a disposable temp dir
```

Scenarios live in `tests/scenarios/conversations.py` as plain lists of
steps (`Say`, `EndSession`, `Restart`, `SetMood`, `ExpectReplyContains`,
`ExpectMood`, `ExpectLongTermRecall` — see `tests/scenarios/steps.py`).
Add a new one there and it's picked up by both the pytest suite and
`run_scenario.py` automatically. Two things worth knowing when writing
new ones:

- `rest_process.py` only builds long term memories from a conversation
  with 4+ logged lines (roughly 2+ exchanges) — a single message won't
  get remembered no matter how memorable.
- Mood assertions should start from `SetMood(...)` rather than the
  random wake mood — moods drift/fade rather than snap, so checking an
  exact category against an unknown random starting point isn't a fair
  test.

---

## Configuration

All configuration lives in `config/settings.py`:

```python
# Which model to use
PRIMARY_MODEL = "llama3.2:1b"

# How many recent exchanges to keep verbatim
SHORT_TERM_MAX_EXCHANGES = 10

# Minutes of inactivity before session resets
SESSION_TIMEOUT_SECONDS = 300  # 5 minutes

# How many long term memories to retrieve per turn
LONG_TERM_RETRIEVE_COUNT = 3
```

### Trying a different model

Different models offer different tradeoffs between speed and quality. 
To try a different model:

```bash
# Pull the model
ollama pull qwen3.5:0.8b

# Update config/settings.py
PRIMARY_MODEL = "qwen3.5:0.8b"
```

General guidance for model selection:

| Model | Size | Speed | Quality | Notes |
|---|---|---|---|---|
| llama3.2:1b | 1.3GB | Fast | Good | Default, recommended for 8GB RAM |
| qwen3.5:0.8b | 1.0GB | Very fast | Good | Smallest option, add /no_think to prompts |
| llama3.2:3b | 2.0GB | Medium | Better | Recommended for 16GB RAM |
| qwen3.5:2b | 2.7GB | Medium | Better | Good balance for 16GB RAM |

---

## Project structure

The layout mirrors biology: a **brain** for cognition and memory, a
**nervous system** carrying messages, and **organs** for each physical
subsystem. The brain never talks to hardware directly — it sends
abstract commands ("blink", "set_expression: curious") through the
nervous system, which routes them to the right organ's driver. Organs
without hardware yet register a mock driver, so the brain and its
tests never depend on anything being plugged in.

```
Robot4Henry/
├── brain/                       # cognition, personality, memory
│   ├── cognition/
│   │   ├── llm_client.py          # Ollama API wrapper
│   │   └── robot_brain.py         # Main brain, wires everything together
│   ├── memory/
│   │   ├── short_term.py           # In-memory conversation buffer
│   │   ├── medium_term.py          # Within-session rolling summary
│   │   ├── long_term.py            # ChromaDB vector store
│   │   └── key_facts.py            # Structured fact store (reserved for future use)
│   ├── limbic/
│   │   ├── mood.py                 # Mood(category, intensity) + random wake mood
│   │   ├── state.py                # LimbicSystem — how mood drifts turn to turn
│   │   └── parsing.py              # extracts the model's trailing MOOD tag
│   ├── session_manager.py         # Inactivity detection, session lifecycle
│   ├── raw_logger.py              # Logs every exchange to SQLite
│   └── rest_process.py            # Builds long term memory after sessions
│
├── nervous_system/               # comms fabric between brain and organs
│   ├── protocol.py                 # shared message format (organ, cmd, payload)
│   ├── serial_transport.py          # USB serial transport (pyserial)
│   └── bus.py                       # organ registry, routes brain commands
│
├── organs/                        # one folder per physical subsystem
│   ├── base.py                      # Organ interface + MockOrgan for dev/tests
│   └── eyes/                        # LCD screens on a Raspberry Pi Pico
│       ├── firmware/                  # MicroPython, runs on the Pico
│       ├── driver.py                   # host-side driver, speaks the protocol
│       └── README.md                   # wiring/pinout/flashing notes
│
├── config/
│   └── settings.py                # All configuration
├── storage/
│   ├── chroma_db/                 # Long term vector memory (gitignored)
│   └── robot.db                   # SQLite database (gitignored)
├── tests/
│   ├── brain/
│   ├── nervous_system/
│   └── organs/
├── main.py                        # Entry point
├── wipe_memory.py                 # Memory reset utility
└── pyproject.toml                 # Package configuration
```

---

## Troubleshooting

**Qbot takes a very long time to respond**

The model may be too large for available RAM. Check memory usage:

```bash
free -h
```

If available memory is under 2GB, switch to a smaller model:

```bash
ollama pull llama3.2:1b
# Set PRIMARY_MODEL = "llama3.2:1b" in config/settings.py
```

**Ollama not found or not running**

```bash
# Check status
systemctl status ollama

# Start if not running
sudo systemctl start ollama

# Enable on boot
sudo systemctl enable ollama
```

**Model not found error**

```bash
# Verify model is pulled
ollama list

# Pull again if missing
ollama pull llama3.2:1b
```

**Tests failing with SQLite errors**

```bash
mkdir -p storage
```

**ChromaDB errors on startup**

```bash
rm -rf storage/chroma_db
mkdir storage/chroma_db
```

---

## Roadmap

This project is being built in phases:

- ✅ **Phase 1** — Conversational brain with memory system
- 🟡 **Phase 2** — Emotional state and expression simulator: mood tracking (`brain/limbic`) done; driving `organs/eyes`/`organs/mouth` over `nervous_system` still to come
- 🔲 **Phase 3** — Voice (`organs/ears` for speech recognition, `organs/voice` for text-to-speech)
- 🔲 **Phase 4** — Safety layer and child-specific tuning
- 🔲 **Phase 5** — Hardware integration (laptop into robot chassis)
- 🔲 **Phase 6** — Vision and scene understanding
- 🔲 **Phase 7** — Navigation and movement (`organs/locomotion`)
- 🔲 **Phase 8** — Full robot integration and polish

---

## Philosophy

Everything in this project runs locally. No API keys, no cloud services, 
no subscriptions. Your child's conversations stay on your hardware.

The robot is designed for children — safety, warmth, and age-appropriate 
responses are built into the personality from the ground up, not bolted on afterwards.

This is a father-son project. Expect it to grow organically, prioritise 
fun over perfection, and value learning over shipping.

---

## Contributing

This is a personal project but questions and suggestions are welcome via issues. 
If you are building something similar for your own child, we would love to hear about it.

---

## Licence

MIT — do whatever you like with it, build something wonderful for your kids.