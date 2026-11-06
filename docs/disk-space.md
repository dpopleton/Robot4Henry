# Disk space

How much disk Qbot takes, by system. Measured on the dev machine on
2026-11-05 unless marked *estimate*. Re-measure with the commands at the
bottom when something big changes (a new model, a new extra).

The robot laptop's disk size isn't recorded yet. Note it here when known.

## Summary

| System | What | Size |
|---|---|---|
| The repo itself | code, docs, `anatomy/` (CAD, PDFs), `.git` | ~12 MB |
| Brain: chat | Python deps (`ollama`, `chromadb`, `sqlalchemy`, `pyyaml`) | ~375 MB |
| Brain: chat | Ollama model in use (`llama3.2:1b`) | 1.3 GB |
| Brain: memory | Chroma's embedding model (`~/.cache/chroma`) | ~170 MB |
| Brain: memory | `storage/chroma_db` + `storage/robot.db` | <1 MB (grows with use) |
| Voice out (R-307) | `piper-tts` + `onnxruntime` | ~220 MB |
| Voice out (R-307) | Henry's voice (`storage/voices/en_GB-northern_english_male-medium.onnx`) | 63 MB |
| Voice in (Whisper) | `openai-whisper` + PyTorch **with CUDA** | ~5.8 GB |
| Voice in (Whisper) | Whisper model (`~/.cache/whisper`, not downloaded yet) | *estimate* 75 MB (tiny) – 460 MB (small) |
| Organs / hardware | `pyserial`, `mpremote` | ~1 MB |
| Tests | `pytest`, `pytest-asyncio` | ~10 MB |
| CAD (dev machine only) | `cadquery` (OCP, VTK, casadi, …) | ~1.1 GB |
| Vision (not installed) | `ultralytics` + `opencv-python` + YOLO nano model | *estimate* ~150 MB on top of PyTorch |

**What the robot needs** (chat, memory, voice in and out, organs):
about 8 GB with the CUDA build of PyTorch, or *estimate* ~3.5 GB with the
CPU-only build. CAD, the spare voices and the extra Ollama models stay on
the dev machine.

## Notes

- **PyTorch is the giant.** Whisper pulls in PyTorch, and pip's default
  Linux build bundles NVIDIA's CUDA libraries: ~4.5 GB of the 5.8 GB
  (`nvidia-*`, `triton`). The robot laptop has no GPU, so those are dead
  weight there. A CPU-only install
  (`pip install torch --index-url https://download.pytorch.org/whl/cpu`
  before the voice extra) is *estimate* ~1 GB. A smaller Whisper
  (e.g. `faster-whisper`, no PyTorch) is another option for when R-307's
  speech-in side is decided.
- **Spare voices.** `storage/voices/` holds all nine voices from the
  voice audition (571 MB). Only Henry's choice is needed; the other eight
  (~510 MB) can go once the choice is settled.
- **Ollama models** live outside the repo (`/usr/share/ollama/.ollama/models`).
  The dev machine has 11 GB of them from experiments (`qwen3:4b-instruct`
  2.5 GB, `nemotron-3-nano:4b` 2.8 GB, `phi3:mini` 2.2 GB, …). The robot
  only needs whichever model the shoot-out (R-104) picks:
  `ollama rm <name>` frees the rest.
- **Grows with use:** conversation memory (`storage/chroma_db`,
  `storage/robot.db`) and the raw conversation logs. Both tiny today.
- **PyAudio** needs the system package `portaudio19-dev` to build
  (a few MB); nothing uses it yet.

## Re-measuring

```bash
du -sh .venv storage .git ~/.cache/chroma ~/.cache/whisper ~/.cache/huggingface
du -sh /usr/share/ollama/.ollama/models && ollama list
# biggest Python packages:
python - <<'EOF'
import importlib.metadata as md, os
s = {d.metadata["Name"]: sum(os.path.getsize(d.locate_file(f)) for f in d.files or []
     if os.path.exists(d.locate_file(f))) for d in md.distributions()}
for n, b in sorted(s.items(), key=lambda x: -x[1])[:20]: print(f"{b/1e6:8.0f} MB  {n}")
EOF
```
